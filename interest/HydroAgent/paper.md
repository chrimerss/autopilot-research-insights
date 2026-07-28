---
title: 'HydroAgent: Formalizing Forecaster Expertise into Skill-Orchestrated Flood
  Forecasting Workflows'
authors: Qingyi Yang; Siqian Qiu; Bing Li; Xu Shan; Jia Feng; Shunan Zhou; Xudong
  Zhou; Tiantian Xing; Jiale Guo; Xiaoyi Dong; Gaoyu Liu; Xiaohuan Liu; Haiqing Pu;
  Qingwen Deng; Xun Zhang; Zhongrun Xiang; Haiyang Qian; Ying Yan; Yongkang Xu; Nuo
  Lei; Tianlong Jia; Baoying Shan; Carlo De Michele
year: '2026'
venue: ''
---

manuscript submitted to AGU Advances
HydroAgent: Formalizing Forecaster Expertise into
Skill-Orchestrated Flood Forecasting Workflows
Qingyi Yang1, Siqian Qiu2, Bing Li3, Xu Shan4, Jia Feng5, Shunan Zhou6,7,
Xudong Zhou8, Tiantian Xing1, Jiale Guo1, Xiaoyi Dong9, Gaoyu Liu10,
Xiaohuan Liu1, Haiqing Pu5, Qingwen Deng11, Xun Zhang12,13, Zhongrun
Xiang14, Haiyang Qian15,16, Ying Yan17, Yongkang Xu18, Nuo Lei13, Tianlong
Jia19, Baoying Shan1, and Carlo De Michele1
1Department of Civil and Environmental Engineering (D.I.C.A.), Politecnico di Milano, 20133 Milano MI,
Italy
2College of Hydraulic and Environmental Engineering, China Three Gorges University, 443002 Yichang,
China
3Independent Researcher, Shandong, 252300, China
4Delft University of Technology, Delft, the Netherlands
5Qinhuangdao Hydrological Survey and Research Center of Hebei Province, Qinhuangdao, China
6School of Hydraulic Engineering, Dalian University of Technology, 116024 Dalian, Liaoning, China
7Institute of Photogrammetry and Remote Sensing, TU Dresden University of Technology, 01062 Dresden,
Germany
8Institute of Hydraulic and Ocean Engineering, Ningbo University, Ningbo 315211, China
9China IPPR International Engineering Co., Ltd., SINOMACH, Beijing, China
10College of Hydrology and Water Resources, Hohai University, Nanjing, China
11School of Earth Science and Engineering, Nanjing University, Nanjing, China
12School of Civil and Environmental Engineering, Cornell University, Ithaca, NY, USA
13College of Civil Engineering, Tongji University, Shanghai, China
14Independent Researcher, Maryland, 20878, USA
15Zhejiang Institute of Hydraulics and Estuary (Zhejiang Institute of Marine Planning and Design),
Hangzhou 310020, China
16Hydro-Climate Extremes Lab (H-CEL), Ghent University, Ghent, Belgium
17Department of Earth, Ocean & Atmospheric Sciences, University of British Columbia, Vancouver, V6T
1Z4, Canada
18College of Water Sciences, Beijing Normal University, Beijing, China
19Karlsruhe Institute of Technology (KIT), Institute of Water and Environment, Karlsruhe, Germany
Corresponding author: Baoying Shan, baoying.shan@polimi.it
–1–
arXiv:2607.23983v1  [physics.geo-ph]  27 Jul 2026

manuscript submitted to AGU Advances
Key points
• HydroAgent transforms tacit forecaster expertise into an auditable skill-orchestrated
workflow driven by large language models
• Skill-guided prior judgment constrains flood peak and volume estimates while im-
proving hydrological scheme selection
• All five state-of-the-art large language models successfully execute the workflow
and achieve comparable judgment accuracy
–2–

manuscript submitted to AGU Advances
Abstract
Operational flood forecasting depends on tacit forecaster expertise that is difficult to for-
malize, audit, and transfer. Although artificial intelligence methods have advanced flood
prediction and model-error correction, most existing studies have not explicitly repre-
sented the tacit expert rules, review checkpoints, and workflow constraints that connect
model outputs to operational warning decisions. To address this issue, we propose Hy-
droAgent, a skill-orchestrated agent framework that embeds Large Language Models (LLMs)
into a model-driven flood forecasting workflow, where each skill encodes explicit rules
to bound LLM reasoning. We validated its effectiveness using five state-of-the-art LLMs
in the South Yamhill River basin. Our results demonstrate that prior judgment captures
observed peak flow and flood volume within 5% tolerance in 10 and 11 out of 14 events,
with 5-fold cross-validation over 129 events yielding Pearson correlations of 0.62 and 0.84.
Building on a high-baseline scheme library (average KGE 0.890), the guided scheme se-
lection further improves KGE by 0.023–0.154, with simulated peak flow and flood vol-
ume falling within the prior judgment ranges for 14 and 13 out of 14 events. All five tested
LLMs successfully execute the HydroAgent workflow with comparable judgment accu-
racy (40%-80%), while showing moderate performance variation and substantial cost dif-
ferences. HydroAgent does not aim to replace human forecasters; instead, it translates
their tacit expertise into an auditable and reproducible workflow, streamlining analyt-
ical steps and supporting more informed decision-making. This skill-orchestrated paradigm
demonstrates how explicit rule boundaries can guide language model reasoning to com-
plement physically based simulation in next-generation flood forecasting.
Plain Language Summary
Flood forecasts are not produced by hydrological models alone; they also depend on
experienced forecasters who judge whether model results make sense for a particular
storm. This experience is valuable, but it is often difficult to formalize and transfer. We
first developed HydroAgent, a workflow that uses large language models within explicit
hydrological rules to make the judgment process more transparent and repeatable. Before
forecasting, HydroAgent groups past floods by magnitude and prepares model parameter
schemes for different flood types. When a new flood begins, it estimates plausible ranges
for the flood peak and total volume by comparing current rainfall, wetness, and river
conditions with similar historical events. Then, it uses those ranges to guide the choice
and adjustment of pre-calibrated model parameters. The hydrological model then
–3–

manuscript submitted to AGU Advances
produces the forecast, which is updated as new observations arrive and reviewed by
human forecasters before warning information is released. In tests for the South Yamhill
River basin, HydroAgent placed observed flood peaks and volumes within its estimated
ranges and improved simulations for several events. This study shows that HydroAgent
can help organize and audit forecaster experience while keeping physical models and
human judgment central to flood-warning decisions.
1 Introduction
Climate change is intensifying the frequency and severity of extreme floods (Allen
& Ingram, 2002; Guan et al., 2024; G. Nearing et al., 2024). Accurate and timely op-
erational flood forecasting systems are increasingly important for loss mitigation and basin-
scale risk management (Fraehr et al., 2023; Najafi et al., 2024). Current forecasting sys-
tems are mainly built on hydrological models, e.g., process-based models. By simulat-
ing rainfall–runoff processes, they produce preliminary flood hydrographs and support
early warning decisions (Jia et al., 2026; Z. P. McEachran et al., 2024). Guided by hy-
drological model forecasts, experienced forecasters make informed judgments and issue
reliable warnings in operational practice (Pagano et al., 2016). However, raw process-
based model outputs are rarely adopted directly as the final forecast, due to the spatial
heterogeneity of precipitation, inherent uncertainty in meteorological forecast data, and
model parameterization errors (Z. McEachran et al., 2025; Tran et al., 2026). Thus, un-
der the prevailing “forecasters-in-the-loop” paradigm, forecasters need to critically eval-
uate and adjust model-generated forecasts by comprehensively considering meteorolog-
ical, geophysical, and operational information (Demeritt et al., 2013; Emerton et al., 2016;
Pagano et al., 2016). For streamflow prediction and flood forecasting, recent compara-
tive evaluations further suggest that forecaster-involved systems consistently outperform
standalone machine learning models, including Long Short-Term Memory (LSTM) net-
works and other deep learning architectures that have shown strong predictive accuracy
in rainfall–runoff modeling (Kratzert et al., 2018a; Frame et al., 2022; G. Nearing et al.,
2024), even when precipitation inputs contain substantial errors (Dong et al., 2025; Tran
et al., 2026). Therefore, the professional judgment of experienced forecasters serves as
a second safeguard for the quality of operational flood forecasts, complementing model
simulations.
–4–

manuscript submitted to AGU Advances
However, this “forecasters-in-the-loop” paradigm also exposes a fundamental bot-
tleneck. The adjusting model parameters and reinterpreting simulated hydrographs pro-
cess by forecasters are inherently tacit and subjective, making such adjustments and their
impact on forecast performance difficult to explicitly represent or rigorously evaluate from
a scientific perspective (Boyle et al., 2000; Gauch et al., 2023; Stuart et al., 2022). Fur-
thermore, training a qualified operational forecaster typically requires years of field ex-
perience, yet such expertise remains highly personal and difficult to transfer systemat-
ically across individuals or institutions (LaDue & Cohen, 2018; Tran et al., 2026). As
a result, the most critical to operational flood forecasting—expert judgment—is the com-
ponent least amenable to explicit representation, independent validation, and system-
atic transfer. This is a major bottleneck for moving flood forecasting toward greater au-
tomation and auditability. Meanwhile, this paradigm faces mounting pressure from rapidly
expanding observational networks, real-time decision-making under incomplete informa-
tion, and flood events that may exceed the historical range under climate change (Kim
& Villarini, 2024; Merz et al., 2021).
Artificial intelligence (AI), particularly deep learning (DL), has already been widely
applied in hydrology, including flood forecasting, streamflow simulation, and model er-
ror correction (Frame et al., 2022; Kratzert et al., 2018a; G. Nearing et al., 2024; Roy
et al., 2023). AI systems can process massive datasets at scale without fatigue and re-
duce subjective bias (Sun et al., 2021). Especially, recent advances in physics-informed
deep learning have further improved predictive accuracy, generalization, and physical con-
sistency across diverse hydrological conditions (Bindas et al., 2024; Shen et al., 2023; Yan
et al., 2023). However, these deep learning for rainfall–runoff simulation, including physics-
informed deep learning model still offer limited interpretability regarding underlying hy-
drological processes. As a result, these models often function as input–output mappings,
which limits trust within the hydrological community (De la Fuente et al., 2023; Feng
et al., 2022). Moreover, AI and DL models can produce predictions inconsistent with es-
tablished hydrological knowledge, making them difficult to trust in out-of-sample basins (G. S. Near-
ing et al., 2021; Read et al., 2019). Even when such models yield correct outputs, it may
remain unclear whether those outputs were obtained for physically valid reasons (Kirchner,
2006; Rudin, 2019). Accordingly, even when DL models achieve stronger prediction per-
formance than process-based models in practice, their outputs still require expert judg-
ment and verification before operational use.
–5–

