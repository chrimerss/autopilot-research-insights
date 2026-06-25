---
subject: Machine Learning / AI Agents
subject_slug: ml-ai
topic: 'UniverSat: A Modality-Agnostic ViT Backbone for Earth Observation'
date: '2026-06-25'
title: 'UniverSat: Resolution- and Modality-Agnostic Transformers for Earth Observation'
authors: Yohann Perron; Guillaume Astruc; Nicolas Gonthier; Clement Mallet; Loic Landrieu
year: '2026'
venue: ''
link: arXiv:2606.23503
figure: /assets/figures/universat/figure.png
source_pdf: https://github.com/chrimerss/autopilot-research-insights/blob/main/interest/UniverSat/UniverSAt.pdf
---

## Summary & Key Contributions

**Core idea.** UniverSat replaces the rigid patch projector of a standard ViT with a **Universal Patch Encoder (UPE)** that maps patches of arbitrary spatial, spectral, and temporal resolution—across optical, radar, elevation, and hyperspectral sensors—into a shared embedding space with a *single* set of weights, requiring no input resampling or band selection.

**Key contributions:**
- **Axial Cross-Attention (ACA)** that sequentially collapses pixel, channel, time, and sub-patch axes (CxTxIxS) with linear complexity, injecting axis-specific metadata (wavelength, polarization, time-in-year, GSD-scaled RoPE).
- **Resolution-flexible output**: target GSD specified at inference, decoupled from input patch size, with a sub-patch skip connection (cross-attention) to recover fine spatial detail.
- **Multimodal SSL training (LM3 + cross-modal contrastive loss)**: latent masked modeling against frozen random projections, with ~90% atom dropping, jointly trained on 7 datasets / 13 sensors / 4 modalities (0.1–300 m GSD, 1–150 timestamps, 1–396 channels).
- **Strong probing results**: SOTA on BrickKiln and Sen1Floods11; on PangaeaBench it reaches SOTA on PASTIS-R and AI4Farms with a linear probe using ~3700–5000x fewer supervised parameters than UperNet-based competitors; competitive on SpectralEarth hyperspectral tasks despite never training on EnMAP.
- **Generalization to unseen sensors/configs** (mono-temporal Sentinel, fewer bands, synthetic HLS) without retraining.

## Connections to My Work

This work is directly relevant to my recent push toward foundation models and benchmarks for geoscience. Most concretely, UniverSat achieves SOTA on **Sen1Floods11** flood segmentation with a frozen linear probe—exactly the kind of generalizable, sensor-agnostic representation I want to leverage in **"FloodSimBench: A Benchmark Dataset for Training Foundational Flood Inundation Models"**. A modality-agnostic backbone that fuses optical + SAR + DEM without resampling could supply the input encoder for foundational inundation models, complementing the physics-grounded learning I explored in **"Rapid Flood Inundation Forecast Using Fourier Neural Operator"** (where DEM and forcing inputs are tightly coupled to spatial resolution).

The multi-sensor fusion theme also connects to my precipitation/soil-moisture remote-sensing line: **"Triple Collocation of Ground-, Satellite- and Land Surface Model-Based Surface Soil Moisture Products in Oklahoma — Part II: New Multi-Sensor Soil Moisture (MSSM) Product"** and **"Joint Collaboration on Comparing NOAA's Ground-Based Weather Radar and NASA-JAXA's Spaceborne Radar"** both grapple with reconciling heterogeneous sensors at different resolutions—precisely the problem UPE solves architecturally. Finally, my agentic-hydrology work (**"HydroAgent: Closing the Gap Between Frontier LLMs and Human Experts in Hydrologic Model Calibration via Simulator-Grounded RL"** and **"AQUAH: Automatic Quantification and Unified Agent in Hydrology"**) could pair a UniverSat-style perception backbone with LLM-driven decision agents for end-to-end flood/hydrology pipelines.

## Critique & Limitations

