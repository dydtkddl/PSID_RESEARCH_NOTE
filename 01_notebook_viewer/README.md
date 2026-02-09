# 📋 Nginx /research 경로 배포 - 최종 체크리스트

## 🎯 프로젝트 개요

**목표:** FastAPI 연구노트 뷰어를 Nginx `/research` 경로에서 완벽 작동

**핵심 설정:**
- FastAPI root_path: `/research`
- Nginx 프록시: `http://127.0.0.1:8151`
- 포트: 8151

---

## 📦 생성된 파일 정리

```
your_project/
│
├── 🆕 main_nginx.py                  # 수정된 FastAPI 앱 (root_path="/research")
├── 🆕 nginx.conf                     # Nginx 설정파일
├── 🆕 template_base.html             # Jinja2 기본 템플릿 (url_for 사용)
├── 🆕 DEPLOYMENT_GUIDE.md            # 배포 가이드 (상세)
├── 🆕 CHANGES_SUMMARY.md             # 변경사항 요약
├── 🆕 deploy.sh                      # 자동화 배포 스크립트
├── 📄 README.md                      # ← 이 파일
│
├── templates/                        # 기존 템플릿 (수정 필요 없음)
│   ├── base.html
│   ├── index.html
│   ├── project.html
│   ├── viewer.html
│   ├── edit.html
│   └── ...
│
└── static/                           # 기존 정적 파일 (수정 필요 없음)
    ├── style.css
    └── ...
```

---

## 🚀 3단계 배포

### Step 1: 자동화 배포 (권장)
```bash
# 터미널에서 프로젝트 디렉토리로 이동
cd /path/to/your_project

# 배포 스크립트 실행
bash deploy.sh

# 자동으로:
# ✓ Python 의존성 설치
# ✓ Nginx 설정 백업 및 적용
# ✓ Nginx 재시작
# ✓ 배포 완료
```

### Step 2: FastAPI 서버 시작
```bash
# 개발 모드
python3 main_nginx.py

# 또는 프로덕션 모드 (권장)
uvicorn main_nginx:app \
  --host 0.0.0.0 \
  --port 8151 \
  --workers 4
```

### Step 3: 접속 확인
```
브라우저 열기:
http://psid.aizen.co.kr/research/
```

---

## ✅ 검증 체크리스트

### 1. 의존성 확인
- [ ] Python 3 설치됨
- [ ] Nginx 설치됨
- [ ] FastAPI, uvicorn, markdown 등 pip 패키지 설치됨

### 2. 파일 확인
- [ ] main_nginx.py 파일 있음
- [ ] nginx.conf 파일 있음
- [ ] templates/ 디렉토리 있음
- [ ] static/ 디렉토리 있음

### 3. Nginx 설정 확인
```bash
sudo nginx -t
# 출력: "test is successful" ✓
```

### 4. 서버 실행 확인
```bash
python3 main_nginx.py
# 출력: "Uvicorn running on 0.0.0.0:8151" ✓
```

### 5. 로컬 테스트
```bash
curl http://127.0.0.1:8151/
# HTML 응답 받음 ✓
```

### 6. Nginx 프록시 테스트
```bash
curl http://localhost/research/
# 동일한 HTML 응답 ✓
```

### 7. 브라우저 접속
```
http://psid.aizen.co.kr/research/
# 페이지 로드됨 ✓
```

---

## 🔧 주요 변경사항

### FastAPI (main_nginx.py)
```python
# 추가된 설정
app = FastAPI(root_path="/research")

# 결과
- URL 자동 정규화: / → /research/
- url_for() 자동 처리
- 리다이렉트 자동 처리
```

### Nginx (nginx.conf)
```nginx
# 추가된 설정
location /research/ {
    proxy_pass http://127.0.0.1:8151;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}

# 결과
- /research/... → 포트 8151로 프록시
- WebSocket 완벽 지원
```

### 템플릿 (모든 HTML)
```html
<!-- 변경 전 (❌ 안됨) -->
<link rel="stylesheet" href="/static/style.css">
<a href="/project">프로젝트</a>

<!-- 변경 후 (✓ 작동) -->
<link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">
<a href="{{ url_for('project_view', rel_path='...') }}">프로젝트</a>
```

---

## 📊 경로 매핑

### 자동 변환

| 요청 URL | FastAPI 라우트 | 실제 처리 |
|----------|---------------|---------|
| `/research/` | `GET /` | 인덱스 페이지 |
| `/research/project?rel_path=...` | `GET /project` | 프로젝트 목록 |
| `/research/view?rel_path=...` | `GET /view` | 파일 상세보기 |
| `/research/edit?rel_path=...` | `GET /edit` | 파일 편집 |
| `/research/static/style.css` | `GET /static/...` | CSS 파일 |
| `/research/download/...` | `GET /download/...` | 파일 다운로드 |

### FastAPI 자동 처리

```python
# 실제 코드
@app.get("/")
async def index(request: Request):
    ...

# url_for('index')
# → "/research/" (자동으로 root_path 추가)

# RedirectResponse(url="/project?...")
# → 자동으로 /research/project로 리다이렉트
```

