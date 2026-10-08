---
title: SWOT‐Fitted River Bathymetry for Global Hydrodynamic Models
authors: ''
year: '2023'
venue: ''
---

SWOT‐Fitted River Bathymetry for Global Hydrodynamic
Models
Augusto Getirana1,2
, Elyssa Collins1,3
, Sujay Kumar1, Yeosang Yoon1,2
, and Wanshu Nie1,2
1Hydrological Sciences Laboratory, NASA Goddard Space Flight Center, Greenbelt, MD, USA, 2Science Systems and
Applications, Inc., Lanham, MD, USA, 3Earth System Science Interdisciplinary Center, University of Maryland College
Park, College Park, MD, USA
Abstract We present a robust, global method to reconcile absolute water surface elevations (WSE) from the
Surface Water and Ocean Topography (SWOT) mission with a large‐scale hydrodynamic model by iteratively
correcting river bathymetry. After removing sensor and representativeness bias, we update riverbed elevations
under DEM and min‐depth feasibility constraints and interpolate corrections along reaches. Applied worldwide
at 0.05° resolution over 2023–2025, the approach reduces the global median absolute WSE bias
(3.10 m →0.18 m), preserving the same global median correlation (0.38). A modest ∼4% increase in the
standard deviation ratio (1.07 →1.11) indicates slight variance inflation. Independent evaluation over
2015–2025 at 16,746 Hydroweb sites and 2123 GRDC gauges, restricted to reaches with updated beds, confirms
substantially reduced bias, negligible change in both correlation and variance, and no significant change in
global median discharge skill. When combined with models, this bias‐aware bathymetry will enable a refined
numerical representation of floods globally.
Plain Language Summary Since its launch in 2022, NASA's Surface Water and Ocean Topography
(SWOT) mission has been providing river water levels at global scale. When we compare satellite
measurements to model results, disparities show up because hydrological models often use terrain maps that
contain vertical errors. This prevents us from using SWOT data to improve the models. We present a robust
method that adjusts the model's river bottom elevations so that modeled water levels align with SWOT. The
method removes known reference and location mismatches, then shifts river bottoms and repeats the model run
until the differences reach an acceptable minimum. Applied worldwide at 5‐km resolution, this approach
reduces the typical (median) water‐level error from 3.10 to 0.18 m after two cycles, without changing overall
flood‐wave timing. A small increase in variability is observed. Checks using data from other satellites and
thousands of stream gauges confirm the large reduction in bias and little change in streamflow accuracy. The
proposed method prepares models to directly ingest SWOT water levels in the future, where we expect further
gains in flood timing and magnitude, supporting better flood risk assessment and water management at
continental scales.
1. Introduction
Accurate representation of river channel geometry and, in particular, riverbed elevation (bathymetry), is a first‐
order control on flood dynamics in hydrodynamic models (Bates, 2023; Nguyen et al., 2026). Channel geometry,
defined here by width, depth, and bed elevation, governs river conveyance and the partitioning of flow between
in‐channel and overbank pathways. Underestimated geometry (narrow or shallow channels) promotes premature
overflow and overestimation of flood extent, whereas overestimated geometry (wide or deep channels) suppresses
overflow and leads to underestimation of inundation. Consequently, errors in riverbed elevation propagate
directly into biases in flood magnitude, extent, and timing, even when hydrologic forcing is accurate (Decharme
et al., 2012; Yamazaki et al., 2011).
Flood simulations also depend on the accuracy of surface and sub‐surface runoff generation, typically derived
from land surface models. These fluxes are subject to uncertainties in forcing and model structure, and are often
improved through bias correction or data assimilation (Collins et al., 2024; Paiva et al., 2013). Satellite obser-
vations of water surface elevation (WSE) provide a direct constraint on river stage and dynamics and, when
combined with channel geometry, on river storage. In particular, the Surface Water and Ocean Topography
RESEARCH LETTER
10.1029/2026GL125708
Special Collection:
Science from the Surface Water
and Ocean Topography Satellite
Mission
Key Points:
•
Iterative SWOT‐fitted bathymetry cuts
global median water surface elevation
(WSE) bias from 3.10 to 0.18 m in two
runs
•
Global median flood‐wave timing is
preserved (median r = 0.38); modest
variance increase (standard deviation
ratio 1.07 →1.11)
•
Comparisons against Hydroweb and
GRDC data confirm WSE bias drop
and preserved global‐scale flood‐wave
amplitude and timing
Supporting Information:
Supporting Information may be found in
the online version of this article.
Correspondence to:
A. Getirana,
augusto.getirana@nasa.gov
Citation:
Getirana, A., Collins, E., Kumar, S., Yoon,
Y., & Nie, W. (2026). SWOT‐fitted river
bathymetry for global hydrodynamic
models. Geophysical Research Letters, 53,
e2026GL125708. https://doi.org/10.1029/
2026GL125708
Received 20 JUL 2026
Accepted 23 SEP 2026
Author Contributions:
Conceptualization: Augusto Getirana
Data curation: Augusto Getirana,
Elyssa Collins, Wanshu Nie
Formal analysis: Augusto Getirana,
Elyssa Collins, Sujay Kumar,
Yeosang Yoon, Wanshu Nie
© 2026 The Author(s). Geophysical
Research Letters published by Wiley
Periodicals LLC on behalf of American
Geophysical Union.
This is an open access article under the
terms of the Creative Commons
Attribution‐NonCommercial‐NoDerivs
License, which permits use and
distribution in any medium, provided the
original work is properly cited, the use is
non‐commercial and no modifications or
adaptations are made.
GETIRANA ET AL.
1 of 12

