from flask import (Blueprint, request, render_template as render, current_app,
    redirect, flash, url_for )
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_mail import Message 
from flask_login import login_user, logout_user, login_required, current_user
from ..extensions import db, mail
from ..models.users import Users
from ..models.servers import Servers
from werkzeug.utils import secure_filename
from PIL import Image
import os

bp = Blueprint('auth', __name__, url_prefix='/auth')

UPLOAD_FOLDER = 'static/uploads/profiles'

@bp.route('/')
def index_auth():
    return render('auth/auth_home.html')

@bp.route('/<int:id>')
def user_profile(id):
    user = Users.query.get(id)
    if not user:
        flash("해당 사용자가 없습니다.")
        return redirect(url_for("auth.register_users")), 404
    if user.is_admin:
        users = Users.query.all()
        return render("auth/user_profile.html", profiles=users, profile=None)
    return render("auth/user_profile.html", profile=user, profiles=None)

def save_resized_picture(form_picture):
    """Resizes and saves an uploaded picture."""
    filename = secure_filename(form_picture.filename)
    upload_path = os.path.join(current_app.root_path, UPLOAD_FOLDER)
    os.makedirs(upload_path, exist_ok=True)
    
    # Resize image
    output_size = (64, 64)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    
    picture_path = os.path.join(upload_path, filename)
    img.save(picture_path)
    
    return f'/{UPLOAD_FOLDER}/{filename}'

