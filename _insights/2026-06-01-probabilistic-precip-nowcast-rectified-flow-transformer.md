---
subject: Machine Learning / AI Agents
subject_slug: ml-ai
topic: 'FREUD: Rectified-Flow Transformers for Probabilistic Precipitation Nowcasting'
date: '2026-06-01'
title: Probabilistic Precipitation Nowcasting with Rectified Flow Transformers
authors: Johannes Schusterbauer; Jannik Wiese; Nick Stracke; Timy Phan; Björn Ommer
year: '2026'
venue: ''
link: https://github.com/CompVis/weather-rf
figure: /assets/figures/probabilistic-precip-nowcast-rectified-flow-transformer/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/Probabilistic_precip_nowcast_rectified_flow_transformer/probabilistic_precipitation_nowcasting_with_rectified_flow_transformer.pdf
---

## Summary & Key Contributions

**Core idea.** The paper introduces **FREUD** (Frame-wise Encoder, United Decoder), a two-stage generative nowcasting pipeline that replaces the standard deterministic VAE decoder with a *rectified-flow* (RF) transformer decoder, paired with a latent-space RF transformer for forecasting. Evaluated on the SEVIR VIL benchmark (60-min lead, 12 frames from 13 past frames).

**Key contributions:**
- **Uncertainty-preserving first stage.** A frame-wise transformer encoder (robust to dropped/corrupted radar frames, prevents future→past leakage) plus a *jointly-decoding* hierarchical RF video decoder (Hourglass-DiT style, space-time factorized + neighborhood attention). Because the decoder is generative, multiple reconstructions from the same latent yield **decoding uncertainty** — variance correlates strongly with precipitation intensity (r=0.997 for the proposed regularizer).
- **Stochastic tanh regularization (T-reg).** A loss-free, architecture-light alternative to KL: latents squashed to [−1,1] via tanh and perturbed with small Gaussian noise (σ=0.001). Avoids adversarial/perceptual losses and loss balancing; yields a compact, zero-centered latent space that improves downstream CRPS/SSIM.
- **Masking-based diffusion-forcing (RaMViD) training** for variable-length conditioning and robustness to frame drops; beats full Diffusion Forcing.
- **SOTA on SEVIR**: CRPS 0.0190 (vs CasCast 0.0202, +5.94%), SSIM 0.7841/0.7937, better calibration (reliability index 0.135 vs 0.312), 96%/68% faster encode/decode FLOPs. Scales with model size, ensemble count, and NFE.
- **CFG is flawed for nowcasting**: increasing guidance systematically inflates precipitation independent of conditioning (shown for FREUD and CasCast), conflating localization gains with a distributional shift.

## Connections to My Work

This paper sits at the intersection of my precipitation and ML-agent lines, and invites direct comparison with my satellite-precipitation evaluation work.

- **Probabilistic vs observational precipitation uncertainty.** My *"Two-decades of GPM IMERG early and final run products intercomparison: Similarity and difference in climatology, rates, and extremes"* and *"Cross-Examination of Similarity, Difference and Deficiency of Gauge, Radar and Satellite Precipitation Measuring Uncertainties for Extreme Events Using Conventional Metrics and Multiplicative Triple Collocation"* quantify *observational* error. FREUD's intensity-correlated decoding variance is conceptually analogous to my triple-collocation error decomposition: both separate irreducible (aleatoric) from model/representation error, and both find heteroscedasticity peaking in heavy rain.
- **Extremes and flash floods.** My *"Evaluation of GPM IMERG and its constellations in extreme events over the conterminous United States"* and *"Introducing Flashiness-Intensity-Duration-Frequency (F-IDF): A New Metric to Quantify Flash Flood Intensity"* show the onset and intensity of extreme rain is the hardest, most safety-critical regime — precisely where FREUD has largest spread yet residual underestimation. F-IDF-style temporal-rate metrics could test whether forecasts preserve flashiness, which CRPS/SSIM ignore.
- **AI surrogate nowcasting.** Methodological neighbor to my *"Rapid Flood Inundation Forecast Using Fourier Neural Operator"* and the agentic pipelines in *"AQUAH: Automatic Quantification and Unified Agent in Hydrology"* and *"HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL"* — a fast probabilistic rain nowcaster is ideal upstream forcing for a coupled flood surrogate.
- **Global reach.** Their radar-only, US-centric limitation maps onto my *"A Review of the Past Half Century of Geostationary Satellite Thermal Observations for Global Precipitation Estimation"* — geostationary IR conditioning is the obvious route to global FREUD.

