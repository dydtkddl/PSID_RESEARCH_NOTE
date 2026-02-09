
---
title: "Troubleshooting: PDF 변환 시 수식 깨짐 및 Windows Asyncio 호환성 문제 해결"
date: 2025-12-19
tags: [fastapi, playwright, pdf, asyncio, windows, troubleshooting]
author: 안용상
status: Resolved
---

## 1. 개요 (Overview)

연구노트 뷰어에서 **Markdown 노트를 PDF로 내보낼 때**, LaTeX 수식(MathJax)이 렌더링되지 않고 원본 텍스트(`$ ... $`) 그대로 나오거나 깨지는 문제가 발생함. 이를 해결하기 위해 렌더링 엔진을 교체하는 과정에서 Windows 환경의 비동기(Asyncio) 이벤트 루프 충돌 문제가 발생하여 이를 해결함.

---

## 2. 초기 문제 (Initial Issue)

### 증상
- 웹 뷰어에서는 `$E=mc^2$` 등의 수식이 정상적으로 렌더링됨.
- **PDF 다운로드** 시에는 수식이 렌더링되지 않고 `$E=mc^2$` 텍스트 그대로 출력되거나 깨짐.

### 원인
- 기존에 사용하던 `markdown-pdf` 라이브러리는 정적인 HTML/CSS만 해석할 뿐, **JavaScript(MathJax)를 실행하지 못함**.
- 따라서 브라우저에서 동적으로 그려주는 수식을 PDF에 담을 수 없음.

### 해결 전략
- **Playwright** 도입: Headless Browser(Chromium)를 띄워 실제 웹페이지처럼 MathJax를 로딩 및 렌더링한 후, 그 화면을 PDF로 인쇄(Print to PDF)하는 방식으로 변경.

---

## 3. 기술적 이슈 (Technical Issue)

Playwright 코드로 변경 후 PDF 생성 요청 시 서버 내부 오류(500) 발생.

### 에러 로그
```text
File "...\asyncio\base_events.py", line 498, in _make_subprocess_transport
    raise NotImplementedError
NotImplementedError

```

### 원인 분석

1. **Windows와 Asyncio:** Windows의 기본 Event Loop인 `SelectorEventLoop`는 `asyncio.create_subprocess_exec` (Playwright가 브라우저를 띄울 때 사용)를 지원하지 않음.
2. **ProactorEventLoop 필요:** Windows에서 Subprocess를 비동기로 다루기 위해서는 `ProactorEventLoop`를 사용해야 함.
3. **Uvicorn의 Reload 간섭:** 코드 상단에 정책 변경 코드를 넣었음에도, `uvicorn.run(..., reload=True)` 옵션을 사용하면 Uvicorn이 파일 변경 감지를 위해 **새로운 자식 프로세스(Worker)**를 띄우면서 이벤트 루프 설정을 **기본값(Selector)으로 초기화**해버림.

---

## 4. 최종 해결 방법 (Solution)

### 4.1. Event Loop 정책 강제 설정 (`main.py`)

Windows 환경일 경우, 앱이 시작되기 전(전역 범위)에 `ProactorEventLoopPolicy`를 적용하도록 설정.

```python
# main.py 최상단 (import 직후)
import sys
import asyncio

if sys.platform == "win32":
    # Windows에서 Playwright(Subprocess) 사용을 위해 필수
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

```

### 4.2. 실행 옵션 변경 (`uvicorn.run`)

`reload=True`를 비활성화하고, 이벤트 루프 정책이 유지되도록 `loop="asyncio"` 옵션을 명시함.

```python
# main.py 최하단
if __name__ == "__main__":
    import uvicorn
    import sys
    import asyncio

    # 안전장치: 실행 시점에도 정책 적용
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8151,
        reload=False,       # [중요] True로 설정 시 Worker 프로세스에서 설정이 초기화됨
        loop="asyncio"      # [중요] 사용자가 설정한 정책을 따르도록 강제
    )

```

### 4.3. 실행 커맨드 변경

터미널에서 `uvicorn` 명령어를 직접 사용하는 대신, 파이썬 스크립트를 직접 실행하여 위 설정을 적용받도록 함.

```bash
# (X) 이렇게 실행하면 안 됨 (설정 무시됨)
uvicorn main:app --reload

# (O) 이렇게 실행해야 함
python main.py

```

### 4.4. 좀비 프로세스 정리 (Port 8151)

테스트 중 서버가 비정상 종료되어 포트가 점유된 경우 해결.

```cmd
# 1. PID 찾기
netstat -ano | findstr :8151

# 2. 강제 종료 (PID가 14684인 경우)
taskkill /PID 14684 /F

```

---

## 5. 결과 (Result)

* **MathJax 렌더링:** PDF 내 수식이 웹 뷰어와 동일한 고품질 벡터 이미지로 저장됨.
* **이미지 경로:** 로컬 이미지 파일들도 깨지지 않고 PDF에 정상 포함됨.
* **안정성:** Windows 환경에서 `NotImplementedError` 없이 안정적으로 브라우저 인스턴스가 생성 및 종료됨.

```
