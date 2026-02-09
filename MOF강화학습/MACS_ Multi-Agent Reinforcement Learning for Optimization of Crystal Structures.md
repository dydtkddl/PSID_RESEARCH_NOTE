---
date: "2024-05-23"
paper_title: "MACS: Multi-Agent Reinforcement Learning for Optimization of Crystal Structures"
short_title: "MACS: 결정 구조 최적화를 위한 다중 에이전트 강화학습"
authors: "Elena Zamaraeva, Christopher M. Collins, George R. Darling, Matthew S. Dyer, Bei Peng, Rahul Savani, Dmytro Antypov, Vladimir V. Gusev, Judith Clymo, Paul G. Spirakis, Matthew J. Rosseinsky"
journal: "arXiv preprint"
year: 2025
status: "translated"
tags: [Multi-Agent Reinforcement Learning, Crystal Structure Optimization, Computational Chemistry, Geometry Optimization, Deep Learning]
category: "Research"
summary: "본 논문은 주기적 결정 구조의 기하 최적화를 위해 다중 에이전트 강화학습(MARL) 기반의 MACS라는 새로운 방법을 제안합니다. 원자들을 개별 에이전트로 모델링하여 부분 관찰 마르코프 게임을 통해 안정적인 구조를 협력적으로 탐색하게 함으로써, 기존 최적화 방법들보다 더 빠르고 효율적이며 낮은 실패율을 달성했습니다."
file_ref: "arXiv:2506.04195v1 [cs.LG] 4 Jun 2025.pdf"
---

<!-- Page 1 -->

# MACS: 결정 구조 최적화를 위한 다중 에이전트 강화학습
(MACS: Multi-Agent Reinforcement Learning for Optimization of Crystal Structures)

**Elena Zamaraeva**$^{1}$, **Christopher M. Collins**$^{*,1}$, **George R. Darling**$^{*,2}$, **Matthew S. Dyer**$^{*,1,2}$
**Bei Peng**$^{*,3}$, **Rahul Savani**$^{*,\dagger,3,4}$, **Dmytro Antypov**$^{1}$, **Vladimir V. Gusev**$^{3}$, **Judith Clymo**$^{3}$
**Paul G. Spirakis**$^{1,3}$, **Matthew J. Rosseinsky**$^{1,2}$

$^1$Leverhulme Research Centre for Functional Materials Design, University of Liverpool, UK
$^2$Department of Chemistry, University of Liverpool, UK
$^3$Department of Computer Science, University of Liverpool, UK
$^4$The Alan Turing Institute, London, UK

## 초록 (Abstract)

원자 구조의 기하 최적화(Geometry optimization)는 계산 화학 및 재료 설계에서 일반적이고 중요한 작업입니다. *최적화 학습(learning to optimize)* 패러다임을 따르는 우리는 주기적 결정 구조 최적화를 해결하기 위해 **MACS(Multi-Agent Crystal Structure optimization)**라고 하는 새로운 다중 에이전트 강화학습 방법을 제안합니다. MACS는 기하 최적화를 부분 관찰 마르코프 게임(partially observable Markov game)으로 취급하며, 여기서 원자들은 안정적인 구성을 집단적으로 발견하기 위해 자신의 위치를 조정하는 에이전트가 됩니다. 우리는 보고된 결정질 재료의 다양한 조성에 대해 MACS를 훈련하여 훈련된 조성의 구조뿐만 아니라 더 큰 크기의 구조와 본 적 없는 조성의 구조까지 성공적으로 최적화하는 정책(policy)을 얻었으며, 이는 뛰어난 확장성과 제로샷 전이성(zero-shot transferability)을 확인시켜 줍니다. 우리는 광범위한 최첨단 최적화 방법들과 우리의 접근 방식을 벤치마킹하고, MACS가 주기적 결정 구조를 훨씬 더 빠르게, 더 적은 에너지 계산으로, 그리고 가장 낮은 실패율로 최적화함을 입증합니다.

## 1. 서론 (Introduction)

계산 화학에서 원자 구조의 기하 최적화는 국소 에너지 최소값(local energy minimum)에 도달할 때까지 3차원 공간에서 일련의 변위를 따라 원자의 안정적인 배열을 찾는 과정입니다 [39]. 기하 최적화 내에서, 본 논문의 초점은 주기성(periodicity)을 특징으로 하는 결정 구조(crystal structures)에 있습니다. 결정 내 원자의 배열은 물리적 및 화학적 특성을 직접 결정합니다. 따라서 결정 구조의 최적화는 새로운 결정질 재료의 발견에 중요하며 전자 공학, 에너지 응용, 정보 저장 및 기타 영역에서 응용됩니다.

사실, 결정 구조 예측(CSP)으로 알려진 재료 설계 내의 전체 분야는 실험실에서의 후속 합성을 위해 바람직한 특성을 가진 안정적인 결정 구조를 계산적으로 예측하는 데 중점을 둡니다 [52, 53]. CSP 워크플로의 상당한 노력은 잠재 에너지 표면(PES)을 탐색하고 후보 구조에 대해 기하 최적화를 수행하여

---
$^*$동등 기여 (Equal contribution)
$^\dagger$교신 저자 (Corresponding author), e-mail: Rahul.Savani@liverpool.ac.uk
Preprint. Under review.

<!-- Page 2 -->

에너지와 국소 원자 힘(local atomic forces)을 최소화하는 데 집중됩니다. 이러한 맥락에서 최적화 방법에 대한 핵심 요구 사항은 국소적으로 최적화된 평형 구조를 빠르게 생성하는 능력입니다.

결정 구조의 기하 최적화를 위한 기존 접근 방식에는 Broyden–Fletcher–Goldfarb–Shanno (BFGS) 알고리즘 [4, 14, 16, 40] 및 켤레 기울기(Conjugate Gradient) [41] 방법과 같은 고전적인 1차 및 2차 최적화 방법뿐만 아니라 Fast Inertial Relaxation Engine (FIRE) [3]과 같이 원자 구조에 맞춤화된 방법이 포함됩니다. 그러나 이러한 방법들은 종종 큰 구조를 최적화하기 위해 상당한 수의 단계가 필요하거나 각 최적화 단계에서 시간이 많이 소요되는 계산을 요구합니다. 이는 CSP와 같이 수천 번의 국소 최적화 실행이 필요한 응용 분야에서 최적화 시간을 병목 현상으로 만듭니다.

본 연구에서 우리는 다중 에이전트 강화학습(MARL)을 사용하여 결정 구조의 기하 최적화를 개선하기 위해 *최적화 학습(learning to optimize, L2O)* 패러다임 [27, 8, 45]을 활용합니다. 우리는 전체적인 구조적 안정성이 개별 원자에 작용하는 힘에 의존한다는 것을 관찰했습니다. 힘은 원자 위치에 대한 에너지의 편미분(또는 그라디언트)이며, 구조가 국소 에너지 최소값을 달성하는 평형 상태에서는 모든 힘이 0입니다. 에너지와 힘은 주로 각 원자의 화학적 특성과 주변 국소 환경에 의해 결정됩니다. 더욱이, 특정 원소의 원자들과 화학적으로 관련된 원소의 원자들은 유사한 화학적 국소 환경을 채택하는 경향이 있어, 최적화된 결정 구조 내에서 여러 유사한 국소 환경을 초래합니다. 따라서 개별 원자를 독립적으로 움직이지만 동시에 안정적인 전체 구조, 즉 에너지 랜드스케이프의 국소 최소값을 집단적으로 발견하는 에이전트로 간주하는 것이 자연스럽습니다. 그러므로 우리는 결정 구조 기하 최적화를 MARL 문제로 공식화하며, 개별 원자가 국소적으로 최적화된 구조를 집단적으로 발견하기 위한 분산된 정책을 학습하는 것을 목표로 합니다.

에너지(및 대부분의 경우 힘) 추정은 모든 최적화 방법에 통합되어 있으며, 이를 위한 다양한 방법이 존재합니다. 에너지/힘을 계산하는 데 사용할 수 있는 방법은 복잡성과 정확성, 따라서 계산 비용이 다양합니다. Lennard-Jones 포텐셜(LJ) [26, 13] 또는 Müller-Brown 표면 [37, 35]은 종종 단순한 시스템을 모델링하는 데 사용되는 반면, 밀도 범함수 이론(DFT)과 같은 더 복잡한 방법은 높은 정확도로 재료의 에너지와 힘을 추정할 수 있지만 계산 비용이 훨씬 큽니다. 우리는 결정 구조에 대해 빠르고 정확한 에너지 및 그라디언트 추정을 제공하는 DFT 데이터로 훈련된 머신러닝 원자 간 포텐셜 모델인 CHGNet [12]을 활용합니다.

본 연구에서 우리는 다음과 같은 기여를 합니다:

*   우리가 아는 한, 주기적 결정 구조 최적화를 해결하기 위해 MARL을 적용한 첫 번째 사례입니다. 우리가 제안한 방법인 **Multi-Agent Crystal Structure optimization (MACS)**는 주기적 결정 구조 최적화를 다중 에이전트 조정 문제로 새롭게 공식화하여 제시합니다.
*   우리의 광범위한 실험은 MACS가 광범위한 최첨단 방법보다 훨씬 더 효율적으로 결정 구조를 최적화함을 보여줍니다. 이러한 실험은 다양한 원소 종, 다양한 종의 수, 별개의 대칭 그룹을 포함하는 다양한 결정질 재료 세트를 다룹니다.
*   MACS는 강력한 제로샷 전이성과 확장성을 보여주며, 새롭고 본 적 없는 조성의 더 큰 구조를 최적화할 때 효율성을 유지합니다. 우리의 연구는 주기적 결정 구조 최적화를 위한 MARL의 잠재력을 열어줍니다.

## 2. 관련 연구 (Related Work)

L2O 개념은 머신러닝을 활용하여 특정 문제에 맞춤화된 새로운 최적화 방법을 개발하며, 그 적용 범위가 빠르게 확장되고 있습니다. 이 패러다임은 베이지안 군집 최적화(Bayesian swarm optimization) [6], 블랙박스 최적화 [9, 28], 적대적 훈련(adversarial training) [54] 또는 편미분 방정식 해결 [18]과 같은 고전적인 최적화 과제에 성공적으로 적용되었습니다.

원자 구조의 기하 최적화 또한 L2O 개념의 대상입니다. [2]에서 저자들은 LJ 및 규산칼슘 수화물 포텐셜 [33]과 Stillinger-Weber 포텐셜(SW) [44]을 사용하여 유한하고 비주기적인 원자 클러스터의 최적화에 대한 그래프 기반 L2O 접근 방식을 제안합니다. 저자들은 그들의 방법이 FIRE, Adam [25], Gradient Descent [43]에 비해 최적화된 클러스터에서 더 낮은 에너지를 달성함을 보여줍니다. 또 다른 연구 [34]는 LJ, SW, Gupta 포텐셜 [19]을 사용하여 원자 클러스터의 최적화를 조사하며 클러스터 내 에너지 최소화에 중점을 둡니다.

<!-- Page 3 -->

분자 최적화 작업에서 주요 목표가 최소 단계 수로 안정적인 분자 구성을 달성하는 것인 경우 [36, 7, 1]에서 탐구되었습니다. [36]에서 저자들은 MARL을 사용하여 MolOpt 최적화기를 훈련하고 세 가지 기준선인 BFGS, FIRE, MDMin [23]과 벤치마킹합니다. [36]의 결과는 MolOpt 최적화기가 MDMin을 능가하고 FIRE와 비슷한 성능을 보이며 BFGS보다는 열등함을 나타냅니다. 마르코프 결정 과정(MDP) 설계의 차이와 별개의 화학 시스템 클래스에 대한 적용에도 불구하고, 우리는 일관성을 유지하기 위해 [36]의 모든 기준선을 연구에 추가했습니다.

강화학습(RL)은 특정 특성을 가진 재료 설계 [17, 24] 및 CSP의 basin-hopping 루틴 최적화 [56]를 포함하여 계산 화학의 다른 영역에서도 가능성을 보여주었습니다. 화학 분야의 다른 RL 응용에 대한 포괄적인 개요는 리뷰 [42]를 참조하십시오.

## 3. 사전 지식 및 문제 공식화 (Preliminaries and Problem Formulation)

### 3.1 주기적 결정 구조와 그 최적화

결정 구조는 단위 셀(unit cell, 일반적으로 평행육면체)과 그 내부의 원자 구성으로 특징지어집니다. 단위 셀은 3차원 모두에서 반복되어 원자의 무한한 주기적 배열을 정의합니다 (2차원 예시는 그림 2a 참조).

기하 최적화 또는 국소 최적화는 초기 구조를 입력으로 받아 단위 셀 내 원자의 위치를 조정하여 에너지가 국소 최소값인 구조를 달성합니다. 기하 최적화를 수행하는 효율적인 절차는 계산 화학 전반에 걸쳐 광범위하게 사용되기 때문에 중요합니다. 잠재 에너지 표면(PES)의 국소 최소값에 있는 원자 구성은 재료의 물리적으로 안정적인 구조를 나타내며, 따라서 재료의 특성은 일반적으로 이러한 구조에 의존합니다. 따라서 광전자, 진동, 기계 및 에너지 특성 계산은 국소 최소값을 달성하기 위한 기하 최적화로 시작됩니다.