## Critique & Limitations

- **Single-benchmark, single-variable validation.** Results hinge on SEVIR VIL (a radar proxy, not gauge-validated rain rate). MeteoNet results are weak and split-sensitive (CSI 0.11–0.14 vs CasCast 0.32), with no public CasCast checkpoint for fair comparison.
- **VIL ≠ precipitation.** They forecast Vertically Integrated Liquid via SEVIR's nonlinear encoding; the kg/m² mapping is approximate and untied to ground-truth rain rate or hydrologically relevant accumulations.
- **Localization trade-off.** Smaller models (and L-LSM without CFG) underperform CasCast on HSS/CSI; their best HSS/CSI require the very CFG they argue is flawed.
- **Persistent underestimation of extremes.** Acknowledged climatology bias in the heavy tail — exactly the flood-relevant regime — with no mechanism beyond ensembling.
- **Calibration still imperfect.** Rank histograms improve but remain non-uniform; only aleatoric uncertainty is empirically probed despite invoking the aleatoric/epistemic framework.
- **σ=0.001 not tuned or ablated**, yet it is core to T-reg.
- **Lead time capped at 60 min** with no rate-of-change (flashiness) fidelity assessment.

## Gaps & Ideas

- **Hydrologically meaningful evaluation.** Add gauge/MRMS-anchored rain-rate and accumulation skill, plus an F-IDF-style temporal-rate metric to test sub-hourly flashiness fidelity.
- **Extreme-tail recalibration.** Replace CFG with tail-aware sampling or post-hoc EVT/quantile mapping; train with weighted/threshold-CRPS to directly reward extremes (cf. FGN).
- **Multi-source conditioning for global reach.** Condition on geostationary IR cloud-top temperature (near-global) and SMAP soil moisture to extend beyond US radar and capture land-surface memory.
- **Coupling to flood surrogates.** Use FREUD's probabilistic ensemble as stochastic forcing into a fast inundation operator, propagating decoding+forecast uncertainty into flood-extent probability maps.
- **Disentangle epistemic uncertainty.** A deep/LoRA ensemble of LSMs would quantify epistemic error, testable against triple-collocation error structures.
- **Agentic deployment.** An agent that adaptively chooses conditioning length, NFE, and ensemble size under latency budgets — extending simulator-grounded RL agents.

## How to Advance / Disrupt the Field

**Goal:** Turn FREUD from a benchmark-topping radar nowcaster into a globally deployable, hydrologically validated, uncertainty-propagating precipitation-to-flood engine.

**Recommended DATA.**
- Beyond SEVIR/VIL: GPM IMERG V07 + MRMS/Stage-IV gauge-radar gridded rain rate for ground-truth-anchored verification (using my IMERG V06→V07 intercomparison protocols).
- Global conditioning: GOES/Himawari/Meteosat geostationary IR brightness temperatures + SMAP/MSSM soil moisture for land-surface memory.
- Extreme subsets: NOAA Storm Events + my 120-year US flood database and F-IDF-labeled flash-flood cases to stress-test the tail.

**Recommended METHODS.**
1. **Tail-aware rectified flow.** Replace CFG with weighted/threshold-CRPS training up-weighting extreme percentiles plus EVT/quantile post-calibration, attacking underestimation without the CFG intensity-shift artifact.
2. **Multi-modal frame-wise encoder.** Ingest IR + soil moisture channels for radar-sparse/global nowcasting and brown-ocean re-intensification dynamics.
3. **Dual-uncertainty quantification.** Combine FREUD decoding ensembles (aleatoric) with a deep/LoRA model ensemble (epistemic), validated against multiplicative triple-collocation error structures.
4. **End-to-end coupling.** Feed the probabilistic nowcast ensemble into a Fourier-Neural-Operator inundation surrogate (cf. my ICCVW FNO flood work) to produce probabilistic flood-extent forecasts — the disruptive deliverable.
5. **Agentic deployment.** Wrap the pipeline in an AQUAH/HydroAgent-style controller that adaptively trades NFE/ensemble-size for latency under operational 5-min update constraints.

**Disruption thesis:** the field rewards CRPS/SSIM on VIL, but the real prize is calibrated, global, impact-relevant precipitation uncertainty. Extending FREUD's loss-free generative compression to multi-sensor conditioning, tail calibration, and flood coupling reframes nowcasting around decision-ready probabilistic hazard.
