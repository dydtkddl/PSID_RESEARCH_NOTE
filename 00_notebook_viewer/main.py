#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
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
    Body,
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
import markdown as md_lib  # pip install markdown

try:
    from docx import Document  # type: ignore
except ImportError:
    Document = None

# ======= 기본 설정 =======

ROOT_DIR = Path(r"C:\Users\PSID_PC_20\Desktop\Reseach_Note").expanduser().resolve()
LOG_FILE = "notebook_viewer.log"
THEME_CONFIG_PATH = Path("themes.json")

# 즐겨찾기 / 최근 문서 / 노트 템플릿 관련 경로
FAVORITES_PATH = Path("favorites.json")
RECENT_PATH = Path("recent.json")
NOTE_TEMPLATES_DIR = Path("note_templates")

MAX_RECENT = 50

DEFAULT_THEME: Dict[str, str] = {
    "card_bg": "#ffffff",
    "card_border": "#dddddd",
    "accent": "#1f7aec",
    "header_bg": "#222222",
}

TEXT_EXTS = {
    ".txt",
    ".md",
    ".py",
    ".rtf",
    ".csv",
    ".json",
    ".yml",
    ".yaml",
    ".log",
}

# Markdown 확장
MD_EXTENSIONS = [
    "extra",
    "tables",
    "fenced_code",
    "codehilite",
    "toc",
    "admonition",
    "sane_lists",
    "smarty",
    "nl2br",
    "meta",
    "footnotes",
    "pymdownx.superfences",
    "pymdownx.tasklist",
    "pymdownx.tilde",
    "pymdownx.highlight",
    "pymdownx.emoji",
    "pymdownx.arithmatex",
]

MD_EXTENSION_CONFIGS = {
    "codehilite": {"guess_lang": False, "noclasses": True},
    "toc": {"permalink": True},
    "pymdownx.tasklist": {"custom_checkbox": True, "clickable_checkbox": False},
    "pymdownx.highlight": {"use_pygments": True, "linenums": False},
    "pymdownx.arithmatex": {"generic": True},
}

TASK_PATTERN = re.compile(r"^\s*[-*]\s+\[( |x|X)\]\s+(.*)$")

# ======= 로깅 =======

logger = logging.getLogger("notebook_viewer")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)

fh = logging.FileHandler(LOG_FILE, encoding="utf-8")
fh.setFormatter(formatter)

sh = logging.StreamHandler()
sh.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(fh)
    logger.addHandler(sh)

logger.info("==== Notebook Viewer starting ====")
logger.info("Markdown extensions enabled: %s", ", ".join(MD_EXTENSIONS))


# ======= 테마 유틸 =======

def load_theme_config() -> Dict[str, Dict[str, str]]:
    if not THEME_CONFIG_PATH.exists():
        logger.info("Theme config not found. Using empty config.")
        return {}

    try:
        with THEME_CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            return data
    except Exception as e:
        logger.exception("Failed to load theme config: %s", e)

    logger.warning("Theme config invalid. Using empty config.")
    return {}


