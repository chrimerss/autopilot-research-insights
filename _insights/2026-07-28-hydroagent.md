---
subject: Machine Learning / AI Agents
subject_slug: ml-ai
topic: 'HydroAgent: Skill-Orchestrated LLM Workflows for Operational Flood Forecasting'
date: '2026-07-28'
title: 'HydroAgent: Formalizing Forecaster Expertise into Skill-Orchestrated Flood
  Forecasting Workflows'
authors: Qingyi Yang; Siqian Qiu; Bing Li; Xu Shan; Jia Feng; Shunan Zhou; Xudong
  Zhou; Tiantian Xing; Jiale Guo; Xiaoyi Dong; Gaoyu Liu; Xiaohuan Liu; Haiqing Pu;
  Qingwen Deng; Xun Zhang; Zhongrun Xiang; Haiyang Qian; Ying Yan; Yongkang Xu; Nuo
  Lei; Tianlong Jia; Baoying Shan; Carlo De Michele
year: '2026'
venue: ''
link: arXiv:2607.23983v1
figure: /assets/figures/hydroagent/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/HydroAgent/HydroAgent.pdf
---

## Summary & Key Contributions

**Core idea.** HydroAgent embeds LLMs into a physically grounded, five-step flood-forecasting workflow (scheme preparation, scenario judgment, scheme selection, rolling forecasting, warning bulletin) using a three-layer separation: a *skill layer* (what to do), an *LLM layer* (how to reason), and a *tool layer* (deterministic computation). The design principle is that the LLM never computes hydrological quantities or validates its own numerical output.

**Key contributions.**
- First skill-orchestrated agent framework that formalizes tacit forecaster *prior judgment* (Step 1) as an auditable, reproducible, contract-bound (`judgment.json`/`report.md`) procedure, with explicit human-review gates after Steps 1-3.
- A six-dimensional weighted analog-retrieval scheme (13-point similarity over total rainfall, duration, soil moisture, event type, max short-duration rainfall, initial flow) plus expert-rule correction and a physical red-line validator (runoff coefficient R in [0.05, 1.1], peak > initial discharge).
- Empirical validation on the South Yamhill River basin (USGS 14194150) using CAMELSH hourly data: prior judgment captures observed peak/volume within 5% in 10/14 and 11/14 events; 5-fold CV over 129 events yields Pearson r = 0.62 (peak) and 0.84 (volume). Guided XAJ scheme selection improves KGE by 0.023-0.154 over a strong baseline (avg KGE 0.890).
- Cross-LLM benchmark of five frontier models (DeepSeek-v3.2, Qwen-3.6-plus, GPT-5.4, Gemini-3.1-pro, Claude-opus-4.6) showing comparable accuracy (40-80% hit rates) but >10x cost dispersion, plus within-model stability (10 repeats) showing skill constraints bound LLM sampling stochasticity.

## Connections to My Work

This paper sits squarely at the intersection of my hydrologic-modeling and AI-agent work. Most directly it is a sibling to my **"HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL"** - both use the *HydroAgent* name and target LLM-driven hydrologic decision-making, but mine uses simulator-grounded RL to close the calibration gap while this paper uses statically authored skills plus deterministic tools with human gates; the two suggest a natural convergence (RL-refined skills). It also connects to my agent-architecture work **"AI Agent for Hydrologic Modeling: Definition, Development and Application"** and **"AQUAH: Automatic Quantification and Unified Agent in Hydrology"**, which define the LLM-orchestrator-plus-hydrologic-tool pattern instantiated here for flood warning. The XAJ + DDS calibration backbone resonates with **"Conus-wide model calibration and validation for CRESTv3.0 - An improved Coupled Routing and Excess STorage distributed hydrological model"** and the review **"A decadal review of the CREST model family: Developments, applications, and outlook"**. Their warning-bulletin/return-period step and Oregon focus link to **"A multi-source 120-year US flood database with a unified common format and public access"** and **"Spatiotemporal Characteristics of US Floods: Current Status and Forecast Under a Future Warmer Climate"**. Their interpretability framing echoes my **"Advancing Satellite Precipitation Retrievals With Data Driven Approaches: Is Black Box Model Explainable?"**

## Critique & Limitations

