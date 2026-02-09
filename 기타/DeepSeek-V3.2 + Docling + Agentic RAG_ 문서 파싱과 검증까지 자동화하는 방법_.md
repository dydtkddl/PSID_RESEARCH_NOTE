---
title: "DeepSeek-V3.2 + Docling + Agentic RAG: 문서 파싱과 검증까지 자동화하는 방법"
source: "Towards AI (Medium) · Gao Dalie (高達烈)"
note: "배너/추천/홍보 문구 제거, 본문 줄글+코드 포함. 코드는 원문 유지(번역 없음)."
---


---

# 전체 줄글 번역 (배너/추천/홍보 제거, 코드 포함)

오픈소스 논리적 모델링을 계속 지켜봐 왔다면, 이 분야가 매우 경쟁적으로 변했다는 걸 알 것이다. 몇 달마다 새로운 모델이 등장해 기존 한계를 깼다고 말하고, 그중 일부는 실제로 그러기도 한다.

불과 이틀 전, 내가 조용히 시험을 마치고 집중 모드로 들어간 뒤 밤늦게 온라인을 스크롤하고 있었다. DeepSeek는 늘 그렇듯 AI 커뮤니티에 충격파를 던졌다.

DeepSeek는 에이전트를 위해 만들어진 최신 모델인 “DeepSeek-V3.2”와 그 고성능 버전을 출시했다.

이 모델들은 효율적인 희소 어텐션과 대규모 강화학습 같은 기술적 혁신을 결합하면서 추론 능력을 크게 개선했다.

DeepSeek-V3.2는 GPT-5와 정면으로 겨룰 수 있고, 장기적 사고와 정리(정리 증명) 역량을 결합한 Speciale는 Gemini-3.0-Pro에 필적하는 성능을 보인다고 한다. 한 독자는 “이 모델은 V3.2라고 부르면 안 되고 V4라고 불러야 한다”고 댓글을 남겼다.

특히 Speciale 버전은 2025년 IMO, IOI, ICPC 월드 챔피언십에서 금메달급 결과를 달성했고, ICPC 월드 챔피언십에서는 상위 2위 안에, IOI에서는 상위 10위 안에 들어 “금메달 성능”을 달성했다고 한다.

내 연구·개발 과정에서는 PDF에서 텍스트 데이터를 가능한 한 정확하게 추출해야 했다. 과거에는 PyMuPDF나 OCR 엔진인 Tesseract를 사용해 PDF에서 텍스트를 추출해 왔다.

이 도구들은 강력하며 수년 동안 많은 프로젝트에서 사용되어 왔다. 하지만 이번에 작업하던 PDF의 특성 때문인지, 다음과 같은 문제를 겪었다.

IBM Research가 개발한 오픈소스 라이브러리 Docling은 이러한 문제를 해결하는 효과적인 솔루션이다. Docling은 PDF와 Word 같은 문서를 구조화하고, Markdown 같은 형식으로 변환할 수 있는 강력한 도구다.

(중간 서술 전환)

이제 내가 무슨 뜻인지 보여주기 위해 라이브 챗봇 데모를 빠르게 보여주겠다.

Ocean AI PDF를 업로드한 다음, 챗봇에게 이렇게 질문할 것이다.
“Ocean AI란 무엇이고, Ocean AI는 OpenAI와 어떻게 다른가?”

챗봇이 출력 결과를 생성하는 방식을 보면, 에이전트가 먼저 **관련성 검사**를 수행해 질문이 실제로 업로드한 문서와 관련이 있는지 판단한다. 관련이 없다면, 환각(hallucination) 답변을 만들어내는 대신 즉시 질문을 거부한다.

관련 있는 질문이라면, 에이전트는 문서를 Markdown이나 JSON 같은 **구조화된 형식**으로 파싱한다. 그다음 BM25 키워드 검색과 벡터 임베딩을 모두 사용하는 **하이브리드 검색**을 수행해, 여러 문서에 걸쳐서라도 가장 관련 있는 섹션을 찾는다.

Research Agent는 이렇게 검색된 내용을 바탕으로 답변을 생성하고, Verification Agent는 원문 문서와 대조해 사실 정확성을 확인하며 근거 없는 주장이나 모순을 잡아낸다.

검증에 실패하면, 자기 수정 루프가 조정된 파라미터로 검색과 리서치를 자동으로 다시 실행하고, 모든 검사를 통과할 때까지 반복한다. 답변이 완전히 검증되면 에이전트가 최종 답변을 반환한다. 어떤 단계에서든 질문이 업로드한 콘텐츠와 무관하다고 판정되면, 환각으로 꾸며내지 않고 그 사실을 명확히 알려준다.

