from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from .users import BaseModel

class SvInfos(BaseModel):
    __tablename__ = 'sv_infos'
    ip_address = db.Column(INET, nullable=False)
    os_info = db.Column(db.String(255), nullable=False)
    total_memory = db.Column(db.String(12), nullable=False)
    cpu_info = db.Column(db.Text, nullable=False)
    cpu_cores = db.Column(db.String(12), nullable=False)
    uptime = db.Column(db.String(100), nullable=False)

    checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    # HostnameIp와 one to many Relationship
    host_infos_id = db.Column(db.Integer, db.ForeignKey('host_infos.id'))

    def __repr__(self):
        return f'<Server {self.name} By {self.host_infos.hostname}>'
