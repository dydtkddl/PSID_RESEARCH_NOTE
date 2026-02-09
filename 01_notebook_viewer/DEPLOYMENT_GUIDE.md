# 연구노트 뷰어 - Nginx /research 경로 배포 가이드

Nginx를 통해 `/research` 경로에서 작동하도록 수정된 전체 프로젝트입니다.

## 📋 주요 변경사항

### 1. FastAPI 설정 (main_nginx.py)
```python
app = FastAPI(
    title="연구노트 뷰어",
    root_path="/research",  # ← Nginx 경로와 매칭
)
```

**`root_path="/research"` 효과:**
- 모든 라우트가 자동으로 `/research/...`로 변환됨
- `url_for()` 호출 시 자동으로 `/research/` 접두사 추가
- 상대경로와 절대경로 모두 올바르게 작동

### 2. Nginx 설정 (nginx.conf)

#### 경로 정규화
```nginx
location = /research {
    return 301 /research/;
}
```

#### 프록시 설정
```nginx
location /research/ {
    proxy_pass http://127.0.0.1:8151;
    proxy_http_version 1.1;
    
    # WebSocket 지원
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

### 3. 정적 파일 경로

FastAPI에서 `root_path` 설정 시:
```python
app.mount("/static", StaticFiles(directory="static"), name="static")
```

이는 자동으로 `/research/static`으로 매핑됨.

Template에서:
```html
<link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">
<!-- 자동으로 /research/static/style.css가 생성됨 -->
```

---

## 🚀 배포 절차

### Step 1: 파일 배치

```
project_root/
├── main_nginx.py              # ← 메인 FastAPI 앱 (root_path="/research")
├── nginx.conf                 # ← Nginx 설정
├── templates/                 # 기존 템플릿 폴더
│   ├── base.html
│   ├── index.html
│   ├── project.html
│   ├── viewer.html
│   ├── edit.html
│   └── ...
└── static/                    # 정적 파일
    ├── style.css
    └── ...
```

### Step 2: Nginx 설정 적용

```bash
# Nginx 설정 파일 백업
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup

# 새 설정 파일 복사
sudo cp nginx.conf /etc/nginx/nginx.conf

# 설정 검증
sudo nginx -t

# Nginx 재시작
sudo systemctl restart nginx
```

### Step 3: FastAPI 서버 실행

```bash
# 의존성 설치
pip install fastapi uvicorn markdown python-multipart pyyaml tqdm

# 서버 실행 (포트 8151)
python main_nginx.py

# 또는 프로덕션 모드
uvicorn main_nginx:app --host 0.0.0.0 --port 8151 --workers 4
```

### Step 4: 접근 테스트

```bash
# 브라우저에서 접속
http://psid.aizen.co.kr/research/
또는
http://localhost/research/
```

---

## ✅ 검증 체크리스트

### URL 경로 검증

| 엔드포인트 | 예상 URL | 작동 확인 |
|-----------|---------|---------|
| 홈 | `/research/` | ✓ |
| 프로젝트 목록 | `/research/project?rel_path=...` | ✓ |
| 파일 보기 | `/research/view?rel_path=...` | ✓ |
| 파일 편집 | `/research/edit?rel_path=...` | ✓ |
| 정적 파일 | `/research/static/style.css` | ✓ |
| 이미지 업로드 | `/research/upload_image` (POST) | ✓ |
| 파일 다운로드 | `/research/download/...` | ✓ |

### 상대경로 검증

Template의 모든 `url_for()` 호출:
```html
<!-- 올바른 방식 -->
<a href="{{ url_for('index') }}">홈</a>  <!-- /research/ -->
<a href="{{ url_for('project_view', rel_path='...') }}">...</a>  <!-- /research/project?... -->
<link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">  <!-- /research/static/... -->

<!-- 절대경로도 자동 처리됨 -->
<img src="/research/media/..." />  <!-- 동작 -->
```

---

## 🔧 트러블슈팅

### 문제 1: Static 파일을 찾을 수 없음
**원인:** Nginx 캐싱 또는 경로 오류

**해결:**
```bash
# Nginx 재시작
sudo systemctl restart nginx

# 브라우저 캐시 클리어 (Ctrl+Shift+Delete)
```

### 문제 2: 상대경로 오류
**원인:** 하드코딩된 절대경로

**해결 - 모든 template에서:**
```html
<!-- ❌ 나쁜 예 -->
<a href="/project">프로젝트</a>

<!-- ✅ 좋은 예 -->
<a href="{{ url_for('project_view', rel_path='...') }}">프로젝트</a>
```

### 문제 3: WebSocket 연결 실패
**원인:** Nginx 업그레이드 헤더 누락

**해결 - nginx.conf:**
```nginx
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

### 문제 4: 폼 제출 후 리다이렉트 오류
**원인:** FastAPI 리다이렉트에 경로 누락

**해결 - main_nginx.py:**
```python
# ❌ 잘못된 것
return RedirectResponse(url="/view?rel_path=...")

# ✅ 올바른 것 (FastAPI가 자동으로 /research/ 추가)
return RedirectResponse(url="/view?rel_path=...")
```

---

## 📊 모니터링

### 로그 확인

```bash
# FastAPI 로그
tail -f notebook_viewer.log

# Nginx 접근 로그
sudo tail -f /var/log/nginx/access.log | grep /research

# Nginx 에러 로그
sudo tail -f /var/log/nginx/error.log
```

### 성능 최적화

```nginx
# nginx.conf에 추가
http {
    # 캐싱
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=research_cache:10m;
    
    location /research/ {
        proxy_cache research_cache;
        proxy_cache_valid 200 10m;
    }
}
```

---

## 🔐 보안 고려사항

### 1. 경로 검증 (이미 구현됨)
```python
def safe_join(rel_path: str) -> Path:
    """ROOT_DIR 바깥 접근 차단"""
    if root not in candidate.parents:
        raise HTTPException(status_code=400, detail="Invalid path")
```

### 2. 파일 업로드 검증
```python
allowed_exts = {".png", ".jpg", ".jpeg", ".gif", ".webp"}
if ext not in allowed_exts:
    raise HTTPException(status_code=400, detail="Invalid file type")
```

### 3. CORS (필요시)
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["psid.aizen.co.kr", "localhost"],
    allow_methods=["GET", "POST"],
)
```

---

## 📝 환경 변수 설정 (선택사항)

```bash
# .env 파일
RESEARCH_ROOT=/path/to/research/notes
RESEARCH_PORT=8151
```

```python
# main_nginx.py에서
from dotenv import load_dotenv
load_dotenv()
ROOT_DIR = Path(os.getenv("RESEARCH_ROOT", r"C:\..."))
```

---

## 🎯 핵심 요점 정리

| 항목 | 설정 값 |
|-----|-------|
| **FastAPI root_path** | `/research` |
| **Nginx 프록시** | `http://127.0.0.1:8151` |
| **포트** | 8151 |
| **접근 URL** | `http://psid.aizen.co.kr/research/` |
| **정적 파일** | `/research/static/...` |
| **URL 생성 방식** | `url_for()` 자동 처리 |

---

## 📞 추가 지원

문제 발생 시:
1. 로그 확인: `tail -f notebook_viewer.log`
2. Nginx 설정 검증: `sudo nginx -t`
3. 포트 확인: `netstat -tulpn | grep 8151`
4. 프록시 테스트: `curl http://127.0.0.1:8151/`

