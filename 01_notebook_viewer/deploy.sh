#!/bin/bash
# 연구노트 뷰어 - Nginx /research 경로 배포 자동화 스크립트

set -e

echo "======================================"
echo "연구노트 뷰어 배포 자동화"
echo "======================================"
echo ""

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Step 1: 의존성 확인
echo -e "${YELLOW}[1/5] 의존성 확인 중...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3이 설치되지 않았습니다${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python 3 설치됨${NC}"

if ! command -v nginx &> /dev/null; then
    echo -e "${RED}Nginx가 설치되지 않았습니다${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Nginx 설치됨${NC}"
echo ""

# Step 2: Python 패키지 설치
echo -e "${YELLOW}[2/5] Python 패키지 설치 중...${NC}"
pip3 install fastapi uvicorn markdown python-multipart pyyaml tqdm -q
echo -e "${GREEN}✓ 패키지 설치 완료${NC}"
echo ""

# Step 3: Nginx 설정 백업 및 적용
echo -e "${YELLOW}[3/5] Nginx 설정 적용 중...${NC}"

if [ -f /etc/nginx/nginx.conf ]; then
    sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup.$(date +%Y%m%d_%H%M%S)
    echo "  백업: /etc/nginx/nginx.conf.backup.*"
fi

if [ -f ./nginx.conf ]; then
    sudo cp ./nginx.conf /etc/nginx/nginx.conf
    echo "  적용: ./nginx.conf → /etc/nginx/nginx.conf"
else
    echo -e "${RED}  ✗ nginx.conf를 찾을 수 없습니다${NC}"
    exit 1
fi

# Nginx 설정 검증
if sudo nginx -t 2>&1 | grep -q "successful"; then
    echo -e "${GREEN}✓ Nginx 설정 검증 통과${NC}"
else
    echo -e "${RED}✗ Nginx 설정 검증 실패${NC}"
    exit 1
fi

# Nginx 재시작
sudo systemctl restart nginx
echo -e "${GREEN}✓ Nginx 재시작 완료${NC}"
echo ""

# Step 4: FastAPI 서버 준비
echo -e "${YELLOW}[4/5] FastAPI 서버 준비 중...${NC}"

if [ ! -f ./main_nginx.py ]; then
    echo -e "${RED}main_nginx.py를 찾을 수 없습니다${NC}"
    exit 1
fi

if [ ! -d ./templates ]; then
    echo -e "${RED}templates/ 디렉토리를 찾을 수 없습니다${NC}"
    exit 1
fi

if [ ! -d ./static ]; then
    echo -e "${RED}static/ 디렉토리를 찾을 수 없습니다${NC}"
    exit 1
fi

echo -e "${GREEN}✓ 필요한 파일 확인 완료${NC}"
echo ""

# Step 5: 배포 정보 출력
echo -e "${YELLOW}[5/5] 배포 정보${NC}"
echo ""
echo "배포 체크리스트:"
echo "  ✓ Python 패키지"
echo "  ✓ Nginx 설정"
echo "  ✓ 필요 파일"
echo ""
echo -e "${GREEN}======================================"
echo "배포 준비 완료!"
echo "=====================================${NC}"
echo ""
echo "다음 명령으로 서버를 시작하세요:"
echo ""
echo -e "${YELLOW}개발 모드:${NC}"
echo "  python3 main_nginx.py"
echo ""
echo -e "${YELLOW}프로덕션 모드:${NC}"
echo "  uvicorn main_nginx:app --host 0.0.0.0 --port 8151 --workers 4"
echo ""
echo -e "${YELLOW}접근 URL:${NC}"
echo "  http://psid.aizen.co.kr/research/"
echo "  http://localhost/research/"
echo ""
echo -e "${YELLOW}로그 확인:${NC}"
echo "  tail -f notebook_viewer.log"
echo ""