결정 구조 최적화의 범위에서 전역 최적화와 국소 최적화는 목표에 따라 구별됩니다. CSP의 궁극적인 목표인 전역 결정 구조 최적화는 주어진 조성에 대해 가장 안정적인 구성을 나타내는 전역 최소 에너지 구조를 식별하는 것을 목표로 합니다. 그러나 전역적으로 최적의 구조를 달성하려면 일반적으로 구조 생성 또는 섭동(perturbation) 후 국소 최적화를 수행하는 많은 반복이 필요합니다 [5, 55, 38, 48].

기하 최적화는 두 가지 조건에서 종료됩니다. 첫 번째 조건인 **성공 조건(condition of success)**은 구조 내 최대 원자 힘의 노름(norm)$^1$이 지정된 임계값에 도달해야 합니다. 우리는 임계값 0.05 eV/Å을 사용하는데, 이는 CSP 응용 분야에서 일반적인 사용 사례를 나타내기 때문입니다 [11]. 두 번째 조건인 **실패 조건(condition of failure)**은 성공 조건을 만족하지 못한 채 최대 허용 최적화 단계 수에 도달할 때 발생합니다. 우리는 최대 단계 수를 1000으로 설정했는데, 이는 BFGS, BFGS with line search, 또는 FIRE와 같은 최첨단 방법을 사용하여 본 연구 내의 구조를 최적화하기에 일반적으로 충분합니다. 따라서 우리의 공식화에서 기하 최적화 문제는 다음과 같습니다.

> **문제 (기하 최적화):** 초기 결정 구조와 최대 1000단계가 주어졌을 때, 고정된 단위 셀 내 원자의 위치를 자율적으로 조정하여 구조 내 모든 원자 힘을 가능한 한 빨리 0.05 eV/Å 미만으로 국소적으로 최소화하시오.

### 3.2 부분 관찰 마르코프 게임으로서의 기하 최적화

우리는 결정 구조의 기하 최적화를 부분 관찰 마르코프 게임(POMG) [32, 31]으로 모델링합니다. POMG는 각 에이전트에 대해 부분 관찰 가능성이 도입된 MDP의 다중 에이전트 확장입니다. 이는 각 에이전트가 환경의 전역 상태에 대한 개인적인 국소 관찰(private local observation)을 가짐을 의미합니다. POMG는 튜플 $<\mathbb{A}, \mathbb{S}, \mathbb{O}, \mathbb{U}, T, R_i>$로 표현될 수 있습니다. 여기서 $\mathbb{A}$는 $N$개의 에이전트 집합; $\mathbb{S}$는 상태 공간; $\mathbb{O} = \mathbb{O}_1 \times \dots \times \mathbb{O}_N$은 결합 관찰 공간(joint observation space)으로, $\mathbb{O}_i$는 에이전트 $a_i$의 관찰 공간; $\mathbb{U} = \mathbb{U}_1 \times \dots \times \mathbb{U}_N$은 결합 행동 공간(joint action space)으로, $\mathbb{U}_i$는 $a_i$의 행동 공간; $R_i$는 전이에 대해 에이전트 $a_i$에게 스칼라 값을 반환하는 개별 보상 함수입니다.

---
$^1$본 논문 전체에서 모든 벡터와 원자 위치는 데카르트 좌표로 표현되며, 거리와 벡터 노름은 L2 노름으로 정의됩니다.

<!-- Page 4 -->

![Figure 1](Figure_1_placeholder)
> **그림 1:** 전체적인 MACS 아키텍처. 우리는 5개의 원자(Sr 원자 1개, Ti 원자 1개, O 원자 3개)를 가진 SrTiO$_3$ 예시를 사용합니다. 각 타임스텝 $t$에서 현재 상태 $s^t$는 개별 관찰 $o_{Sr}^t, o_{Ti}^t, o_{O1}^t, o_{O2}^t, o_{O3}^t$로 변환되어 에이전트(정책) 네트워크로 전달됩니다. 에이전트 네트워크는 개별 행동을 출력하고, 이는 스케일링되어 구조를 업데이트하기 위한 원자의 변위로 사용됩니다. 에너지 계산기(CHGNet)는 업데이트된 구조에 대한 그라디언트를 제공하여 다음 상태 $s^{t+1}$을 구성하고 개별 보상을 계산합니다. 정책 훈련 과정은 정책 네트워크, Q-네트워크, 리플레이 버퍼를 사용하는 표준 SAC [21] 워크플로를 따릅니다.

에이전트들이 상태 $s \in \mathbb{S}$에서 결합 행동 $u \in \mathbb{U}$를 취했을 때 상태 $s \in \mathbb{S}$에서 상태 $s' \in \mathbb{S}$로 전이; $T(s, u): \mathbb{S} \times \mathbb{U} \rightarrow \mathbb{S}$는 전이 함수로, 에이전트들이 상태 $s \in \mathbb{S}$에서 결합 행동 $u \in \mathbb{U}$를 취했을 때 다음 상태 $s' \in \mathbb{S}$로 전이할 확률을 결정합니다. 전이 함수는 우리의 문제 설정에서 결정론적(deterministic)입니다.

결정 구조의 기하 최적화를 POMG로 모델링함으로써, 우리는 구조의 주기적 단위 셀 내 각 원자를 국소 관찰에만 접근할 수 있는 개별 에이전트로 취급합니다. 모든 에이전트는 독립적으로 동시에 행동하여 개별 보상을 최대화함으로써 국소 최소 에너지 구조를 집단적으로 발견합니다. 각 에이전트는 서로 다른 보상 함수를 갖지만, 한 원자의 위치를 최적화하면 주변 원자의 상대적 위치가 개선되므로 공통 목표를 향해 정렬됩니다. 우리는 국소 관찰 공간의 합리적인 크기를 통해 학습 문제를 더 다루기 쉽게 만들고 많은 수의 원자로 확장성을 개선하기 위해 의도적으로 부분 관찰 가능성을 부과합니다. MACS의 일반적인 체계는 그림 1에 제시되어 있습니다.

## 4. 방법론 (Methodology)

이 섹션에서는 관찰 공간, 행동 공간, 보상 함수를 정의하여 주기적 결정 구조 최적화의 제안된 POMG 공식화를 공식적으로 소개합니다. 그런 다음 우리가 사용하는 특정 RL 알고리즘의 선택과 그 구성에 대해 논의합니다.

**관찰 (Observations).** 결정 구조의 각 원자는 동일한 단위 셀 내의 이웃 원자뿐만 아니라 이웃 단위 셀의 주기적 이미지(periodic images)로 둘러싸여 있습니다. 이를 감안하여, 우리는 각 에이전트가 자신의 특징과 $k$개의 *가장 가까운 이웃(nearest neighbors)*의 특징을 관찰할 수 있도록 관찰 공간을 설계합니다. $k$개의 가장 가까운 이웃은 에이전트와 가장 가까운 $k$개의 원자를 의미하며, 단위 셀 내부 또는 이웃 단위 셀의 주기적 이미지에서 거리가 증가하는 순서로 나열됩니다. 그림 2a는 구조 내 특정 원자의 $k$개 가장 가까운 이웃에 대한 2차원 예시를 보여줍니다.

관찰 공간을 정의하기 위해, 타임스텝 $t$에서 에이전트 $a_i$의 특징 벡터 $\mathbf{f}_{a_i}^t$를 정의하는 것으로 시작합니다:

$$ \mathbf{f}_{a_i}^t = concat([r_i, c_i^t, \log(|\mathbf{g}_i^t|)], \mathbf{g}_i^t, \mathbf{d}_i^{t-1}, \mathbf{g}_i^t - \mathbf{g}_i^{t-1}). \quad (1) $$

여기서 $concat$은 연결(concatenation) 함수입니다; $r_i$는 $a_i$의 공유 결합 반경(covalent radius)으로, 최적화 중에 변경되지 않으며 서로 다른 종을 구별하고 중요한

<!-- Page 5 -->

![Figure 2](Figure_2_placeholder)
> **그림 2:** (a) 3개의 원자를 가진 구조에 대한 2차원 단위 셀 및 가장 가까운 이웃. 하나의 원자가 다른 단위 셀에 속한 12개의 가장 가까운 이웃에 연결된 것으로 표시됩니다; (b,c) (b) 80개 원자를 가진 SrTiO$_3$ 및 (c) 96개 원자를 가진 Ca$_3$Ti$_3$O$_7$의 테스트 세트에 대한 국소 최소값의 에너지 분포. 수직선은 실험 구조의 에너지를 나타냅니다.

화학적 정보를 전달하는 역할을 합니다. 성분 $c_i^t$는 행동 공간을 정의할 때 설명될 행동 스케일링 인자입니다. $\mathbf{g}_i^t$는 타임스텝 $t$에서 에이전트 $a_i$의 그라디언트 벡터로, CHGNet에 의해 제공되며 과도하게 큰 값을 피하기 위해 스케일링됩니다 (부록 A 참조); $\log(|\mathbf{g}_i^t|)$는 보상 함수에 사용되며 보상이 관찰에 의존함을 더 잘 포착하기 위해 특징 벡터에 추가됩니다. 우리는 원자와 그 국소 환경의 안정성을 직접 나타내는 그라디언트 벡터를 사용하는 특징을 *힘 관련(force-related)* 특징이라고 부릅니다. $\mathbf{g}_i^t - \mathbf{g}_i^{t-1}$은 이전 타임스텝 $t$로부터의 그라디언트 벡터 변화로 이전 단계가 얼마나 성공적이었는지를 반영하며, $\mathbf{d}_i^{t-1}$은 이전 타임스텝 $t-1$에서의 $a_i$의 변위입니다; 이들은 최적화 역학을 반영하도록 설계된 *이력(history)* 특징입니다. 힘 관련 및 이력 특징은 섹션 5.4에서 정책 효율성에 대한 중요성을 입증합니다.

이제 타임스텝 $t$에서 $a_i$의 전체 관찰을 다음과 같이 제시할 준비가 되었습니다:

$$ \mathbf{o}_{a_i}^t = concat(\mathbf{f}_{a_i}^t, \mathbf{f}_{n_{i1}^t}^t, \dots, \mathbf{f}_{n_{ik}^t}^t, [|\mathbf{r}_{i1}^t|, \dots, |\mathbf{r}_{ik}^t|], \mathbf{r}_{i1}^t, \dots, \mathbf{r}_{ik}^t). \quad (2) $$

여기서 타임스텝 $t$에서 $\mathbf{r}_{i1}^t, \dots, \mathbf{r}_{ik}^t$는 $a_i$의 $k$개 가장 가까운 이웃의 ($a_i$에 대한) 상대적 위치이며, $n_{i1}^t, \dots, n_{ik}^t$는 해당 위치를 점유하는 에이전트입니다. 에이전트의 가장 가까운 이웃의 상대적 위치와 그들의 특징 벡터는 에이전트 국소 환경의 기하학적 및 화학적 특성을 반영합니다. 관찰 설계는 부록 A의 예시로 설명되어 있습니다. 본 연구에서는 $k$개의 가장 가까운 이웃을 빠르게 구성하기 위해 average-minimum-distance 패키지 [50, 49]를 사용하고 $k=12$로 설정합니다; 따라서 관찰 벡터의 길이는 204입니다.

**행동 (Actions).** 행동 공간에 대한 직관적인 설계는 행동을 에이전트의 변위로 정의하는 것입니다. 효율적인 학습을 보장하기 위해, 우리는 행동의 크기(order of magnitude)를 안내하기 위해 타임스텝 $t$에서 $a_i$의 그라디언트 벡터 노름(gnorm)에 의존하는 스케일링 인자 $c_i^t$를 사용할 것을 제안합니다:

$$ c_i^t = \min(|\mathbf{g}_i^t|, c_{max}). \quad (3) $$

여기서 $c_{max}$는 과도하게 큰 단계를 피하기 위한 조정 가능한 하이퍼파라미터입니다 (본 연구에서는 $c_{max} = 0.4$). 타임스텝 $t$에서 행동 $\mathbf{u}_{a_i}^t \in [-1, 1]^3$이 주어지면, $a_i$의 변위는 다음과 같습니다:

$$ \mathbf{d}_i^t = c_i^t \mathbf{u}_{a_i}^t. \quad (4) $$

변위는 에이전트를 단위 셀 경계를 넘어 이동시킬 수 있으며, 이 경우 단위 셀 내 위치가 급격하게 변경됩니다. 관찰 벡터나 행동 벡터 모두 단위 셀 내 원자의 위치를 사용하지 않는 것이 중요한데, 이 접근 방식은 단위 셀 간의 부드러운 교차와 다른 단위 셀에서 동일한 에이전트에 해당하는 여러 이웃을 처리할 수 있게 해주기 때문입니다.

**보상 (Rewards).** 보상 함수는 구조 내 원자 힘을 충분히 낮은 값으로 줄이는 목표를 반영해야 합니다. 따라서 우리는 현재 타임스텝 $t$와 다음 타임스텝 $t+1$에서의 $a_i$의 gnorm을 사용하여 $a_i$에 대한 개별 보상을 다음과 같이 구성할 것을 제안합니다:

$$ R_{a_i}^t = \log(|\mathbf{g}_i^t|) - \log(|\mathbf{g}_i^{t+1}|). \quad (5) $$

로그 항은 최적화되지 않은 구조와 최적화된 구조 사이의 gnorm 크기의 상당한 차이를 감안할 때, 최적화 초기 단계에서 단기 이득으로 정책이 편향되는 것을 방지하는 데 도움이 됩니다. 우리는 에피소드를 구조의 완전한 최적화로 정의하고 할인 인자 $\gamma = 0.995$를 사용하여 정책이 낮은 힘을 더 빨리 달성하도록 장려합니다.

<!-- Page 6 -->

**독립적 SAC (Independent SAC).** 에이전트들이 국소적으로 최적화된 구조를 집단적으로 발견하도록 훈련하기 위해, 우리는 독립적 Soft Actor-Critic (SAC)을 사용합니다. 이는 다른 모든 에이전트를 환경의 일부로 취급하여 단일 에이전트에서 다중 에이전트 설정으로 SAC [21]를 확장합니다. 따라서 다중 에이전트 문제는 동일한 환경을 공유하는 동시 단일 에이전트 문제들의 집합으로 분해됩니다. SAC는 샘플 효율성과 엔트로피 정규화(entropy regularization) 사용으로 인해 선택되었으며, 이는 차선책 정책으로의 조기 수렴을 방지하고 탐색(exploration)과 활용(exploitation) 간의 균형을 촉진합니다.

독립적 SAC를 사용한 MACS 워크플로는 그림 1에 제시되어 있습니다. 구조가 주어지면 CHGNet을 사용하여 원자에 작용하는 힘을 추정합니다. 먼저 그라디언트 벡터가 스케일링된 다음 국소 관찰 벡터가 구성되고 정규화됩니다. 관찰에서 정규화 전에 그라디언트 벡터를 스케일링하는 것이 중복처럼 보일 수 있지만, 이는 그라디언트 방향을 더 잘 보존하고 훈련을 안정적으로 만드는 데 도움이 됩니다. 그런 다음 관찰 벡터는 정책 네트워크로 전달됩니다. 우리는 [21]에서 제안되고 RLlib [29]에서 구현된 표준 SAC 아키텍처를 사용하며, 효율적인 훈련을 위해 모든 에이전트 간에 공유되는 정책 네트워크와 트윈 Q-네트워크를 활용합니다. 정책 및 Q-네트워크는 ReLU 활성화 함수가 있는 2계층 MLP입니다. 정책 네트워크는 행동 벡터에 대한 세 쌍(평균, 표준편차)을 출력하며, 이는 행동 공간 제한에 맞추기 위해 tanh 스쿼싱(squashing)을 통과합니다. 튜플 $<\mathbf{o}_{a_i}^t, \mathbf{u}_{a_i}^t, \mathbf{o}_{a_i}^{t+1}, R_{a_i}^t>$는 1,000만 용량의 리플레이 버퍼에 저장됩니다. 하이퍼파라미터 튜닝 세부 사항은 부록 A에 제공됩니다.

## 5. 실험 (Experiments)

이 섹션에서는 기하 최적화에 일반적으로 사용되는 방법들과 MACS를 벤치마킹합니다. 우리는 다양한 화학 시스템 세트에 대해 MACS를 훈련하고 접근 방식의 효율성과 신뢰성을 평가하는 다양한 평가 지표를 사용하여 기준선과 성능을 비교합니다. 우리는 훈련된 정책을 적용하여 본 적 없는 조성 내의 본 적 없는 (더 큰) 크기의 구조를 최적화함으로써 접근 방식의 확장성과 제로샷 전이성을 입증합니다. 또한 관찰 공간, 행동 공간 및 보상 함수 설계가 MACS 성능에 미치는 영향을 조사하기 위해 절제 연구(ablation studies)를 수행합니다. 마지막으로 최적화된 구조에 대한 에너지 분포를 분석하여 MACS와 기준선에 의한 최적화 결과를 비교합니다.

### 5.1 훈련 및 테스트 데이터셋 생성

우리는 6가지 다양한 화학 조성 세트에 대해 MACS를 훈련합니다: Y$_2$O$_3$ [56], Cu$_{28}$S$_{16}$ [11], SrTiO$_3$ [10], Ca$_3$Ti$_2$O$_7$ [11], Ca$_3$Al$_2$Si$_3$O$_{12}$ [20], K$_3$Fe$_5$F$_{15}$ [22]. 이러한 조성은 원소 수(2–4개)와 실험 구조를 설명하는 데 필요한 원자 수(5–80개)가 다양합니다. 우리는 Ab Initio Random Structure Searching 패키지(AIRSS) [30]를 적용하여 훈련 및 테스트 구조를 생성합니다. 훈련 중에는 초기 의사 무작위(pseudo random) 구조가 즉석에서 생성되며, 훈련 조성 중 하나에 속할 확률이 동일하고 합리적인 부피를 가진 ~40개의 원자를 갖는 조건입니다 (자세한 내용은 부록 B 참조). 정책이 훈련되는 모든 조성에 대해 각각 300개의 구조로 구성된 3개의 테스트 세트를 생성하며, 구조는 K, 1.5K, 2K 원자를 포함합니다. 여기서 K는 훈련 중 사용된 구조의 크기입니다.

MACS의 전이성을 입증하기 위해 훈련 과정에 참여하지 않는 3가지 새로운 조성에 대한 테스트 세트를 생성합니다. 구체적으로 훈련 목록에서 SrTiO$_3$ 조성을 선택하고 동일한 원소 세트에서 3가지(Sr$_2$TiO$_4$, Sr$_3$Ti$_2$O$_7$, Sr$_4$Ti$_3$O$_{10}$)를 선택합니다. 이러한 각각의 새로운 조성에 대해 두 개의 테스트 세트를 만듭니다: 하나는 훈련 구조와 거의 같은 크기의 구조를 가지고, 다른 하나는 그 크기의 두 배인 구조를 가집니다.

### 5.2 기준선 및 평가 지표

우리는 6가지 기준선에 대해 MACS를 벤치마킹합니다: **BFGS**는 그라디언트 정보를 기반으로 헤세 행렬(Hessian matrix)을 근사하는 준-뉴턴(quasi-Newton) 방법입니다; **BFGSLS**는 라인 서치(line search)가 있는 BFGS의 변형입니다 [51]; **FIRE**는 추가적인 속도 조정 및 적응형 시간 단계를 갖춘 분자 역학 접근 방식을 기반으로 하는 1차 방법입니다; **FIRE+BFGSLS**는 최대 250단계의 FIRE 후 최대 750단계의 BFGSLS가 이어져 구조를 미세 조정하는 하이브리드 접근 방식입니다 [15, 11]; **MDMin**은 모든 원자의 질량이 1인 velocity-Verlet 방법의 수정입니다; **CG**는 켤레 기울기(conjugate gradient) 기준선, 구체적으로 Polak-Ribiere 알고리즘을 나타냅니다. 모든 기준선은 Atomic Simulation Environment 패키지(ASE) [23] 또는 SciPy [47]에 구현되어 있습니다. 우리는 구조 최적화가 최대 1000단계까지 지속되거나 모든 원자의 힘이 정의된 임계값 미만이 될 때까지 허용합니다.

<!-- Page 7 -->

기하 최적화 방법을 비교하는 자연스러운 방법은 초기 구성을 최적화하는 데 필요한 시간과 단계 수이므로, 우리의 첫 두 가지 평가 지표는 성공적인 최적화 간의 평균 단계 수($\mathbf{N}_{mean}$)와 평균 최적화 시간($\mathbf{T}_{mean}$)입니다. BFGSLS와 CG의 경우, 두 알고리즘의 각 단계가 하나 이상의 에너지 계산을 포함할 수 있으므로 단계 수가 에너지 계산 수와 같지 않음을 관찰합니다. 에너지 계산은 최적화 시간에 크게 기여하므로 성공적인 최적화 간의 평균 에너지 계산 수($\mathbf{C}_{mean}$)도 평가 지표로 사용합니다. 마지막으로 각 방법의 신뢰성을 추정하기 위해 실패율($\mathbf{P}_F$)을 고려합니다.

**표 1:** 모든 테스트 세트에서 MACS와 기준선의 성능 비교 ($\mathbf{T}_{mean}$, $\mathbf{C}_{mean}$, $\mathbf{N}_{mean}$, $\mathbf{P}_F$). 지표 $\mathbf{N}_{mean}$과 $\mathbf{C}_{mean}$은 단일 값(동일한 경우) 또는 ; 기호로 구분되어(다른 경우) 표시됩니다. $\mathbf{T}_{mean}$, $\mathbf{C}_{mean}$, $\mathbf{P}_F$의 가장 낮은 값은 굵게 표시됩니다. 테스트 세트별 표준 오차 및 $\mathbf{P}_F$는 부록 B에 제공됩니다.

| Composition | N atoms | Tmean (sec) | | | | | | | Nmean ; Cmean | | | | | |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| | | **MACS** | BFGS | FIRE | MDMin | BFGSLS | FIRE+<br>BFGSLS | CG | **MACS** | BFGS | FIRE | MDMin | BFGSLS | FIRE+<br>BFGSLS | CG |
| Y$_2$O$_3$ | 40<br>60<br>80 | **18**<br>**32**<br>**48** | 48<br>85<br>137 | 42<br>92<br>130 | 74<br>155<br>207 | 28<br>70<br>97 | 38<br>74<br>112 | 64<br>118<br>184 | **121**<br>**147**<br>**169** | 313<br>340<br>395 | 262<br>338<br>393 | 442<br>553<br>625 | 137 ; 185<br>178 ; 281<br>206 ; 307 | 252 ; 267<br>324 ; 357<br>360 ; 403 | 122 ; 543<br>145 ; 642<br>171 ; 754 |
| Cu$_{28}$S$_{16}$ | 44<br>66<br>88 | **29**<br>**51**<br>**74** | 62<br>112<br>175 | 47<br>88<br>120 | 116<br>205<br>315 | 54<br>60<br>110 | 47<br>79<br>117 | 81<br>147<br>275 | **150**<br>**186**<br>**230** | 293<br>355<br>414 | 257<br>307<br>392 | 543<br>633<br>745 | 147 ; 177<br>176 ; 201<br>213 ; 239 | 232 ; 242<br>280 ; 291<br>352 ; 365 | 158 ; 716<br>198 ; 881<br>283 ; 1269 |
| SrTiO$_3$ | 40<br>60<br>80 | **57**<br>**90**<br>**142** | 94<br>163<br>242 | 109<br>202<br>366 | 248<br>461<br>672 | 65<br>138<br>214 | 102<br>200<br>332 | 134<br>250<br>452 | **143**<br>**179**<br>**208** | 255<br>316<br>329 | 314<br>379<br>446 | 625<br>719<br>765 | 133 ; 190<br>169 ; 255<br>199 ; 317 | 276 ; 299<br>321 ; 406<br>355 ; 433 | 141 ; 572<br>168 ; 681<br>205 ; 837 |
| Ca$_3$Ti$_2$O$_7$ | 48<br>72<br>96 | **59**<br>**106**<br>**163** | 135<br>199<br>276 | 119<br>239<br>412 | 264<br>479<br>705 | 68<br>184<br>195 | 120<br>252<br>324 | 156<br>301<br>499 | **146**<br>**183**<br>**205** | 270<br>310<br>353 | 324<br>408<br>467 | 623<br>707<br>762 | 136 ; 185<br>168 ; 249<br>193 ; 267 | 284 ; 317<br>335 ; 374<br>369 ; 447 | 151 ; 618<br>186 ; 756<br>213 ; 876 |
| K$_3$Fe$_5$F$_{15}$ | 46<br>69<br>92 | **31**<br>**51**<br>**96** | 82<br>146<br>236 | 124<br>214<br>377 | 155<br>276<br>485 | 68<br>118<br>154 | 98<br>181<br>271 | 132<br>248<br>371 | **111**<br>**128**<br>**143** | 274<br>320<br>359 | 246<br>293<br>326 | 501<br>596<br>642 | 135 ; 178<br>163 ; 259<br>176 ; 236 | 246 ; 263<br>299 ; 344<br>353 ; 396 | 134 ; 602<br>160 ; 720<br>181 ; 815 |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | **117**<br>**237**<br>343 | 127<br>266<br>**333** | 226<br>389<br>627 | 585<br>1068<br>1279 | 167<br>276<br>400 | 190<br>422<br>627 | 307<br>572<br>958 | 209<br>264<br>317 | **189**<br>**230**<br>**246** | 307<br>382<br>461 | 700<br>755<br>894 | 141 ; 264<br>165 ; 296<br>189 ; 327 | 269 ; 311<br>316 ; 391<br>350 ; 458 | 147 ; 553<br>177 ; 669<br>214 ; 814 |
| **Compositions unseen during training** | | | | | | | | | | | | | | | |
| Sr$_2$TiO$_4$ | 56<br>112 | **65**<br>**189** | 145<br>358 | 174<br>665 | 361<br>759 | 105<br>414 | 139<br>440 | 234<br>559 | **172**<br>**245** | 335<br>420 | 371<br>554 | 700<br>850 | 162 ; 218<br>242 ; 397 | 319 ; 353<br>427 ; 508 | 175 ; 716<br>245 ; 1003 |
| Sr$_3$Ti$_2$O$_7$ | 48<br>96 | **54**<br>**159** | 123<br>369 | 151<br>497 | 315<br>800 | 88<br>366 | 130<br>375 | 191<br>477 | **153**<br>**227** | 288<br>382 | 345<br>501 | 676<br>817 | 153 ; 210<br>212 ; 343 | 299 ; 323<br>385 ; 449 | 167 ; 682<br>223 ; 909 |
| Sr$_4$Ti$_3$O$_{10}$ | 34<br>68 | **30**<br>**113** | 77<br>202 | 87<br>238 | 174<br>498 | 48<br>149 | 76<br>205 | 106<br>307 | **126**<br>**186** | 251<br>310 | 282<br>408 | 547<br>729 | 124 ; 173<br>179 ; 304 | 256 ; 275<br>339 ; 385 | 137 ; 557<br>183 ; 743 |
| AVERAGE$^2$ | 66 | **99** | 175 | 239 | 444 | 152 | 207 | 297 | **182** | 315 | 366 | 673 | 171 ; 253 | 317 ; 361 | 179 ; 747 |
| $\mathbf{P}_F$ (%) | | **0.36** | 3 | 9.64 | 46.19 | **0.36** | 0.82 | 18.22 | | | | | | | |

