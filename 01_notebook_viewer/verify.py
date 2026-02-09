#!/usr/bin/env python3
"""
Nginx /research 경로 배포 검증 스크립트
설정이 올바른지 확인하는 자동화 도구
"""

import subprocess
import sys
import socket

def run_command(cmd, desc):
    """명령어 실행 및 결과 출력"""
    print(f"\n▶ {desc}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✓ {desc} - 성공")
            return True
        else:
            print(f"✗ {desc} - 실패")
            if result.stderr:
                print(f"  에러: {result.stderr.split(chr(10))[0]}")
            return False
    except subprocess.TimeoutExpired:
        print(f"✗ {desc} - 타임아웃 (5초)")
        return False
    except Exception as e:
        print(f"✗ {desc} - 예외: {e}")
        return False

def check_port(port):
    """포트 사용 여부 확인"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    return result == 0

def main():
    print("""
╔════════════════════════════════════════════════════════╗
║  Nginx /research 경로 배포 검증 스크립트              ║
║  FastAPI + Nginx 설정 확인                             ║
╚════════════════════════════════════════════════════════╝
""")
    
    checks = []
    
    # 1. Python 확인
    print("\n[1/8] Python 환경 확인")
    if run_command("python3 --version", "Python 3"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 2. Nginx 설치 확인
    print("\n[2/8] Nginx 설치 확인")
    if run_command("nginx -v", "Nginx"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 3. Nginx 설정 검증
    print("\n[3/8] Nginx 설정 검증")
    if run_command("sudo nginx -t", "Nginx 설정 문법"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 4. FastAPI 패키지 확인
    print("\n[4/8] FastAPI 패키지 확인")
    if run_command("python3 -c 'import fastapi'", "FastAPI 설치"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 5. main_nginx.py 확인
    print("\n[5/8] main_nginx.py 파일 확인")
    if run_command("test -f main_nginx.py", "main_nginx.py 파일"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 6. templates 디렉토리 확인
    print("\n[6/8] templates 디렉토리 확인")
    if run_command("test -d templates", "templates 디렉토리"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 7. static 디렉토리 확인
    print("\n[7/8] static 디렉토리 확인")
    if run_command("test -d static", "static 디렉토리"):
        checks.append(True)
    else:
        checks.append(False)
    
    # 8. 포트 확인
    print("\n[8/8] 포트 사용 확인")
    if check_port(8151):
        print("⚠ 포트 8151이 이미 사용 중입니다 (서버가 실행 중일 수 있음)")
        checks.append(True)
    else:
        print("✓ 포트 8151이 비어있습니다")
        checks.append(True)
    
    # 결과 요약
    print("\n" + "="*52)
    print(f"검증 결과: {sum(checks)}/{len(checks)} 통과")
    print("="*52)
    
    if all(checks):
        print("\n✓ 모든 검증 완료! 배포 준비 완료")
        print("\n다음 명령어로 배포하세요:")
        print("  1. bash deploy.sh")
        print("  2. python3 main_nginx.py")
        print("  3. http://psid.aizen.co.kr/research/ 접속")
        return 0
    else:
        print("\n✗ 일부 검증 실패. 위의 메시지를 확인하세요.")
        print("\n해결 방법:")
        print("  1. DEPLOYMENT_GUIDE.md 참고")
        print("  2. 트러블슈팅 섹션 확인")
        print("  3. 로그 확인: tail -f notebook_viewer.log")
        return 1

if __name__ == "__main__":
    sys.exit(main())
