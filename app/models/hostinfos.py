from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from .users import BaseModel
from .sar_traffic import SarTraffic

# server와 one to one Relationship
class HostInfos(BaseModel):
    __tablename__ = 'host_infos'

    hostname = db.Column(db.String(20), nullable=False, unique=True)
    ip_address = db.Column(INET, nullable=False, unique=True)
    os_info = db.Column(db.String(100), nullable=False)
    kernel_version = db.Column(db.String(100), nullable=False)
    total_memory = db.Column(db.String(12), nullable=False)
    cpu_info = db.Column(db.Text, nullable=False)
    cpu_cores = db.Column(db.String(12), nullable=False)
    checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Servers와 one to one Relationship
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))

    # SvInfos와 one to many Relationship
    sar_traffic = db.relationship('SarTraffic', backref='host_infos', lazy=True)

    def __repr__(self):
        return f'<HostInfos {self.hostname} for {self.ip_address}>'
