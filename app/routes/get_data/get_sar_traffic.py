
def get_sar_traffic():
    import paramiko # type: ignore
    import os
    from ...extensions import db
    from ...models.servers import Servers

    # 현재 파일의 위치를 기준으로 셸 스크립트의 절대 경로를 생성합니다.
    current_dir = os.path.dirname(os.path.abspath(__file__))
    local_script = os.path.join(current_dir, '..','..', 'shell_script', 'sar_traffic.sh')
    remote_script = '/tmp/sar_traffic.sh'
    servers = db.session.query(Servers).all()
    for server in servers:
        try:
            # SSH 클라이언트 생성 및 연결
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server.ip_address, port=server.port, 
                        username=server.login_id, password=server.password)
            
            # SFTP로 스크립트 업로드
            sftp = ssh.open_sftp()
            sftp.put(local_script, remote_script)
            sftp.close()

            # 원격 서버의 IP 주소를 가져와서 파일 이름을 구성합니다.
            _, stdout, stderr = ssh.exec_command("hostname -I | awk '{print $1}'")
            ip_address = stdout.read().decode('utf-8').strip()
            filename = f"month_traffic_{ip_address}.csv"
            remote_output_file = f"/tmp/{filename}"

            # 셸 스크립트에 실행 권한을 부여하고 실행합니다.
            commands = [
                f'chmod +x {remote_script}',
                remote_script
            ]

            for cmd in commands:
                _, stdout, _ = ssh.exec_command(cmd, get_pty=True)
                stdout.channel.recv_exit_status()

            # 결과 파일 다운로드
            local_output_path = os.path.join(current_dir, '..','..', 'data')
            local_output_file = os.path.join(local_output_path, filename)
            # local_output_file = f"{local_output_path}/{filename}"
            sftp = ssh.open_sftp()
            sftp.get(remote_output_file, local_output_file)
            sftp.close()

            sftp = ssh.open_sftp()
            sftp.remove(remote_output_file)
            sftp.close()

        except Exception as e:
            print(f"연결 실패: {e}")
        finally:
            # 연결 종료
            ssh.close()

# sudo가 필요한 명령은 ssh.exec_command("echo password|sudo -$command") 방식으로 처리 가능
# • 보안상 passowrd 대신 key_filename='~/ssh/id_rsa' 방식 권장
# • paramiko는 scp를 직접 지원하지 않지만, sftp로 파일 전송 가능
# 필요하시면 paramiko 대신 fabric, pexpect, 또는 asyncssh 같은 고급 도구로 확장하는 방법도 알려드릴게요!