---
date: "2025-05-20"
paper_title: "Solubility Behavior of CO2 in Ionic Liquids Based on Ionic Polarity Index Analyses"
short_title: "이온 극성 지수 분석에 기반한 이온성 액체 내 CO2 용해도 거동"
authors: "Xiaoyang Liu, Kathryn E. O’Harra, Jason E. Bara, and C. Heath Turner"
journal: "J. Phys. Chem. B"
year: 2021
status: "translated"
tags: [Ionic Liquids, CO2 Solubility, Ionic Polarity Index, DFT, Molecular Simulation]
category: "Research"
summary: "이 연구는 이온 극성 지수(IPI)를 사용하여 이온성 액체(IL) 내의 CO2 용해도를 예측하는 새로운 스크리닝 방법을 제안합니다. 다가(multivalent) 및 일가(monovalent) 이온에 대한 양자 화학 계산을 통해 정전기적 특성과 자유 부피(FFV)가 용해도에 미치는 영향을 분석하고, 이를 바탕으로 효율적인 이온성 액체 설계를 위한 용해도 상평형 그림을 제시합니다."
file_ref: "Solubility Behavior of CO2 in Ionic Liquids Based on Ionic Polarity Index Analyses.pdf"
---

<!-- Page 1 -->

# 이온 극성 지수 분석에 기반한 이온성 액체 내 CO$_2$ 용해도 거동

**Xiaoyang Liu, Kathryn E. O’Harra, Jason E. Bara, and C. Heath Turner\***

**Cite This:** *J. Phys. Chem. B* 2021, 125, 3665−3676

---

**초록 (ABSTRACT):** 이온성 액체(Ionic liquids, ILs)는 다양한 음이온과 양이온의 적절한 선택을 통해 효과적인 CO$_2$ 용매로 작용할 수 있습니다. 그러나 잠재적인 IL 조성의 라이브러리가 방대하기 때문에, 예상되는 물성을 특성화하고 순위를 매기기 위한 빠른 스크리닝(screening) 방법이 필요합니다. 우리는 최근 부피 기반 접근법과 정전기 전위(electrostatic potential) 분석을 효과적으로 연결하고, 바람직한 IL 물성을 빠르게 스크리닝하는 데 사용할 수 있는 단일 지표인 **이온 극성 지수(ionic polarity index, IPI)** 파라미터를 제안했습니다. 본 연구에서는 해당 음이온 및 양이온의 IPI를 사용하여 IL 내 CO$_2$ 부피 용해도(volumetric solubility)에 대한 상관관계를 생성합니다. 이러한 관계는 일반적으로 동족 이온 계열(homologous ion series) 내의 IL 그룹에 적용할 수 있으며, 이는 가스 용매화 성능을 극대화하기 위해 서로 다른 이온 쌍을 사전 선별(prescreening)하는 데 특히 유용할 수 있습니다.

---

## ■ 서론 (INTRODUCTION)

산업용 가스 포집, 특히 CO$_2$ 포집 및 분리를 위해 이온성 액체(ILs)를 사용하는 것에 대한 많은 관심이 있어 왔습니다.$^{1-3}$ 벌크(bulk) IL은 높은 비용, 높은 점도 등의 요인으로 인해 실행 가능한 산업적 규모의 솔루션을 제공하지 못할 수 있지만, IL의 이점을 활용할 수 있는 몇 가지 고분자 플랫폼이 있습니다. 여기에는 지지된 IL 막(supported IL membranes, SILMs),$^{4,5}$ 중합된 이온성 액체(polymerized ionic liquids, PILs),$^{6}$ 그리고 이온성 폴리이미드(ionic polyimides)와 같은 기타 하이브리드/복합 재료가 포함됩니다.$^{7-10}$

지난 10~20년 동안 컴퓨터 자원이 급격히 증가함에 따라 IL 설계를 위한 합리적인 스크리닝 접근법이 등장했습니다. 다양한 계산 접근법(및 기본 가정)을 기반으로 잘 알려진 스크리닝 기술에는 양자 구조-물성 관계(Quantum Structure−Property Relationship, QSTR), 부피 기반 열역학(Volume-Based Thermodynamic, VBT) 또는 부피 기반 접근법(Volume-Based Approach, VBA),$^{11-13}$ 실제 용매화를 위한 도체 유사 스크리닝 모델(COnductor-like Screening MOdel for Realistic Solvation, COSMO-RS),$^{14,15}$ 그리고 단일 이온 쌍의 양자 화학 계산$^{16,17}$ 등이 있으며, 이는 최근 리뷰에서 논의되었습니다.$^{18}$

보다 구체적으로, IL 내 가스 용해도를 스크리닝하기 위한 예측 계산 기술은 UNIFAC(universal quasi-chemical functional-group activity coefficients)$^{19}$과 같은 활동도 계수 모델, COSMO-RS$^{14,15}$ 또는 개선된 버전인 COSMO-SAC(COSMO segment activity coefficient),$^{20}$ 그리고 RST(regular solution theory)$^{21,22}$를 포함한 여러 열역학적 접근법을 활용해 왔습니다. 또한 GCNLF(group contribution nonrandom lattice−fluid) EOS,$^{23,24}$ GC(group contribution) EOS,$^{25}$ SAFT 기반(statistical associating fluid theory) EOS$^{26}$와 같은 상태 방정식(EOS) 모델도 사용되었습니다. IL 내 가스 용해도를 예측하기 위한 이러한 모델들의 방법론과 성능은 Lei 등의 최근 리뷰에 요약되어 있습니다.$^{2}$ IL 내 CO$_2$ 용해도 예측과 관련하여 가장 일반적인 접근 방식은 COSMO-RS$^{14,15}$ 또는 COSMO-SAC$^{20}$인 경향이 있습니다. 이들은 IL 분자 구조에 대한 정보만 필요로 하는 *a priori* 예측 방법(실험적 파라미터화와 무관함)입니다.$^{2}$

예를 들어, Zhang 등$^{27}$은 COSMO-RS를 사용하여 408개의 서로 다른 IL(24개 양이온 및 17개 음이온)에서 CO$_2$ 흡수를 예측했습니다. 그 결과 tris(pentafluoroethyl)-trifluorophosphate ([FEP]$^-$) 음이온을 가진 IL에서 더 많은 CO$_2$가 흡수될 수 있음이 밝혀졌으며(Henry 법칙 상수 0.2 MPa, 이는 298 K에서 IL 내 CO$_2$ 물리흡착의 최저 한계에 해당), 이 결과는 나중에 실험 데이터로 확인되었습니다.$^{27}$ Palomar 등은 또한 20개의 CO$_2$-IL 시스템을 포함하여 35개의 기체 용질-IL 시스템에 대해 Henry 법칙 계수를 예측하기 위한 COSMO-RS 방법을 평가했으며, 시뮬레이션 결과는 실험 데이터와 잘 일치했습니다.$^{28}$ 유사하게, Manan 등$^{29}$은 COSMO-RS를 통해 27개 IL에서 15개 다른 가스의 흡착 거동을 예측했지만, 예측된 결과가 IUPAC 데이터베이스에서 수집된 실험 데이터와 정성적으로만 일치한다는 것을 발견했습니다.$^{2}$ Lei 등$^{2}$이 요약한 바와 같이, IL 내 CO$_2$ 용해도를 예측하기 위해 UNIFAC과 COSMO-RS 모델을 비교할 때, UNIFAC 결과가 실험 데이터에 더 가까운 경향이 있는 반면, 두 가지 버전의 COSMO-RS 모델은 큰 편차를 보입니다.$^{2}$ 이는 COSMO-RS가 *a priori* 예측을 제공하는 반면 UNIFAC은 실험적으로 파라미터화되었기 때문에 놀라운 일은 아니지만, IL 스크리닝을 전적으로 COSMO-RS 결과에만 의존할 때는 주의가 필요하다는 사실을 강조합니다.$^{2}$

<!-- Page 2 -->

여기서 우리는 CO$_2$ 가스 흡착을 위한 IL 스크리닝을 위해 빠르고 신뢰할 수 있으며(동족 IL 계열 내에서), 다가(multivalent) IL에도 적용 가능한 대안적인 계산 접근 방식을 취합니다. 우리의 이전 분자 수준 모델링 연구$^{30}$는 다가 IL이 높은 자유 부피(free volume)와 CO$_2$ 흡수 용량으로 인해 CO$_2$ 포집 응용 분야에서 잠재적으로 효과적일 수 있음을 시사했습니다. 이 모델링 연구는 전반적인 IL 성능에 대한 기저 기여도를 강조했는데, 이는 두 가지 별개의 원천인 **음이온 효과(anion effect)**와 **자유 부피 효과(free volume effect)**에서 비롯됩니다. 또한, IL 내의 평균 정전기 전위(electrostatic potential, ESP)와 결과적인 부분 자유 부피(fractional free volume, FFV) 및 CO$_2$와의 상호 작용 사이에는 강력한 연관성이 있습니다(예: 평균 ESP 크기가 낮을수록 CO$_2$ 부피 용해도가 높음). 우리의 이전 분자 동역학(MD) 결과$^{30}$는 또한 두 가지 다른 하위 범주의 IL 시스템과 예상되는 거동을 구별했습니다: (1) *작은 FFV를 가진 IL:* 동족 양이온 IL 시리즈를 비교할 때, CO$_2$ 용해도는 CO$_2$와 음이온 종의 친화력에 반비례합니다; (2) *큰 FFV를 가진 IL:* CO$_2$ 용해도는 음이온과 CO$_2$의 친화력에 비례하여 증가합니다. 현재 연구는 높은 FFV를 가진 IL을 추가로 탐색하고 빠른 스크리닝 프로토콜로 성능을 평가하려는 노력입니다. 따라서 우리가 선택한 IL은 하나 또는 두 개의 방향족 고리에 직접 연결된 두 개 이상의 양이온(또는 음이온)을 포함하며, 측쇄의 크기는 최소화되어 효과적으로 IL "골격(frameworks)"을 형성합니다(그림 1에 설명됨).$^{30}$

일반적으로 벌크 IL 내의 전체적인 정전기적 환경은 별도의 음이온 및 양이온 정전기적 기여의 조합으로 근사할 수 있습니다$^{30}$ (편극성 및 고차 상호 작용 무시). 정전기 전위 계산은 분자의 친전자성 및 친핵성 공격 위치를 찾는 데 광범위하게 사용되어 왔으며,$^{31,32}$ 우리의 경우 이는 반대 이온 간 또는 CO$_2$와 양이온/음이온 간의 결합 위치를 식별하는 것과 관련이 있습니다. 우리의 이전 연구는 벌크 IL 또는 이미다졸 기반 용매 내의 ESP가 CO$_2$ 포집$^{30}$ 또는 가스 분리 응용 분야$^{33}$에서 IL을 위한 스크리닝 도구로 사용될 수 있음을 나타냈습니다. 결과적으로, 우리는 **이온 극성 지수(IPI)**라고 하는 새로운 양자 화학(QC) 기반 파라미터를 제안했습니다. 이는 이온의 평균 정전기 표면 전위($\bar{V}$)와 이온의 순 전하($q$)의 비율로 정의됩니다.$^{34}$ IPI는 VBA와 ESP 분석을 효과적으로 혼합하며, 일가 및 다가 이온 모두에 일관되게 적용될 수 있습니다.

