---
subject: Machine Learning / AI Agents
subject_slug: ml-ai
topic: 'WorldTensor: Harmonised Global Dataset for Earth System Foundation Models'
date: '2026-07-09'
title: A harmonised dataset for Earth system foundation models
authors: Carlos Rodriguez-Pardo; Massimo Tavoni
year: ''
venue: ''
link: doi:10.5281/zenodo.19047618
figure: /assets/figures/earthsystemfoundationmodels/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/EarthSystemFoundationModels/A_harmonised_dataset_for_Earth_system_foundation_models.pdf
---

## Summary & Key Contributions

**Core contribution.** WorldTensor is a harmonised, multimodal global dataset aligning ~757 variable families (658 temporal + 99 static; ~52,823 NetCDF files, ~46 GB) onto a common 0.25° lat–lon grid (matching ERA5) at annual resolution across 14 domains (climate, extremes, air quality, emissions, land use, vegetation, hydrology, cryosphere, ocean, agriculture, energy, human systems, hazards & conflict, static context).

**Key technical moves:** CRS-aware regridding (bilinear/continuous, nearest-neighbour/categorical, conservative area-weighting for fine inputs) with antimeridian-seam and polar-edge handling; rasterisation of point/line/polygon data (power plants, hazards, rivers) into density/count/distance surfaces; annual temporal harmonisation with variable-appropriate statistics and anchor-year interpolation; CF-compliant NetCDF with PyTorch `WorldTensorYearDataset`/`PatchDataset` loaders; and a five-layer validation (physical bounds, land-budget consistency, historical-event detection, semivariogram structure, ICA eco-climatic recovery, RCF/MOSAIKS embedding probes at mean R²=0.63). Framed explicitly as coupled human–Earth research infrastructure for geospatial foundation-model pretraining.

## Connections to My Work

This dataset directly intersects my agenda on **foundation models and coupled human–environment flood systems**. My preprint *"FloodSimBench: A Benchmark Dataset for Training Foundational Flood Inundation Models"* is the flood-domain analogue to WorldTensor's ambition — both aim to standardise heterogeneous geospatial inputs into ML-ready tensors; WorldTensor's static land-surface priors (soil, topography, distance-to-river from HydroRIVERS) and hydrology domain (GRACE, GLDAS, WAD2M) are exactly the covariates FloodSimBench needs for cross-basin transfer. My *"Societal and environmental interconnections: future directions for flood inundation models"* (ERL 2025) argues precisely for co-locating socioeconomic exposure with physical hazard — WorldTensor's human_systems + hazards_and_conflict domains operationalise that call. My *"Severe floods significantly reduce global rice yields"* (Science Advances 2025) coupled crop, hydrology, and flood data manually — WorldTensor's GGCP10 crop production, LUH3 land use, and disaster catalogs on one grid would have collapsed that pipeline. Finally, *"Rapid Flood Inundation Forecast Using Fourier Neural Operator"* and *"HydroAgent"* / *"AQUAH"* point to how such a harmonised tensor could feed neural-operator emulators and LLM-driven hydrologic agents with consistent context layers.

## Critique & Limitations

1. **Annual resolution kills flood/flash-flood utility.** The authors admit sub-annual signals (COVID-19 dip, Pinatubo) are attenuated. For hydrology, annual means erase the event-scale dynamics (peak discharge, flashiness) that matter most — the same limitation I quantified in *"Introducing Flashiness-Intensity-Duration-Frequency (F-IDF)"*. WorldTensor is unusable for inundation or extreme-event work as-is.
2. **Uncertainty is discarded.** SoilGrids quantiles, GRACE measurement-error and scale-factor fields are dropped; only central estimates survive. This is dangerous for downstream ML that should propagate uncertainty, and contradicts best practice from triple-collocation work.
3. **Spurious cross-domain correlations.** The authors themselves warn co-locating point-rasterised data (power plants, conflict) with dense reanalysis on a common grid can induce artificial correlations — a real risk for naive foundation-model training.
4. **0.25° (~28 km) is too coarse** for the flood/urban/exposure use cases the paper advertises; 30 m settlement layers are averaged into meaninglessness.
5. **Validation is shallow.** Only 54 of 757 variable families were bounds-checked; only 3/5 historical events were detected at |z|>1. No held-out downstream task on a real foundation model — the RCF/ICA probes are proxies, not proof of foundation-model value.
6. **License exclusions fragment coverage** (EDGAR fossil CO2 excluded), and temporal coverage is wildly heterogeneous (ocean starts 2010, land use 1900), complicating multi-domain tensor construction.

## Gaps & Ideas

- **Sub-annual companion release.** A monthly/daily tier for hydrology, precipitation, and hazard domains would unlock flood, flash-flood, and event-detection science. My F-IDF and CREST-VEC work needs at least sub-daily forcing.
- **Uncertainty-aware tensors.** Attach per-pixel uncertainty bands (from GRACE, SoilGrids, satellite QA) as parallel channels so downstream models can do heteroscedastic learning — analogous to triple-collocation error characterisation.
- **Multi-resolution / hierarchical grids.** Nest a 1 km flood/urban tier under the 0.25° tier so fine-scale settlement and river networks aren't destroyed.
- **Causal disentanglement layer.** Provide tooling to flag/regularise spurious cross-domain correlations (e.g., decision-tree error attribution as in my *"Disentangling error structures of precipitation datasets using decision trees"*).
- **Agentic access.** An LLM agent (cf. HydroAgent/AQUAH) that automatically selects, subsets, and aligns WorldTensor variables for a user-specified geoscience task would dramatically lower the barrier to use.
- **Benchmark tasks.** Ship curated downstream evaluation tasks (flood inundation, crop-yield anomaly, disaster exposure) so the community can measure real foundation-model transfer, not just RCF probes.

## How to Advance / Disrupt the Field

**Plan: Build a hydrology-native, multi-resolution, uncertainty-aware foundation-model corpus and evaluate it on real coupled human–water tasks.**

*Data.* Extend WorldTensor with (a) a **sub-annual hydrometeorology tier** — IMERG V07 precipitation (validated in my *"How has the latest IMERG V07 improved..."* and *"Evaluation of IMERG climate trends..."*), ERA5-Land daily forcing, and GRACE-FO monthly TWS; (b) a **1 km inundation/exposure tier** from FloodSimBench (my preprint), Sentinel-1/2, and 30 m settlement layers preserved (not averaged); (c) **per-pixel uncertainty channels** from SoilGrids quantiles and GRACE error fields; (d) HydroRIVERS + river-network connectivity as structured graph priors.

*Methods.* (1) Pretrain a **masked-autoencoder / neural-operator hybrid** foundation model on the multi-resolution tensor, using the finite-value masks for missing-modality learning — extending the Fourier Neural Operator approach from my ICCVW 2023 flood paper to a spatiotemporal, multimodal setting. (2) Fine-tune on a **coupled human–water benchmark suite**: flood inundation mapping (CREST-iMAP/CREST-VEC ground truth), global rice-yield-from-flood prediction (Science Advances 2025 labels), and disaster-exposure forecasting. (3) Deploy an **LLM agent (HydroAgent/AQUAH-style) with simulator-grounded RL** to automate variable selection, temporal alignment, and uncertainty propagation from the corpus. (4) Use **decision-tree error attribution** to audit and regularise spurious cross-domain correlations. This disrupts the current 'physics-only weather emulator' paradigm by delivering the first foundation model demonstrably transferable to societally-relevant flood, agriculture, and exposure tasks — the missing evaluation WorldTensor itself does not provide.