(SWOT) mission offers near‐global WSE observations at scales relevant for large rivers, creating new oppor-
tunities to constrain hydrodynamic models.
However, both flood modeling and the effective use of satellite observations are fundamentally limited by un-
certainties in riverbed elevation. While river width and surface extent can be estimated from remote sensing (Feng
et al., 2022; Pavelsky & Smith, 2008; Yamazaki et al., 2014), bathymetry remains largely unobservable at large
scales (Andreadis et al., 2013; Jiang et al., 2021). Existing approaches to infer riverbed elevation, such as rating‐
curve inversion, optimization, and data assimilation (Andreadis et al., 2007; Durand et al., 2008; Getirana
et al., 2009; Neal et al., 2021; Yoon et al., 2012), are often data‐intensive or region‐specific, which may limit their
scalability. As a result, large‐scale hydrodynamic models rely on simplified parameterizations of channel ge-
ometry, introducing systematic errors in simulated water levels and storage (Decharme et al., 2012; Getirana
et al., 2012; Luo et al., 2017; Yamazaki et al., 2011).
These structural errors have two key consequences. First, they degrade flood simulations by misrepresenting river
storage and overflow thresholds, leading to biases in flood extent and timing (Neal et al., 2021). Second, they
introduce meter‐scale offsets between modeled and observed WSE, limiting the integration of satellite obser-
vations (Getirana et al., 2013; Yamazaki et al., 2012). Anomaly‐based approaches can remove mean biases but
discard absolute elevation information that governs hydraulic gradients, backwater effects, and floodplain con-
nectivity. Addressing riverbed elevation errors is therefore essential for both physically consistent flood modeling
and the use of satellite‐derived WSE. Improving bathymetry aligns modeled and observed water levels while
restoring realistic surface water dynamic properties that control flooding.
Here, we propose a global approach to estimate riverbed elevation by leveraging systematic differences between
observed and simulated WSE. The method decomposes these differences into components, and iteratively up-
dates riverbed elevations to minimize bias. By directly targeting structural errors in bathymetry, the approach has
the potential to improve flood representation while enabling the consistent use of SWOT WSE observations. We
demonstrate the method using the Hydrological Modeling and Analysis Platform (HyMAP; Getirana et al., 2012)
and evaluate its impact on simulated water levels and discharge across global river networks.
2. Methods
To improve riverbed elevation estimates using SWOT WSE, we decompose the absolute mismatch between
SWOT and the model WSE values (ΔH) into three components: (a) geolocation/representativeness bias arising
from mismatches between the SWOT sampling location and the model/DEM location (bloc); (b) systematic sensor
biases (bsen); and (c) residual model‐parameter bias attributable primarily to riverbed elevation and related ge-
ometry (bpar). Formally, for reach r and iteration t:
ΔHr,t = H
SWOT
r
−H
model
r,t
= bloc
r
+ bsen
r
+ bpar
r,t + εr,t
(1)
where HSWOT and Hmodel are the SWOT and modeled WSE, and ε captures random measurement and model
errors. The workflow proceeds sequentially. We first estimate and remove bloc and bsen. The remaining difference
is attributed primarily to bpar, which is used to update riverbed elevation under physical constraints. These updates
are then propagated along the river network and the model is rerun iteratively until convergence. Because river
hydraulics are nonlinear due to inertia, diffusion, floodplain exchange, backwater, etc., local riverbed edits can
induce upstream/downstream changes. As a result, multiple iterations to correct bpar are therefore expected.
Figure 1 illustrates a hypothetical grid cell and its DEM pixels, as well as the elevation profile of the river pixels
and biases assumed in Equaton 1.
2.1. Geolocation/Representativeness Bias
River models often define riverbed and WSE at the outlet node of each grid cell (Figure 1a). Depending on the
SWOT product used, particularly the Vector Reach Data Product, those outlet nodes may not spatially coincide
with satellite data. This is also the case for other radar altimeters (e.g., Jason and Sentinel). In the SWOT reach
product, WSE is derived from spatially distributed observations aggregated over a reach segment, rather than
corresponding to a single point location, which introduces representativeness differences relative to model outlet
Funding acquisition: Augusto Getirana,
Sujay Kumar
Investigation: Augusto Getirana,
Elyssa Collins
Methodology: Augusto Getirana
Project administration: Sujay Kumar
Resources: Augusto Getirana
Software: Augusto Getirana, Sujay Kumar
Supervision: Augusto Getirana
Validation: Augusto Getirana
Visualization: Augusto Getirana
Writing – original draft:
Augusto Getirana, Elyssa Collins
Writing – review & editing:
Augusto Getirana, Elyssa Collins,
Sujay Kumar, Yeosang Yoon, Wanshu Nie
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
2 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

nodes. Let xout
r
be the outlet location of cell x and xSWOT
r
the downstream endpoint of a SWOT reach. Using a fine‐
resolution DEM elevation (zDEM), we quantify the representativeness correction as:
bloc
r
= zDEM(xSWOT
r
) −zDEM(xout
r )
(2)
which we subtract from ΔHr,t before attributing remaining bias to parameters.
2.2. Systematic Sensor Bias
This term represents a systematic difference between SWOT WSE and model/DEM elevations at the same river
location after both data sets have been transformed to the EGM96 vertical datum. The Shuttle Radar Topography
Mission (SRTM; Farr et al., 2007) is the DEM basis for many hydrography products (USGS, 2007; Yamazaki
et al., 2019), and it was acquired in February 2000. We estimate this cross‐sensor bias by averaging SWOT WSE
over a seasonally comparable mid‐January to mid‐March (or JM period) within the mission window. For each
reach, we have:
Figure 1. Schematic for the SWOT‐fitted riverbed correction: (a) Plan view and longitudinal profile of a hypothetical river within one model grid cell (illustrated with a
10 × 10 DEM sub‐grid); WSE and bed are referenced to the cell outlet. (b–c) Iterative bed updates at sample cross‐sections where SWOT WSE lies above (b) or below
(c) the modeled WSE. (d–e) Along‐channel bed profiles before (d) and after (e) linear interpolation of anchor corrections between SWOT‐fitted reach endpoints.
Abbreviations are defined in Methods.
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
3 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