이전 MD$^{30}$ 및 밀도 범함수 이론(DFT) 연구$^{34}$에서 보고된 다가 IL을 기반으로, 우리는 CO$_2$와의 상호 작용과 관련하여 IL 정전기적 특성(예: 평균 ESP($\bar{V}$), 글로벌 ESP 극값($V_X$), IPI($\bar{V}/q$))의 역할을 조사합니다. 비교를 위해, 우리는 $n = 1-12$인 [C$_n$mim]$^+$ (1-n-alkyl-3-methylimidazolium) 양이온과 [BF$_4$]$^-$ (tetrafluoroborate), [Br]$^-$ (bromide), [CCN$_3$]$^-$ (tricyanomethanide), [Cl]$^-$ (chloride), [OAc]$^-$ (acetate), [PF$_6$]$^-$ (hexafluorophosphate), [Tf$_2$N]$^-$ (bistriflimide)와 같은 더 일반적으로 사용되는 일가 이온에 대해서도 유사한 분석을 포함합니다. 우리는 IPI와 FFV 및 CO$_2$ 용해도 간의 상관관계뿐만 아니라 동일한 음이온 또는 양이온 기반 IL에 대한 FFV-용해도 상평형 그림(phase diagrams)을 확립합니다. 이러한 분석은 CO$_2$ 물리흡착을 위한 일가 및 다가 이온 IL 설계 모두에 대한 가이드라인을 제공하며, 유사한 접근 방식이 다른 가스 종의 물리흡착 스크리닝에도 적용될 수 있습니다.

## ■ 연구 방법 (METHODS)

다양한 이온 종은 QC 방법을 사용하여 이완(relaxed) 및 분석된 후 CO$_2$와의 상호 작용에 대한 상세한 평가가 이어집니다. 기하학적 최적화를 수행하고 고립된 이온의 정전기 전위 특성을 계산하는 데 사용된 QC 방법은 이전 연구에 설명되어 있습니다.$^{34}$ 여기에는 DFT(B97-3c 범함수 사용)를 통해 얻은 121개 이온 데이터 세트에 대해 계산된 IPI 값이 포함됩니다.$^{35}$ 고립된 CO$_2$ 분자에 대한 정전기 전위 분포...

![Figure 1](Figure1_placeholder)
> **Figure 1.** 이온에 흡착된 CO$_2$의 DFT 최적화 구조. 양이온의 H 원자와 CO$_2$의 O 원자 사이, 그리고 음이온의 O 원자와 CO$_2$의 C 원자 사이의 결합 거리(단위: Å)가 그림에 표시되어 있습니다 (빨간색 = 산소, 흰색 = 수소, 회색 = 탄소, 파란색 = 질소, 하늘색 = 불소, 노란색 = 황).

<!-- Page 3 -->

...또는 이온에 결합된 CO$_2$는 고립된 이온에 사용된 분석과 유사하게 Multiwfn$^{36-38}$에 의해 분석됩니다. 고려된 모든 종에 대해, 국소 최소값에 도달했음을 확인하고 영점 진동 에너지(ZPE)를 얻기 위해 진동수 계산(frequency calculations)이 수행됩니다. 이온과 CO$_2$의 결합 에너지는 Gaussian 09$^{42}$를 사용하여 B3LYP 범함수$^{39,40}$와 더 큰 6-311 + g(d,p) 기저 집합(basis set) 및 DFT-D3 보정$^{41}$을 사용한 단일 점 에너지 계산을 기반으로 합니다. 결합 상호 작용을 평가할 때 기저 집합 중첩 오류(BSSE)를 설명하기 위해 Counterpoise (CP) 보정도 적용됩니다.$^{43}$

상호 작용 에너지($E_{\text{int}}$)는 식 1과 같이 이완된 복합체의 총 에너지($E_{\text{complex}}$)에서 고립된 이온과 CO$_2$ 분자의 에너지 합($E_{\text{ion}}^*$ 및 $E_{\text{CO}_2}^*$, 각각 결합된 복합체에서 얻은 해당 종의 기하학적 구조에 해당하며 별표로 표시됨)을 뺀 값으로 정의됩니다.

$$ E_{\text{int}} = E_{\text{complex}} - (E_{\text{ion}}^* + E_{\text{CO}_2}^*) \quad (1) $$

이에 비해, 결합 에너지($E_{\text{bind}}$)는 이완된 복합체와 가장 낮은 에너지 기하학적 구조를 가진 이완된 분리된 종 간의 에너지 차이로 정의됩니다. 또한 이러한 에너지 값은 복합체 내 분자 간의 상호 작용 에너지($E_{\text{int}}$), 영점 진동 에너지 차이($\Delta E_{\text{ZPE}}$), 변형 에너지($E_{\text{def}}$)로 세분화될 수 있습니다. 마지막 항은 이온이나 CO$_2$가 이완된 복합체에서 발견되는 새로운 기하학적 구조를 채택하기 위한 구조적 변화와 관련된 에너지를 설명합니다.$^{18}$

$$ E_{\text{bind}} = E_{\text{int}} + \Delta E_{\text{ZPE}} + E_{\text{def}} \quad (2) $$

실제로 IL은 일반적으로 이온 교환을 포함하는 복분해 반응(metathesis reaction)에 의해 합성됩니다. 이온은 자체적으로 존재하지 않고 반대 이온을 동반합니다.$^{18}$ 따라서 $E_{\text{int}}$는 IL 시스템의 상호 작용을 비교하는 데 더 적절한 기준을 제공합니다.

궁극적으로 CO$_2$-이온 종의 결합 에너지와 특성은 네 가지 다른 기본 상호 작용의 상호 작용에 기인할 수 있습니다: 정전기($E_{\text{elec}}$), 교환($E_{\text{exch}}$), 유도($E_{\text{ind}}$), 분산($E_{\text{dis}}$). 우리는 대칭 적응 섭동 이론(Symmetry-Adapted Perturbation Theory, SAPT)을 사용하여 이러한 기여를 분해합니다. 이는 B3LYP 최적화 기하학적 구조를 사용하여 sSAPT0/jun-cc-pVDZ$^{44}$와 함께 비교적 높은 수준의 이론에서 수행됩니다. 이 접근 방식은 "브론즈(bronze)" 수준 SAPT로 명명되었으며, 0.49 kcal/mol의 전체 오차와 저렴한 계산 비용으로 정확한 상호 작용 에너지를 생성할 수 있습니다.$^{45}$ PSI4$^{46}$ 코드가 SAPT 분석을 수행하는 데 사용됩니다. 또한 SAPT는 본질적으로 BSSE가 없으므로 추가 보정이 필요하지 않습니다. SAPT 결합 에너지는 결합 상태 구성에 해당하는 이온 구조와 관련하여 계산되므로 에너지 기준은 앞서 정의한 $E_{\text{int}}$와 일치해야 합니다. 프레임워크 SAPT에 따르면 총 상호 작용 에너지($E_{\text{SAPT}}$)는 다음과 같이 다양한 기여로 분해될 수 있습니다:

$$ E_{\text{SAPT}} = E_{\text{elec}} + E_{\text{exch}} + E_{\text{ind}} + E_{\text{dis}} \quad (3) $$

## ■ 결과 및 토론 (RESULTS AND DISCUSSION)

우리는 현재 데이터베이스에 있는 IL과 CO$_2$ 간의 상호 작용 평가(에너지의 SAPT 기반 분해 분석 포함)로 시작한 다음, 이러한 결과를 기본적인 IL 특성(예: 정전기적 설명자)과 연결합니다. 마지막으로 IPI를 사용하여 IL 용매 내의 CO$_2$ 용해도를 정량화하고 예측합니다.

**다가 및 일가 이온과 CO$_2$ 간의 상호 작용.** 우리는 최근 여러 다가 및 일반적인 일가 이온(총 121개)의 상세한 ESP 표면 및 기타 정전기적 특성을 제공했습니다.$^{34}$ 이제 이온과 CO$_2$의 상호 작용을 연구하기 위해 그림 1과 같이 이온과 함께 CO$_2$의 흡착된 구조를 최적화하기 위한 추가 QC 계산을 수행했습니다. CO$_2$의 O 원자는 양이온의 글로벌 ESP 최대값에 강하게 흡착되는 반면, CO$_2$의 C 원자는 음이온의 글로벌 ESP 최소값에 강하게 흡착되는 것으로 나타났습니다(즉, 정전기학이 흡착 위치에 강력한 영향을 미침). 흡착 값은 CO$_2$와의 상호 작용에서 이온의 글로벌 ESP 극값의 중요성을 강조하는 데 도움이 됩니다. 이러한 결합 에너지와 SAPT 접근법을 통한 해당 에너지 분해는 **Table 1**에 요약되어 있습니다. 양이온과 CO$_2$의 상호 작용은 이온의 형식 전하(formal charge)에 따라 증가합니다. 즉, 양이온과의 CO$_2$ 결합 에너지 크기는 C3 > C2 > C1이며 값은 각각 -9.43, -7.46, -5.59 kcal/mol입니다. 음이온과 관련하여 결합 에너지의 상대적 크기는 A3 > A1 > A2이며 에너지는 각각 -11.54, -8.36, -8.09 kcal/mol입니다. SAPT 분석과 관련하여 $E_{\text{int}}$와 $E_{\text{SAPT}}$의 차이는 $\pm 1$ kcal/mol 이내입니다. 이는 두 에너지 값이 서로 다른 이론적 접근 방식을 기반으로 하기 때문에 추가적인 일관성 검사를 제공합니다. 결합 에너지에 대한 정전기적 기여는 전체 상호 작용을 지배하며, 이온의 ESP 분석의 중요성을 강조합니다.

우리는 또한 **Table S1**에 나열된 더 일반적인 일가 음이온 및 양이온과 CO$_2$의 상호 작용을 계산했으며, 최적화된 기하학적 구조는 **Figure S1**에 나와 있습니다. 알킬 사슬 길이의 함수로서 [C$_n$mim]$^+$ ($n = 1-12$)와 CO$_2$의 상호 작용 에너지는 **Figure S2**에 나와 있습니다. 이온과 CO$_2$의 분자 간 상호 작용의 본질에 대한 더 깊은 통찰력을 얻기 위해, 이러한 이온의 SAPT 유도 상호 작용 에너지를 계산하여 **Table S1**에 요약했습니다. 여기서 대부분의 이온에 대한 $E_{\text{int}}$와 $E_{\text{SAPT}}$ 간의 편차는 [OAc]$^-$ 음이온을 제외하고 $\pm 1$ kcal/mol 이내입니다. 일부 연구에서는 이미다졸륨 아세테이트 IL이 화학 흡착 메커니즘을 통해 CO$_2$와 상호 작용한다고 보고했으며, 이는 이러한 편차를 설명할 수 있습니다.$^{47,48}$

