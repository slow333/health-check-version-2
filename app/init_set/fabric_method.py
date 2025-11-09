# pip install fabric
'''
from fabric import Connection

# 접속 정보
host = "your.server.ip"
user = "your_username"
password = "your_password"
local_script = "myscript.sh"
remote_script = "/tmp/myscript.sh"
output_file = "/tmp/script_output.txt"

# 연결 생성
conn = Connection(host=host, user=user, connect_kwargs={"password": password})

# 1. 스크립트 업로드
conn.put(local_script, remote=remote_script)

# 2. 실행 권한 부여
conn.run(f"chmod +x {remote_script}")

# 3. 스크립트 실행 및 결과 저장
conn.run(f"{remote_script} > {output_file} 2>&1")

# 4. 결과 파일 다운로드
conn.get(remote=output_file, local="script_output.txt")

print("스크립트 실행 완료. 결과는 'script_output.txt'에 저장됨.")
'''

