import paramiko # type: ignore

hostname = 'your_server_ip'
port = 22
username = 'your_username'
password = 'your_password'

def check_server_health(hostname, username, password):
    try:
        ssh_client = paramiko.SSHClient()
        # 서버의 호스트 키를 자동으로 추가 (보안에 취약하므로 테스트 용도로만 사용)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        ssh_client.connect(hostname, port, username, password)
        
        print(f"[{hostname}] 서버에 SSH 연결 성공")
        
        # 원격 서버에서 명령어 실행
        # stdin, stdout, stderr = ssh_client.exec_command('ls -l')
        stdin, stdout, stderr = ssh_client.exec_command('uptime')
        
        print("--- 명령어 실행 결과 ---")
        output = stdout.readlines()
        for line in output: print(line.strip())
        result = stdout.read().decode()
        
        error = stderr.readlines()
        if error:
            print("--- 에러 출력 ---")
            for line in error:
                print(line.strip())
        return result
        
    except Exception as e:
        print(f"연결 실패: {e}")
        
    finally:
        # 연결 종료
        if 'ssh_client' in locals() and ssh_client:
            ssh_client.close()
            print("SSH 연결 종료")