## DeepSeek-V3.2는 무엇이 특별한가?
대부분의 강력한 AI 모델은 공통된 문제를 겪는다. 파일 길이가 길어질수록 모델 실행 속도는 크게 떨어지고 비용은 급격히 상승한다. 전통적인 모델이 문맥을 이해하기 위해 각 단어를 다른 모든 단어와 비교하려 하기 때문이다.

DeepSeek-V3.2는 DeepSeek Sparse Attention(DSA)이라는 새로운 방법을 도입해 이 문제를 해결한다. 이를 도서관에서 연구하는 연구자에 비유할 수 있다.

- 전통 방식(집약 어텐션): 연구자가 질문 하나에 답하려고 서가의 모든 책을 페이지마다 전부 읽는다. 포괄적이지만 극도로 느리고 엄청난 노력이 든다.
- 새로운 방식(DeepSeek-V3.2): 연구자가 디지털 색인(Lightning Indexer)을 사용해 핵심 페이지를 빠르게 찾아 그 부분만 읽는다. 정확도는 유지하면서 훨씬 빠르다.

## Docling은 무엇이 특별한가?
Docling이 기존 도구들과 비교해 돋보이는 가장 큰 이유는, 생성형 AI—특히 RAG(Retrieval Augmented Generation)—와의 협업을 전제로 설계되었다는 점이다.

현대 AI 애플리케이션은 단순히 텍스트를 추출하는 것만으로는 부족하다. AI가 문서 내용을 깊이 이해하고 정확한 답을 생성하려면, 다음과 같은 의미까지 알아야 한다.

- 이 문장이 논문의 “초록(abstract)”인지 “결론(conclusion)”인지?
- 숫자 문자열이 단순 텍스트가 아니라 “표(table)”라면, 각 셀의 의미는 무엇인지?
- 이 이미지에 붙어 있는 “캡션(caption)”은 무엇인지?

PyMuPDF와 Tesseract가 텍스트를 “문자열”로 추출하는 반면, Docling은 비전-언어 모델(VLM)의 힘을 활용해 이러한 구조와 관계를 분석하고, 풍부한 정보를 담은 “DoclingDocument” 객체로 출력한다.

이 구조화된 데이터가 RAG의 검색(retrieval)과 답변 생성 품질을 크게 끌어올리는 핵심이다.

## 코딩 시작
이제 RagAnything와 멀티모달 RAG를 어떻게 사용하는지 단계별로 살펴보자. 모델을 지원하는 라이브러리를 설치하기 위해 requirements를 pip로 설치한다.

`pip install requirements`

다음 단계는 보통 하던 대로 관련 라이브러리를 임포트하는 것이다. 진행하면서 각각의 의미가 분명해질 것이다.

- DocumentConverter: 문서를 구조화된 DoclingDocument 형식으로 변환하는 고수준 Python 클래스
- EnsembleRetriever: 가중 Reciprocal Rank Fusion을 사용해 여러 리트리버의 결과를 통합하고 정렬하는 앙상블 리트리버

## DocLing: VerificationAgent 설명 (번역)
나는 AI가 생성한 답변을 원문 문서에 대해 팩트체크하는 VerificationAgent 클래스를 만들었다. __init__에서는 결정론적 출력을 위해 온도 0으로 deepseek-v3.2 모델을 초기화하고, LLM이 네 가지 방식으로 답변을 검증하도록 프롬프트 템플릿을 구성한다. (주장이 직접적으로 지지되는지, 어떤 부분이 근거 없는지, 무엇이 모순되는지, 질문과 관련 있는지) 또한 일관된 파싱을 위해 구조화된 응답 형식을 강제한다.

check()에서는 답변 문자열과 Document 객체 리스트를 받아 문서 텍스트를 모두 추출해 하나의 컨텍스트 문자열로 합친 다음, LangChain 파이프라인(프롬프트 → LLM → 문자열 파서)을 만들어 답변과 컨텍스트로 실행하여 검증 리포트를 얻는다.

디버깅을 위해 리포트와 컨텍스트를 모두 로깅하고, 발생한 에러는 다시 예외로 던진다. 마지막으로 검증 리포트 텍스트와 사용한 컨텍스트 문자열을 담은 dict를 반환한다. 핵심 목적은 RAG가 만든 답변이 실제로 원문 문서에 의해 지지되는지 확인해 환각을 잡아내는 것이다.

