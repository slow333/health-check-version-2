# from ..extensions import db
# from sqlalchemy.dialects.postgresql import INET # type: ignore
# from werkzeug.security import generate_password_hash
# from .users import BaseModel

# class SvInfo(BaseModel):
#     __tablename__ = 'sv_info'

#     os_info = db.Column(db.String(100), nullable=False)
#     total_memory = db.Column(db.String(12), nullable=False)
#     cpu_info = db.Column(db.Text, nullable=False)
#     cpu_cores = db.Column(db.String(12), nullable=False)
#     uptime = db.Column(db.String(100), nullable=False)

#     checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     # HostInfos와 one to many Relationship
#     sv_info_id = db.Column(db.Integer, db.ForeignKey('sv_info.id'), nullable=False)

#     def __repr__(self):
#         return f'<Server {self.sv_info.hostname} By {self.sv_info.ip_address}>'
    
# class SvResources(BaseModel):
#     __tablename__ = 'sv_resources'
    
#     free_memory = db.Column(db.String(12), nullable=False)
#     cpu_usage = db.Column(db.String(12), nullable=False)
#     disk_usage = db.Column(db.Text, nullable=False)
#     custom_1 = db.Column(db.String(12))
#     custom_2 = db.Column(db.String(12))
#     custom_3 = db.Column(db.String(12))
#     custom_4 = db.Column(db.String(12))
#     checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     # HostInfos와 one to many Relationship
#     sv_info_id = db.Column(db.Integer, db.ForeignKey('sv_info.id'), nullable=False)

#     def __repr__(self):
#         return f'<Server {self.sv_info.hostname} By {self.sv_info.ip_address}>'

# class SVSysctl(BaseModel):
#     __tablename__ = 'sv_sysctl'

#     swappiness = db.Column(db.String(12))
#     dirty_ratio = db.Column(db.String(12))
#     dirty_background_ratio = db.Column(db.String(12))
#     overcommit_memory = db.Column(db.String(12))
#     overcommit_ratio = db.Column(db.String(12))
#     custom_1 = db.Column(db.String(12))
#     custom_2 = db.Column(db.String(12))
#     custom_3 = db.Column(db.String(12))
#     custom_4 = db.Column(db.String(12))
#     checked_date = db.Column(db.DateTime, default=db.func.current_timestamp())
#     # SV_INFO와 one to many Relationship
#     sv_info_id = db.Column(db.Integer, db.ForeignKey('sv_info.id'), nullable=False)

#     def __repr__(self):
#         return f'<Server {self.sv_info.hostname} By {self.sv_info.ip_address}>'