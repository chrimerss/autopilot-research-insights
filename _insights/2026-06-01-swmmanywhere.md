---
subject: Hydrology & Hydrologic Modeling
subject_slug: hydrology
topic: 'SWMManywhere: Global synthetic urban drainage model generation + Sobol sensitivity
  analysis'
date: '2026-06-01'
title: 'SWMManywhere: A workflow for generation and sensitivity analysis of synthetic
  urban drainage models, anywhere'
authors: Barnaby Dobson
year: '2025'
venue: ''
link: https://doi.org/10.1016/j.envsoft.2025.106358
figure: /assets/figures/swmmanywhere/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/SWMManywhere/SWMManywhere.pdf
---

## Summary & Key Contributions

**Core contribution.** SWMManywhere is an open-source, end-to-end Python workflow that synthesizes a fully-described urban drainage model (UDM) — sub-catchments, network topology, and pipe-by-pipe hydraulic design — anywhere on Earth using only open global geospatial datasets (OSM streets/rivers, Google-Microsoft ML-derived building footprints, NASADEM 30 m DEM). Minimal user input is a bounding box; everything else (download, reprojection to UTM, cleaning, simulation in SWMM via PySWMM) is automated.

**Key novelties.**
- Use of a **minimum spanning arborescence (MSA)** (Tarjan 1977) to derive *directed* network topology, which natively incorporates pipe slope (unlike MST-based methods that need post-hoc correction).
- Introduction of **contributing impervious area** as a cost factor in topology derivation (echoing fractal flow-distribution ideas), alongside slope, angle, and length — each with both linear scaling and exponential parameters.
- Adapting Duque et al. (2022)'s pipe-by-pipe hydraulic design with a Rational-Method design flow and a surcharge feasibility constraint.
- Treating **outfall locations as an explicit unknown** (first in UDM synthesis literature).

**Sensitivity analysis.** A large Sobol global SA (18 parameters, 16 metrics, N=38,912 evaluations) across 8 networks (Cran Brook UK + 7 Bellinge DK). Findings: (1) high-quality simulations achievable (NSE > 0.7 for flow and flooding); (2) `node merge distance`, `max street length`, and `river buffer distance` (surface/manhole/outfall controls) are dominant; (3) sensitivity is overwhelmingly through *interactions* (second-order+), not first-order; (4) no globally transferable 'behavioural' parameter values exist, motivating an **uncertainty-/ensemble-driven** philosophy over chasing a single 'correct' UDM.

## Connections to My Work

This paper sits squarely at the intersection of my urban hydrology, flood, and AI-agent threads.

- **Calibration equifinality & uncertainty.** SWMManywhere's central thesis — that the panacea of a single 'correct' model is false and an ensemble/uncertainty-driven approach is needed — is directly relevant to my work on automated, simulator-grounded calibration in *"HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL"*. HydroAgent's RL-over-simulator paradigm could be retargeted at SWMManywhere's 18-dim parameter space to learn behavioural parameter policies that respect interaction structure (which Sobol flagged as dominant).
- **Agentic automation of modeling.** The workflow's CLI/config-file-driven, modular 'graph function' architecture is a natural target for the agent frameworks in *"AQUAH: automatic quantification and unified agent in hydrology"* and *"AI Agent for Hydrologic Modeling: Definition, Development and Application"* — an LLM agent could orchestrate SWMManywhere region selection, data QA, parameter sampling, and result interpretation.
- **Flood inundation foundation models.** SWMManywhere produces pluvial-flooding timeseries globally; this is a potential pipe (pun intended) into the training corpus for *"FloodSimBench: A Benchmark Dataset for Training Foundational Flood Inundation Models"* — synthetic UDMs add the *urban subsurface* component largely missing from surface-only inundation benchmarks, and connect to *"Societal and environmental interconnections: future directions for flood inundation models."*
- **Remote-sensing input quality.** The paper's reliance on NASADEM (30 m) and ML building footprints — and its honest caveat that their quality degrades outside wealthy temperate regions — resonates with my satellite-evaluation work (e.g., *"How has the latest IMERG V07 improved the precipitation estimates and hydrologic utility over CONUS against IMERG V06?"*), since precipitation forcing is flagged as the missing global high-frequency dataset for these models.
- **Environmental justice angle.** The authors note case studies are limited to wealthy European cities; my *"Interweaving Hydrology and Indigenous Knowledge for Flood-related Environmental Justice with the Otoe-Missouria Tribe"* and *"Future heavy rainfall and flood risks for Native Americans under climate and demographic changes"* highlight exactly the underserved, data-sparse regions where global UDM synthesis would be most transformative.

## Critique & Limitations

