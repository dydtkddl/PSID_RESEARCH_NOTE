---
date: "2024-10-24"
paper_title: "Simulating the ionic liquid mixing with organic-solvent clarifies the mixture’s SFG spectral behavior and the specific surface region originating SFG"
short_title: "이온성 액체와 유기 용매 혼합물의 SFG 스펙트럼 거동 및 표면 기원 영역 시뮬레이션"
authors: "Leila Sakhtemanian, Anjeeta Duwadi, Steven Baldelli & Mohammad Hadi Ghatee"
journal: "Scientific Reports"
year: 2024
status: "translated"
tags: [Molecular dynamics, Ionic liquids, Benzonitrile, SFG spectroscopy, Surface structure]
category: "Research"
summary: "이온성 액체 [C4mim][PF6]와 벤조니트릴(BZN) 혼합물의 분자 동역학 시뮬레이션을 통해 구조적·동적 특성을 규명하고, BZN이 양이온의 부틸 꼬리에 적층되는 현상이 실험적 SFG 스펙트럼 변화의 원인임을 밝혀냈다. 특히 시뮬레이션 결과는 표면에 노출된 분자 부분만이 SFG 신호를 생성하며, 하부 표면(subsurface)은 기여하지 않음을 입증하여 기존의 모호성을 해소했다."
file_ref: "Scientific Reports_2024_Simulating the ionic liquid mixing.pdf"
---

<!-- Page 1 -->
# 유기 용매와의 이온성 액체 혼합 시뮬레이션을 통한 혼합물의 SFG 스펙트럼 거동 및 SFG 발생 특정 표면 영역 규명

**Leila Sakhtemanian$^1$, Anjeeta Duwadi$^2$, Steven Baldelli$^2$ & Mohammad Hadi Ghatee$^{1\bowtie}$**

극성 벤조니트릴(benzonitrile, BNZ) 용매와 혼합된 친환경 이온성 액체(ionic liquid) $[C_4mim][PF_6]$의 분자 동역학(MD) 시뮬레이션은 전기화학 및 재료 과학 응용에 필수적인 구조적 및 동적 특성에 대한 상세한 통찰력을 제공합니다. 다양한 몰 분율($X_{BZN}$)에서 수행된 시뮬레이션은 반경(radial), 공간(spatial) 및 결합 분포 함수(combined distribution functions)를 통해 혼합물의 물리적, 구조적, 동적 특성을 밝혀내며, 수소 결합을 통한 효과적인 상호작용을 강조합니다. 시뮬레이션 결과, BZN이 양이온의 부틸 꼬리(butyl tail)에 적층(stacking)된다는 사실이 밝혀졌으며, 이는 독특한 실험적 관찰 결과(후술함)에 대한 중요한 설명을 제공합니다. BZN을 첨가하면 혼합물의 액체 동역학(liquid dynamics)은 낮은 $X_{BZN}$에서는 선형적으로, 높은 $X_{BZN}$에서는 기하급수적으로 증가하며, $0.5X_{BZN}$에서 주목할 만한 특이 전이(singular transition)가 나타납니다. 혼합물의 표면 구조를 시뮬레이션하여 실험적 합 주파수 생성(SFG) 분광학 결과를 검증하고 뒷받침하기 위한 포괄적인 노력이 이루어졌습니다. 결과적으로, 시뮬레이션된 BZN 적층 구조는 (1) $X_{BZN} < 0.8$에서 SFG 스펙트럼 내 $C \equiv N$ 진동 모드의 부재, (2) $X_{BZN}$이 0.5에 접근함에 따라 사라지는 $CH_3$ SFG 신호의 점진적인 감소를 설명합니다. 마지막으로, 본 연구는 표면에 있는 분자 부분(moieties)만이 SFG 진동 신호를 생성하고 하부 표면(subsurface)에 있는 부분은 생성하지 않는다는 것을 증명함으로써 지속적인 모호성을 제거했습니다.

**Keywords:** 이성분 혼합물(Binary mixture), 농도 의존성(Concentration-dependence), 동적 특성(Dynamic properties), MD 시뮬레이션(MD simulation), SFG 기원 영역(SFG origination region), 시너지 원리(Synergistic principle), 밀도 및 표면 장력(Density and surface tension), 확산 계수(Diffusion coefficients)

이온성 액체(ILs)의 조절 가능한 용해도는 낮은 증기압, 높은 열적 안정성, 낮은 녹는점과 같은 다른 특성들과 함께 IL을 독특한 종류의 용매로 만듭니다. IL의 가용화(solubilization) 능력은 양이온의 알킬 사슬 길이와 음이온의 종류에 따라 달라지며, 이를 통해 광범위한 유기 및 무기 물질을 용해할 수 있습니다. 또한, IL은 효율적으로 재사용할 수 있어 다양한 화학 반응에 매우 매력적입니다.

양이온과 음이온을 맞춤화함으로써 학계와 산업계 모두에서 가치 있는 특정 특성을 갖도록 IL을 설계할 수 있습니다$^{1,2}$. 예를 들어, 흔히 사용되는 이미다졸륨(imidazolium) 기반 이온성 액체는 두 개의 인접하지 않은 질소 원자를 가진 5원 방향족 고리 구조를 특징으로 하며, 이 질소 원자들은 다양한 길이의 알킬기를 가집니다. 대조적으로, 암모늄 및 포스포늄 기반 IL은 선형 알칸 사슬 구조의 양이온을 갖습니다$^3$. 이러한 예는 이온성 액체의 다양한 구조가 친수성 및 소수성 변형을 모두 생성할 수 있게 하여 용매화 특성, 가용화 영역 및 전해질의 안정성을 제어하는 데 중요함을 강조합니다.

IL과 유기 용매의 혼화성(miscibility)은 화학 합성, 촉매, 추출 및 전기화학 분야에서 수많은 응용 분야를 제공합니다. 또한, 이러한 이온성 액체가 혼합 용매를 형성하는 능력은 점도, 극성 및 전기 전도도와 같은 물리적 특성에 상당한 변화를 가져와 잠재적 응용 분야를 더욱 확장합니다. 혼합 용매는 순수 용매에서는 관찰되지 않는 독특하고 복잡한 거동을 나타낼 수 있습니다. 이러한 특성은 서로 다른 용매 분자와 용질 간의 상호 작용에서 비롯되며, 새로운 용매화 동역학, 열역학적 특성 및 화학적 반응성을 유도합니다. 이러한 거동을 이해하는 것은 화학 합성을 포함한 광범위한 응용 분야에 중요합니다.

$^1$Department of Chemistry, Shiraz University, 71946 Shiraz, Iran. $^2$Department of Chemistry, University of Houston, Houston, TX 77204-5003, USA. $^\bowtie$email: mhghatee@shirazu.ac.ir; mhghatee2@gmail.com

<!-- Page 2 -->
제약 제제, 환경 과학 및 재료 개발 등 다양한 분야에서 중요합니다. 또한, 가능한 용매 조합의 방대한 수와 다양한 조건은 탐구와 발견을 위한 풍부한 환경을 제공합니다.

다양한 음이온을 가진 1-alkyl-3-methylimidazolium과 같은 다양한 이미다졸륨 기반 IL에 대한 광범위한 실험 및 계산 연구는 수많은 응용 결과를 낳았습니다$^{4–15}$. 용매의 구조적 조사 또한 아세톤, 메탄올, 에탄올, 디클로로메탄과 같은 유기 용매에 초점을 맞추었습니다$^{16–18}$. 자연적으로 발생하는 물 용매와 혼합된 이온성 액체의 성능은 점도, 극성 및 전도도와 같은 조절 가능한 특성을 초래할 수 있습니다. 이러한 혼합물은 산업적 지속 가능성을 향상시킬 잠재력에 대해 연구되었으며 일반적으로 아세톤 냉각 응용 분야에 제안됩니다$^{19}$.