def save_theme_config(cfg: Dict[str, Dict[str, str]]) -> None:
    try:
        with THEME_CONFIG_PATH.open("w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        logger.info("Theme config saved: %s", THEME_CONFIG_PATH)
    except Exception as e:
        logger.exception("Failed to save theme config: %s", e)


def get_theme_for_project(project_rel_path: str) -> Dict[str, str]:
    cfg = load_theme_config()
    theme = cfg.get(project_rel_path, {})
    merged = {**DEFAULT_THEME, **theme}
    return merged


# ======= 공통 유틸 =======

def safe_join(rel_path: str) -> Path:
    """
    ROOT_DIR / rel_path 를 resolve 하고,
    ROOT_DIR 바깥이면 에러.
    """
    root = ROOT_DIR.resolve()
    candidate = (ROOT_DIR / rel_path).resolve()

    if candidate == root:
        return candidate

    if root not in candidate.parents:
        logger.warning("Attempt to access outside root: %s", candidate)
        raise HTTPException(status_code=400, detail="Invalid path")

    return candidate


def read_text_file(path: Path) -> Optional[str]:
    for enc in ("utf-8", "cp949", "latin-1"):
        try:
            with path.open("r", encoding=enc, errors="replace") as f:
                return f.read()
        except Exception:
            continue
    logger.warning("Failed to read text file with known encodings: %s", path)
    return None


def read_docx_file(path: Path) -> Optional[str]:
    if Document is None:
        return None
    try:
        doc = Document(str(path))
        texts = [p.text for p in doc.paragraphs]
        return "\n".join(texts)
    except Exception as e:
        logger.exception("Failed to read docx: %s", e)
        return None


def render_markdown(md_text: str) -> str:
    """
    확장 전부 켠 markdown 렌더링.
    오류 나면 raw text를 <pre>로 반환.
    """
    try:
        html_out = md_lib.markdown(
            md_text,
            extensions=MD_EXTENSIONS,
            extension_configs=MD_EXTENSION_CONFIGS,
            output_format="html5",
        )
        return html_out
    except Exception as e:
        logger.exception("Markdown render failed: %s", e)
        escaped = html.escape(md_text)
        return f"<pre>{escaped}</pre>"


def parse_frontmatter(md_text: str) -> Tuple[Dict[str, Any], str]:
    """
    파일 최상단의 YAML-like frontmatter 파싱
    ---
    key: value
    tags: [a, b]
    ---
    """
    meta: Dict[str, Any] = {}

    if not md_text.startswith("---"):
        return meta, md_text

    end_idx = md_text.find("\n---", 3)
    if end_idx == -1:
        return meta, md_text

    # '---\n' 이후부터 frontmatter 내용
    if md_text.startswith("---\n"):
        fm_text = md_text[4:end_idx]
    else:
        fm_text = md_text[3:end_idx]
    body = md_text[end_idx + 4:]  # '\n---' 이후

    for line in fm_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if not key:
            continue

        # 리스트형(tags 등)
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            items = [
                v.strip().strip("'\"")
                for v in inner.split(",")
                if v.strip()
            ]
            meta[key] = items
        else:
            meta[key] = val.strip().strip("'\"")

    return meta, body.lstrip("\n")


def normalize_tags(meta: Dict[str, Any]) -> List[str]:
    val = meta.get("tags")
    if isinstance(val, list):
        return [str(v).strip() for v in val if str(v).strip()]
    if isinstance(val, str):
        return [t.strip() for t in val.split(",") if t.strip()]
    return []


def extract_tasks_from_markdown(
    md_text: str,
    note_rel_path: str,
) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []
    for idx, line in enumerate(md_text.splitlines(), start=1):
        m = TASK_PATTERN.match(line)
        if not m:
            continue
        status = "done" if m.group(1).lower() == "x" else "open"
        text = m.group(2).strip()
        if not text:
            continue
        tasks.append(
            {
                "rel_path": note_rel_path,
                "line_no": idx,
                "status": status,
                "text": text,
            }
        )
    return tasks


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.exception("Failed to load json %s: %s", path, e)
        return default


def _save_json(path: Path, data) -> None:
    try:
        with path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.exception("Failed to save json %s: %s", path, e)


def load_favorites() -> List[str]:
    data = _load_json(FAVORITES_PATH, [])
    if isinstance(data, list):
        return [str(p) for p in data]
    return []


def save_favorites(favs: List[str]) -> None:
    unique = []
    for r in favs:
        if r not in unique:
            unique.append(r)
    _save_json(FAVORITES_PATH, unique)


def is_favorite(rel_path: str) -> bool:
    favs = load_favorites()
    return rel_path in favs


def register_recent(rel_path: str) -> None:
    """
    최근 문서 목록 관리 (최대 MAX_RECENT개)
    """
    now = datetime.now().isoformat(timespec="seconds")
    data = _load_json(RECENT_PATH, [])
    if not isinstance(data, list):
        data = []

    # 중복 제거 후 맨 앞에 추가
    filtered = [it for it in data if it.get("rel_path") != rel_path]
    filtered.insert(0, {"rel_path": rel_path, "ts": now})
    if len(filtered) > MAX_RECENT:
        filtered = filtered[:MAX_RECENT]

    _save_json(RECENT_PATH, filtered)


def load_recent(limit: int = 10) -> List[Dict[str, Any]]:
    data = _load_json(RECENT_PATH, [])
    if not isinstance(data, list):
        return []
    results: List[Dict[str, Any]] = []

    for item in data[:limit]:
        rel = item.get("rel_path")
        ts = item.get("ts")
        if not isinstance(rel, str):
            continue
        try:
            path = safe_join(rel)
        except HTTPException:
            continue
        if not path.exists() or not path.is_file():
            continue

        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime).strftime(
            "%Y-%m-%d %H:%M"
        )
        rel_norm = rel.replace("\\", "/")
        project_rel_path = rel_norm.split("/")[0] if "/" in rel_norm else ""
        project_name = (
            safe_join(project_rel_path).name if project_rel_path else ""
        )

        results.append(
            {
                "rel_path": rel_norm,
                "file_name": path.name,
                "project_rel_path": project_rel_path,
                "project_name": project_name,
                "view_ts": ts,
                "modified": modified,
            }
        )
    return results