H
SWOT,JM
r
= medianJM (HSWOT
r
)
(3)
The reach‐level systematic offset is then
bsen
r
= H
SWOT,JM
r
−zDEM(xSWOT
r
)
(4)
which is removed from all SWOT–model comparisons for that reach. This step targets sensor differences and
errors associated to SRTM measurements (Simard et al., 2024).
2.3. Residual Parameter Bias and Riverbed‐Elevation Updates
After removing bsen and bloc, we attribute the residual
ˆb
par
r,t = ΔHr,t −bsen
r
−bloc
r
(5)
to bias dominated by model parameterization and update the riverbed elevation as:
zbed,new
r,t
= zbed,old
r,t
+ ˆb
par
r,t
(6)
We then enforce a physical feasibility constraint to prevent the channel from “vanishing,”, that is, a minimum
prescribed river depth dmin = 0.5 m. In rare cases where updates violate feasibility, an overflow adjustment is
applied to maintain a minimum channel depth (Text S1 in Supporting Information S1). In practice, the overflow
adjustment is typically ≤0.5 m. Note that the constraint assumes rectangular cross‐sections and fixed roughness;
structural simplifications (e.g., cross‐sectional shape, floodplain storage) can also imprint biases and are not
explicitly corrected here.
This bias partition assumes that, after representativeness corrections, residuals primarily reflect bathymetry/
geometry error. Other structural choices (e.g., rectangular cross‐sections, single‐value roughness, river width
uncertainty, and simplified floodplain storage, in addition to runoff fluxes) may also contribute to bias and are not
explicitly corrected here.
2.4. Spatial Interpolation of Riverbed Updates and Iteration
Riverbed updates are first estimated at reaches with reliable SWOT constraints (“anchor” set A, defined as reach
endpoints with reliable SWOT observations used to constrain riverbed updates) and are then extended across the
network by linear interpolation along flow paths between outlet nodes. Let cr ≡zbed,new
r
−
zbed,old
r
denote the
post‐constraint correction at anchor reach r ∈A (i.e., after applying the DEM upper bound and dmin; see Sec-
tion 2.3). Riverbed corrections are interpolated along flow paths between anchor reaches using along‐channel
distances (see Text S2 in Supporting Information S1).
The updated outlet‐referenced riverbed map {zbed,new
r
} is used in the next simulation, residuals are recomputed
against SWOT, and the cycle repeats until a convergence criterion is met, for example, global‐median ∣ˆb
par
t ∣< ϵ.
To avoid overfitting and error compensations, we adopted ϵ = 0.2 m.
2.5. Modeling Framework
HyMAP is a global‐scale hydrodynamic model capable of simulating surface water dynamics, including water
storage, elevation and discharge in‐stream, in rivers and floodplains using the local inertia formulation (Bates
et al., 2010). Local inertia represents river flow diffusiveness and the inertia of large water masses of deep flow,
which is essential for a physically‐based representation of wetlands, lakes, floodplains, tidal effects, and im-
poundments. HyMAP resolves the local inertia formulation unidimensionally (i.e., a unique flow direction is
attributed to each grid cell). Rivers and floodplains interact laterally and have independent flow dynamics, with
roughness and geometry derived from land cover characteristics, topography and river parameterization
(Getirana, Kumar, et al., 2025).
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
4 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

HyMAP is run globally at 5‐km resolution over 2015–2025 using the configuration presented in Getirana
et al. (2026) and briefly described below. All elevations are transformed to EGM96 prior to comparison, and only
reaches with sufficient SWOT sampling and stable quality flags are used for fitting (see SWOT data processing
section below).
Channel geometry and roughness. We prescribe rectangular cross‐sections and spatially varying roughness in
channels and floodplains globally following Getirana et al. (2012). River width, w [m], is derived from MERIT‐
Hydro at 3‐arcsec spatial resolution (Yamazaki et al., 2019), and gap‐filled with a simple discharge‐based
function (see details in Text S3 in Supporting Information S1).
Topography, hydrography, and forcings. River network and elevations are also derived from MERIT‐Hydro
processing. HyMAP was forced with daily surface runoff and baseflow from the Global Land Data Assimila-
tion System Version 2.2 (GLDAS‐2.2). GLDAS‐2.2 runoff was bias‐corrected using a gauge‐based multiplicative
scaling approach inspired by Collins et al. (2024), in which correction factors are derived from
observed–simulated discharge mismatches and applied over upstream drainage areas (see details in Text S4 in
Supporting Information S1).
Copernicus Marine Service's altimetry‐based daily sea surface height data (Taburet et al., 2019) are used as
downstream boundary conditions along coastlines (171,218 coastal grid cells globally) to represent the impacts of
sea level variability on river dynamics (see details in Text S5 in Supporting Information S1).
2.6. SWOT Data Processing
We adopted SWOT WSE observations from the SWOT_L2_HR_RiverSP_2.0 data product between 1 July 2023
and 10 March 2025 for each reach in the SWOT Prior River Database (SWORD) version 16 about twice every
21 days (Altenau et al., 2021). To facilitate downloading such a large number of observations, we used the
Hydrocron tool (Greguska et al., 2025). We filtered the downloaded observations using the bitwise quality flag
(“reach_q_b”; SWOT, 2024) and an outlier filter. For the bitwise quality flag, we filtered out all observations with
a bit >17, which removes observations with greater degradation (e.g., geolocation quality). For the outlier filter,
we calculated the median and standard deviation across the time series for each reach and removed observations
that were outside of the median ±2 times the standard deviation. These filters retained approximately 28% of the
original observations (total of 3,634,164 measurements globally).
HyMAP‐SWOT connection. The SWORD‐mirror network (Sikder et al., 2024) was used as a “connector” between
HyMAP grids and SWORD river reaches. SWORD‐mirror is based on SWORD version 16 and includes a subset
of 241,852 SWORD reaches. We assumed 0.12° as the maximum distance between each SWORD‐mirror reach
and HyMAP grids. Within the 0.12° radius, a drainage area match was performed, where the closest HyMAP
drainage area was assigned to the SWORD‐mirror reach. If drainage area mismatch is greater than ±20%, the
reach is neglected. The process resulted in 188,517 HyMAP‐SWORD matches; a 78% retention.
2.7. Model Evaluation
To assess how SWOT‐fitted bathymetry impacts model skill independently of SWOT, we compared HyMAP
simulations against two global data sets over 2015–2025: Hydroweb (WSE) at 16,746 altimetric locations and
GRDC daily discharge at 2123 gauges. We computed the normalized information contribution (NIC; Kumar
et al., 2014) for standard metrics relative to the default‐bed simulation, that is, Kling‐Gupta Efficiency (KGE),
relative error (RE), correlation (r), and standard deviation ratio (rstd). Consistent with our WSE evaluation
protocol, for Hydroweb we report NIC of unbiased KGE (ubKGE) and Δ∣bias∣in place of KGE and RE. Positive
NIC indicates improvement, while negative Δ∣bias∣denotes reduced absolute bias. Analyses were restricted to
locations where SWOT data is available and the riverbed was updated, which substantially reduces the number of
evaluation sites relative to the full Hydroweb/GRDC catalogs but isolates the direct effect of bathymetry fitting.
River bathymetry was also evaluated against river cross‐section surveys at 3,132 locations, 1,262 in Brazil and
1,870 in the contiguous U.S. (CONUS). This is a subset of 6,629 stations available at river reaches affected by the
SWOT‐fitting approach. Details on the river cross‐section data acquisition and processing are provided in Text S6
in Supporting Information S1.
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
5 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

