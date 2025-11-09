from flask import (
  Blueprint, redirect, 
  render_template as render, url_for) # type: ignore
from flask_login import current_user, login_required
from ..extensions import db
from ..models.users import Users
from ..models.servers import Servers
from ..models.hostinfos import HostInfos
from ..models.svinfos import SvInfos
from .get_data.get_svinfos import get_svinfos

bp = Blueprint("svinfos", __name__, url_prefix="/health/svinfos")

@bp.route("/")
def index():
    svinfos = db.session.query(SvInfos).all()
    current_user_id = current_user.get_id()
     
    svinfo_server_by_user = db.session.query(SvInfos)\
        .join(SvInfos.host_infos)\
        .join(HostInfos.access_info)\
        .join(Servers.operators)\
        .filter(Users.id == current_user_id).all()
    
    svinfos = db.session.query(SvInfos).all()

    return render("health/svinfos/index.html", 
        svinfo_server_by_user=svinfo_server_by_user, 
        svinfos=svinfos)

# get_svinfos -> svinfos 자동 생성
@bp.route("/generate")
@login_required
def generate_svinfo():
    svinfos = get_svinfos()
    current_user_id = current_user.get_id()
    hostinfos = db.session.query(HostInfos)\
        .join(HostInfos.access_info)\
        .join(Servers.operators)\
        .filter(Users.id == current_user_id).first()
    # get hostname and ip address from current user
    current_server = db.session.query(Servers)\
        .join(Servers.operators)\
        .filter(Users.id == current_user_id).first()

    for info in svinfos:
        print(info.get("os_info").split()[1])
        hostinfo = db.session.query(HostInfos).filter_by(ip_address=info.get("ip_address")).first()
        existing_svinfo = db.session.query(SvInfos)\
            .filter(SvInfos.ip_address == info.get("ip_address"))\
            .filter(hostinfo.hostname == info.get("os_info").split()[1]).first()
            # .filter(and_(SvInfos.ip_address == info.get("ip_address"), SvInfos.host_infos.hostname == info.get("os_info").split()[1] )).first()
        if existing_svinfo:
            existing_svinfo.ip_address = info.get("ip_address")
            existing_svinfo.os_info = info.get("os_info")
            existing_svinfo.total_memory = info.get("total_memory")
            existing_svinfo.cpu_info = info.get("cpu_info")
            existing_svinfo.cpu_cores = info.get("cpu_cores")
            existing_svinfo.uptime = info.get("uptime")
            existing_svinfo.checked_date = info.get("checked_date")
            existing_svinfo.host_infos_id = hostinfo.id
        else:
            svinfos = SvInfos(ip_address=info.get("ip_address"), 
                              os_info=info.get("os_info"), total_memory=info.get("total_memory"), cpu_info=info.get("cpu_info"), cpu_cores=info.get("cpu_cores"), uptime=info.get("uptime"), checked_date=info.get("checked_date"))
            hostinfo.sv_infos.append(svinfos)
            svinfos.host_infos_id = hostinfo.id
            db.session.add(svinfos)
    db.session.commit()

    return redirect(url_for("svinfos.index"))