IL 특성을 조사하는 것 외에도, 우리 그룹의 최근 연구에는 순수 액체 BZN의 MD 시뮬레이션이 포함되어 있으며, 이는 중요한 구조적 정보를 산출했습니다$^{20}$. 용매로서 BZN에 대한 관심은 낮은 증기압, 높은 끓는점, 강한 극성에서 비롯되며, 이는 다양한 유기 및 생화학 물질에 다재다능하게 사용될 수 있게 합니다. 생명의 기원에서 BZN(최근 성간 공간에서 발견됨)의 가설적 역할은 단순한 용매 기능을 넘어 연구를 강화시켰습니다. 한편, 헥사플루오로포스페이트($[PF_6]^-$) 및 비스(트리플루오로메틸설포닐)이미드($[NTf_2]^-$) 음이온을 포함하는 IL은 상당히 더 넓은 산화 환원 안정성을 보여 전기화학적 응용에 적합합니다. 본 연구는 $[C_4mim][PF_6] + BZN$ 혼합물을 조사하여 이 두 용매 클래스의 분자 동역학을 검토하고 공용매(co-solvency) 개념을 확장합니다. 계산 및 실험 연구 모두 유사한 화합물을 탐구하여 벌크 및 계면에서 뚜렷한 미세상 분리(microphase segregation)를 밝혀냈습니다. 예를 들어, 아세토니트릴, 메탄올, 물과 같은 극성 용매뿐만 아니라 비극성 n-헥산을 $[C_4mim][PF_6]$에 용해시키는 연구가 수행되었습니다. 이러한 연구는 알칸이 비극성 도메인에 존재하는 반면, 아세토니트릴은 극성 및 비극성 도메인 모두에 대해 균형 잡힌 친화력을 나타냄을 보여줍니다. 메탄올은 음이온과 강한 수소 결합을 형성하고 양이온 헤드와는 약한 결합을 형성합니다$^{21,22}$. 특성에 따라 용질은 IL의 다른 영역과 우선적으로 상호 작용할 수 있습니다: (1) 비극성 도메인(예: 알칸), (2) 극성 네트워크(예: 회합성 물 유체), 또는 (3) 극성 및 비극성 영역 사이의 계면(아세토니트릴, 아세톤 또는 작은 할로겐화 탄화수소와 같은 쌍극자 용질이 점유)$^{23}$. 이 후자 그룹의 용매는 쌍극자를 배향하고 IL 음이온 및 양이온과 동시에 상호 작용하여 이온 용매화 붕괴를 촉진하는 능력 때문에 많은 이온성 액체에 특히 효과적입니다$^{23}$. 특히, 더 높은 쌍극자는 더 낮은 양이온-음이온 전하 이동과 상관관계가 있어 더 안정적인 전기화학적 특성을 유도하며, 이는 IL과 BZN 모두에 적용됩니다$^3$. 1-ethyl-3-methylimidazolium과 1-hexyl-3-methylimidazolium bis(trifluoromethane)sulfonimide($[C_2mim][NTf_2] + [C_6mim][NTf_2]$)의 등몰 혼합물 구조가 컴퓨터 시뮬레이션에 의해 조사되었습니다$^{24}$. 이러한 연구는 순수 성분에서 관찰되는 중간 구조와 유사한 극성 및 비극성 도메인 간의 미세상 분리를 밝혀냈습니다. 극성 도메인은 이온 채널 및 클러스터의 3차원 네트워크를 나타낸 반면, 비극성 도메인은 $[C_2mim][NTf_2]$에서는 분산되어 나타나고 $[C_6mim][NTf_2]$와 같이 더 긴 알킬 사슬에서는 연속적으로 나타났습니다$^{24}$. 최근 연구는 분야를 발전시키기 위해 다중 이온성 액체의 혼합물에 초점을 맞추고 있습니다$^{25–32}$. 또한, 물, 공용매 및 불순물을 포함한 다양한 첨가제가 이미다졸륨 기반 이온성 액체의 물리적 특성(예: 점도, 밀도, 표면 장력)에 미치는 영향은 잘 문서화되어 있습니다. 이러한 연구들은 순수 이온성 액체와 물$^{33–38}$, 벤젠$^{39}$, 아세토니트릴$^{40–42}$, 알코올$^{21,43,44}$과 같은 유기 화합물과의 혼합물에 대한 연구를 촉발했습니다.

광범위한 계산 및 실험 연구에도 불구하고, 유기 합성에 일반적으로 사용되는 이온성 액체와 벤조니트릴 간의 상호 작용에 대한 정보는 여전히 불충분합니다. 최근 $[C_4mim][PF_6]$와 BZN의 이성분 혼합물의 표면 구조가 합 주파수 생성(SFG) 진동 분광법과 표면 장력 측정을 사용하여 조사되었습니다$^{45}$. 이에 따르면 표면 구조는 조성과 온도에 따라 달라지며, 벤조니트릴이 이온성 액체의 표면 구조에 미치는 영향은 미미함을 나타냅니다. 이온성 액체의 SFG 스펙트럼은 벤조니트릴이 존재할 때 이미다졸륨 고리나 메틸렌 그룹에 해당하는 피크를 나타내지 않았습니다$^{45}$. 이러한 관찰은 BZN이 존재할 때 액체-증기 계면에서 $[C_4mim][PF_6]$의 고도로 회합된 이온 쌍(ion pairs)이 형성됨을 시사합니다.

반대로, 실험적 방법과 분자 동역학(MD) 시뮬레이션은 정제된 힘장(force field)을 사용하여 벤조니트릴과 유사한 아세토니트릴(ACN)과 혼합된 친수성 이온성 액체($[C_4mim][BF_4]$)를 조사하는 데 사용되었습니다$^{40–42}$. 낮은 몰 분율(예: $X_{IL} = 0.3$)에서 과잉 몰 부피의 최소값과 증가된 양이온-음이온 및 ACN-ACN 상호 작용이 관찰되었습니다$^{40}$. $X_{IL} \ge 0.5$의 경우, $[C_4mim][BF_4]+ACN$ 및 $[C_2mim][BF_4]+ACN$ 혼합물의 표면 연구는 벌크보다 표면에서 3배 더 높은 ACN 축적을 나타냈습니다. 낮은 $X_{IL}$을 가진 혼합물의 경우, ACN과 IL이 벌크 전체에 고르게 분산되어 더 높은 $X_{IL}$에 비해 덜 뚜렷한 액체-증기 분리를 초래합니다$^{41}$. ACN과 혼합된 소수성 IL $[C_5mim][NTf_2]$의 MD 시뮬레이션은 ACN과 양이온 헤드의 수소 원자 사이의 강한 상호 작용을 나타냈으며, ACN 분자는 이온 네트워크와 비극성 도메인 사이의 표면 영역에 우선적으로 위치했습니다$^{42}$. 또한, 두 가지 아졸(azole) 기반 이온성 액체와 메탄올, 에탄올, 부탄올, 이소프로판올과의 혼합물에 대해 298~313 K의 온도 범위에서 밀도 및 점도의 실험적 측정이 수행되었습니다$^{46}$.

이성분 액체 혼합물에 대한 관심을 감안하여, 우리는 다양한 비율에 걸쳐 MD 시뮬레이션을 사용하여 유기 용매 BZN과 친환경 용매 IL 1-butyl-3-methylimidazolium hexafluorophosphate($[C_4mim][PF_6]$)의 혼합 메커니즘을 조사했습니다. 우리는 실온에서 이러한 혼합물의 물리적, 구조적 및 동적 특성을 탐구했습니다. 시뮬레이션은 BZN으로 희석 시 IL 구조적 상관관계, 상대적 배향, 확산 및 표면 장력의 변화에 대한 통찰력을 제공했습니다. 표면 구조 시뮬레이션은 우리의 발견을 검증하기 위해 수행되었으며, 이는 최근의 실험적 SFG 진동 분광법 결과와 밀접하게 일치합니다$^{45}$. 이러한 시뮬레이션 조사는 SFG 스펙트럼의 해석을 뒷받침하고, 상세한 분자적 통찰력을 제공하며, 보완했습니다. SFG 스펙트럼을 검증하고 상세화하는 것 외에도, 시뮬레이션 결과는 증강된 주파수(augmented frequency) 빔이 독점적으로 생성되는 계면 영역을 식별했습니다.

<!-- Page 3 -->
### 계산 방법 (Computational method)

$[C_4mim][PF_6]$ IL과 벤조니트릴은 B3LYP 함수와 6-311++G(3df,3pd) 기저 집합(basis set)을 사용하여 Gaussian 09$^{47}$로 최적화되었습니다. 진동 주파수는 유효한 위치 에너지 표면(potential energy surface)을 보장했습니다. Gaussian 09의 CHELPG$^{48}$는 원자들의 부분 전하를 도출했습니다. 그림 1은 계산에 사용된 BZN, $[C_4mim][PF_6]$ 및 라벨링된 원자들을 보여줍니다.

모든 원자(All-atom) 고전적 MD 시뮬레이션은 OPLS-AA$^{50,51}$ 힘장(force field)과 함께 Gromacs (4.5.5)$^{49}$ 소프트웨어를 사용하여 수행되었습니다. 상호 작용 위치 에너지 함수는 분자 내 및 분자 간을 포함합니다:

$$ U = U_{stretch} + U_{bend} + U_{torsion} + U_{LJ} + U_{coulomb} \quad (1) $$

$$ U = \sum_{bond} k_r(r - r_{eq})^2 + \sum_{angle} k_\theta (\theta - \theta_{eq})^2 + \sum_{n=0}^{5} C_n (\cos(\phi))^n + U_{LJ} + U_{coulomb} \quad (2) $$

$$ U_{LJ} = \sum_{i=1}^{N-1} \sum_{j>1}^{N} \left\{ 4\epsilon_{ij} \left[ \left( \frac{\sigma_{ij}}{r_{ij}} \right)^{12} - \left( \frac{\sigma_{ij}}{r_{ij}} \right)^{6} \right] \right\} \quad (3) $$

$$ U_{Coulomb} = \frac{1}{4\pi \epsilon_0} \frac{q_i q_j}{r_{ij}} \quad (4) $$

여기서 모든 매개변수는 일반적인 의미를 갖습니다.

다양한 몰 분율($X_{BZN} = 0, 0.1, 0.3, 0.5, 0.7, 0.8, 0.9, 1$)을 가진 BZN과 $[C_4mim][PF_6]$의 혼합물이 선택되었습니다. 표 1은 각 혼합물에 대한 시뮬레이션 앙상블을 준비하는 데 사용된 $[C_4mim][PF_6]$ 이온 쌍과 BZN 분자의 양을 포함합니다. 모든 혼합물 내의 $BZN/[C_4mim][PF_6]$ 비율은 거의 동일한 원자 수와 최종 최적화된 슬래브 두께를 갖도록 조정되었습니다. 모든 혼합물을 시뮬레이션하기 위해 $80 \times 80 \times 250 (xyz) \mathring{A}^3$ 크기의 직사각형 상자가 사용되었습니다.

