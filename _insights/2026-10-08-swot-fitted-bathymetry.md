---
subject: Floods & Inundation
subject_slug: floods
topic: SWOT-fitted global river bathymetry for hydrodynamic flood models (HyMAP)
date: '2026-10-08'
title: SWOT‐Fitted River Bathymetry for Global Hydrodynamic Models
authors: ''
year: '2023'
venue: ''
link: https://doi.org/10.1029/2026GL125708
figure: /assets/figures/swot-fitted-bathymetry/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/SWOT-fitted-bathymetry/Geophysical
  Research Letters - 2026 - Getirana - SWOT‐Fitted River Bathymetry for Global Hydrodynamic
  Models.pdf
---

## Summary & Key Contributions

**What it does.** Getirana et al. reconcile absolute SWOT river water surface elevation (WSE; RiverSP v2.0, SWORD v16 reaches, Jul 2023–Mar 2025) with the 5-km global HyMAP hydrodynamic model by iteratively adjusting riverbed elevation.

**Method.**
- The SWOT-minus-model mismatch ΔH is decomposed into a geolocation/representativeness bias (b_loc, from fine-DEM elevation differences between the SWOT reach endpoint and the model cell outlet), a systematic sensor/datum bias (b_sen, from mid-Jan to mid-Mar SWOT medians compared to SRTM, which was acquired in Feb 2000), and a residual parameter bias (b_par).
- b_par is added to the bed elevation, subject to a DEM upper bound and a 0.5 m minimum depth.
- Corrections at anchor reaches are linearly interpolated along flow paths, and the model is rerun until the global-median |b_par| is below 0.2 m.

**Key results.**
- Global median |WSE bias| against SWOT falls from 3.10 m to 0.89 m after the first iteration and 0.18 m after the second. About 1.9 m of the improvement comes from removing b_sen and b_loc alone.
- Median correlation is unchanged (0.38). The standard deviation ratio rises slightly (1.07→1.11).
- Independent Hydroweb WSE (16,746 sites, 2015–2025) shows a median Δ|bias| of −0.46 m with no change in correlation or ubKGE. GRDC discharge (2,123 gauges) shows no significant change in global median KGE, RE, r or rstd.
- Against surveyed cross-sections, CONUS MAE drops from 1.55 to 1.29 m, and Brazil MAE from 3.76 to 3.44 m.
- The Nile and Niger profiles show reservoir artifacts.

**Contribution.** A scalable, model-agnostic-in-principle recipe, with a released global bathymetry dataset, for making SWOT absolute WSE usable (rather than anomalies only) in global hydrodynamic models. It also prepares the ground for SWOT WSE data assimilation.

## Connections to My Work

**Flood inundation modeling.** Your CREST-VEC and CREST-iMAP work ("CREST-iMAP v1.0: A fully coupled hydrologic-hydraulic modeling framework dedicated to flood inundation mapping and prediction"; "CREST-VEC: A framework towards more accurate and realistic flood simulation across scales") depends on channel geometry and bed elevation, which this paper identifies as the dominant structural error. SWOT-fitted bed elevations could replace or constrain the channel-geometry parameterization in the CREST-VEC vector routing, especially in large, low-slope rivers.

**Model-error attribution.** The bias partition into b_loc, b_sen and b_par parallels your error-structure work ("Disentangling error structures of precipitation datasets using decision trees"; "Cross-Examination of Similarity, Difference and Deficiency of Gauge, Radar and Satellite Precipitation Measuring Uncertainties..."). Here the same idea is applied to river stage, and ML could be used to learn the decomposition rather than fix it by hand.

**Benchmarks and neural surrogates.** "FloodSimBench: A Benchmark Dataset for Training Foundational Flood Inundation Models" and "Rapid Flood Inundation Forecast Using Fourier Neural Operator" need physically consistent bed elevation and depth fields as inputs and as training targets. This dataset offers a global, observation-anchored source for them. Its documented regional trade-offs also give hard test cases for generalization.

