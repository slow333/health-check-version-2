cmd_host = [
    {'name': "echo hostname;", 'cmd': 'hostname;' },
    {'name': "echo ip_address;", 'cmd': 'hostname -I;' },
    {'name': "echo os_info;", 'cmd': "cat /etc/redhat-release;" },
    {'name': "echo kernel_version;", 'cmd': "uname -a | awk '{print $3}';" },
    {'name': "echo total_memory;", 'cmd': "free -m  | awk 'NR==2{print $2}';" },
    {'name': "echo cpu_info;", 'cmd': 'lscpu | grep "Model name:" | head -n 1;' },
    {'name': "echo cpu_cores;", 'cmd': 'grep -c processor /proc/cpuinfo;' },
    {'name': "echo checked_date;", 'cmd': "date '+%Y-%m-%d %H:%M';"},
]

def get_hostinfos():
    from ...extensions import db
    from ...models.servers import Servers
    import paramiko # type: ignore

    servers = db.session.query(Servers).all()

    if len(servers) > 0:
        hostinfo_list = []

        for server in servers:
            try:
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # For testing only
                ssh_client.connect(server.ip_address, 22, server.login_id, server.password)

                cmd = ''
                for item in cmd_host:
                    cmd += item['name']
                    cmd += item['cmd']

                _, stdout, stderr = ssh_client.exec_command(cmd)

                full_output = stdout.read().decode()
                output_lines = full_output.splitlines()

                error_output = stderr.read().decode()
                if error_output:
                    print(error_output)

                host_info = {}
                for i, item in enumerate(output_lines):
                    if(i%2 == 0):
                        host_info[item.strip()] = output_lines[i+1].strip()
                hostinfo_list.append(host_info)
            except Exception as e:
                print(f"연결 실패: {e}")
            finally:
                ssh_client.close()
        return hostinfo_list
    else:
        return None