에너지 최소화는 최급강하법(steepest descent algorithm)$^{52}$을 사용하여 수행되었으며, 이후 0.001 ps의 시간 간격으로 0.5 ns 동안 등온-등압 앙상블(NPT)에서 시뮬레이션을 계속했습니다. 온도와 압력은

| $X_{BZN}$ | 분자 수 | | 원자 수 |
| :--- | :--- | :--- | :--- |
| | **$[C_4mim][PF_6]$** | **BZN** | **Total** |
| 0.0 | 1050 | 0 | 33,600 |
| 0.1 | 1000 | 112 | 33,456 |
| 0.3 | 890 | 385 | 33,485 |
| 0.5 | 750 | 740 | 33,430 |
| 0.7 | 525 | 1250 | 33,050 |
| 0.8 | 399 | 1600 | 33,568 |
| 0.9 | 225 | 2025 | 33,525 |
| 1.0 | 0 | 2575 | 33,475 |

**Table 1.** 다양한 혼합물의 시뮬레이션에 사용된 $[C_4mim][PF_6]$ 및 BZN 분자의 수.

![Figure 1](Figure1_placeholder)
**Fig. 1.** 최적화된 BZN 분자와 $[C_4mim][PF_6]$ 이온 쌍의 구조. 전체적으로 사용된 원자 라벨도 표시되어 있다.

<!-- Page 4 -->
각각 0.1 ps와 2 ps의 결합 상수(coupling constants)를 갖는 Nose-Hoover 및 Parrinello–Rahman 알고리즘을 사용하여 298 K 및 1 bar로 유지되었습니다. 그 후 시뮬레이션은 NVT 앙상블에서 약 200 ns 동안 가열-냉각 사이클 [298–443 K]을 거쳤으며, 결합 길이는 LINCS$^{53}$를 통해 제약되었습니다. 단거리 비결합 상호 작용에는 1.4 nm 차단 거리(cut-off distance)가 사용되었으며, 장거리 상호 작용은 Particle-mesh Ewald 정전기학$^{54}$ 및 분산 에너지 보정으로 처리되었습니다. 앙상블은 단계적으로 298 K로 냉각되었고, 시뮬레이션은 NVT 앙상블에서 0.002 ps 시간 간격으로 약 300 ns 동안 계속되어 안정적인 평형 상태에 도달했습니다. 분석은 시뮬레이션의 마지막 10 ns에 초점을 맞추었습니다.

### 결과 및 토의 (Results and discussion)
#### 구조적 특성 (Structural properties)
힘장(force field)의 타당성, 즉 시뮬레이션 결과의 타당성을 위한 일반적인 관행으로서, 우리는 액체 밀도($\rho$)와 표면 장력($\gamma$)을 시뮬레이션했습니다. 이 결과들과 실험 데이터(순수 $[C_4mim][PF_6]$의 경우 298 K에서 $\gamma = 47.50 \, mJ/m^2$ 및 $\rho = 1.36730 \, g/cm^3$; 순수 BZN의 경우 $\gamma = 38.33 \, mJ/m^2$ 및 $\rho = 1.00069 \, g/cm^3$)$^{8,55,56}$ 사이에 좋은 일치가 결론지어졌으며, 편차는 각각 1.2%, 3.45% 및 2.71%, 7.06%를 넘지 않았습니다.

이성분 혼합물($[C_4mim][PF_6]+BZN$)의 분자 간 상관관계는 반경 분포 함수(RDFs)를 사용하여 분석되었습니다. 그림 2는 양이온, 음이온 및 BZN 분자의 질량 중심(COM) 간의 상관 함수를 보여줍니다. 양이온$\cdots$음이온 상관 함수의 첫 번째 피크는 혼합물 전체에서 일관되게 유지되며($\sim 0.47 \, nm$), 피크 높이는 $X_{BZN}= 0.0 < 0.1 < 0.3 \ll 0.5 < 0.7 \ll 0.8 \ll 0.9$ 순서입니다. 이러한 단거리 상관관계는 모든 $X_{BZN}$ 값에서 양이온$\cdots$음이온 정전기적 상호 작용의 강력한 효과를 강조합니다. $X_{BZN}$을 증가시키면 IL이 이온 쌍으로 분리되는 현상(시너지)이 강화되는데, 여기서 시너지는 개별적인 영향을 능가하는 집단적 효과를 나타냅니다$^{57}$. IL의 이온적 특성은 양이온$\cdots$음이온 상호 작용 및 수명이 긴 클러스터에서 국소적인 질서를 촉진하여 지배적인 양이온$\cdots$음이온 상관관계를 초래합니다(Fig. 2a 대 b, c 참조).

IL 내의 이온 간 상호 작용은 분자 구성에 의해 영향을 받으며 주어진 몰 분율의 혼합물을 사용하여 분석할 수 있습니다. 양이온$\cdots$양이온($C\cdots C$) 및 음이온$\cdots$음이온($A\cdots A$) 상관관계는 반대 전하로 인한 강한 정전기적 인력을 나타내는 양이온$\cdots$음이온($C\cdots A$) 상호 작용보다 약합니다. $C\cdots C$ 및 $A\cdots A$ RDF의 첫 번째 피크 높이(Fig. 2b, c)는 $A\cdots C$의 경향을 반영하지만 $0.5X_{BZN}$과 $0.8X_{BZN}$ 사이에서 역전된 상관관계 순서를 보입니다; $C\cdots C$ 및 $A\cdots A$ 상관관계는 $0.8X_{BZN}$보다 $0.5X_{BZN}$에서 더 강합니다. 낮은 몰 분율($0.3X_{BZN}$까지)에서는 $C\cdots C$ 및 $A\cdots A$ 상관관계에서 감지할 수 있는 변화가 보이지 않습니다. $X_{BZN}$에 따른 이러한 상관관계 이동은 0.3 및 0.7에서의 밀도 전이와 상관관계가 있으며, 0.5에서 최소값을 갖습니다(상호 동적 특성 섹션 참조). 두 번의 전이는 등몰 분율($0.5X_{BZN}$) 근처인 $0.3X_{BZN}$ 및 $0.7X_{BZN}$에서 발생합니다. $C\cdots C$ 및 $A\cdots A$ RDF의 첫 번째 피크 높이는 $X_{BZN}$에 따라 증가합니다. $A\cdots A$, $C\cdots C$ 및 $A\cdots C$의 첫 번째 피크 위치(각각 $\sim 0.94, 0.9, 0.47 \, nm$)는 $C\cdots A$가 모든 몰 분율에서 가장 강한 상관관계임을 나타냅니다. $C\cdots C$ 및 $A\cdots A$ 상관관계는 주변적인 것으로 간주되어야 합니다.

BZN을 포함하는 상관관계(즉, $A\cdots BZN$, $C\cdots BZN$, $BZN\cdots BZN$)는 각각 Fig. 2d–f의 RDF로 설명됩니다. 낮은 $X_{BZN}(=0.1, 0.3, 0.5)$과 높은 $X_{BZN}(=0.7, 0.8, 0.9)$에 대해 첫 번째 피크 높이의 경향에 체계적인 변화가 존재합니다. 이에 따라 IL과 BZN 분자 간의 상관관계는 낮은 $X_{BZN}$에서 더 두드러지며 $X_{BZN}$이 증가함에 따라 감소합니다. 전반적으로 IL과 BZN은 모든 혼합물에서 $A\cdots BZN > BZN\cdots BZN > C\cdots BZN$의 순서로 상관관계를 갖습니다.

$BZN\cdots BZN$ 및 $C\cdots BZN$ RDF는 첫 번째 피크 위치가 $A\cdots BZN$($\sim 0.56 \, nm$)보다 약간 더 먼 거리(일반적으로 각각 $\sim 0.62 \, nm$ 및 $\sim 0.68 \, nm$)에 있음을 보여줍니다. 양이온보다 작은 음이온의 크기가 이를 설명할 수 있습니다. 여기서, 모든 $X_{BZN}$에서 $\sim 0.40 \, nm$의 $BZN\cdots BZN$ RDF에 대해 숄더(shoulder)가 관찰되며(Fig. 2f), 이는 적층 모드(stacking mode)에서 $BZN\cdots BZN$의 가장 가까운 접근 거리와 일치합니다(순수 액체 BZN에 대해 이전에 연구됨$^{20}$). 이 숄더는 다른 $X_{BZN}$ 수준보다 $0.1X_{BZN}$ 혼합물에서 처음 나타납니다. 따라서 수많은 IL 이온은 $0.1X_{BZN}$에서 BZN 분리를 촉진하여 시너지 효과를 통해 적층 모드의 작은 $BZN\cdots BZN$ 응집체를 형성합니다$^{57}$. $0.5X_{BZN}$에서의 첫 번째 피크 높이는 다른 분율을 초과하며 숄더가 더 두드러집니다. 이러한 RDF는 각 분자의 COM을 기반으로 하고 BZN의 COM은 평면 부분에 있기 때문에, 더 높은 피크는 더 실질적인 적층 구조를 나타냅니다. $0.5X_{BZN}$ 혼합물은 시너지 상호 작용을 향상시켜 $A\cdots BZN$, $C\cdots BZN$ 및 $BZN\cdots BZN$을 포함하는 벌크 상호 작용을 최적화합니다.