**Calibration agents.** "HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL" and "AI Agent for Hydrologic Modeling: Definition, Development and Application" could automate the iterative fit-rerun-check loop here, including convergence criteria, basin-specific tuning, and flagging reservoir or tidal reaches.

**Large-scale flood trends.** "Spatiotemporal variability of global river extent..." (Gao et al.) and "Spatiotemporal Characteristics of US Floods" would benefit from improved in-channel storage and overbank thresholds.

## Critique & Limitations

**Attribution is assumed, not demonstrated.** After removing b_loc and b_sen, all remaining WSE error is assigned to bed elevation. Width, roughness, runoff bias, rectangular cross-sections and floodplain storage are fixed. The bed therefore absorbs compensating errors. The authors acknowledge this, but the cross-section evidence (Brazil bias only moves from −3.34 to −2.89 m) suggests the fitted bed is often a stage-matching tuning parameter and not true bathymetry.

**Questionable sensor-bias estimate.** b_sen is computed by comparing a Jan–Mar SWOT median (2024–2025) against SRTM (Feb 2000). This conflates SRTM vegetation and canopy penetration error, C-band radar behavior over water, 25 years of channel change and interannual hydrology, and regulation. It is also not clear that it is a pure instrument bias. The ~1.9 m reduction from this step alone is large and receives no uncertainty analysis or sensitivity test.

**Evaluation is circular and narrow.**
- The headline 3.10→0.18 m result is evaluated against the same SWOT data used for fitting, so it is largely a fit residual.
- Independent checks are restricted to reaches that were updated, so the generalization claim is untested elsewhere.
- The two-iteration stopping criterion (ε = 0.2 m) is only loosely justified.
- There is no held-out SWOT cross-validation, such as withholding reaches or time periods.
- Hydroweb and SWOT may share altimetric or datum issues.
- Sparse GRDC coverage, with compensating regional gains and losses, makes the "no change" discharge claim weak, since a zero median can hide real regional degradation.

**Poor skill baseline and high attrition.** A median r of 0.38 at SWOT reaches means the temporal dynamics are poorly simulated to begin with, so "timing preserved" is a weak assurance. Only ~28% of SWOT observations and 78% of reach matches are retained, with no analysis of what is lost (small, braided, tidal or high-latitude rivers).

**Variance inflation and static bed.** The reported ~4% rstd increase is dismissed, yet it is evidence that the correction changes dynamics. A time-invariant bed is fit to a 20-month record, with no treatment of seasonal sediment dynamics.

**Other gaps.** No uncertainty is attached to the bed estimates. The method is evaluated on only one model at 5-km resolution, in which a single outlet-referenced cell elevation represents a heterogeneous reach. Reservoirs, tides and deltas are poorly handled. Linear interpolation along the flow path ignores tributary and slope information. The dataset is released, but the fitted bathymetry's physical validity for flood extent is untested because no inundation or flood-extent evaluation is shown.

## Gaps & Ideas

