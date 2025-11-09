# hostname,IP,Interface,Date Time,rxpck/s,txpck/s,rxkB/s,txkB/s

from ..extensions import db
from sqlalchemy.dialects.postgresql import INET # type: ignore
from .users import BaseModel
from sqlalchemy import DateTime

class SarTraffic(BaseModel):
    __tablename__ = 'sar_traffic'
    hostname = db.Column(db.String(40), nullable=False)
    ip_address = db.Column(INET, nullable=False)
    interface_name = db.Column(db.String(40), nullable=False)
    date_time = db.Column(DateTime, nullable=False)
    rxkB_per_second = db.Column(db.Float)
    txkB_per_second = db.Column(db.Float)

    checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    # HostnameIp와 one to many Relationship
    host_infos_id = db.Column(db.Integer, db.ForeignKey('host_infos.id'))

    def __repr__(self):
        return f'<SarTraffic {self.hostname} By {self.ip_address}>'
