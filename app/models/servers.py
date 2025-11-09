from ..extensions import db
from sqlalchemy.dialects.postgresql import INET
from .users import BaseModel
from .hostinfos import HostInfos

class Servers(BaseModel):
    __tablename__ = 'servers'
    server_name = db.Column(db.String(30), unique=True, nullable=False)
    login_id = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(INET, nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    port = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=db.func.current_timestamp())
    id_ip = db.Column(db.String(20))

    # ServerId와 one to one Relationship
    hostinfo = db.relationship('HostInfos', backref='access_info', uselist=False, lazy=True)

    def __init__(self, server_name, ip_address, login_id,  **kwargs):
        super().__init__(server_name=server_name, ip_address=ip_address, login_id=login_id, **kwargs)
        if not self.port:
            self.port = 22
        if not self.id_ip:
            self.id_ip = f"{self.login_id}@{self.ip_address}"

    # SV_INFO와 one to one Relationship
    # sv_info = db.relationship('SV_INFO', backref='server', uselist=False, lazy=True)

    def __repr__(self):
        return f'<Servers {self.id_ip}>'
    