def load_favorite_notes(limit: int = 50) -> List[Dict[str, Any]]:
    favs = load_favorites()
    notes: List[Dict[str, Any]] = []
    for rel in favs[:limit]:
        try:
            path = safe_join(rel)
        except HTTPException:
            continue
        if not path.exists() or not path.is_file():
            continue
        stat = path.stat()
        modified = datetime.fromtimestamp(stat.st_mtime).strftime(
            "%Y-%m-%d %H:%M"
        )
        rel_norm = rel.replace("\\", "/")
        project_rel_path = rel_norm.split("/")[0] if "/" in rel_norm else ""
        project_name = (
            safe_join(project_rel_path).name if project_rel_path else ""
        )

        notes.append(
            {
                "rel_path": rel_norm,
                "file_name": path.name,
                "project_rel_path": project_rel_path,
                "project_name": project_name,
                "modified": modified,
            }
        )
    return notes


def list_note_templates() -> List[Dict[str, Any]]:
    """
    note_templates/*.md 목록
    """
    templates: List[Dict[str, Any]] = []
    if not NOTE_TEMPLATES_DIR.exists():
        return templates

    for p in sorted(NOTE_TEMPLATES_DIR.glob("*.md")):
        templates.append(
            {
                "name": p.stem,
                "file_name": p.name,
            }
        )
    return templates


# ======= 데이터 수집 =======

def get_project_list() -> List[Dict[str, Any]]:
    if not ROOT_DIR.exists():
        logger.error("Root directory does not exist: %s", ROOT_DIR)
        raise FileNotFoundError(f"Root directory not found: {ROOT_DIR}")

    logger.info("Scanning root for projects: %s", ROOT_DIR)

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
        projects.append(
            {
                "name": d.name,
                "rel_path": rel_str,
                "theme": theme,
            }
        )

    logger.info("Found %d projects", len(projects))
    return projects


def list_markdown_files(project_rel_path: str) -> List[Dict[str, Any]]:
    project_root = safe_join(project_rel_path)

    if not project_root.exists() or not project_root.is_dir():
        logger.warning("Project directory not found: %s", project_root)
        raise HTTPException(status_code=404, detail="Project not found")

    logger.info("Listing markdown files in project: %s", project_root)

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
        modified = datetime.fromtimestamp(modified_ts).strftime(
            "%Y-%m-%d %H:%M"
        )

        notes.append(
            {
                "name": p.name,
                "rel_path": rel_str,
                "created": created,
                "modified": modified,
                "created_ts": created_ts,
                "modified_ts": modified_ts,
            }
        )

    logger.info("Listed %d markdown notes", len(notes))
    return notes


def extract_image_paths_from_markdown(
    md_text: str,
    note_rel_path: str,
) -> List[str]:
    """
    - MD 내의 상대 이미지 경로( ![](), <img src=""> )를 찾아서
    - note_rel_path 기준 상대 경로로 변환해서 리스트 반환.

    번들 zip 만들 때 사용.
    """
    logger.info("Extracting image paths from markdown: %s", note_rel_path)
    img_paths: List[str] = []

    note_rel_norm = note_rel_path.replace("\\", "/")
    note_dir_rel = (
        "/".join(note_rel_norm.split("/")[:-1]) if "/" in note_rel_norm else ""
    )

    # 1) ![](path)
    md_img_pattern = re.compile(r"!\[[^\]]*]\(([^)]+)\)")
    for match in md_img_pattern.findall(md_text):
        src = match.strip()
        if (
            " " in src
            and not src.startswith(("http://", "https://", "data:", "/"))
        ):
            src = src.split(" ")[0]

        if src.startswith(("http://", "https://", "data:")):
            continue

        if src.startswith("/research/media/"):
            rel = src[len("/research/media/") :]
        else:
            if note_dir_rel:
                rel = f"{note_dir_rel}/{src}"
            else:
                rel = src

        rel_norm = str(Path(rel)).replace("\\", "/")
        img_paths.append(rel_norm)

    # 2) <img src="...">
    html_img_pattern = re.compile(
        r'<img[^>]+src=["\']([^"\']+)["\']',
        re.IGNORECASE,
    )
    for src in html_img_pattern.findall(md_text):
        src = src.strip()
        if src.startswith(("http://", "https://", "data:")):
            continue

        if src.startswith("/research/media/"):
            rel = src[len("/research/media/") :]
        else:
            if note_dir_rel:
                rel = f"{note_dir_rel}/{src}"
            else:
                rel = src
        rel_norm = str(Path(rel)).replace("\\", "/")
        img_paths.append(rel_norm)

    uniq = sorted(set(img_paths))
    logger.info("Found %d image paths", len(uniq))
    return uniq


# ======= FastAPI 앱 =======