- **Single-basin, retrospective validation.** All quantitative results come from one humid basin (South Yamhill) chosen because it matches XAJ assumptions (saturation-excess, no snow, no reservoir regulation). Transferability is asserted, not demonstrated.
- **Small validation set with confounded exclusions.** Only 14 held-out events (2020-2024), 2 excluded post hoc. The headline 5%-tolerance hit rate is applied to interval midpoints and to whether observations fall in intervals, but interval width is a tunable degree of freedom, so hit rate can be inflated by widening ranges. No proper scoring rule (CRPS, interval score) or reliability/calibration analysis.
- **Tail failure is systematic.** Type I (largest) floods have the worst hit rates (27-53%) and the 1996 extreme (1326 m3/s) is badly underestimated - exactly the events that matter most. Case retrieval structurally cannot extrapolate beyond its library, and 'controlled extrapolation' is under-specified.
- **The LLM's marginal value is unclear.** Retrieval + expert rules + physical red-lines do most of the constraining, and all five LLMs perform comparably, yet the key ablation is missing: how does a deterministic (non-LLM) analog-weighting baseline perform? Without it, the paper cannot show the LLM adds skill beyond structured retrieval.
- **Uncertainty only partially quantified** (acknowledged). Meteorological forcing, parameter, and structural uncertainty are unaddressed; the single XAJ structure likely dominates error.
- **Reproducibility caveat.** The released package excludes the full codebase and live LLM execution environment, so production benchmarks cannot be regenerated.

## Gaps & Ideas

- **Deterministic-vs-LLM ablation.** Quantify incremental skill of LLM reasoning over a pure weighted-analog/kNN baseline and a small tabular ML model - the single most important missing experiment.
- **Tail-event handling.** Couple HydroAgent with a regional LSTM (trained across many CAMELSH basins) as a fallback when the target event lies outside the case-library support; let the LLM route to LSTM vs XAJ vs defer-to-human based on retrieval confidence.
- **Proper uncertainty quantification.** Replace point-interval hit rates with ensemble forecasting (multiple forcings x multiple hydrologic structures) scored by CRPS/interval score and reliability diagrams.
- **Data assimilation.** Ingest SMAP surface/root-zone soil moisture and satellite-derived inundation/discharge to update the event description and constrain the rolling forecast (Step 3).
- **Hallucination diagnostics.** Add next-token gradient-sensitivity or self-consistency checks at the scenario-parsing stage where the LLM extracts structured variables from free text.
- **Cross-basin skill transfer.** Test whether skills authored for one basin degrade gracefully, and whether a shared versioned hydrology skill library generalizes across climate regimes.

## How to Advance / Disrupt the Field

**Goal:** turn HydroAgent from a single-basin, retrospective, interval-hit demonstrator into a benchmarked, uncertainty-aware, multi-basin operational assistant, and disrupt the LLM-orchestrator paradigm by making the LLM's contribution measurable and learnable.

**Recommended DATA.** (1) CAMELS-US / CAMELSH hourly across 50-200 basins spanning humid, arid, snow-dominated, and regulated regimes to break single-basin dependence and stress Type-I tails. (2) SMAP L3/L4 surface + root-zone soil moisture and GPM IMERG V07 precipitation for antecedent-condition and forcing constraints. (3) Sentinel-1/Landsat-derived inundation extents and USGS real-time gauges for Step-3 assimilation and independent validation. (4) A curated record-breaking-event holdout to explicitly test extrapolation.

**Recommended METHODS.** (1) *Ablation-first benchmarking*: a leaderboard comparing (a) deterministic weighted-analog retrieval, (b) regional LSTM, (c) hybrid physics-ML/differentiable models, and (d) LLM-orchestrated HydroAgent, all scored with CRPS, interval score, and reliability diagrams instead of 5% hit rates. (2) *Simulator-grounded RL to refine skills*, bridging this paper with my "HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL" and "AI Agent for Hydrologic Modeling: Definition, Development and Application": let the agent learn when to trust XAJ vs LSTM vs human-defer from simulator reward, replacing static hand-authored rules. (3) *Ensemble UQ*: multi-forcing x multi-structure ensembles (XAJ, CREST-VEC, LSTM, transformer) to decompose forcing/parameter/structural uncertainty. (4) *Assimilation operator*: use SMAP soil moisture as an observation operator to constrain Step-1 priors and Step-3 rolling updates. (5) *Hallucination/interpretability audits*: next-token gradient-sensitivity probing and self-consistency voting at the parsing stage. Releasing an open multi-basin benchmark plus code would establish the community standard this emerging field currently lacks.