---

## 🐛 문제 해결

### 문제: Static 파일 404

**진단:**
```bash
# 브라우저 개발자도구에서 확인
# CSS, JS 파일이 로드되지 않음
```

**원인:**
- Nginx 재시작 미실시
- url_for() 미사용

**해결:**
```bash
sudo systemctl restart nginx
# 또는
sudo /etc/init.d/nginx restart
```

### 문제: 이미지 업로드 실패

**진단:**
```bash
# 콘솔에서 404 또는 500 에러
```

**원인:**
- upload_image 라우트 경로 오류

**해결:**
```python
# main_nginx.py 확인
@app.post("/upload_image", name="upload_image")
async def upload_image(...):
    ...
```

### 문제: 페이지 리다이렉트 오류

**진단:**
```bash
# 저장 후 `/view` 대신 `/research/view`로 이동 안 됨
```

**원인:**
- RedirectResponse에서 절대경로 사용
- FastAPI가 자동으로 처리하지 못함

**해결:**
```python
# ❌ 이전
return RedirectResponse(url="/view?rel_path=...")

# ✓ 수정 (FastAPI가 자동으로 /research/ 추가)
return RedirectResponse(url="/view?rel_path=...")
```

---

## 📈 성능 모니터링

### 로그 확인

```bash
# FastAPI 로그
tail -f notebook_viewer.log

# Nginx 접근 로그
sudo tail -f /var/log/nginx/access.log

# Nginx 에러 로그
sudo tail -f /var/log/nginx/error.log

# 특정 경로만 보기
sudo tail -f /var/log/nginx/access.log | grep /research
```

### 포트 확인

```bash
# 8151 포트 사용 확인
netstat -tulpn | grep 8151

# Nginx 상태
sudo systemctl status nginx

# 프로세스 확인
ps aux | grep uvicorn
ps aux | grep nginx
```

---

## 🔐 보안 체크리스트

- [ ] 경로 검증 (safe_join) 적용됨
- [ ] 파일 업로드 확장자 제한 (png, jpg, gif 등)
- [ ] 입력값 HTML 이스케이프 처리
- [ ] CORS 설정 (필요시)
- [ ] HTTPS 인증서 설정 (프로덕션)

---

## 💾 백업 및 복구

### 백업 생성

```bash
# Nginx 설정 백업
sudo cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# 프로젝트 백업
tar -czf research_backup.tar.gz \
  main_nginx.py templates/ static/

# 설정 백업
tar -czf config_backup.tar.gz \
  themes.json favorites.json recents.json
```

### 복구 방법

```bash
# Nginx 복구
sudo cp /etc/nginx/nginx.conf.backup /etc/nginx/nginx.conf
sudo systemctl restart nginx

# 프로젝트 복구
tar -xzf research_backup.tar.gz
```

---

## 📞 자주 묻는 질문 (FAQ)

### Q1: 기존 URL 패턴 사용 가능?
**A:** 아니오. 반드시 `url_for()` 사용 필수

### Q2: /khu_chatbot, /SEI는?
**A:** 별도 포트(8501, 8502)로 독립 운영. 충돌 없음

### Q3: HTTPS 적용 방법?
**A:** certbot으로 자동 설정
```bash
sudo certbot --nginx -d psid.aizen.co.kr
```

### Q4: 여러 FastAPI 앱 실행?
**A:** 각각 다른 포트로 운영. Nginx가 자동 라우팅

### Q5: 로드 밸런싱?
**A:** uvicorn 워커 수 증가
```bash
uvicorn main_nginx:app --workers 4
```

---

## 🎓 학습 리소스

- **root_path 개념**: [FastAPI 문서](https://fastapi.tiangolo.com/)
- **Nginx 프록시**: [Nginx 공식 문서](https://nginx.org/)
- **Uvicorn 배포**: [Uvicorn 가이드](https://www.uvicorn.org/)

---

## ✨ 최종 체크

배포 전 마지막 확인:

- [ ] main_nginx.py에 `root_path="/research"` 있음
- [ ] nginx.conf의 proxy_pass가 `http://127.0.0.1:8151`
- [ ] 모든 템플릿에서 `url_for()` 사용
- [ ] `sudo nginx -t` 통과
- [ ] Nginx 재시작됨
- [ ] FastAPI 서버 실행 중
- [ ] 브라우저에서 `/research/` 접속 확인

---

## 🎉 축하합니다!

**모든 설정이 완료되었습니다!**

```bash
# 서버 시작
python3 main_nginx.py

# 브라우저 열기
# http://psid.aizen.co.kr/research/

# 즐겨보세요! 🚀
```

---

## 📝 추가 필요시

- 문서 수정: `DEPLOYMENT_GUIDE.md` 참고
- 설정 변경: `CHANGES_SUMMARY.md` 참고
- 자동 배포: `deploy.sh` 실행

**행운을 빕니다! 🌟**
