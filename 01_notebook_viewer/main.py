#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
연구노트 뷰어 - Nginx /research 경로 호환 버전
FastAPI root_path="/research" 설정으로 모든 라우트 자동 조정
"""

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple, Set
import os
import json
import logging
from datetime import datetime
import html
import io
import zipfile
import re
import shutil

from fastapi import (
    FastAPI,
    Request,
    HTTPException,
    Query,
    Form,
    UploadFile,
    File,
)
from fastapi.responses import (
    HTMLResponse,
    FileResponse,
    RedirectResponse,
    StreamingResponse,
    PlainTextResponse,
)
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from starlette.exceptions import HTTPException as StarletteHTTPException

from tqdm import tqdm
import markdown as md_lib

try:
    from docx import Document
except ImportError:
    Document = None

try:
    import yaml
except ImportError:
    yaml = None


# ======= 기본 설정 =======

ROOT_DIR = Path(r"C:\Users\PSID_PC_20\Desktop\Reseach_Note").expanduser().resolve()
LOG_FILE = "notebook_viewer.log"
THEME_CONFIG_PATH = Path("themes.json")
FAVORITES_FILE = Path("favorites.json")
RECENTS_FILE = Path("recents.json")

DEFAULT_THEME: Dict[str, str] = {
    "card_bg": "#ffffff",
    "card_border": "#dddddd",
    "accent": "#1f7aec",
    "header_bg": "#222222",
}

TEXT_EXTS = {
    ".txt", ".md", ".py", ".rtf", ".csv", ".json", ".yml", ".yaml", ".log",
}

MD_EXTENSIONS = [
    "extra", "tables", "fenced_code", "codehilite",
    "toc", "admonition", "sane_lists", "smarty", "nl2br",
    "meta", "footnotes",
    "pymdownx.superfences", "pymdownx.tasklist", "pymdownx.tilde",
    "pymdownx.highlight", "pymdownx.emoji", "pymdownx.arithmatex",
]

MD_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False, "noclasses": True},
    "toc": {"permalink": True},
    "pymdownx.tasklist": {"custom_checkbox": True, "clickable_checkbox": False},
    "pymdownx.highlight": {"use_pygments": True, "linenums": False},
    "pymdownx.arithmatex": {"generic": True},
}

TASK_PATTERN = re.compile(r"^(\s*[-*]\s+\[( |x|X)\]\s+)(.+)$")


# ======= 로깅 =======

logger = logging.getLogger("notebook_viewer")
logger.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s - %(message)s")

fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(formatter)

sh = logging.StreamHandler()
sh.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(sh)

logger.info("==== Notebook Viewer starting (Nginx /research mode) ====")
logger.info(f"ROOT_DIR: {ROOT_DIR}")
logger.info(f"Markdown extensions: {', '.join(MD_EXTENSIONS)}")


# ======= 간단 캐시 =======

MD_CACHE: Dict[str, Dict[str, Any]] = {}


# ======= 테마 유틸 =======

def load_theme_config() -> Dict[str, Dict[str, str]]:
    if not THEME_CONFIG_PATH.exists():
        return {}
    try:
        with THEME_CONFIG_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.warning(f"Failed to load theme config: {e}")
        return {}


def save_theme_config(cfg: Dict[str, Dict[str, str]]) -> None:
    try:
        with THEME_CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        logger.info("Theme config saved")
    except Exception as e:
        logger.error(f"Failed to save theme config: {e}")


def get_theme_for_project(project_rel_path: str) -> Dict[str, str]:
    cfg = load_theme_config()
    theme = cfg.get(project_rel_path, {})
    merged = {**DEFAULT_THEME, **theme}
    return merged


# ======= 공통 유틸 =======

def safe_join(rel_path: str) -> Path:
    """경로 검증"""
    root = ROOT_DIR.resolve()
    candidate = (ROOT_DIR / rel_path).resolve()
    
    if candidate == root:
        return candidate
    
    if root not in candidate.parents:
        logger.warning(f"Attempt to access outside root: {candidate}")
        raise HTTPException(status_code=400, detail="Invalid path")
    
    return candidate


def read_text_file(path: Path) -> Optional[str]:
    """텍스트 파일 읽기"""
    for enc in ("utf-8", "cp949", "latin-1"):
        try:
            with path.open("r", encoding=enc, errors="replace") as f:
                return f.read()
        except Exception:
            continue
    logger.warning(f"Failed to read text file: {path}")
    return None


def read_docx_file(path: Path) -> Optional[str]:
    """DOCX 파일 읽기"""
    if Document is None:
        return None
    try:
        doc = Document(str(path))
        texts = [p.text for p in doc.paragraphs]
        return "\n".join(texts)
    except Exception as e:
        logger.exception(f"Failed to read docx: {e}")
        return None


def render_markdown(md_text: str) -> str:
    """Markdown 렌더링"""
    try:
        html_out = md_lib.markdown(
            md_text,
            extensions=MD_EXTENSIONS,
            extension_configs=MD_EXTENSION_CONFIGS,
            output_format="html5",
        )
        return html_out
    except Exception as e:
        logger.exception(f"Markdown render failed: {e}")
        escaped = html.escape(md_text)
        return f"<pre>{escaped}</pre>"


# ======= 즐겨찾기 / 최근 문서 =======

def load_favorites() -> Set[str]:
    if not FAVORITES_FILE.exists():
        return set()
    try:
        with FAVORITES_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(data)
    except Exception as e:
        logger.warning(f"Failed to load favorites: {e}")
    return set()


def save_favorites(fav: Set[str]) -> None:
    try:
        with FAVORITES_FILE.open("w", encoding="utf-8") as f:
            json.dump(sorted(fav), f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save favorites: {e}")


def load_recents() -> List[Dict[str, Any]]:
    if not RECENTS_FILE.exists():
        return []
    try:
        with RECENTS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except Exception as e:
        logger.warning(f"Failed to load recents: {e}")
    return []


def save_recents(recents: List[Dict[str, Any]]) -> None:
    try:
        with RECENTS_FILE.open("w", encoding="utf-8") as f:
            json.dump(recents, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error(f"Failed to save recents: {e}")


def touch_recent(rel_path: str) -> None:
    """최근 문서에 추가"""
    recents = load_recents()
    now = datetime.now().isoformat()
    
    recents = [r for r in recents if r.get("rel_path") != rel_path]
    recents.insert(0, {"rel_path": rel_path, "ts": now})
    recents = recents[:50]
    
    save_recents(recents)


# ======= 데이터 수집 =======

def get_project_list() -> List[Dict[str, Any]]:
    if not ROOT_DIR.exists():
        logger.error(f"Root directory does not exist: {ROOT_DIR}")
        raise FileNotFoundError(f"Root directory not found: {ROOT_DIR}")
    
    dirs = sorted(
        [p for p in ROOT_DIR.iterdir() if p.is_dir()],
        key=lambda p: p.name.lower(),
    )
    
    theme_cfg = load_theme_config()
    projects: List[Dict[str, Any]] = []
    
    for d in tqdm(dirs, desc="Projects", unit="proj"):
        rel = d.relative_to(ROOT_DIR)
        rel_str = str(rel).replace(os.sep, "/")
        theme = {**DEFAULT_THEME, **theme_cfg.get(rel_str, {})}
        projects.append({
            "name": d.name,
            "rel_path": rel_str,
            "theme": theme,
        })
    
    logger.info(f"Found {len(projects)} projects")
    return projects


def list_markdown_files(project_rel_path: str) -> List[Dict[str, Any]]:
    project_root = safe_join(project_rel_path)
    
    if not project_root.exists() or not project_root.is_dir():
        logger.warning(f"Project directory not found: {project_root}")
        raise HTTPException(status_code=404, detail="Project not found")
    
    md_paths = sorted(
        project_root.rglob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    
    notes: List[Dict[str, Any]] = []
    
    for p in tqdm(md_paths, desc="Loading MD list", unit="file"):
        rel = p.relative_to(ROOT_DIR)
        rel_str = str(rel).replace(os.sep, "/")
        
        stat = p.stat()
        created_ts = stat.st_ctime
        modified_ts = stat.st_mtime
        created = datetime.fromtimestamp(created_ts).strftime("%Y-%m-%d %H:%M")
        modified = datetime.fromtimestamp(modified_ts).strftime("%Y-%m-%d %H:%M")
        
        # Frontmatter 추출
        try:
            content = read_text_file(p) or ""
            fm, _ = parse_frontmatter(content)
            metadata = fm or {}
        except:
            metadata = {}
        
        notes.append({
            "name": p.name,
            "rel_path": rel_str,
            "created": created,
            "modified": modified,
            "created_ts": created_ts,
            "modified_ts": modified_ts,
            "tags": metadata.get("tags", []),
            "status": metadata.get("status", ""),
        })
    
    logger.info(f"Listed {len(notes)} markdown notes")
    return notes


def parse_frontmatter(md_text: str) -> Tuple[Optional[Dict], str]:
    """간단한 YAML frontmatter 파서"""
    pattern = r"^---\s*\n(.*?)\n---\s*\n(.*)"
    match = re.match(pattern, md_text, re.DOTALL)
    
    if not match:
        return None, md_text
    
    try:
        if yaml:
            fm = yaml.safe_load(match.group(1)) or {}
        else:
            fm = {}
        body = match.group(2)
        return fm, body
    except Exception as e:
        logger.warning(f"Failed to parse frontmatter: {e}")
        return None, md_text


def get_md_info(path: Path) -> Dict[str, Any]:
    """MD 파일 정보 (frontmatter, 태그, 상태, 태스크 등)"""
    if path in MD_CACHE:
        return MD_CACHE[path]
    
    text = read_text_file(path)
    if text is None:
        return {"text": None, "meta": {}, "tags": [], "status": "", "tasks": []}
    
    fm, body = parse_frontmatter(text)
    meta = fm or {}
    tags = meta.get("tags", [])
    if isinstance(tags, str):
        tags = [tags]
    
    status = meta.get("status", "")
    
    # 태스크 추출
    tasks: List[Dict[str, Any]] = []
    for i, line in enumerate(body.split("\n"), 1):
        match = TASK_PATTERN.match(line)
        if match:
            done = match.group(2).lower() == "x"
            text_part = match.group(3)
            tasks.append({
                "line_no": i,
                "done": done,
                "text": text_part,
            })
    
    result = {
        "text": text,
        "meta": meta,
        "tags": tags,
        "status": status,
        "tasks": tasks,
    }
    MD_CACHE[path] = result
    return result


# ======= FastAPI 앱 (root_path="/research") =======

app = FastAPI(
    title="연구노트 뷰어",
    root_path="/research",
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ======= 예외 핸들러 =======

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(f"HTTP {exc.status_code}: {exc.detail}")
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled error: {exc}")
    return PlainTextResponse("서버 내부 오류", status_code=500)


# ======= 라우트: 인덱스 =======

@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request) -> HTMLResponse:
    logger.info("GET / - index (project list)")
    projects = get_project_list()
    favorites = load_favorites()
    recents_raw = load_recents()
    
    recent_notes: List[Dict[str, Any]] = []
    favorite_notes: List[Dict[str, Any]] = []
    
    # 최근 문서 (상위 5개)
    for r in recents_raw[:5]:
        rel_path = r.get("rel_path")
        if not isinstance(rel_path, str):
            continue
        try:
            p = safe_join(rel_path)
        except HTTPException:
            continue
        if not p.exists() or not p.is_file():
            continue
        recent_notes.append({
            "name": p.name,
            "rel_path": rel_path,
            "ts": r.get("ts"),
        })
    
    # 즐겨찾기
    for rel_path in sorted(favorites):
        try:
            p = safe_join(rel_path)
        except HTTPException:
            continue
        if not p.exists() or not p.is_file():
            continue
        favorite_notes.append({
            "name": p.name,
            "rel_path": rel_path,
        })
    
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "projects": projects,
            "default_theme": DEFAULT_THEME,
            "recent_notes": recent_notes,
            "favorite_notes": favorite_notes,
        },
    )


# ======= 라우트: 프로젝트 뷰 =======

@app.get("/project", response_class=HTMLResponse, name="project_view")
async def project_view(
    request: Request,
    rel_path: str = Query(...),
    sort: str = Query("modified"),
    order: str = Query("desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=200),
    q: Optional[str] = Query(None),
) -> HTMLResponse:
    logger.info(f"GET /project (rel_path={rel_path}, page={page})")
    
    project_dir = safe_join(rel_path)
    if not project_dir.exists() or not project_dir.is_dir():
        raise HTTPException(status_code=404, detail="Project not found")
    
    theme = get_theme_for_project(rel_path)
    all_notes = list_markdown_files(rel_path)
    
    # 검색
    if q:
        q_lower = q.lower()
        filtered = [
            n for n in all_notes
            if q_lower in n["name"].lower() or q_lower in n["rel_path"].lower()
        ]
    else:
        filtered = all_notes
    
    # 정렬
    reverse = order.lower() == "desc"
    if sort.lower() == "name":
        filtered.sort(key=lambda n: n["name"].lower(), reverse=reverse)
    elif sort.lower() == "created":
        filtered.sort(key=lambda n: n["created_ts"], reverse=reverse)
    else:
        filtered.sort(key=lambda n: n["modified_ts"], reverse=reverse)
    
    # 페이지네이션
    total = len(filtered)
    total_pages = max((total + page_size - 1) // page_size, 1)
    if page > total_pages:
        page = total_pages
    
    start = (page - 1) * page_size
    page_notes = filtered[start:start + page_size]
    
    favorites = load_favorites()
    for n in page_notes:
        n["is_favorite"] = n["rel_path"] in favorites
    
    return templates.TemplateResponse(
        "project.html",
        {
            "request": request,
            "project_name": project_dir.name,
            "project_rel_path": rel_path,
            "notes": page_notes,
            "theme": theme,
            "sort": sort,
            "order": order,
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": total_pages,
            "q": q or "",
        },
    )


# ======= 라우트: 상세 보기 =======

@app.get("/view", response_class=HTMLResponse, name="view_file")
async def view_file(
    request: Request,
    rel_path: str = Query(...),
) -> HTMLResponse:
    logger.info(f"GET /view (rel_path={rel_path})")
    
    target = safe_join(rel_path)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    rel_norm = rel_path.replace("\\", "/")
    touch_recent(rel_norm)
    
    parts = rel_norm.split("/")
    project_rel_path = parts[0] if len(parts) > 1 else ""
    project_name: Optional[str] = None
    theme = DEFAULT_THEME
    other_notes: List[Dict[str, Any]] = []
    
    if project_rel_path:
        try:
            project_dir = safe_join(project_rel_path)
            if project_dir.exists() and project_dir.is_dir():
                project_name = project_dir.name
                theme = get_theme_for_project(project_rel_path)
                all_notes = list_markdown_files(project_rel_path)
                other_notes = [n for n in all_notes if n["rel_path"] != rel_norm]
        except Exception as e:
            logger.warning(f"Error listing other notes: {e}")
    
    ext = target.suffix.lower()
    is_markdown = ext == ".md"
    
    html_content: Optional[str] = None
    unsupported_reason: Optional[str] = None
    metadata: Dict = {}
    tags: List[str] = []
    status: str = ""
    
    try:
        if is_markdown:
            info = get_md_info(target)
            metadata = info.get("meta", {})
            tags = info.get("tags", [])
            status = info.get("status", "")
            raw_text = info.get("text")
            if raw_text is None:
                unsupported_reason = "Markdown 파일을 읽을 수 없습니다."
            else:
                html_content = render_markdown(raw_text)
        else:
            unsupported_reason = f"미리보기를 지원하지 않는 형식: {ext}"
    except Exception as e:
        logger.exception(f"Error preparing file content: {e}")
        raise HTTPException(status_code=500, detail="File processing error")
    
    download_url = request.url_for("download_file", rel_path=rel_path)
    is_favorite = rel_norm in load_favorites()
    
    return templates.TemplateResponse(
        "viewer.html",
        {
            "request": request,
            "rel_path": rel_path,
            "file_name": target.name,
            "file_type": ext or "파일",
            "html_content": html_content,
            "unsupported_reason": unsupported_reason,
            "download_url": str(download_url),
            "project_rel_path": project_rel_path,
            "project_name": project_name,
            "other_notes": other_notes,
            "theme": theme,
            "metadata": metadata,
            "tags": tags,
            "status": status,
            "is_markdown": is_markdown,
            "is_favorite": is_favorite,
        },
    )


# ======= 라우트: 편집 =======

@app.get("/edit", response_class=HTMLResponse, name="edit_file")
async def edit_file(
    request: Request,
    rel_path: str = Query(...),
) -> HTMLResponse:
    logger.info(f"GET /edit (rel_path={rel_path})")
    
    target = safe_join(rel_path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    if target.suffix.lower() != ".md":
        raise HTTPException(status_code=400, detail="MD 파일만 수정 가능")
    
    raw_text = read_text_file(target)
    if raw_text is None:
        raise HTTPException(status_code=500, detail="파일을 읽을 수 없습니다")
    
    rel_norm = rel_path.replace("\\", "/")
    project_rel_path = rel_norm.split("/")[0] if "/" in rel_norm else ""
    theme = get_theme_for_project(project_rel_path) if project_rel_path else DEFAULT_THEME
    
    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "rel_path": rel_path,
            "file_name": target.name,
            "raw_content": raw_text,
            "theme": theme,
            "image_base_dir": str(Path(rel_path).parent).replace("\\", "/"),
        },
    )


# ======= 라우트: 저장 =======

@app.post("/save", name="save_file")
async def save_file(
    rel_path: str = Form(...),
    content: str = Form(...),
) -> RedirectResponse:
    logger.info(f"POST /save (rel_path={rel_path})")
    
    target = safe_join(rel_path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    with target.open("w", encoding="utf-8") as f:
        f.write(content)
    
    logger.info(f"Saved file: {target}")
    
    # 캐시 무효화
    if target in MD_CACHE:
        del MD_CACHE[target]
    
    return RedirectResponse(
        url=f"/research/view?rel_path={rel_path}",
        status_code=303
    )


# ======= 라우트: 미리보기 =======

@app.post("/render_preview", name="render_preview")
async def render_preview(content: str = Form(...)) -> HTMLResponse:
    html = render_markdown(content)
    return HTMLResponse(html)


# ======= 라우트: 이미지 업로드 =======

@app.post("/upload_image", name="upload_image")
async def upload_image(
    base_rel_dir: str = Form(...),
    image: UploadFile = File(...),
):
    logger.info(f"POST /upload_image (base_rel_dir={base_rel_dir})")
    
    base_dir = safe_join(base_rel_dir) if base_rel_dir else ROOT_DIR
    images_dir = base_dir / "_images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    orig_name = image.filename or "image"
    ext = Path(orig_name).suffix.lower()
    if ext not in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        ext = ".png"
    
    fname = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ext
    save_path = images_dir / fname
    
    data = await image.read()
    with save_path.open("wb") as f:
        f.write(data)
    
    logger.info(f"Saved image: {save_path}")
    
    md_path = f"_images/{fname}"
    return {"ok": True, "md_path": md_path}


# ======= 라우트: 다운로드 =======

@app.get("/download/{rel_path:path}", name="download_file")
async def download_file(rel_path: str) -> FileResponse:
    target = safe_join(rel_path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    logger.info(f"Download: {target}")
    return FileResponse(
        path=str(target),
        filename=target.name,
        media_type="application/octet-stream",
    )


# ======= 라우트: 즐겨찾기 토글 =======

@app.post("/toggle_favorite", name="toggle_favorite")
async def toggle_favorite(rel_path: str = Form(...)) -> RedirectResponse:
    logger.info(f"POST /toggle_favorite (rel_path={rel_path})")
    
    fav = load_favorites()
    if rel_path in fav:
        fav.discard(rel_path)
    else:
        fav.add(rel_path)
    save_favorites(fav)
    
    return RedirectResponse(
        url=f"/research/view?rel_path={rel_path}",
        status_code=303
    )


# ======= 라우트: 미디어 서빙 =======

@app.get("/media/{rel_path:path}", name="serve_media")
async def serve_media(rel_path: str) -> FileResponse:
    target = safe_join(rel_path)
    if not target.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(path=str(target))


# ======= 실행 =======

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting server on 0.0.0.0:8151")
    uvicorn.run("main:app", host="0.0.0.0", port=8151, reload=True)