$^2$평균은 모든 테스트에 대한 지표 값의 평균, 즉 위 열의 평균으로 취해집니다.

### 5.3 MACS 정책 평가

우리는 총 ~80000단계 동안 MACS를 훈련합니다. 훈련 후, 우리는 MACS와 기준선을 사용하여 테스트 세트의 구조를 최적화합니다. 이때 동일한 하드웨어를 사용하지만 각 최적화에 정확히 하나의 CPU 사용을 허용합니다 (자세한 내용은 부록 B 참조).

표 1은 위에서 언급한 4가지 평가 지표($\mathbf{T}_{mean}$, $\mathbf{N}_{mean}$, $\mathbf{C}_{mean}$, $\mathbf{P}_F$)를 다루는 모든 테스트 세트에 대한 MACS와 기준선의 최적화 결과를 보여줍니다. 우리는 MACS가 거의 모든 테스트 세트에서 모든 기준선보다 상당히 빠르고 더 적은 에너지 계산을 필요로 함을 관찰합니다 (몇 가지 예외 제외). 구체적으로, 평균적으로 MACS의 $\mathbf{T}_{mean}$과 $\mathbf{C}_{mean}$은 최고의 기준선인 BFGSLS보다 각각 34% 및 28% 적습니다. 또한 MACS가 가장 낮은 실패율($\mathbf{P}_F = 0.36\%$)을 가지며 이 지표에서 BFGSLS와 비슷하게 수행함을 알 수 있습니다. $\mathbf{N}_{mean}$ 측면에서 BFGSLS는 MACS보다 약간 더 나은 성능을 보이며 평균적으로 5% 더 적은 단계를 필요로 합니다. MACS는 CG와 비슷하게 수행하며 다른 모든 기준선을 능가합니다. 그러나 CG는 MACS보다 훨씬 높은 실패율($\mathbf{P}_F = 18.22\%$)을 가집니다. BFGSLS와 CG 모두 단계당 여러 에너지 계산을 포함하므로 MACS에 비해 총 에너지 계산이 더 많고 최적화 시간이 더 깁니다.

<!-- Page 8 -->

![Figure 3](Figure_3_placeholder)
> **그림 3:** (a, d) SrTiO$_3$ (a) 및 Ca$_3$Al$_2$Si$_3$O$_{12}$ (d) 조성 내 80개 원자의 성공적으로 최적화된 모든 구조에 대한 평균 에너지 진화; (b,c,e,f) 절제 연구: MACS 및 그 변형에 대한 훈련 중 모든 조성에 걸친 할인된 에피소드 보상 (b, e) 및 평균 에피소드 길이 (c, f).

MACS는 Ca$_3$Al$_2$Si$_3$O$_{12}$를 제외한 모든 조성 및 구조 크기에서 $\mathbf{T}_{mean}$ 및 $\mathbf{C}_{mean}$에서 모든 기준선을 일관되게 능가합니다. Ca$_3$Al$_2$Si$_3$O$_{12}$의 경우 MACS는 BFGS 다음으로 1위 또는 2위를 차지합니다. 이는 구조 크기가 증가함에 따라 경쟁력 있는 성능을 유지하므로 우리 방법의 확장성을 보여줍니다. 또한 MACS는 훈련되지 않은 조성의 모든 구조 세트에서 $\mathbf{T}_{mean}$ 및 $\mathbf{C}_{mean}$에서 모든 기준선을 능가하므로 뛰어난 제로샷 전이성을 보여줍니다.

그림 2b와 2c는 서로 다른 방법으로 얻은 국소 최소값에 대한 에너지 분포를 보여줍니다. 동일한 구조 세트를 최적화할 때 MACS와 기준선이 동일한 국소 최소값 분포에서 샘플링함을 알 수 있습니다. 그림 3a와 3d는 80개의 원자를 포함하는 SrTiO$_3$ 및 Ca$_3$Al$_2$Si$_3$O$_{12}$ 구조의 테스트 세트에 대해 성공적인 모든 최적화에 대해 평균화된 에너지 진화를 보여줍니다. 이는 MACS가 기준선보다 에너지를 더 빠르게 감소시키거나 그중 가장 좋은 것과 비슷하게 수행함을 보여줍니다.

### 5.4 절제 연구 (Ablation Studies)

우리는 섹션 4에서 제안된 MACS 설계(MACS라고 함)를 그 변형들과 비교합니다.

**관찰 (Observations).** 우리는 관찰 공간의 특징 표현이 방법의 성능에 미치는 영향을 조사하기 위해 절제 실험을 수행합니다. 구체적으로 식 1에 제공된 MACS 원자 특징 벡터를 식 6에서 9의 특징 벡터(feat.6, feat.7, feat.8 또는 feat.9라고 함)와 비교합니다. 이들은 일부 힘 관련 또는 이력 특징을 제외한 축소된 특징 표현을 사용합니다. 모든 설정에 대해 훈련 중 모든 조성에 걸쳐 달성된 평균 에피소드 보상과 평균 에피소드 길이를 평가합니다. 그림 3b와 3e에서 볼 수 있듯이 MACS와 feat.9가 최고의 성능을 달성하는 반면 feat.6은 최악의 성능을 보여줍니다. 이는 관찰 공간에 힘 관련 특징을 포함하는 것의 중요성을 보여줍니다. 그런 다음 테스트 세트에서 SrTiO$_3$ 조성을 최적화할 때 다양한 특징 설계로 훈련된 정책을 평가합니다. 표 2는 MACS가 $\mathbf{T}_{mean}$ 및 $\mathbf{N}_{mean}$에서 feat.7 및 feat.8보다 훨씬 더 나은 성능을 보임을 보여줍니다.

$$ \mathbf{f}_{a_i}^t = concat([r_i, c_i^t], \mathbf{d}_i^{t-1}), \quad (6) $$
$$ \mathbf{f}_{a_i}^t = concat([r_i, c_i^t, \log(|\mathbf{g}_i^t|)], \mathbf{g}_i^t), \quad (7) $$
$$ \mathbf{f}_{a_i}^t = concat([r_i, c_i^t, \log(|\mathbf{g}_i^t|)], \mathbf{g}_i^t, \mathbf{g}_i^t - \mathbf{g}_i^{t-1}), \quad (8) $$
$$ \mathbf{f}_{a_i}^t = concat([r_i, c_i^t, \log(|\mathbf{g}_i^t|)], \mathbf{g}_i^t, \mathbf{d}_i^{t-1}). \quad (9) $$

feat.9 설계는 MACS에 비해 $\mathbf{N}_{mean}$에서 약간 낮은 성능을 보이고 $\mathbf{T}_{mean}$에서 더 나은 성능을 보입니다. 부록 B에서 우리는 나머지 모든 테스트 세트에 대해 feat.9를 추가로 평가하고 평균적으로 MACS보다 ~7.7% 더 많은 최적화 단계를 수행함을 확인합니다. 이러한 결과는 힘 관련 및 이력 특징 모두 MACS의 경쟁력 있는 성능에 중요하다는 것을 보여줍니다.

**보상 (Rewards).** 보상 함수가 우리 방법의 성능에 미치는 영향을 조사하기 위해 두 가지 추가 보상 설계를 탐구합니다. 첫 번째 보상 설계(rew.10)의 경우, 고정된 페널티를 추가합니다.

<!-- Page 9 -->

(식 5에 사용된 보상에 각 단계마다 -0.05로 조정됨) 이는 더 빠른 최적화를 장려하는지 탐구하기 위함입니다:

$$ R_{a_i}^t = \log(|\mathbf{g}_i^t|) - \log(|\mathbf{g}_i^{t+1}|) + penalty. \quad (10) $$

**표 2:** 관찰 공간의 다양한 특징 표현(feat.7-9) 및 다양한 보상 함수(rew.10,11)를 사용한 MACS의 성능 비교. 가장 좋은 숫자는 굵게 표시됩니다. feat.6 설계는 구조를 성공적으로 최적화하지 못하여 제외되었습니다.

| | | Tmean (sec) | | | | | | Nmean | | | | | |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Composition | N atoms | MACS | feat.7 | feat.8 | feat.9 | rew.10 | rew.11 | MACS | feat.7 | feat.8 | feat.9 | rew.10 | rew.11 |
| SrTiO$_3$ | 40<br>60<br>80 | 57<br>90<br>142 | 146<br>242<br>385 | 79<br>147<br>236 | **46**<br>**82**<br>**132** | 50<br>88<br>154 | 54<br>83<br>161 | **143**<br>**179**<br>**208** | 416<br>504<br>572 | 256<br>303<br>373 | 145<br>184<br>209 | 144<br>187<br>220 | 169<br>202<br>239 |
| AVERAGE | 60 | 96 | 258 | 154 | **87** | 97 | 99 | **177** | 498 | 311 | 180 | 184 | 204 |
| $\mathbf{P}_F$ (%) | | 0.22 | 8.11 | 0.44 | 0.44 | **0** | 0.33 | | | | | | |

두 번째 보상 설계(rew.11)는 식 5에 사용된 원래 개별 보상에 모든 에이전트의 평균 보상을 더하여 부분 보상 공유의 효과를 탐구합니다:

$$ R_{a_i}^t = \log(|\mathbf{g}_i^t|) - \log(|\mathbf{g}_i^{t+1}|) + \frac{1}{N} \sum_{j=1}^{N} (\log(|\mathbf{g}_j^t|) - \log(|\mathbf{g}_j^{t+1}|)). \quad (11) $$

그림 3c와 3f는 서로 다른 보상 함수로 우리 방법이 달성한 평균 에피소드 보상과 평균 에피소드 길이를 보여줍니다. 에피소드 보상은 서로 다른 보상 함수 간의 성능을 비교할 수 있도록 정규화되었습니다. rew.10과 rew.11이 MACS와 유사하게 수행됨을 알 수 있습니다. 그런 다음 테스트 세트에서 SrTiO$_3$ 조성을 최적화할 때 세 가지 보상 함수로 훈련된 정책을 평가합니다. 표 2는 MACS가 가장 큰 구조(80개 원자)가 있는 테스트 세트에서 $\mathbf{T}_{mean}$ 및 $\mathbf{N}_{mean}$에서 rew.10 및 rew.11보다 우수한 성능을 달성함을 보여줍니다.

**행동 (Actions).** 우리는 행동 벡터가 원자의 변위로 직접 사용되는(식 3에 정의된 스케일링 인자 $c_i^t$ 없이) 간단한 행동 설계(act.12)를 고려합니다:

$$ \mathbf{d}_i^t = \mathbf{u}_{a_i}^t. \quad (12) $$

그림 3b는 두 행동 설계 모두 유사한 에피소드 보상으로 수렴하지만, act.12는 샘플 효율성과 안정성이 훨씬 떨어짐을 보여줍니다. 또한 그림 3e는 act.12가 더 높은 평균 에피소드 길이로 수렴하여 더 많은 최적화 단계를 초래함을 보여줍니다. 이는 행동 설계에 도입된 스케일링 인자가 MACS의 경쟁력 있는 성능에 중요하며, 더 샘플 효율적이고 안정적인 학습을 가능하게 함을 보여줍니다.

## 6. 결론 (Conclusion)