@bp.route('/register', methods=['GET','POST'])
def register_users():
    if request.method == 'GET':
        return render('auth/register.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # A checkbox will be in the form data if it was checked, otherwise it won't.
        is_admin = 'is_admin' in request.form

        user = Users.query.filter_by(username=username).first()

        profile_image_uri = '/static/image/default.jpg' # Default image
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and file.filename != '':
                profile_image_uri = save_resized_picture(file)
        
        if user:
            flash(f'User {username} is already registered.')
            return render('auth/register.html')
        if confirm_password != password:
            flash('암호가 일치하지 않습니다.')
            return render('auth/register.html')
        
        else:
            user = Users(username=username, email=email, 
                    is_admin=is_admin, profile_image=profile_image_uri)
            user.set_password(password)
            user.check_password(password)
            db.session.add(user)
            db.session.commit()

            flash('사용자가 추가되었습니다.!')
            return redirect(url_for('auth.login_users'))

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_user(id):
    user = db.session.get(Users, id)
    if not user:
        flash("해당 사용자가 없습니다.")
        return redirect(url_for("auth.register_users")), 404
    if not (current_user.is_admin or user.id == current_user.id):
        flash("수정할 권한이 없습니다.")
        return redirect(url_for("auth.register_users"))
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")

        edit_user = Users.query.filter_by(username=username).first()
        user_email = Users.query.filter_by(email=email).first()
        
        if edit_user.email == email:
            pass
        elif user_email:
            flash(f"해당 '{email}'은 이미 등록되어 있습니다.")
            return render("auth/user_edit.html", profile=user_email)
        edit_user.email = email

        db.session.commit()

        if 'profile_image' in request.files:
            file = request.files['profile_image']
            print(file)
            if file and file.filename != '':
                user.profile_image = save_resized_picture(file)

        db.session.commit()
        flash("사용자 정보가 수정되었습니다.")
        return redirect(url_for("auth.user_profile", id=current_user.id))
    else:
        return render("auth/user_edit.html", profile=user)

@bp.route('/login', methods=['GET','POST'])
def login_users():
    if request.method == 'GET':
        return render('auth/login.html')
    elif request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        error = None
        user = Users.query.filter_by(username=username).first()
        if user is None:
            error = '사용자 명을 확인하세요.'
        elif not check_password_hash(user.password, password):
            error = '암호를 확인하세요.'
        
        if error is None:
            login_user(user)
            flash(f'안녕하세요 😊 {user.username} 님!')
            return redirect(url_for('auth.user_profile', id=user.id))
        
        else:
            flash(error)
            return render('auth/login.html')

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.index_auth'))

@bp.route("/<int:id>/manage_server", methods=["GET", "POST"])
@login_required
def manage_server(id):
    servers = db.session.query(Servers).all()
    user = db.session.query(Users).filter_by(id=id).first_or_404()

    if request.method == "POST":
        # user에서 operator IDs를 통해 해당 리스트를 검색
        server_ids = request.form.getlist("allowed_servers")
        managed_servers = db.session.query(Servers)\
            .filter(Servers.id.in_(server_ids)).all()
        user.allowed_servers = managed_servers

        db.session.commit()
        flash(f"User '{user.username}' managed servers updated successfully.")
        return redirect(url_for("auth.user_profile", id=current_user.id))
    return render("auth/manage_server.html", user=user, servers=servers)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_server(id):
    if request.method == "POST":
        user = db.session.query(Users).filter_by(id=id).first()
        if user.is_admin:
            flash("관리자 계정은 삭제할 수 없습니다.")
            return redirect(url_for("auth.index_auth"))
        if current_user.id != user.id and not current_user.is_admin:
            flash("다른 사용자의 계정을 삭제할 권한이 없습니다.")
            return redirect(url_for("auth.index_auth"))
        if current_user.id == user.id or current_user.is_admin:
            db.session.delete(user)
            db.session.commit()
        return redirect(url_for("auth.index_auth"))
    elif request.method == "GET":
        user = db.session.query(Users).filter_by(id=id).first()
        return render("auth/user_delete.html", user=user)
# ============= 암호 변경 기능 =============================
def get_reset_token(user_id):
    s = Serializer(current_app.config.get('SECRET_KEY'))
    # TimedJSONWebSignatureSerializer(deprecated) 에서 expiration을 넣던게 없어짐
    # URLSafeTimedSerializer에서는 기본이 text로 decode('utf-8') 없어짐
    return s.dumps({ 'user_id': user_id })

def verify_reset_token(token):
    s = Serializer(current_app.config.get('SECRET_KEY'))
    try:
        # URLSafeTimedSerializer는 여기서 expiration을 설정 108초 이상
        user_id = s.loads(token, max_age=1800)['user_id']
    except:
        return None
    return Users.query.get(user_id)

def send_email(user):
    token = get_reset_token(user.id)
    msg = Message('Reset Your Password', 
                    recipients=[user.email], 
                    sender=current_app.config.get('MAIL_USERNAME') or 'noreply@demo.com')
    msg.body = f''' 패스워드 초기화하려면 아래 링크를 클릭하세요.
{url_for('auth.reset_with_token', token=token, _external=True)}
이 메일을 요청하지 않았으면 무시하세요.'''
    mail.send(msg)

@bp.route('/reset_password', methods=['GET','POST'])
def reset_password():
    if request.method == 'GET':
        return render('auth/reset_request.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        user = Users.query.filter_by(email=email).first()
        if user is None:
            flash('해당 email에 해당하는 유저가 없습니다.')
            return render('auth/reset_request.html')

        send_email(user)
        flash('A password reset link has been sent to your email address.')
        return redirect(url_for('auth.login_users'))

@bp.route('/reset_password/<token>', methods=['GET','POST'])
def reset_with_token(token):
    user = verify_reset_token(token)
    if user is None:
        flash('해당 토큰은 유효하지 않습니다.')
        return redirect(url_for('auth.reset_password'))
    if request.method == 'GET':
        return render('auth/reset_with_token.html', token=token)
    elif request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('암호가 일치하지 않습니다..')
            return render('auth/reset_with_token.html', token=token)
        
        user.password = generate_password_hash(password)
        db.session.commit()
        flash('암호가 재 설정되었습니다..')
        return redirect(url_for('auth.login_users'))