```python
import os
import hashlib
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import List
from docling.document_converter import DocumentConverter
from langchain_text_splitters import MarkdownHeaderTextSplitter
from config import constants
from config.settings import settings
from utils.logging import logger

class DocumentProcessor:
    def __init__(self):
        self.headers = [("#", "Header 1"), ("##", "Header 2")]
        self.cache_dir = Path(settings.CACHE_DIR)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def validate_files(self, files: List) -> None:
        """Validate the total size of the uploaded files."""
        total_size = sum(os.path.getsize(f.name) for f in files)
        if total_size > constants.MAX_TOTAL_SIZE:
            raise ValueError(f"Total size exceeds {constants.MAX_TOTAL_SIZE//1024//1024}MB limit")

    def process(self, files: List) -> List:
        """Process files with caching for subsequent queries"""
        self.validate_files(files)
        all_chunks = []
        seen_hashes = set()

        for file in files:
            try:
                # Generate content-based hash for caching
                with open(file.name, "rb") as f:
                    file_hash = self._generate_hash(f.read())

                cache_path = self.cache_dir / f"{file_hash}.pkl"

                if self._is_cache_valid(cache_path):
                    logger.info(f"Loading from cache: {file.name}")
                    chunks = self._load_from_cache(cache_path)
                else:
                    logger.info(f"Processing and caching: {file.name}")
                    chunks = self._process_file(file)
                    self._save_to_cache(chunks, cache_path)

                # Deduplicate chunks across files
                for chunk in chunks:
                    chunk_hash = self._generate_hash(chunk.page_content.encode())
                    if chunk_hash not in seen_hashes:
                        all_chunks.append(chunk)
                        seen_hashes.add(chunk_hash)

            except Exception as e:
                logger.error(f"Failed to process {file.name}: {str(e)}")
                continue

        logger.info(f"Total unique chunks: {len(all_chunks)}")
        return all_chunks

    def _process_file(self, file) -> List:
        """Original processing logic with Docling"""
        if not file.name.endswith(('.pdf', '.docx', '.txt', '.md')):
            logger.warning(f"Skipping unsupported file type: {file.name}")
            return []

        converter = DocumentConverter()
        markdown = converter.convert(file.name).document.export_to_markdown()
        splitter = MarkdownHeaderTextSplitter(self.headers)
        return splitter.split_text(markdown)

    def _generate_hash(self, content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    def _save_to_cache(self, chunks: List, cache_path: Path):
        with open(cache_path, "wb") as f:
            pickle.dump({
                "timestamp": datetime.now().timestamp(),
                "chunks": chunks
            }, f)

    def _load_from_cache(self, cache_path: Path) -> List:
        with open(cache_path, "rb") as f:
            data = pickle.load(f)
        return data["chunks"]

    def _is_cache_valid(self, cache_path: Path) -> bool:
        if not cache_path.exists():
            return False

        cache_age = datetime.now() - datetime.fromtimestamp(cache_path.stat().st_mtime)
        return cache_age < timedelta(days=settings.CACHE_EXPIRE_DAYS)


```
RelevanceChecker 설명 (번역)

나는 RelevanceChecker 클래스를 만들어, 검색된 문서가 사용자 질문에 답할 수 있는지 판단하도록 세 가지 범주로 분류하게 했다.

__init__에서는 API 키로 deepseek-v3.2 모델을 초기화하고, LLM이 구절을 “CAN_ANSWER”(완전 답변), “PARTIAL”(주제 언급은 하지만 불완전), “NO_MATCH”(주제 언급 없음)으로 분류하도록 프롬프트 템플릿을 만든다. 특히 주제를 조금이라도 언급하면 “NO_MATCH”가 아니라 “PARTIAL”이어야 한다고 강조한다. 그리고 프롬프트 → LLM → 문자열 파서로 LangChain 체인을 구성한다.

check()에서는 질문, 리트리버, 그리고 분석할 상위 문서 개수 k(기본 3)를 받는다. 리트리버를 질문으로 호출해 관련 청크를 가져오고, 아무것도 없으면 즉시 “NO_MATCH”를 반환한다.

문서 개수와 상위 k개 청크의 200자 미리보기를 디버그로 출력한다. 상위 k개 텍스트를 두 줄 공백으로 합친 뒤, 질문과 함께 LLM 체인에 넣어 분류 문자열을 받는다.