각 CO$_2$-이온 복합체에 대해 서로 다른 SAPT 유도 인력 기여의 백분율이 계산되었으며...

**Table 1. 진공 상태에서 이온과 CO$_2$ 사이의 상호 작용 에너지 및 결합 에너지(단위: kcal/mol)와 $E_{\text{SAPT}}$ 값에 대한 다양한 기본 기여도**

| | $E_{\text{int}}$ | $\Delta E_{\text{ZPE}}$ | $E_{\text{def}}$ | $E_{\text{bind}}$ | $E_{\text{elec}}$ | $E_{\text{exch}}$ | $E_{\text{ind}}$ | $E_{\text{dis}}$ | $E_{\text{SAPT}}$ |
|---|---|---|---|---|---|---|---|---|---|
| C1...CO$_2$ | −5.59 | 0.48 | 0.33 | −4.78 | −4.36 | 2.97 | −2.32 | −2.02 | −5.73 |
| C2...CO$_2$ | −7.46 | 0.68 | 0.66 | −6.12 | −4.47 | 3.25 | −3.44 | −2.59 | −7.25 |
| C3...CO$_2$ | −9.43 | 0.53 | 0.92 | −7.98 | −5.71 | 3.87 | −5.05 | −2.79 | −9.68 |
| A1...CO$_2$ | −8.36 | 0.49 | 0.80 | −7.08 | −9.88 | 8.37 | −2.59 | −4.71 | −8.81 |
| A2...CO$_2$ | −8.09 | 0.60 | 0.44 | −7.05 | −9.27 | 8.18 | −2.18 | −5.44 | −8.71 |
| A3...CO$_2$ | −11.54 | 0.42 | 1.81 | −9.31 | −14.30 | 9.66 | −4.40 | −3.35 | −12.39 |

<!-- Page 4 -->

...그림 2a에 나와 있습니다. 결과는 정전기적 기여가 지속적으로 주요 역할을 하지만 유도 및 분산 상호 작용도 중요하다는 것을 보여줍니다. 일반적인 일가 음이온의 경우 정전기 에너지가 전체 에너지의 60% 이상을 차지하는 반면, 일반적인 일가 양이온([C$_n$mim]$^+$)의 경우 기여의 55% 이상이 정전기 상호 작용에 기인할 수 있습니다. 더 큰 다가 양이온(C1, C2, C3)의 경우 정전기 기여가 감소하고 양이온 크기에 따라 유도 기여가 증가합니다. 다가 음이온을 포함하는 정전기 상호 작용도 가장 큰 기여를 하지만, 음이온 크기가 커짐에 따라 분산 상호 작용의 기여가 증가하는 반면 유도 및 정전기 기여는 감소합니다.

SAPT 분석 결과는 정전기 에너지가 이온과 CO$_2$ 사이의 총 인력 에너지에 가장 큰 기여를 한다는 것을 나타내며, 이는 CO$_2$와 상호 작용하는 IL에 대한 이전 SAPT 기반 분석과 일치합니다.$^{49}$ 본 연구에서 조사된 다가 음이온의 경우 정전기 기여가 유도 및 분산 기여보다 강하며, 이는 이전 연구에서 보고된 에너지 분해 분석과 잘 일치합니다.$^{30}$ 또한 양이온 종에 관계없이 A3 기반 IL은 CO$_2$와 가장 강한 정전기 상호 작용을 보이며, A1 및 A2 기반 IL이 그 뒤를 잇습니다. 이 거동은 또한 이전 MD 기반 분석에서 CO$_2$와 음이온의 정전기 기여 순서와 일치합니다.$^{30}$ 그러나 양이온을 비교할 때 고립된 양이온과 벌크 IL 내 양이온 거동 사이에 명백한 상관관계가 없는데, 이는 음이온이 벌크 IL 특성(예: 점도 및 흡수 엔탈피)에서 주요 역할을 한다는 것을 나타냅니다. 전반적으로 음이온과 CO$_2$ 상호 작용의 정전기적 기여는 양이온과의 상호 작용보다 큽니다.

우리는 또한 **Figure 2b**와 같이 일가 및 다가 이온과 결합하기 전(고립)과 후의 CO$_2$ ESP 분포를 비교합니다. 비교를 위해 CO$_2$와 결합하기 전/후의 이러한 다가 이온의 ESP 분포는 **Figure S3**에 표시되어 있으며, 일가 이온의 결합 전/후는 **Figure S4**에 표시되어 있습니다. 전반적으로 CO$_2$의 ESP는 결합 환경의 극성에 따라 크게 변하지만, 해당 이온의 ESP는 상대적으로 영향을 받지 않습니다. CO$_2$ ESP 분포 모양은 양이온과 결합할 때(O 원자를 통해) 크게 변하지 않지만 ESP 분포의 하단 끝은 감소하는 경향이 있습니다. O 원자가 양이온과 상호 작용할 때 결합 부위의 ESP는 더 양(positive)이 되는 반면, CO$_2$의 반대쪽 O 원자로부터의 양의 기여는 양이온과의 거리로 인해 감소합니다. 따라서 기체상 CO$_2$ ESP 분포의 왼쪽 피크는 감소하는 반면, 오른쪽 피크는 CO$_2$가 더 높은 $\bar{V}$ 값을 가진 양이온에 결합할 때 증가합니다. CO$_2$가 음이온에 결합할 때 기체상 ESP 분포의 두 피크는 넓어지는데, 이는 중앙에 위치한 결합 부위(C 원자)가 자연스럽게 두 O 원자를 음이온의 정전기적 환경으로 끌어당기기 때문입니다. 따라서 C 원자 피크는 감소하는 반면 두 O 원자에 대한 피크는 증가합니다.

벌크 IL에서 CO$_2$는 고립된 이온과 상호 작용하지 않으므로 실제 시스템의 정전기 상호 작용은 약화될 것입니다. 그러나 **Figure 2**의 정보는 CO$_2$와의 정전기 효과 범위를 해석하기 위한 맥락을 제공합니다. 고전적(힘장 기반) 분자 시뮬레이션 연구에서 편극 효과를 근사하기 위해 IL 분자에 스케일링된(즉, 비정수) 전하를 사용하는 것이 일반적이 되었습니다. **Figure 2**의 정보를 바탕으로 IL에 흡수된 용질 종에 대해 동일한 효과를 모방하기 위해 유사한 경험적 보정이 필요할 수 있습니다.

**다가/일가 이온에 대한 정전기 설명자의 적용.** 최근 논문에서 일가 및 다가 이온의 글로벌 ESP 극값($V_X$)과 평균 ESP($\bar{V}$) 값의 상관관계가 조사되었습니다.$^{34}$ 일반적으로 글로벌 ESP 극값은 이온의 평균 ESP에 따라 증가합니다. 여기서 우리는 또한 **Figure 3**과 같이 일가 및 다가 이온과 CO$_2$의 상호 작용 에너지($E_{\text{int}}$)와 글로벌 ESP 극값($V_X$) 값 사이의 상관관계를 발견했습니다. 음이온과 양이온의 글로벌 ESP 최대 및 최소 위치는 각각 CO$_2$의 가장 극성인 위치와 강하게 상호 작용한다는 점에 유의해야 합니다.

![Figure 2](Figure2_placeholder)
> **Figure 2.** (a) 서로 다른 이온과 CO$_2$의 상호 작용 에너지에 대한 SAPT 유도 기여도. 정전기($E_{\text{elec}}$), 유도($E_{\text{ind}}$), 분산($E_{\text{dis}}$)으로 표시됨. (b) 기체상에 고립된 CO$_2$(회색으로 표시되고 CO$_2$로 라벨링됨) 대 서로 다른 이온에 결합된 CO$_2$의 Multiwfn$^{36-38}$으로 분석된 1 kcal/mol 간격의 정전기 전위 분포 비교. 명확성을 위해 복합체의 라벨은 이온 종만 식별합니다(예: BF$_4$는 [BF$_4$]$^-$에 결합된 CO$_2$를 나타냄). 삽입 그림은 $\rho = 0.001$ e/Bohr$^3$에서 고립된 CO$_2$의 ESP 매핑된 분자 vdW 등가면이며, 색상 스케일은 (-13, 28) kcal/mol입니다.

<!-- Page 5 -->

이온의 글로벌 극값은 원자가와 작용기의 특성에 의해 결정됩니다. 이러한 상관관계는 IPI 파라미터의 중요성에 대한 이전 논의와 결합되어, 단순히 이온의 부피와 원자가에 기초하여 CO$_2$에 대한 이상적인 IL 흡수제를 찾는 것을 안내하는 매우 간단한 맥락을 제공합니다. 그러나 이전 연구$^{30}$에서 논의한 바와 같이, 양이온/음이온과 CO$_2$의 특히 강하거나 약한 상호 작용은 흡착을 저해합니다. 반대 이온 및 양이온/음이온과 CO$_2$의 친화력을 포함한 최적의 정전기적 상보성은 더 높은 CO$_2$ 용해도로 이어집니다.$^{30}$

이온의 정전기적 상보성 때문에 글로벌 극값은 반대 이온 간의 가장 활성적인 결합 부위이기도 합니다. 따라서 경쟁으로 인해 고립된 이온의 글로벌 극값은 벌크 IL에서 CO$_2$가 반드시 접근할 수 있는 것은 아닙니다. 그러나 벌크 [C$_4$mim]-[Tf$_2$N]에 대한 최근 MD 시뮬레이션 연구$^{50}$에 따르면 상온에서 이온의 약 15%가 "자유 상태(free states)"에 있어 글로벌 극값의 의미 있는 부분이 접근 가능할 수 있음을 시사합니다. 또한 대칭성이 높은 이온의 경우 여러 개의 동일한 글로벌 극값이 존재하는 경우가 많으며, 이는 이러한 유리한 흡수 부위 중 하나가 접근 가능할 가능성을 높입니다(이온이 여러 반대 이온으로 둘러싸인 구성 포함).

