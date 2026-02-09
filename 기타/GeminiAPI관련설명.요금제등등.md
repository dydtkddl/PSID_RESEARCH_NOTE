# Gemini API “요금제(Free/Paid)” + “사용량 등급(Quota Tier)” 전체 정리 (Gemini 3 Pro Preview 포함)

> 공식 문서(참고):
- Rate limits: https://ai.google.dev/gemini-api/docs/rate-limits
- Pricing: https://ai.google.dev/gemini-api/docs/pricing
- Gemini 3 가이드: https://ai.google.dev/gemini-api/docs/gemini-3

---

## 0) 헷갈리기 쉬운 핵심: **요금제(Free/Paid)** 와 **사용량 등급(Free/Tier1~3)** 는 “서로 다른 축”
Gemini API에서 “돈”과 “한도”는 아래 2개 축으로 관리됩니다.

### A. 요금제(Price plan)
- **Free**: 일부 모델만 제한적으로 사용 가능, 입력/출력 토큰 무료, Google AI Studio 사용 가능, **콘텐츠가 제품 개선에 사용될 수 있음**
- **Paid**: Pay-as-you-go(사용량 기반 과금), 더 높은 한도, Context caching/Batch API 등 고급 기능, 고급 모델 접근, **콘텐츠가 제품 개선에 사용되지 않음**

### B. 사용량 등급(Quota tier / Usage tier)
- 프로젝트 단위로 **RPM/TPM/RPD 같은 “속도/일일” 한도를 얼마나 크게 주는지**를 결정하는 등급
- **Free / Tier 1 / Tier 2 / Tier 3**로 나뉨
- Paid 요금제를 쓴다고 해서 자동으로 Tier 3가 되는 게 아니라, **결제/누적지출 조건**에 따라 Tier가 올라갑니다.

---

## 1) Rate limit(요청 제한) 지표 정의: RPM / TPM / RPD (+ IPM, TPD)
Rate limit은 일정 기간 동안 API에 보낼 수 있는 요청량을 제한합니다. 보통 3가지로 측정합니다.

- **RPM (Requests Per Minute)**: 분당 요청 수
- **TPM (Tokens Per Minute, input)**: 분당 입력 토큰 수
- **RPD (Requests Per Day)**: 일일 요청 수

추가로 모델에 따라:
- **IPM (Images Per Minute)**: 이미지 생성 가능한 모델(예: Imagen 계열)에서 쓰는 분당 이미지 지표(개념적으로 TPM과 유사)
- **TPD (Tokens Per Day)**: 어떤 모델은 “일일 토큰” 한도가 따로 있을 수 있음

### 중요한 운영 규칙
- 한도는 **각 지표마다 별도로 평가**됩니다.
  예) RPM=20이면 1분에 21번째 요청은 TPM/RPD가 남아도 **바로 rate limit 에러**가 납니다.
- Rate limit은 **API 키별이 아니라 “프로젝트(project)별”** 적용됩니다.
- **RPD(일일 요청 수)는 태평양 표준시(Pacific Time) 자정에 리셋**됩니다.
- **Preview/Experimental 모델은 rate limit이 더 엄격**합니다.
- 문서에 적힌 한도는 **보장치가 아니라**, 실제 용량이 달라질 수 있습니다.

---

## 2) 사용량 등급(Usage tiers) — Free / Tier 1 / Tier 2 / Tier 3
Rate limit은 “프로젝트의 사용량 등급”에 연결됩니다.

### 등급 자격 요건(공식 기준)
- **Free**: 대상 국가(eligible countries) 사용자
- **Tier 1**: 프로젝트에 **유료 결제(Billing) 계정이 연결된 상태**
- **Tier 2**: 연결된 결제 계정의 Google Cloud 누적 지출 **$250 초과** + 결제 성공 후 **30일 경과**
- **Tier 3**: 누적 지출 **$1,000 초과** + 결제 성공 후 **30일 경과**

> 업그레이드 요청 시 자동 악용 방지 시스템에서 추가 검사가 수행되며, 요건을 충족해도 드물게 거부될 수 있습니다.

---

## 3) Free vs Paid 요금제(Price plan) — 무엇이 달라지나?
### Free 요금제(개발/소규모 시작)
- 특정 모델만 “제한적” 접근
- 입력/출력 토큰이 **무료**
- Google AI Studio 사용 가능
- **콘텐츠가 제품 개선에 사용될 수 있음**(Used to improve products: Yes)

### Paid 요금제(프로덕션/고용량)
- Pay-as-you-go 과금
- **더 높은 rate limit**
- **Context caching 사용 가능**
- **Batch API 사용 가능(표준 대비 “50% 비용 절감” 구조가 명시됨)**
- Google의 더 고급 모델 접근
- **콘텐츠가 제품 개선에 사용되지 않음**(Used to improve products: No)

---

## 4) Gemini 3 Pro Preview / Gemini 3 Pro Image Preview — “API 요금제 관점” 핵심
### (1) Gemini 3 Pro Preview (`gemini-3-pro-preview`)
- **Gemini API에서는 Free tier가 “없음(Not available)”**
  - 즉, API로 쓰려면 사실상 **Paid 전제**로 보는 게 안전합니다.
- Google AI Studio에서는 “무료로 시험”은 가능(체험과 API 과금 정책은 별개)

