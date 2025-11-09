from ..extensions import db
from .users import BaseModel
import enum

class CAT(str, enum.Enum):
    HOST_INFO = 'host_info' # 서버의 hostname, ip_address 정보를 가져오는 명령어
    SV_INFO = 'sv_info' # 서버의 os_info, total_memory, cpu_cores, uptime 정보를 가져오는 명령어
    SV_SYSCTL = 'sv_sysctl' # 서버의 swappiness, dirty_ratio, overcommit_memory 정보를 가져오는 명령어
    SV_RESOURCES = 'sv_resources' # 서버의 cpu_usage, disk_usage 정보를 가져오는 명령어
    CUSTOM = 'custom' # 사용자 정의 명령어

# no Relationship
class Commands(BaseModel):
    __tablename__ = 'commands'
    category = db.Column(db.Enum(CAT, name='category_enum'), nullable=False)
    name = db.Column(db.String(80), nullable=False, unique=True)
    cmd = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f'<Commands {self.name}>'
