---
subject: Machine Learning / AI Agents
subject_slug: ml-ai
topic: 'GEOID-Flood: Multi-Modal SAR/Optical Flood Segmentation Benchmark'
date: '2026-08-04'
title: 'GEOID-Flood: A Large-Scale Multi-Modal Benchmark Dataset for Flood Segmentation'
authors: Gaetano Chiriaco; Luca Barco; Andrea Bragagnolo; Claudio Rossi; Edoardo Arnaudo
year: '2026'
venue: ''
link: https://arxiv.org/abs/2608.02315
figure: /assets/figures/geoid-flood/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/GEOID-Flood/GEOID-Flood.pdf
---

## Summary & Key Contributions

GEOID-Flood is a large-scale, multi-modal flood segmentation benchmark derived from Copernicus EMS Rapid Mapping activations, spanning **219 events across 65 countries over a decade (2016–2026)** and **~14,282 tiles** at 1024×1024 (10 m GSD). Its distinctive design choices:

- **Bi-temporal, co-registered SAR (Sentinel-1 GRD *and* RTC), pre-event Sentinel-2 composite, and Copernicus GLO-30 DEM** in a single tuple — addressing the fragmentation of prior datasets that offer only one or two sensors.
- A **dedicated permanent-water layer** derived from AlphaEarth Foundations (AEF) annual embeddings via a lightweight MLP decoder, enabling separation of *transient flooding* from *permanent water* — a distinction most flood datasets omit.
- **Event-level, continent-stratified, spatially-non-leaking splits** plus a temporally disjoint held-out set (post-Jan 2026) for honest cross-dataset generalization tests.
- A **reproducible benchmark** across four RQs: (RQ1) foundation vs. conventional encoders; (RQ2) temporal modeling vs. post-hoc water differencing; (RQ3) modality contributions; (RQ4) transfer to unseen events.

**Key findings:** foundation models (TerraMind, DOFA, OlmoEarth) offer only a *modest, consistent* edge over ImageNet encoders (binary IoU clustered 0.844–0.884); end-to-end optical–SAR *fusion with finetuning* best resolves transient flooding (IoU_flood up to 0.521); GRD marginally beats RTC and DEM adds negligible gain; and models trained on GEOID-Flood transfer better to unseen 2026 events than those trained on Kuro Siwo, MMFlood, WorldFloods v2, or Sen1Floods11.

## Connections to My Work

This benchmark sits squarely at the intersection of my flood-inundation and ML-for-geoscience work. Most directly, it parallels **"FloodSimBench: A Benchmark Dataset for Training Foundational Flood Inundation Models"** — both are large-scale benchmarks built to test whether foundation-model-style representations transfer across flood events, though FloodSimBench targets physically-based *inundation depth/extent* simulation whereas GEOID-Flood targets *observed* SAR/optical segmentation. A fusion of the two framings (simulated hydrodynamics as prior + observed SAR as constraint) is natural.

My **"A multi-source 120-year US flood database with a unified common format and public access"** and **"CREST-iMAP v1.0: A fully coupled hydrologic-hydraulic modeling framework dedicated to flood inundation mapping and prediction"** / **"A Comprehensive Flood Inundation Mapping for Hurricane Harvey Using an Integrated Hydrological and Hydraulic Model"** work shares the concern that inconsistent formats and event-level heterogeneity confound cross-study comparison — GEOID-Flood's standardized SAR normalization (GRD+RTC) and event-level splits are exactly the kind of unification I argued for. The permanent-water-vs-flood-water separation is also the operational heart of **"Can re-infiltration process be ignored for flood inundation mapping and prediction during extreme storms? A case study in Texas Gulf Coast region"**, where distinguishing standing floodwater from baseline hydrography drives accuracy.

Methodologically, the use of foundation-model encoders relates to **"Rapid Flood Inundation Forecast Using Fourier Neural Operator"** and my agentic ML work (**"AQUAH: Automatic Quantification and Unified Agent in Hydrology"**, **"HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL"**) — GEOID-Flood provides a clean labeled target that such surrogate/agent systems could be evaluated against or coupled with. Finally, the SAR focus connects to my remote-sensing lineage (**"Joint Collaboration on Comparing NOAA's Ground-Based Weather Radar and NASA-JAXA's Spaceborne Radar"**), where sensor-processing conventions and radiometric normalization dominate downstream error.

## Critique & Limitations