#### 가격(표준 / Batch)
- **Standard**
  - Input: **$2.00/1M tokens**(프롬프트 ≤200k), **$4.00/1M tokens**(>200k)
  - Output(Thinking 포함): **$12.00/1M tokens**(≤200k), **$18.00/1M tokens**(>200k)
  - Context caching: **$0.20/1M**(≤200k), **$0.40/1M**(>200k) + **$4.50/1M tokens/hour**(저장)
  - Search grounding: 월 **5,000 prompts 무료**, 이후 **(추후 과금/Coming soon)** **$14/1,000 search queries**
- **Batch**
  - Input: **$1.00/1M tokens**(≤200k), **$2.00/1M tokens**(>200k)
  - Output(Thinking 포함): **$6.00/1M tokens**(≤200k), **$9.00/1M tokens**(>200k)
  - Context caching: Standard와 동일 구조
  - Search grounding: **1,500 RPD 무료**, 이후 **(추후 과금/Coming soon)** **$14/1,000 search queries**

> 참고: Gemini 3의 Search grounding 과금은 **2026-01-05부터 시작**한다고 명시되어 있습니다.

### (2) Gemini 3 Pro Image Preview (`gemini-3-pro-image-preview`)
- 텍스트/추론 토큰 단가는 **Gemini 3 Pro**와 동일 계열로 제시되며,
- 이미지 출력은 별도 높은 단가(예: $120/1M tokens 등)로 책정됩니다.
- Batch에서는 이미지/토큰 비용이 낮아집니다(문서 표 참고).

---

## 5) Batch API(일괄 처리) 관련 “별도” 제한 + (Tier별) enqueued tokens
Batch API 호출은 “일반 호출”과 별도의 rate limit이 적용됩니다.

### 공통 제한(모든 Tier)
- **동시 batch 요청(Concurrent batch requests): 100**
- **입력 파일 크기 제한: 2GB**
- **파일 저장 한도: 20GB**
- **모델별 enqueued tokens 한도**: “현재 활성 batch job들”에 큐잉 가능한 토큰 총량

### Tier별 Batch enqueued tokens (공식 표 요약)
#### Tier 1
- Gemini 3 Pro Preview: **50,000,000**
- Gemini 2.5 Pro: **5,000,000**
- Gemini 2.5 Flash: **3,000,000**
- Gemini 2.5 Flash Preview: **3,000,000**
- Gemini 2.5 Flash-Lite: **10,000,000**
- Gemini 2.5 Flash-Lite Preview: **10,000,000**
- Gemini 2.0 Flash: **10,000,000**
- Gemini 2.0 Flash-Lite: **10,000,000**
- (멀티모달 생성) Gemini 3 Pro Image Preview: **2,000,000**

#### Tier 2
- Gemini 3 Pro Preview: **500,000,000**
- Gemini 2.5 Pro: **500,000,000**
- Gemini 2.5 Flash: **400,000,000**
- Gemini 2.5 Flash Preview: **400,000,000**
- Gemini 2.5 Flash-Lite: **500,000,000**
- Gemini 2.5 Flash-Lite Preview: **500,000,000**
- Gemini 2.0 Flash: **1,000,000,000**
- Gemini 2.0 Flash-Lite: **1,000,000,000**
- Gemini 3 Pro Image Preview: **270,000,000**

#### Tier 3
- Gemini 3 Pro Preview: **1,000,000,000**
- Gemini 2.5 Pro: **1,000,000,000**
- Gemini 2.5 Flash: **1,000,000,000**
- Gemini 2.5 Flash Preview: **1,000,000,000**
- Gemini 2.5 Flash-Lite: **1,000,000,000**
- Gemini 2.5 Flash-Lite Preview: **1,000,000,000**
- Gemini 2.0 Flash: **5,000,000,000**
- Gemini 2.0 Flash-Lite: **5,000,000,000**
- Gemini 3 Pro Image Preview: **1,000,000,000**

---

## 6) 다음 등급으로 업그레이드하는 방법(공식 절차)
1. Google Cloud 프로젝트에 **Cloud Billing 활성화**(Free → Paid 전환의 전제)
2. AI Studio의 **API keys 페이지**로 이동
3. 업그레이드 대상 프로젝트에서 **“Upgrade” 클릭**
   - 자격 요건을 충족한 프로젝트에만 Upgrade가 표시됨
4. 간단한 검증 후 등급 업그레이드

---

## 7) “비율 제한 상향 요청” (Rate limit increase request)
- 각 모델 변형마다 연결된 RPM 등 rate limit이 있고,
- Paid tier는 별도 폼을 통해 상향 요청이 가능하지만 **승인 보장 없음**(검토 후 결정)

---

## 8) PDF 논문 번역 작업에 바로 연결되는 해석(요금/한도 관점)
- **Gemini 3 Pro Preview**는 API에서 Free tier가 없어서, “대량 PDF 번역”에 붙이면 비용/운영(한도) 관리가 중요합니다.
- 비용을 줄이려면:
  - **Batch API**를 적극 사용(표준 대비 50% 절감 구조 + Gemini 3 Pro도 Batch 단가가 절반 수준으로 구성)
  - 긴 PDF는 페이지/섹션 단위로 잘라 **TPM/RPM에 걸리지 않게** 처리
  - 필요 시 Context caching(유료)로 반복 컨텍스트 비용을 줄이는 전략을 고려

---