- **Validation breadth is thin.** Only 8 networks in 2 temperate, wealthy European countries; the authors themselves flag this as a key limitation and report a 'significant paucity of publicly available reliable SWMM models.' Generalization claims to 'anywhere' are therefore largely untested where data quality is worst.
- **No hydraulic structures.** Weirs, orifices, storages, and pumps — established as dominant controls on real UDM behaviour — are entirely omitted, and the real models were *stripped* of these to enable comparison. This biases the comparison favorably and limits realism for combined/large systems.
- **Forcing & roughness fixed.** Precipitation must be user-supplied (no global high-frequency dataset), and Manning's n / depression storage are held constant across networks — both major uncertainty sources are effectively removed rather than analyzed.
- **Second-order indices uninformative.** The most important interaction effects (the paper's own finding that sensitivity is mostly through interactions) could not be quantified because second-order confidence intervals were 'prohibitively large' even at N=38,912 — so the central claim rests partly on inference rather than resolved indices.
- **'Too efficient' networks.** The MSA + pipe-by-pipe design drains too fast (falling limb recedes too quickly), systematically over-sizes diameters, and cannot represent incremental real-world network evolution. The fast-receding hydrograph is a structural artifact, not just parameter mis-tuning.
- **Outfall/comparison protocol is heuristic.** The 'most commonly represented outfall' sub-selection for flow comparison introduces a non-trivial, potentially confounding step that is hard to reproduce or audit.
- **No quantification of input-data error propagation.** OSM/footprint/DEM uncertainty is acknowledged qualitatively but never propagated into the SA — yet it is plausibly the single largest error term globally.

## Gaps & Ideas

- **Input-data uncertainty as first-class SA dimension.** Treat OSM completeness, footprint accuracy, and DEM resolution/error as sampled inputs (not fixed), to learn where data quality — vs. parameters — dominates output variance globally. This directly tests their 'surface elements are most sensitive' claim under realistic data degradation.
- **Learn the parameter–interaction manifold.** Since Sobol couldn't resolve second-order indices, use surrogate / emulator models (Gaussian processes, gradient-boosted trees, or graph neural nets on the street graph) trained on the 38k existing runs to cheaply estimate interaction structure and identify behavioural *regions* rather than point values.
- **Synthesize hydraulic structures from imagery.** Detect weirs/storages from high-res satellite and add pumps as topology-derivation elements — closing the realism gap the authors flag.
- **Global benchmark of synthetic UDMs.** Build a FloodSimBench-style corpus of SWMManywhere-generated UDMs paired with simulated pluvial flooding to pretrain foundation flood models that include subsurface conveyance.
- **Agentic calibration/QA loop.** An LLM agent that inspects downloaded data, flags low-quality OSM regions, proposes parameter ensembles, runs SWMM, and reasons over continuity errors — turning the 'one hypothesis' ensemble philosophy into an automated pipeline.
- **Equity-targeted deployment.** Apply to Indigenous, Global South, and data-sparse communities where below-ground surveys are infeasible — the highest-value use case the paper cannot currently demonstrate.

## How to Advance / Disrupt the Field

**Goal: turn SWMManywhere from a deterministic-per-run workflow into a globally-validated, uncertainty-native, agent-orchestrated urban-flood foundation system.**

**Phase 1 — Resolve the interaction problem with emulators (advance).** DATA: the existing 38,912 SWMManywhere evaluations (Dobson et al. 2024b) plus newly generated runs over 50+ globally diverse cities. METHODS: train a graph-neural-network / gradient-boosted surrogate that maps (street-graph features + 18 parameters + input-data-quality covariates) -> 16 metrics. Use the surrogate to compute Sobol total- and second-order indices at near-zero cost, finally resolving the interaction structure that the original N could not. This replaces brute-force HPC SA with a learned sensitivity model — a methodological disruption to how SA is done on expensive geoscience workflows.

**Phase 2 — Make uncertainty native via simulator-grounded RL (disrupt).** Adapt my *HydroAgent* simulator-grounded RL framework: the policy proposes parameter *ensembles* (not single points), rewarded by multi-metric behavioural coverage and SWMM continuity error, learning to generate plausible-hypothesis UDM ensembles directly. Pair with the AQUAH agent for autonomous region selection, OSM/footprint QA, and natural-language reporting.

**Phase 3 — Foundation flood model integration.** DATA: couple SWMManywhere pluvial-flooding outputs with IMERG V07 precipitation forcing and global DEMs to build a FloodSimBench-style training set that adds *urban subsurface conveyance* — currently absent from surface-only inundation benchmarks. METHODS: pretrain a foundational inundation emulator on synthetic + real UDM pairs, enabling rapid scenario ensembles (climate, urban growth) for cities with no measured drainage network.

**Phase 4 — Equity-driven validation (advance + impact).** DATA: partner with Tribal/Global-South utilities to obtain even a handful of real SWMM models in underrepresented climates and street-data regimes. METHODS: blind validation of synthetic-vs-real performance under degraded input data, propagating OSM/DEM/footprint error explicitly — directly addressing the paper's stated limitation that it cannot yet be trusted outside wealthy temperate regions.

**Net effect:** the field moves from 'generate one synthetic UDM and compare to one real network' to 'generate calibrated, data-quality-aware UDM ensembles anywhere, validate equitably, and feed them into agent-driven foundation flood models.'