**다가 IL에서 IPI와 CO$_2$ 용해도의 연결.** 다가 음이온 및 양이온에 대한 이전 연구에 따르면 벌크 IL에 대해 계산된 평균 ESP 값은 IL의 CO$_2$ 용해도 및 FFV와 직접적인 상관관계가 있을 수 있습니다.$^{30}$ 그러나 이 분석에는 시간이 많이 소요되는 MD 및 그랜드 캐노니컬 몬테카를로(GCMC) 시뮬레이션이 필요합니다(예: 이러한 시스템을 초기화하고 평형화하는 데 시간이 많이 걸릴 수 있으며 일반적으로 긴 시뮬레이션 시간이 필요함). 따라서 분자 수준 시뮬레이션의 예측 능력에도 불구하고 CO$_2$ 포집 또는 분리와 같은 특정 응용 분야를 위한 IL의 빠른 스크리닝에 필요한 효율성이 부족한 경우가 많습니다. 따라서 우리는 후보 IL의 자동화된 분석 및 사전 선별에 더 적합한 DFT 기반 계산에 중점을 둡니다.

음이온 효과와 자유 부피 효과를 모두 시각화하기 위해 **Figure 4**는 음이온 및 양이온 IPI의 함수로서 CO$_2$ 용해도의 2D 등고선 지도를 보여줍니다. 가장 낮은 용해도 값과 가장 높은 용해도 값은 모두 높은 음이온 IPI 영역 내에 나타나며, 이는 A1 기반 IL에 해당합니다. 양이온 IPI 페어링은 용해도 스펙트럼상의 위치를 결정합니다. 양이온과 음이온 IPI 값의 차이가 클수록 FFV가 증가하여 CO$_2$ 흡수가 향상됩니다. 따라서 현재의 경우 음이온의 IPI 값은 최대화되어야 하고 양이온의 IPI는 최소화되어야 합니다. 이 분석에 따르면 A1C3는 후보 풀 내에서 최적의 선택이어야 하며, 이는 MD/GCMC 시뮬레이션에서 예측된 이전 결과와 일치합니다.$^{30}$ 그러나 이러한 IL은 더 큰 IL 후보 풀의 작은 조각일 뿐이므로 결과가 동족 이온 계열 외부에는 광범위하게 적용되지 않을 수 있습니다.

**다양한 접근법으로 계산된 FFV 비교.** 연구자들 사이에서 널리 인정받고 있는 이전에 제안된 FFV 방정식은 다음과 같이 계산할 수 있습니다.$^{51}$

$$ \text{FFV} = (V_m - V_0)/V_m = 1 - \rho V_0 \quad (4) $$

여기서 $V_m = 1/\rho$는 비체적(specific volume)이고 $V_0$는 점유 부피(occupied volume)입니다. Lee$^{51}$는 이 점유 부피가 영점 몰 부피(즉, 0 K에서)이며, 이는 다음 방정식과 같이 Bondi 그룹 기여 방법$^{52}$을 통해 이론적으로 결정된 반데르발스(vdW) 부피와 밀접한 관련이 있다고 지적했습니다.

$$ V_0 = 1.3 V_{\text{vdW}} \quad (5) $$

1.3이라는 값은 대략적인 스케일링 계수입니다. 그러나 최근에는 1.288이라는 값이 더 적절한 것으로 밝혀졌습니다.$^{53}$ 따라서 FFV는 $V_{\text{vdW}}$와 다음과 같이 관련될 수 있습니다.

$$ \text{FFV} = (V_m - 1.3 V_{\text{vdW}})/V_m \quad \text{또는} $$
$$ \text{FFV} = (V_m - 1.288 V_{\text{vdW}})/V_m \quad (6) $$

COSMO 부피와 Bondi 그룹 기여로 계산된 vdW 부피를 비교함으로써 Shannon 등은 일부 유기 분자의 경우 COSMO 부피가 $1.3 \times V_{\text{vdW}}$에 매우 가깝다($\pm 5\%$)는 것을 발견했습니다.$^{54}$ 따라서 그들은 COSMO에 따라 IL 내의 FFV를 다음과 같이 계산할 것을 제안했습니다.

$$ \text{FFV}_{\text{cosmo}} = (V_m - V_{\text{cosmo}})/V_m \quad (7) $$

![Figure 3](Figure3_placeholder)
> **Figure 3.** 이온 ESP 매핑된 분자 vdW 표면($\rho = 0.001$ e/Bohr$^3$ 등가면)의 $V_X$와 $E_{\text{int}}$의 상관관계. 주황색: Table S1에 나열된 일반적인 IL 음이온; 빨간색: 본 연구에서 연구된 A1, A2, A3; 보라색: $n = 1-12$인 [C$_n$mim]$^+$; 파란색: 본 연구에서 연구된 C1, C2, C3.

![Figure 4](Figure4_placeholder)
> **Figure 4.** 음이온 및 양이온 IPI의 함수로서 CO$_2$ 용해도(이전 MD/GCMC 시뮬레이션$^{30}$ 기반)의 등고선 플롯.

<!-- Page 6 -->

또한 Shannon의 논문$^{54}$에 나열된 바와 같이 Bondi 및 COSMO 방법을 사용하여 여러 유기 용매의 FFV를 비교할 때 과소평가와 과대평가가 모두 발생했습니다. Zhu 등$^{55}$은 이상 기체 상태에서 6-311++ g(d,p) 기저 집합과 함께 B3LYP를 사용하여 Gaussian 09로 일반적으로 사용되는 이온의 이온 부피를 계산했습니다. 그들은 또한 BVP86/TZVP/DGA1 이론 수준에서 Gaussian 03을 사용하여 COSMO 부피를 계산했습니다.$^{55}$ 그들은 COSMO 부피가 vdW 부피에 가깝다는 것을 발견했으며, 이는 $V_{\text{vdW}} \approx V_{\text{cosmo}}$임을 의미합니다. 그들은 또한 [C$_n$mim][BF$_4$] ($n = 2, 4, 6, 8$)의 FFV를 계산했으며 결과는 Shannon의 결과보다 높았습니다. 우리의 계산에서도 vdW 부피 표면이 $\rho = 0.001$ e/Bohr$^3$ 등가면으로 정의될 때 이온에 대한 COSMO 부피가 Multiwfn에서 계산된 vdW 부피에 가깝다는 것을 발견했습니다(**Table 2** 참조).

편의성 때문에 COSMO-RS 방법은 IL의 FFV를 예측하는 데 자주 사용되었습니다(실험적 CO$_2$ 흡수 성능을 설명하기 위해). 그러나 COSMO-RS 접근법을 통해 추정된 FFV는 잠재적으로 비정상적인 결과를 초래할 수 있습니다. COSMO-RS 가정 중 하나는 IL이 가능한 한 "이온성"(또는 극성)이어야 한다는 것입니다. 즉, 양이온 크기가 최소화되고(예: 짧은 알킬 사슬) 음이온이 완전히 비편재화되고 크기가 최대화될 때 이러한 특성이 최적화된다는 의미입니다.$^{54}$ 실제로 이러한 IL에는 특히 동종 이온(co-ions) 내의 상호 작용을 통해 눈에 띄는 구조적 분리 및 불균일성이 있을 수 있으며, 이는 이전 연구에서 연구된 A2 기반 IL과 같이 FFV 값을 높일 수 있습니다.$^{30}$ 결과적으로 COSMO로 계산된 FFV는 분자 시뮬레이션과 직접 비교할 때 일관되지 않은 결과를 초래할 수 있습니다.

IL 내의 FFV를 벤치마킹하기 위해 앞서 설명한 접근 방식(OPLS-AA 힘장$^{56}$의 개별 원자의 Lennard-Jones 직경을 기반으로 한 무한히 작은 프로브로 측정)을 통해 300 K 및 1 bar에서 MD 시뮬레이션에서 직접 얻은 데이터를 사용합니다. 이는 벌크 구조 환경이 직접 평가되므로 COSMO-RS보다 더 신뢰할 수 있을 것으로 예상됩니다. 비교를 위해 이러한 IL의 COSMO-RS 계산도 수행하여 FFV 값을 추정했습니다.

우리는 또한 Gromacs의 자유 부피 도구(gmx freevolume)$^{57}$를 사용하여 MD 시뮬레이션에서 IL의 FFV를 계산했습니다. 이는 Bondi 값으로 원자 반경을 추정합니다.$^{52,58}$ 보고된 FFV 값은 $\text{FFV}^0 = (V_m - V_{\text{vdW}})/V_m$ 및 $\text{FFV} = (V_m - 1.3V_{\text{vdW}})/V_m$으로 계산됩니다. 여기서 우리는 다른 방법으로 계산된 FFV 값의 정의를 명확히 하고자 합니다. (a) $\text{FFV}^0$는 무한히 작은 프로브, 즉 0 Å에 해당하는 FFV에 해당하는 부분 자유 부피를 나타내며, (b) FFV는 다음에 해당하는 부분 자유 부피를 나타냅니다...

**Table 2. COSMOThermX, 분자 시뮬레이션(MD/GCMC)의 몬테카를로 추정치, Multiwfn 프로그램을 사용한 DFT에서 계산된 IL의 vdW 부피 및 FFV 비교$^a$**

| | COSMO-RS | | Multiwfn | MD/GCMC | | MD gmx freevolume | |
|---|---|---|---|---|---|---|---|
| | $V_m$ | $V_{\text{cosmo}}$ | $\text{FFV}_{\text{cosmo}}$ | $V_{\text{vdW}}$ | $\text{FFV}^0$ (LJ) | $\text{FFV}^0$ (Bondi) | $\text{FFV}^0$ (gmx) | $\text{FFV}$ (gmx) |
| | Å$^3$ | Å$^3$ | | Å$^3$ | | | | |
| A1C1 | 618 | 569 | 0.081 | 598 | 0.253 | 0.281 | 0.280 | 0.064 |
| A1C2 | 1771 | 1604 | 0.094 | 1679 | 0.310 | 0.333 | 0.334 | 0.135 |
| A1C3 | 1207 | 1039 | 0.139 | 1079 | 0.321 | 0.343 | 0.343 | 0.146 |
| A2C1 | 857 | 766 | 0.106 | 775 | 0.289 | 0.307 | 0.308 | 0.101 |
| A2C2 | 2486 | 2196 | 0.117 | 2210 | 0.360 | 0.375 | 0.374 | 0.186 |
| A2C3 | 1684 | 1433 | 0.149 | 1433 | 0.346 | 0.361 | 0.360 | 0.168 |
| A3C1 | 1677 | 1441 | 0.141 | 1510 | 0.269 | 0.293 | 0.292 | 0.080 |
| A3C2 | 796 | 670 | 0.159 | 697 | 0.319 | 0.339 | 0.337 | 0.138 |
| A3C3 | 3265 | 2587 | 0.208 | 2667 | 0.328 | 0.348 | 0.346 | 0.150 |

$^a$ [cation]$_n$[anion]$_m$의 IL 쌍에 대해 $V_m$ 또는 $V_{\text{vdW}} = n \cdot V_{\text{cation}} + m \cdot V_{\text{anion}}$.

