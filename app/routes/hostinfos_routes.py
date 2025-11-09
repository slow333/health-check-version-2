from flask import (
  Blueprint, redirect, 
  render_template as render, url_for) # type: ignore
from flask_login import current_user, login_required
from ..extensions import db
from ..models.users import Users
from ..models.servers import Servers
from ..models.hostinfos import HostInfos
from .get_data.get_hostinfos import get_host_info

bp = Blueprint("hostinfos", __name__, url_prefix="/health/hostinfos")

@bp.route("/")
def index():
    hostinfos = db.session.query(HostInfos).all()
    current_user_id = current_user.get_id()
    # hostinfo를 통해 사용자 id로 필터링
    hostinfo_server_by_user = db.session.query(HostInfos)\
        .join(HostInfos.access_info)\
        .join(Servers.operators)\
        .filter(Users.id == current_user_id).all()

    return render("health/hostinfos/index.html", 
        hostinfo_server_by_user=hostinfo_server_by_user, 
        hostinfos=hostinfos)

# severs -> hostinfos 자동 생성
@bp.route("/generate")
@login_required
def generate_host():
    hostinfos = get_host_info()
    for info in hostinfos:
        query_existing = db.session.query(HostInfos)\
            .filter_by(ip_address=info.get("ip_address")).first()
        if query_existing:
            continue
        new_host = HostInfos(
            hostname=info.get("hostname"), 
            ip_address=info.get("ip_address"))
        db.session.add(new_host)
        server = db.session.query(Servers).filter_by(ip_address=info.get("ip_address")).first()
        if server:
            new_host.access_info = server
        db.session.commit()
    return redirect(url_for("hostinfos.index"))