1. **Uncertainty-aware bathymetry.** Replace the deterministic two-pass fit with an ensemble or Bayesian approach (ensemble smoother or particle-batch fit) that jointly estimates bed, width and roughness, and outputs a bed posterior per reach. Perturb b_sen and b_loc to propagate their uncertainty.
2. **Joint geometry fitting.** SWOT also provides width and slope. Fit bed elevation, width and Manning n against WSE, width and slope together to reduce the aliasing of runoff and width errors into the bed. Test identifiability via synthetic (OSSE) experiments in which the true bed is known.
3. **Learned correction fields.** Train an ML regressor (gradient boosting or a graph neural network on the SWORD river network) to predict bed corrections from drainage area, slope, DEM source, land cover and SWOT residuals. This extends corrections to unobserved reaches and replaces linear interpolation, with spatial block cross-validation.
4. **Held-out inundation validation.** Evaluate flood extent and depth, not just WSE and Q: SWOT pixel cloud and raster, Sentinel-1/2 flood masks, and USGS high-water marks. Compare default and fitted beds in major events such as Harvey 2017 and the 2024 Rio Grande do Sul floods.
5. **Datum and DEM alternatives.** Replace SRTM-based b_sen with FABDEM, Copernicus GLO-30 or ICESat-2/GEDI river-surface profiles. Test whether the b_sen estimate depends on the choice of DEM.
6. **Temporal and operational extension.** Allow seasonally varying effective bed or roughness, handle reservoirs by using SWOT lake products and bathymetry (SWOT lakes, G-REALM) and tide-aware boundary treatment, and evolve toward sequential assimilation, as in Yoon et al. (2026).
7. **Operational use for flood-risk work.** Test whether bias-corrected beds change flood-hazard exposure estimates (for example, the rice-yield and Native American flood-risk analyses), so the downstream value is quantified.

## How to Advance / Disrupt the Field

**Goal.** Turn SWOT bathymetry fitting from a deterministic, HyMAP-specific calibration into a validated, uncertainty-quantified, model-agnostic bathymetry layer. The aim is to show it improves flood inundation in a vector-routed model such as CREST-VEC and to use it to train a global neural flood surrogate.

**Data.**
- SWOT L2 RiverSP/PIXC reach and node products (WSE, width, slope) with SWORD v16 (extend beyond Mar 2025 as new cycles arrive).
- SWOT raster/pixel-cloud water masks and Sentinel-1/2 flood extents for inundation validation.
- MERIT-Hydro, FABDEM and GLO-30 as alternative DEM baselines (b_sen sensitivity), plus ICESat-2 and GEDI river-surface heights.
- Hydroweb/DAHITI altimetry, GRDC, USGS NWIS/NXSDB cross-sections and ANA Brazil as independent data. Hold out at least 20–30% of reaches and the latest months for validation.
- ERA5-Land, GLDAS, MSWEP or IMERG as multiple runoff forcings to test whether the fit is forcing-robust.
- Reservoir and dam data (GRanD/GeoDAR) and tide gauges for boundary handling.

**Methods.**
1. **Synthetic twin experiments.** In CREST-VEC and HyMAP, impose known bed, width and runoff errors and check whether the algorithm recovers the true bed, which tests identifiability and quantifies error aliasing.
2. **Ensemble joint estimation** (iterative ensemble smoother) of bed, width and roughness with SWOT WSE, width and slope as observations, with b_sen/b_loc treated as uncertain nuisance terms.
3. **Graph-based ML prior.** Train a graph neural network on the river network to predict bed corrections from covariates and SWOT residuals, replacing linear interpolation. Use spatial block cross-validation and report uncertainty.
4. **Agentic automation.** Use a HydroAgent-style agent to run the iterate/diagnose/stop loop per basin, with guard-rails for reservoirs, tides and deltas, and with convergence determined by held-out skill rather than fit residual.
5. **Downstream tests.** (a) Compare flood extent and depth against SWOT/Sentinel observations and high-water marks for 5–10 events. (b) Add the fitted bed as a static input to a Fourier-neural-operator or FloodSimBench-trained foundation model and measure gains in stage and extent skill.

**Metrics for success.** Held-out reach WSE bias (not fit-set), flood-extent CSI/F1 and depth RMSE, cross-section MAE and hit rate, discharge KGE decomposed by region (not just global median), and calibration (CRPS/reliability) of the bed uncertainty.

**Why this could disrupt.** If the held-out gains hold, the field moves from treating bathymetry as a static prior to treating it as an evolving, observation-constrained, uncertainty-aware state. That would give global flood models and AI surrogates a physically consistent absolute-elevation foundation, and give your group a distinct contribution at the intersection of SWOT, hydrodynamics and ML.
