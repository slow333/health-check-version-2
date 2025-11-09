from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from werkzeug.utils import secure_filename
from app.extensions import db
from ..models.images import Images

bp = Blueprint('images', __name__, url_prefix='/images')

@bp.route('/')
def index():
    images = Images.query.order_by(Images.id.desc()).all()
    return render_template('images/index.html', images=images)

@bp.route('/upload', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        pic = request.files.get('pic')
        title = request.form.get('title')
        if not title:
            title = '좋아요!!!'

        if not pic:
            flash('No image selected!', 'danger')
            return redirect(url_for('images.upload_image'))

        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype
        if not filename or not mimetype:
            flash('Bad upload!', 'danger')
            return redirect(url_for('images.upload_image'))

        img_data = pic.read()
        image = Images(title=title, img=img_data, name=filename, mimetype=mimetype)
        db.session.add(image)
        db.session.commit()

        flash(f'Image "{filename}" has been uploaded successfully.', 'success')
        return redirect(url_for('images.upload_image'))

    images = Images.query.order_by(Images.id.desc()).all()
    return render_template('images/upload.html', images=images)

@bp.route('/get_image/<int:id>')
def get_image(id):
    image = Images.query.get_or_404(id)
    return Response(image.img, mimetype=image.mimetype)

@bp.route('/delete/<int:id>')
def delete_image(id):
    image = Images.query.get_or_404(id)
    db.session.delete(image)
    db.session.commit()
    flash(f'Image "{image.name}" has been deleted successfully.', 'success')
    return redirect(url_for('images.index'))

# @bp.route('/upload', methods=['GET', 'POST'])
# def upload_image():
#     if request.method == 'POST':
#         pic = request.files.get('pic')

#         if not pic:
#             flash('No image selected!', 'danger')
#             return redirect(request.url)

#         filename = secure_filename(pic.filename)
#         mimetype = pic.mimetype
#         if not filename or not mimetype:
#             flash('Bad upload!', 'danger')
#             return redirect(request.url)

#         img_data = pic.read()
#         image = Images(img=img_data, name=filename, mimetype=mimetype)
#         db.session.add(image)
#         db.session.commit()

#         flash(f'Image "{filename}" has been uploaded successfully.', 'success')
#         return redirect(url_for('image.upload_image'))

#     images = Images.query.order_by(Images.id.desc()).all()
#     return render_template('contents/image/upload.html', images=images)
