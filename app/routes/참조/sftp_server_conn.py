import paramiko # type: ignore
import os

# SFTP 연결 정보 설정
hostname = 'sftp.example.com'
port = 22
username = 'your_username'
password = 'your_password' # 비밀번호 대신 키 기반 인증을 권장합니다.

# 로컬 및 원격 파일 경로
local_file_path = '/path/to/local/file.txt'
remote_file_path = '/path/to/remote/file.txt'
download_destination_path = '/path/to/local/downloaded_file.txt'

def get_file_from_sftp_client():
    try:
        # SSH 클라이언트 생성
        ssh_client = paramiko.SSHClient()

        # 호스트 키 정책 설정 (주의: 개발 용도로만 사용)
        # 실제 운영 환경에서는 `known_hosts` 파일을 사용하세요.
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # SFTP 서버에 연결
        ssh_client.connect(hostname, port, username, password)
        print(f"SFTP 서버 {hostname}에 연결되었습니다.")

        # SFTP 세션 열기
        sftp_client = ssh_client.open_sftp()

        # 2. 파일 다운로드
        print(f"파일을 다운로드하는 중: {remote_file_path} -> {download_destination_path}")
        sftp_client.get(remote_file_path, download_destination_path)
        print("다운로드 완료.")

        # 3. local 디렉터리 파일 목록 보기
        os.chdir('/path/to/local/')
        
        files = os.getcwd().listdir()
        for file in files:
            print(f"-  {file}")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        # 연결 종료
        if sftp_client:
            sftp_client.close()
        if ssh_client:
            ssh_client.close()
        print("\nSFTP 연결이 종료되었습니다.")

def upload_file_to_sftp_client(hostname, port, username, password):
    try:
        # SSH 클라이언트 생성
        ssh_client = paramiko.SSHClient()

        # 호스트 키 정책 설정 (주의: 개발 용도로만 사용)
        # 실제 운영 환경에서는 `known_hosts` 파일을 사용하세요.
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # SFTP 서버에 연결
        ssh_client.connect(hostname, port, username, password)
        print(f"SFTP 서버 {hostname}에 연결되었습니다.")

        # SFTP 세션 열기
        sftp_client = ssh_client.open_sftp()

        # 1. 파일 업로드
        print(f"파일을 업로드하는 중: {local_file_path} -> {remote_file_path}")
        sftp_client.put(local_file_path, remote_file_path)
        print("업로드 완료.")

        # 3. 원격 디렉터리 파일 목록 보기
        print(f"\n원격 경로 '{sftp_client.getcwd()}'의 파일 목록:")
        files = sftp_client.listdir()
        for file in files:
            print(f"-  {file}")

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        # 연결 종료
        if sftp_client:
            sftp_client.close()
        if ssh_client:
            ssh_client.close()
        print("\nSFTP 연결이 종료되었습니다.")