---
title: "QM9 & Electrolyte Genome 1주차 태스크"
short_title: "Week1_QM9_EG_Task"
document_type: "주차별 태스크 정의서"
language: "ko"
date: "2025-12-03"
affiliation: "경희대학교 화학공학과 대학원"
keywords: ["QM9", "Electrolyte Genome", "electrolyte additive", "screening", "statistics", "correlation", "dataset profiling", "ZIB"]
file_ref: "Week1_QM9_ElectrolyteGenome_1주차태스크_20251203.docx"
version: "v1.0"
---

# Week1: QM9 & Electrolyte Genome (1주차 태스크)

## 목적
- QM9 데이터셋과 Electrolyte Genome 데이터셋의 **구조와 물성**을 파악하고, 전해질 첨가제 스크리닝에 활용 가능한 **변수와 기본 통계**를 확보한다.

## 구체적인 목표
- QM9와 Electrolyte Genome에서 제공되는 **주요 물성 종류**와 **데이터 구조**를 파악한다.
- 핵심 물리화학적 물성에 대해 **기본 통계**, **분포**, **상관관계**를 계산한다.
- 구조 다양성(원자 수, 분자량 등)에 대한 **기초 분석**을 수행한다.
- 향후 ZIB 첨가제 스크리닝과 머신러닝 모델에 사용할 **우선순위 변수 후보**를 정리한다.

## 역할 분담
- QM9 데이터셋 분석 담당: **정민주**
- Electrolyte Genome API 및 데이터셋 분석 담당: **진석환**

---

# 1) QM9 데이터셋 분석 담당 태스크 (정민주)

## 1.1 데이터 구조 및 물성 파악
- QM9 원본 파일 로드 (PyTorch dataset 또는 직접 다운로드)
- 컬럼명 리스트 정리 (물성명, 구조 정보, 식별자 등)
- 각 컬럼이 의미하는 물성 간단 정리
  - 예: HOMO, LUMO, gap, dipole moment, polarizability, 에너지 항목 등
- 각 물성의 단위 정리

## 1.2 기본 통계 및 분포 분석
- 주요 물성에 대해 기초 통계량 계산
  - (HOMO, LUMO, gap, dipole moment, polarizability, 선택한 에너지 항목)
- 위 물성들에 대한 히스토그램 생성 등 시각화
  - 필요 시 간단한 밀도 곡선 또는 박스플롯 추가

## 1.3 상관관계 분석
- 선택 물성들에 대한 상관계수 행렬 계산
- 상관계수 heatmap 작성
- 일부 조합에 대해 scatter plot 작성
  - 예: gap–dipole, gap–에너지 항목 등

## 1.4 구조 다양성 분석
- 분자당 원자 수 분포 분석(히스토그램)
- 분자량 분포 분석
- 주요 원소 조성 비율 정리 (C, N, O, F 등)
- 가능하면 조성과 주요 물성 간 관계 분석

## 1.5 산출물 정리(예시)
- 분석 코드 파일 (`.py` 또는 `.ipynb`)
- 통계 요약 파일 (예: `qm9_stats_summary.csv`)
- 그림 파일 (히스토그램, 상관계수 heatmap, 대표 산점도)
- 간단 요약 메모 (주요 관찰 사항, 유용해 보이는 물성 후보 목록)

---

# 2) Electrolyte Genome 데이터셋 분석 담당 태스크 (진석환)

## 2.1 API 및 데이터 수집
- 관련 API 문서 확인
- 계정 및 API 키 발급 절차 정리
- 파이썬 스크립트로 API 호출 코드 작성
- 응답 JSON을 DataFrame으로 변환하고 로컬 파일로 저장

## 2.2 물성 종류 및 데이터 구조 파악
- 얻을 수 있는 물성 항목 목록 정리
  - 예: 산화 전위, 환원 전위, HOMO, LUMO, stability window, 용해도 관련 지표 등
- 각 물성의 단위와 의미 간단 정리
- 각 물성별 결측치 비율 계산

## 2.3 기본 통계 및 분포 분석
- 주요 물성에 대해 기초 통계량 계산
  - (산화 전위, 환원 전위, HOMO, LUMO, gap, 용해도 관련 지표 등)
- 각 물성에 대한 히스토그램 생성
- 산화 전위와 환원 전위 관계 산점도 작성
- ZIB 설계에 의미 있어 보이는 조합 일부 산점도 작성
  - 예: gap–stability window

## 2.4 상관관계 및 결측 패턴 분석
- 선택 물성들에 대한 상관계수 행렬 및 heatmap 작성
- 결측치가 많은 물성 항목 리스트업
- 필요 시 결측 패턴 간단 시각화

## 2.5 데이터 규모 및 구조 표현 파악
- 전체 분자 개수, 고유 분자 개수, 중복 여부 집계
- 구조 표현 형식 종류 정리 (SMILES, InChI, 3D 구조 제공 여부 등)
- QM9와 공통으로 존재하는 물성 항목 리스트업 (가능하면)

## 2.6 산출물 정리(예시)
- API 호출 및 데이터 저장 스크립트
- 정제된 데이터 파일 (가능하면)
- 그림 파일 (히스토그램, 상관계수 heatmap, 주요 산점도)
- 간단 요약 메모 (데이터 특징, ZIB 첨가제 설계에 바로 쓸 수 있는 물성 후보 목록)