manuscript submitted to AGU Advances
More recently, large language models (LLMs) and agent-based systems have pre-
sented new capabilities that extend beyond conventional numerical modeling (Boiko et
al., 2023; Yao et al., 2022). Traditional DL approaches fit input–output relationships,
while LLMs enable natural language reasoning, task planning, and tool invocation (Yan
et al., 2025; Pursnani et al., 2024; Ramirez & Demir, 2024). Unlike conventional black-
box models that produce only numerical outputs, LLMs can articulate the rationale be-
hind each decision in natural language, yielding a human-readable reasoning trace that,
when embedded in a structured workflow, becomes inspectable by domain experts. These
capabilities offer the potential to bridge the gap between computational frameworks and
operational flood forecasting (He et al., 2025), not by replacing numerical models, but
by supporting scenario-aware, forecaster-like judgment. However, most LLM-based ap-
plications in hydrology mainly include (1) prompt-based assistance, (2) post-event re-
porting, (3) question-answering tasks (Pursnani et al., 2024), and (4) single-task appli-
cations, such as hydrological model calibration (Zhu et al., 2026), hydropower schedul-
ing (Luo et al., 2025), and hazard narrative extraction (Zhou et al., 2025). Although single-
step tool invocation can support specific computations, current LLM-based applications
still lack integrated workflow orchestration capabilities for representing and executing
the structured, multi-stage reasoning process of operational flood forecasting. Recent ad-
vances in agent systems have introduced skills as an organizational paradigm to address
this limitation (X. Li et al., 2026; Ling et al., 2026). A skill encapsulates a reusable, mod-
ular capability, typically comprising natural-language instructions, invocation logic, tool-
usage procedures, and executable code, thereby enabling an agent to solve recurring classes
of problems (Su et al., 2026). This structure enables LLM agents to reason and act within
explicit rule boundaries, rather than relying on unconstrained generation. Flood fore-
casting is especially well matched to this organization because it is inherently a staged
workflow, in which each step has defined inputs and outputs, domain rules, physical con-
straints, and review boundaries (Nevo et al., 2022). What is needed, therefore, is not an-
other black-box predictor, but an agent structure that can organize scenario interpre-
tation, expert judgment, deterministic computation, and human review within one ex-
ecutable workflow.
In this study, we present HydroAgent, a skill-orchestrated framework for integrat-
ing LLMs into a hydrological-model-driven flood forecasting workflow. Rather than re-
placing the real-time flood forecasting, HydroAgent is asked to coordinate the workflow
–6–

manuscript submitted to AGU Advances
that surrounds the hydrological model: scheme preparation, scenario understanding and
prior judgment, flood type selection, rolling forecasting, and bulletin publication. The
resulting system is intended to be accurate, auditable, and reproducible, while still al-
lowing language-model reasoning where human expertise is normally required. The main
contributions of this paper are threefold. First, we propose HydroAgent, to the best of
our knowledge the first skill-orchestrated framework that embeds LLMs into a hydrological-
model-driven flood forecasting workflow while separating expert judgment from numer-
ical calibration. This represents a new mode of human–AI collaboration in which expert
knowledge, deterministic computation, and language-model reasoning are integrated within
an auditable operational pipeline. Second, we formalize forecaster-style prior judgment
as an executable and auditable skill (Step1), thereby enabling expert reasoning to be rep-
resented as a repeatable operational procedure. Third, we evaluate HydroAgent across
five state-of-the-art LLMs, demonstrating the robustness and transferability of the skill-
orchestrated hydrological agent paradigm.
The rest of this paper is organized as follows. Section 2 describes the HydroAgent
framework, the skill-execution boundary, the Step1 prior-judgment mechanism, and the
study area and evaluation protocol. Section 3 presents a workflow case report, the bench-
mark results, and a discussion of implications and limitations. Section 4 concludes the
paper.
2 Methodology
2.1 Overall HydroAgent workflow
HydroAgent is a skill-orchestrated agent framework for flood forecasting that em-
beds a language model into a physically grounded workflow rather than replacing that
workflow with end-to-end black-box prediction. The system is organized around three
distinct role boundaries. The skill layer defines what should be done: it specifies the op-
erational rules, input-output contracts, and quality constraints that govern each fore-
casting step. The LLM layer defines how to reason: it interprets the event context, co-
ordinates the workflow, and generates explainable text, but it does not directly compute
hydrological quantities. The tool layer defines how to compute: it performs determin-
istic scoring, model calibration, simulation, and artifact generation. This separation is
deliberate. In flood forecasting, the language model should not validate its own numer-
–7–

manuscript submitted to AGU Advances
ical output, and the executor should not decide what the business logic means. HydroA-
gent therefore uses skills to constrain what the language model may request, while en-
suring that hydrograph simulations are executed by deterministic hydrological models
in the tool layer rather than by the language model itself.
HydroAgent workflow includes five steps: (1) scheme preparation, (2) scenario judg-
ment, (3) scheme selection, (4) rolling forecasting, and (5) warning bulletin. Across all
steps, structured JSON interfaces (e.g., scheme.json, judgment.json, and forecast.json)
transfer information between successive steps and keep the workflow traceable and re-
producible (Figure 1). In Step 0, scheme preparation, historical flood events are first clas-
sified into distinct groups according to peak flow magnitude (e.g., Type I–V), with basin-
specific thresholds detailed in Section 2.4. Events within each group are then used to in-
dependently calibrate the parameters of a hydrological model, the Xinanjiang (XAJ) model (Zhao,
1992), using the Dynamically Dimensioned Search (DDS) algorithm (Tolson & Shoemaker,
2007). Detailed descriptions of the XAJ model and the DDS algorithm are provided in
Text S1 and Text S2, respectively. Calibration yields one XAJ parameter set per flood
type. These five parameter sets together form the basin-specific forecasting scheme—
a type-indexed parameter library, which provides the basis for the subsequent real-time
steps.
Chatgpt
Claude
Deepseek
Gemini
LLM – Reasoning Core
Goal Reached
Skill 2
Skill 3
P
ET
Skill 1
What is Skill?
Without Skill:
With Skill:
Reason & Select
Invoke & Execute
Tool and Executor
Read File, Event Calibration, Compile Scheme, ...
Skill Registry (5 Skills) 
Scenario Judgment, Scheme Selection, ...
HydroAgent (Agent Layer)
HydroAgent Layered stack
Step 3: Rolling Forecasting
Step 4: Warning Bulletin
Step 2: Scheme Selection 
Flood Forecasting Workﬂow
Step 0: Scheme Preparation
Hydrological
model
Forcing data
Calibration
algorithm
Skills
Step 1: Scenario Judgment
Judgment Range
Params 
Selected
Calibration and Scheme Preparation
Warning Assessment
Real Time Rolling Forecasting
Expert Judgment
Flood Type Selection
re-think every step
follow a proven path
Peak Range
Volume Range
Cases
Basin: × × ×
Warning level: × × ×  
Provided by HydroAgent
Peak ﬂow & time: × × ×
Veriﬁed by × × × 
Peak      
Peak 228 m³ s⁻¹
Apr 12 19:00
Volume 
√
√
Figure 1.
Schematic overview of the HydroAgent framework.
–8–