- **Permanent-water labels are model-derived (AEF-MLP), not independently observed.** The authors themselves flag that the cross-dataset comparison is scored against GEOID-Flood's own labels, so the binary-water transfer advantage is *partly circular*. Anchoring claims on binary water where conventions converge is honest, but the flood-class superiority still leans on labels that inherit the AEF decoder's biases.
- **Geographic skew toward Europe (140 of 219 events).** Continent-stratified sampling helps balance *splits*, but cannot manufacture representativeness the source catalog lacks — tropical/monsoonal flash-flood regimes (South Asia, Sahel) remain under-sampled, precisely where flood impact is highest.
- **CEMS delineation as ground truth carries residual noise.** Rapid Mapping products are operational products, not gold-standard field validation; flash-flood acquisition-to-delineation gaps are acknowledged as a filtering pain point, implying survivorship bias toward slower, well-mapped events.
- **No post-event Sentinel-2** (justified by cloud cover) means optical context can only inform the *pre-event* baseline — the fusion gains are about better change reference, not observing the flood optically. This limits generality of the 'optical–SAR fusion wins' conclusion.
- **Modest foundation-model edge may reflect the decoder/protocol, not the encoders.** With a strong shared U-Net decoder and adequate finetuning, the encoder is 'not the bottleneck' — but this could equally mean the *task* (binary water) is too easy to discriminate encoders, while the harder flood class (IoU_flood ~0.48–0.52) never gets a purpose-built architecture beyond generic fusion.
- **No hydrological/topographic reasoning.** DEM 'adds no measurable gain,' but the ablation feeds raw elevation, not hydrologically-informed features (HAND, flow accumulation, slope), which is a missed opportunity given how central terrain is to inundation physics.

## Gaps & Ideas

- **Hydrologically-conditioned inputs.** Replace raw DEM with **Height Above Nearest Drainage (HAND), flow accumulation, and slope**; the finding that 'DEM adds no gain' likely reflects poor feature engineering, not irrelevance of terrain. Floodwater cannot climb hills — a physics-aware prior should sharpen the flood/permanent-water boundary.
- **Independent label validation.** Couple the AEF-derived permanent-water layer with an orthogonal reference (e.g., high-water-occurrence JRC-GSW masks reconciled with OSM + a held-out hand-labeled subset) to break the circularity in cross-dataset scoring.
- **Physics-ML coupling.** Use a hydrodynamic model (CREST-iMAP-style) to generate *simulated inundation priors* per event, then treat SAR segmentation as a data-assimilation/correction problem — bridging my simulation work with this observational benchmark.
- **Flash-flood stress subset.** Explicitly curate the hard, temporally-misaligned flash-flood cases the pipeline currently discards, as a diagnostic split; these are the operationally critical, worst-transfer scenarios.
- **Agentic evaluation.** An LLM-agent (à la AQUAH/HydroAgent) could orchestrate model/modality selection per event context (cloud state, sensor availability, terrain), automating the RQ3 modality-selection insight into a deployable pipeline.
- **Depth/volume beyond extent.** Extent segmentation ignores inundation depth — the highest-impact hydrologic quantity. A multi-task head predicting extent + depth (supervised by hydrodynamic simulation or gauge cross-sections) would greatly increase downstream value.

## How to Advance / Disrupt the Field

**Goal: turn GEOID-Flood from an extent-segmentation benchmark into a physics-grounded, globally-representative *flood impact* benchmark and modeling stack.**

**Data to add:**
- **Hydrologic covariates:** HAND, flow accumulation, slope, and channel network derived from GLO-30 (and MERIT-Hydro) — replacing/augmenting the raw DEM layer.
- **Simulated inundation priors:** per-event CREST-iMAP / hydrodynamic runs forced by IMERG V07 precipitation (leveraging my IMERG evaluation work) to provide physics-consistent floodwater probability maps as an extra input channel.
- **Geographic rebalancing corpus:** targeted ingestion of tropical/monsoonal CEMS + UNOSAT + Dartmouth Flood Observatory events to counter the Europe skew, plus a small hand-labeled field-validated subset for unbiased scoring.
- **Depth references:** gauge/rating-curve and LiDAR-derived water-surface elevations where available, to enable a depth-prediction target.

**Methods:**
1. **Physics-informed fusion architecture:** extend the mid-fusion TerraMind-B design with a *hydrologic branch* (HAND/flow-accumulation encoder) whose features constrain the flood class — a soft physical prior that penalizes floodwater on steep, high-HAND terrain. Train with a topographically-weighted loss.
2. **Neural-operator surrogate coupling:** use a **Fourier Neural Operator** (as in my ICCVW flood-forecast work) to propagate the simulated inundation prior forward in time, and use SAR segmentation as an observational correction (differentiable data assimilation), yielding *forecast* rather than *nowcast* flood maps.
3. **Agentic orchestration:** an LLM-driven controller (AQUAH/HydroAgent lineage) selects modality stack and fusion strategy per event based on cloud state, sensor availability, and terrain regime — operationalizing the paper's RQ3 finding.
4. **Honest generalization protocol:** score transfer only on *independently-validated* flood extent and (where available) depth, breaking the label-derivation circularity the authors correctly flagged.

**Disruptive framing:** the paper's headline is 'training design matters more than the encoder.' The real leap is 'physics + observation matters more than either encoder or training design' — a hybrid hydrodynamic-ML benchmark would reframe flood mapping from a segmentation contest into an assimilation-and-forecast problem with direct societal-impact outputs (depth, affected population, yield loss — echoing **"Severe floods significantly reduce global rice yields"**).
