from flask import redirect, url_for, flash
from flask_admin import Admin, AdminIndexView
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

# Custom Admin Index View to secure the main admin page
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
         return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('You do not have permission to access the admin panel.', 'danger')
        return redirect(url_for('auth.login_users'))

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        flash('You do not have permission to access this resource.', 'danger')
        return redirect(url_for('auth.login_users'))

class UserView(SecureModelView):
    # 이 메서드가 빠지면 `TypeError` 발생 가능성이 높아집니다.
    def __init__(self, model, session, **kwargs):
        super().__init__(model, session, **kwargs)

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)
        elif not is_created:
            del form.password

class ServerInfoView(SecureModelView):
    # Use AJAX for the 'users' relationship
    # This will render a search box instead of a dropdown
    form_ajax_refs = {
        'operators': {
        'fields': ['username', 'email'], 
        'placeholder': 'Please select a user',
        'page_size': 10,
        'minimum_input_length': 1, 
        }
    }

def init_admin(app, db):
    admin = Admin(
        app,
        name='Admin Panel', 
        index_view=SecureAdminIndexView(name='Dashboard', url='/admin')
    )

    # Add all specified models to the admin interface
    from .models.servers import Servers
    from .models.users import Users
    admin.add_view(UserView(Users, db.session, category='Models'))
    admin.add_view(ServerInfoView(Servers, db.session, category='Models'))