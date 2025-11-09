from flask import (
  Blueprint, request, redirect, 
  render_template as render, flash, url_for) # type: ignore
from flask_login import current_user, login_required # type: ignore
from ..extensions import db
from ..models.servers import Servers
from ..models.users import Users
from .pagenation import pagenation
from sqlalchemy import or_, and_, cast, String # type: ignore

bp = Blueprint("servers_infos", __name__, url_prefix="/health/servers")

@bp.route("/")
def index():
    search_name = request.args.get('server_name', '')
    search_ip = request.args.get('ip_address', '')
    search_user = request.args.get('user', '')

    query = db.session.query(Servers)
    # ========== Search Logic ==========
    # user을 선택한 상태에서 search_name이나 ip_address를 검색하면 and 조건으로 검색
    # user만 선택한 상태에서는 user으로만 검색
    # server_name이나 ip_address만 검색한 상태에서는 or 조건으로 검색
    # INET 형태의 ip_address cast를 통해 String으로 변환 후에 검색
    if search_user and not (search_name or search_ip):
        query = query.join(Servers.operators).filter(Users.username == search_user)
    elif  search_user and (search_name or search_ip):
        filter = []
        if search_name:
            filter.append(Servers.server_name.ilike(f'%{search_name}%'))
        if search_ip:
            filter.append(cast(Servers.ip_address, String).ilike(f'%{search_ip}%'))
        query = query.join(Servers.operators)\
            .filter(Users.username == search_user)\
                .filter(or_(*filter))

    if search_name or search_ip:
        filter = []
        if search_name:
            filter.append(Servers.server_name.ilike(f'%{search_name}%'))
        if search_ip:
            filter.append(cast(Servers.ip_address, String).ilike(f'%{search_ip}%'))
        query = query.filter(or_(*filter))
    # ========== end Search Logic ==========    

    pagination_data = pagenation(query, per_page=10, orders=Servers.id.desc())
    current_user_id = current_user.get_id()
    server_list_by_user = db.session.query(Servers)\
        .join(Servers.operators)\
        .filter(Users.id == current_user_id).all()
    users = db.session.query(Users).all()

    return render("health/servers/index.html", 
        server_list_by_user=server_list_by_user,          
        servers=pagination_data['query_result'], 
        users=users,
        pagenation = pagination_data,
        )

@bp.route("/create", methods=["GET", "POST"])
@login_required
def create_server():
    if request.method == "POST":
        server_name = request.form.get("server_name")
        login_id = request.form.get("login_id")
        ip_address = request.form.get("ip_address")
        port = request.form.get("port")
        password = request.form.get("password")

        if not port:
            port = 22

        if not ip_address or not login_id or not server_name:
            flash("IP 주소, 로그인 ID, 서버 이름은 필수입니다.")
            return render(url_for("servers_infos.create_server"))
        query_existing = db.session.query(Servers).filter_by(ip_address=ip_address).first()
        if query_existing:
            flash("이미 존재하는 서버입니다.")
            return render(url_for("servers_infos.create_server"))

        new_server = Servers(server_name=server_name, login_id=login_id, ip_address=ip_address, port=port, password=password)

        # Get operator IDs from the form and fetch user objects
        operator_ids = request.form.getlist("operators")
        if operator_ids:
            operators = db.session.query(Users).filter(Users.id.in_(operator_ids)).all()
            new_server.operators = operators

        db.session.add(new_server)
        db.session.commit()
        flash(f"Server '{new_server.server_name}' created successfully.")
        return redirect(url_for("servers_infos.index"))
    else:
        users = db.session.query(Users).all()
        return render("health/servers/create_server.html", users=users)

@bp.route("/<int:id>/edit", methods=["GET", "POST"])
@login_required
def edit_server(id):
    server = db.session.query(Servers).filter_by(id=id).first_or_404()
    users = db.session.query(Users).all()

    if request.method == "POST":
        server_name = request.form.get("server_name")
        login_id = request.form.get("login_id")
        ip_address = request.form.get("ip_address")
        port = request.form.get("port")
        password = request.form.get("password")

        if not port:
            port = 22

        if not ip_address or not login_id or not server_name:
            flash("IP 주소, 사용자 이름, 서버 이름은 필수입니다.")
            return render(url_for("servers.edit_server"))
        if server.ip_address != ip_address:
            query_existing = db.session.query(Servers).filter_by(ip_address=ip_address).first()
            if query_existing:
                flash("해당 IP 주소로 등록된 서버가 이미 존재합니다.")
                return render("health/servers/edit_server.html", users=users, server=server)

        server.server_name = server_name
        server.login_id = login_id
        server.ip_address = ip_address
        server.port = port
        server.password = password

        # user에서 operator IDs를 통해 해당 리스트를 검색
        operator_ids = request.form.getlist("operators")
        operators = db.session.query(Users).filter(Users.id.in_(operator_ids)).all()
        server.operators = operators

        db.session.commit()
        flash(f"Server '{server.server_name}' updated successfully.")
        return redirect(url_for("servers_infos.index"))
    return render("health/servers/edit_server.html", users=users, server=server)

@bp.route("/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_server(id):
    if request.method == "POST":
        server = db.session.query(Servers).filter_by(id=id).first()
        db.session.delete(server)
        db.session.commit()
        return redirect(url_for("servers_infos.index"))
    else:
        server = db.session.query(Servers).filter_by(id=id).first()
        return render("health/servers/delete_server.html", server=server)
