from ...extensions import db
from ...models.servers import Servers

servers = db.session.query(Servers).all()

cmd_sv_info = [
    {'name': "echo ip_address;", 'cmd': 'hostname -I;' },
    {'name': "echo os_info;", 'cmd': 'uname -a;' },
    {'name': "echo total_memory;", 'cmd': "free -m  | awk 'NR==2{print $2}';" },
    {'name': "echo cpu_info;", 'cmd': 'lscpu | grep "Model name:" | head -n 1;' },
    {'name': "echo cpu_cores;", 'cmd': 'grep -c processor /proc/cpuinfo;' },
    {'name': "echo uptime;", 'cmd': "uptime | awk '{print $3, $4}';"},
    {'name': "echo checked_date;", 'cmd': "date '+%Y-%m-%d %H:%M';"},
]

def get_svinfos():
    import paramiko # type: ignore

    svinfos_list = []

    for server in servers:
        try:
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # For testing only
            ssh_client.connect(server.ip_address, 22, server.login_id, server.password)
            
            cmd = ''
            for item in cmd_sv_info:
                cmd += item['name']
                cmd += item['cmd']

            _, stdout, stderr = ssh_client.exec_command(cmd)

            full_output = stdout.read().decode()
            output_lines = full_output.splitlines()

            # `lscpu` 명령어의 출력에서 "Model name:" 부분을 제거합니다.
            for index, line in enumerate(output_lines):
                if "Model name:" in line:
                    line = line.replace("Model name:", "").strip()
                    output_lines[index] = line

            error_output = stderr.read().decode()
            if error_output:
                print(error_output)

            sv_infos = {}
            # 각 키를 기준으로 출력을 분리하고, 여러 줄의 값을 한 줄로 합칩니다.
            for i in range(0, len(output_lines), 2):
                key = output_lines[i].strip()
                value = output_lines[i+1].strip().replace('\n', ' ')
                sv_infos[key] = value
            svinfos_list.append(sv_infos)
        except Exception as e:
            print(f"연결 실패: {e}")
        finally:
            ssh_client.close()
    return svinfos_list