3. Results
Comparing HyMAP WSE (default riverbed) with SWOT at 85,307 locations yields a global median |bias| of
3.10 m and a mean of 6.84 m (Figure 2a). Removing bsen and bloc substantially reduces errors (Figure 2b): the
median and mean |bias| drop to 1.12 and 1.92 m, respectively. This demonstrates that accounting for represen-
tativeness and reference‐related offsets substantially reduces the mismatch between SWOT and modeled WSE.
Proceeding with the riverbed fitting, median global biases computed between SWOT and modeled WSE drop to
0.89 m at the first iteration (Figure 2c). After two iterations, the median |bias| falls to 0.18 m (Figure 2d). Large
residual biases are concentrated at lower elevations, such as rivers within the central and low Amazon basin, East
and West Africa, and Australia. The global median correlation remains unchanged at r = 0.38, indicating no
overall shift in flood‐wave timing; higher correlations cluster in the tropics (e.g., northern South America,
Figure 2. Global SWOT‐fitted riverbed. (a–d) Heatmaps of WSE bias between SWOT and HyMAP at 85,307 locations for (a) default riverbed, (b) sensor‐ and
representativeness–corrected WSE (after removing bsen + bloc), (c) iteration 1 of bathymetry fitting, and (d) iteration 2. (e–g) Spatial distribution of (e) bias,
(f) correlation, and (g) standard deviation ratio for the default riverbed simulation. (h–j) Same three metrics after iteration 2. Here, bsen denotes sensor and bloc denotes
geolocation/representativeness bias (see Methods).
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
6 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

western/central Africa, south–southeast Asia). In contrast, the standard deviation ratio shows ∼4% degradation
(1.07 →1.11), that is, slightly amplified WSE variability, most evident in western South America, central Africa,
and southeast Asia (Figures 2g and 2j).
Mirroring the evaluation against SWOT, comparisons against Hydroweb's water elevation (Figures 3a–3d)
indicate a substantial reduction in absolute WSE bias (global median Δ∣bias∣= −0.46 m). Global median cor-
relation shows no net change (NICr = 0), confirming that flood‐wave timing is not generally degraded by the
static bed update. Hydroweb further shows no substantial degradation in variability, with a median NICrstd ≈0,
and correspondingly no change in global ubKGE (median NICubKGE ≈0). On the discharge side, no significant
change is detected in global medians of KGE, RE, r, or rstd at GRDC gauges, indicating that the bathymetry
correction does not materially alter bulk streamflow skill at the global scale.
Regionally, NIC patterns for GRDC discharge reveal coherent, but compensating, signals that explain the near‐
zero global medians (Figures 3e–3h). NICKGE shows broad improvements across South America, especially
Brazil, along long, low‐slope reaches. In contrast, clusters of negative NICKGE in parts of Europe and North
America (U.S. and Canada) indicate localized degradations that offset South American gains. For RE, we find
Figure 3. Impact of SWOT‐fitted riverbed on simulated WSE and streamflow. Performance changes are summarized using the normalized information contribution
(NIC) for key metrics, that is, Kling‐Gupta efficiency (KGE), relative error (RE), correlation (r), and standard deviation ratio (rstd), computed relative to the default
riverbed. Panels compare simulations against independent data sets: Hydroweb altimetric WSE (left) and GRDC daily discharge (right). For WSE, we report NIC of
unbiased KGE (ubKGE) in place of KGE and Δ∣bias∣(change in absolute bias) in place of RE.
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
7 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

