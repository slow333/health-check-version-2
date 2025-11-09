from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from .users import BaseModel
from .svinfos import SvInfos
from .sar_traffic import SarTraffic

# server와 one to one Relationship
class HostInfos(BaseModel):
    __tablename__ = 'host_infos'

    hostname = db.Column(db.String(20), nullable=False, unique=True)
    ip_address = db.Column(INET, nullable=False, unique=True)

    # Servers와 one to one Relationship
    server_id = db.Column(db.Integer, db.ForeignKey('servers.id'))

    # SvInfos와 one to many Relationship
    sv_infos = db.relationship('SvInfos', backref='host_infos', lazy=True)
    sar_traffic = db.relationship('SarTraffic', backref='host_infos', lazy=True)

    def __repr__(self):
        return f'<HostInfos {self.hostname} for {self.ip_address}>'