본 연구에서 우리는 주기적 결정 구조 최적화를 위한 새로운 MARL 방법인 MACS를 제시합니다. MACS는 기하 최적화를 다중 에이전트 조정 문제로 모델링하는 새로운 모델을 도입합니다. 이는 화학적 및 기하학적 정보의 표현력이 풍부하면서도 간결한 표현의 균형을 맞추고, 복잡한 원자 상호 작용을 모델링하며, 효율적이고 확장 가능한 정책 학습을 가능하게 하는 독특한 과제를 제기하는 미개척 방향입니다. 우리는 MACS를 다양한 최첨단 방법과 비교하는 광범위한 실험을 수행하고, 다양한 테스트 케이스 세트에서 결정 구조를 효율적으로 최적화할 수 있는 정책을 학습하여 모든 기준선을 크게 능가함을 입증합니다. 우리는 모든 테스트 세트에서 평균적으로 MACS가 가장 강력한 기준선인 BFGSLS보다 34% 더 빠르고 28% 더 적은 에너지 계산으로 구조를 최적화하며 가장 낮은 실패율을 유지함을 보여줍니다.

MACS는 훈련 중에 접하지 않은 더 큰 크기와 조성의 구조 최적화에서 기준선보다 우수하므로 확장성과 제로샷 전이성을 보여줍니다. 결론적으로 MACS는 주기적 결정 구조를 위한 보편적인 기하 최적화기가 될 잠재력을 가지고 있습니다.

**한계 및 향후 연구.** 본 연구에서 원자 종을 구별하는 유일한 특징은 공유 결합 반경입니다. 다양한 원자 특징과 기존 설명자(descriptor) 구현 [57, 46]이

<!-- Page 10 -->

향후 고려될 것입니다. 섹션 5.4의 관찰 공간 분석은 이력이 방법의 효율성에 중요한 역할을 한다는 것을 확인했습니다. 따라서 순환 신경망(RNN)을 방법에 통합하면 MACS를 개선할 수 있으며, 우리는 이 문제를 추가로 조사할 것입니다. 향후 연구를 위한 또 다른 유망한 방향은 구조의 단위 셀을 최적화하는 방법을 배우는 것입니다. 우리는 단위 셀 벡터를 별도의 에이전트로 취급하여 원자가 위치를 최적화하는 방식과 유사하게 최적화할 계획입니다. 마지막으로 구조의 에너지를 추정하는 다른 방법을 CHGNet 대신 사용할 수 있습니다. 특히 DFT는 기존 방법 중 가장 정확한 에너지 추정기이므로 관심이 있습니다. CHGNet이 DFT로 훈련되었으므로, CHGNet으로 훈련하고 DFT로 실행하는(train-with-CHGNet-run-with-DFT) 워크플로는 향후 연구를 위한 유망한 개념을 제시합니다.

## 7. 감사의 말 (Acknowledgements)

저자들은 우리 연구의 질을 향상시킨 귀중한 피드백을 주신 Igor Potapov 교수님께 감사드립니다.
저자들은 Leverhulme Research Centre for Functional Materials Design을 통해 Leverhulme Trust로부터 자금 지원을 받았음을 밝힙니다. 오픈 액세스를 목적으로, 저자들은 이 제출물에서 발생하는 저자 승인 원고(Author Accepted Manuscript) 버전에 크리에이티브 커먼즈 저작자 표시(CC BY) 라이선스를 적용했습니다.

## 참고문헌 (References)

[1] Kabir Ahuja, William H Green, and Yi-Pei Li. Learning to optimize molecular geometries using reinforcement learning. Journal of Chemical Theory and Computation, 17(2):818–825, 2021.
[2] Vaibhav Bihani, Sahil Manchanda, Srikanth Sastry, Sayan Ranu, and NM Anoop Krishnan. Stridernet: A graph reinforcement learning approach to optimize atomic structures on rough energy landscapes. In International Conference on Machine Learning, pages 2431–2451. PMLR, 2023.
[3] Erik Bitzek, Pekka Koskinen, Franz Gähler, Michael Moseler, and Peter Gumbsch. Structural relaxation made simple. Physical review letters, 97:170201, 2006.
[4] Charles George Broyden. The convergence of a class of double-rank minimization algorithms 1. general considerations. IMA Journal of Applied Mathematics, 6(1):76–90, 1970.
[5] Christian J Burnham and Niall J English. Crystal structure prediction via basin-hopping global optimization employing tiny periodic simulation cells, with application to water–ice. Journal of Chemical Theory and Computation, 15(6):3889–3900, 2019.
[6] Yue Cao, Tianlong Chen, Zhangyang Wang, and Yang Shen. Learning to optimize in swarms. Advances in neural information processing systems, 32, 2019.
[7] Yu-Cheng Chang and Yi-Pei Li. Integrating chemical information into reinforcement learning for enhanced molecular geometry optimization. Journal of Chemical Theory and Computation, 19(23):8598–8609, 2023.
[8] Tianlong Chen, Xiaohan Chen, Wuyang Chen, Howard Heaton, Jialin Liu, Zhangyang Wang, and Wotao Yin. Learning to optimize: A primer and a benchmark. Journal of Machine Learning Research, 23(189):1–59, 2022.
[9] Yutian Chen, Matthew W Hoffman, Sergio Gómez Colmenarejo, Misha Denil, Timothy P Lillicrap, Matt Botvinick, and Nando Freitas. Learning to learn without gradient descent by gradient descent. In International Conference on Machine Learning, pages 748–756. PMLR, 2017.
[10] Christopher M Collins, George R Darling, and Matthew J Rosseinsky. The flexible unit structure engine (fuse) for probe structure-based composition prediction. Faraday Discussions, 211:117–131, 2018.
[11] Christopher M Collins, Hasan M Sayeed, George R Darling, John B Claridge, Taylor D Sparks, and Matthew J Rosseinsky. Integration of generative machine learning with the heuristic crystal structure prediction code fuse. Faraday Discussions, 256:85–103, 2025.

<!-- Page 11 -->

[12] Bowen Deng, Peichen Zhong, Kyujung Jun, Janosh Riebesell, Kevin Han, Christopher J Bartel, and Gerbrand Ceder. CHGNet as a pretrained universal neural network potential for charge-informed atomistic modelling. Nature Machine Intelligence, 5(9):1031–1041, September 2023.
[13] Jonathan PK Doye, Mark A Miller, and David J Wales. The double-funnel energy landscape of the 38-atom lennard-jones cluster. The Journal of Chemical Physics, 110(14):6896–6906, 1999.
[14] Roger Fletcher. A new approach to variable metric algorithms. The Computer Journal, 13(3):317–322, 1970.
[15] Julian D Gale and Andrew L Rohl. The general utility lattice program (gulp). Molecular Simulation, 29(5):291–341, 2003.
[16] Donald Goldfarb. A family of variable-metric methods derived by variational means. Mathematics of computation, 24(109):23–26, 1970.
[17] Prashant Govindarajan, Santiago Miret, Jarrid Rector-Brooks, Mariano Phielipp, Janarthanan Rajefndran, and Sarath Chandar. Learning conditional policies for crystal design using offline reinforcement learning. Digital Discovery, 3(4):769–785, 2024.
[18] Daniel Greenfeld, Meirav Galun, Ronen Basri, Irad Yavneh, and Ron Kimmel. Learning to optimize multigrid pde solvers. In International Conference on Machine Learning, pages 2415–2423. PMLR, 2019.
[19] Raju P Gupta. Lattice relaxation at a metal surface. Physical Review B, 23(12):6265, 1981.
[20] Vladimir V Gusev, Duncan Adamson, Argyrios Deligkas, Dmytro Antypov, Christopher M Collins, Piotr Krysta, Igor Potapov, George R Darling, Matthew S Dyer, Paul Spirakis, and Matthew J Rosseinsky. Optimality guarantees for crystal structure prediction. Nature, 619(7968):68 72, 2023.
[21] Tuomas Haarnoja, Aurick Zhou, Pieter Abbeel, and Sergey Levine. Soft actor-critic: Off-policy maximum entropy deep reinforcement learning with a stochastic actor. In International Conference on Machine Learning, pages 1861–1870. PMLR, 2018.
[22] Anne-Marie Hardy, Antoine Hardy, and Gérard Ferey. Structure cristalline du bronze pseudo-quadratique K$_{0.6}$FeF$_3$: transition pyrochlore-quadratique pour les composés KMM’X6. Acta Crystallographica Section B, 29(8):1654–1658, Aug 1973.
[23] Ask Hjorth Larsen, Jens Jrgen Mortensen, Jakob Blomqvist, Ivano E Castelli, Rune Christensen, Marcin Duak, Jesper Friis, Michael N Groves, Bjrk Hammer, Cory Hargus, Eric D Hermes, Paul C Jennings, Peter Bjerre Jensen, James Kermode, John R Kitchin, Esben Leonhard Kolsbjerg, Joseph Kubal, Kristen Kaasbjerg, Steen Lysgaard, Jn Bergmann Maronsson, Tristan Maxson, Thomas Olsen, Lars Pastewka, Andrew Peterson, Carsten Rostgaard, Jakob Schitz, Ole Schtt, Mikkel Strange, Kristian S Thygesen, Tejs Vegge, Lasse Vilhelmsen, Michael Walter, Zhenhua Zeng, and Karsten W Jacobsen. The atomic simulation environmenta python library for working with atoms. Journal of Physics: Condensed Matter, 29(27):273002, 2017.
[24] Christopher Karpovich, Elton Pan, and Elsa A Olivetti. Deep reinforcement learning for inverse inorganic materials design. npj Computational Materials, 10(1):287, 2024.
[25] Diederik P Kingma and Jimmy Ba. Adam: A method for stochastic optimization. arXiv preprint arXiv:1412.6980, 2014.
[26] JE Lennard and I Jones. On the determination of molecular fields.i. from the variation of the viscosity of a gas with temperature. Proceedings of the Royal Society of London. Series A, Containing Papers of a Mathematical and Physical Character, 106(738):441–462, 1924.
[27] Ke Li and Jitendra Malik. Learning to optimize. arXiv preprint arXiv:1606.01885, 2016.
[28] Xiaobin Li, Kai Wu, Xiaoyu Zhang, and Handing Wang. B2opt: Learning to optimize black-box optimization with little budget. In Proceedings of the AAAI Conference on Artificial Intelligence, volume 39, pages 18502–18510, 2025.

<!-- Page 12 -->

[29] Eric Liang, Richard Liaw, Robert Nishihara, Philipp Moritz, Roy Fox, Ken Goldberg, Joseph Gonzalez, Michael Jordan, and Ion Stoica. Rllib: Abstractions for distributed reinforcement learning. In International Conference on Machine Learning, pages 3053–3062. PMLR, 2018.
[30] Leandro Liborio, Simone Sturniolo, and Dominik Jochym. Computational prediction of muon stopping sites using ab initio random structure searching (airss). The Journal of Chemical Physics, 148(13):134114, 2018.
[31] Michael L Littman. Markov games as a framework for multi-agent reinforcement learning. In William W Cohen and Haym Hirsh, editors, Machine Learning Proceedings 1994, pages 157–163. Morgan Kaufmann, San Francisco (CA), 1994.
[32] Ryan Lowe, YI WU, Aviv Tamar, Jean Harb, OpenAI Pieter Abbeel, and Igor Mordatch. Multi-agent actor-critic for mixed cooperative-competitive environments. In I. Guyon, U. Von Luxburg, S. Bengio, H. Wallach, R. Fergus, S. Vishwanathan, and R. Garnett, editors, Advances in Neural Information Processing Systems, volume 30. Curran Associates, Inc., 2017.
[33] Enrico Masoero, E Del Gado, RJ-M Pellenq, F-J Ulm, and Sidney Yip. Nanostructure and nanomechanics of cement: polydisperse colloidal packing. Physical review letters, 109(15):155503, 2012.
[34] Amil Merchant, Luke Metz, Samuel S Schoenholz, and Ekin D Cubuk. Learn2hop: Learned optimization on rough landscapes. In International Conference on Machine Learning, pages 7643–7653. PMLR, 2021.
[35] Alexis W Mills, Joshua J Goings, David Beck, Chao Yang, and Xiaosong Li. Exploring potential energy surfaces using reinforcement machine learning. Journal of Chemical Information and Modeling, 62(13):3169–3179, 2022.
[36] Rohit Modee, Sarvesh Mehta, Siddhartha Laghuvarapu, and U Deva Priyakumar. Molopt: Autonomous molecular geometry optimization using multiagent reinforcement learning. The Journal of Physical Chemistry B, 127(48):10295–10303, 2023.
[37] Klaus Müller and Leo D Brown. Location of saddle points and minimum energy paths by a constrained simplex optimization procedure. Theoretica chimica acta, 53:75–93, 1979.
[38] Artem R Oganov, Andriy O Lyakhov, and Mario Valle. How evolutionary crystal structure prediction works and why. Accounts of chemical research, 44(3):227–237, 2011.
[39] H Bernhard Schlegel. Geometry optimization. Wiley Interdisciplinary Reviews: Computational Molecular Science, 1(5):790–809, 2011.
[40] David F Shanno. Conditioning of quasi-newton methods for function minimization. Mathematics of Computation, 24(111):647–656, 1970.
[41] Jonathan Richard Shewchuk et al. An introduction to the conjugate gradient method without the agonizing pain. Technical report, Pittsburgh, PA, USA, 1994.
[42] Bhuvanesh Sridharan, Animesh Sinha, Jai Bardhan, Rohit Modee, Masahiro Ehara, and U Deva Priyakumar. Deep reinforcement learning in chemistry: A review. Journal of Computational Chemistry, 45(22):1886–1898, 2024.
[43] Frank H Stillinger and Randall A LaViolette. Local order in quenched states of simple atomic substances. Physical Review B, 34(8):5136, 1986.
[44] Frank H Stillinger and Thomas A Weber. Computer simulation of local order in condensed phases of silicon. Physical review B, 31(8):5262, 1985.
[45] Ke Tang and Xin Yao. Learn to optimize – a brief overview. National Science Review, 11(8):nwae132, 2024.
[46] Andrij Vasylenko, Dmytro Antypov, Sven Schewe, Luke M Daniels, John B Claridge, Matthew S Dyer, and Matthew J Rosseinsky. Digital features of chemical elements extracted from local geometries in crystal structures. Digital Discovery, 2025.