clear improvements in the Amazon and scattered positive sites in Canada and Europe, but these are counter-
balanced by nearby degradations, yielding a global median ≈0. It is important to note that GRDC data distribution
is highly heterogeneous across the globe, with large voids in Africa, Middle East, Asia and Russia (Figure S1 in
Supporting Information S1 shows examples of streamflow simulations globally). This prevents a comprehensive
quantification of actual impacts of bathymetry fitting on simulated streamflow at the global scale.
Correlation changes are similarly heterogeneous: net improvements over Brazil (and pockets in Australia) coexist
with degradations across portions of North America and Europe, while South Africa is mixed. The standard
deviation ratio mirrors this spatial distribution, that is, improved variance behavior in Brazil, but degraded in parts
of North America and Europe. Collectively, these maps suggest that while the bathymetry correction successfully
restores absolute stage accuracy globally, its secondary effects on streamflow variability and phasing depend on
local hydraulics and configuration (e.g., roughness/width priors, management, floodplain connectivity, DEM
alignment, and SWOT data availability). This spatial heterogeneity underscores the need for basin‐specific tuning
to retain the global bias reduction while minimizing regional penalties in dynamical skill.
Comparison of SWOT‐fitted bathymetry against surveyed cross‐section observations shows reduced height error
in both countries, but with opposite starting biases and unequal gains (Figures 4a and 4b). At CONUS gauges, the
default bathymetry initially overestimated mean flow depth by 1.05 m on average (81% of gauges over‐pre-
dicted); after iteration 2, the mean bias drops to 0.08 m (56% over‐predicted), mean absolute error (MAE) falls by
16.6% (1.55 →1.29 m), and the fraction of gauges within their reported observational uncertainty rises from
21.1% to 27.3%. At Brazilian gauges, HyMAP instead underestimates mean river height (mean bias of −3.34 m,
7% over‐predicted); after iteration 2, the bias drops to −2.89 m (14% over‐predicted), MAE falls by 8.5%
(3.76 →3.44 m), and the hit rate (i.e., modeled river‐height estimates falling within the observational uncertainty
interval) nearly quadruples (2.3% →10%). These results demonstrate that the SWOT‐fitting approach proposed in
this study not only reduces the bias between simulated and SWOT WSE, but also moves river height estimates in
the right direction when evaluated against independent, surveyed observations at large spatial scales.
Across five major rivers (Amazon, Mississippi, Nile, Murray and Niger), outlet‐referenced profiles show that
SWOT‐fitted bathymetry introduces more spatially variable river heights than the relatively flat DEM‐derived
riverbed elevations. These are hydro‐geomorphologically more plausible, though we lack independent data to
quantify accuracy (Figure 4). Profiles also reveal reservoir signatures that the current workflow does not explicitly
treat. On the Nile, the Aswan Dam (∼1,200 km from the outlet) produces local artifacts (e.g., a slight upstream
bed rise near the dam) because the SWOT data set used excludes reservoir WSE. Similar features appear on the
Niger, near the Jebba–Kainji cascade (∼1,000 km). These cases underscore the need to incorporate managed
systems (reservoir bathymetry and operations) in future iterations.
Flow velocity responses are generally modest, aligning with the near‐zero global change in discharge skill. For the
Amazon, mean velocity changes negligibly (1.04 →1.02 m/s) despite riverbed adjustments. A clearer dynamical
effect emerges on the Nile, where fitted depths roughly drop by half from a deep default (∼19 m), likely
increasing overbank flow and decreasing mean velocity from 0.78 to 0.72 m/s by iteration 2. Overall, the profiles
illustrate how bathymetry fitting can alter local hydraulics (river height, velocity) while preserving basin‐scale
flow statistics (except in shallow or strongly managed reaches, where targeted treatment of boundaries and
infrastructure is necessary).
4. Discussion and Conclusions
This study demonstrates an effective approach to refine global river bathymetry by reconciling WSE from SWOT
with a global hydrodynamic model (HyMAP). We decompose observation–model mismatch into sensor biases,
geolocation/representativeness, and residual parameter components, then iteratively update riverbed elevations
under a DEM/min‐depth feasibility constraint. The outlet‐referenced geometry used by HyMAP at 5‐km reso-
lution and an along‐channel interpolation of “anchor” corrections allow the method to operate consistently across
heterogeneous river lengths, sampling densities, and hydroclimates while keeping the updates hydraulically
coherent along flow paths.
The SWOT‐fitting over 2023–2025 achieves the intended target: the global median |bias| drops from 3.10 m
(default bed) to 0.18 m by iteration 2, while timing remains essentially unchanged—global median correlation
0.38 for both the default and iteration 2. The principal tradeoff is a modest but widespread amplitude increase: the
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
8 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

global median standard deviation ratio rises by ∼4%. Mechanistically, shifting the bathymetry without
re‐optimizing width/roughness can steepen local WSE gradients or alter backwater extents, increasing variance
even as median bias drops.
Independent evaluation over 2015–2025 confirms the SWOT‐based findings: substantially reduced bias, un-
changed global median correlation and standard deviation ratio, and marginally improved ubKGE, with no
significant change in global median discharge skill. In practical terms, the approach restores the absolute level
Figure 4. SWOT‐fitted riverbed overview. At the top, change in absolute errors between the default (Def) and iteration 2 (Iter2) riverbed parameterizations, when
compared to surveys (negative values mean improvement), (a) in the contiguous U.S. and (b) Brazil alongside a table with key metrics, including: number of locations
(N), mean and median profile count per location, mean absolute error (MAE) of river height estimates for Def and Iter2, change in MAE (ΔMAE%) and hit rate. At the
bottom, longitudinal profiles for selected major rivers: (c–g) riverbed elevation; (h–l) river height; (m–q) flow velocity. Each panel shows results for Def and Iter2.
Profiles extend upstream from the river outlet and are truncated at 200 m elevation.
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
9 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