![Figure 5](Figure5_placeholder)
> **Figure 5.** (a) 이온 극성 차이와 $\text{FFV}^0$ 간의 음이온 의존적 상관관계. (b) 벌크 IL 내 MD 시뮬레이션된 $\text{FFV}^0$ (LJ) 대 IPI에 의한 분석적 예측(보라색): $\text{FFV}^0 = 0.9 - 0.003 \cdot (\bar{V}_A/q_A + 2\bar{V}_C/q_C)$, RMSE = 0.012. 선은 눈을 위한 가이드이며 음영 처리된 영역은 RMSE 내의 값을 나타냅니다. COSMO-RS 접근법(빨간색)으로 추정된 $\text{FFV}_{\text{cosmo}}$ 값과 MD 시뮬레이션의 LJ 파라미터에 의해 정의된 $\text{FFV} = 1.3\text{FFV}^0(\text{LJ}) - 0.3$ (파란색)이 비교를 위해 포함되었습니다.

<!-- Page 7 -->

...시스템에서 실제로 접근 가능한 공간입니다. 이 두 번째 정의는 1.3 계수를 포함하는 FFV에 해당합니다.

이러한 결과는 **Table 2**와 같이 Lennard-Jones (LJ) 시그마 파라미터 또는 Bondi 반경으로 정의된 원자 표면을 사용하여 MD 시뮬레이션에서 가져온 이전 몬테카를로 추정치와의 비교로 제공됩니다. 결과는 매우 일관적입니다. 그러나 COSMO로 계산된 FFV는 동일한 경향을 따르지 않습니다. 예를 들어 A3 기반 IL은 A2 기반 IL보다 더 큰 FFV 값을 갖습니다. 따라서 COSMO-RS로 계산된 FFV는 다양한 음이온 종을 가진 IL을 비교하는 데 적합하지 않을 수 있습니다. MD 기반 추정치는 유한한 온도에서 벌크 시스템의 FFV를 직접 추정하기 때문에 훨씬 더 정확할 것으로 예상됩니다. 기본적으로 다음 섹션의 $\text{FFV}^0$ 값은 **Table 2**에 보고된 $\text{FFV}^0$ (LJ)를 나타냅니다.

FFV 비교 외에도 COSMO-RS로 예측한 CO$_2$ 용해도를 직접적인 MD/GCMC 결과와 비교하며, 자세한 내용은 지원 정보(Supporting Information)의 섹션 3에 제공됩니다. 몇 가지 유사한 경향이 있지만 COSMO-RS로 예측한 정량적 결과는 MD/GCMC로 얻은 값과 거리가 멀어 COSMO-RS가 다가 IL의 CO$_2$ 용해도를 예측하는 데 적합하지 않을 수 있음을 시사합니다.

**IPI와 FFV의 연결.** FFV 추정치 외에도 총 FFV 값을 음이온과 양이온에서 발생하는 기여로 분해하려고 시도했습니다. 우리는 이전에 FFV와 IL 내 평균 ESP(MD 시뮬레이션에서)의 선형 관계를 확인했으므로,$^{30}$ 양이온/음이온 종과 FFV 사이에 만들 수 있는 가능한 DFT 기반 연결이 있습니다. 따라서 우리는 음이온과 양이온의 IPI 값 차이의 함수로 FFV를 플롯하고, 이를 **Figure 5a**와 같이 **이온 극성 차이(ionic polarity difference, IPD = $\bar{V}_A/q_A - \bar{V}_C/q_C$)**라고 합니다. IPD와 FFV 간의 상관관계는 이 선형 관계의 절편(여기서는 "본능적 자유 부피(instinctive free volume)"라고 함)이 음이온의 선택에 의해 강력하게 결정됨을 나타냅니다. 음이온의 본능적 자유 부피는 A2 > A3 > A1이며, 이는 vdW 부피의 순서와 일치하고 음이온 IPI 값의 반대 순서와 일치합니다. FFV는 IPD에 대해 증가하며, 이는 잠재적으로 음이온과 양이온 종 사이의 응집력 또는 상보성이 감소함을 나타냅니다. 동일한 음이온을 가진 IL을 비교할 때 FFV는 양이온의 부피에 대해 증가하는 경향이 있지만 유의미하지는 않습니다.

단순화를 위해 $\text{FFV}^0$ 대 IPD 기울기가 다른 음이온 그룹에 대해 불변(평균 기울기는 0.006)이라고 가정하면, $\text{FFV}^0 = 0.006 \cdot (\bar{V}_A/q_A - \bar{V}_C/q_C) + [- 0.009 \cdot (\bar{V}_A/q_A) + 0.9]$ 또는 $\text{FFV}^0 = 0.9 - 0.003 \cdot (\bar{V}_A/q_A + 2\bar{V}_C/q_C)$ (RMSE = 0.012)가 됩니다. MD 시뮬레이션된 $\text{FFV}^0$ (LJ) 값과 예측된 FFV 값의 상관관계는 **Figure 5b**에 나와 있으며, 일반적으로 사용되는 COSMO-RS 접근법$^{54}$ $\text{FFV}_{\text{cosmo}} = (V_m - V_{\text{cosmo}})/V_m$으로 계산된 FFV 값과 MD 시뮬레이션의 LJ 파라미터에 의해 $\text{FFV} = 1.3\text{FFV}^0(\text{LJ}) - 0.3$으로 정의된 값도 참조로 표시됩니다. 예측된 FFV 값(보라색으로 표시됨)에 약간의 산포가 있지만 예측이 빠르며 다음 섹션과 같이 용해도를 평가하기 위해 IPI와 결합할 수 있습니다.

**IPI와 용해도의 연결.** 정전기 정보를 기반으로 IPI 방정식으로 예측된 $\text{FFV}^0$ 값을 사용하여 음이온 IPI 기준으로 CO$_2$ 용해도 예측(RMSE = 2.893 g/L)을 도출할 수 있습니다. 자세한 내용은 지원 정보의 섹션 4에 제공됩니다.

$$ S_{\text{CO}_2}[\text{g/L}] = 25 \cdot [(\bar{V}_A/q_A) - 58] \cdot (\text{FFV}^0 - 0.275) + 10 \quad (8) $$

유사하게, IPI 예측 $\text{FFV}^0$ 값을 사용한 양이온 IPI 기준에 기반한 용해도 예측 방정식(RMSE = 2.906 g/L)은 다음과 같이 쓸 수 있습니다.

$$ S_{\text{CO}_2}[\text{g/L}] = 70 \cdot [(\bar{V}_C/q_C) - 68] \cdot (\text{FFV}^0 - 0.335) + 20 \quad (9) $$

CO$_2$ 용해도 예측과 GCMC 시뮬레이션 값의 비교는 **Figure 6**에 나와 있습니다. GCMC 시뮬레이션의 상세한 FFV-용해도 상관관계는 이전 논문의 그림 7에 나와 있습니다.$^{30}$ 여기서 음이온/양이온 용해도 예측 방정식에는 두 가지 의미 있는 요소가 있습니다: $\bar{V}_A/q_A = 58$ kcal/mol/e 및 $\bar{V}_C/q_C = 68$ kcal/mol/e. 이는 다음 섹션에서 자세히 설명하는 바와 같이 음이온 또는 양이온 계열 내에서 FFV에 대해 CO$_2$ 용해도가 어떻게 변하는지를 결정했습니다.

**FFV-용해도 상평형 그림(Phase Diagram).** 음이온 용해도 및 FFV 예측 방정식을 기반으로 **Figure 7**과 같이 식별할 수 있는 4가지 특징적인 영역이 있습니다.

![Figure 6](Figure6_placeholder)
> **Figure 6.** 벌크 IL 내 GCMC 시뮬레이션된 CO$_2$ 용해도 대 예측된 용해도. (a) 수정된 음이온 용해도 방정식: $S_{\text{CO}_2}[\text{g/L}] = 25 \cdot [(\bar{V}_A/q_A) - 58] \cdot (\text{FFV}^0 - 0.275) + 10$, RMSE = 2.893 g/L. (b) 수정된 양이온 용해도 방정식: $S_{\text{CO}_2}[\text{g/L}] = 70 \cdot [(\bar{V}_C/q_C) - 68] \cdot (\text{FFV}^0 - 0.335) + 20$, RMSE = 2.906 g/L. 두 플롯의 선은 눈을 위한 가이드이며 음영 처리된 영역은 RMSE 내의 값을 나타냅니다.

<!-- Page 8 -->

7a. 유사하게, **Figure 7b**와 같이 양이온 용해도 및 FFV 예측 방정식을 기반으로 한 4가지 특징적인 영역이 있습니다.

동일한 음이온 기반 IL을 비교할 때, 영역 1과 4의 경우 양이온 IPI가 감소함에 따라(자유 부피 효과에 의해 지배됨) 용해도가 증가하고, 영역 2와 3의 경우 양이온 IPI가 증가함에 따라(음이온 효과에 의해 지배됨) 용해도가 증가합니다. 동일한 양이온 기반 IL을 비교할 때, 영역 5와 8의 경우 음이온 IPI가 감소함에 따라(자유 부피 효과에 의해 지배됨) 용해도가 증가하고, 영역 6과 7의 경우 음이온 IPI가 증가함에 따라(음이온 효과에 의해 지배됨) 용해도가 증가합니다. 더 높은 CO$_2$ 용해도 영역(2, 4, 7, 및...

![Figure 7](Figure7_placeholder)
> **Figure 7.** (a) 동일한 음이온 기반 IL 및 (b) 동일한 양이온 기반 IL에 대한 FFV-용해도 상평형 그림. 파란색 영역은 자유 부피 효과가 지배적인 반면, 빨간색 영역은 음이온 효과에 더 강한 영향을 받습니다. 조건은 $P = 1$ bar 및 $T = 300$ K에 해당합니다.

![Figure 8](Figure8_placeholder)
> **Figure 8.** $T = 298$ K에서 (a) [Tf$_2$N] 기반 이미다졸륨 IL 및 (b) [C$_4$mim] 기반 IL 내 실험적으로 측정된 CO$_2$ 몰 분율 용해도와 양이온/음이온 IPI의 플롯, 그리고 (c) [Tf$_2$N] 기반 IL 및 (d) 불소 기능화된 [C$_6$mim] 기반 IL. Brennecke 등$^{59,60}$의 연구에서 가져옴. 점선은 눈을 위한 가이드입니다.

<!-- Page 9 -->

...8)의 경우, 큰 부피를 가진 다가 음이온 또는 양이온이 더 작은 일가 반대 이온과 짝을 이루어 향상된 CO$_2$ 용해도를 발생시킵니다.