<!-- Page 13 -->

[47] Pauli Virtanen, Ralf Gommers, Travis E Oliphant, Matt Haberland, Tyler Reddy, David Cournapeau, Evgeni Burovski, Pearu Peterson, Warren Weckesser, Jonathan Bright, et al. Scipy 1.0: fundamental algorithms for scientific computing in python. Nature methods, 17(3):261–272, 2020.
[48] Junjie Wang, Hao Gao, Yu Han, Chi Ding, Shuning Pan, Yong Wang, Qiuhan Jia, Hui-Tian Wang, Dingyu Xing, and Jian Sun. Magus: machine learning and graph theory assisted universal structure searcher. National Science Review, 10(7):nwad128, 2023.
[49] Daniel Widdowson and Vitaliy Kurlin. Resolving the data ambiguity for periodic crystals. In Advances in Neural Information Processing Systems, 2022.
[50] Daniel Widdowson, Marco M Mosca, Angeles Pulido, Vitaliy Kurlin, and Andrew I Cooper. Average minimum distances of periodic point sets - foundational invariants for mapping periodic crystals. MATCH Communications in Mathematical and in Computer Chemistry, 87(3):529–559, 2022.
[51] Philip Wolfe. Convergence conditions for ascent methods. ii: Some corrections. SIAM Review, 13(2):185–188, 1971.
[52] Scott M Woodley and Richard Catlow. Crystal structure prediction from first principles. Nature materials, 7(12):937–946, 2008.
[53] Scott M Woodley, Graeme M Day, and R Catlow. Structure prediction of crystals, surfaces and nanoparticles. Philosophical Transactions of the Royal Society A, 378(2186), 2020.
[54] Yuanhao Xiong and Cho-Jui Hsieh. Improved adversarial training via learned optimizer. In Computer Vision–ECCV 2020: 16th European Conference, Glasgow, UK, August 23–28, 2020, Proceedings, Part VIII 16, pages 85–100. Springer, 2020.
[55] Shiyue Yang and Graeme M Day. Exploration and optimization in crystal structure prediction: Combining basin hopping with quasi-random sampling. Journal of Chemical Theory and Computation, 17(3):1988–1999, 2021.
[56] Elena Zamaraeva, Christopher M Collins, Dmytro Antypov, Vladimir V Gusev, Rahul Savani, Matthew S Dyer, George R Darling, Igor Potapov, Matthew J Rosseinsky, and Paul G Spirakis. Reinforcement learning in crystal structure prediction. Digital Discovery, 2(6):1831–1840, 2023.
[57] Quan Zhou, Peizhe Tang, Shenxiu Liu, Jinbo Pan, Qimin Yan, and Shou-Cheng Zhang. Learning atoms for materials discovery. Proceedings of the National Academy of Sciences, 115(28):E6411–E6417, 2018.

<!-- Page 14 -->

## A. MACS 설계 및 하이퍼파라미터 튜닝 (The MACS design and hyperparameter tuning)

### A.1 가장 가까운 이웃 예시

우리는 정사각형 단위 셀과 3개의 원자 $a_1, a_2, a_3$를 가진 구조의 2차원 예시를 고려합니다. 여기서 $a_2$와 $a_3$는 동일한 화학 원소와 관련이 있습니다. 구조가 최적화 중이라고 가정하고, 그림 4는 타임스텝 $t$에서의 원자 배열을 보여줍니다. 여기서 에이전트 $a_1$의 경우, 첫 번째 가장 가까운 이웃은 이웃 단위 셀에 있는 원자 $a_2$의 주기적 이미지이므로 $n_{11}^t = a_2$; 두 번째 가장 가까운 이웃은 다른 이웃 단위 셀에 있는 $a_3$의 주기적 이미지이고, 세 번째 가장 가까운 이웃은 원자 $a_3$ 자체이므로 $n_{12}^t = n_{13}^t = a_3$입니다. 또한 $\mathbf{r}_{11}^t, \mathbf{r}_{12}^t, \mathbf{r}_{13}^t$는 $a_1$에 대한 $a_1$의 세 가장 가까운 이웃의 위치, 즉 $a_1$에서 세 가장 가까운 이웃 각각까지의 유클리드 공간 벡터를 나타냅니다. 따라서 타임스텝 $t$에서 에이전트 $a_1$에 대한 관찰 벡터는 다음과 같습니다:

$$ \mathbf{o}_{a_1}^t = concat(\mathbf{f}_{a_1}^t, \mathbf{f}_{a_2}^t, \mathbf{f}_{a_3}^t, \mathbf{f}_{a_3}^t, [|\mathbf{r}_{11}^t|, |\mathbf{r}_{12}^t|, |\mathbf{r}_{13}^t|], \mathbf{r}_{11}^t, \mathbf{r}_{12}^t, \mathbf{r}_{13}^t). \quad (13) $$

최적화 과정 동안 $k$개의 가장 가까운 이웃 목록은 각 타임스텝마다 업데이트됩니다: 기존의 가장 가까운 이웃은 목록에서 상대적 위치와 순서를 업데이트할 수 있으며, 일부는 목록을 떠나고 새로운 이웃으로 대체될 수 있습니다.

![Figure 4](Figure_4_placeholder)
> **그림 4:** 3개의 원자를 가진 2차원 구조와 원자 $a_1$ 중 하나에 대한 3개의 가장 가까운 이웃.

amd 패키지 [50, 49]는 각 단계에서 모든 원자에 대해 $k$개의 가장 가까운 이웃의 정렬된 목록을 빠르게 구성하는 데 사용됩니다.

### A.2 가장 가까운 이웃의 수 $k$

우리는 에이전트의 국소 관찰에서 고려해야 할 가장 가까운 이웃의 수를 탐구합니다. 우리는 10, 12, 15개의 가장 가까운 이웃을 선택하고 이 하이퍼파라미터만 다른 세 가지 정책을 MACS를 사용하여 훈련합니다. 그림 5는 MACS가 학습한 세 가지 정책이 훈련 중 평균 에피소드 보상과 평균 에피소드 길이 모두에서 비슷한 성능을 달성함을 보여줍니다. 그런 다음 이 정책들로 Y$_2$O$_3$, SrTiO$_3$, Ca$_3$Al$_2$Si$_3$O$_{12}$ 조성의 테스트 세트 구조를 최적화합니다. 표 3은 $k=15$인 정책이 가장 높은 실패율과 가장 긴 최적화를 가짐을 보여줍니다. $k=10$과 $k=12$인 정책은 비슷하며, 후자가 약간 더 낫기 때문에 본 연구를 위해 선택되었습니다.

<!-- Page 15 -->

**표 3:** 에이전트의 국소 관찰에서 고려되는 가장 가까운 이웃의 수가 다른 MACS의 성능 비교. 가장 좋은 숫자는 굵게 표시되며, 표준 오차는 괄호 안에 있습니다.

| | | Tmean (sec) | | | | Nmean | | |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Composition | N atoms | k = 10 | k = 12 | k = 15 | k = 10 | k = 12 | k = 15 |
| Y$_2$O$_3$ | 40<br>60<br>80 | **17(0)**<br>34(1)<br>51(1) | 18(1)<br>**32(1)**<br>**48(1)** | 26(2)<br>48(3)<br>81(4) | 123(2)<br>150(3)<br>179(4) | **121(3)**<br>**147(3)**<br>**169(3)** | 137(4)<br>171(5)<br>201(6) |
| SrTiO$_3$ | 40<br>60<br>80 | **48(1)**<br>**76(2)**<br>139(3) | 57(12)<br>90(12)<br>142(13) | 51(2)<br>88(2)<br>**138(3)** | 148(3)<br>**178(4)**<br>215(5) | **143(3)**<br>179(4)<br>**208(5)** | 164(4)<br>196(4)<br>232(5) |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | 124(4)<br>**231(7)**<br>380(11) | **117(4)**<br>237(14)<br>**343(16)** | 148(6)<br>245(8)<br>436(13) | **207(5)**<br>274(7)<br>333(8) | 209(5)<br>**264(7)**<br>**317(8)** | 238(7)<br>307(8)<br>367(9) |
| AVERAGE | 60 | 122 | **120** | 140 | 201 | **196** | 224 |
| $\mathbf{P}_F$ (%) | | **0.56** | 0.78 | 3.52 | | | |

![Figure 5](Figure_5_placeholder)
> **그림 5:** 에이전트의 국소 관찰에서 고려되는 가장 가까운 이웃의 수($k$)가 다른 MACS가 달성한 평균 에피소드 보상 및 평균 에피소드 길이.

<!-- Page 16 -->

### A.3 그라디언트 벡터 스케일링

$g_{0_i}^t$를 타임스텝 $t$에서 에이전트 $a_i$에 대해 CHGNet 또는 다른 에너지/그라디언트 계산기가 제공하는 그라디언트 벡터라고 합시다. 본 연구에서 관찰/행동/보상에 사용되는 해당 스케일링된 그라디언트 벡터는 다음과 같이 계산됩니다:

$$ \mathbf{G}_i^t = \begin{cases} \mathbf{g}_{0_i}^t, & \text{if } \|\mathbf{g}_{0_i}^t\|_\infty < g_{max}, \\ \mathbf{g}_{0_i}^t \times \frac{g_{max}}{\|\mathbf{g}_{0_i}^t\|_\infty}, & \text{otherwise.} \end{cases} \quad (14) $$

여기서 $g_{max}$는 조정 가능한 파라미터입니다. 우리의 실험은 그라디언트 벡터가 일반적으로 최적화 시작 시 $[-50, 50]$ 범위의 성분을 갖지만, 때때로 최대 500의 성분을 가진 벡터가 있을 수 있음을 보여주었습니다. 이러한 그라디언트 벡터는 훈련의 균형을 크게 깨뜨리고 결국 그라디언트 폭발로 이어집니다 (그림 6 참조). 실제로 크거나 매우 큰 그라디언트 벡터 사이에는 차이가 없으며, 모두 매우 바람직하지 않은 원자 환경을 나타냅니다. 방향을 보존하는 합리적인 성분 값으로 그라디언트 벡터를 스케일링하면 이 문제를 완화하는 데 도움이 됩니다. 그림 7은 $g_{max}$의 다른 값으로 훈련하는 동안 MACS가 달성한 평균 에피소드 보상과 평균 에피소드 길이를 보여줍니다. $g_{max}=20$인 MACS는 가장 높은 보상으로 수렴하는데, 이는 최적화 시작 시 더 높은 gnorm, 따라서 더 높은 보상 때문일 것으로 예상됩니다. 그러나 $g_{max}=5$인 MACS는 높은 에피소드 보상을 달성하면서 가장 낮은 평균 에피소드 길이로 수렴하므로, 본 연구에서는 $g_{max}=5$를 사용합니다.

![Figure 6](Figure_6_placeholder)
> **그림 6:** 서로 다른 $g_{max}$를 사용한 MACS의 훈련 중 그라디언트 노름.

![Figure 7](Figure_7_placeholder)
> **그림 7:** 서로 다른 $g_{max}$ 값에 따른 MACS의 성능 비교.

<!-- Page 17 -->

### A.4 행동을 위한 하이퍼파라미터 튜닝

스케일링 인자 $c_i^t$는 원자 변위의 크기를 안내하기 위해 타임스텝 $t$에서 에이전트 $a_i$의 행동에 적용됩니다. $c_i^t$의 상한은 과도하게 큰 변위를 피하기 위해 하이퍼파라미터 $c_{max}$에 의해 정의됩니다. 그림 8은 $c_{max}$의 두 가지 변형을 비교하고 더 작은 $c_{max}$가 정책이 훨씬 더 높은 평균 에피소드 보상과 더 낮은 에피소드 길이로 수렴하도록 허용함을 보여주며, 따라서 본 연구를 위해 $c_{max}=0.4$가 선택되었습니다.