information (the main constraint for using SWOT magnitudes) with global‐scale compensating changes in flood‐
wave timing and with no significant change in global median discharge skill.
The following factors were adopted to correct riverbed elevation: (a) removing sensor and representativeness
components before attributing residuals to bathymetry; (b) enforcing feasibility via a DEM upper bound and a
minimum depth of 0.5 m to prevent channels from “vanishing,” with localized DEM lifts only when fitted updates
exceed feasible geometry; and (c) performing along‐channel interpolation between SWOT‐constrained anchors
using outlet‐to‐outlet distances.
Limitations remain. First, sensor bias alignment assumes SWOT WSE averaged over the mid‐January to mid‐
March period is a suitable proxy for stage during SRTM acquisition (February 2000); this seasonal statio-
narity may be violated where interannual variability, regulation, or morphological change shifts absolute stage.
Second, the SWOT record is still short and unevenly sampled, which constrains separation of persistent bias from
transient hydrologic states and increases sensitivity to quality control screening. Third, residual misfit reflects
broader model uncertainty beyond bathymetry, including meteorological forcing errors, imperfect vertical water
and energy fluxes and storages, occasional mismatches between SWORD and HyMAP reaches, and structural
simplifications that matter most in (a) tide‐ and surge‐influenced coastal reaches, (b) managed systems with
reservoir operations, water withdrawals, and flood control structures, and (c) deltaic bifurcations. Uncertain river
widths also propagate into the hydrodynamic modeling. Finally, implementation details are model‐specific, so
replication across other models and data sets is needed, ideally leading to an ensemble of riverbed elevation fields
with quantified uncertainty. Hence, future SWOT‐fitted riverbed studies should focus on sensitivity analyses of
multiple methods to determine global river bathymetry, including rating curves and traditional optimization and
assimilation, while benefitting from sustained SWOT data acquisition. Such studies should also account for sub‐
daily coastal interactions and human activities, as these processes may lag flood waves and add uncertainty to the
bias correction.
Because riverbed elevation controls channel storage, hydraulic gradients, backwater effects, and the transition
from in‐channel to overbank flow, reducing bathymetric errors is essential for more realistic simulation of flood
magnitude, extent, and timing. By using SWOT WSE to constrain riverbed elevation while largely preserving
flood‐wave timing and discharge skill, the proposed approach strengthens both flood modeling and the physically
consistent use of satellite‐derived WSE. It also provides a more reliable foundation for future assimilation of
SWOT WSE and related variables to further improve flood‐wave dynamics (Yoon et al., 2026). The integration of
such methods with global hydrological models constrained with multi‐satellite data sets has the potential to
substantially improve our capability to predict extreme hydrological events (Getirana et al., 2024).
Conflict of Interest
The authors declare no conflicts of interest relevant to this study.
Availability Statement
HyMAP is freely available within NASA's Land Information System (LIS) Framework through https://github.co
m/NASA‐LIS/LISF. Global Land Data Assimilation System (GLDAS) Catchment Land Surface Model L4 daily
0.25 × 0.25° GRACE‐DA1 V2.2 (GLDAS_CLSM025_DA1_D_EP) data is available from NASA's Goddard
Earth Sciences Data and Information Services Center (GES DISC) (Li et al., 2020). Altimetry‐based daily sea
surface heights (SEALEVEL_GLO_PHY_L4_MY_008_047) can be obtained from the Copernicus Marine
Service (European Union‐Copernicus Marine Service, 2021). SWOT Level 2 River Single‐Pass Vector Reach
Data Product, Version 2.0 is available from NASA's Earth Data (SWOT, 2024). GRDC data are available from
https://portal.grdc.bafg.de/applications/public.html?publicuser=PublicUser. Hydroweb data are available on
https://hydroweb.next.theia‐land.fr/. SWORD‐mirror is available from (Sikder et al., 2024). River cross‐section
data are available from Brazil's Hidroweb data portal https://www.snirh.gov.br/hidroweb/ and USGS’ National
Cross‐Section Database (NXSDB) (Whaling et al., 2026). Global SWOT‐fitted river bathymetry and other pa-
rameters needed to run HyMAP and replicate results are available from Getirana, Collins, et al. (2025).
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
10 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