BZN 분자의 ortho, meta, para 수소 원자와 음이온 불소(F) 원자는 수소 결합을 형성합니다. 그림 3a는 ortho-H 원자와 하나의 음이온 F 원자 사이의 RDF를 보여주며, $\sim 0.27 \, nm$에서 수소 결합을 나타냅니다. 그림 3b, c의 부틸 말단 C 원자 간의 상관관계에서 알 수 있듯이, 양이온의 부틸 사슬 간의 상호 작용에서는 반데르발스 힘이 우세합니다. BZN 농도의 체계적인 효과는 그림 3a–c에서 분명합니다. BZN의 N 원자와 양이온 H 원자 사이의 수소 결합은 $0.5X_{BZN}$에 대해 그림 3d에 묘사되어 있으며, 가장 강렬한 피크는 $\sim 0.27 \, nm$에 있고 다른 $X_{BZN}$ 값에서도 일관됩니다(표시되지 않음). 그림 3d의 색상 코드는 수소 결합 확률을 보여주며, $H_1–H_3$(이미다졸 고리) > $H_{13}–H_{15}$(메틸기) > $H_4–H_5$(메틸렌기) > $H_6–H_{12}$(부틸 꼬리) 순으로 순위가 매겨집니다(Fig. 1 라벨 참조). 이미다졸륨 헤드 그룹에 더 가까운 수소 원자는 BZN의 N 원자와 강하게 상관관계를 갖습니다. 이 $N\cdots (H_1–H_3)$ 상관관계는 두 번째 피크까지 지속되어 헤드 그룹 상호 작용의 중요성을 강조합니다.

추가적인 구조 분석은 그림 3e와 같이 $C_{14}$(para C) 및 $C_{11}$과 양이온 C 및 N 원자 간의 상관관계를 조사합니다. 가장 날카로운 피크는 $C_{14}$와 $C_7$(부틸 꼬리 C) 상관관계를 나타냅니다. 두 번째 껍질(shell)에서 지속되는 다른 상관관계는 $C_{11}$과 $C_8$(메틸 C), $N_1$ 및 $N_2$(이미다졸 고리 N들), $C_4$(메틸렌 C)를 포함합니다. 이러한 발견은 BZN 분자 응집 및 적층 구성의 형성을 나타냅니다. 동시에 BZN 방향족 고리는 양이온 알킬과 상호 작용하는 반면, $C \equiv N$ 그룹은 이미다졸륨 고리의 H 원자와 상호 작용합니다.

TRAVIS 소프트웨어$^{58}$를 사용하여 $0.5 X_{BZN}$에서 BZN 분자 주변 이온의 공간 분포 함수(SDFs)를 분석하여 추가적인 통찰력을 얻었으며, 이는 그림 4에 나와 있습니다. 음이온 구름은 주로 BZN의 H 원자, 특히 ortho-H를 감싸고 있어 음이온의 F 원자와의 잠재적인 수소 결합 형성을 시사합니다(Fig. 4a). 반대로 음이온은 $C \equiv N$ 그룹과 반발적으로 상호 작용하여 뒤쪽 측면을 점유합니다. 유사하게,

<!-- Page 5 -->
양이온 구름은 $C \equiv N$ 그룹 주변에 공간적 분포를 나타내며, 이는 BZN의 N 원자와 양이온의 H 원자, 특히 이미다졸 고리에 있는 H 원자 사이의 수소 결합에 기인합니다. 그림 3d 및 e의 RDF와 일치하며, 4b는 양이온 부틸 사슬 주변으로 BZN 분자 구름이 확장됨을 보여줍니다.

#### 배위 및 에너지 프로파일 (Coordination and energy profiles)
상관 함수를 통해 계산된 배위수(CN)는 혼합물 성분의 상대적 구조를 설명합니다. 양이온–음이온, BZN–음이온, BZN–양이온 및 BZN–BZN 상호 작용에 대한 CN 값은 TRAVIS 패키지$^{58}$를 사용하여 $X_{BZN}$에 걸쳐 결정되었습니다(Table 2). $X_{BZN}$이 증가함에 따라 양이온–음이온 쌍의 CN은 감소하는 반면, 양이온, 음이온 및 다른 BZN 분자 주변의 BZN에 대해서는 증가합니다. 이는 BZN 분자가 음이온과 양이온 사이에 위치하여 BZN–양이온 적층 구조를 형성하고 음이온과 수소 결합을 형성함을 시사하며, 이는 순수 벤조니트릴의 분자 동역학 시뮬레이션에서의 평면 및 적층 클러스터와 일치합니다$^{20}$. $X_{BZN}$이 0.3에서 0.7인 혼합물에서 양이온-음이온 CN은 3으로 일정하게 유지됩니다. 그러나 RDF(Fig. 2a)는 $X_{BZN}$이 증가함에 따라 더 낮은 양이온-음이온 동역학을 시사함으로써 이를 식별합니다. $X_{BZN} = 0.9$인 혼합물에서 IL은 CN=2와 상호 작용하며, 이는 낮은 몰 분율의 IL이 약 2개의 IL을 포함하는 확률 높은 클러스터로 분리됨을 나타냅니다. 이 관점은 BZN–BZN에 대해 계산된 CN에도 적용되지만, 혼합물 전반에 걸쳐 BZN 분자는 2~13개의 다른 BZN 분자와 배위할 수 있습니다. 흥미롭게도, 배위

![Figure 2](Figure2_placeholder)
**Fig. 2.** 벌크 용액 내 다양한 $X_{BZN}$에 대한 (a) 양이온$\cdots$음이온 ($C\cdots A$), (b) 음이온$\cdots$음이온 ($A\cdots A$), (c) 양이온$\cdots$양이온 ($C\cdots C$), (d) 음이온$\cdots$벤조니트릴 ($A\cdots BZN$), (e) 양이온$\cdots$벤조니트릴 ($C\cdots BZN$), (f) 벤조니트릴$\cdots$벤조니트릴 ($BZN\cdots BZN$)의 질량 중심 RDFs.

<!-- Page 6 -->
$IL\cdots IL$ 및 $BZN\cdots BZN$의 수는 등몰 혼합물에서 거의 동일하며, 이는 이 혼합물에서 BZN이 알킬 사슬에 적층될 가능성을 뒷받침합니다. 이는 등몰 혼합물에서 표 2의 다른 CN들을 비교할 때도 만족스럽습니다.

IL에 BZN을 첨가할 때의 용매화 에너지론을 조사하기 위해, 다양한 $X_{BZN}$ 혼합물에 대해 위치(potential), 레너드-존스(LJ), 총 에너지의 경향을 계산했습니다. 그림 5는 이온성 액체에 BZN을 첨가하면 위치 에너지가 증가하고(더 양의 값), LJ 에너지는 꾸준히 감소하며(더 음의 값), 운동 에너지는 일정하게 유지됨을 보여줍니다. 전반적으로 IL에 BZN을 첨가하면 양이온-음이온 정전기적 상호 작용이 감소하고 총 에너지가 증가합니다(더 양의 값). 특히 $X_{BZN} = 0.5$에서 총 에너지와 LJ 에너지 사이에 대략적인 균형이 존재합니다.

#### 공간적 배향 (Spatial orientation)
BZN과 IL 간의 공간적 상호 작용은 TRAVIS 패키지$^{58}$를 통해 반경 및 각도 분포를 통합한 결합 분포 함수(CDFs)를 사용하여 조사되었습니다. 보충 그림 S1-A는 반데르발스 힘을 통해 상호 작용하는 양이온 알킬 사슬에 대한 CDF를 보여줍니다. 가장 확률 높은 배향은 앞서 논의한 바와 같이(Fig. 3b) 부틸 말단 C 원자($C_7$) 사이의 거리에 해당하는 0.42 nm 주변에서 발생합니다. 알킬

![Figure 3](Figure3_placeholder)
**Fig. 3.** 다양한 혼합물에서의 사이트-사이트(Site-site) RDFs: (a) ortho-H$\cdots$F, (b,c) C(부틸 꼬리)$\cdots$C(부틸 꼬리). 또한, $0.5 X_{BZN}$ 혼합물에서 (d) N(BZN)$\cdots$H(양이온) 및 (e) C(BZN)$\cdots$C 및 N(양이온)에 대한 상관관계가 표시됨. 원자 라벨은 Fig. 1 참조.

<!-- Page 7 -->
사슬은 주로 $\sim 60^\circ$ 및 $180^\circ$의 각도를 형성하며, $\theta \sim 0^\circ$인 $\sim 0.5 \, nm$ 및 $\sim 0.94 \, nm$에서의 배향은 덜 빈번합니다. 이는 보충 그림 S1-B에 도식적으로 표시된 부틸 꼬리 원자($C_6$, Fig. 3c)의 평균 거리와 밀접하게 일치합니다.

보충 그림 S1-A는 또한 유사한 구조를 가진 혼합물을 비교하는데, $X_{BZN}(=0.3 \text{ 및 } 0.5)$에서의 배향은 $0.0X_{BZN}$과 동일한 강도로 나타나지만 분포가 더 좁습니다. 시각적 비교를 통해 $0.5X_{BZN}$ 혼합물이 공용매 관점에서 구조적으로 잘 정의되어 있음을 확인하며, BZN이 잘 조직된 BZN+IL 구조를 생성하는 상호 작용을 유도합니다. $0.5X_{BZN}$에서 혼합물의 수축(밀도 낮아짐)으로 확인된 시너지를 통해 추가적인 안정화가 가능합니다.