우리는 또한 행동 공간을 설계하기 위한 간단한 접근 방식을 탐구합니다: 행동 벡터는 스케일링 인자 $c_i^t$ 없이 원자의 변위로 직접 사용됩니다(식 12). 우리는 정책 학습에 미치는 영향을 조사하기 위해 행동 공간에 대한 다양한 경계를 고려합니다. 즉, 다양한 $a_{max}$ 값에 대해 $[-a_{max}, a_{max}]^3$을 고려합니다. 우리는 SAC에서 정책 네트워크의 출력이 tanh 스쿼싱된 다음 행동 공간 제한에 맞게 스케일링된다는 점에 주목합니다. 이는 행동 공간 제한에 따라 동일한 행동 벡터에 대해 다른 정책 출력 크기로 이어집니다. 이를 고려하여 목표 엔트로피의 다양한 값도 탐구합니다. 우리는 다양한 행동 공간 경계와 목표 엔트로피 값으로 MACS가 달성한 평균 에피소드 보상과 평균 에피소드 길이를 비교합니다. 그림 9는 행동 공간에 대한 더 넓은 경계($a_{max}=0.2$)가 훈련을 더 안정적으로 만드는 반면, 행동 공간에 대한 더 좁은 경계($a_{max}=0.1$)는 더 낮은 평균 에피소드 길이를 달성할 수 있게 함을 보여줍니다. 우리는 가장 성능이 좋은 변형, 즉 절제 연구를 위해 목표 엔트로피 T_E= -12인 $a_{max}=0.1$을 선택합니다.

![Figure 8](Figure_8_placeholder)
> **그림 8:** 서로 다른 $c_{max}$ 값에 따른 MACS의 성능 비교.

![Figure 9](Figure_9_placeholder)
> **그림 9:** 서로 다른 행동 공간 경계 및 목표 엔트로피 값에 따른 MACS의 성능 비교.

<!-- Page 18 -->

### A.5 기타 하이퍼파라미터

MACS를 훈련하는 데 사용된 하이퍼파라미터 목록은 표 4에 나와 있습니다. 그림 10과 11은 하이퍼파라미터의 다양한 변형에 대해 훈련 중 MACS가 달성한 평균 에피소드 보상과 평균 에피소드 길이를 보여줍니다. 훈련 배치 크기(그림 10c 및 10d)와 엔트로피 학습률(그림 11c 및 11d)이 중요한 역할을 함을 알 수 있습니다.

**표 4:** MACS 훈련에 사용된 하이퍼파라미터.

| Hyperparameter | value |
| :--- | :---: |
| $\gamma$ | 0.995 |
| Training batch size | 8192 |
| Target entropy | -8 |
| Truncate episodes | TRUE |
| Target network update frequency | 1000 |
| Number of samples before learning starts | 500 |
| Tau | 0.001 |
| Initial alpha | 1 |
| Use twin q | TRUE |
| Actor learning rate | 0.0003 |
| Critic learning rate | 0.0003 |
| Entropy learning rate | 0.0001 |
| Replay buffer capacity | 10000000 |
| Use prioritised replay buffer | FALSE |
| $g_{max}$ | 5 |
| $c_{max}$ | 0.4 |
| Observation component-wise normalization | TRUE |
| Number of nearest neighbors k | 12 |
| Max steps in episode | 1000 |

![Figure 10](Figure_10_placeholder)
> **그림 10:** 리플레이 버퍼 용량 및 훈련 배치 크기의 다양한 값에 따른 MACS의 성능 비교. 파란색 선은 항상 논문에서 사용된 값을 나타냅니다.

<!-- Page 19 -->

![Figure 11](Figure_11_placeholder)
> **그림 11:** 목표 엔트로피, 엔트로피/액터/크리틱 학습률, 트윈 Q-네트워크 플래그의 다양한 값에 따른 MACS의 성능 비교. 파란색 선은 항상 본 연구에서 사용된 값을 나타냅니다.

<!-- Page 20 -->

## B. 추가 실험 세부 사항 및 결과 (Additional experimental details and results)

### B.1 훈련 및 테스트 목적을 위한 하드웨어 사용

우리는 2개의 20코어 Intel(R) Xeon(R) Gold 6138 CPU (2.00 GHz)와 384 GB 메모리가 장착된 Linux 클러스터 노드에서 40개의 동시에 실행되는 환경을 사용하여 총 ~80000 훈련 단계 동안 MACS를 훈련합니다. 모든 기준선은 데이터 기반이거나 훈련되지 않았습니다; 그들은 명시적이고 결정론적인 논리를 기반으로 합니다.

MACS와 기준선을 사용한 테스트 세트의 최적화는 MACS를 훈련하는 데 사용된 것과 동일한 하드웨어에서 수행되었습니다. 그러나 테스트 세트의 최적화에는 단일 CPU 코어만 사용되었으며 나머지 39개 코어는 유휴 상태로 유지되었습니다. 이 설정은 기준선이 병렬화되지 않았으므로 MACS가 병렬화를 통해 이점을 얻는 것을 방지하여 공정한 비교를 보장하기 위해 선택되었습니다.

### B.2 기준선

기준선은 CHGNet 패키지를 통해 액세스되며, 이는 다시 ASE 패키지에서 제공하는 최적화 방법과 인터페이스합니다. 우리는 ASE에 구현된 BFGS, BFGSLS, FIRE, MDMin을 사용하는 반면, CG는 SciPy에 구현되어 있으며 CHGNet $\rightarrow$ ASE 체인을 통해 액세스됩니다. 기준선의 하이퍼파라미터는 잘 튜닝되어 있으며 수정 없이 일반적으로 사용됩니다; 우리는 이를 있는 그대로 채택합니다.

### B.3 무작위 구조 생성

우리는 다음과 같은 방식으로 훈련 및 테스트 구조를 생성합니다. 조성, 원자 수, 파라미터 $v$가 주어지면 AIRSS 패키지를 사용하여 의사 무작위 구조를 생성합니다. AIRSS는 $[v - 5\%, v + 5\%]$ 범위의 무작위 부피를 가진 단위 셀을 생성하고 두 원자 사이의 최소 거리가 1Å이 되도록 이 단위 셀 내에 원자를 배치합니다.

훈련 중 각 에피소드의 시작 부분에서 훈련 조성 목록에서 조성을 무작위로 선택합니다. 우리는 실제 재료의 물리학을 반영하기 위해 훈련과 테스트 모두에서 주어진 조성에 대한 실험 구조의 부피를 파라미터 $v$로 사용합니다. 또 다른 파라미터는 구조 내 원자 수이며, 조성이 주어졌을 때 40개 원자에 가장 가깝도록 선택됩니다.

### B.4 추가 실험 결과

표 5는 모든 테스트 세트에서 $\mathbf{T}_{mean}$ (표준 오차 포함) 측면에서 MACS와 모든 기준선을 비교합니다. 표 6은 모든 테스트 세트에서 $\mathbf{N}_{mean}$ 및 $\mathbf{C}_{mean}$ (표준 오차 포함) 측면에서 MACS와 모든 기준선을 비교합니다. 표 7은 모든 테스트 세트 및 방법에 대한 $\mathbf{P}_F$를 보여줍니다. 그림 12와 13은 모든 테스트 세트에 대해 서로 다른 방법으로 얻은 국소 최소값에 대한 에너지 분포를 보여줍니다. 그림 14와 15는 서로 다른 방법에 의한 모든 테스트 세트의 성공적인 모든 최적화에 대해 평균화된 에너지 진화를 보여줍니다.

<!-- Page 21 -->

**표 5:** 모든 테스트 세트에서 $\mathbf{T}_{mean}$에 의한 MACS와 기준선의 비교. 표준 오차는 괄호 안에 있습니다.

| | | Tmean (sec) | | | | | |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Composition | N atoms | MACS | BFGS | FIRE | MDMin | BFGSLS | FIRE+BFGSLS | CG |
| Y$_2$O$_3$ | 40<br>60<br>80 | **18(1)**<br>**32(1)**<br>**48(1)** | 48(2)<br>85(3)<br>137(4) | 42(2)<br>92(3)<br>130(4) | 74(2)<br>155(3)<br>207(4) | 28(2)<br>70(7)<br>97(7) | 38(2)<br>74(2)<br>112(4) | 64(4)<br>118(6)<br>184(9) |
| Cu$_{28}$S$_{16}$ | 44<br>66<br>88 | **29(1)**<br>**51(1)**<br>**74(2)** | 62(2)<br>112(3)<br>175(4) | 47(1)<br>88(2)<br>120(2) | 116(3)<br>205(4)<br>315(4) | 54(12)<br>60(1)<br>110(2) | 47(1)<br>79(2)<br>117(2) | 81(3)<br>147(5)<br>275(7) |
| SrTiO$_3$ | 40<br>60<br>80 | **57(12)**<br>**90(12)**<br>**142(13)** | 94(3)<br>163(6)<br>242(8) | 109(3)<br>202(5)<br>366(8) | 248(5)<br>461(6)<br>672(7) | 65(5)<br>138(10)<br>214(16) | 102(1)<br>200(21)<br>332(17) | 134(7)<br>250(13)<br>452(20) |
| Ca$_3$Ti$_2$O$_7$ | 48<br>72<br>96 | **59(12)**<br>**106(12)**<br>**163(12)** | 135(5)<br>199(6)<br>276(7) | 119(3)<br>239(4)<br>412(14) | 264(5)<br>479(7)<br>705(7) | 68(3)<br>184(18)<br>195(6) | 120(4)<br>252(5)<br>324(13) | 156(7)<br>301(14)<br>499(21) |
| K$_3$Fe$_5$F$_{15}$ | 46<br>69<br>92 | **31(1)**<br>**51(1)**<br>**96(12)** | 82(3)<br>146(4)<br>236(6) | 124(5)<br>214(8)<br>377(12) | 155(3)<br>276(5)<br>485(8) | 68(5)<br>118(19)<br>154(9) | 98(6)<br>181(16)<br>271(17) | 132(7)<br>248(11)<br>371(16) |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | **117(4)**<br>**237(14)**<br>343(16) | 127(5)<br>266(8)<br>**333(8)** | 226(7)<br>389(14)<br>627(18) | 585(5)<br>1068(7)<br>1279(6) | 167(23)<br>276(16)<br>400(7) | 190(5)<br>422(13)<br>627(17) | 307(17)<br>572(31)<br>958(47) |
| **Compositions unseen during training** | | | | | | | | |
| Sr$_2$TiO$_4$ | 56<br>112 | **65(2)**<br>**189(13)** | 145(5)<br>358(10) | 174(5)<br>665(18) | 361(5)<br>759(6) | 105(10)<br>414(63) | 139(2)<br>440(8) | 234(12)<br>559(23) |
| Sr$_3$Ti$_2$O$_7$ | 48<br>96 | **54(1)**<br>**159(12)** | 123(4)<br>369(10) | 151(4)<br>497(10) | 315(5)<br>800(6) | 88(6)<br>366(65) | 130(1)<br>375(6) | 191(9)<br>477(20) |
| Sr$_4$Ti$_3$O$_{10}$ | 34<br>68 | **30(1)**<br>**113(12)** | 77(3)<br>202(6) | 87(3)<br>238(6) | 174(4)<br>498(7) | 48(3)<br>149(23) | 76(3)<br>205(4) | 106(6)<br>307(16) |

**표 6:** 모든 테스트 세트에서 $\mathbf{N}_{mean}$ 및 $\mathbf{C}_{mean}$에 의한 MACS와 기준선의 비교. 지표 $\mathbf{N}_{mean}$과 $\mathbf{C}_{mean}$은 단일 값(동일한 경우) 또는 ; 기호로 구분되어(다른 경우) 표시됩니다. 표준 오차는 괄호 안에 있습니다.