응답을 대문자로 변환해 유효한 라벨 3개 중 하나인지 확인하고, 예상 밖의 값이면 “NO_MATCH”로 강제한다. 마지막으로 검증된 분류값을 반환해, 리트리버가 쓸 만한 문서를 찾았는지 혹은 웹 검색 같은 대체 방법으로 넘어가야 하는지 신호를 제공한다.

# agents/relevance_checker.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_deepseek import ChatDeepSeek
from config.settings import settings

class RelevanceChecker:
    def __init__(self):
        # self.llm = ChatOpenAI(api_key=settings.OPENAI_API_KEY, model="gpt-4o")
        self.llm = ChatDeepSeek(api_key=settings.DEEPSEEK_API_KEY, model="deepseek-chat")


        self.prompt = ChatPromptTemplate.from_template(
            """
            You are given a user question and some passages from uploaded documents.

            Classify how well these passages address the user's question.
            Choose exactly one of the following responses (respond ONLY with that label):

            1) "CAN_ANSWER": The passages contain enough explicit info to fully answer the question.
            2) "PARTIAL": The passages mention or discuss the question's topic (e.g., relevant years, facility names)
            but do not provide all the data or details needed for a complete answer.
            3) "NO_MATCH": The passages do not discuss or mention the question's topic at all.

            Important: If the passages mention or reference the topic or timeframe of the question in ANY way,
            even if incomplete, you should respond "PARTIAL", not "NO_MATCH".

            Question: {question}
            Passages: {document_content}

            Respond ONLY with "CAN_ANSWER", "PARTIAL", or "NO_MATCH".
            """
        )

        self.chain = self.prompt | self.llm | StrOutputParser()

    def check(self, question: str, retriever, k=3) -> str:
        """
        1. Retrieve the top-k document chunks from the global retriever.
        2. Combine them into a single text string.
        3. Pass that text + question to the LLM chain for classification.

        Returns: "CAN_ANSWER" or "PARTIAL" or "NO_MATCH".
        """

        print(f"[DEBUG] RelevanceChecker.check called with question='{question}' and k={k}")

        # Retrieve doc chunks from the retriever
        top_docs = retriever.invoke(question)[:k]  # Only use top k docs
        if not top_docs:
            print("[DEBUG] No documents returned from retriever.invoke(). Classifying as NO_MATCH.")
            return "NO_MATCH"

        print(f"[DEBUG] Retriever returned {len(top_docs)} docs.")

        # Show a quick snippet of each chunk for debugging
        for i, doc in enumerate(top_docs):
            snippet = doc.page_content[:200].replace("\n", "\\n")
            print(f"[DEBUG] Chunk #{i+1} preview (first 200 chars): {snippet}...")

        # Combine the top k chunk texts into one string
        document_content = "\n\n".join(doc.page_content for doc in top_docs)
        print(f"[DEBUG] Combined text length for top {k} chunks: {len(document_content)} chars.")

        # Call the LLM
        response = self.chain.invoke({
            "question": question,
            "document_content": document_content
        }).strip()

        print(f"[DEBUG] LLM raw classification response: '{response}'")

        # Convert to uppercase, check if it's one of our valid labels
        classification = response.upper()
        valid_labels = {"CAN_ANSWER", "PARTIAL", "NO_MATCH"}
        if classification not in valid_labels:
            print("[DEBUG] LLM did not respond with a valid label. Forcing 'NO_MATCH'.")
            classification = "NO_MATCH"
        else:
            print(f"[DEBUG] Classification recognized as '{classification}'.")

        return classification

ResearchAgent 설명 (번역)

나는 ResearchAgent 클래스를 만들어, 검색된 문서를 컨텍스트로 사용해 질문에 대한 답변을 생성하도록 했다.

제공된 컨텍스트를 바탕으로 정확하고 사실적으로 답하라는 프롬프트 템플릿을 만들었고, 컨텍스트가 부족하면 “제공된 문서만으로는 이 질문에 답할 수 없습니다”라고 명시적으로 말하도록 지시했다.

generate()에서는 질문 문자열과 Document 객체 리스트를 받아 모든 문서 텍스트를 두 줄 공백으로 이어붙여 하나의 컨텍스트 문자열을 만든다.

체인을 질문과 컨텍스트로 호출하면 템플릿에 값이 들어가고, DeepSeek로 요청이 전송되며, 생성된 답이 문자열로 반환된다. try-except로 답변과 전체 컨텍스트를 로깅해 디버깅 가능하게 하고, 예외가 나면 다시 던진다.