manuscript submitted to AGU Advances
When a potential flood event is forecast, HydroAgent enters the real-time forecast-
ing pipeline, which comprises four successive steps. Step 1, scenario judgment, is the core
validation target of this work. Here, the agent parses the scenario, retrieves similar his-
torical cases, and derives prior intervals for peak flow and flood volume. Step 2, scheme
selection, retrieves from the Step 0 library the parameter set matching the Step 1 prior
ranges and runs the XAJ simulation. The detailed calibration workflow is summarized
in Text S3. Step 3, rolling forecasting, updates the simulation as new real-time rainfall
and discharge information arrives. Step 4, warning bulletin, generates the formal fore-
casting report and warning output under human review. Among these steps, Step 1 con-
stitutes the reasoning core of HydroAgent, translating forecaster expertise into LLM-driven
prior judgment within explicit skill boundaries. Steps 0 and 2 form the hydrological core,
in which the hydrological model and the calibration algorithm execute deterministic com-
putation under their respective skills. Steps 3 and 4 form the early-warning and post-
processing module, also executed within defined skill boundaries. HydroAgent pauses
after Steps 1, 2, and 3 (Expert Reviews #1–#3 in Figure 2) to await expert approval
before advancing, keeping the workflow auditable and reliable.
2.2 Skill design and execution boundary
In HydroAgent, a skill is the unit that turns a hydrological task into an executable
module. A skill is defined as a statically authored, self-contained procedural specifica-
tion that encodes a complete workflow, including instructions, permitted tools, acces-
sible resources, and a required output structure. It functions as a controlled execution
template that constrains and guides the agent’s behavior for a specific class of tasks. Each
skill is stored in a SKILL.md file. Following the principle of progressive disclosure, only
the skill’s lightweight metadata is preloaded into the active prompt. The full body is dy-
namically loaded on demand when the skill is matched to the current task (Wu et al.,
2026). During execution, the active skill boundary is fixed for the run, and the available
tools are restricted by the skill’s metadata together with runtime tool filtering. Each skill
contains four components. First, Instructions define the workflow logic and the do-and-
don’t constraints that the agent must follow. Second, Tools define which deterministic
actions the agent may invoke, together with the expected input and output schemas. Third,
Resources define what data sources the skill may access, such as the historical case li-
brary, basin observations, or scheme files. Fourth, an Output Contract defines the canon-
–9–

manuscript submitted to AGU Advances
ical artifact that must be produced when the skill completes. This design keeps the skill
boundary explicit and stable across runs, while allowing the underlying language model
to vary within the same workflow logic. HydroAgent thereby separates procedural con-
trol from event-specific reasoning and deterministic computation.
Step 1 is the clearest example of this organization. The Step 1 skill requires the
agent to parse the event, retrieve similar cases prior to discharge simulation based on an-
tecedent conditions such as rainfall and soil moisture, compare the current event with
the historical record, and apply physical constraints before producing a prior judgment,
followed by an explicit human review gate. Its tool set includes load cases for case-library
overview, score cases for similarity computation, get case detail for retrieving full
case records, get scoring rules for accessing hydrological constraints, and save prior judgment
for contract persistence. Its resources include the case catalog and the Step 0 scheme.
Its output contract includes judgment.json for machine consumption and report.md
for human review. This structure ensures that the reasoning trace is recorded, the nu-
merical score is reproducible, and the final prior judgment can be passed directly to Step
2.
This separation clarifies the respective responsibilities of each layer and supports
auditability, numerical reproducibility, and procedural maintainability. The skill layer
defines the procedure, the language model interprets event-specific differences within that
procedure, and the tool layer performs deterministic scoring and artifact generation. As
a result, HydroAgent preserves reproducibility at the execution level while keeping the
workflow logic maintainable across runs.
2.3 Step1 prior-judgment skill
The Step 1 skill formalizes the judgment process that a human forecaster would
normally perform when turning event information into a prior forecast interval. In prac-
tice, forecasters combine quantitative event attributes, such as rainfall amount, with in-
sights from similar historical cases to estimate plausible ranges of peak flow and flood
volume. To make this process explicit, the skill is organized into four computational stages,
followed by a final human review gate: scenario parsing, analog event retrieval, expert-
rule reasoning, and physical constraint validation. The workflow begins with scenario
semantic parsing. Given a free-text event description, the language model extracts struc-
–10–

manuscript submitted to AGU Advances
tured variables such as rainfall amount, rainfall duration, maximum k-hour cumulative
rainfall, antecedent soil-moisture class, weather type, and initial discharge. If fields are
missing, the model must request clarification rather than generate non-observed values.
This requirement is important because the prior judgment is only meaningful when it
is anchored in an explicit event description.
First, once the event has been parsed, a six-dimensional similarity retrieval is per-
formed in which the executor computes a weighted score over the historical case library
through score cases and returns the top five analogs. The scoring dimensions repre-
sent the main controls on flood response: total rainfall, rainfall duration, soil moisture,
event type, maximum short-duration rainfall, and initial flow. The score has a maximum
of 13 points, with total rainfall given the largest weight because it is a dominant con-
trol on runoff magnitude, while duration, antecedent wetness, and flow conditions remain
important for shaping the response. Specifically, total rainfall contributes up to 3 points,
while the other five dimensions each contribute up to 2 points. Continuous variables are
scored using relative-difference functions, whereas soil moisture and event type are scored
using ordinal and categorical similarity rules, respectively. The use of a continuous rather
than categorical score makes the retrieval more discriminative and helps improve the rank-
ing among closely related hydrological events. This retrieval step instantiates the case-
based example introduced in Section 2.2. Supplementary Text S4 and Table S1 summa-
rize the scoring rule used in Step 1.
Second, the retrieved analogs then enter an expert-rule reasoning stage. The lan-
guage model loads the full case records with get case detail and accesses hydrolog-
ical constraints with get scoring rules before applying expert judgment to correct the
raw similarity result. The reasoning is organized into two complementary parts: analog
correction and boundary handling. Analog correction accounts for differences in rain-
fall amount, antecedent wetness, rainfall intensity, storm duration, and basin-scale runoff
controls. For example, short-duration intense rainfall is treated as more likely to pro-
duce sharper peaks, whereas persistent low-intensity rainfall is treated as more likely to
produce attenuated hydrographs (Breinl et al., 2021). Boundary handling then uses an
anchor case to constrain the upper bound when a close analog exists and falls back to
controlled extrapolation when the target event lies outside the support of the case library.
These rules allow the skill to refine the similarity score into a physically plausible prior
–11–

manuscript submitted to AGU Advances
interval rather than relying solely on nearest-neighbor matching. The detailed rule def-
initions are summarized in Supplementary Text S5 and Table S2.
Third, before the prior judgment is finalized, a physical red-line validation verifies
that the proposed interval satisfies a runoff-coefficient constraint R ∈[0.05, 1.1] and must
not violate obvious hydrological impossibilities such as a forecast peak below the initial
discharge. If a proposed interval fails a physical check, the skill tightens or adjusts the
interval and records the reason in the report. The validated prior-judgment package in-
cludes the peak flow and flood volume intervals, similar cases, flood type, confidence, and
a reasoning summary. Fourth, this package is written to judgment.json for downstream
consumption and to report.md for human review. The final forecaster-in-the-loop con-
firmation then acts as an explicit gate before the judgment is persisted and passed to
Step 2. This stage is not a separate computational step, but rather the point at which
the prior judgment becomes eligible for downstream calibration. The same design pat-
tern extends naturally to the other skills, whose full instructions and tool interfaces fol-
low the same skill-based structure.
To further assess the generalization of Step 1, we use a stratified 5-fold cross-validation
over 129 historical flood events spanning 1995–2024. Events are grouped by flood class
(Type I–V) and distributed across folds in a round-robin manner so that each fold pre-
serves the overall class distribution; within each fold, the agent is evaluated on held-out
events and is only allowed to retrieve cases from the corresponding reference pool. This
design tests whether the Step 1 prior-judgment skill can recover physically reasonable
intervals when the target event is excluded from the retrieval pool. This validation is re-
ported separately from the 14-event benchmark used to demonstrate workflow execution.
2.4 Study Area and Data
HydroAgent is tested in the South Yamhill River basin, with USGS gauge 14194150
at McMinnville, Oregon, USA, used as the outlet. This basin serves as a demonstration
testbed rather than a fixed domain of application: the same workflow can be transferred
to other basins once local observations, model schemes, warning thresholds, and forecaster
rules are converted into basin-specific skills and case libraries. The South Yamhill basin
was selected because its humid runoff response is consistent with the main assumptions
of the XAJ model, especially saturation-excess runoff generation, with a high runoff co-
–12–

manuscript submitted to AGU Advances
efficient, negligible snow influence, and no major reservoir regulation. The analysis used
hourly hydrometeorological records from the CAMELSH data set for 1995–2024, includ-
ing streamflow observations associated with the gauge (Tran et al., 2025; Tran, 2025).
Flood events were extracted from the hourly record using a peak-over-threshold
procedure. For each event, we calculated rainfall amount, rainfall duration, maximum
short-duration rainfall, antecedent wetness, initial discharge, peak discharge, and flood
volume. Events were assigned to five basin-specific flood types according to observed peak
discharge: Type I (Qp ≥490 m3 s−1; 14 events), Type II (350 ≤Qp < 490 m3 s−1;
23 events), Type III (260 ≤Qp < 350 m3 s−1; 22 events), Type IV (205 ≤Qp <
260 m3 s−1; 26 events), and Type V (175 ≤Qp < 205 m3 s−1; 28 events). The event
archive contains 129 historical flood events distributed across these five types. A sub-
set of 113 events from 1995–2019 was used as the historical case library and as the cal-
ibration set for the Step 0 XAJ parameter schemes. The 14 events from 2020–2024 were
held out for independent validation of Step 1 scenario judgment and Step 2 scheme se-
lection. Two flood events in the validation period were excluded from the analysis (N.15 20240129
and N.16 20241229). Their hydrographs are shown in Figure S1 of the Supporting In-
formation. We excluded the Event N.15 20240129 since its discharge series does not rep-
resent a complete flood event: the hydrograph remains nearly flat throughout the pe-
riod and corresponds to the recession of the preceding event rather than an independent
flood. Event N.16 20241229 was excluded because our discharge record ends on 31 De-
cember 2024, whereas the recession of this event extends into 2025, leaving the hydro-
graph truncated. The 129-event archive was also used for the stratified 5-fold cross-validation
described above.
3 Results and Discussion
3.1 HydroAgent-driven flood forecasting results
The capability of HydroAgent to orchestrate the full Step 0–Step 4 chain is illus-
trated with a March 2022 flood event (N.6 20220302). This event is selected for its rep-
resentativeness of a moderate-magnitude storm (max-24 h 59.0 mm), medium soil mois-
ture, and low initial flow of 16 m3/s, whose long duration naturally traverses all five work-
flow stages in a single trace. Prior to the event, Step 0 had already produced a five-class
parameter library (Type I–V, average KGE 0.890 across 113 calibrated events) for the
–13–

manuscript submitted to AGU Advances
basin (Figure 2). Since event-type stratification is not standard practice in operational
hydrology, a complementary experiment was conducted in which a single unified param-
eter set was calibrated across all 113 events and benchmarked against the five-type scheme;
results are reported in Figure S2.
The forecaster initiated Step 1 by submitting a meteorological scenario to HydroA-
gent (Figure 2): 120 mm of areal rainfall over 87 effective hours (mean intensity 1.4 mm/h,
max-24 h 59.0 mm), medium soil moisture, and an initial channel flow of 16.0 m3/s. Re-
trieving analogous historical cases, Step 1 returned a Type III class judgment with a peak
range of 220–330 m3/s, a volume range of 0.85–1.35 ×108 m3, medium confidence, and
a normal risk flag. The observed peak of 294.49 m3/s falls within this range, confirm-
ing successful scenario recognition. The workflow paused at Expert Review #1 (Figure 2),
prompting the duty engineer to either approve the results or request a revision which
triggers a rollback with suggested values. Only upon confirming the physical reasonable-
ness did the chain advance to Step 2. In Step 2, the parameters of the hydrological model
were fine-tuned using initial values selected from the Step 0 parameter library, tuning
sm (188.48 →110.32 mm), kg (0.0764 →0.3698), b (1.337 →1.082), l (12 →18), and
cs (0.923 →0.935). The resulting hourly hydrograph (Figure 2) placed the simulated
peak at 290.86 m3/s at 2022-03-02 22:00, against the observed peak of 294.49 m3/s; peak
error decreased from −14.9% to −1.2% and volume error from −0.5% to +0.8%, with
KGE rising from 0.834 to 0.921. Expert Review #2 validated the hydrograph shape be-
fore rolling forecasting was authorized.
In Step 3, HydroAgent assimilated incoming observed flows and rolled the forecast
forward in real time (Figure 2). Once the event receded, Step 4 compiled a draft bul-
letin: peak time 2022-03-02 22:00, return period approximately 2.1 years, warning level
“No Flood Warning Issued”, with recommended continued monitoring of hydrological
conditions. Expert Review #3 engineer verified and signed off the bulletin for release
(Figure 2). The following section evaluates Step 1 generalization across all held-out events.
3.2 Validation of Prior Judgment and Scheme Selection
To validate the performance of Step 1 scenario judgment, we apply HydroAgent
to the selected river basin and evaluate the accuracy of judgment results for peak flow
and flood volume across 14 flood events during the validation period (2020–2024) based
–14–

manuscript submitted to AGU Advances
HydroAgent web UI demonstration
HydroAgent
User input: Basin 14194150; 1995-2019 hourly data. Request scheme compilation.
Step 0 - Scheme Library
 Offline completed before the forecasting dialogue. 113 events calibrated; Avg KGE 0.890; XAJ parameters grouped by type; scheme saved.
User input: US-14194150 basin forecasts a rainfall, ~120 mm rainfall over 87 h (max-24 h 59 mm;
max-72 h 105 mm), medium soil moisture. Initial flow 16 m3/s. Please estimate the peak and volume.
Step 1 - Scenario Judgment
 Parsed scenario -> JSON. Retrieved top-5 flood cases. Reasoning over local rainfall-runoff rules -> Class Type III. Peak range 220-330 m3/s.
Volume range 0.85-1.35 x 108 m3. // Paused for Expert Review #1
P
Human Review Gate #1 - scenario range approval
Expert checks class, analogue cases, peak range, and volume range.
Approved -> Continue
Revise -> Roll back with suggested values
User input: Expert review confirmed. Proceed to Step 2 scheme selection.
Step 2 - Scheme Selection
 Selected the optimal parameter set from the Step 0 scheme library, matching Step 1 constraints. KGE 0.834 -> 0.921; peak error 14.9% -> 1.2%;
volume error -0.5% -> 0.8%; peak 290.862 m3/s; volume 1.25 x 108 m3. // Paused for Expert Review #2
Metric
Selected scheme
KGE
0.921
Peak error
1.2%
Volume error
0.8%
Peak flow
290.862 m3/s
Total volume
1.25 x 108 m3
P
Human Review Gate #2 - hydrograph approval
Expert evaluates hydrograph shape, timing, peak error, and volume error.
Approved -> Continue
Revise -> Roll back with suggested values
User input: Hydrograph approved. Proceed to Step 3 rolling forecast.
Step 3 - Rolling Forecast
 Rolling playback monitor updates the trajectory in real time and checks warning thresholds as observations arrive. // Paused for Expert Review #3
P
Human Review Gate #3 - warning decision approval
Expert checks rolling deviation trend and warning conclusion.
Approved -> Continue
Revise -> Roll back with suggested values
User input: Warning decision approved. Proceed to Step 4 bulletin generation.
Step 4 - Bulletin
 Peak 272 m3/s @ 2022-03-02 22:00; RP approx. 2.1 yr; No Flood Warning Issued.
Figure 2.
End-to-end workflow of HydroAgent for the March 2022 flood event on South
Yamhill River (basin 14194150), illustrating the Step 0–Step 4 chain and three forecaster-in-the-
loop expert review checkpoints.
–15–

manuscript submitted to AGU Advances
on historical flood records from 1995 to 2024, as shown in Figure 3a. These results are
performed using GPT-5.4 as the LLM backbone, which was one of the most powerful mod-
els available at the time of this study. The performance of other LLMs is shown in Fig-
ures S4 and is discussed in Section 3.4. Figure 3a shows the judgment ranges of peak flow
and flood volume for each event, as inferred from the five most similar historical cases
retrieved by the Step 1 skill. The results show that the judgment ranges encompass the
observed values in most cases, with hit rates of 10 and 11 out of 14 events for peak flow
and flood volume within a 5% tolerance margin, respectively. All judgment ranges are
narrower than the spread of the top five similar historical cases, reflecting the refinement
introduced by LLM reasoning. This indicates that the Step 1 skill can effectively con-
strain the predicted intervals based on the retrieved cases. Two cases (N.1 20200114 and
N.14 20241121) fall outside the predicted ranges for both peak flow and flood volume,
where the LLM underestimated the flood severity. Both events are Type V floods in which
the peak flows only marginally exceed the minimum threshold of our flood definition,
resulting in relatively mild flood signals that are inherently more difficult to estimate ac-
curately.
To further evaluate the generalization capability of Step 1 scenario judgment, we
perform stratified 5-fold cross-validation on 129 historical flood events (1995–2024), as
shown in Figure 3b. The results show that the performance across each fold is compa-
rable, with Pearson correlation coefficients (r) of 0.62 and 0.84 between observed val-
ues and predicted midpoints for peak flow and flood volume, respectively. The judgment
performance for flood volume is better than that for peak flow, consistent with the val-
idation results in Figure 3a. One extreme case (evt 19960209) exhibits a peak flow of
1326 m3/s, nearly twice the maximum peak flow among all other cases. This event is sub-
stantially underestimated by the LLM, as its characteristics have no close analogs in the
historical record, making accurate judgment inherently challenging.
Following the determination of judgment ranges in Step 1, Step 2 selects the op-
timal parameter set from the pre-calibrated scheme library (Step 0) to produce the fore-
cast hydrograph. The full results of all 14 validation events are summarized in Table S3.
Among these, 11 out of 14 events yield KGE values after Step 2 scheme selection equal
to or greater than those obtained by directly applying the default flood type classifica-
tion based on the Step 1 prior judgment ranges, with KGE improvements ranging from
0.023 to 0.154 for the five events where the scheme was updated. The simulated peak
–16–

manuscript submitted to AGU Advances
100
200
300
400
500
600
700
800
900
Peak flow (m³/s)
N.1_20200114
N.2_20200130
N.3_20210114
N.4_20210204
N.5_20210217
N.6_20220302
N.7_20221229
N.8_20230113
N.9_20230412
N.10_20231208
N.11_20240111
N.12_20240302
N.13_20240313
N.14_20241121
(a1) Validation for peak, 2020 2024
0
1
2
3
4
5
6
Flood volume (1e8 m³)
(a2) Validation for volume, 2020 2024
Observed
Step1 judgement interval
Similar cases (Top5)
0
200
400
600
800
1000
1200
1400
Predicted Midpoint (m³/s)
0
200
400
600
800
1000
1200
1400
Observed (m³/s)
r = 0.62 (n=129)
(b1) Five-fold CV for peak, 1995 2024
0
1
2
3
4
5
6
Predicted Midpoint (1e8 m³)
0
1
2
3
4
5
6
r = 0.84 (n=129)
(b2) Five-fold CV for volume, 1995 2024
Fold 0
Fold 1
Fold 2
Fold 3
Fold 4
Figure 3.
HydroAgent performance for Step1 scenario judgment using GPT-5.4. (a1) and
(a2) show per-event comparison across 14 flood events during the validation period (2020–2024)
of observed values (stars), Step1 judgment ranges (boxes), and Top5 similar historical cases (dots
with range whiskers) for peak flow and flood volume, respectively. (b1) and (b2) show 5-fold
cross-validation results (1995–2024, 129 cases in total) for peak flow and flood volume, respec-
tively. Predicted range midpoints are plotted against observed values, with a 1:1 reference line
and ±20% band. Pearson correlation coefficients are annotated in each panel.
–17–

manuscript submitted to AGU Advances
flow and flood volume after scheme selection fall within the Step 1 judgment ranges (with
a 5% tolerance margin) for 14 and 13 out of 14 events, respectively, confirming that the
selected parameter sets produce forecasts consistent with the prior judgment.
Figure 4 presents six representative events selected to illustrate a range of outcomes,
including cases with substantial KGE improvement (N.6, N.9, N.10, N.13), an unchanged
scheme where the default was already optimal (N.3), and a case where Step 1 misjudg-
ment led to degraded performance (N.14). For event N.13 20240313 (Figure 4e), the de-
fault simulation (dashed blue) substantially underestimates the peak flow, whereas the
scheme selected by Step 2 (orange) closely reproduces both the peak magnitude and the
overall hydrograph shape, improving the KGE from 0.720 to 0.874. In contrast, for event
N.3 20210114 (Figure 4a), the KGE remains unchanged at 0.916, indicating that Step
2 correctly retains the original scheme when it is already the best available option.
Three events (N.1, N.8, and N.14) exhibit decreased KGE after scheme selection.
All three are Type V floods with observed peak flows only marginally exceeding the min-
imum flood threshold, producing relatively mild flood signals. For these events, Step 1
tends to overestimate the judgment ranges, as illustrated by the elevated shaded band
in Figure 4f. This upward bias directs Step 2 to select a parameter set that generates
higher peak flows and flood volumes, resulting in overestimated hydrographs that diverge
from the observed discharge. This error propagation from Step 1 to Step 2 highlights that
the accuracy of Step 1 judgment is a critical prerequisite for the overall forecasting per-
formance of HydroAgent.
3.3 Cross-LLM benchmark and within-LLM stability
The portability of the skill-orchestrated design is supported by a stratified 5-fold
cross-validation benchmark of Step 1 across five state-of-the-art LLMs (DeepSeek-v3.2,
Qwen-3.6-plus, GPT-5.4, Gemini-3.1-pro-preview, and Claude-opus-4.6; Figure 5). All
five LLMs operate within the same step 1 skill and achieve broadly comparable per-fold
hit rates (Figure 5a, generally 40–80%), with GPT-5.4 yielding the highest flood-volume
hit rates (74–80% across Folds 1–3) but no model winning by a clear margin. This sup-
ports the central design claim that the workflow, rather than the choice of LLM, gov-
erns forecasting quality. In contrast, Figure 5c reveals substantial cost dispersion that
is largely decoupled from accuracy: GPT-5.4 completes the full benchmark in 1.5 h, whereas
–18–

manuscript submitted to AGU Advances
0
5
10
Rainfall (mm/h)
(a) N.3_20210114
12/16
12/24
01/01
01/09
01/18
Date
0
200
400
600
800
Discharge (m3/s)
KGE: 0.916 -> 0.916
Volume range: [4.20, 5.80] -> 5.70
0
5
10
Rainfall (mm/h)
(b) N.6_20220302
02/27
03/02
03/04
03/07
03/10
Date
0
200
400
600
800
Discharge (m3/s)
KGE: 0.834 -> 0.921
Volume range: [0.90, 1.60] -> 1.25
0
2
4
Rainfall (mm/h)
(c) N.9_20230412
04/09
04/10
04/12
04/14
04/15
Date
0
75
150
225
300
Discharge (m3/s)
KGE: 0.833 -> 0.871
Volume range: [0.68, 0.90] -> 0.77
0
5
10
Rainfall (mm/h)
(d) N.10_20231208
11/30
12/04
12/07
12/11
12/15
Date
0
150
300
450
600
Discharge (m3/s)
KGE: 0.830 -> 0.906
Volume range: [1.50, 2.40] -> 2.63
0
2
4
Rainfall (mm/h)
(e) N.13_20240313
03/10
03/11
03/13
03/15
03/16
Date
0
75
150
225
300
Discharge (m3/s)
KGE: 0.720 -> 0.874
Volume range: [0.70, 0.95] -> 0.82
0
5
10
Rainfall (mm/h)
(f) N.14_20241121
11/16
11/19
11/23
11/26
11/29
Date
0
75
150
225
300
Discharge (m3/s)
KGE: 0.715 -> 0.509
Volume range: [1.35, 1.95] -> 1.58
Observed
Before type selection
After type selection
Peak range
Figure 4.
Comparison of simulated flood hydrographs before and after Step 2 scheme selec-
tion for six representative validation events: (a) event N.3 20210114, (b) event N.6 20220302,
(c) event N.9 20230412, (d) event N.10 20231208, (e) event N.13 20240313, and (f) event
N.14 20241121. Blue bars represent hourly rainfall; black, dashed blue, and orange lines rep-
resent observed discharge, simulated discharge before scheme selection, and simulated discharge
after scheme selection, respectively. The shaded orange band indicates the peak flow range identi-
fied in Step 1.
–19–

manuscript submitted to AGU Advances
Claude-opus-4.6 and Qwen-3.6-plus require 4.3 and 4.7 h, respectively, and monetary cost
spans more than an order of magnitude, from approximately 30 CNY (DeepSeek-v3.2)
to 390 CNY (Claude-opus-4.6, roughly 4× that of GPT-5.4 and 13× that of DeepSeek).
These results suggest that, within the accuracy range observed in this benchmark, bud-
get and latency become first-order considerations alongside accuracy when selecting an
LLM for this workflow. Per-class hit rates (Figure 5b) further show that all five LLMs
perform worst on Type I floods (27–53%), pointing to a shared limitation that is exam-
ined below.
Beyond cross-model comparison, we examined the within-model stability of the Step 1
skill by repeating the prior-judgment task ten times for each of the 14 validation events
using GPT-5.4 (Figure S3). The resulting peak flow and flood volume intervals are tightly
clustered across the ten runs, with within-event range widths substantially narrower than
the Top-5 retrieved-case spread for nearly every event. This indicates that, under the
explicit retrieval rules, physical red-line validation, and contract-bound output enforced
by the skill, the sampling stochasticity inherent to LLM generation is constrained to a
range narrower than the inter-case spread that drives the prior intervals, suggesting lim-
ited impact on the resulting forecasts. Importantly, the two events (N.1 20200114, N.14 20241121)
that fall outside the predicted ranges in Section 3.2 also fall outside the ranges across
all ten repeats, confirming that their underestimation reflects a systematic limitation at
the tail of the case library rather than sampling variance.
3.4 Discussion and outlook
This paper developed a framework to embed large language models into the flood-
forecasting workflow and showed that all five tested LLMs could support forecasts that
captured observed peak flow and flood volume with useful skill. The central value of Hy-
droAgent is not that it replaces process-based hydrological models, but that it organizes
expert judgment, numerical simulation, and human review into an explicit, auditable,
and reproducible workflow. By decomposing forecasting into multiple steps, in which LLMs
are responsible for scenario interpretation and workflow orchestration while process-based
models remain responsible for hydrological simulation, HydroAgent preserves physical
constraints that are often weakened in purely end-to-end deep-learning frameworks (Kratzert
et al., 2018b; Xiang et al., 2020). It is also consistent with the forecasters-in-the-loop paradigm,
in which human expertise remains essential for interpreting uncertain meteorological in-
–20–

manuscript submitted to AGU Advances
deepseek-v3.2
qwen-3.6-plus
gpt-5.4
gemini-3.1-pro-preview
claude-opus-4-6
0
20
40
60
80
100
Hit rate (%)
(a) Per-fold judgement hit rate for peak and volume
Bar style
Peak
Volume
K-fold
Fold 0
Fold 1
Fold 2
Fold 3
Fold 4
deepseek-v3.2
qwen-3.6-plus
gpt-5.4
gemini-3.1-pro-preview
claude-opus-4-6
0
20
40
60
80
100
Hit rate (%)
(b) Per-class judgement hit rate for peak and volume
Flood class
Type_I
Type_II
Type_III
Type_IV
Type_V
deepseek-v3.2
qwen-3.6-plus
gpt-5.4
gemini-3.1-pro-preview
claude-opus-4-6
0
1
2
3
4
Hour
(c) Time and money cost
Cost
Time cost
Money cost
0
100
200
300
400
CNY
Figure 5.
Performance and cost comparison of five LLMs (DeepSeek-v3.2, Qwen-3.6-plus,
GPT-5.4, Gemini-3.1-pro-preview, and Claude-opus-4.6) in the Step 1 stratified 5-fold cross-
validation over 129 flood events (1995–2024). (a) Per-fold hit rates across folds 0–4, with fold
sample sizes of 28, 27, 25, 25, and 24 events, respectively. (b) Per-class hit rates across flood
classes Type I–V, with corresponding event counts of 15, 27, 26, 29, and 32. (c) Running time
(hours, left axis) and monetary cost (CNY, right axis) for the full benchmark. In (a) and (b),
solid bars denote peak-flow hit rate and hatched bars denote flood-volume hit rate; color encodes
the LLM. A judgment is reported as a hit when the prediction error is within 5%.
–21–

manuscript submitted to AGU Advances
puts and model outputs (Tran et al., 2026). Transferring HydroAgent to other basins,
or operational systems, requires replacing or adapting the input data including local hy-
drometeorological records, basin-specific model schemes, warning thresholds, and fore-
caster experience. The main technical challenge is thus not only model portability, but
also the systematic encoding of local expert knowledge into reusable and testable work-
flow components.
The next step is to move HydroAgent from offline retrospective tests toward real
operational use. This requires multi-basin validation across different climate regimes, hy-
drological response types, and basin scales to evaluate whether the current skill frame-
work is transferable. Real-time testing during actual flood seasons is also essential, be-
cause operational value depends not only on retrospective accuracy but also on how fore-
casters interact with the system under time pressure, uncertain rainfall forecasts, incom-
plete observations, and institutional review procedures. Such deployment would allow
HydroAgent to accumulate forecaster feedback, update its case library, and refine local
skills after each event. Looking further ahead, the standardization of hydrological skills,
including version control, quality assessment, benchmark testing, and community shar-
ing, may allow broader reuse of the framework and more systematic improvement of fore-
casting skills. HydroAgent may also benefit from rapid progress in LLM-agent research,
especially in memory and iterative skill refinement, which could improve long-term adap-
tation through continued interaction (Cai et al., n.d.). These capabilities could help Hy-
droAgent evolve from a static offline workflow into a continuously improving operational
assistant, with possible future extensions to broader hydrological early warning (Alfieri
et al., 2013), reservoir operation (Jain et al., 2023; Jia et al., 2019), and risk analysis (Apel
et al., 2009).
We acknowledge some limitations in our study. From Figure 5, it is clear that all
LLMs performance is the worst in type I flood. This may be related to the difficulty that
data-driven models often face in representing extremes or tail distributions. Similar lim-
itations have also been reported in intercomparisons of deep-learning-based Earth sys-
tem models (Watson, 2022; Z. Zhang et al., 2026). However, physics constrained deep-
learning-based hybrid Earth system models generally behave better compared to pure
deep learning models. This indicates the need to further improve the interpretability and
generalization of HydroAgent. Therefore, future work should consider developing the work-
flow based on a hybrid modeling framework (Reichstein et al., 2019). In such a frame-
–22–

manuscript submitted to AGU Advances
work, process-based models, machine learning models, Earth observation products, and
LLM-based reasoning could be combined within the same operational workflow. In par-
ticular, incorporating a regional LSTM model, that is trained on a large number of catch-
ments within a region, is especially promising, as previous studies have demonstrated
its robust performance for streamflow prediction (Jia et al., 2026; Kratzert et al., 2018a).
The LLM would not need to replace the hydrological model. Instead, it could help de-
termine when to rely on the process-based simulation, when to call a machine-learning
correction model, and when the uncertainty is large enough to require additional expert
review. A more ambitious version of this framework may require hydrology-specific LLM
adaptation or retraining, because general-purpose LLMs are not trained to represent hy-
drological process knowledge (like water balance), forecast uncertainty, and hydrolog-
ical operational decision rules in a systematic way. For example, Med-PaLM achieved
expert-level clinical reasoning through medical instruction tuning of a general-purpose
LLM (Singhal et al., 2023), and GraphCast attained operational-level skill in global weather
forecasting through domain-specific foundation-model training (Lam et al., 2023). These
cases suggest that comparable gains could be achievable through hydrology-specific adap-
tation.
A further limitation of the current framework is that forecast uncertainty is still
only partially quantified. Reasoning variability across the five LLMs provides one par-
tial view of uncertainty in the language-model component. However, the current work-
flow still needs to examine the uncertainty from the LLM, especially the hallucination.
One way is to examine the derivative of output to input to analyze the next-token gra-
dient sensitivity (S. Zhang et al., n.d.). Recent studies have raised similar concerns that
data-driven models may learn predictive associations without capturing the underlying
causal or physical mechanisms, and have proposed diagnostic strategies to distinguish
whether models are learning “why” rather than only “what” (Shan et al., 2024). Op-
erational decisions depend not only on the predicted peak flow or flood volume, but also
on how these quantities change under different rainfall, soil moisture, antecedent flow,
or future climate conditions. A model may achieve good predictive accuracy under his-
torical conditions while still producing physically unrealistic responses when the forc-
ing changes. Therefore, future evaluations of HydroAgent should include sensitivity tests
to examine whether the forecast response is hydrologically reasonable.
–23–

manuscript submitted to AGU Advances
Uncertainty from the meteorological variables like precipitation, model calibration,
and the hydrological model structures are not well quantified. Meanwhile, the current
simple hydrological model structure may also contribute a large portion of the uncer-
tainty (Clark et al., 2008). Future work could design an idealized experiment to quan-
tify the uncertainty from each component in HydroAgent. This can be done by using
an ensemble framework (Cloke & Pappenberger, 2009) of meteorological forcing variables,
and different hydrological models. Machine-learning-based hydrological models like LSTM (Kratzert
et al., 2018a), transformer (Yin et al., 2022), or hybrid models (Bhasme et al., 2022) can
also be considered in HydroAgent.
To reduce uncertainty and improve forecast robustness, another important direc-
tion is to embed available Earth observation data into the HydroAgent workflow. The
purpose is to better constrain the uncertainty in meteorological forcing variables like pre-
cipitation (Y. Li et al., 2016), parameter tuning, and other components of the forecast
workflow. Satellite data provide unique information on hydrological states, such as soil
moisture, that could help reduce forecast uncertainty, for example, through SMAP ob-
servations and SMAP-derived surface and root-zone soil moisture products (Entekhabi
et al., 2010; Reichle et al., 2017). Such information could be used to quantitatively up-
date the event description, revise the prior judgment, or constrain the rolling forecast (Jadidoleslam
et al., 2021). For example, after a new flood event occurs, the corresponding observa-
tions could be added to the case library. Comparisons between new observations and fore-
casts could also be used to refine event-retrieval rules and to support Step 3 updating.
This would allow HydroAgent to evolve from a static case-based system toward a con-
tinuously updated forecasting workflow. Such assimilation could also help test the ro-
bustness of LLM-supported reasoning by comparing workflow outputs with satellite ob-
servations. However, this also requires careful treatment of observation error and spa-
tial representativeness, because the value of additional observations depends on whether
they are consistent with the model states and forecast variables.
LLM agents for hydrology remain an emerging research direction. HydroAgent pro-
vides one step toward this direction by showing how language models can be embedded
as workflow orchestrators that interact with hydrological models, case libraries, expert
rules, and human forecasters. However, further exploration is needed to evaluate the re-
liability, failure modes, uncertainty, and transferability under diverse hydrological and
operational conditions. This may require transparent skill designs, community bench-
–24–

manuscript submitted to AGU Advances
marks, uncertainty-aware evaluation, and close collaboration between hydrologists, fore-
casters, and AI researchers. These efforts may evaluate whether LLM agents can become
trustworthy components of next-generation hydrological forecasting and decision-support
systems.
4 Conclusion
In this study, we proposed HydroAgent, a skill-orchestrated agent framework that
embeds LLMs into a physically based flood forecasting workflow translating the tacit ex-
pertise of operational forecasters into an auditable and reproducible procedure. HydroA-
gent was tested on the South Yamhill River basin (Oregon, USA) using 129 historical
flood events (1995–2019) for scheme preparation and 14 recent events (2020–2024) for
validation. The Step 1 scenario judgment skill captured observed peak flow and flood
volume within a 5% tolerance margin in 10 and 11 out of 14 validation events, respec-
tively, and stratified 5-fold cross-validation over all 129 historical events yielded Pear-
son correlations of 0.62 for peak flow and 0.84 for flood volume. The Step 2 scheme se-
lection, guided by these prior ranges, improved KGE by 0.023–0.154 for events where the
scheme was updated, with simulated peak flow and flood volume falling within the prior
judgment ranges for 14 and 13 out of 14 events. All five state-of-the-art LLMs success-
fully executed the full workflow with comparable judgment accuracy, though moderate
performance variation and substantial cost differences emerged across models. Ten re-
peated runs further confirmed the robustness of the skill-constrained judgment, with tightly
clustered prior ranges across all validation events. A notable limitation arose for Type
V floods with weak hydrological signals, where Step 1 misjudgment propagated into Step
2 and degraded the forecast hydrograph, highlighting that prior-judgment accuracy is
a critical prerequisite for the overall forecasting chain.
These results suggest that HydroAgent’s primary contribution lies not in direct nu-
merical prediction, but in the transparent orchestration of expert judgment, physically
based simulation, and human review within an auditable workflow. Rather than replac-
ing hydrological models, HydroAgent formalizes tacit forecaster expertise into operational
skills with explicit boundaries that constrain language model reasoning to complement
physical simulation, offering a viable paradigm for next-generation intelligent flood fore-
casting. Nonetheless, HydroAgent remains a first step toward a fully operational system.
Extending it to multiple basins across different climate regimes, integrating hybrid mod-
–25–

manuscript submitted to AGU Advances
eling with Earth observation data, and enabling continuous case-library updating through
cross-basin retrieval could further strengthen its physical consistency and operational adapt-
ability.
Open Research Statement
The hourly hydrometeorological records used in this study were obtained from the
CAMELSH data set (Tran, 2025), available at https://zenodo.org/records/16763144. Stream-
flow observations for USGS gauge 14194150 (South Yamhill River at McMinnville, Ore-
gon) are publicly available through the USGS National Water Information System (https://waterdata.usgs.gov/).
The research products generated in this study, including processed event data, cal-
ibrated model parameters, benchmark outputs, figures, tables, metadata, schemas, and
figure-reproduction scripts, are openly available at https://github.com/BaoyingShan0/Open-
Research-Data-for-HydroAgent-flood-forecast-paper. This package supports inspection,
auditing, and reproduction of the reported figures and tables, but does not include the
full HydroAgent codebase or the live LLM execution environment needed to fully regen-
erate production benchmark runs.
Conflict of Interest declaration
The authors declare there are no conflicts of interest for this manuscript.
–26–

manuscript submitted to AGU Advances
Acknowledgments
We thank the Hydro90 community for bringing together this group of authors and for
enabling the rapid progress of this work. This work received in-kind computational sup-
port in the form of token credits from Zeta Frontier Technology (Hangzhou) Co., Ltd.
The sponsor had no role in study design, methodology, analysis, interpretation of results,
manuscript writing, or the decision to submit the manuscript.
–27–

manuscript submitted to AGU Advances
References
Alfieri, L., Burek, P., Dutra, E., Krzeminski, B., Muraro, D., Thielen, J., & Pappen-
berger, F.
(2013).
Glofas–global ensemble streamflow forecasting and flood
early warning. Hydrology and Earth System Sciences, 17(3), 1161–1175.
Allen, M. R., & Ingram, W. J. (2002). Constraints on future changes in climate and
the hydrologic cycle. Nature, 419(6903), 224–232.
Apel, H., Aronica, G. T., Kreibich, H., & Thieken, A. H.
(2009).
Flood risk
analyses–how detailed do we need to be?
Natural Hazards, 49(1), 79–98.
doi: 10.1007/s11069-008-9277-8
Bhasme, P., Vagadiya, J., & Bhatia, U.
(2022).
Enhancing predictive skills in
physically-consistent way: Physics informed machine learning for hydrological
processes. Journal of Hydrology, 615, 128618.
Bindas, T., Tsai, W.-P., Liu, J., Rahmani, F., Feng, D., Bian, Y., . . . Shen, C.
(2024).
Improving river routing using a differentiable muskingum-cunge model
and physics-informed machine learning.
Water Resources Research, 60(1),
e2023WR035337.
Boiko, D. A., MacKnight, R., Kline, B., & Gomes, G. (2023). Autonomous chemical
research with large language models. Nature, 624(7992), 570–578.
Boyle, D. P., Gupta, H. V., & Sorooshian, S.
(2000).
Toward improved calibra-
tion of hydrologic models: Combining the strengths of manual and automatic
methods. Water Resources Research, 36(12), 3663–3674.
Breinl, K., Lun, D., M¨uller-Thomy, H., & Bl¨oschl, G.
(2021).
Understanding
the relationship between rainfall and flood probabilities through combined
intensity-duration-frequency analysis. Journal of Hydrology, 602, 126759.
Cai, Y., Hao, Y., Zhou, J., Yan, H., Lei, Z., Zhen, R., . . . He, L.
(n.d.).
Building
Self-Evolving Agents via Experience-Driven Lifelong Learning: A Frame-
work and Benchmark.
Retrieved 2026-05-23, from http://arxiv.org/abs/
2508.19005 doi: 10.48550/arXiv.2508.19005
Clark, M. P., Slater, A. G., Rupp, D. E., Woods, R. A., Vrugt, J. A., Gupta, H. V.,
. . . Hay, L. E.
(2008).
Framework for understanding structural errors (fuse):
A modular framework to diagnose differences between hydrological models.
Water Resources Research, 44(12).
Cloke, H. L., & Pappenberger, F.
(2009).
Ensemble flood forecasting: A review.
–28–

manuscript submitted to AGU Advances
Journal of hydrology, 375(3-4), 613–626.
De la Fuente, L. A., Ehsani, M. R., Gupta, H. V., & Condon, L. E.
(2023).
To-
wards interpretable lstm-based modelling of hydrological systems.
Hydrology
and Earth System Sciences Discussions, 2023, 1–36.
Demeritt, D., Nobert, S., Cloke, H. L., & Pappenberger, F.
(2013).
The european
flood alert system and the communication, perception, and use of ensemble
predictions for operational flood risk management.
Hydrological Processes,
27(1), 147–157.
Dong, N., Hao, H., Yang, M., Wei, J., Xu, S., & Kunstmann, H.
(2025).
Deep-
learning-based sub-seasonal precipitation and streamflow ensemble forecasting
over the source region of the yangtze river.
Hydrology and Earth System Sci-
ences, 29(8), 2023–2042.
Emerton, R. E., Stephens, E. M., Pappenberger, F., Pagano, T. C., Weerts, A. H.,
Wood, A. W., . . . others (2016). Continental and global scale flood forecasting
systems. Wiley Interdisciplinary Reviews: Water, 3(3), 391–418.
Entekhabi, D., Njoku, E. G., O’Neill, P. E., Kellogg, K. H., Crow, W. T., Edelstein,
W. N., . . . Van Zyl, J. (2010). The soil moisture active passive (smap) mission.
Proceedings of the IEEE, 98(5), 704–716. doi: 10.1109/JPROC.2010.2043918
Feng, D., Liu, J., Lawson, K., & Shen, C.
(2022).
Differentiable, learnable, re-
gionalized process-based models with multiphysical outputs can approach
state-of-the-art hydrologic prediction accuracy.
Water Resources Research,
58(10), e2022WR032404.
Fraehr, N., Wang, Q. J., Wu, W., & Nathan, R.
(2023).
Supercharging hydrody-
namic inundation models for instant flood insight.
Nature Water, 1(10), 835–
843.
Frame, J. M., Kratzert, F., Klotz, D., Gauch, M., Shalev, G., Gilon, O., . . . Nearing,
G. S.
(2022).
Deep learning rainfall–runoff predictions of extreme events.
Hydrology and Earth System Sciences, 26, 3377–3392.
Gauch, M., Kratzert, F., Gilon, O., Gupta, H., Mai, J., Nearing, G., . . . Klotz, D.
(2023).
In defense of metrics: Metrics sufficiently encode typical human pref-
erences regarding hydrological model performance.
Water Resources Research,
59(6), e2022WR033918.
Guan, Y., Gu, X., Slater, L. J., Li, X., Li, J., Wang, L., . . . Zhang, X.
(2024).
–29–

manuscript submitted to AGU Advances
Human-induced intensification of terrestrial water cycle in dry regions of the
globe. npj Climate and Atmospheric Science, 7(1), 45.
He, G., Luo, J., Luo, F., Yang, X., Jing, X., & Cui, H.
(2025).
Iwms-llm: an intel-
ligent water resources management system based on large language models.
Journal of Hydroinformatics.
Jadidoleslam, N., Mantilla, R., & Krajewski, W. F.
(2021).
Data assimilation of
satellite-based soil moisture into a distributed hydrological model for stream-
flow predictions. Hydrology, 8(1), 52.
Jain, S. K., Shilpa, L., Rani, D., & Sudheer, K. (2023). State-of-the-art review: Op-
eration of multi-purpose reservoirs during flood season.
Journal of Hydrology,
618, 129165.
Jia, T., Chen, G., Li, Y., Chang, X., & Ehret, U.
(2026).
Streamflow prediction in
data-scarce regions with semi-supervised deep learning.
EGUsphere, 2026, 1–
37.
Jia, T., Qin, H., Yan, D., Zhang, Z., Liu, B., Li, C., . . . Zhou, J. (2019). Short-term
multi-objective optimal operation of reservoirs to maximize the benefits of
hydropower and navigation. Water, 11(6), 1272.
Kim, H., & Villarini, G.
(2024).
Higher emissions scenarios lead to more extreme
flooding in the united states. Nature communications, 15(1), 237.
Kirchner, J. W.
(2006).
Getting the right answers for the right reasons: Linking
measurements, analyses, and models to advance the science of hydrology.
Wa-
ter resources research, 42(3).
Kratzert, F., Klotz, D., Brenner, C., Schulz, K., & Herrnegger, M. (2018a). Rainfall–
runoff modelling using long short-term memory (lstm) networks.
Hydrology
and Earth System Sciences, 22, 6005–6022.
Kratzert, F., Klotz, D., Brenner, C., Schulz, K., & Herrnegger, M. (2018b). Rainfall–
runoff modelling using long short-term memory (lstm) networks.
Hydrology
and Earth System Sciences, 22(11), 6005–6022.
LaDue, D. S., & Cohen, A. E.
(2018).
Facilitating the self-directed learning efforts
of professional meteorologists. Bulletin of the American Meteorological Society,
99(12), 2519–2527.
Lam, R., Sanchez-Gonzalez, A., Willson, M., Wirnsberger, P., Fortunato, M., Alet,
F., . . . others (2023). Learning skillful medium-range global weather forecast-
–30–

manuscript submitted to AGU Advances
ing. Science, 382(6677), 1416–1421.
Li, X., Chen, W., Liu, Y., Zheng, S., Chen, X., He, Y., . . . others
(2026).
Skills-
bench: Benchmarking how well agent skills work across diverse tasks.
arXiv
preprint arXiv:2602.12670.
Li, Y., Grimaldi, S., Walker, J. P., & Pauwels, V. R.
(2016).
Application of re-
mote sensing data to constrain operational rainfall-driven flood forecasting: A
review. Remote Sensing, 8(6), 456.
Ling, G., Zhong, S., & Huang, R.
(2026).
Agent skills: A data-driven analysis of
claude skills for extending large language model functionality.
arXiv preprint
arXiv:2602.08004.
Luo, W., Zhang, F., Wang, L., Hu, S., Xu, B., & Zhao, J.
(2025).
Improving llm-
assisted hydropower operation through data query enhanced agent. In Interna-
tional hydropower development conference (pp. 551–567).
McEachran, Z., Ghosh, R., Renganathan, A., Sharma, S., Lindsay, K., Steinbach,
M., . . . Kumar, V. (2025). Knowledge-guided machine learning for operational
flood forecasting. Water Resources Research, 61(11), e2024WR039064.
McEachran, Z. P., Kietzmann, J., & Johnston, M. (2024). Parsimonious streamflow
forecasting system based on a dynamical systems approach. Journal of Hydrol-
ogy, 641, 131776.
Merz, B., Bl¨oschl, G., Vorogushyn, S., Dottori, F., Aerts, J. C., Bates, P., . . . others
(2021). Causes, impacts and patterns of disastrous river floods. Nature Reviews
Earth & Environment, 2(9), 592–609.
Najafi, H., Shrestha, P. K., Rakovec, O., Apel, H., Vorogushyn, S., Kumar, R., . . .
Samaniego, L.
(2024).
High-resolution impact-based early warning system for
riverine flooding. Nature communications, 15(1), 3726.
Nearing, G., Cohen, D., Dube, V., Gauch, M., Gilon, O., Harrigan, S., . . . others
(2024).
Global prediction of extreme floods in ungauged watersheds.
Nature,
627(8004), 559–563.
Nearing, G. S., Kratzert, F., Sampson, A. K., Pelissier, C. S., Klotz, D., Frame,
J. M., . . . Gupta, H. V.
(2021).
What role does hydrological science
play in the age of machine learning?
Water Resources Research, 57(3),
e2020WR028091.
Nevo, S., Morin, E., Gerzi Rosenthal, A., Metzger, A., Barshai, C., Weitzner, D., . . .
–31–

manuscript submitted to AGU Advances
others
(2022).
Flood forecasting with machine learning models in an opera-
tional framework. Hydrology and Earth System Sciences, 26(15), 4013–4032.
Pagano, T. C., Pappenberger, F., Wood, A. W., Ramos, M.-H., Persson, A., & An-
derson, B.
(2016).
Automation and human expertise in operational river
forecasting. Wiley Interdisciplinary Reviews: Water, 3(5), 692–705.
Pursnani, V., Ramirez, C. E., Sermet, Y., & Demir, I. (2024). Hydrosuite-ai: Facili-
tating hydrological research with llm-driven code assistance. EarthArXiv.
Ramirez, C. E., & Demir, I. (2024). Ai-assisted voice enabled computing framework
for hydrological analysis. EarthArXiv.
Read, J. S., Jia, X., Willard, J., Appling, A. P., Zwart, J. A., Oliver, S. K., . . . oth-
ers (2019). Process-guided deep learning predictions of lake water temperature.
Water Resources Research, 55(11), 9173–9190.
Reichle, R. H., De Lannoy, G. J. M., Liu, Q., Koster, R. D., Kimball, J. S., Crow,
W. T., . . . Smith, E. B. (2017). Global assessment of the smap level-4 surface
and root-zone soil moisture product using assimilation diagnostics.
Journal of
Hydrometeorology, 18(12), 3217–3237. doi: 10.1175/JHM-D-17-0130.1
Reichstein, M., Camps-Valls, G., Stevens, B., Jung, M., Denzler, J., Carvalhais, N.,
& Prabhat, F.
(2019).
Deep learning and process understanding for data-
driven earth system science. Nature, 566(7743), 195–204.
Roy, A., Kasiviswanathan, K., Patidar, S., Adeloye, A. J., Soundharajan, B.-S., &
Ojha, C. S. P. (2023). A novel physics-aware machine learning-based dynamic
error correction model for improving streamflow forecast accuracy.
Water
Resources Research, 59(2), e2022WR033318.
Rudin, C. (2019). Stop explaining black box machine learning models for high stakes
decisions and use interpretable models instead.
Nature machine intelligence,
1(5), 206–215.
Shan, X., Steele-Dunne, S., Hahn, S., Wagner, W., Bonan, B., Albergel, C., . . . Ku,
O.
(2024).
Assimilating ascat normalized backscatter and slope into the land
surface model isba-a-gs using a deep neural network as the observation op-
erator: Case studies at ismn stations in western europe.
Remote Sensing of
Environment, 308, 114167.
Shen, C., Appling, A. P., Gentine, P., Bandai, T., Gupta, H., Tartakovsky, A., . . .
others (2023). Differentiable modelling to unify machine learning and physical
–32–

manuscript submitted to AGU Advances
models for geosciences. Nature Reviews Earth & Environment, 4(8), 552–567.
Singhal, K., Azizi, S., Tu, T., Mahdavi, S. S., Wei, J., Chung, H. W., . . . others
(2023).
Large language models encode clinical knowledge.
Nature, 620(7972),
172–180.
Stuart, N. A., Hartfield, G., Schultz, D. M., Wilson, K., West, G., Hoffman, R.,
. . . others
(2022).
The evolving role of humans in weather prediction and
communication.
Bulletin of the American Meteorological Society, 103(8),
E1720–E1746.
Su, W., Long, J., Ai, Q., Tang, Y., Wang, C., Tu, Y., & Liu, Y.
(2026).
Skill re-
trieval augmentation for agentic ai. arXiv preprint arXiv:2604.24594.
Sun, A. Y., Jiang, P., Mudunuru, M. K., & Chen, X.
(2021).
Explore spatio-
temporal learning of large sample hydrology using graph neural networks.
Water Resources Research, 57(12), e2021WR030394.
Tolson, B. A., & Shoemaker, C. A.
(2007).
Dynamically dimensioned search al-
gorithm for computationally efficient watershed model calibration.
Water Re-
sources Research, 43(1), W01413.
Tran, V. N.
(2025).
Camelsh: A large-sample hourly hydrometeorological dataset
and attributes at watershed-scale for contiguous united states.
Zenodo.
Re-
trieved from https://zenodo.org/records/16763144
doi: 10.5281/zenodo
.16763144
Tran, V. N., Xu, D., Le, P., Kim, J., Van Nguyen, T., Nguyen, G. T., . . . Ivanov,
V. Y.
(2026).
The value of forecasters-in-the-loop in real-time flood fore-
casting in the age of machine learning.
Geophysical Research Letters, 53(8),
e2025GL118317.
Tran, V. N., Xu, D., Nguyen, T. V., Kim, T., Ivanov, V. Y., et al.
(2025).
CAMELSH: A large-sample hourly hydrometeorological dataset and at-
tributes at watershed-scale for conus.
Scientific Data, 12, 1307.
doi:
10.1038/s41597-025-05612-6
Watson, P. A.
(2022).
Machine learning applications for weather and climate need
greater focus on extremes. Environmental Research Letters, 17(11), 111004.
Wu, Y., Li, T.-L., & Liu, H.
(2026).
Behavioral integrity verification for ai agent
skills. Retrieved from https://arxiv.org/abs/2605.11770
Xiang, Z., Yan, J., & Demir, I.
(2020).
A rainfall-runoff model with lstm-
–33–

manuscript submitted to AGU Advances
based sequence-to-sequence learning.
Water resources research, 56(1),
e2019WR025326.
Yan, S., Li, Z., Zhu, S., Wen, Y., Zhang, M., Chen, M., . . . Hong, Y. (2025). Aquah:
Automatic quantification and unified agent in hydrology.
In Proceedings of the
ieee/cvf international conference on computer vision workshops (iccvw).
Yan, S., Ma, Z., Li, X., Hu, H., Xu, J., Ji, Q., & Weng, F.
(2023).
Pcssr-dnnwa: A
physical constraints based surface snowfall rate retrieval algorithm using deep
neural networks with attention module. Geophysical Research Letters, 50(13).
Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y.
(2022).
React: Synergizing reasoning and acting in language models.
Retrieved from
https://arxiv.org/abs/2210.03629
Yin, H., Guo, Z., Zhang, X., Chen, J., & Zhang, Y.
(2022).
Rr-former: Rainfall-
runoff modeling based on transformer. Journal of Hydrology, 609, 127781.
Zhang, S., Wen, X., Yang, J., Wen, Z., Liu, F., Han, B., . . . Tan, M.
(n.d.).
Next-
token gradient sensitivity probing for llm hallucination detection.
Zhang, Z., Fischer, E., Zscheischler, J., & Engelke, S.
(2026).
Physics-based mod-
els outperform ai weather forecasts of record-breaking extremes.
Science Ad-
vances, 12(18), eaec1433.
Zhao, R.-J.
(1992).
The xinanjiang model applied in china.
Journal of hydrology,
135(1-4), 371–381.
Zhou, Y., Matyas, C., Liu, P., & Li, H.
(2025).
Identification of tropical cyclone–
related flash floods from hazard narratives using a large language model–based
approach. npj Natural Hazards, 2(1), 104.
Zhu, Z., Tang, Y., Tang, X., Zhang, J., Gao, C., Zhang, S., . . . Guan, T.
(2026).
Large language models as calibration agents in hydrological modeling: Feasibil-
ity and limitations. Geophysical Research Letters, 53(2), e2025GL120043.
References From the Supporting Information
Gong, J., Liu, X., Yao, C., Li, Z., Weerts, A. H., Li, Q., Bastola, S., Huang, Y., & Xu,
J. (2025). State updating of the Xin’anjiang model: Joint assimilating streamflow and
multi-source soil moisture data via the asynchronous ensemble Kalman filter with en-
hanced error models. Hydrology and Earth System Sciences, 29, 335–360. https://doi
.org/10.5194/hess-29-335-2025
–34–

manuscript submitted to AGU Advances
Luo, Y., Zhou, Y., Xu, H., Chen, H., Chang, F.-J., & Xu, C.-Y. (2024). Enhancing physically-
based flood forecasts through fusion of long short-term memory neural network with un-
scented Kalman filter. Journal of Hydrology, 641, 131819. https://doi.org/10.1016/
j.jhydrol.2024.131819
Wang, Y., Liu, W., Zhu, F., Xu, B., Li, W., Tong, J., & Zhong, P.-a. (2025). Modeling
the cumulative impact of minor impoundments on watershed hydrology: Enhancements
to the Xin’anjiang model. Journal of Hydrology, 660, 133399. https://doi.org/10.1016/
j.jhydrol.2025.133399
–35–