양이온 주변의 BZN 분자의 각도 분포는 $0.5X_{BZN}$에서 그림 6a, b의 도식과 다양한 $X_{BZN}$ 수준에서 보충 그림 S2를 사용하여 연구되었습니다. 그림 6a와 보충 그림 S2-Aa–f는 주로 양이온의 부틸 사슬과 BZN 고리 사이의 (각도-길이) 상관관계를 통해 이러한 분포를 분석하는 데 도움이 됩니다. CDF는 각도 $\theta=0^\circ$ 및 $180^\circ$에서 두 개의 등고선을 보여주며, 0.42–0.5 nm를 중심으로 합니다(Fig. 3e). 이러한 패턴은 BZN($\uparrow$)이 IL($\uparrow$)과 평행($\uparrow\uparrow$), 역평행($\uparrow\downarrow$) 또는 결합된($\downarrow\uparrow\uparrow$) 모드로 상호 작용함을 시사합니다. 후자는 알킬 사슬(0° 또는 180°)에 있는 BZN 분자를 나타내며, 여기서 $C \equiv N$ 그룹은

| $X_{BZN}$ | Cation–anion | BZN–cation | BZN–anion | BZN–BZN |
| :--- | :--- | :--- | :--- | :--- |
| 0.0 | 4 | – | – | – |
| 0.1 | 4 | 0 | 0 | 0 |
| 0.3 | 3 | 2 | 1 | 2 |
| 0.5 | 3 | 4 | 2 | 4 |
| 0.7 | 3 | 6 | 4 | 7 |
| 0.8 | 2 | 7 | 5 | 10 |
| 0.9 | 2 | 9 | 7 | 13 |
| 1.0 | – | – | – | 15 |

**Table 2.** 시뮬레이션된 $[C_4mim][PF_6]$ 및 BZN의 다양한 혼합물에서 성분들의 배위수.

![Figure 4](Figure4_placeholder)
**Fig. 4.** $0.5 X_{BZN}$에서의 SDFs: (a) BZN 분자 주변의 양이온(빨간색) 및 음이온(파란색). (b) 양이온 주변의 BZN 분자 SDF. (c) 양이온, 음이온 및 BZN 분자에 대한 색상 코드 예시.

<!-- Page 8 -->
이미다졸 고리와 수소 결합을 형성합니다. 낮은 $X_{BZN}(0.1, 0.3, 0.5)$에서는 이러한 구성의 확률이 증가하는 반면, 높은 $X_{BZN}(0.7, 0.8, 0.9)$에서는 그 개체수가 감소합니다(Fig. 6, 보충 그림 S2-A). 높은 $X_{BZN}$에서는 더 넓은 각도 범위가 보이는 반면, 낮은 값에서는 0° 및 180°에 집중됩니다. 이러한 배향은 보충 그림 S2-B에 설명되어 있습니다.

구조 분석은 $C \equiv N$ 그룹과 이미다졸 고리의 H-원자 사이의 가능한 수소 결합에 초점을 맞추었습니다. $\sim 0.26 \, nm$(Fig. 3d)에서 가장 가능성 있는 배향은 100°에서 180°까지 걸쳐 있으며, 높은 $X_{BZN}$보다 낮은 $X_{BZN}$에서 확률이 더 높습니다(Fig. 6b 및 보충 그림 S2-Ag–l; 보충 자료 참조).

![Figure 5](Figure5_placeholder)
**Fig. 5.** $[C_4mim][PF_6]$ 및 BZN 혼합물 전체에 걸친 다양한 에너지의 변화.
- **그림 내 텍스트:**
    - total energy (총 에너지)
    - potential energy (위치 에너지)
    - LJ energy (레너드-존스 에너지)
    - kinetic energy (운동 에너지)

![Figure 6](Figure6_placeholder)
**Fig. 6.** ($0.5 X_{BZN}$ 혼합물에서의) 결합 분포 함수(CDFs): (a) 양이온과 BZN 분자 (적층 모드), (b) 양이온과 BZN 분자 (수소 결합 상호 작용), (c) 음이온과 BZN 분자. 해당하는 IL+BZN 상호 작용도 도식적으로 표시됨.
- **그림 내 텍스트:**
    - angle (degree) (각도 (도))
    - $a-0.5X_{BZN}$
    - $b-0.5X_{BZN}$
    - $c-0.5X_{BZN}$

<!-- Page 9 -->
Fig. S2-C). F-원자를 통해 상호 작용하는 음이온은 수소 결합으로 인해 BZN의 H-원자 근처에서 발견됩니다(Fig. 3a). $X_{BZN}$이 증가함에 따라 음이온과 BZN(ortho-H를 통한) 사이의 상호 작용은 약해집니다(Fig. 6c 및 보충 그림 S2m–r). 확률적 등고선 분포는 $\sim 0.28, 0.48, 0.67, 0.92 \, nm$에서 나타나며, $\sim 0.28 \, nm$가 120°에서 180° 사이에서 가장 확률이 높습니다.

보충 그림 S3은 다양한 $X_{BZN}$ 값에서 양이온$\cdots$음이온 쌍의 CDF를 보여줍니다. 0.26 nm 주변의 가장 확률 높은 구성은 음이온(F-원자)과 양이온의 가장 산성인 H-원자 사이의 거리에 해당하며 130° 각도로 배향되어 있습니다. $\sim 1:1$ 몰 비율에서 BZN은 $IL\cdots BZN$ 상호 작용을 강화하여 대부분의 양이온–음이온 상호 작용을 약화시킵니다. RDF, SDF 및 CDF 분석은 BZN 분자가 IL의 부틸 꼬리에 적층됨을 확인합니다. $C \equiv N$ 그룹은 이미다졸륨 고리와 상호 작용하고(Figs. 3d 및 6b, 보충 그림 S2-Ag–l), 그 para-C 원자는 부틸 사슬의 말단 C와 강하게 상관관계를 갖습니다(Figs. 3e 및 6a, 보충 그림 S2-Aa–f). 순수 BZN 액체$^{20}$에서 두드러진 이 역평행 적층은 이성분 혼합물로 확장됩니다(Fig. 7). BZN은 이미다졸륨과 제한된 상관관계를 보이지만, $H_3$ 원자와의 수소 결합은 적층을 향상시킬 가능성이 높습니다(Fig. 4b). 이미다졸 고리 위의 음이온은 정전기적 힘을 통해 상호 작용합니다: 하나의 F-원자는 양이온 $H_3$ 원자와 $\sim 130^\circ$에서 상관관계를 갖고, 다른 하나는 BZN의 ortho-H 원자와 $\sim 120^\circ–180^\circ$에서 수소 결합을 형성하여 BZN을 양이온의 알킬 사슬을 따라 정렬시킵니다(Fig. 7).

#### 밀도 프로파일 및 SFG 증거 (Density profiles and SFG evidences)
우리는 이전에 수행된 실험적 SFG 진동 분광법$^{45}$의 분자적 기원을 탐구하기 위해 IL + BZN 혼합물의 표면 구조를 시뮬레이션했습니다. 실험의 세 가지 주요 발견은 (i) IL의 메틸렌 그룹 및 이미다졸륨 고리에서 SFG 신호가 없음, (ii) IL $-CH_3$ 그룹에 대한 SFG 강도가 점진적으로 손실되어 $0.5X_{BZN}$에서 사라짐, (iii) $X_{BZN} < 0.8$인 혼합물에서 $C \equiv N$ 그룹의 SFG 신호가 없음입니다.

![Figure 7](Figure7_placeholder)
**Fig. 7.** 결합된 평행-역평행 적층 모드($\downarrow\uparrow\uparrow$)에서 IL과 상관된 BZN의 도식적 표현. 양이온은 빨간색, 음이온은 파란색, BZN은 청록색으로 표시됨. 세 개의 메틸렌 그룹이 적층 구성에 참여한다는 점에 유의. 명확성을 위해 수소 원자는 생략됨.

<!-- Page 10 -->
0.8. 묽은 용액($X_{BZN} < 0.4$)에서 BZN 분자가 표면에서 더 질서 정연하다는 결론이 내려졌습니다$^{45}$. 시뮬레이션은 이러한 질서가 BZN이 IL 양이온 알킬 사슬에 적층되는 것에서 비롯되는 반면, $C \equiv N$ 그룹은 낮은 $X_{BZN}$에서 이미다졸륨 고리 수소와 수소 결합을 형성함을 시사합니다(Fig. 6a, b 및 보충 그림 S2-Aa–l). 낮은 $X_{BZN}$에서 각 BZN은 주로 이온 쌍과 상호 작용하여 벌크 및 표면 영역 모두에서 더 질서 정연한 $BZN\cdots IL$ 구조를 생성합니다. 보충 그림 S2-Ag–l은 $0.9 X_{BZN}$까지 감지 가능한 $C \equiv N$ 피크가 없음을 뒷받침합니다. $X_{BZN} < 0.8$에 대한 SFG 스펙트럼에서 $C \equiv N$의 진동 신호가 없는 것$^{45}$은 수소 결합 구속(confinement) 때문이며, $X_{BZN} > 0.8$의 경우 과잉 BZN이 교란되지 않은 진동 상태를 허용합니다.

