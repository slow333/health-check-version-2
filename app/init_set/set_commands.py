import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app import create_app
from app.extensions import db
from app.models.commands import Commands

def seed_data():
    """Seeds the database with initial data."""
    app = create_app()
    with app.app_context():
        # Check if data already exists to prevent duplicates
        # if db.session.query(Commands).first():
        #     print("Data already exists. Skipping seeding.")
        #     return

        print("Seeding database...")
        commands = [
            Commands(category='host_info', name='hostname', cmd='hostname;'),
            Commands(category='host_info', name='ip_address', cmd='hostname -I;'),
            Commands(category='sv_info', name='os_version', cmd='uname -a'),
            Commands(category='sv_info', name='top_Info', cmd='top -b -n1'),
            Commands(category='sv_info', name='total_memory', cmd="free -m  | awk 'NR==2{print $2}';"),
            Commands(category='sv_info', name='total_swap', cmd="free -m  | awk 'NR==3{print $2}';"),
            Commands(category='sv_info', name='cpu_cores', cmd='grep -c processor /proc/cpuinfo;'),
            Commands(category='sv_info', name='free_memory', cmd="free -m  | awk 'NR==2 {print (($4+$6)/$2)*100 }';"),
            Commands(category='sv_info', name='cpu_usage', cmd="vmstat 1 1 | tail -n 1 | awk '{print $13}';"),
            Commands(category='sv_info', name='disk_usage', cmd='df -h;'),
            Commands(category='sv_info', name='uptime', cmd='uptime;'),
            Commands(category='sv_info', name='checked_date', cmd="date '+%Y-%m-%d %H:%M';"),

            Commands(category='sv_sysctl', name='vm.swappiness', cmd='sysctl vm.swappiness;'),
            Commands(category='sv_sysctl', name='vm.dirty_ratio', cmd='sysctl vm.dirty_ratio;'),
            Commands(category='sv_sysctl', name='vm.dirty_background_ratio', cmd='sysctl vm.dirty_background_ratio;'),
            Commands(category='sv_sysctl', name='vm.overcommit_memory', cmd='sysctl vm.overcommit_memory;'),
            Commands(category='sv_sysctl', name='vm.overcommit_ratio', cmd='sysctl vm.overcommit_ratio;'),
        ]
        commands_sysstat = [
            Commands(category='sv_sysstat', name='network_traffic', cmd='sar -n DEV;'),
        ]

        db.session.add_all(commands)
        db.session.commit()
        print("Database seeded successfully.")

if __name__ == '__main__':
    seed_data()

'''
현재 활성화된 서비스 목록을 보여줍니다.
systemctl list-units --type=service
bash file
최근 한달간의 트래픽을 수집
#!/bin/bash

# 출력 파일 초기화
output_file="monthly_traffic_summary.csv"
# 헤더 추가
echo "Date,Time,Interface,rxpck/s,txpck/s,rxkB/s,txkB/s" > $output_file

# 오늘 날짜 기준 최근 30일
for i in {0..29}; do
  # 날짜 계산-오늘 날짜를 맨 마지막으로 보냄(8일이면, 31로 함)
  day=$(date -d "-$i day" +%d)
  file="/var/log/sa/sa$day"

  # 파일 존재 여부 확인
  if [ -f "$file" ]; then
    # sar 명령어로 네트워크 트래픽 수집
    LC_ALL=C sar -n DEV -f "$file" | grep -vE "IFACE|lo" | awk -v d=$(date -d "-$i day" +%Y-%m-%d) '{
      printf "%s,%s,%s,%.2f,%.2f,%.2f,%.2f\n", d, $1, $2, $3, $4, $5, $6
    }' >> $output_file
  fi
done
$2         $3,     $4,         $5,       $6
IFACE   rxpck/s   txpck/s    rxkB/s    txkB/s 
'''