app = FastAPI(
    title="연구노트 뷰어",
    root_path="/research",
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


# ======= 예외 핸들러 =======

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    logger.error(
        "HTTP error %s on %s %s",
        exc.status_code,
        request.method,
        request.url.path,
    )
    return PlainTextResponse(
        str(exc.detail),
        status_code=exc.status_code,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path,
    )
    return PlainTextResponse(
        "서버 내부 오류가 발생했습니다.",
        status_code=500,
    )


# ======= 라우트: 인덱스 =======

@app.get("/", response_class=HTMLResponse, name="index")
async def index(request: Request) -> HTMLResponse:
    logger.info("GET / - index (project list)")
    projects = get_project_list()
    recent_notes = load_recent(limit=8)
    favorite_notes = load_favorite_notes(limit=8)

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


# ======= 라우트: 프로젝트 리스트뷰 (정렬 / 검색 / 페이지) =======

@app.get("/project", response_class=HTMLResponse, name="project_view")
async def project_view(
    request: Request,
    rel_path: str = Query(..., description="ROOT 기준 프로젝트 디렉토리 경로"),
    sort: str = Query("modified", description="정렬 기준: name|created|modified"),
    order: str = Query("desc", description="정렬 방향: asc|desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=200),
    q: Optional[str] = Query(None, description="파일명/경로 검색어"),
) -> HTMLResponse:
    logger.info(
        "GET /project (rel_path=%s, sort=%s, order=%s, page=%s, page_size=%s, q=%s)",
        rel_path,
        sort,
        order,
        page,
        page_size,
        q,
    )

    project_dir = safe_join(rel_path)
    if not project_dir.exists() or not project_dir.is_dir():
        logger.warning("Project not found for view: %s", project_dir)
        raise HTTPException(status_code=404, detail="Project not found")

    theme = get_theme_for_project(rel_path)
    all_notes = list_markdown_files(rel_path)

    # 검색
    if q:
        q_lower = q.lower()
        filtered = [
            n
            for n in all_notes
            if q_lower in n["name"].lower()
            or q_lower in n["rel_path"].lower()
        ]
    else:
        filtered = all_notes

    # 정렬
    sort_key = sort.lower()
    reverse = order.lower() == "desc"

    def key_func(n: Dict[str, Any]):
        if sort_key == "name":
            return n["name"].lower()
        elif sort_key == "created":
            return n["created_ts"]
        else:
            return n["modified_ts"]

    filtered.sort(key=key_func, reverse=reverse)

    # 페이지네이션
    total = len(filtered)
    total_pages = max((total + page_size - 1) // page_size, 1)
    if page > total_pages:
        page = total_pages

    start = (page - 1) * page_size
    end = start + page_size
    page_notes = filtered[start:end]

    favs_set = set(load_favorites())
    for n in page_notes:
        n["is_favorite"] = n["rel_path"] in favs_set

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


# ======= 라우트: 전역 검색 =======

@app.get("/search", response_class=HTMLResponse, name="search_view")
async def search_view(
    request: Request,
    q: str = Query("", description="검색어 (비워두면 태그/상태만으로 검색 가능)"),
    tag: Optional[str] = Query(None, description="frontmatter tags 필터"),
    status: Optional[str] = Query(None, description="frontmatter status 필터"),
) -> HTMLResponse:
    logger.info("GET /search (q=%s, tag=%s, status=%s)", q, tag, status)

    q_strip = q.strip()
    tag_strip = (tag or "").strip()
    status_strip = (status or "").strip().lower()

    results: List[Dict[str, Any]] = []

    # 아무 필터도 없으면 아직 검색 안 한 상태로 간주
    if not q_strip and not tag_strip and not status_strip:
        return templates.TemplateResponse(
            "search.html",
            {
                "request": request,
                "q": "",
                "tag": "",
                "status": "",
                "results": [],
                "searched": False,
            },
        )

    logger.info("Starting global search over markdown files...")
    all_md = sorted(
        ROOT_DIR.rglob("*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    for p in tqdm(all_md, desc="Global search", unit="file"):
        rel = p.relative_to(ROOT_DIR)
        rel_str = str(rel).replace("\\", "/")

        text = read_text_file(p)
        if text is None:
            continue

        meta, body = parse_frontmatter(text)
        tags = normalize_tags(meta)
        fm_status = str(meta.get("status", "")).strip().lower()

        # 태그 필터
        if tag_strip:
            if tag_strip not in tags:
                continue

        # 상태 필터
        if status_strip:
            if fm_status != status_strip:
                continue

        # 검색어 필터
        if q_strip:
            q_lower = q_strip.lower()
            if q_lower not in body.lower() and q_lower not in p.name.lower():
                continue

            idx = body.lower().find(q_lower)
            snippet = ""
            if idx != -1:
                start = max(0, idx - 80)
                end = min(len(body), idx + 80)
                snippet = body[start:end].replace("\n", " ")
        else:
            snippet = body[:160].replace("\n", " ")

        stat = p.stat()
        modified = datetime.fromtimestamp(stat.st_mtime).strftime(
            "%Y-%m-%d %H:%M"
        )
        project_rel_path = rel_str.split("/")[0] if "/" in rel_str else ""
        project_name = (
            safe_join(project_rel_path).name if project_rel_path else ""
        )

        results.append(
            {
                "rel_path": rel_str,
                "file_name": p.name,
                "project_rel_path": project_rel_path,
                "project_name": project_name,
                "tags": tags,
                "status": fm_status,
                "snippet": snippet,
                "modified": modified,
            }
        )

    favs_set = set(load_favorites())
    for r in results:
        r["is_favorite"] = r["rel_path"] in favs_set

    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "q": q_strip,
            "tag": tag_strip,
            "status": status_strip,
            "results": results,
            "searched": True,
        },
    )


# ======= 라우트: TODO / Task 전역 뷰 =======

@app.get("/tasks", response_class=HTMLResponse, name="tasks_view")
async def tasks_view(request: Request) -> HTMLResponse:
    logger.info("GET /tasks - collecting tasks from markdown files")

    all_md = sorted(ROOT_DIR.rglob("*.md"))
    open_tasks: List[Dict[str, Any]] = []
    done_tasks: List[Dict[str, Any]] = []

    for p in tqdm(all_md, desc="Scanning tasks", unit="file"):
        rel = p.relative_to(ROOT_DIR)
        rel_str = str(rel).replace("\\", "/")
        text = read_text_file(p)
        if text is None:
            continue

        meta, body = parse_frontmatter(text)
        tags = normalize_tags(meta)
        fm_status = str(meta.get("status", "")).strip().lower()

        tasks = extract_tasks_from_markdown(body, rel_str)
        if not tasks:
            continue

        project_rel_path = rel_str.split("/")[0] if "/" in rel_str else ""
        project_name = (
            safe_join(project_rel_path).name if project_rel_path else ""
        )

        for t in tasks:
            data = {
                "rel_path": t["rel_path"],
                "line_no": t["line_no"],
                "status": t["status"],
                "text": t["text"],
                "project_rel_path": project_rel_path,
                "project_name": project_name,
                "tags": tags,
                "note_status": fm_status,
                "file_name": p.name,
            }
            if t["status"] == "done":
                done_tasks.append(data)
            else:
                open_tasks.append(data)

    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "open_tasks": open_tasks,
            "done_tasks": done_tasks,
        },
    )


# ======= 라우트: 테마 설정 =======

@app.get("/settings", response_class=HTMLResponse, name="settings_view")
async def settings_view(
    request: Request,
    rel_path: str = Query(..., description="ROOT 기준 프로젝트 디렉토리 경로"),
) -> HTMLResponse:
    logger.info("GET /settings?rel_path=%s", rel_path)

    project_dir = safe_join(rel_path)
    if not project_dir.exists() or not project_dir.is_dir():
        logger.warning("Project not found for settings: %s", project_dir)
        raise HTTPException(status_code=404, detail="Project not found")

    theme = get_theme_for_project(rel_path)

    return templates.TemplateResponse(
        "settings.html",
        {
            "request": request,
            "project_name": project_dir.name,
            "project_rel_path": rel_path,
            "theme": theme,
            "default_theme": DEFAULT_THEME,
        },
    )


@app.post("/settings", response_class=HTMLResponse)
async def settings_save(
    rel_path: str = Form(...),
    card_bg: str = Form(...),
    card_border: str = Form(...),
    accent: str = Form(...),
    header_bg: str = Form(...),
) -> RedirectResponse:
    logger.info("POST /settings for rel_path=%s", rel_path)

    new_theme = {
        "card_bg": card_bg or DEFAULT_THEME["card_bg"],
        "card_border": card_border or DEFAULT_THEME["card_border"],
        "accent": accent or DEFAULT_THEME["accent"],
        "header_bg": header_bg or DEFAULT_THEME["header_bg"],
    }

    cfg = load_theme_config()
    cfg[rel_path] = new_theme
    save_theme_config(cfg)

    return RedirectResponse(
        url=f"/research/project?rel_path={rel_path}",
        status_code=303,
    )


# ======= 라우트: 상세 보기 =======

@app.get("/view", response_class=HTMLResponse, name="view_file")
async def view_file(
    request: Request,
    rel_path: str = Query(..., description="ROOT 기준 상대 파일 경로"),
) -> HTMLResponse:
    logger.info("GET /view (view %s)", rel_path)

    target = safe_join(rel_path)
    if not target.exists() or not target.is_file():
        logger.warning("File not found: %s", target)
        raise HTTPException(status_code=404, detail="File not found")

    rel_norm = rel_path.replace("\\", "/")
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
                other_notes = [
                    n for n in all_notes if n["rel_path"] != rel_norm
                ]
        except Exception as e:
            logger.exception("Error while listing other notes: %s", e)

    # 최근 문서에 기록
    register_recent(rel_norm)

    ext = target.suffix.lower()
    is_pdf = ext == ".pdf"
    is_hwp = ext in {".hwp", ".hwpx"}
    is_docx = ext == ".docx"
    is_text = ext in TEXT_EXTS
    is_markdown = ext == ".md"

    text_content: Optional[str] = None
    html_content: Optional[str] = None
    unsupported_reason: Optional[str] = None
    frontmatter_meta: Dict[str, Any] = {}
    meta_tags: List[str] = []
    meta_status: str = ""

    try:
        if is_markdown:
            raw_text = read_text_file(target)
            if raw_text is None:
                unsupported_reason = "Markdown 파일을 읽을 수 없습니다."
            else:
                frontmatter_meta, body = parse_frontmatter(raw_text)
                meta_tags = normalize_tags(frontmatter_meta)
                meta_status = str(frontmatter_meta.get("status", "")).strip()
                html_content = render_markdown(body)

        elif is_text:
            raw_text = read_text_file(target)
            if raw_text is None:
                unsupported_reason = "텍스트 파일을 읽을 수 없습니다."
            else:
                text_content = raw_text

        elif is_docx:
            raw_text = read_docx_file(target)
            if raw_text is None:
                if Document is None:
                    unsupported_reason = (
                        "python-docx가 설치되어 있지 않습니다. "
                        "(pip install python-docx)"
                    )
                else:
                    unsupported_reason = (
                        "docx 파일을 읽는 중 오류가 발생했습니다."
                    )
            else:
                text_content = raw_text

        elif is_pdf:
            # embed로 직접 보기
            pass

        elif is_hwp:
            unsupported_reason = "HWP/HWXP 파일은 미리보기 미지원 (다운로드만 가능)"

        else:
            unsupported_reason = f"미리보기를 지원하지 않는 형식입니다: {ext}"
    except Exception as e:
        logger.exception("Error while preparing file content: %s", e)
        raise HTTPException(
            status_code=500,
            detail="파일 내용을 처리하는 중 오류가 발생했습니다.",
        )

    download_bundle_url = request.url_for("download_bundle", rel_path=rel_path)
    download_file_url = request.url_for("download_file", rel_path=rel_path)

    note_dir_rel = (
        "/".join(rel_norm.split("/")[:-1]) if "/" in rel_norm else ""
    )
    media_base_url: Optional[str] = None
    if note_dir_rel:
        media_base_url = str(
            request.url_for("serve_media", rel_path=note_dir_rel)
        )

    fav_flag = is_favorite(rel_norm)

    return templates.TemplateResponse(
        "viewer.html",
        {
            "request": request,
            "rel_path": rel_path,
            "file_name": target.name,
            "file_type": ext or "파일",
            "is_pdf": is_pdf,
            "html_content": html_content,
            "text_content": text_content,
            "unsupported_reason": unsupported_reason,
            "download_bundle_url": str(download_bundle_url),
            "download_md_url": str(download_file_url),
            "project_rel_path": project_rel_path,
            "project_name": project_name,
            "other_notes": other_notes,
            "theme": theme,
            "media_base_url": media_base_url,
            "is_markdown": is_markdown,
            "frontmatter": frontmatter_meta,
            "meta_tags": meta_tags,
            "meta_status": meta_status,
            "is_favorite": fav_flag,
        },
    )


# ======= 라우트: 새 문서 생성 =======

@app.get("/new", response_class=HTMLResponse, name="new_file")
async def new_file(
    request: Request,
    rel_path: str = Query(..., description="ROOT 기준 프로젝트 디렉토리 경로"),
) -> HTMLResponse:
    logger.info("GET /new (project=%s)", rel_path)

    project_dir = safe_join(rel_path)
    if not project_dir.exists() or not project_dir.is_dir():
        raise HTTPException(status_code=404, detail="Project not found")

    theme = get_theme_for_project(rel_path)
    templates_list = list_note_templates()

    return templates.TemplateResponse(
        "new.html",
        {
            "request": request,
            "project_rel_path": rel_path,
            "project_name": project_dir.name,
            "theme": theme,
            "note_templates": templates_list,
        },
    )


@app.post("/new", response_class=HTMLResponse)
async def create_file(
    request: Request,
    project_rel_path: str = Form(...),
    title: str = Form(...),
    content: str = Form(""),
) -> RedirectResponse:
    logger.info(
        "POST /new (project=%s, title=%s)",
        project_rel_path,
        title,
    )

    if not title.strip():
        raise HTTPException(status_code=400, detail="제목은 필수입니다.")

    raw_name = title.strip()
    if not raw_name.lower().endswith(".md"):
        raw_name += ".md"

    safe_name = re.sub(r'[\\/:*?"<>|]', "_", raw_name)

    rel = str(Path(project_rel_path) / safe_name).replace("\\", "/")
    target = safe_join(rel)

    if target.exists():
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_name = f"{Path(safe_name).stem}_{ts}.md"
        rel = str(Path(project_rel_path) / safe_name).replace("\\", "/")
        target = safe_join(rel)

    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8", errors="replace") as f:
        f.write(content)

    logger.info("Created new note: %s", target)

    view_url = request.url_for("view_file")
    redirect_url = f"{view_url}?rel_path={rel}"
    return RedirectResponse(url=redirect_url, status_code=303)


# ======= 라우트: 기존 문서 수정 =======

@app.get("/edit", response_class=HTMLResponse, name="edit_file")
async def edit_file(
    request: Request,
    rel_path: str = Query(..., description="ROOT 기준 상대 파일 경로"),
) -> HTMLResponse:
    logger.info("GET /edit (rel_path=%s)", rel_path)

    target = safe_join(rel_path)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    if target.suffix.lower() != ".md":
        raise HTTPException(
            status_code=400, detail="현재는 .md 파일만 웹에서 수정 가능합니다."
        )

    raw_text = read_text_file(target)
    if raw_text is None:
        raise HTTPException(status_code=500, detail="파일을 읽을 수 없습니다.")

    rel_norm = rel_path.replace("\\", "/")
    note_dir_rel = (
        "/".join(rel_norm.split("/")[:-1]) if "/" in rel_norm else ""
    )

    project_rel_path = rel_norm.split("/")[0] if "/" in rel_norm else ""
    theme = (
        get_theme_for_project(project_rel_path)
        if project_rel_path
        else DEFAULT_THEME
    )

    image_base_dir = note_dir_rel or project_rel_path or ""

    media_base_url: Optional[str] = None
    if note_dir_rel:
        media_base_url = str(
            request.url_for("serve_media", rel_path=note_dir_rel)
        )

    return templates.TemplateResponse(
        "edit.html",
        {
            "request": request,
            "rel_path": rel_path,
            "file_name": target.name,
            "raw_content": raw_text,
            "image_base_dir": image_base_dir,
            "theme": theme,
            "media_base_url": media_base_url,
        },
    )


@app.post("/save", response_class=HTMLResponse, name="save_file")
async def save_file(
    request: Request,
    rel_path: str = Form(...),
    content: str = Form(...),
) -> RedirectResponse:
    logger.info("POST /save (rel_path=%s)", rel_path)

    target = safe_join(rel_path)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    # 간단 백업 (원본을 .bak-타임스탬프 로 복사)
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = target.with_suffix(
            target.suffix + f".bak-{ts}"
        )
        shutil.copy2(target, backup_path)
        logger.info("Backup created: %s", backup_path)
    except Exception as e:
        logger.exception("Failed to create backup for %s: %s", target, e)

    with target.open("w", encoding="utf-8", errors="replace") as f:
        f.write(content)

    logger.info("Saved file: %s", target)

    view_url = request.url_for("view_file")
    redirect_url = f"{view_url}?rel_path={rel_path}"
    return RedirectResponse(url=redirect_url, status_code=303)


# ======= 라우트: 라이브 프리뷰 =======

@app.post("/render_preview")
async def render_preview(payload: Dict[str, str] = Body(...)) -> Dict[str, str]:
    """
    에디터용 라이브 프리뷰 API
    frontmatter는 렌더링에서 제외하고 본문만 렌더링
    """
    md_text = payload.get("markdown", "")
    meta, body = parse_frontmatter(md_text)
    html_out = render_markdown(body)
    return {"html": html_out}


# ======= 라우트: 이미지 업로드 (Ctrl+V 등) =======

@app.post("/upload_image", name="upload_image")
async def upload_image(
    base_rel_dir: str = Form(..., description="이미지를 저장할 기준 폴더 (ROOT 기준 상대경로)"),
    image: UploadFile = File(...),
):
    logger.info(
        "POST /upload_image (base_rel_dir=%s, filename=%s)",
        base_rel_dir,
        image.filename,
    )

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

    logger.info("Saved pasted image: %s", save_path)

    # MD에서 note 기준 폴더에서의 상대경로
    md_path = f"_images/{fname}"
    return {"ok": True, "md_path": md_path}


# ======= 라우트: 템플릿 내용 조회 =======

@app.get("/note_template", name="note_template_content")
async def note_template_content(
    name: str = Query(..., description="템플릿 파일명 (예: template_review.md)"),
) -> PlainTextResponse:
    logger.info("GET /note_template (name=%s)", name)

    tpl_path = NOTE_TEMPLATES_DIR / name
    if not tpl_path.exists() or not tpl_path.is_file():
        raise HTTPException(status_code=404, detail="Template not found")

    text = read_text_file(tpl_path)
    if text is None:
        raise HTTPException(status_code=500, detail="템플릿을 읽을 수 없습니다.")
    return PlainTextResponse(text)


# ======= 라우트: 프로젝트 폴더 기반 media 서빙 =======

@app.get("/media/{rel_path:path}", name="serve_media")
async def serve_media(rel_path: str) -> FileResponse:
    logger.info("GET /media/%s", rel_path)
    target = safe_join(rel_path)

    if not target.exists() or not target.is_file():
        logger.warning("Media file not found: %s", target)
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=str(target))