이러한 용해도 및 FFV 예측은 9개의 데이터 포인트를 기반으로 하므로 현재 데이터 세트($\bar{V}/q \in [60, 75]$ kcal/mol/e)를 벗어나는 IPI 값에 대해서는 편차가 있을 수 있습니다. 더 많은 시스템, 특히 더 넓은 범위의 IPI 값을 가진 시스템을 고려한다면 예측의 신뢰성이 향상될 것입니다. 이는 잠재적으로 가스 분리를 위한 효과적인 IL 흡수제를 사전 선별하기 위한 간단하고 효율적인 지도로 이어질 수 있습니다.

**용해도 벤치마킹 및 예측.** 여기서 우리는 FFV-용해도 상평형 그림(**Figure 7**)의 잠재적 응용을 테스트하여 일반적으로 사용되는 일가 IL의 CO$_2$ 흡수 특성을 정량화합니다. 예를 들어, $1 \le n \le 8$인 [C$_n$mim]$^+$ 양이온(IPI > 70 kcal/mol/e)은 C1 기반 IL과 유사한 "더 작은 FFV" 시스템으로 취급될 수 있습니다. 따라서 CO$_2$ 용해도는 자유 부피 효과에 의해 지배되어야 합니다. $n > 8$인 경우(IPI < 70 kcal/mol/e), 양이온은 C2 및 C3 기반 IL과 유사한 "더 큰 FFV" 그룹으로 취급될 수 있습니다. 따라서 용해도는 음이온 효과에 의해 결정되어야 합니다. CO$_2$ 흡수에 일반적으로 사용되는 일가 음이온의 경우 IPI 값은 58 kcal/mol/e보다 크므로, $1 \le n \le 8$일 때 [C$_n$mim]$^+$ 기반 IL과 유사하게 CO$_2$ 용해도 또한 자유 부피 효과에 의해 지배됩니다.

참고로 Brennecke 등$^{59}$은 [Tf$_2$N] 기반 이미다졸륨 IL과 [C$_4$mim] 기반 IL에서 25 °C 고압에서의 CO$_2$ 실험적 몰 용해도를 비교했습니다. 동일한 음이온 기반 IL에 대한 CO$_2$ 용해도는 [C$_6$mmim]$^+$ (2,3-dimethyl-1-hexylimidazolium) < [C$_4$mim]$^+$ < [C$_6$mim]$^+$ < [C$_8$mim]$^+$ 순서로 증가한 반면, 동일한 양이온 기반 IL에 대한 CO$_2$ 용해도는 [NO$_3$]$^-$ (nitrate) < [DCA]$^-$ (dicyanamide) < [BF$_4$]$^-$ < [PF$_6$]$^-$ < [OTf]$^-$ (trifluoromethanesulfonate) < [Tf$_2$N]$^-$ < [methide] (tris-(trifluoromethylsulfonyl)-methide) 순서로 증가했습니다. 이에 비해 우리는 이러한 IL의 CO$_2$ 몰 분율 용해도를 양이온/음이온 IPI와 연관시키며(**Figure 8a,b**), 해당 데이터는 **Table S4**에 제공됩니다. 양이온/음이온 IPI와 몰 CO$_2$ 흡수 용량의 플롯은 부피 용해도가 몰 용해도와 강한 양의 상관관계가 있기 때문에(적어도 작은 IL에 대한 일관된 양이온 계열 내에서; 참조로 **Figure S6** 참조) 양이온/음이온 IPI가 이 경우 효과적일 수 있음을 나타냅니다. CO$_2$ 용해도는 [Tf$_2$N] 기반 또는 [C$_4$mim] 기반 IL에서 각각 분자 부피 증가 또는 양이온/음이온 IPI 감소에 따라 증가합니다.

우리는 또한 Brennecke 등$^{60}$이 보고한 불소 기능화된 양이온/음이온 내의 CO$_2$ 용해도를 조사합니다. 동일한 음이온 기반 IL에 대한 CO$_2$ 용해도는 [C$_8$H$_4$F$_{13}$mim]$^+$ (1-methyl-3-(tridecafluorooctyl)-imidazolium) > [C$_6$H$_4$F$_9$mim]$^+$ (1-methyl-3-(nonafluorohexyl)imidazolium) > [Et$_3$NBH$_2$mim]$^+$ (1-methylimidazole)(triethylamine)boronium > [C$_6$mim]$^+$ > [C$_6$mpy]$^+$ (1-hexyl-3-methylpyridinium) 순서로 감소한 반면, [C$_6$mim] 기반 IL에 대한 CO$_2$ 용해도는 [pFAP]$^-$ (tris-(heptafluoropropyl)trifluoro-phosphate) > [eFAP]$^-$ (tris-(pentafluoroethyl)trifluoro-phosphate) > [Tf$_2$N]$^-$ 순서로 감소했습니다. 용해도 대 IPI의 플롯은 **Figure 8c,d**에 나와 있습니다. 이전 관찰과 유사하게, 몰 CO$_2$ 용해도는 일반적으로 [Tf$_2$N] 기반 기능화된 IL 및 불소 기능화된 [C$_6$mim] 기반 IL에 대해 양이온 IPI 및 음이온 IPI가 감소함에 따라 증가합니다. 이러한 IL 쌍은 "더 작은 FFV" 시스템으로 간주되므로, 동일한 음이온/양이온 기반 IL에 대해 이온 부피가 증가하거나 IPI가 감소함에 따라 CO$_2$ 용해도가 증가합니다.

동일한 양이온 기반 IL의 IPI와 몰 용해도의 상관관계가 동일한 음이온 기반 IL의 상관관계보다 낫다는 것은 분명합니다. 대부분의 경우 양이온은 음이온보다 부피가 크므로, 음이온 유형에 비해 양이온 유형을 변경할 때 부피 용해도에 더 큰 영향을 미칩니다.

일반적으로 사용되는 음이온 또는 양이온의 경우 이온 크기가 상대적으로 작습니다. 따라서 CO$_2$ 용해도는 음이온이나 양이온의 극성이 아니라 자유 부피 효과에 의해 결정되는 경우가 가장 많습니다. 긴 알킬 사슬 길이 이미다졸륨([C$_{12}$mim]) 기반 IL 내의 CO$_2$ 용해도는 Dai 등$^{61}$에 의해 고압에서 $T = 333.15$ K에서 측정되었습니다. **Figure 9**는...

![Figure 9](Figure9_placeholder)
> **Figure 9.** Dai 등$^{61}$의 연구에서 가져온 $T = 298$ K에서의 [C$_{12}$mim] 기반 IL의 실험적 CO$_2$ 용해도(COSMO-RS 예측 몰 부피를 사용하여 실험적 몰 용해도에서 변환됨)와 음이온 IPI의 비교. 점선은 눈을 위한 가이드입니다.

...CO$_2$ 부피 용해도(COSMO-RS 모델$^{62,63}$에 기반한 298.15 K에서의 IL 쌍의 몰 부피를 사용하여 추정됨)에 대한 음이온 IPI의 플롯입니다; 실험적 몰 용해도는 **Table S6**에 나열되어 있습니다. 참조로 1 대 10 bar에서 Brennecke 그룹$^{59}$의 IL 쌍의 실험적으로 측정된 몰 부피 간의 비교가 **Figure S6b**에 나와 있습니다. 압력에 대해 작은 차이만 관찰되므로 단순화를 위해 IL 쌍의 몰 부피는 온도나 압력의 변화에 불변한다고 가정합니다. 몰 용해도(**Table S6**)는 "작은 FFV" 시스템(예: [C$_4$mim]- 및 [C$_6$mim] 기반 IL)과 유사성을 보여줍니다. 부피 용해도와의 관계는 반대 경향을 나타냅니다. 이는 증가하는 몰 부피에 기인하며, 이는 증가하는 용해도를 능가하고, 이 관찰은 우리가 제안한 FFV-용해도 상평형 그림에 의해 정확하게 예측됩니다.

더 높은 CO$_2$ 용해도를 위해 동일한 음이온 기반 IL을 사전 선별하려면 음이온 FFV-용해도 상평형 그림을 사용해야 합니다. 예를 들어, [Cl]$^-$에 대한 IPI는 138 kcal/mol/e (>58 kcal/mol/e)이므로 이와 짝을 이룰 더 낮은 양이온 IPI를 찾아야 합니다. 계산된 다가 및 일가 양이온 데이터 세트를 B3LYP-D3/6-311 + g(d,p) 방법과 결합하면 최적의 IL 쌍은 C3Cl$_3$이어야 합니다. 예측된 값은 파라미터화된 IPI 범위인 60-75 kcal/mol/e를 훨씬 벗어나지만(식 8 및 9를 통한 $S_{\text{CO}_2}$에 대한 비정상적인 결과로 이어짐), 지침은 여전히 C3Cl$_3$ IL이 다른 [Cl]$^-$ 기반 IL인 [C$_n$mim] ($n = 1-12$) 및 C1-C3보다 더 높은 CO$_2$ 용해도를 가져야 함을 시사합니다. 따라서 우리는 또한 GCMC...

<!-- Page 10 -->

...시뮬레이션을 실행하여 CO$_2$ 용해도를 직접 평가했으며, $S_{\text{CO}_2}[\text{g/L}] = 30.8$을 얻었습니다. 이는 원래 IL 그룹 내에서 가장 높은 용해도를 약간 초과합니다. 일반적으로 [Cl]$^-$ 기반 IL의 CO$_2$ 용해도를 개선하려면 알킬 사슬 길이를 늘리거나 양이온 전하를 늘려야 합니다.

또한 최근 논문$^{34}$에서 연구된 이온을 고려하면, trihexyl-tetradecyl-phosphonium [P$_{66614}$]$^+$ 양이온은 가장 큰 부피(778 Å$^3$)와 함께 가장 낮은 양이온 IPI(52 kcal/mol/e)를 갖습니다. 이 양이온은 [Cl]$^-$ 기반 IL 중에서 가장 높은 CO$_2$ 흡수를 가질 것으로 예측됩니다. 그런 다음 FFV-용해도 상평형 그림의 영역 7에 따라 최적의 음이온 쌍을 위해 [P$_{66614}$]$^+$ 양이온을 스크리닝하면 [Cl]$^-$ 음이온이 여전히 최선의 선택입니다. 이에 비해 [P$_{66614}$]$^+$ 기반 IL의 CO$_2$ 흡수에 대한 이전 실험 연구는 [P$_{66614}$] (pyrazole) [Pyr]에서 등몰(equimolar) CO$_2$ 용해도를 보여주었으며, 이는 85 g/L에 해당합니다(DFT 계산 vdW 부피 기준).$^{64}$ 그러나 [P$_{66614}$][Pyr] IL은 화학 흡착 메커니즘을 통해 CO$_2$와 상호 작용하며, 이는 우리 연구 범위(즉, 물리흡착 현상)를 벗어납니다.

## ■ 결론 (CONCLUSIONS)

