import paramiko

# 접속 정보
hostname = '192.168.219.7'
port = 22
username = 'root'
password = '1'
local_script = '../routes/shell_script/sar_traffic.sh'
remote_script = '/tmp/sar_traffic.sh'
# output_file = "/tmp/monthly_traffic_summary.csv"

# SSH 클라이언트 생성 및 연결
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname, port=port, username=username, password=password)
print("="*20)
# cmd = 'hostname -I'
# _, stdout_ip, stderr_ip = ssh.exec_command(cmd)
# file_name = f"monthly_traffic_{stdout_ip.read().decode().strip()}.csv"
# output_file=f"/tmp/{file_name}"
# print(output_file)

# SFTP로 스크립트 업로드
sftp = ssh.open_sftp()
sftp.put(local_script, remote_script)
sftp.close()

# 실행 권한 부여 및 실행
commands = [
    f'chmod +x {remote_script}',
    f'{remote_script} 2>&1'
    # f'{remote_script} > {output_file} 2>&1'
]

for cmd in commands:
    stdin, stdout, stderr = ssh.exec_command(cmd)
    stdout.channel.recv_exit_status()  # 명령 완료 대기

# 결과 파일 다운로드
local_path = "../routes/get_data/traffic_data/"
sftp = ssh.open_sftp()
sftp.get("/tmp/monthly_traffic_summary_rhel7.csv", "../routes/get_data/traffic_data/monthly_traffic_summary_rhel7.csv")
sftp.close()

# 연결 종료
ssh.close()

print("스크립트 실행 완료. 결과는 'script_output.csv'에 저장됨.")