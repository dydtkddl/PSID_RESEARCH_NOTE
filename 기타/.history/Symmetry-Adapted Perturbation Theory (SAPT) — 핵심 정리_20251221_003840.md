# Symmetry-Adapted Perturbation Theory (SAPT) — 핵심 정리

> 본 문서는 사용자가 제공한 Wikipedia 발췌 내용을 바탕으로, SAPT의 목적·아이디어·에너지 분해 항을 정리한 Markdown 노트입니다.

---

## 1) SAPT란?

**Symmetry-adapted perturbation theory (SAPT)** 는 전자구조이론에서 **비공유(non-covalent) 상호작용**(분자–분자, 원자–분자 등)을 기술하기 위해 개발된 방법론이며, 넓게는 **에너지 분해 분석(EDA, Energy Decomposition Analysis)** 계열로 분류됩니다.

SAPT가 겨냥하는 대상은 전형적으로 다음과 같은 상호작용입니다.

- 정전기적 인력/반발 (electrostatics)
- 파울리 반발(교환) (exchange / Pauli repulsion)
- 유도(분극) (induction / polarization)
- 분산력 (dispersion; London dispersion)

---

## 2) “슈퍼분자(supermolecular)” 방식과의 대비

많은 EDA 방법은 먼저 **슈퍼분자 방식**으로 총 상호작용 에너지를 계산합니다.

- 이합체(또는 복합체) 에너지: \(E_{AB}\)
- 분리된 단량체 에너지: \(E_A\), \(E_B\)

총 상호작용 에너지는 다음처럼 정의됩니다.


ΔE_int = E_AB − E_A − E_B


이 방식의 대표적인 결함으로 **BSSE(basis set superposition error)** 가 있습니다. 즉, 복합체 계산에서 두 단량체가 서로의 기저함수를 “빌려 쓰는” 효과 때문에, 단순한 빼기식 정의가 기저 선택에 민감해지고 오차가 커질 수 있습니다.

---

## 3) SAPT의 핵심 아이디어: “섭동(perturbation)으로 상호작용을 직접 계산”

SAPT는 이름 그대로 **분자 간 상호작용을 섭동으로 취급**하여 상호작용 에너지를 전개합니다. 즉,

- “전체 시스템 에너지에서 단량체 에너지를 빼는” 방식이 아니라
- **상호작용 자체를 섭동으로 두고** 그에 대한 에너지 기여를 항별로 계산합니다.

이 관점의 중요한 결과 중 하나는, 상호작용 에너지를 섭동으로 다루는 과정에서 **BSSE가 자연스럽게 억제/회피되는 구조**를 가진다는 점입니다(슈퍼분자 빼기 방식 대비).

---

## 4) SAPT가 주는 추가 가치: 에너지 성분 분해(물리적 해석)

SAPT는 섭동 전개이므로, 총 상호작용 에너지가 다음 성분들의 합으로 “자연스럽게” 분해됩니다.

- **정전기(전하밀도–전하밀도)**: electrostatics
- **교환(파울리 반발)**: exchange
- **유도(분극, 전기장에 의한 궤도 변화)**: induction
- **분산(순간적 상관에 의한 인력)**: dispersion

또한 각 항에는 보통 **exchange-counterpart**(예: exch-ind, exch-disp) 가 동반됩니다. 이는 유도/분산 같은 항도 “교환(반대칭성)” 효과와 결합해 보정되어야 함을 반영합니다.

---

## 5) SAPT0 (가장 단순한 수준)에서의 항 구성

Wikipedia 발췌 내용에서 소개된 가장 단순한 접근이 **SAPT0** 입니다.

- SAPT0는 **분자 내부 상관(intramolecular correlation)** 을 무시하고,
- **Hartree–Fock 밀도(HF densities)** 를 기반으로 계산합니다.

SAPT0에서 상호작용 에너지는 보통 다음 항들의 합으로 표현됩니다.


E_int^(SAPT0)
= E_elst^(1) + E_exch^(1)
+ E_ind^(2) + E_exch-ind^(2)
+ E_disp^(2) + E_exch-disp^(2)


의미를 정리하면:

- \(E_{\text{elst}}^{(1)}\): 1차 정전기(두 전하/전자밀도의 고전적 상호작용)
- \(E_{\text{exch}}^{(1)}\): 1차 교환(파울리 반발)
- \(E_{\text{ind}}^{(2)}\): 2차 유도(상대의 전기장에 의해 궤도가 분극되는 효과)
- \(E_{\text{exch-ind}}^{(2)}\): 유도항에 대한 교환 보정
- \(E_{\text{disp}}^{(2)}\): 2차 분산(런던 분산력; 전자 상관 기반)
- \(E_{\text{exch-disp}}^{(2)}\): 분산항에 대한 교환 보정

**중요 포인트**: Wikipedia 발췌 기준으로 “모든 구성 성분이 등장하는 가장 낮은 차수”가 **분자 간 섭동에 대한 2차** 입니다(정전기/교환은 1차, 유도/분산은 2차에서 등장).

---

## 6) 더 높은 수준의 SAPT

더 높은 차수의 섭동 항을 포함하기 위해 다음과 같은 확장이 가능합니다.

- many-body perturbation theory(MBPT) 기반 고차 항 포함
- coupled-cluster(예: CC) 기반 고차 항 포함
- DFT 기반 변형(SAPT(DFT) 계열)도 존재

일반적으로 고급 SAPT는 정확도 측면에서 **슈퍼분자 CCSD(T)** 수준에 근접하는 것으로 소개됩니다(문헌/구현·기저 선택에 따라 달라질 수 있음).

---

## 7) 실무적 관점의 “SAPT로 무엇을 얻나?”

SAPT 계산의 산출물은 단순한 \(E_{\text{int}}\) 하나가 아니라, 다음과 같은 **물리 성분별 숫자**입니다.

- \(E_{\text{elst}}\): 전하·쌍극자·사중극자 등 정전기 기여가 큰지
- \(E_{\text{exch}}\): 근접 접촉에서 파울리 반발이 얼마나 강한지
- \(E_{\text{ind}}\): 분극/유도(전기장에 의한 전자 재배열)가 얼마나 큰지
- \(E_{\text{disp}}\): 분산력이 얼마나 지배적인지
- 각 항의 exchange-counterpart까지 포함해 해석 가능

즉, SAPT는 “왜 붙는지/왜 밀어내는지”를 **정량적으로 분해해 설명**하는 데 특히 유용합니다.

---

## 참고/출처

- Wikipedia, *“Symmetry-adapted perturbation theory”* (사용자 제공 발췌 기반 정리, CC BY-SA 계열 라이선스 문서).