# ======= 라우트: 단일 파일 다운로드 =======

@app.get("/download/{rel_path:path}", name="download_file")
async def download_file(rel_path: str) -> FileResponse:
    target = safe_join(rel_path)

    if not target.exists() or not target.is_file():
        logger.warning("Download - file not found: %s", target)
        raise HTTPException(status_code=404, detail="File not found")

    logger.info("Download file: %s", target)
    return FileResponse(
        path=str(target),
        filename=target.name,
        media_type="application/octet-stream",
    )


# ======= 라우트: MD + 이미지 ZIP 번들 =======

@app.get("/download_bundle/{rel_path:path}", name="download_bundle")
async def download_bundle(rel_path: str) -> StreamingResponse:
    logger.info("GET /download_bundle/%s", rel_path)

    target = safe_join(rel_path)
    if not target.exists() or not target.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    if target.suffix.lower() != ".md":
        raise HTTPException(
            status_code=400, detail="MD 파일에 대해서만 번들 다운로드를 지원합니다."
        )

    md_text = read_text_file(target)
    if md_text is None:
        raise HTTPException(status_code=500, detail="MD 파일을 읽을 수 없습니다.")

    img_rel_paths = extract_image_paths_from_markdown(md_text, rel_path)

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        # MD 파일
        zf.write(str(target), arcname=target.name)
        # 이미지들
        for img_rel in img_rel_paths:
            try:
                img_path = safe_join(img_rel)
            except HTTPException:
                continue
            if not img_path.exists() or not img_path.is_file():
                continue
            arcname = f"images/{img_path.name}"
            zf.write(str(img_path), arcname=arcname)

    buf.seek(0)
    zip_name = f"{target.stem}_bundle.zip"
    logger.info(
        "Bundle ZIP created for %s with %d images",
        target,
        len(img_rel_paths),
    )

    headers = {
        "Content-Disposition": f'attachment; filename="{zip_name}"'
    }
    return StreamingResponse(
        buf,
        media_type="application/zip",
        headers=headers,
    )


