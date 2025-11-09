from flask import (
  Blueprint, redirect, request,
  render_template as render, flash, url_for) # type: ignore
from flask_login import current_user, login_required
from ..extensions import db
from ..models.users import Users
from ..models.servers import Servers
from ..models.hostinfos import HostInfos
from ..models.sar_traffic import SarTraffic
from .pagenation import pagenation
from .get_data.get_sar_traffic import get_sar_traffic
import os
import re
from sqlalchemy import or_, and_, cast, String # type: ignore
from datetime import datetime
# hostname,IP,Interface,Date Time,rxkB/s,txkB/s

bp = Blueprint("sar_traffic", __name__, url_prefix="/health/sar_traffic")

@bp.route("/generate")
@login_required
def generate_traffic():
    get_sar_traffic()
    # down 받은 파일을 불러오기
    current_dir = os.path.dirname(os.path.abspath(__file__))
    down_dir = os.path.join(current_dir,'..', 'data')
    for file in os.listdir(down_dir):
        if file.endswith(".csv"):
            file_path = os.path.join(down_dir, file)
            with open(file_path, 'r') as f:
                lines = f.readlines()[1:] # Skip header
                for line in lines:
                    pattern_time = "[0-2][0-9]:[0-5][0-9]:[0-5][0-9]"
                    if re.finditer(pattern_time, line) is None:
                        continue

                    data = line.strip().split(',')
                    if data[2] == "LINUX" or len(data[2]) == 0 or data[3].endswith("Average:"):
                        continue
                    hostname = data[0]
                    ip_address = data[1]
                    interface_name = data[2]
                    date_time = data[3]
                    rxkB_per_second = data[4]
                    txkB_per_second = data[5]
                    # print("============", hostname, ip_address, interface_name, date_time, rxkB_per_second, txkB_per_second)

                    try:
                        date_time = datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
                        hostinfo = db.session.query(HostInfos).filter_by(ip_address=ip_address).first()
                        if not hostinfo:
                            continue
                        existing_traffic_data = db.session.query(SarTraffic).filter(and_(
                            SarTraffic.hostname == hostname,
                            SarTraffic.ip_address == ip_address,
                            SarTraffic.interface_name == interface_name,
                            SarTraffic.date_time == date_time,
                        )).first()
                        if existing_traffic_data:
                            continue

                        new_traffic_data = SarTraffic(
                            hostname=hostname,
                            ip_address=ip_address,
                            interface_name=interface_name,
                            date_time=date_time,
                            rxkB_per_second=float(rxkB_per_second),
                            txkB_per_second=float(txkB_per_second),
                            host_infos_id=hostinfo.id
                        )
                        hostinfo.sar_traffic.append(new_traffic_data)
                        db.session.add(new_traffic_data)
                    except (ValueError, IndexError) as e:
                        print(f"Skipping line due to error: {e} -> {line.strip()}")
                        continue
            db.session.commit()
            os.remove(file_path)

    return redirect(url_for("sar_traffic.index"))

@bp.route("/")
def index():
    hostname = request.args.get('hostname', '')
    ip_address = request.args.get('ip_address', '')
    start_date = request.args.get('start_date', '')
    end_date = request.args.get('end_date', '')

    query = db.session.query(SarTraffic)

    # ========== Search Logic ==========
    # 모든 조건에 대해 개별 검색 and 조건
    # date_time을 구간으로 검색 조건
    filters = []
    if hostname:
        filters.append(SarTraffic.hostname.ilike(f'%{hostname}%'))
    if ip_address:
        filters.append(cast(SarTraffic.ip_address, String).ilike(f'%{ip_address}%'))
    if start_date:
        filters.append(SarTraffic.date_time >= start_date)
    if end_date:
        # 날짜에 23:59:59를 추가하여 해당일 전체를 포함하도록 합니다.
        filters.append(SarTraffic.date_time <= f'{end_date} 23:59:59')

    query = query.filter(and_(*filters))
    # ========== end Search Logic ==========
    pagenation_data = pagenation(query=query, per_page=20, orders=SarTraffic.id.desc(), request_args=request.args)

    return render("health/sar_traffic/index.html",
                  traffic_data = pagenation_data['query_result'],
                  pagenation = pagenation_data,
                  hostname=hostname,
                  ip_address=ip_address,
                  start_date=start_date,
                  end_date=end_date
                  )
