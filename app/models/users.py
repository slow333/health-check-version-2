from ..extensions import db
from flask_login import UserMixin # type: ignore
from werkzeug.security import generate_password_hash, check_password_hash

class BaseModel(db.Model):
    __abstract__ = True
    __allow_unmapped__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

# Association table for the many-to-many relationship between Users and Servers
class ServerUser(BaseModel):
    __tablename__ = 'users_servers'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))

class Users(UserMixin, BaseModel):
    __tablename__ = 'users'
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password  = db.Column(db.Text(), nullable=False)
    profile_image = db.Column(db.String(80), nullable=True, default='default.jpg')
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # many to many Relationship with Servers
    allowed_servers = db.relationship('Servers', secondary='users_servers',
                        backref='operators', lazy='dynamic')

    def set_password(self, password):
        self.password  = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f'<Users {self.username}>'