# ======= 라우트: 즐겨찾기 토글 =======

@app.get("/favorite/toggle", name="toggle_favorite")
async def toggle_favorite(request: Request, rel_path: str = Query(...)) -> RedirectResponse:
    logger.info("GET /favorite/toggle (rel_path=%s)", rel_path)
    favs = load_favorites()
    if rel_path in favs:
        favs = [r for r in favs if r != rel_path]
        logger.info("Removed from favorites: %s", rel_path)
    else:
        favs.insert(0, rel_path)
        logger.info("Added to favorites: %s", rel_path)
    save_favorites(favs)

    referer = request.headers.get("referer")
    if referer:
        return RedirectResponse(url=referer, status_code=303)

    view_url = request.url_for("view_file")
    redirect_url = f"{view_url}?rel_path={rel_path}"
    return RedirectResponse(url=redirect_url, status_code=303)


# ======= 라우트: 로그 뷰어 =======

@app.get("/debug/log", response_class=HTMLResponse, name="debug_log_view")
async def debug_log_view(request: Request) -> HTMLResponse:
    logger.info("GET /debug/log")
    try:
        with open(LOG_FILE, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        tail = "".join(lines[-500:])
    except Exception as e:
        logger.exception("Failed to read log file: %s", e)
        tail = "로그를 읽는 중 오류가 발생했습니다."

    return templates.TemplateResponse(
        "log.html",
        {
            "request": request,
            "log_text": tail,
        },
    )


# ======= 개발용 실행 =======

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8151, reload=True)