- **No hydrology-relevant downstream tasks beyond Sen1Floods11.** Evaluation is dominated by land-cover/crop/tree classification and segmentation; there is no continuous regression (e.g., inundation depth, streamflow, soil moisture), which is what hydrologists actually need.
- **Self-acknowledged specialization tradeoff.** In standard regimes (VHR RGB, mono-temporal S2) modality-specific models can be more accurate/efficient, and unseen *non-optical* sensors still require fitting a small modality-encoding vector—so the 'agnostic' claim is softer for radar/hyperspectral.
- **Probing-only protocol.** Strong linear/kNN results are encouraging but do not show whether the backbone supports fine-tuning gains, nor robustness under domain shift (different continents, cloud regimes, flood vs. non-flood).
- **Temporal modeling is shallow.** Only K=4 timestamps sampled per tile, chosen to minimize cloud; this discards the dense-time-series signal crucial for flood event dynamics and rainfall-runoff response.
- **Compute / reproducibility.** 30K GPU-h project footprint (~31 t CO2); the fixed UPE collapse order (pixel→channel→time→subpatch) is asserted but not ablated, and bilinear upsampling for any-resolution output may smear sharp hydraulic features (channels, levees).
- **No uncertainty quantification**, which is essential for any operational forecasting or risk product.

## Gaps & Ideas

- **Flood-domain foundation backbone.** Fine-tune/probe UniverSat on FloodSimBench: can a sensor-agnostic encoder predict *continuous* inundation extent/depth rather than binary segmentation? Test cross-sensor transfer (train S1, infer S2+DEM).
- **Hydrologic regression head.** Add a Fourier-Neural-Operator or physics-informed decoder on top of UPE embeddings to map multimodal observations → inundation depth fields, marrying the perception backbone with my FNO inundation work.
- **Dense temporal flood dynamics.** Replace the K=4 cloud-minimizing sampling with event-centric sampling around precipitation peaks; couple with IMERG precipitation forcing as an additional 'modality' channel.
- **Precipitation/soil-moisture as modalities.** Treat IMERG, radar QPE, and MSSM soil moisture as input modalities—UPE's per-channel descriptor mechanism is ideal for ingesting non-imagery geophysical fields.
- **Agentic orchestration.** Use AQUAH/HydroAgent-style LLM agents to select which sensors/timestamps UniverSat ingests for a given basin and event, closing the perception–decision loop.
- **Uncertainty & calibration.** Add probabilistic heads (deep ensembles / evidential) for risk-grade outputs.

## How to Advance / Disrupt the Field

**Plan: Build a continuous, multimodal *Flood Foundation Model* by repurposing UniverSat's UPE as the perception layer of an end-to-end inundation forecasting system.**

**Data.** (1) FloodSimBench as the supervised target (continuous inundation extent/depth from coupled hydrologic-hydraulic simulations, leveraging my CREST-iMAP/CREST-VEC outputs). (2) Sentinel-1 SAR + Sentinel-2 optical for observation (handles cloud occlusion via SAR). (3) High-res DEM/DTM (already a UPE modality) for hydraulic conditioning. (4) IMERG V07 precipitation and radar QPE as forcing 'modalities' encoded via UPE's per-channel descriptors. (5) MSSM soil moisture for antecedent wetness. (6) Validation against my 120-year US flood database and event hindcasts (e.g., Hurricane Harvey).

**Methods.** (1) Initialize from pretrained UniverSat-B; extend the channel-descriptor vocabulary to admit geophysical forcing fields, not just radiance/polarization. (2) Replace the segmentation linear probe with a **Fourier Neural Operator decoder** (building on 'Rapid Flood Inundation Forecast Using Fourier Neural Operator') that maps fused embeddings + DEM to continuous depth fields at user-specified GSD—exploiting UniverSat's any-resolution output. (3) Add a **physics-informed loss** enforcing mass conservation / monotonic depth–DEM consistency to curb bilinear smearing at channels and levees. (4) Use **event-centric temporal sampling** keyed to precipitation peaks rather than cloud minimization. (5) Add **evidential/ensemble uncertainty heads** for risk-grade probabilistic maps. (6) Wrap the whole pipeline in an **AQUAH/HydroAgent-style LLM agent** that chooses sensors, output resolution, and forcing inputs per basin/event—delivering a self-configuring operational flood nowcasting system. **Disruption thesis:** a single shared backbone that ingests *any* available sensor + forcing for *any* basin at *any* resolution would replace today's bespoke, basin-by-basin flood models, and the benchmark (FloodSimBench) would standardize evaluation the way GeoBench/Pangaea did for land cover.