| | | Nmean ; Cmean | | | | | |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Composition | N atoms | MACS | BFGS | FIRE | MDMin | BFGSLS | FIRE+BFGSLS | CG |
| Y$_2$O$_3$ | 40<br>60<br>80 | **121(3)**<br>**147(3)**<br>**169(3)** | 313(10)<br>340(10)<br>395(10) | 262(4)<br>338(5)<br>393(4) | 442(11)<br>553(12)<br>625(14) | 137(2) ; 185(7)<br>178(5) ; 281(23)<br>206(5) ; 307(20) | 252(3) ; 267(6)<br>324(4) ; 357(9)<br>360(5) ; 403(14) | 122(2) ; 543(10)<br>145(3) ; 642(12)<br>171(3) ; 754(15) |
| Cu$_{28}$S$_{16}$ | 44<br>66<br>88 | **150(3)**<br>**186(4)**<br>**230(5)** | 293(6)<br>355(8)<br>414(7) | 257(4)<br>307(5)<br>392(6) | 543(11)<br>633(11)<br>745(12) | 147(3) ; 177(6)<br>176(3) ; 201(4)<br>213(4) ; 239(4) | 232(3) ; 242(3)<br>280(3) ; 291(4)<br>352(3) ; 365(4) | 158(3) ; 716(13)<br>198(4) ; 881(20)<br>283(6) ; 1269(26) |
| SrTiO$_3$ | 40<br>60<br>80 | **143(3)**<br>**179(4)**<br>**208(5)** | 255(8)<br>316(10)<br>329(8) | 314(5)<br>379(6)<br>446(7) | 625(12)<br>719(14)<br>765(17) | 133(3) ; 190(16)<br>169(3) ; 255(14)<br>199(4) ; 317(26) | 276(2) ; 299(3)<br>321(3) ; 406(48)<br>355(3) ; 433(24) | 141(3) ; 572(13)<br>168(4) ; 681(16)<br>205(5) ; 837(21) |
| Ca$_3$Ti$_2$O$_7$ | 48<br>72<br>96 | **146(3)**<br>**183(4)**<br>**205(4)** | 270(9)<br>310(8)<br>353(9) | 324(5)<br>408(6)<br>467(6) | 623(13)<br>707(15)<br>762(18) | 136(2) ; 185(10)<br>168(3) ; 249(27)<br>193(3) ; 267(9) | 284(2) ; 317(11)<br>335(3) ; 374(7)<br>369(3) ; 447(23) | 151(3) ; 618(12)<br>186(3) ; 756(12)<br>213(4) ; 876(15) |
| K$_3$Fe$_5$F$_{15}$ | 46<br>69<br>92 | **111(2)**<br>**128(2)**<br>**143(2)** | 274(8)<br>320(7)<br>359(6) | 246(3)<br>293(4)<br>326(4) | 501(10)<br>596(11)<br>642(10) | 135(3) ; 178(7)<br>163(4) ; 259(53)<br>176(4) ; 236(13) | 246(4) ; 263(6)<br>299(5) ; 344(28)<br>353(5) ; 396(16) | 134(3) ; 602(16)<br>160(3) ; 720(12)<br>181(4) ; 815(20) |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | 209(5)<br>264(7)<br>317(8) | **189(5)**<br>**230(5)**<br>**246(6)** | 307(6)<br>382(6)<br>461(7) | 700(31)<br>755(55)<br>894(0) | 141(4) ; 264(46)<br>165(3) ; 296(16)<br>189(3) ; 327(6) | 269(3) ; 311(6)<br>316(3) ; 391(14)<br>350(3) ; 458(16) | 147(4) ; 553(15)<br>177(4) ; 669(15)<br>214(6) ; 814(23) |
| **Compositions unseen during training** | | | | | | | | |
| Sr$_2$TiO$_4$ | 56<br>112 | **172(4)**<br>**245(5)** | 335(10)<br>420(10) | 371(6)<br>554(8) | 700(14)<br>850(16) | 162(3) ; 218(7)<br>242(5) ; 397(35) | 319(3) ; 353(6)<br>427(4) ; 508(10) | 175(4) ; 716(15)<br>245(4) ; 1003(19) |
| Sr$_3$Ti$_2$O$_7$ | 48<br>96 | **153(4)**<br>**227(5)** | 288(8)<br>382(9) | 345(5)<br>501(7) | 676(12)<br>817(20) | 153(3) ; 210(10)<br>212(4) ; 343(31) | 299(2) ; 323(3)<br>385(3) ; 449(7) | 167(4) ; 682(17)<br>223(5) ; 909(19) |
| Sr$_4$Ti$_3$O$_{10}$ | 34<br>68 | **126(3)**<br>**186(5)** | 251(8)<br>310(8) | 282(5)<br>408(6) | 547(13)<br>729(14) | 124(3) ; 173(14)<br>179(4) ; 304(62) | 256(3) ; 275(3)<br>339(3) ; 385(8) | 137(4) ; 557(17)<br>183(3) ; 743(14) |

<!-- Page 22 -->

**표 7:** $\mathbf{P}_F$ (%)에 의한 MACS와 기준선의 비교.

| Composition | N atoms | MACS | BFGS | FIRE | MDMin | BFGSLS | FIRE+BFGSLS | CG |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Y$_2$O$_3$ | 40<br>60<br>80 | **0.33**<br>**0**<br>0.67 | 5.67<br>4.33<br>12.67 | 7<br>16<br>18.33 | 17.33<br>28.67<br>39.33 | **0.33**<br>1<br>**0.33** | 1.33<br>0.67<br>1.33 | 19<br>26.67<br>32.33 |
| Cu$_{28}$S$_{16}$ | 44<br>66<br>88 | 0.33<br>0.33<br>**0** | 3.67<br>2.67<br>**0** | 1<br>2.67<br>0.33 | 4<br>15<br>56.67 | 0.67<br>**0**<br>**0** | **0**<br>**0**<br>**0** | 6.67<br>11<br>3.33 |
| SrTiO$_3$ | 40<br>60<br>80 | **0**<br>**0.33**<br>**0.33** | 2.33<br>2.33<br>3 | 3.33<br>5<br>9.33 | 25<br>46.33<br>71.67 | **0**<br>0.67<br>**0.33** | 0.33<br>0.67<br>1.33 | 15.67<br>21<br>26.67 |
| Ca$_3$Ti$_2$O$_7$ | 48<br>72<br>96 | **0**<br>**0**<br>0.33 | 3.67<br>0.67<br>0.67 | 1.33<br>1.67<br>3.33 | 22.33<br>54<br>72.33 | **0**<br>0.33<br>**0** | **0**<br>0.33<br>**0** | 10.33<br>13<br>20 |
| K$_3$Fe$_5$F$_{15}$ | 46<br>69<br>92 | **0**<br>**0**<br>**0** | 1.33<br>1.33<br>2.33 | 17.67<br>22.67<br>33.67 | 4.67<br>14<br>20.33 | 0.33<br>**0**<br>0.33 | 4.33<br>3<br>4 | 14<br>19.33<br>20 |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | 1<br>3<br>1.33 | 1.33<br>1.33<br>**0** | 5<br>3<br>4.67 | 90<br>97<br>99.67 | **0**<br>0.33<br>**0** | 1<br>**0**<br>0.33 | 19<br>24.33<br>27 |
| **Compositions unseen during training** | | | | | | | | |
| Sr$_2$TiO$_4$ | 56<br>112 | 0.33<br>**0** | 3.33<br>5.67 | 14<br>31 | 46.33<br>90 | 1.33<br>1.33 | **0**<br>**0** | 17.67<br>20.67 |
| Sr$_3$Ti$_2$O$_7$ | 48<br>96 | **0**<br>**0** | 2.67<br>3.67 | 4<br>14 | 38.33<br>81.33 | 0.33<br>1 | 0.33<br>**0** | 17.67<br>20.33 |
| Sr$_4$Ti$_3$O$_{10}$ | 34<br>68 | 0.33<br>**0** | 5<br>2.33 | 4<br>8.33 | 18.67<br>55.67 | **0**<br>**0** | 0.67<br>**0** | 14.67<br>17 |

<!-- Page 23 -->

![Figure 12](Figure_12_placeholder)
> **그림 12:** 서로 다른 방법으로 얻은 국소 최소값의 에너지 분포. 수직선은 실험 구조의 에너지를 나타냅니다.

<!-- Page 24 -->

![Figure 13](Figure_13_placeholder)
> **그림 13:** 서로 다른 방법으로 얻은 국소 최소값의 에너지 분포. 수직선은 실험 구조의 에너지를 나타냅니다.

<!-- Page 25 -->

![Figure 14](Figure_14_placeholder)
> **그림 14:** 주어진 테스트 세트에서 모든 방법에 대해 성공적으로 최적화된 모든 구조에 대해 평균화된 에너지 진화.

<!-- Page 26 -->

![Figure 15](Figure_15_placeholder)
> **그림 15:** 주어진 테스트 세트에서 모든 방법에 대해 성공적으로 최적화된 모든 구조에 대해 평균화된 에너지 진화.

### B.5 조성 타겟 훈련

우리는 MACS가 기준선(BFGS)보다 성능이 떨어졌던 유일한 조성(Ca$_3$Al$_2$Si$_3$O$_{12}$)에 대해서만 MACS를 훈련합니다. 우리는 교차 조성 훈련(cross-composition training)과 동일한 기간 동안 정책을 훈련합니다. 표 8은 Ca$_3$Al$_2$Si$_3$O$_{12}$ 구조에 대해 특별히 훈련된 MACS가 BFGS 및 훈련 세트의 모든 조성에 걸쳐 훈련된 MACS보다 모든 지표에서 우수함을 확인합니다. Ca$_3$Al$_2$Si$_3$O$_{12}$ 조성은 가장 많은 수의 종을 가지고 있으며, 그 관찰 공간은 본 연구의 다른 조성보다 더 다양할 수 있습니다. 우리는 훈련 중 복잡한 조성의 비율을 늘리거나 더 오래 훈련하면 MACS가 이를 더 잘 최적화하는 데 도움이 될 수 있다고 제안합니다.

**표 8:** Ca$_3$Al$_2$Si$_3$O$_{12}$ 조성에 대해 훈련된 MACS 정책(MACS individual)과 훈련 세트의 모든 조성에 걸쳐 훈련된 MACS 정책(MACS) 및 BFGS의 비교.

| | | Tmean (sec) | | | Nmean | | |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| Composition | N atoms | MACS | MACS individual | BFGS | MACS | MACS individual | BFGS |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | 117<br>237<br>343 | **85**<br>**170**<br>**237** | 127<br>266<br>333 | 209<br>264<br>317 | **153**<br>**205**<br>**229** | 189<br>230<br>246 |
| AVERAGE | 60 | 232 | **164** | 242 | 264 | **196** | 222 |
| $\mathbf{P}_F$ (%) | | 1.78 | **0.33** | 0.89 | | | |

<!-- Page 27 -->

### B.6 추가 절제 연구

**관찰 (Observations).** MACS와 feat.9는 훈련 중 유사한 평균 에피소드 보상과 평균 에피소드 길이를 달성할 뿐만 아니라 SrTiO$_3$ 구조 최적화에서도 유사한 성능을 보입니다. 우리는 feat.9 설계를 사용하여 모든 테스트 세트의 최적화를 진행하고 표 9에서 MACS와 feat.9의 결과를 비교합니다. 두 정책은 $\mathbf{T}_{mean}$ 측면에서 비슷하지만, MACS는 feat.9보다 7.7% 낮은 $\mathbf{N}_{mean}$을 달성하여 MACS의 우수성을 확인합니다$^3$.

**표 9:** $\mathbf{T}_{mean}$ 및 $\mathbf{N}_{mean}$에 의한 feat.9 설계와 MACS의 비교. 표준 오차는 괄호 안에 있습니다.

| | | Tmean (sec) | | Nmean | |
| :--- | :---: | :---: | :---: | :---: | :---: |
| Composition | N atoms | MACS | feat.9 | MACS | feat.9 |
| Y$_2$O$_3$ | 40<br>60<br>80 | **18(1)**<br>**32(1)**<br>**48(1)** | 22(1)<br>39(1)<br>61(2) | **121(3)**<br>**147(3)**<br>**169(3)** | 143(5)<br>168(4)<br>211(6) |
| Cu$_{28}$S$_{16}$ | 44<br>66<br>88 | **29(1)**<br>**51(1)**<br>74(2) | 29(1)<br>54(2)<br>**67(3)** | **150(3)**<br>**186(4)**<br>**230(5)** | 158(4)<br>214(6)<br>338(30) |
| SrTiO$_3$ | 40<br>60<br>80 | 57(12)<br>90(12)<br>142(13) | **44(1)**<br>**81(2)**<br>**132(3)** | **143(3)**<br>**179(4)**<br>**208(5)** | 145(3)<br>184(5)<br>209(4) |
| Ca$_3$Ti$_2$O$_7$ | 48<br>72<br>96 | 59(12)<br>106(12)<br>163(12) | **56(1)**<br>**98(2)**<br>**134(3)** | **146(3)**<br>**183(4)**<br>**205(4)** | 154(3)<br>183(4)<br>214(4) |
| K$_3$Fe$_5$F$_{15}$ | 46<br>69<br>92 | **31(1)**<br>**51(1)**<br>**96(12)** | 38(1)<br>64(2)<br>112(2) | **111(2)**<br>**128(2)**<br>**143(2)** | 141(3)<br>167(4)<br>183(4) |
| Ca$_3$Al$_2$Si$_3$O$_{12}$ | 40<br>60<br>80 | 117(4)<br>237(14)<br>343(16) | **111(3)**<br>**195(5)**<br>**334(8)** | 209(5)<br>264(7)<br>317(8) | **189(5)**<br>**245(7)**<br>**292(7)** |
| **Compositions unseen during training** | | | | | |
| Sr$_2$TiO$_4$ | 56<br>112 | 65(2)<br>189(13) | **63(1)**<br>**174(4)** | **172(4)**<br>**245(5)** | 172(4)<br>247(5) |
| Sr$_3$Ti$_2$O$_7$ | 48<br>96 | 54(1)<br>**159(12)** | **53(1)**<br>159(4) | **153(4)**<br>**227(5)** | 155(4)<br>229(5) |
| Sr$_4$Ti$_3$O$_{10}$ | 34<br>68 | **30(1)**<br>113(12) | 31(1)<br>**88(2)** | **126(3)**<br>**186(5)** | 131(3)<br>190(4) |
| AVERAGE | 66 | **100** | 101 | **181** | 195 |

---
$^3$88개 원자의 Cu$_{28}$S$_{16}$ 구조 테스트 세트의 최적화는 클러스터 유지 보수 작업으로 인해 중단되었으며 테스트에 사용된 하드웨어 교체로 인해 완료할 수 없었습니다. 이 테스트 세트의 나머지 구조 최적화가 집계된 숫자를 변경할 수 있지만, 우리는 MACS가 feat.9보다 일관되게 더 적은 에너지 계산을 필요로 하므로 MACS가 feat.9보다 일관되게 우수한 성능을 보인다는 결론을 내리기 위해 모든 테스트 세트 간의 비교에 의존합니다.