References
Altenau, E. H., Pavelsky, T. M., Durand, M. T., Yang, X., Frasson, R. P. M., & Bendezu, L. (2021). The surface water and ocean topography
(SWOT) mission river database (SWORD): A global river network for satellite data products. Water Resources Research, 57(7),
e2021WR030054. https://doi.org/10.1029/2021WR030054
Andreadis, K. M., Clark, E. A., Lettenmaier, D. P., & Alsdorf, D. E. (2007). Prospects for river discharge and depth estimation through
assimilation of swath‐altimetry into a raster‐based hydrodynamics model. Geophysical Research Letters, 34(10), 1–5. https://doi.org/10.1029/2
007GL029721
Andreadis, K. M., Schumann, G. J. P., & Pavelsky, T. (2013). A simple global river bankfull width and depth database. Water Resources Research,
49(10), 7164–7168. https://doi.org/10.1002/wrcr.20440
Bates, P. (2023). Fundamental limits to flood inundation modelling. Nature Water, 1(7), 566–567. https://doi.org/10.1038/s44221‐023‐00106‐4
Bates, P. D., Horritt, M. S., & Fewtrell, T. J. (2010). A simple inertial formulation of the shallow water equations for efficient two‐dimensional
flood inundation modelling. Journal of Hydrology, 387(1–2), 33–45. https://doi.org/10.1016/j.jhydrol.2010.03.027
Collins, E. L., David, C. H., Riggs, R., Allen, G. H., Pavelsky, T. M., Lin, P., et al. (2024). Global patterns in river water storage dependent on
residence time. Nature Geoscience, 17(5), 433–439. https://doi.org/10.1038/s41561‐024‐01421‐5
Decharme, B., Alkama, R., Papa, F., Faroux, S., Douville, H., & Prigent, C. (2012). Global off‐line evaluation of the ISBA‐TRIP flood model.
Climate Dynamics, 38(7–8), 1389–1412. https://doi.org/10.1007/s00382‐011‐1054‐9
Durand, M., Andreadis, K. M., Alsdorf, D. E., Lettenmaier, D. P., Moller, D., & Wilson, M. (2008). Estimation of bathymetric depth and slope
from data assimilation of swath altimetry into a hydrodynamic model. Geophysical Research Letters, 35(20). https://doi.org/10.1029/2008GL0
34150
European Union‐Copernicus Marine Service. (2021). Global ocean gridded L4 sea surface heights and derived variables reprocessed (1993‐
ongoing) [Dataset]. Mercator Ocean International. https://doi.org/10.48670/MOI‐00148
Farr, T. G., Rosen, P. A., Caro, E., Crippen, R., Duren, R., Hensley, S., et al. (2007). The shuttle radar topography mission. Reviews of Geophysics,
45(2). https://doi.org/10.1029/2005RG000183
Feng, D., Gleason, C. J., Yang, X., Allen, G. H., & Pavelsky, T. M. (2022). How have global river widths changed over time? Water Resources
Research, 58(8), e2021WR031712. https://doi.org/10.1029/2021WR031712
Getirana, A., Bonnet, M.‐P., Calmant, S., Roux, E., Filho, O. C. R., & Mansur, W. J. (2009). Hydrological monitoring of poorly gauged basins
based on rainfall‐runoff modeling and spatial altimetry. Journal of Hydrology, 379(3–4), 205–219. https://doi.org/10.1016/j.jhydrol.2009.0
9.049
Getirana, A., Boone, A., Yamazaki, D., Decharme, B., Papa, F., & Mognard, N. (2012). The hydrological modeling and analysis platform
(HyMAP): Evaluation in the Amazon basin. Journal of Hydrometeorology, 13(6), 1641–1665. https://doi.org/10.1175/JHM‐D‐12‐021.1
Getirana, A., Boone, A., Yamazaki, D., & Mognard, N. (2013). Automatic parameterization of a flow routing scheme driven by radar altimetry
data: Evaluation in the Amazon basin. Water Resources Research, 49(1), 614–629. https://doi.org/10.1002/wrcr.20077
Getirana, A., Collins, E., Alcântara, E., Balsamo, G., Bates, P., Dube, T., et al. (2026). Floods in 2025. Nature Reviews Earth & Environment, 7(5),
270–273. https://doi.org/10.1038/s43017‐026‐00779‐x
Getirana, A., Collins, E. L., Kumar, S., Yoon, Y., & Nie, W. (2025a). Global SWOT‐fitted river bathymetry [Dataset]. Figshare. https://doi.org/1
0.6084/m9.figshare.30434293.v3
Getirana, A., Kumar, S., Arsenault, K., Yoon, Y., & Geiger, J. (2025). The HyMAP‐3 hydrodynamic model (technical memorandum no. NASA/
TM‐20250009546). NASA.
Getirana, A., Kumar, S., Bates, P., Boone, A., Lettenmaier, D., & Munier, S. (2024). The SWOT mission will reshape our understanding of the
global terrestrial water cycle. Nature Water, 2(12), 1139–1142. https://doi.org/10.1038/s44221‐024‐00352‐0
Greguska, F., Tebaldi, N., McDonald, V., Vanesa, Nickles, C., & Wood, J. (2025). Podaac/hydrocron: 1.6.4. https://doi.org/10.5281/zenodo.1583
1782
Jiang, L., Westphal Christensen, S., & Bauer‐Gottwein, P. (2021). Calibrating 1D hydrodynamic river models in the absence of cross‐section
geometry using satellite observations of water surface elevation and river width. Hydrology and Earth System Sciences, 25(12),
6359–6379. https://doi.org/10.5194/hess‐25‐6359‐2021
Kumar, S. V., Peters‐Lidard, C. D., Mocko, D., Reichle, R., Liu, Y., Arsenault, K. R., et al. (2014). Assimilation of remotely sensed soil moisture
and snow depth retrievals for drought estimation. Journal of Hydrometeorology, 15(6), 2446–2469. https://doi.org/10.1175/JHM‐D‐13‐0132.1
Li, B., Beaudoing, H., & Rodell, M., & Hydrological Sciences Laboratory (HSL). (2020). GLDAS catchment land surface model L4 daily 0.25 x
0.25 degree GRACE‐DA1 early product, version 2.2 [Dataset]. NASA Goddard Earth Sciences Data and Information Services Center. https://
doi.org/10.5067/IIU5JWU2AGRP
Luo, X., Li, H.‐Y., Leung, L. R., Tesfa, T. K., Getirana, A., Papa, F., & Hess, L. L. (2017). Modeling surface water dynamics in the Amazon Basin
using MOSART‐Inundation v1.0: Impacts of geomorphological parameters and river flow representation. Geoscientific Model Development,
10(3), 1233–1259. https://doi.org/10.5194/gmd‐10‐1233‐2017
Neal, J., Hawker, L., Savage, J., Durand, M., Bates, P., & Sampson, C. (2021). Estimating River channel bathymetry in large scale flood
inundation models. Water Resources Research, 57(5), e2020WR028301. https://doi.org/10.1029/2020WR028301
Nguyen, M., Wilson, M. D., Lane, E. M., Brasington, J., & Pearson, R. A. (2026). Quantifying uncertainty in flood predictions due to river
bathymetry estimation. Hydrology and Earth System Sciences, 30(1), 183–203. https://doi.org/10.5194/hess‐30‐183‐2026
Paiva, R. C. D., Collischonn, W., Bonnet, M.‐P., Gonçalves, L. G. G. D., Calmant, S., Getirana, A., & Silva, J. S. D. (2013). Assimilating in situ
and radar altimetry data into a large‐scale hydrologic‐hydrodynamic model for streamflow forecast in the Amazon. Hydrology and Earth
System Sciences, 17(7), 2929–2946. https://doi.org/10.5194/hess‐17‐2929‐2013
Pavelsky, T. M., & Smith, L. C. (2008). RivWidth: A software tool for the calculation of river widths from remotely sensed imagery. IEEE
Geoscience and Remote Sensing Letters, 5(1), 70–73. https://doi.org/10.1109/LGRS.2007.908305
Sikder, M. S., Wang, J., Allen, G. H., Sheng, Y., Yamazaki, D., Crétaux, J.‐F., & Pavelsky, T. M. (2024). HarP: Harmonized prior river‐lake
database [Dataset]. Zenodo. https://doi.org/10.5281/zenodo.14205131
Simard, M., Denbina, M., Marshak, C., & Neumann, M. (2024). A global evaluation of radar‐derived digital elevation models: SRTM,
NASADEM, and GLO‐30. Journal of Geophysical Research: Biogeosciences, 129(11), e2023JG007672. https://doi.org/10.1029/2023JG00
7672
SWOT. (2024). SWOT level 2 River single‐pass vector data product, version C [Dataset]. PO.DAAC, CA, USA. https://doi.org/10.5067/SWOT‐RI
VERSP‐2.0
Taburet, G., Sanchez‐Roman, A., Ballarotta, M., Pujol, M.‐I., Legeais, J.‐F., Fournier, F., et al. (2019). Duacs DT2018: 25 years of reprocessed sea
level altimetry products. Ocean Science, 15(5), 1207–1224. https://doi.org/10.5194/os‐15‐1207‐2019
Acknowledgments
This research was supported by NASA's
Surface Water and Ocean Topography
(SWOT) mission. Computing resources
supporting this work were provided by the
NASA High‐End Computing (HEC)
Program through the NASA Center for
Climate Simulation (NCCS) at NASA
Goddard Space Flight Center.
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
11 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License