마지막으로 초안 답변과 사용한 컨텍스트를 담은 dict를 반환해, 생성 결과와 근거 추적성을 동시에 확보한다.
```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class ResearchAgent:
    def __init__(self):
        """Initialize the research agent with the OpenAI model."""
        # self.llm = ChatOpenAI(
        #     model="gpt-4-turbo",
        #     temperature=0.3,
        #     api_key=settings.OPENAI_API_KEY  # Pass the API key here
        # )
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0.3,
            api_key=settings.DEEPSEEK_API_KEY  # Pass the API key here
        )
        self.prompt = ChatPromptTemplate.from_template(
            """Answer the following question based on the provided context. Be precise and factual.

            Question: {question}

            Context:
            {context}

            If the context is insufficient, respond with: "I cannot answer this question based on the provided documents."
            """
        )

    def generate(self, question: str, documents: List[Document]) -> Dict:
        """Generate an initial answer using the provided documents."""
        context = "\n\n".join([doc.page_content for doc in documents])

        chain = self.prompt | self.llm | StrOutputParser()
        try:
            answer = chain.invoke({
                "question": question,
                "context": context
            })
            logger.info(f"Generated answer: {answer}")
            logger.info(f"Context used: {context}")
        except Exception as e:
            logger.error(f"Error generating answer: {e}")
            raise

        return {
            "draft_answer": answer,
            "context_used": context
        }
```

VerificationAgent 설명 (번역)

나는 VerificationAgent 클래스를 만들어, AI가 생성한 답변을 원문 문서에 대해 팩트체크하여 환각을 잡아내도록 했다. __init__에서 온도 0(완전 결정론)의 deepseek-v3.2 모델을 초기화하고, LLM이 네 가지를 검증하도록 프롬프트 템플릿을 만든다: 직접적 사실 근거 여부, 근거 없는 주장, 모순, 질문 관련성. 그리고 구조화된 형식으로 응답하도록 강제한 뒤 LangChain 체인을 구성한다.

check()에서는 답변 문자열과 Document 리스트를 받아 문서 텍스트를 모두 이어붙인 컨텍스트를 만들고, 답변과 컨텍스트로 체인을 호출해 검증 리포트를 받는다. try-except로 리포트와 컨텍스트를 로깅하며, 최종적으로 검증 리포트와 사용 컨텍스트를 담은 dict를 반환해 추적 가능성을 확보한다.

```
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, List
from langchain_core.documents import Document
from langchain_deepseek import ChatDeepSeek
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class VerificationAgent:
    def __init__(self):
        # self.llm = ChatOpenAI(
        #     model="gpt-4-turbo",
        #     temperature=0,
        #     api_key=settings.OPENAI_API_KEY  # Pass the API key here
        # )
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            temperature=0,
            api_key=settings.DEEPSEEK_API_KEY  # Pass the API key here
        )
        self.prompt = ChatPromptTemplate.from_template(
            """Verify the following answer against the provided context. Check for:
            1. Direct factual support (YES/NO)
            2. Unsupported claims (list)
            3. Contradictions (list)
            4. Relevance to the question (YES/NO)

            Respond in this format:
            Supported: YES/NO
            Unsupported Claims: [items]
            Contradictions: [items]
            Relevant: YES/NO

            Answer: {answer}
            Context: {context}
            """
        )

    def check(self, answer: str, documents: List[Document]) -> Dict:
        """Verify the answer against the provided documents."""
        context = "\n\n".join([doc.page_content for doc in documents])

        chain = self.prompt | self.llm | StrOutputParser()
        try:
            verification = chain.invoke({
                "answer": answer,
                "context": context
            })
            logger.info(f"Verification report: {verification}")
            logger.info(f"Context used: {context}")
        except Exception as e:
            logger.error(f"Error verifying answer: {e}")
            raise

        return {
            "verification_report": verification,
            "context_used": context
        }

```

결론 (번역)

DeepSeek V3.2는 규모로 이기는 것이 아니라 더 똑똑한 사고로 이긴다. 희소 어텐션 메커니즘, 더 낮은 비용, 더 강한 장문 컨텍스트 인지, 그리고 더 우수한 툴 사용 추론 능력을 통해, 오픈소스 모델이 막대한 하드웨어 예산 없이도 경쟁력을 유지할 수 있음을 보여준다.

모든 벤치마크에서 1등을 하지는 않을 수 있지만, 오늘날 사용자가 AI와 상호작용하는 방식을 크게 개선한다. 그리고 바로 그 점이, 매우 경쟁적인 시장에서 이 모델이 돋보이는 이유다.