배향 및 상대적 위치를 포함한 표면 분자 구조는 3차원 경계 조건 하에서 각 혼합물의 슬래브를 시뮬레이션하여 연구되었습니다. 보충 그림 S4는 BZN, IL, 양이온, 음이온 조각 및 전체 시스템의 수 밀도(number density)를 보여줍니다. 비교를 위해 순수 IL 및 BZN 시뮬레이션이 수행되었습니다. 순수 IL(보충 그림 S5)에서 양이온은 표면에 더 많이 노출되며, 이는 알려진 현상입니다$^{59}$. 부틸 사슬은 증기상으로 돌출되는 반면, 메틸 그룹과 이미다졸륨 고리는 표면 아래에 있으며, 이는 메틸렌 그룹이나 이미다졸륨 고리에서 피크가 없는 SFG 진동 스펙트럼$^{45}$과 일치합니다. 순수 IL에 대한 수 밀도(Fig. 8에 플롯됨)는 최외각 표면에 부틸 사슬의 말단 메틸 그룹이 포함되어 있고, 그 뒤를 이어 메틸렌 그룹, 고리의 C 원자, 메틸 그룹이 있음을 보여줍니다. 이는 SFG 스펙트럼의 배열$^{45}$과 일치하며, 이미다졸륨 고리가 표면과 평행함을 시사합니다. 추가 시뮬레이션은 고리가 주로 하부 표면(subsurface)에 확장된 밀도 프로파일을 가지고 있음을 보여줍니다. 이러한 결과는 SFG가 표면에 노출된 분자 부분에서 발생함을 시사합니다. 이성분 혼합물을 시뮬레이션하면 각 성분이 서로를 어떻게 탐색하는지 명확히 하여 합 주파수 빔을 생성하는 영역에 대한 모호성을 해결합니다. 그림 8에는 표면의 분자 부분에 대한 그림도 포함되어 있으며, 이는 SFG 발생의 지역적 기원을 나타낼 수 있습니다.

0.1 및 $0.3X_{BZN}$ 혼합물(보충 그림 S4b, c)의 경우, 빈번한 $BZN\cdots IL$ 적층으로 인해 BZN 분자가 주로 벌크 상에 존재합니다(Fig. 7). 양이온과 음이온의 표면 배향은 순수 IL의 배향을 반영합니다. $0.5X_{BZN}$(Fig. 9 및 보충 그림 S4d)에서 BZN과 IL 모두 표면 밀도가 증가하며, 더 높은 BZN 분율은 IL 조각이 표면에 도달하는 것을 방지합니다. 중간 몰 분율에서 BZN과 IL은 최외각 표면을 놓고 경쟁하며, 이들의 상호 작용은 감수성(susceptibilities)과 SFG 활성에 영향을 미칩니다. SFG 스펙트럼은 $0.5X_{BZN}$ 근처에서 $CH_3$ 피크의 점진적인 감소를 보여줍니다$^{45}$. $0.5X_{BZN}$에 대한 그림 9는 IL과 BZN 표면 밀도의 교차점을 보여주며 0으로 부드럽게 외삽됩니다. BZN은 특히 $0.5X_{BZN}$ 근처에서 최외각 표면을 점점 더 지배하게 되는데(보충 그림 S4, S6), 이는 1:1 혼합물의 구조적 형태에서 양이온의 알킬 사슬에 BZN이 적층되는 것에 기인합니다.

이러한 발견과 일관되게, SFG 스펙트럼은 BZN이 계면에서 더 질서 정연함을 나타냅니다$^{45}$. 시뮬레이션 및 SFG로 연구된 혼합물에는 SFG 빔을 생성하고 산란시킬 수 있는 자유(상관되지 않은) 알킬 말단 $CH_3$ 그룹 또는 자유 벤조니트릴 고리 $-CH$(각각 $X_{BZN} < 0.5$ 또는 $X_{BZN} > 0.5$인 혼합물에서)가 있습니다. 다른 몰 분율에 대한 밀도 프로파일(Fig. 9 및 보충 그림 S6)을 자세히 살펴보면