USGS. (2007). HydroSHEDS. USGS‐Sci. Chaning World HydroSHEDS, 1–27.
Whaling, A. R., McDonald, R. R., Knight, T., LeRoy, J. Z., & Creighton, A. L. (2026). National cross‐section database (NXSDB) [Dataset]. Water
Year 2023 (schema version 1.2.0, September 2025). https://doi.org/10.5066/P13PPXKN
Yamazaki, D., Baugh, C. A., Bates, P. D., Kanae, S., Alsdorf, D. E., & Oki, T. (2012). Adjustment of a spaceborne DEM for use in floodplain
hydrodynamic modeling. Journal of Hydrology, 436–437, 81–91. https://doi.org/10.1016/j.jhydrol.2012.02.045
Yamazaki, D., Ikeshima, D., Sosa, J., Bates, P. D., Allen, G. H., & Pavelsky, T. M. (2019). MERIT hydro: A high‐resolution global hydrography
map based on latest topography dataset. Water Resources Research, 55(6), 5053–5073. https://doi.org/10.1029/2019WR024873
Yamazaki, D., Kanae, S., Kim, H., & Oki, T. (2011). A physically based description of floodplain inundation dynamics in a global river routing
model. Water Resources Research, 47(4), 1–21. https://doi.org/10.1029/2010WR009726
Yamazaki, D., O’Loughlin, F., Trigg, M. A., Miller, Z. F., Pavelsky, T. M., & Bates, P. D. (2014). Development of the global width database for
large Rivers. Water Resources Research, 50(4), 3467–3480. https://doi.org/10.1002/2013WR014664
Yoon, Y., Durand, M., Merry, C. J., Clark, E. A., Andreadis, K. M., & Alsdorf, D. E. (2012). Estimating river bathymetry from data assimilation of
synthetic SWOT measurements. Journal of Hydrology, 464–465, 363–375. https://doi.org/10.1016/j.jhydrol.2012.07.028
Yoon, Y., Getirana, A., Kumar, S. V., Collins, E., & Wegiel, J. W. (2026). Assimilation of SWOT water surface elevation enhances simulations of
river dynamics in the Ohio River Basin. Geophysical Research Letters, 53(18). https://doi.org/10.1029/2026gl122610
References From the Supporting Information
Getirana, A., Jung, H. C., Arsenault, K., Shukla, S., Kumar, S., Peters‐Lidard, C., et al. (2020). Satellite gravimetry improves seasonal streamflow
forecast initialization in Africa. Water Resources Research, 56(2), 2019WR026259. https://doi.org/10.1029/2019WR026259
Koster, R. D., Suarez, M. J., Ducharne, A., Stieglitz, M., & Kumar, P. (2000). A catchment‐based approach to modeling land surface processes in a
general circulation model: 1. Model structure. Journal of Geophysical Research, 105(D20), 24809–24822. https://doi.org/10.1029/2000JD90
0327
Kumar, S. V., Zaitchik, B. F., Peters‐Lidard, C. D., Rodell, M., Reichle, R., Li, B., et al. (2016). Assimilation of Gridded GRACE terrestrial water
storage estimates in the North American land data assimilation system. Journal of Hydrometeorology, 17(7), 1951–1972. https://doi.org/10.117
5/JHM‐D‐15‐0157.1
Li, B., Rodell, M., Kumar, S., Beaudoing, H. K. H. K., Getirana, A., Zaitchik, B. F. B. F., et al. (2019). Global GRACE data assimilation for
groundwater and drought monitoring: Advances and challenges. Water Resources Research, 55(9), 1–23. https://doi.org/10.1029/2018wr02
4618
Rousseeuw, P. J. (1991). Tutorial to robust statistics. Journal of Chemometrics, 5(1), 1–20. https://doi.org/10.1002/cem.1180050103
Rousseeuw, P. J., & Hubert, M. (2018). Anomaly detection by robust statistics. WIREs Data Mining and Knowledge Discovery, 8(2), e1236.
https://doi.org/10.1002/widm.1236
Geophysical Research Letters
10.1029/2026GL125708
GETIRANA ET AL.
12 of 12
 19448007, 2026, 19, Downloaded from https://agupubs.onlinelibrary.wiley.com/doi/10.1029/2026GL125708, Wiley Online Library on [08/10/2026]. See the Terms and Conditions (https://onlinelibrary.wiley.com/terms-and-conditions) on Wiley Online Library for rules of use; OA articles are governed by the applicable Creative Commons License