우리는 동일한 음이온 또는 양이온 기반 IL에 대한 CO$_2$ 용해도 상평형 그림을 기반으로 IL 쌍을 사전 선별하기 위한 간단한 전략을 제안합니다. 효과적인 CO$_2$ 용매를 식별하기 위한 우리의 설계 프레임워크는 다가 IL뿐만 아니라 [C$_n$mim]$^+$, [BF$_4$]$^-$, [Br]$^-$, [CCN$_3$]$^-$, [Cl]$^-$, [OAc]$^-$, [PF$_6$]$^-$, [Tf$_2$N]$^-$와 같은 더 일반적인 일가 이온으로 구성된 IL과도 관련이 있습니다. 더 작은 일가 반대 이온과 짝을 이룬 큰 부피를 가진 다가 음이온 또는 양이온은 CO$_2$ 흡수에 더 나은 용매가 될 것으로 예상됩니다. 이와 함께 더 큰 음이온은 IL의 녹는점을 낮출 수 있으며, 이는 일반적으로 산업 응용 분야에 유익합니다.$^{65}$ 여기서 제안된 용해도 상평형 그림은 다른 기체 흡착제를 위한 IL 설계를 안내하는 데에도 유용할 수 있습니다.

## ■ 관련 콘텐츠 (ASSOCIATED CONTENT)

**Supporting Information**
지원 정보는 https://pubs.acs.org/doi/10.1021/acs.jpcb.1c01508 에서 무료로 이용할 수 있습니다.

*   일반적으로 사용되는 양이온 및 음이온에 의한 CO$_2$ 흡수; CO$_2$와 결합하기 전후의 다가/일가 양이온 및 음이온의 ESP 분포; COSMO-RS 및 MD/GCMC 시뮬레이션에 의해 예측된 CO$_2$ 용해도 비교; CO$_2$ 용해도와 IPI의 상관관계; 음이온 IPI와 실험적으로 측정된 흡수의 용해도 벤치마크 (Figures S1−S6, Tables S1−S6) (PDF)

## ■ 저자 정보 (AUTHOR INFORMATION)

**교신 저자 (Corresponding Author)**
**C. Heath Turner** − Department of Chemical and Biological Engineering, The University of Alabama, Tuscaloosa, Alabama 35487, United States; orcid.org/0000-0002-5707-9480; Phone: 205-348-1733; Email: hturner@eng.ua.edu

**저자 (Authors)**
**Xiaoyang Liu** − Department of Chemical and Biological Engineering, The University of Alabama, Tuscaloosa, Alabama 35487, United States; orcid.org/0000-0002-8172-6756
**Kathryn E. O’Harra** − Department of Chemical and Biological Engineering, The University of Alabama, Tuscaloosa, Alabama 35487, United States
**Jason E. Bara** − Department of Chemical and Biological Engineering, The University of Alabama, Tuscaloosa, Alabama 35487, United States; orcid.org/0000-0002-8351-2145

전체 연락처 정보는 다음에서 확인할 수 있습니다: https://pubs.acs.org/10.1021/acs.jpcb.1c01508

**참고 (Notes)**
저자들은 경쟁하는 재정적 이익이 없음을 선언합니다.

## ■ 감사의 말 (ACKNOWLEDGMENTS)

이 연구에 대한 지원은 국립과학재단(National Science Foundation, CBET-1605411)과 미국 에너지부(U.S. Department of Energy), 과학국(Office of Science), 기초 에너지 과학국(Office of Basic Energy Sciences), 분리 과학 프로그램(Separation Science program, Award Number DE-SC0018181)에서 제공했습니다. 컴퓨터 자원은 앨라배마 슈퍼컴퓨터 센터(Alabama Supercomputer Center)에서 제공했습니다.

## ■ 참고문헌 (REFERENCES)

(1) Zeng, S.; Zhang, X.; Bai, L.; Zhang, X.; Wang, H.; Wang, J.; Bao, D.; Li, M.; Liu, X.; Zhang, S. Ionic-Liquid-Based CO$_2$ Capture Systems: Structure, Interaction and Process. *Chem. Rev.* **2017**, *117*, 9625−9673.
(2) Lei, Z.; Dai, C.; Chen, B. Gas Solubility in Ionic Liquids. *Chem. Rev.* **2013**, *114*, 1289−1326.
(3) Zhang, X.; Zhang, X.; Dong, H.; Zhao, Z.; Zhang, S.; Huang, Y. Carbon Capture with Ionic Liquids: Overview and Progress. *Energy Environ. Sci.* **2012**, *5*, 6668−6681.
(4) Gupta, K. M.; Chen, Y.; Hu, Z.; Jiang, J. Metal−Organic Framework Supported Ionic Liquid Membranes for CO$_2$ Capture: Anion Effects. *Phys. Chem. Chem. Phys.* **2012**, *14*, 5785−5794.
(5) Gouveia, A. S. L.; Tomé, L. C.; Lozinskaya, E. I.; Shaplov, A. S.; Vygodskii, Y. S.; Marrucho, I. M. Exploring the Effect of Fluorinated Anions on the CO$_2$/N$_2$ Separation of Supported Ionic Liquid Membranes. *Phys. Chem. Chem. Phys.* **2017**, *19*, 28876−28884.
(6) Samadi, A.; Kemmerlin, R. K.; Husson, S. M. Polymerized Ionic Liquid Sorbents for CO$_2$ Separation. *Energy Fuels* **2010**, *24*, 5797−5804.
(7) Abedini, A.; Crabtree, E.; Bara, J. E.; Turner, C. H. Molecular Simulation of Ionic Polyimides and Composites with Ionic Liquids as Gas-Separation Membranes. *Langmuir* **2017**, *33*, 11377−11389.
(8) Abedini, A.; Crabtree, E.; Bara, J. E.; Turner, C. H. Molecular Analysis of Selective Gas Adsorption within Composites of Ionic Polyimides and Ionic Liquids as Gas Separation Membranes. *Chem. Phys.* **2019**, *516*, 71−83.
(9) Szala-Bilnik, J.; Abedini, A.; Crabtree, E.; Bara, J. E.; Turner, C. H. Molecular Transport Behavior of CO$_2$ in Ionic Polyimides and Ionic Liquid Composite Membrane Materials. *J. Phys. Chem. B.* **2019**, *123*, 7455−7463.
(10) Szala-Bilnik, J.; Crabtree, E.; Abedini, A.; Bara, J. E.; Turner, C. H. Solubility and Diffusivity of CO$_2$ in Ionic Polyimides with [C(CN)$_3$]$_x$[oAc]$_{1-x}$ Anion Composition. *Comput. Mater. Sci.* **2020**, *174*, 109468.
(11) Jenkins, H. D. B.; Roobottom, H. K.; Passmore, J.; Glasser, L. Relationships among Ionic Lattice Energies, Molecular (Formula Unit) Volumes, and Thermochemical Radii. *Inorg. Chem.* **1999**, *38*, 3609−3620.
(12) Jenkins, H. D. B.; Tudela, D.; Glasser, L. Lattice Potential Energy Estimation for Complex Ionic Salts from Density Measurements. *Inorg. Chem.* **2002**, *41*, 2364−2367.
(13) Glasser, L.; Jenkins, H. D. B. Volume-Based Thermodynamics: A Prescription for Its Application and Usage in Approximation and Prediction of Thermodynamic Data. *J. Chem. Eng. Data* **2011**, *56*, 874−880.

<!-- Page 11 -->