![Figure 8](Figure8_placeholder)
**Fig. 8.** 순수 IL $[C_4mim][PF_6]$의 C 원자 수 밀도 프로파일.
- **그림 내 텍스트:**
    - number density (#/nm³) (수 밀도)
    - C7-butyl
    - C6-butyl
    - C5-butyl
    - C4-butyl
    - C3-ring
    - C1-ring
    - C2-ring
    - C8-methyl

<!-- Page 11 -->
(보충 그림 S4) 특히 계면의 최외각 영역에서 BZN과 IL 사이에 유의미한 상관관계가 발생하지 않음을 시사합니다.

이러한 고려 사항에 따라, SFG 방사 강도의 제곱근(ref 45의 Fig. 3b)은 IL의 $CH_3$ 피크에 대해 $X_{BZN}$에 따라 감소하고 BZN의 CH 피크에 대해 증가하며, 이는 특정 진동 모드의 진동자 수와의 비례 관계를 반영합니다. 보충 그림 S4 및 S6은 표면의 BZN 분자 수가 $X_{BZN}$에 따라 증가함을 보여줍니다. 약 $0.5X_{BZN}$에서 $CH_3$ 및 CH에 대한 SFG 강도는 정체(plateau)되며, 이는 두 성분이 표면에 존재하고 논의된 바와 같이 상관되어 있음을 나타냅니다. RDF 플롯(Figs. 2 및 3)은 음이온, 양이온 및 BZN 간의 강한 상호 작용을 보여주며, 이는 $0.5X_{BZN}$ 혼합물에서 가장 낮은 자유 진동 모드로 이어집니다. IL+BZN 혼합물의 형태학적 분석(보충 그림 S7)은 BZN 농도가 증가함에 따라($X_{BZN} > 0.5$), IL이 표면에서 이동하여 벌크 내에 작은 응집체를 형성하고, BZN이 외부 표면에서 우세하며, 저에너지 BZN 분자가 열역학적 안정성을 위해 표면으로 이동함을 보여줍니다. 이러한 요인들은 BZN에 대한 더 높은 SFG 강도에 기여합니다. 또한, IL-BZN 적층(Fig. 7)은 메틸렌 그룹이 BZN과 상호 작용하도록 유도합니다.

#### 상호 동적 특성 (Inter-dynamic properties)
이성분 혼합물에서 BZN과 IL의 동적 특성은 평균 제곱 변위(MSDs)를 사용하는 자기 확산 계수($D_i$)와 같은 수송 특성의 시뮬레이션을 통해 조사됩니다. 혼합물에 대한 MSD 기반 확산 계수는 보충 자료에 자세히 설명되어 있습니다. 그림 10은 다양한 $X_{BZN}$에서 IL, BZN, 양이온 및 음이온 성분의 확산 계수를 보여줍니다. BZN은 모든 몰 분율에서 IL 음이온 및 양이온보다 일관되게 더 높은 확산 계수를 나타냅니다. 양이온과 음이온의 확산 계수는 IL의 확산 계수와 밀접하게 일치하며, 이는 강한 양이온-음이온 상관관계를 나타냅니다. 확산 계수는 몰 분율에 따라 체계적으로 변하며, 질량 밀도 및 표면 장력의 변화와 평행하게 $0.5X_{BZN}$ 주변에서 분자 수송의 상당한 변화가 있습니다(보충 그림 S9). 이러한 경향은 BZN의 더 높은 확산 계수가 혼합물의 전체 확산을 증가시킨다는 것을 보여줍니다. 이는 두 가지 유변학적 영역을 도입합니다: 확산 계수가 순수 IL과 유사한 낮은 $X_{BZN}$($\sim 0.1$에서 $0.3$)과 순수 BZN과 유사한 높은 $X_{BZN}$($\sim 0.9$). 확산 계수는 $0.5X_{BZN}$까지 선형적으로 증가하다가 기하급수적으로 가속화되며, 이는 진행 중인 연구에서 추가 조사의 필요성을 강조합니다.

### 결론 (Conclusions)
$[C_4mim][PF_6]$ 이온성 액체(IL)와 유기 용매 BZN의 혼합을 다양한 혼합물의 MD 시뮬레이션을 통해 연구했습니다. 이 과정은 등몰 혼합물($0.5X_{BZN}$)에서 더 효과적일 수 있는 상당한 시너지를 드러냈으며, 두 성분 모두에 대해 중간 정도의 배위수를 유도했습니다. 등몰 혼합물은 독특한 확산 계수와 에너지 프로파일을 나타내어 총 에너지와 반데르발스 에너지의 균형을 맞췄습니다. 이 혼합물은 벌크 밀도와 표면 장력에서 구조적 변화를 보여 벌크와 표면 특성 간의 상관관계를 확인했습니다. 낮은 $X_{BZN}$ 값에서 높은 IL 농도는 BZN 분자가 분리되고 적층되게 하여 $0.5X_{BZN}$에서 정점에 이릅니다. 이 최적의 $IL\cdots BZN$ 배향은 열역학적으로 유리한 상태를 달성합니다. 더 높은 $X_{BZN}$에서 BZN은 표면에 축적되어 IL을 안쪽으로 밀어내어 표면 에너지를 낮춥니다. 확산 계수는 낮은 몰 분율에서는 선형적으로, 높은 분율에서는 기하급수적으로 변했으며, $0.5X_{BZN}$에서 눈에 띄는 피크를 보였습니다. 혼합물 표면 시뮬레이션에 할애된 상당 부분은 실험적 SFG와 일관된 것으로 밝혀졌습니다.

![Figure 9](Figure9_placeholder)
**Fig. 9.** $0.5 X_{BZN}$ 혼합물에 대한 BZN 및 IL 조각들의 국소 수 밀도(Local number densities).
- **그림 내 텍스트:**
    - number density (#/nm³) (수 밀도)
    - BZN
    - IL
    - cation (양이온)
    - anion (음이온)

<!-- Page 12 -->
![Figure 10](Figure10_placeholder)
**Fig. 10.** 전체 시스템, BZN 및 IL 조각들의 계산된 자기 확산 계수의 농도 의존성.
- **그림 내 텍스트:**
    - Diffusion coefficient (확산 계수)
    - sys (시스템)
    - BZN
    - cation (양이온)
    - anion (음이온)
    - IL

결과$^{45}$는 (i) $X_{BZN} \le 0.8$까지 SFG 스펙트럼에서 $C \equiv N$ 진동 모드의 부재와 (ii) $0.5X_{BZN}$ 근처에서 SFG 신호(알킬 $-CH_3$ 및 벤조니트릴 CH)의 점진적인 소멸을 명확히 했습니다. 이러한 시뮬레이션은 $-CH_3$ 및 CH 신축 모드의 SFG 신호에 대한 새로운 통찰력을 제공합니다. 시뮬레이션은 특히 SFG 실험에서 합 주파수 빔을 독점적으로 생성하는 표면 영역의 특정 분자 부분을 식별하는 데 도움을 주어 오랜 의문을 효과적으로 해결합니다.

### 데이터 가용성 (Data availability)
이 연구의 결과를 뒷받침하는 데이터는 논문 및 보충 자료 내에서 이용 가능합니다.

**Received: 25 July 2024; Accepted: 26 September 2024**
**Published online: 05 October 2024**

### 참고문헌 (References)
1. Wang, Y. et al. Local and long-range organization in room temperature ionic liquids. *Langmuir*. **37**, 605–615 (2021).
2. Rama, R., Meenakshi, S., Pandian, K. & Gopinath, S. C. B. Room temperature ionic liquids-based electrochemical sensors: an overview on Paracetamol detection. *Crit. Rev. Anal. Chem*. **52**, 1422–1431 (2021).
3. Ayatollahi, S. F., Bahrami, M. & Ghatee, M. H. Electrochemical stability of low viscosity ion-pair electrolytes: structure and interaction in quaternary ammonium-based ionic liquid containing bis(trifluoromethylsulfonyl)imide anion and analogue. *Electrochim. Acta*. **501**, 144762 (2024).
4. Pontonia, D., DiMichiel, M. & Deutsch, M. Binary mixtures of homologous room-temperature ionic liquids: temperature and composition evolution of the nanoscale structure. *J. Mol. Liq*. **338**, 116587 (2021).
5. Wei, C., Jiang, K., Fang, T. & Liu, X. Insight into the adsorption of imidazolium-based ionic liquids on graphene by first principles simulation. *J. Mol. Liq*. **338**, 116641 (2021).
6. Roy, H. A., Hamlow, L. A. & Rodgers, M. T. Gas-phase binding energies and dissociation dynamics of 1alkyl-3-methylimidazolium tetrafluoroborate ionic liquid clusters. *J. Phys. Chem. A*. **124**, 10181–10198 (2020).
7. Paschoal, V. H. & Ribeiro, M. C. C. Structure and dynamics of aromatic and alkyl substituted imidazolium-based ionic liquids. *J. Mol. Liq*. **340**, 117285 (2021).
8. Ghatee, M. H. & Zolghadr, A. R. Surface tension measurements of imidazolium-based ionic liquids at liquid -vapor equilibrium. *Fluid Phase Equilib*. **263**, 168–175 (2008).
9. Neumann, J. G. & Stassen, H. Anion effect on gas absorption in imidazolium-based ionic liquids. *J. Chem. Inf. Model*. **60**, 661–666 (2020).
10. Ghatee, M. H., Zare, M., Moosavi, F. & Zolghadr, A. R. Temperature-dependent density and viscosity of the ionic liquids 1-alkyl 3-methylimidazolium iodides: experiment and molecular dynamics simulation. *J. Chem. Eng. Data*. **55**, 3084–3088 (2010).
11. Ghatee, M. H. & Moosavi, F. Physisorption of hydrophobic and hydrophilic 1-alkyl-3-methylimidazolium ionic liquids on the graphenes. *J. Phys. Chem. C*. **115**, 5626–5636 (2011).
12. Legut, D. et al. Inhibition of steel corrosion with imidazolium-based compounds – experimental and theoretical study. *Corros. Sci*. **191**, 109716 (2021).
13. Jorabchi, M., Ludwig, N. R. & Paschek, D. Quasi-universal solubility behavior of light gases in imidazolium-based ionic liquids with varying anions: a molecular dynamics simulation study. *J. Phys. Chem. B*. **125**, 1647–1659 (2021).
14. Ghatee, M. H., Zolghadr, A. R., Moosavi, F. & Ansari, Y. Studies of structural, dynamical, and interfacial properties of 1-alkyl-3-methylimidazolium iodide ionic liquids by molecular dynamics simulation. *J. Chem. Phys*. **136**, 124706–124714 (2012).
15. Bernardino, K., Zhang, Y., Ribeiro, M. C. C. & Maginn, E. J. Effect of alkyl-group flexibility on the melting point of imidazolium based ionic liquids. *J. Chem. Phys*. **153**, 044504 (2020).

<!-- Page 13 -->
16. Lago, N. F., Albertí, M., Lombardi, A. & Pirani, F. A force field for acetone: the transition from small clusters to liquid phase investigated by molecular dynamics simulations. *Theor. Chem. Acc*. **135**, 1–9 (2016).
17. Guevara-Carrion, G., Nieto-Draghi, C., Vrabec, J. & Hasse, H. Prediction of transport properties by molecular simulation: methanol and ethanol and their mixture. *J. Phys. Chem. B*. **112**, 16664–16674 (2008).
18. Gupta, S., Chakraborty, A. & Sen, P. Elucidation of intriguing methanol-dichloromethane binary solvent mixture: synergistic effect, analytical modeling, NMR and photo-induced electron transfer studies. *J. Mol. Liq*. **223**, 274–282 (2016).
19. El-Sinawi, A., Silaipillayarputhur, K., Al-Mughanam, T. & Hardacre, C. Performance of ionic liquid-water mixtures in an acetone cooling application. *Sustainability*. **13**, 2949 (2021).
20. Sakhtemanian, L. & Ghatee, M. H. Simulation investigation of bulk and surface properties of liquid benzonitrile: ring stacking assessment and deconvolution. *ACS Omega*. **7**, 29, 25693–25704 (2022).
21. Lopes, J. N. C., Gomes, M. F. C. & Pádua, A. A. H. Nonpolar, polar, and associating solutes in ionic liquids. *J. Phys. Chem. B*. **110**, 16816–16818 (2006).
22. Pádua, A. A. H., Gomes, C., Canongia Lopes, J. & M. F. and A. Molecular solutes in ionic liquids: a structural perspective. *Acc. Chem. Res*. **40**, 1087–1096 (2007).
23. Shimizu, K., Gomes, M. F. C., Pádua, A. A. H., Rebelo, L. P. N. & Lopes, J. N. C. Three commentaries on the nano-segregated structure of ionic liquids. *J. Mol. Struct. Theochem*. **946**, 70–76 (2010).
24. Shimizu, K., Tariq, M., Rebelo, L. P. N. & Lopes, J. N. C. Binary mixtures of ionic liquids with a common ion revisited: a molecular dynamics simulation study. *J. Mol. Liq*. **153**, 52–56 (2010).
25. Bhargava, B. L. & Balasubramanian, S. Insights into the structure and dynamics of a room-temperature ionic liquid: ab initio molecular dynamics simulation studies of 1-n-butyl-3-methylimidazolium hexafluorophosphate ($[bmim][PF_6]$) and the $[bmim][PF_6]-CO_2$ mixture. *J. Phys. Chem. B*. **111**, 4477–4487 (2007).
26. Kapoor, U. & Shah, J. K. Preferential ionic interactions and microscopic structural changes drive nonideality in the binary ionic liquid mixtures as revealed from molecular simulations. *Ind. Eng. Chem. Res*. **55**, 13132–13146 (2016).
27. Bruce, D. W. et al. Nano-segregation and structuring in the bulk and at the surface of ionic-liquid mixtures. *J. Phys. Chem. B*. **121**, 6002–6020 (2017).
28. Kapoor, U. & Shah, J. K. Thermophysical properties of imidazolium-based binary ionic liquid mixtures using molecular dynamics simulations. *J. Chem. Eng. Data*. **63**, 2512–2252 (2018).
29. Zhang, Y., Khalifa, K., Newberg, J. T. & Maginn E. and Anion enhancement at the liquid-vacuum interface of an ionic liquid mixture. *J. Phys. Chem. C*. **122**, 27392–27401 (2018).
30. Gouveia, A. S. L. et al. I. M. Neat ionic liquids versus ionic liquid mixtures: a combination of experimental data and molecular simulation. *Phys. Chem. Chem. Phys*. **21**, 23305–23309 (2019).
31. Wang, X. et al. Understanding of structures, dynamics, and hydrogen bonds of imidazolium-based ionic liquid mixture from molecular dynamics simulation. *Chem. Phys*. **525**, 110391 (2019).
32. Fuladi, S. et al. Multicomponent phase separation in ternary mixture ionic liquid electrolytes. *J. Phys. Chem. B*. **125**, 7024–7032 (2021).
33. Wang, Y. L. et al. Microstructural and dynamical heterogeneities in ionic liquids. *Chem. Rev*. **120** (13), 5798–5877 (2020).
34. Jiang, Y., Wang, Z., Lei, Z. & Yu, G. Structural effects on thermodynamic behavior and hydrogen bond interactions of water–ionic liquid systems. *Chem. Eng. Sci*. **230**, 116186 (2021).
35. Jiang, W., Wang, Y. & Voth, G. A. Molecular dynamics simulation of nanostructural organization in ionic liquid/water mixtures. *J. Phys. Chem. B*. **111**, 4812–4818 (2007).
36. Feng, S. & Voth, G. A. Molecular dynamics simulations of imidazolium-based ionic liquid/water mixtures: alkyl side chain length and anion effects. *Fluid Phase Equilib*. **294**, 148–156 (2010).
37. Niazi, A. A., Rabideau, B. D. & Ismail, A. E. Effects of water concentration on the structural and diffusion properties of imidazolium based ionic liquid–water mixtures. *J. Phys. Chem. B*. **117**, 1378–1388 (2013).
38. Ghorai, P. K. & Sharma, A. Effect of water on structure and dynamics of $[BMIM][PF_6]$ ionic liquid: an all-atom molecular dynamics simulation investigation. *J. Chem. Phys*. **144**, 114505–114511 (2016).
39. Tang, C., Saielli, G. & Wang, Y. Influence of anion species on liquid–liquid phase separation in [EMIm+][X–]/benzene mixtures. *J. Phys. Chem. B*. **127** (49), 10583–10591 (2023).
40. Wu, X., Liu, Z., Huang, S. & Wang, W. Molecular dynamics simulation of room-temperature ionic liquid mixture of [bmim][BF4] and acetonitrile by a refined force field. *Phys. Chem. Chem. Phys*. **7**, 2771–2779 (2005).
41. Chaban, V. V. & Prezhdo, O. V. How toxic are ionic liquid/acetonitrile mixtures? *J. Phys. Chem. Lett*. **2**, 2499–2503 (2011).
42. Bardak, F. et al. Nanostructural organization in acetonitrile/ionic liquid mixtures: molecular dynamics simulations and optical kerr effect spectroscopy. *ChemPhysChem*. **13**, 1687–1700 (2012).
43. Otero-Mato, J. M. et al. Structure, dynamics and conductivities of ionic liquid-alcohol mixtures. *J. Mol. Liq*. **355**, 118955 (2022).
44. Méndez-Morales, T., Carrete, J., Cabeza, O., Gallego, L. J. & Varela, L. M. Molecular dynamics simulations of the structural and thermodynamic properties of imidazolium-based ionic liquid mixtures. *J. Phys. Chem. B*. **115**, 11170–11182 (2011).
45. Duwadi, A. & Baldelli, S. Evidence for ion association at the gas–liquid interface of the mixture of 1butyl-3-methylimidazolium hexafluorophosphate and benzonitrile: a sum frequency generation spectroscopy and surface tension study. *J. Phys. Chem. B*. **127**, 3496–3504 (2023).
46. Shi, Y. et al. Thermodynamic properties of DBN-based ionic liquids and their binary mixtures with primary alcohols. *J. Mol. Liq*. **371**, 121060 (2023).
47. Frisch, M. J. et al. GAUSSIAN 09 Revision A.02 (Gaussian, Inc., 2009).
48. Breneman, C. M. & Wiberg, K. B. Determining atom-centered monopoles from molecular electrostatic potentials. The need for high sampling density in formamide conformational analysis. *J. Comput. Chem*. **11**, 361–373 (1990).
49. Pronk, S. et al. GROMACS 4.5: a high-throughput and highly parallel open source molecular simulation toolkit. *Bioinformatics*. **29** (7), 845–854 (2013).
50. Price, M. L. P., Ostrovsky, D. & Jorgensen, W. L. Gas-phase and liquid-state properties of esters, nitriles, and nitro compounds with the opls-aa force field. *J. Comput. Chem*. **22**, 1340–1352 (2001).
51. Doherty, B., Zhong, X., Gathiaka, S., Li, B. & Acevedo, O. Revisiting opls force field parameters for ionic liquid simulations. *J. Chem. Theory Comput*. **13** (12), 6131–6145 (2017).
52. Payne, M. C., Teter, M. P., Allan, D. C., Arias, T. A. & Joannopoulos, J. D. Iterative minimization techniques for ab initio total energy calculations: molecular dynamics and conjugate gradients. *Rev. Mod. Phys*. **64**, 1045–1097 (1992).
53. Hess, B., Bekker, H., Berendsen, H. J. & Fraaije, J. G. LINCS: a linear constraint solver for molecular simulations. *J. Comput. Chem*. **18**, 1463–1472 (1997).
54. Abraham, M. J. & Gready, J. E. Optimization of parameters for molecular dynamics simulation using smooth particle-mesh ewald in GROMACS 4.5. *J. Comput. Chem*. **32** (9), 2031–2040 (2011).
55. Lei, Y., Chen, Z., An, X., Huang, M. & Shen, W. Measurements of density and heat capacity for binary mixtures {x benzonitrile + (1-x) (octane or nonane)}. *J. Chem. Eng. Data*. **55**, 4154–4161 (2010).
56. Shukla, R. K., Kumar, A., Srivastava, U., Awasthi, N. & Pandey, J. D. Estimation of the surface tensions of benzonitrile, chlorobenzene, benzyl chloride and benzyl alcohol in mixtures with benzene by associated and non-associated processes at 298.15, 303.15 and 313.15 K. *J. Solut. Chem*. **41**, 1112–1132 (2012).

<!-- Page 14 -->
57. Roell, K. R., Reif, D. M. & Motsinger-Reif, A. A. An introduction to terminology and methodology of chemical synergy perspectives from across disciplines. *Front. Pharmacol*. **8**, 1–11 (2017).
58. Brehm, M. & Kirchner, B. TRAVIS-a free analyzer and visualizer for monte carlo and molecular dynamics trajectories. *J. Am. Chem. Soc*. **51**, 2007–2023 (2011).
59. Ghatee, M. H., Fotouhabadi, Z., Zolghadr, A. R., Ghanavati, F. & Borousan, F. Molecular dynamics studies of binary mixtures of pyridine and alkyl derivatives in n-octane. *Fluid Ph Equilib*. **393**, 101–110 (2015).

### 감사의 글 (Acknowledgements)
저자들은 재정적 지원을 해준 쉬라즈 대학교(Shiraz University) 연구 위원회에 감사를 표합니다. 컴퓨터 시간은 부분적으로 기초 과학 연구소(IPM)의 고성능 컴퓨팅 연구 실험실에서 제공되었습니다. MHG는 텍사스 휴스턴 대학교(University of Houston, TX)에서 부여한 안식년 휴가(2017년 1월-9월)에 대해 감사를 표합니다.

### 저자 기여 (Author contributions)
L.S.: 초안 작성, 시뮬레이션, 소프트웨어, 시각화, 분석. A.D.: 교정, 시뮬레이션 결과를 실험적 SFG 스펙트럼과 매칭. S.B.: 시뮬레이션 결과를 SFG 실험 스펙트럼과 매칭, 교정. M.H.G.: 개념화, 해석, 집필 및 편집, 분석, 시각화, 감독.

### 선언 (Declarations)
**경쟁 이익 (Competing interests)**
저자들은 경쟁 이익이 없음을 선언합니다.

**추가 정보 (Additional information)**
**보충 정보 (Supplementary Information)** 온라인 버전에는 https://doi.org/10.1038/s41598-024-74561-8 에서 이용 가능한 보충 자료가 포함되어 있습니다.

**교신 (Correspondence)** 및 자료 요청은 M.H.G.에게 주소로 보내야 합니다.

**재인쇄 및 허가 정보 (Reprints and permissions information)**는 www.nature.com/reprints 에서 이용 가능합니다.

**출판사 참고 사항 (Publisher’s note)** Springer Nature는 출판된 지도 및 기관 제휴의 관할권 주장과 관련하여 중립을 유지합니다.

**오픈 액세스 (Open Access)** 이 기사는 크리에이티브 커먼즈 저작자 표시-비영리-변경 금지 4.0 국제 라이선스(Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License)에 따라 라이선스가 부여되었으며, 원저작자와 출처에 적절한 크레딧을 제공하고, 크리에이티브 커먼즈 라이선스에 대한 링크를 제공하며, 라이선스 자료를 수정했는지 여부를 표시하는 한, 모든 매체 또는 형식으로 비상업적 사용, 공유, 배포 및 복제를 허용합니다. 이 기사에 포함된 제3자 자료를 수정할 권한은 없습니다. 이미지 또는 기타 제3자 자료는 기사의 크리에이티브 커먼즈 라이선스에 포함되어 있습니다(별도로 명시되지 않는 한). 자료가 기사의 크리에이티브 커먼즈 라이선스에 포함되지 않고 귀하의 의도된 사용이 법적 규정에 의해 허용되지 않거나 허용된 사용을 초과하는 경우, 저작권 소유자로부터 직접 허가를 받아야 합니다. 이 라이선스의 사본을 보려면 http://creativecommons.org/licenses/by-nc-nd/4.0/ 을 방문하십시오.

© The Author(s) 2024