(14) Klamt, A. The COSMO and COSMO-RS solvation models. *Wiley Interdiscip. Rev.: Comput. Mol. Sci.* **2011**, *1*, 699−709.
(15) Klamt, A.; Eckert, F.; Arlt, W. COSMO-RS: An Alternative to Simulation for Calculating Thermodynamic Properties of Liquid Mixtures. *Annu. Rev. Chem. Biomol. Eng.* **2010**, *1*, 101−122.
(16) Turner, E. A.; Pye, C. C.; Singer, R. D. Use of ab Initio Calculations toward the Rational Design of Room Temperature Ionic Liquids. *J. Phys. Chem. A* **2003**, *107*, 2277−2288.
(17) Izgorodina, E. I.; Golze, D.; Maganti, R.; Armel, V.; Taige, M.; Schubert, T. J. S.; MacFarlane, D. R. Importance of Dispersion Forces for Prediction of Thermodynamic and Transport Properties of Some Common Ionic Liquids. *Phys. Chem. Chem. Phys.* **2014**, *16*, 7209−7221.
(18) Izgorodina, E. I.; Seeger, Z. L.; Scarborough, D. L. A.; Tan, S. Y. S. Quantum Chemical Methods for the Prediction of Energetic, Physical, and Spectroscopic Properties of Ionic Liquids. *Chem. Rev.* **2017**, *117*, 6696−6754.
(19) Kato, R.; Gmehling, J. Systems with Ionic Liquids: Measurement of VLE and $\gamma^\infty$ Data and Prediction of Their Thermodynamic Behavior Using Original UNIFAC, Mod. UNIFAC (Do) and COSMO-RS (Ol). *J. Chem. Thermodyn.* **2005**, *37*, 603−619.
(20) Lin, S.-T.; Sandler, S. I. A Priori Phase Equilibrium Prediction from a Segment Contribution Solvation Model. *Ind. Eng. Chem. Res.* **2002**, *41*, 899−913.
(21) Camper, D.; Scovazzo, P.; Koval, C.; Noble, R. Gas Solubilities in Room-Temperature Ionic Liquids. *Ind. Eng. Chem. Res.* **2004**, *43*, 3049−3054.
(22) Scovazzo, P.; Camper, D.; Kieft, J.; Poshusta, J.; Koval, C.; Noble, R. Regular Solution Theory and CO$_2$ Gas Solubility in Room-Temperature Ionic Liquids. *Ind. Eng. Chem. Res.* **2004**, *43*, 6855−6860.
(23) You, S.-S.; Yoo, K.-P.; Lee, C. S. An Approximate Nonrandom Lattice Theory of Fluids: General Derivation and Application to Pure Fluids. *Fluid Phase Equilib.* **1994**, *93*, 193−213.
(24) You, S.-S.; Yoo, K.-P.; Soo Lee, C. An Approximate Nonrandom Lattice Theory of Fluids: Mixtures. *Fluid Phase Equilib.* **1994**, *93*, 215−232.
(25) Breure, B.; Bottini, S. B.; Witkamp, G.-J.; Peters, C. J. Thermodynamic Modeling of the Phase Behavior of Binary Systems of Ionic Liquids and Carbon Dioxide with the Group Contribution Equation of State. *J. Phys. Chem. B* **2007**, *111*, 14265−14270.
(26) Karakatsani, E. K.; Economou, I. G.; Kroon, M. C.; Peters, C. J.; Witkamp, G.-J. tPC-PSAFT Modeling of Gas Solubility in Imidazolium-Based Ionic Liquids. *J. Phys. Chem. C* **2007**, *111*, 15487−15492.
(27) Zhang, X.; Liu, Z.; Wang, W. Screening of Ionic Liquids to Capture CO$_2$ by COSMO-RS and Experiments. *AIChE J.* **2008**, *54*, 2717−2728.
(28) Palomar, J.; Gonzalez-Miquel, M.; Polo, A.; Rodriguez, F. Understanding the Physical Absorption of CO$_2$ in Ionic Liquids Using the COSMO-RS Method. *Ind. Eng. Chem. Res.* **2011**, *50*, 3452−3463.
(29) Manan, N. A.; Hardacre, C.; Jacquemin, J.; Rooney, D. W.; Youngs, T. G. A. Evaluation of Gas Solubility Prediction in Ionic Liquids using COSMOthermX. *J. Chem. Eng. Data* **2009**, *54*, 2005−2022.
(30) Liu, X.; O’Harra, K. E.; Bara, J. E.; Turner, C. H. Molecular Insight into the Anion Effect and Free Volume Effect of CO$_2$ Solubility in Multivalent Ionic Liquids. *Phys. Chem. Chem. Phys.* **2020**, *22*, 20618−20633.
(31) Gadre, S. R.; Shirsat, R. N., *Electrostatics of Atoms and Molecules*; Universities Press: 2000.
(32) Politzer, P.; Truhlar, D. G., *Chemical Applications of Atomic and Molecular Electrostatic Potentials: Reactivity, Structure, Scattering, and Energetics of Organic, Inorganic, and Biological Systems*; Springer Science & Business Media: 2013.
(33) Liu, H.; Zhang, Z.; Bara, J. E.; Turner, C. H. Electrostatic Potential within the Free Volume Space of Imidazole-Based Solvents: Insights into Gas Absorption Selectivity. *J. Phys. Chem. B.* **2013**, *118*, 255−264.
(34) Liu, X.; O’Harra, K. E.; Bara, J. E.; Turner, C. H. Screening Ionic Liquids Based on Ionic Volume and Electrostatic Potential Analyses. *J. Phys. Chem. B* **2021**, DOI: 10.1021/acs.jpcb.0c10259.
(35) Brandenburg, J. G.; Bannwarth, C.; Hansen, A.; Grimme, S. B97-3c: A Revised Low-Cost Variant of the B97-D Density Functional Method. *J. Chem. Phys.* **2018**, *148*, No. 064104.
(36) Lu, T.; Chen, F. Multiwfn: A Multifunctional Wavefunction Analyzer. *J. Comput. Chem.* **2012**, *33*, 580−592.
(37) Lu, T.; Chen, F. Quantitative Analysis of Molecular Surface Based on Improved Marching Tetrahedra Algorithm. *J. Mol. Graphics Modell.* **2012**, *38*, 314−323.
(38) Lu, T.; Manzetti, S. Wavefunction and Reactivity Study of Benzo[a]pyrene Diol Epoxide and Its Enantiomeric Forms. *Struct. Chem.* **2014**, *25*, 1521−1533.
(39) Lee, C.; Yang, W.; Parr, R. G. Development of the Colle-Salvetti Correlation-Energy Formula into A Functional of the Electron Density. *Phys. Rev. B* **1988**, *37*, 785.
(40) Becke, A. D. A New Mixing of Hartree−Fock and Local Density-Functional Theories. *J. Chem. Phys.* **1993**, *98*, 1372−1377.
(41) Grimme, S.; Antony, J.; Ehrlich, S.; Krieg, H. A Consistent and Accurate ab initio Parametrization of Density Functional Dispersion Correction (DFT-D) for the 94 Elements H-Pu. *J. Chem. Phys.* **2010**, *132*, 154104.
(42) Frisch, M.; Trucks, G.; Schlegel, H. B.; Scuseria, G. E.; Robb, M. A.; Cheeseman, J. R.; Scalmani, G.; Barone, V.; Mennucci, B.; Petersson, G., et al., *Gaussian 09, Revision D. 01*; Gaussian. Inc.: Wallingford CT 2009.
(43) Boys, S. F.; Bernardi, F. The Calculation of Small Molecular Interactions by the Differences of Separate Total Energies. Some Procedures with Reduced Errors. *Mol. Phys.* **2006**, *19*, 553−566.
(44) Lao, K. U.; Herbert, J. M. Breakdown of the Single-Exchange Approximation in Third-Order Symmetry-Adapted Perturbation Theory. *J. Phys. Chem. A* **2011**, *116*, 3042−3047.
(45) Parker, T. M.; Burns, L. A.; Parrish, R. M.; Ryno, A. G.; Sherrill, C. D. Levels of Symmetry Adapted Perturbation Theory (SAPT). I. Efficiency and Performance for Interaction Energies. *J. Chem. Phys.* **2014**, *140*, No. 094106.
(46) Parrish, R. M.; Burns, L. A.; Smith, D. G. A.; Simmonett, A. C.; DePrince, A. E., III; Hohenstein, E. G.; Bozkaya, U.; Sokolov, A. Y.; di Remigio, R.; Richard, R. M.; Gonthier, J. F.; James, A. M.; McAlexander, H. R.; Kumar, A.; Saitow, M.; Wang, X.; Pritchard, B. P.; Verma, P.; Schaefer, H. F., III; Patkowski, K.; King, R. A.; Valeev, E. F.; Evangelista, F. A.; Turney, J. M.; Crawford, T. D.; Sherrill, C. D. Psi4 1.1: An Open-Source Electronic Structure Program Emphasizing Automation, Advanced Libraries, and Interoperability. *J. Chem. Theory Comput.* **2017**, *13*, 3185−3197.
(47) Gurau, G.; Rodríguez, H.; Kelley, S. P.; Janiczek, P.; Kalb, R. S.; Rogers, R. D. Demonstration of Chemisorption of Carbon Dioxide in 1,3-Dialkylimidazolium Acetate Ionic Liquids. *Angew. Chem., Int. Ed.* **2011**, *50*, 12024−12026.
(48) Kelemen, Z.; Péter-Szabó, B.; Székely, E.; Hollóczki, O.; Firaha, D. S.; Kirchner, B.; Nagy, J.; Nyulászi, L. An Abnormal N-Heterocyclic Carbene−Carbon Dioxide Adduct from Imidazolium Acetate Ionic Liquids: The Importance of Basicity. *Chem. - Eur. J.* **2014**, *20*, 13002−13008.
(49) Zhao, Y.; Pan, M.; Kang, X.; Tu, W.; Gao, H.; Zhang, X. Gas Separation by Ionic Liquids: A Theoretical Study. *Chem. Eng. Sci.* **2018**, *189*, 43−55.
(50) Feng, G.; Chen, M.; Bi, S.; Goodwin, Z. A. H.; Postnikov, E. B.; Brilliantov, N.; Urbakh, M.; Kornyshev, A. A. Free and Bound States of Ions in Ionic Liquids, Conductivity, and Underscreening Paradox. *Phys. Rev. X* **2019**, *9*, No. 021024.
(51) Lee, W. M. Selection of Barrier Materials from Molecular Structure. *Polym. Eng. Sci.* **1980**, *20*, 65−69.
(52) Bondi, A. A., *Physical Properties of Molecular Crystals Liquids, and Glasses*; Wiley: New York: 1968.
(53) Horn, N. R. A Critical Review of Free Volume and Occupied Volume Calculation Methods. *J. Membr. Sci.* **2016**, *518*, 289−294.
(54) Shannon, M. S.; Tedstone, J. M.; Danielsen, S. P. O.; Hindman, M. S.; Irvin, A. C.; Bara, J. E. Free Volume as the Basis of Gas Solubility and Selectivity in Imidazolium-Based Ionic Liquids. *Ind. Eng. Chem. Res.* **2012**, *51*, 5565−5576.

<!-- Page 12 -->

(55) Zhu, P.; Kang, X.; Latif, U.; Gong, M.; Zhao, Y. A Reliable Database for Ionic Volume and Surface: Its Application To Predict Molar Volume and Density of Ionic Liquid. *Ind. Eng. Chem. Res.* **2019**, *58*, 10073−10083.
(56) Robertson, M. J.; Tirado-Rives, J.; Jorgensen, W. L. Improved Peptide and Protein Torsional Energetics with the OPLS-AA Force Field. *J. Chem. Theory Comput.* **2015**, *11*, 3499−3509.
(57) Lourenço, T. C.; Coelho, M. F. C.; Ramalho, T. C.; van der Spoel, D.; Costa, L. T. Insights on the Solubility of CO$_2$ in 1-Ethyl-3-methylimidazolium Bis(trifluoromethylsulfonyl)imide from the Microscopic Point of View. *Environ. Sci. Technol.* **2013**, *47*, 7421−7429.
(58) Bondi, A. van der Waals Volumes and Radii. *J. Phys. Chem.* **1964**, *68*, 441−451.
(59) Aki, S. N. V. K.; Mellein, B. R.; Saurer, E. M.; Brennecke, J. F. High-Pressure Phase Behavior of Carbon Dioxide with Imidazolium-Based Ionic Liquids. *J. Phys. Chem. B* **2004**, *108*, 20355−20365.
(60) Muldoon, M. J.; Aki, S. N. V. K.; Anderson, J. L.; Dixon, J. K.; Brennecke, J. F. Improving Carbon Dioxide Solubility in Ionic Liquids. *J. Phys. Chem. B* **2007**, *111*, 9001−9009.
(61) Dai, C.; Lei, Z.; Chen, B. Gas Solubility in Long-Chain Imidazolium-Based Ionic Liquids. *AIChE J.* **2017**, *63*, 1792−1798.
(62) Diedenhofen, M.; Klamt, A. COSMO-RS as A Tool for Property Prediction of IL Mixtures—A Review. *Fluid Phase Equilib.* **2010**, *294*, 31−38.
(63) Palomar, J.; Ferro, V. R.; Torrecilla, J. S.; Rodríguez, F. Density and Molar Volume Predictions Using COSMO-RS for Ionic Liquids. An Approach to Solvent Design. *Ind. Eng. Chem. Res.* **2007**, *46*, 6041−6048.
(64) Wang, C.; Luo, X.; Luo, H.; Jiang, D. E.; Li, H.; Dai, S. Tuning the Basicity of Ionic Liquids for Equimolar CO$_2$ Capture. *Angew. Chem., Int. Ed.* **2011**, *50*, 4918−4922.
(65) Nelyubina, Y. V.; Shaplov, A. S.; Lozinskaya, E. I.; Buzin, M. I.; Vygodskii, Y. S. A New Volume-Based Approach for Predicting Thermophysical Behavior of Ionic Liquids and Ionic Liquid Crystals. *J. Am. Chem. Soc.* **2016**, *138*, 10076−10079.
