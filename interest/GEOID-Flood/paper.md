---
title: 'GEOID-Flood: A Large-Scale Multi-Modal Benchmark Dataset for Flood Segmentation'
authors: Gaetano Chiriaco; Luca Barco; Andrea Bragagnolo; Claudio Rossi; Edoardo Arnaudo
year: '2026'
venue: ''
---

GEOID-Flood: A Large-Scale Multi-Modal
Benchmark Dataset for Flood Segmentation
Gaetano Chiriaco1 , Luca Barco1,2 , Andrea Bragagnolo1 , Claudio Rossi1 ,
and Edoardo Arnaudo1
1 Fondazione LINKS, Via Pier Carlo Boggio, 61, 10138 Torino, Italy
{name}.{surname}@linksfoundation.com
2 Politecnico di Torino, Corso Duca degli Abruzzi 24, 10129 Torino, Italy
{name}.{surname}@polito.it
Abstract. Geospatial foundation models aim to learn representations
that transfer across regions and sensors, yet evaluating them on specific
tasks requires large, high-quality, multi-modal benchmarks that measure
how well such models extract value from data. Concerning flood map-
ping, existing datasets rarely combine bi-temporal SAR and co-registered
optical imagery at scale, leaving the value of foundation models for this
downstream task largely untested. We introduce GEOID-Flood3, a large-
scale multi-modal flood segmentation benchmark, derived from Coper-
nicus Emergency Management Service activations, spanning 219 events
across 65 countries over ten years. The dataset provides more than 14 000
tiles with co-registered pre- and post-event Sentinel-1, in GRD and RTC
format, pre-event Sentinel-2 composite, and DEM, including manually
validated labels that separate background from permanent water and
flooded water. Using this benchmark, we evaluate foundation models
against conventional encoders across single-image, multi-temporal, and
multi-modal protocols. We report three main findings: foundation models
offer a consistent but modest advantage; optical–SAR fusion with fine-
tuning best resolves transient flooding; and models trained on GEOID-
Flood
transfer to unseen events better than those trained on existing
datasets.
Keywords: Flood Segmentation · Synthetic Aperture Radar · Geospa-
tial Foundation Models · Benchmark Dataset
1
Introduction
Floods are among the most frequent and damaging natural hazards, affecting
more people worldwide than any other weather-related disaster, and both their
frequency and severity are projected to rise under a warming climate [8, 18].
To reduce and quantify their impact, there is a growing need to map flood ex-
tent rapidly and over wide areas. Remote Sensing has become the backbone of
operational flood monitoring [25, 36], where mapping must stay reliable under
3 https://github.com/links-ads/geoid-flood
arXiv:2608.02315v1  [cs.CV]  3 Aug 2026

2
G. Chiriaco et al.
Fig. 1: Representative tiles from three GEOID-Flood events. From left to right:
pre- and post-event Sentinel-1 GRD and RTC (VV/VH format), pre-event Sentinel-2
(RGB), DEM, and label. Flooded water is shown in cyan, permanent water in blue,
invalid pixels in gray.
cloud cover, at night, and across wide geographic extents. Synthetic Aperture
Radar (SAR) meets these requirements, but open water is intrinsically ambigu-
ous in Sentinel-1 backscatter: a single acquisition rarely separates permanent
rivers and reservoirs from newly inundated terrain. Resolving this ambiguity
demands temporal context (pre/post-event change), together with annotations
that distinguish transient flooding from both background soil and permanent wa-
ter bodies. Meeting these requirements at operational scale, i.e., across diverse
regions, events, and sensors, points to two needs: representations that general-
ize beyond their training conditions, and benchmarks rich enough to evaluate
whether they do.
Deep learning, and in particular geospatial foundation models pretrained
on large Earth-observation corpora, offers a promising answer to the first. The
second, however, remains under-explored: existing datasets rarely meet the cri-
teria needed to evaluate such models [9]. To our knowledge, no public dataset
combines bi-temporal SAR for pre- and post-event scenes, co-registered optical
imagery for multi-modal fusion, and event-level train/test splits at continental
scale.
We address this gap with GEOID-Flood (Geospatial Earth Observation Im-
agery Dataset for Floods), a large-scale flood benchmark derived from Coperni-
cus Emergency Management Service (CEMS) activations. It covers 1 141 749 km2
of flood-affected terrain, nearly double the largest prior dataset and the widest
spatial extent reported to date over the longest acquisition window so far (2016–
2026). Unlike existing benchmarks, which typically provide one or two sensors,
GEOID-Flood jointly offers bi-temporal Sentinel-1 (S1), in GRD and RTC vari-
ants, Sentinel-2 (S2), and a Digital Elevation Model (DEM), and pairs these
inputs with a dedicated permanent water layer, so that transient flooding is
annotated separately from background and permanent water (Fig. 1).

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
3
Table 1: Comparison of satellite-based flood segmentation datasets.
JRC-GSW: JRC Global Surface Water; OSM: OpenStreetMap; HL: hand-labeled; AEF:
AlphaEarth-derived.
⋆Image size reported as the average size of raw tiles.
Dataset
Modality
Resolution
Image size
Events Tiles Area (km2) Temporal Coverage
Perm. water
FloodNet [31]
RGB (drone)
VHR
4 000 × 3 000
1
2 343
N/A
post
2017
–
Sen1Floods11 [3]
S1, S2
10 m
512 × 512
11
4 831
120 406
post
2016–2019 JRC-GSW, HL
ETCI 2021 [17]
S1
10 m
256 × 256
5
33 405
36 623
post
2017–2019
N/A
WorldFloods v2 [30]
S2
10 m
3 443 × 3 204⋆
144
509
586 618
post
2016–2023
JRC-GSW
MMFlood [27]
S1, DEM
20 m
909 × 993⋆
95
1 748
137 659
post
2014–2021
OSM hydro.
OmbriaNet [10]
S1, S2
10 m
256 × 256
23
844
553
pre+post 2017–2021
CEMS
Kuro Siwo [4]
S1, DEM
10 m
224 × 224
43
67 490
338 000
pre+post 2015–2022
HL
CAU-Flood [15]
S1, S2
10 m
256 × 256
18
18 302
95 142
pre+post 2016–2022
HL
S1GFloods [34]
S1
10 m
256 × 256
46
5 360
35 127
pre+post 2015–2022
HL
STURM-Flood [28]
S1
10 m
128 × 128
47
21 602
35 399
post
2016–2024
OSM
S2
29
2 675
GEOID-Flood
S1, S2, DEM
10 m
1 024 × 1 024
219
14 282
1 141 749
pre+post 2016–2026
AEF
This design lets us study representation quality and temporal modelling in
a single, controlled setting. We organize our analysis around four research ques-
tions that link the dataset (Sec. 3) to the methodological choices (Sec. 4) and
experiments (Sec. 5):
– RQ1 (pretraining): how do geospatial foundation models compare to other
pretrained encoders, and does finetuning beat frozen features?
– RQ2 (temporal): Is modelling the flood class with a specific loss or archi-
tecture better than deriving it with post-hoc water-body delineation?
– RQ3 (modality): considering multi-modal encoders, which inputs most im-
prove flood and permanent-water discrimination (e.g., optical, RTC, GRD)?
– RQ4 (generalization): does training on GEOID-Flood transfer to unseen,
out-of-period events better than existing benchmarks?
In an attempt to answer these questions, we provide three contributions:
(1) GEOID-Flood, a global flood benchmark dataset with a dedicated permanent
water layer and multi-sensor co-registration at scale; (2) a reproducible train-
ing and evaluation protocol, from single-image binary segmentation to multi-
temporal multi-class segmentation; and (3) an extensive backbone benchmark
for flood detection and water body segmentation, comparing foundation models
against conventional backbones and GEOID-Flood against existing datasets.
2
Related Work
Flood Mapping Datasets. Considering flood-specific datasets, there is little
shared consensus on input modalities or temporal modelling. Optical datasets
such as WorldFloods [26,30] lack SAR entirely, while SAR-centric datasets such
as MMFlood [27], Kuro Siwo [4], and S1GFloods [34] provide no optical counter-
part, and Sen1Floods11 [3] pairs the two only at a single flood-time acquisition,
precluding bi-temporal change analysis. Datasets that do combine SAR and op-
tical (OmbriaNet [10], CAU-Flood [15], and STURM-Flood [28]) are, however,

4
G. Chiriaco et al.
missing pre-event SAR or remain largely unpaired (CAU-Flood pairs pre-event
S2 with post-event S1 only; STURM-Flood supplies 21 602 S1 tiles but only
2 675 corresponding S2 images). Furthermore, none of them distinguishes flood-
ing from permanent water.
Annotation strategies vary widely. Existing labels range from automatically
derived or weakly supervised masks (i.e., prone to systematic noise, especially
from optical composites under flood-time cloud cover) to fully manual delin-
eations, as in Kuro Siwo, re-annotated by SAR specialists, or Sen1Floods11,
which hand-labels only 446 of its 4 831 tiles (<10%). Manual annotation, how-
ever, is not by itself a guarantee of quality: as Fig. 3 shows, hand-drawn de-
lineations do not necessarily yield cleaner or more accurate boundaries than
well-curated automated products.
SAR processing heterogeneity is a further issue: datasets distribute SAR at
different processing levels and value ranges (e.g., raw GRD [27], terrain-corrected
RTC [4]) with no common normalization, hindering cross-dataset evaluation and
operational deployment. Split design is also often overlooked. Several datasets
adopt random tile-level splits that risk spatial leakage between train and test [10,
28,31], possibly compromising reported performance.
Finally, permanent water derivation is far from standardized. MMFlood adopts
OpenStreetMap hydrography [27], although incomplete, while the JRC Global
Surface Water product [29] used by WorldFloods and Sen1Floods11 is Landsat-
derived at 30 m and lacks most narrow rivers and small water bodies. In both
cases, these systematic gaps propagate into the flood label. Table 1 summarizes
the properties of existing flood datasets.
GEOID-Flood is designed to address these limitations jointly. It pairs fully
co-registered pre- and post-event Sentinel-1 with a cloudless pre-event Sentinel-2
composite as optical reference; distributes SAR at two standardized processing
levels (GRD and RTC), removing the cross-dataset normalization gap; draws its
ground truth from manually curated CEMS delineations that prioritize SAR-
derived sources, sidestepping cloud-induced optical noise; derives a dedicated
permanent water layer from AlphaEarth Foundations embeddings [5] to sepa-
rate permanent from flooded water; and adopts event-level partitioning with a
temporally disjoint held-out test set to rule out spatial leakage.
Flood Delineation Methods. Classical approaches to SAR-based flood de-
lineation apply intensity thresholding or fuzzy-logic rules to exploit the low
backscatter signature of open water [25, 36]. These methods remain competi-
tive baselines on small, homogeneous scenes but degrade in urban areas, dense
vegetation, and turbulent water conditions. Deep learning segmentation has
largely replaced classical methods on benchmark tasks. Fully convolutional net-
works applied to SAR data [20] and encoder-decoder architectures based on
U-Net [33] and DeepLabV3+ [6] dominate current flood-segmentation bench-
marks. Change detection architectures, including dual-branch transformers [1]
and Siamese networks applied to SAR pairs [40], have demonstrated strong per-
formance in flood detection tasks. The recent success of geospatial foundation
models has extended transferable representations to many downstream tasks in-

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
5
cluding land-cover mapping, crop monitoring, and disaster assessment. Models
such as OlmoEarth [16], DOFA [39], and TerraMind [19] have demonstrated
strong generalization across different sensors and areas. Their growing adoption
and increasing number of different foundation models and approaches have ex-
posed the need to rigorously benchmark these models on complex tasks, with
large-scale, robust datasets [9].
3
The GEOID-Flood Dataset
GEOID-Flood is a large-scale, multi-modal benchmark for flood segmentation,
pairing co-registered Sentinel-1 SAR and Sentinel-2 optical imagery with manu-
ally filtered flood masks derived from CEMS Rapid Mapping activations. It spans
219 flood events across 65 countries and a decade of acquisitions, capturing a
diversity of climates, land cover, and sensor conditions absent from existing flood
datasets. We detail the data sources, the construction pipeline, and the resulting
statistics in the next sections.
3.1
Data sources
Each CEMS activation corresponds to a flood event and contains one or more
Areas of Interest (AoIs), regions impacted by the event. Large-scale events can
have dozens of AoIs of heterogeneous sizes and shapes. For every pair of event
and AoI, CEMS publishes a series of vector delineation products over the hours
and days following the disaster, progressively refining the mapped flood extent
as new satellite acquisitions become available. Each product is associated with
a pre-event reference image, used to assess the situation before the disaster,
and a post-event image, which depicts the situation after the flood. We select
a single product per pair: we prioritize products derived from Sentinel-1 and
Sentinel-2 imagery, so that annotation and training data share the same sen-
sor and resolution; when no Sentinel-derived product exists, we select the first
available product with the highest quality, following CEMS directives [7] (in de-
creasing order: Grading, Delineation Monitoring, Delineation, First Estimate).
All selected labels were manually inspected and corrected where necessary.
Each product carries three reference dates: the event date (when the flood
occurred), the pre-event image date, and the post-event image date, the latter
two being the acquisition dates of the satellite scenes used to produce the fi-
nal analysis. It also records a sensor field, namely the satellite from which each
acquisition was derived. For each event-AoI pair, the recorded date and sensor
determine which acquisition we retrieve: if the sensor is Sentinel-1 and the ex-
act post-event scene used by CEMS analysts is available, we retrieve that same
scene; otherwise, we take the closest available acquisition after the event date.
We mirror this procedure for the pre-event acquisition, taking the image cor-
responding to the reported pre-event date, or nearest acquisition preceding the
event date instead.
Four satellite sources are co-registered at 10 m ground sampling distance:
Sentinel-1 Ground Range Detected (GRD) and Radiometrically Terrain-Corrected

6
G. Chiriaco et al.
(RTC) products (VV and VH polarizations, pre- and post-event), a pre-event
Sentinel-2 composite (Level-2A surface reflectance, 12 spectral bands resampled
to 10 m), and the Copernicus GLO-30 DEM [11] as a static elevation layer.
3.2
Construction pipeline
Dataset construction comprises five automated and reproducible stages operat-
ing directly on public Copernicus products:
Spatial partitioning. Using metadata from each CEMS activation, we subdivide
each variable AoI into regular 10 240 m square bounding boxes aligned to UTM
grids, giving a consistent spatial footprint across events.
Data retrieval. For each AoI we retrieve Sentinel-1 GRD and RTC at both
the pre- and post-event dates through the Sentinel Hub APIs [35]. Sentinel-2
is retrieved for the pre-event period only: floods are typically accompanied by
persistent cloud cover which, compounded by the optical revisit interval, makes a
clear acquisition near the post-event delineation date extremely unlikely [30] (see
Fig. 3). Given the optical source, we minimize the cloud coverage by applying
a median composite over each tile, selecting a window of three weeks from the
event date, and a maximum of 3 S2-L2A acquisitions. Considering terrain, we
download the Copernicus GLO-30 DEM and resample it to the 10 m grid as an
additional static layer.
Validity mask generation. We derive two validity masks. Despite the median
composite, certain geographical areas may still display cloud coverage. For this
reason, an auxiliary cloud mask is produced by running OmniCloudMask [38] on
the pre-event Sentinel-2 scene, yielding per-pixel clear, thin, or thick labels. We
further generate a pixel validity mask that marks usable pixels as the intersection
of the AoI boundary, the image footprint, and the tile bounding box.
Label composition. CEMS products map flood extent but not permanent water;
since single-image water segmentation must distinguish the two, separating these
classes is a core design decision of GEOID-Flood. As existing global layers are
unsuitable at our resolution (Sec. 2), we provide a dedicated 10 m permanent
water layer by training a lightweight model on the Earth Surface Water (ESW)
dataset [24] from annual AlphaEarth Foundations (AEF) embeddings [5] (full
details and examples in Sec. B). We rasterize into flood labels only those CEMS
polygons explicitly categorized as flood, excluding trace-level annotations. The
final label merges these layers into background, permanent water, flooded water,
and invalid, the last assigned to pixels under thick cloud when the cloud mask
is selected, or outside the validity mask.
Quality filtering. We discard bounding boxes that had missing or partial modal-
ities, excessive cloud cover, or imagery inconsistent with the reference label; this
is common in flash floods, where even a small acquisition-to-delineation gap
misaligns annotations.

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
7
Fig. 2:
Global distribution of GEOID-Flood AoIs, colored by split assignment
(train/validation/test). The inset enlarges Europe, where touching AoIs share a split
to prevent boundary leakage.
3.3
Dataset statistics
GEOID-Flood covers 219 flood events spanning January 2016 to March 2026, of
which the most recent form a temporally disjoint held-out set reserved for cross-
dataset experiments. The dataset spans 65 countries across six continents, with
a minimum of 13 up to a maximum of 30 events per year. The events decom-
pose into 1 055 valid event-AoI pairs, derived from applying the quality filtering
stage described above to a pool of 1 333 candidate areas. Each pair may yield
one or more 10 240 m bounding boxes, producing a total of 14 282 valid tiles at
1024 × 1024 pixels. Every tile provides a complete (S1pre, S1post, S2pre, DEM)
tuple of curated, ML-ready imagery. Given the source catalog, Europe dominates
the geographic distribution with 140 events, as shown in Fig. 2. However, sev-
eral large-scale events have been mapped across the globe, and we deliberately
ensured that regions outside Europe remain well represented across splits.
Specifically, AoIs are stratified by continent and sampled with target propor-
tions of 70/10/20 % for training, validation and test respectively, so that every
region is proportionally represented in each subset. To prevent boundary leakage,
adjacent or overlapping AoIs are constrained to the same split, keeping spatially
contiguous areas together (see Fig. 2). This event-level partitioning yields 8 938
tiles for training, 1 241 for validation, and 2 674 for testing. A further 1 429 tiles,
drawn from events post-dating January 2026, form the temporally disjoint held-
out set, used exclusively for the cross-dataset comparison of Sec. 5.5. Figure 1
shows representative tiles from three GEOID-Flood events with all modalities
and label layers; Fig. 3 gives a side-by-side comparison with literature datasets
on a shared event.
Held-out set To support cross-dataset generalization experiments, we con-
struct a dedicated held-out test set from CEMS activations published after Jan-
uary 2026 (EMSR857–EMSR871, 83 event-AoI pairs, spanning February–March
2026). The chosen window (February–March 2026) provides a sufficient number
of activations to be used as a test set while remaining temporally disjoint, by

8
G. Chiriaco et al.
Fig. 3: Visual comparison of GEOID-Flood against other popular datasets on a shared
area. First row: available labels, second row: corresponding post-event modality of each
dataset.
construction, from our own splits and all the other datasets mentioned in Sec. 2.
The held-out set follows the same construction pipeline and modality structure
as the main dataset, and is used exclusively for the cross-dataset experiments in
Sec. 5.5.
4
Methodology
We benchmark geospatial foundation models and conventional encoders on GEOID-
Flood under a shared training protocol (Sec. A.3), aimed at answering the re-
search questions of Sec. 1. After defining the segmentation task (Sec. 4.1), we
organize the experiments into three training scenarios of increasing complexity
(Sec. 4.2): a single-image backbone benchmark (RQ1); paired training that in-
troduces explicit flood supervision (RQ2); and fusion that adds optical context
(RQ3). Two further studies, reported in Sec. 5, complete the picture: a modality
ablation that isolates input contributions (RQ3, Sec. 5.4) and a cross-dataset
protocol that measures generalization to unseen events (RQ4, Sec. 5.5).
4.1
Task formulation
We formulate flood mapping as a per-pixel semantic segmentation problem. Each
tile carries a three-class label: background, permanent water, and flooded water.
We evaluate models in both single-image and multi-image settings, each with
its own target formulation. A single SAR acquisition does not, in general, pro-
vide enough evidence to separate flooded water from permanent water, as both
yield similarly dark returns in VV/VH backscatter. For single-image training we
therefore reduce the problem to a binary water-body segmentation, remapping
labels according to the acquisition time step: on pre-event tiles, flooded pixels
are relabelled as background, since inundation is only meaningful after the event;
on post-event tiles, flooded and permanent water are merged into a single water

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
9
class, so the target reflects total surface-water extent. When pre- and post-event
images are processed jointly, temporal context makes the two water classes sep-
arable, and the full three-class target is retained. In all settings, pixels outside
the CEMS analysis area and other invalid pixels are excluded from the loss.
4.2
Training scenarios
The single-image and multi-image settings of Sec. 4.1 instantiate as three scenar-
ios of increasing temporal and modal complexity. Scenario (i) is run across the
full encoder zoo (Sec. A.1) as our backbone comparison; since scenarios (ii)–(iii)
probe temporal and multi-modal design choices rather than the backbone itself,
we fix the encoder there to a single backbone selected from (i).
(i) Single-image. Pre- and post-event crops are treated as independent samples:
the model performs one forward pass per tile, trained with cross-entropy (CE)
on the remapped binary water-body labels from Sec. 4.1. This is our primary
instrument for ranking frozen and finetuned foundation models against conven-
tional ImageNet-pretrained encoders (RQ1); its binary predictions also form the
post-hoc three-class baseline against which explicit flood modelling is measured
(RQ2).
(ii) Paired, two-pass. We draw co-registered pre-/post-event pairs and apply the
same encoder-decoder to each time step in two separate forward passes, summing
the two CE terms under the binary remapping of (i). To this we add a flood-
change loss (RQ2): a binary CE term on pixels that are water post-event but
not pre-event, sharpening sensitivity to the flooded-water class. We further vary
the pre-event modality (RQ3): the default S1 →S1 pairing is compared against
S2 →S1 (optical pre-event, radar post-event) and S1 + S2 →S1 (both pre-event
modalities), testing whether pre-event optical context helps.
(iii) Paired, single-pass (fusion). Both images enter in a single forward pass and
the target retains its full three-class structure (RQ2). We compare two fusion
strategies: early fusion stacks the two acquisitions along the channel dimension
through one encoder-decoder, while mid fusion encodes each in a separate branch
and merges the feature maps by element-wise subtraction (post minus pre) be-
fore a shared decoder. Each strategy is run on three pre-/post-event pairings:
Sentinel-1 GRD alone (S1), the pre-event Sentinel-2 image with post-event SAR
(S2 →S1), and an optically augmented stack (S1 + S2) that concatenates the
two modalities. Contrasting (iii) with (i)–(ii) (Sec. 5.1) isolates the benefit of
explicit over post-hoc flood modelling (RQ2).
5
Experiments
5.1
Evaluation protocol
All models and scenarios are evaluated on the test split (Sec. 3.3) under two tasks:
a generic binary water-body segmentation (water vs. background, on remapped

10
G. Chiriaco et al.
labels) and a specific multiclass flood detection (background, permanent wa-
ter, flooded water), using a standard U-Net decoder in every configuration. For
single-image and paired models (scenarios (i) and (ii)), the three-class map is
derived at inference without a dedicated head: we run the binary model on the
pre- and post-event tiles, combine the two water masks, and assign flood as their
pre-/post-event difference. Scenario (iii) predicts the three classes directly. We
report both tasks in F1 score and Intersection over Union (IoU), where the sub-
script avg indicates macro-averaged results, and take IoUflood as the primary
reference metric for flood detection. Throughout, we use binary for water-body
delineation results and multiclass for flooded-area delineation.
5.2
Model benchmark
Table 2 addresses RQ1 across the full encoder zoo under scenario (i), while Fig. 4
shows some inferences on the test set. Both show how narrow the gap is: all mod-
els but the frozen Satlas Swin-B fall within a 0.04 range of binary IoU (0.844–
0.884). The finetuned version of TerraMind-L reaches the best results (IoUbin
0.884, F1bin 0.936). However, Swin-T reaches 0.873 IoU while being nearly an
order of magnitude smaller (32 M vs. 323 M), matching or outperforming every
finetuned foundation model except TerraMind in base and large variants. The
gap between geospatial foundation models and ImageNet-pretrained encoders is
therefore small under this shared protocol: with a strong shared decoder and ade-
quate training, the backbone is not the bottleneck, and most encoders converge to
similar scores, leaving remote sensing-specific pre-training a consistent but mod-
est edge on SAR water segmentation. Finetuning gives small gains to already
robust backbones, but provides sizable gains for weaker or smaller ones (e.g.,
Satlas Swin-B, 0.751 →0.861). While binary water segmentation is well handled
across the benchmark, the flood class remains harder to tackle, with the highest
IoUflood at 0.484. This motivates the need for flood-specific approaches, presented
in the following sections. Guided by the benchmark, we adopt TerraMind-B for
all remaining experiments, given its balance between accuracy and practical-
ity for operational use: negligible loss in performance w.r.t. the top performing
model, at roughly a third of the parameters (101 M vs. 323 M).
5.3
Paired and change-focused extensions
Focusing now on RQ2, we investigate whether temporal pairing improves on
the single-image baseline, and whether explicitly modelling the flood change
can further improve performance. Table 3 reports a progression of increasingly
explicit flood modelling approaches, from single-image differencing (scenario (i)),
to paired options in double and single pass (scenarios (ii)–(iii)), while Fig. 5
shows representative inferences across these scenarios on the test set.
For scenario (ii), the paired flood-change loss matches the post-hoc base-
line on binary water when frozen but trails it on flooded water; finetuning
lifts IoUflood only marginally over the baseline (0.486 vs. 0.479). Considering

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
11
Table 2: Single-modality (Sentinel-1 GRD) benchmark on the GEOID-Flood test split.
All models are trained under scenario (i) (Sec. 4.2). Metrics follow Sec. 5.1.
Binary
Multiclass
Model
Params (M)
F1
IoU
IoUbg
IoUperm
IoUflood
IoUavg
F1avg
Frozen Encoder Foundation Models
TerraMind-T
12.33 (6.90)
0.926
0.868
0.974
0.823
0.460
0.752
0.840
TerraMind-S
30.92 (9.44)
0.924
0.866
0.973
0.827
0.448
0.749
0.837
TerraMind-B
100.87 (15.53)
0.931
0.877
0.975
0.849
0.478
0.767
0.851
TerraMind-L
322.83 (20.32)
0.934
0.881
0.976
0.856
0.484
0.772
0.854
DOFA-B
126.92 (15.53)
0.924
0.864
0.973
0.797
0.450
0.740
0.831
DOFA-L
357.53 (20.32)
0.921
0.861
0.972
0.792
0.444
0.736
0.828
OlmoEarth-B
104.48 (15.53)
0.925
0.867
0.974
0.808
0.445
0.742
0.832
SSL4EO (RN-50)
37.98 (12.43)
0.910
0.844
0.969
0.771
0.413
0.718
0.813
Satlas Swin-B
92.72 (12.27)
0.842
0.751
0.952
0.592
0.213
0.586
0.690
Finetuned Encoder Foundation Models
TerraMind-T
12.33
0.926
0.869
0.974
0.823
0.461
0.753
0.840
TerraMind-S
30.92
0.926
0.868
0.973
0.824
0.469
0.756
0.843
TerraMind-B
100.87
0.932
0.878
0.975
0.856
0.479
0.771
0.853
TerraMind-L
322.83
0.936
0.884
0.977
0.871
0.478
0.775
0.855
DOFA-B
126.92
0.929
0.873
0.975
0.833
0.477
0.761
0.847
DOFA-L
357.53
0.928
0.872
0.974
0.822
0.471
0.756
0.843
OlmoEarth-B
104.48
0.926
0.868
0.973
0.830
0.484
0.757
0.845
SSL4EO (RN-50)
37.98
0.920
0.858
0.972
0.813
0.428
0.737
0.827
Satlas Swin-B
92.72
0.921
0.861
0.972
0.813
0.449
0.745
0.834
ImageNet-Pretrained Supervised Backbones
ResNet-50
29.34
0.919
0.857
0.971
0.808
0.431
0.737
0.827
ResNet-101
48.33
0.916
0.853
0.971
0.800
0.421
0.731
0.822
ConvNeXt-T
32.34
0.924
0.866
0.973
0.829
0.446
0.749
0.837
ConvNeXt-B
92.35
0.928
0.871
0.974
0.846
0.462
0.760
0.845
Swin-T
32.04
0.929
0.873
0.974
0.847
0.469
0.763
0.848
Swin-B
91.53
0.925
0.866
0.973
0.828
0.454
0.752
0.839
scenario (iii), ad-hoc feature fusion is a viable approach, but only when fine-
tuned. Both fusion variants sit near or below the baseline when frozen; early
fusion suffers most, as its single shared encoder must represent both acquisitions
identically, whereas mid fusion may benefit from separate branches. Finetuning
lifts both above the baseline, suggesting that the gain derives from learning the
change end-to-end rather than from pairing.
Anticipating RQ3, adding optical context proves decisive. Finetuned early
fusion reaches the best flooded-water IoU (0.521) and binary water (F1bin 0.942),
and how the optical is included has little effect on results: using the pre-event
Sentinel-2 composite in place of the pre-event SAR (S2 →S1) matches stacking
it onto the bi-temporal SAR (S1 + S2).
5.4
Modality ablation
Given the available multi-modal encoders and the fusion results, we investi-
gate which inputs are most effective in this context (RQ3). Isolating a frozen
TerraMind-B, we vary only the input stack across the four available modali-
ties (S1-GRD, S1-RTC, S2-L2A, DEM) in different combinations (Tab. 4). Since

12
G. Chiriaco et al.
Fig. 4: Qualitative comparison on three GEOID-Flood test events (rows) (Sec. 4.2),
using five different encoders, finetuned under scenario (i)
Table 3: Results of scenarios on GEOID-Flood: the single-image baselines (i); paired
double-pass (ii), and fusion-based (iii).
Binary
Multiclass
Scenarios
Enc.
Input
F1
IoU
IoUbg
IoUperm
IoUflood
IoUavg
F1avg
(i) Single-image
Post-hoc 3-class
Fr.
S1
0.931
0.877
0.975
0.849
0.478
0.767
0.851
Post-hoc 3-class
FT
S1
0.932
0.878
0.975
0.856
0.479
0.771
0.853
(ii) Paired, two-pass
Flood loss
Fr.
S1
0.929
0.873
0.974
0.840
0.465
0.760
0.845
Flood loss
Fr.
S2→S1
0.920
0.858
0.972
0.839
0.430
0.747
0.833
Flood loss
Fr.
S1+S2→S1
0.924
0.865
0.973
0.854
0.449
0.759
0.843
Flood loss
FT
S1
0.933
0.879
0.975
0.860
0.486
0.774
0.855
Flood loss
FT
S2→S1
0.931
0.876
0.975
0.868
0.486
0.776
0.857
Flood loss
FT
S1+S2→S1
0.929
0.872
0.974
0.863
0.491
0.776
0.857
(iii) Paired, single-pass (fusion)
Early fusion
Fr.
S1
0.921
0.861
0.972
0.844
0.407
0.741
0.827
Mid fusion
Fr.
S1
0.925
0.867
0.973
0.833
0.476
0.761
0.847
Early fusion
Fr.
S2→S1
0.933
0.878
0.975
0.897
0.443
0.772
0.849
Mid fusion
Fr.
S2→S1
0.936
0.883
0.976
0.895
0.467
0.779
0.856
Early fusion
Fr.
S1+S2→S1
0.929
0.873
0.974
0.898
0.440
0.771
0.848
Mid fusion
Fr.
S1+S2→S1
0.937
0.887
0.977
0.896
0.488
0.787
0.863
Early fusion
FT
S1
0.937
0.886
0.977
0.872
0.494
0.781
0.861
Mid fusion
FT
S1
0.937
0.886
0.977
0.885
0.490
0.784
0.862
Early fusion
FT
S2→S1
0.942
0.895
0.979
0.906
0.521
0.802
0.875
Mid fusion
FT
S2→S1
0.940
0.890
0.978
0.905
0.499
0.794
0.868
Early fusion
FT
S1+S2→S1
0.941
0.892
0.978
0.902
0.521
0.800
0.874
Mid fusion
FT
S1+S2→S1
0.942
0.894
0.979
0.911
0.513
0.801
0.873
Sentinel-2 is unavailable post-event, we restrict the ablation to pre-event tiles,
where flooded water is absent and the task reduces to water-body delineation.
The Sentinel-1 product is not as influential as one may think; however, GRD
consistently edges out RTC (IoUbin 0.931 vs. 0.922), suggesting that terrain
backscatter correction might not matter in this case, and resampling might even
introduce slight artifacts. Likewise, the DEM stays within noise of the baseline

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
13
Fig. 5: Qualitative comparison on three GEOID-Flood test events (rows) (Sec. 4.2)
across the scenarios of Tab. 3: the single-image baseline (i, TerraMind-B on S1), the
paired double-pass model (ii), and early- and mid-fusion (iii).
Table 4: Modality ablation results on GEOID-Floodwith different input combinations.
SAR
S2-L2A
DEM
F1bin
IoUbin
S1 GRD
–
–
0.963±0.002
0.931±0.003
✓
–
0.972±0.001
0.946±0.001
–
✓
0.965±0.002
0.934±0.003
✓
✓
0.972±0.001
0.947±0.002
S1 RTC
–
–
0.958±0.002
0.922±0.004
✓
–
0.965±0.001
0.935±0.003
–
✓
0.960±0.004
0.924±0.006
✓
✓
0.970±0.001
0.942±0.004
(0.931 →0.934, within ±0.003 std), indicating that raw elevation data might be
redundant when paired with the SAR signal. Pre-event Sentinel-2 instead helps
most by a wide margin (+0.015, to 0.946), enriching features with optical in-
formation. Nevertheless, we do not rule out that purpose-built or more recent
encoders could better exploit all these modalities; we therefore retain them in
the released dataset to support future work.
5.5
Cross-dataset generalization
Finally, we assess whether training on GEOID-Flood generalizes to unseen events
better than existing benchmarks (RQ4). We train the same U-Net (TerraMind-
B), frozen and finetuned, on each of Kuro Siwo [4], MMFlood [27], World-
Floods v2 [30], and Sen1Floods11 [3], and evaluate every model on the held-
out set (Sec. 3.3). The external datasets follow widely different SAR prepro-
cessing conventions (Fig. 3); to remove this as a confounder, we re-download
and reprocess every scene through a common Sentinel-1 RTC pipeline (terrain-
flattened γ0, GLO-30 DEM, 10 m; Sec. 3.1) and apply the same channel nor-
malization throughout. Sentinel-1 sources are re-acquired at their original dates,

14
G. Chiriaco et al.
Table 5: Cross-dataset generalization results, training on the selected dataset and
testing on the GEOID-Flood held-out set, composed of flood events in 2026.
Binary
Multiclass
Training set
F1
IoU
IoUbg
IoUperm
IoUflood
IoUavg
F1avg
Frozen encoder
MMFlood [27]
0.873
0.790
0.954
0.520
0.512
0.662
0.779
Sen1Floods11 [3]
0.851
0.759
0.938
0.499
0.463
0.633
0.755
WorldFloods v2 [30]
0.882
0.802
0.954
0.655
0.515
0.708
0.816
Kuro Siwo [4]
0.887
0.809
0.963
0.543
0.568
0.691
0.803
GEOID-Flood
0.911
0.845
0.971
0.709
0.590
0.757
0.852
Finetuned encoder
MMFlood [27]
0.758
0.659
0.943
0.202
0.380
0.509
0.619
Sen1Floods11 [3]
0.879
0.797
0.956
0.648
0.504
0.703
0.811
WorldFloods v2 [30]
0.877
0.795
0.954
0.650
0.492
0.698
0.808
Kuro Siwo [4]
0.888
0.811
0.957
0.635
0.544
0.712
0.820
GEOID-Flood
0.917
0.854
0.972
0.716
0.601
0.763
0.857
while WorldFloods v2, annotated on Sentinel-2, is paired with its temporally
closest Sentinel-1 scene, dropping pairs more than two days apart. Because pre-
processing and normalization are shared and no model has seen any held-out
event, models differ only in the training set they learned from.
GEOID-Flood is the strongest training source in both regimes. On binary wa-
ter it transfers best, ahead of every external source including the CEMS-derived
Kuro Siwo, and the three-class metrics follow the same ordering. Among external
sources, Kuro Siwo transfers best on binary water and WorldFloods v2 on the
three-class task (F1avg 0.816), the latter notable given its optical-derived labels.
Finetuning the source does not overturn this ordering and is dataset-dependent:
it clearly helps Sen1Floods11 but destabilizes MMFlood, whose strong flood/non-
flood imbalance makes full finetuning harder (IoUflood 0.512→0.380).
Since the held-out permanent water labels share GEOID-Flood ’s derivation,
the binary water lead is partly expected; the flood metrics, independently derived
from CEMS, confirm that scale and diversity yield genuine transfer gains.
6
Conclusion
We introduced GEOID-Flood, a large-scale multi-modal flood benchmark from
Copernicus EMS Rapid Mapping activations. Benchmarking geospatial founda-
tion models against ImageNet-pretrained encoders, we find that training design
matters more than the encoder: foundation models hold only a modest edge,
temporal pairing alone does not help, and the best results come from end-to-end
change-focused architectures and optical-SAR fusion. Training on GEOID-Flood
also transfers to unseen events better than every benchmark we evaluate, in both
regimes. Some limitations remain: coverage is geographically skewed towards Eu-
rope (140 of 219 events), labels inherit residual noise from CEMS delineations
and the DL-derived permanent-water layer, and flooded water, the rarest class,
stays the hardest throughout. The cross-dataset comparison is moreover scored
against GEOID-Flood ’s labels, so we anchor its claim on binary water delin-

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
15
eation, where source conventions converge. Within this scope, optical context
helps only before the event and the RTC and DEM layers add no measur-
able gain with the encoders tested, though purpose-built architectures may yet
exploit them. By releasing GEOID-Flood with all modalities and a dedicated
permanent-water layer, we provide a benchmark on which these gaps can be
addressed.
Acknowledgements
This study was carried out in the context of the SIU (CUP I53D24000060005)
and REHUBS (grant number 101214051) projects.
References
1. Bandara, W.G.C., Patel, V.M.: A transformer-based Siamese network for change
detection. In: IGARSS 2022-2022 IEEE International Geoscience and Remote Sens-
ing Symposium. pp. 207–210. IEEE (2022)
2. Bastani, F., Wolters, P., Gupta, R., Ferdinando, J., Kembhavi, A.: SatlasPretrain:
A large-scale dataset for remote sensing image understanding. In: Proceedings of
the IEEE/CVF International Conference on Computer Vision. pp. 16772–16782
(2023)
3. Bonafilia, D., Tellman, B., Anderson, T., Issenberg, E.: Sen1Floods11: A georefer-
enced dataset to train and test deep learning flood algorithms for Sentinel-1. In:
Proceedings of the IEEE/CVF conference on computer vision and pattern recog-
nition workshops. pp. 210–211 (2020)
4. Bountos, N.I., Sdraka, M., Zavras, A., Karasante, I., Karavias, A., Herekakis, T.,
Thanasou, A., Michail, D., Papoutsis, I.: Kuro Siwo: 33 billion m2 under the water.
A global multi-temporal satellite dataset for rapid flood mapping. In: Advances
in Neural Information Processing Systems (NeurIPS), Datasets and Benchmarks
Track (2024)
5. Brown, C.F., Kazmierski, M.R., Pasquarella, V.J., Rucklidge, W.J., Samsikova, M.,
Zhang, C., Shelhamer, E., Lahera, E., Wiles, O., Ilyushchenko, S., Gorelick, N.,
Zhang, L.L., Alj, S., Schechter, E., Askay, S., Guinan, O., Moore, R., Boukouvalas,
A., Kohli, P.: AlphaEarth foundations: An embedding field model for accurate and
efficient global mapping from sparse label data. arXiv preprint arXiv:2507.22291
(2025), https://arxiv.org/abs/2507.22291
6. Chen, L.C., Zhu, Y., Papandreou, G., Schroff, F., Adam, H.: Encoder-decoder with
atrous separable convolution for semantic image segmentation. In: Proceedings of
the European conference on computer vision (ECCV). pp. 801–818 (2018)
7. Copernicus Emergency Management Service: Copernicus emergency management
service on-demand mapping. Directorate Space, Security and Migration, European
Commission Joint Research Centre (EC JRC) (2012–2025), https://mapping.
emergency.copernicus.eu/, © European Union, 2012–2025
8. CRED, UNDRR: The human cost of disasters: An overview of the last 20 years
(2000–2019). Tech. rep., Centre for Research on the Epidemiology of Disasters
(CRED) and UN Office for Disaster Risk Reduction (UNDRR), Geneva (2020)

16
G. Chiriaco et al.
9. Doerksen, K., Kerner, H.: Earthshift: a benchmark for measuring robustness to
real-world distribution shifts in earth observation (2026), https://arxiv.org/
abs/2605.29330
10. Drakonakis, G.I., Tsagkatakis, G., Fotiadou, K., Tsakalides, P.: OmbriaNet—
supervised flood mapping via convolutional neural networks using multitemporal
Sentinel-1 and Sentinel-2 data fusion. IEEE Journal of Selected Topics in Applied
Earth Observations and Remote Sensing 15, 2341–2356 (2022)
11. European Space Agency, Sinergise: Copernicus global digital elevation model.
OpenTopography (2021). https://doi.org/10.5270/ESA-c5d3d65
12. Feng, Z., Atzberger, C., Jaffer, S., Knezevic, J., Sormunen, S., Young, R., Li-
saius, M.C., Immitzer, M., Jackson, T., Ball, J., Coomes, D.A., Madhavapeddy,
A., Blake, A., Keshav, S.: TESSERA: Temporal embeddings of surface spectra
for Earth representation and analysis. In: Proceedings of the IEEE/CVF Con-
ference on Computer Vision and Pattern Recognition (CVPR) (2026), https:
//arxiv.org/abs/2506.20380
13. Gomes, C., Blumenstiel, B., Almeida, J.L.d.S., de Oliveira, P.H., Fraccaro, P., Es-
cofet, F.M., Szwarcman, D., Simumba, N., Kienzler, R., Zadrozny, B.: TerraTorch:
The geospatial foundation models toolkit. In: IEEE International Geoscience and
Remote Sensing Symposium (IGARSS) (2025)
14. He, K., Zhang, X., Ren, S., Sun, J.: Deep residual learning for image recognition. In:
Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition.
pp. 770–778 (2016)
15. He, X., Zhang, S., Xue, B., Zhao, T., Wu, T.: Cross-modal change detection flood
extraction based on convolutional neural network. International Journal of Applied
Earth Observation and Geoinformation 117, 103197 (2023)
16. Herzog, H., Bastani, F., Zhang, Y., Tseng, G., Redmon, J., Sablon, H., Park, R.,
Morrison, J., Buraczynski, A., Farley, K., et al.: Olmoearth: Stable latent image
modeling for multimodal earth observation. In: Proceedings of the IEEE/CVF
Conference on Computer Vision and Pattern Recognition. pp. 34806–34817 (2026)
17. Interagency Implementation and Advanced Concepts Task Force: ETCI 2021 com-
petition on flood detection. Tech. rep., NASA (2021)
18. IPCC: Climate Change 2021: The Physical Science Basis. Contribution of Working
Group I to the Sixth Assessment Report of the Intergovernmental Panel on Climate
Change. Cambridge University Press (2021)
19. Jakubik, J., Yang, F., Blumenstiel, B., Scheurer, E., Sedona, R., Maurogiovanni, S.,
Bosmans, J., Dionelis, N., Marsocci, V., Kopp, N., et al.: TerraMind: Large-scale
generative multimodality for Earth observation. In: Proceedings of the IEEE/CVF
International Conference on Computer Vision. pp. 7383–7394 (2025)
20. Kang, W., Xiang, Y., Wang, F., Wan, L., You, H.: Flood detection in Gaofen-3
SAR images via fully convolutional networks. Sensors 18(9), 2915 (2018)
21. Liu, Z., Lin, Y., Cao, Y., Hu, H., Wei, Y., Zhang, Z., Lin, S., Guo, B.: Swin Trans-
former: Hierarchical vision transformer using shifted windows. In: Proceedings of
the IEEE/CVF International Conference on Computer Vision. pp. 10012–10022
(2021)
22. Liu, Z., Mao, H., Wu, C.Y., Feichtenhofer, C., Darrell, T., Xie, S.: A ConvNet for
the 2020s. In: Proceedings of the IEEE/CVF Conference on Computer Vision and
Pattern Recognition. pp. 11976–11986 (2022)
23. Loshchilov, I., Hutter, F.: Decoupled weight decay regularization. In: International
Conference on Learning Representations (2019)
24. Luo, X.: Earth surface water dataset. Zenodo (2021). https://doi.org/10.5281/
zenodo.5205674

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
17
25. Martinis, S., Twele, A., Voigt, S.: Towards operational near real-time flood de-
tection using a split-based automatic thresholding procedure on high resolution
TerraSAR-X data. Natural Hazards and Earth System Sciences 9(2), 303–314
(2009)
26. Mateo-García, G., Veitch-Michaelis, J., Smith, L., Oprea, S.V., Schumann, G.,
Gal, Y., Baydin, A.G., Backes, D.: Towards global flood mapping onboard low
cost satellites with machine learning. Scientific Reports 11, 7249 (2021)
27. Montello, F., Arnaudo, E., Rossi, C.: MMFlood: A multimodal dataset for flood
delineation from satellite imagery. IEEE Access 10, 96774–96787 (2022)
28. Notarangelo, N., Wirion, C., van Winsen, F.: STURM-Flood: a curated dataset
for deep learning-based flood extent mapping leveraging Sentinel-1 and Sentinel-2
imagery. Big Earth Data 9(3), 412–438 (2025)
29. Pekel, J.F., Cottam, A., Gorelick, N., Belward, A.S.: High-resolution mapping of
global surface water and its long-term changes. Nature 540(7633), 418–422 (2016)
30. Portalés-Julià, E., Mateo-García, G., Purcell, C., Gómez-Chova, L.: Global flood
extent segmentation in optical satellite images. Scientific Reports 13(1), 20316
(2023)
31. Rahnemoonfar, M., Chowdhury, T., Sarkar, A., Varshney, D., Yari, M., Murphy,
R.R.: FloodNet: A high resolution aerial imagery dataset for post flood scene un-
derstanding. IEEE Access 9, 89644–89654 (2021)
32. Robinson, C., Lehmann, N., Stewart, A.J., Ekim, B., Fang, H., Corley, I.A.,
Cordeiro, M.: Advancing Earth observation through machine learning: A TorchGeo
tutorial. arXiv preprint arXiv:2603.02386 (2026), https://arxiv.org/abs/2603.
02386
33. Ronneberger, O., Fischer, P., Brox, T.: U-Net: Convolutional networks for biomed-
ical image segmentation. In: International Conference on Medical image computing
and computer-assisted intervention. pp. 234–241. Springer (2015)
34. Saleh, T., Weng, X., Holail, S., Hao, C., Xia, G.S.: DAM-Net: Global flood de-
tection from SAR imagery using differential attention metric-based vision trans-
formers. ISPRS Journal of Photogrammetry and Remote Sensing 212, 440–453
(2024)
35. Sinergise: Sentinel Hub. Satellite data access and processing platform, https://
www.sentinel-hub.com
36. Twele, A., Cao, W., Plank, S., Martinis, S.: Sentinel-1-based flood mapping: a
fully automated processing chain. International Journal of Remote Sensing 37(13),
2990–3004 (2016)
37. Wang, Y., Braham, N.A.A., Xiong, Z., Liu, C., Albrecht, C.M., Zhu, X.X.:
SSL4EO-S12: A large-scale multimodal, multitemporal dataset for self-supervised
learning in Earth observation [Software and Data Sets]. IEEE Geoscience and Re-
mote Sensing Magazine 11(3), 98–106 (2023)
38. Wright, N., Duncan, J.M., Callow, J.N., Thompson, S.E., George, R.J.: Training
sensor-agnostic deep learning models for remote sensing: Achieving state-of-the-art
cloud and cloud shadow identification with OmniCloudMask. Remote Sensing of
Environment 322, 114694 (2025)
39. Xiong, Z., Wang, Y., Zhang, F., Stewart, A.J., Hanna, J., Borth, D., Papoutsis,
I., Le Saux, B., Camps-Valls, G., Zhu, X.X.: Neural plasticity-inspired multimodal
foundation model for Earth observation. arXiv preprint arXiv:2403.15356 (2024)
40. Zhao, B., Sui, H., Liu, J.: Siam-DWENet: Flood inundation detection for SAR im-
agery using a cross-task transfer Siamese network. International Journal of Applied
Earth Observation and Geoinformation 116, 103132 (2023)

18
G. Chiriaco et al.
A
Models and Optimization
This appendix details how the models benchmarked in Sec. 4 are built, trained,
and scored. All runs are implemented in TerraTorch v1.1 [13] with PyTorch
Lightning in bf16-mixed precision under a fixed global seed. They share the op-
timizer, schedule, loss, augmentation, and tiled-inference protocol described be-
low, and differ only in the encoder, the decoder family, the learning-rate regime,
and the scenario-specific task head.
A.1
Encoder zoo
We evaluate the geospatial foundation models TerraMind v1 (tiny, small, base,
large) [19], DOFA (base, large) [39], OlmoEarth [16], SSL4EO-ResNet50 [37],
and Satlas Swin-B [2], alongside the ImageNet-pretrained encoders ResNet-
50/101 [14], ConvNeXt-Tiny/Base [22], and Swin-Tiny/Base [21]. Each geospa-
tial foundation model is run in two settings: with frozen features, where only
the decoder and head are updated, and finetuned, where the encoder and de-
coder are updated jointly. The ImageNet-pretrained encoders are always trained
end-to-end, with no frozen components.
A.2
Decoder and segmentation head
Each foundation-model encoder is coupled with a U-Net [33] decoder (chan-
nel widths [512, 256, 128, 64]) and a segmentation head with dropout 0.3. For
the transformer foundation models, the token outputs are converted into the
spatial feature pyramid the decoder expects through backbone-specific necks:
four intermediate blocks are selected, their token sequences are reshaped to 2-D
feature maps, and a learned interpolation produces a four-level pyramid; the con-
volutional SSL4EO-ResNet50 exposes its native four stages directly. The Swin
baseline needs only a dimension-permutation neck and 224×224 inputs. The
head emits per-pixel logits over 2 classes for the binary scenarios (i)–(ii) and
3 classes (background, permanent water, flooded water) for the change-focused
fusion architectures (iii).
A.3
Optimization
All models are trained for 20 epochs with AdamW [23] under a cosine-annealed
learning rate (ηmin = 10−6). We use three learning-rate regimes matched to the
training mode:
– Frozen foundation models (decoder and head only): learning rate 5 ×
10−6, weight decay 0.1.
– Finetuned foundation models: decoder learning rate 5 × 10−5 with a
discriminative, 10× lower encoder rate of 5 × 10−6, weight decay 0.1.
– ImageNet-pretrained encoders (end-to-end): decoder learning rate 5 ×
10−4 with an encoder rate of 5 × 10−5, weight decay 0.01.

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
19
The objective is pixel-wise cross-entropy with index 255 ignored, so that pix-
els outside the Copernicus EMS analyzed area and invalid pixels (e.g. SAR
no-data) are excluded from the loss. We train on 256×256 crops at stride 128
(training tiles only) with D4 geometric augmentation, using a batch size of 8–64
depending on encoder and modality count. Training uses early stopping with
patience 5 on the validation IoU of the positive class (binary water for scenarios
(i)–(ii), flooded water for the three-class fusion models); the reported checkpoint
is the one maximizing that same validation IoU, binary water IoU for the single-
image and paired models, flooded-water IoU for the fusion models. Inputs are
normalized per channel: Sentinel-1 GRD VV/VH use our training-set statistics
(µVV = −12.6, σVV = 5.2; µVH = −20.3, σVH = 5.9, in dB), except backbones
that ship their own published SAR statistics (e.g. SSL4EO-ResNet50), which
use those.
A.4
Inference and tiling
At test time, each 1024×1024 test tile is partitioned into a 4×4 grid of non-
overlapping 256×256 windows, and each window is scored in a single forward
pass; metrics are accumulated over all windows. Models that predict three classes
directly (scenario (iii)) are scored on that output; for the single-image and paired
binary models the three-class flood map is assembled post-hoc by combining the
binary pre- and post-event water masks, as described in Sec. 5.1.
B
Permanent Water Layer Generation
Accurately distinguishing pre-existing, permanent water bodies from transient
flood inundation is a prerequisite for flood delineation. Rather than relying on
an external product such as the JRC Global Surface Water [29], we generate a
per-scene permanent water mask directly from annual geospatial embeddings,
without requiring cloud-free Sentinel-2 imagery at inference time.
The core motivation is that annual embeddings are derived from multi-
temporal composites spanning a full year, making them insensitive to the specific
imaging conditions of any single acquisition. Permanent water bodies leave a sta-
ble imprint in these composites that is qualitatively different from the transient
signal of a flood event occurring in the same year. A lightweight model trained
to decode this imprint should therefore produce a permanent water prior that is
both temporally robust and spatially precise, and that can be applied on demand
to any geographic extent covered by the embedding catalogue.
B.1
Training data
We train and evaluate on the Earth Surface Water (ESW) dataset [24], which
provides binary water/non-water labels for 95 globally distributed Sentinel-2
Level-2A scenes acquired in 2019. Following the original split, we tile each scene

20
G. Chiriaco et al.
into non-overlapping 256 × 256 pixel patches, yielding 788 training tiles and 307
test tiles spanning diverse geographic and climatic conditions.
Based on the spatial and temporal extents of the ESW dataset, we down-
load the same areas of interest from two publicly available annual embedding
sources: (i) AlphaEarth Foundations (AEF) [5], 64-dimensional embeddings at
10 m resolution, available globally from 2017 to 2025, and (ii) TESSERA [12],
128-dimensional embeddings at 10 m resolution, also available globally in a vari-
able range, around 2017 to 2025. Both sources are fetched for the calendar year
matching the Sentinel-2 acquisition (2019 for the ESW dataset).
A key property of both embedding catalogues is that each annual embed-
ding aggregates multi-temporal observations from the entire year into a single
compact representation. Permanent water bodies (e.g., rivers, lakes, reservoirs,
coastal lagoons) produce a distinctive and stable pattern in this annual compos-
ite that is markedly different from ephemeral flood signals, seasonal moisture
variation, or cloud-shadow artifacts.
B.2
Methodology
Since the input is already a spatially dense, semantically rich volume, we do
not employ additional heavyweight encoders. Instead, we design two simple
lightweight decoders that operate directly on the embedding tensor. The first
is a linear probe, a 1×1 convolution mapping directly to logits, comprising only
65 parameters for AEF and 129 parameters for TESSERA; it tests how much
information is linearly accessible in the raw embedding without any spatial ag-
gregation. The second is a shallow convolutional decoder (1×1 →3×3 →1×1)
with non-linearities, totalling 41 281 parameters for AEF and 45 377 parameters
for TESSERA, whose spatial convolution aggregates information over a 5 × 5
effective receptive field and allows the model to sharpen predictions along water
boundaries.
We evaluate two reference baselines that require no embedding features.
First, we include JRC-GSW [29], a training-free static product derived from
the full 1984–2021 Landsat archive providing per-pixel water occurrence statis-
tics at 30 m resolution. We binarise the occurrence layer at ≥75%, a threshold
commonly adopted in the literature for permanent water, and query it directly
from the Microsoft Planetary Computer STAC catalogue. Second, we train a
DeepLabV3+ [6] model (ResNet-50 backbone, ≈25 M parameters) on the six
Sentinel-2 bands augmented with two NDWI variants and NDVI, following the
setup of [32]. This provides a spectral segmentation reference trained with com-
parable computational resources; unlike the embedding models, it has full access
to the reflectance signal of each input scene.
B.3
Results
Implementation details. We tile each scene into non-overlapping 256 × 256
pixel patches following the original ESW split, comprising 788 training tiles and
307 test tiles. All models are trained for 50 epochs with AdamW [23] (η = 10−4,

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
21
Table 6: Water body delineation on the Earth Surface Water test set. The upper block
provides baselines, including JRC-GSW as state-of-the-art reference water. The lower
block provides embedding-based results. Best results in bold.
Encoder
Decoder
#Params
F1
IoU Precision Recall
JRC-GSW [29] (occ.≥75%)
– 0.874 0.776
0.900
0.849
ResNet50
DeepLabV3+
25.6M 0.773 0.692
0.837
0.794
AEF
Linear
65 0.883 0.791
0.906
0.862
TESSERA Linear
129 0.902 0.821
0.844
0.969
TESSERA MLP
45K 0.911 0.837
0.852
0.980
AEF
MLP
41K 0.963 0.928
0.956
0.969
weight decay 10−4) and a cosine-annealing schedule. Table 6 reports test-set
performance on the ESW dataset.
Linear probes are already strong. Even without any spatial aggrega-
tion, the linear probes reach 0.883 F1 for AEF and 0.902 F1 for TESSERA.
That a single 1×1 convolution with fewer than 130 parameters attains this level
confirms that both embedding spaces encode permanent water as a nearly lin-
early separable signal, a direct consequence of the annual temporal aggregation
described above.
Adding the spatial decoder yields +8.0 F1 points for AEF (from 0.883 to
0.963) but only +0.9 F1 points for TESSERA (from 0.902 to 0.911). AEF’s
more compact 64-dimensional space benefits from explicit neighbourhood aggre-
gation to resolve boundary ambiguities, whereas TESSERA’s 128-dimensional
representation already encodes sufficient per-pixel context.
Notably, JRC-GSW achieves F1 = 0.874 without any training on the ESW
dataset, already ahead of DeepLabV3+ and only 8.9 points below our best model.
This confirms that permanent water is an exceptionally stable signal: decades of
Landsat observations accumulate into a reliable occurrence prior that generalizes
well across scenes. A good portion of the residual gap to AEF-MLP could also
be attributed to resolution: JRC-GSW operates at 30 m while our embeddings
produce predictions at 10 m, enabling finer delineation of narrow rivers, canals,
and coastal features that are missed or blurred at coarser scales.
DeepLabV3+ reaches only 0.773 F1, sitting below even the training-free JRC-
GSW. We do not claim this is a tight spectral upper bound: a more elabo-
rate setup (larger backbone, heavy augmentation, or scene-specific finetuning)
could improve performance, but this comparison reflects a realistic, resource-
comparable regime. The key limitation of spectral models is rather generaliz-
ability: a model trained on a limited number of scenes might not transfer well
to globally distributed AoIs, each acquired under different atmospheric, sensor,
and surface conditions. Annual geospatial embeddings sidestep this thanks to
their full-year multi-temporal composition, and a single lightweight model can
be applied globally without retraining with comparable robustness.

22
G. Chiriaco et al.
Qualitative examples are shown in Fig. 6. The AEF-MLP model correctly
delineates rivers, narrow channels, and coastal features despite never observing
any spectral band of the input scene.
B.4
Inference Pipeline
For each area of interest (AoI) in the flood dataset, we fetch the AEF embedding
corresponding to the year of the flood event and run the AEF-MLP model to
produce a binary permanent water mask at 10 m resolution. Events predating the
AEF coverage window (before 2017) use the earliest available year as a proxy;
permanent water bodies are stable over multi-year periods, so this introduces
negligible error. Binarisation uses hysteresis thresholding (p ≥0.5 as seeds, p ≥
0.3 for spatial extension) to prevent fragmentation of narrow rivers and elongated
reservoirs.
The pipeline was applied to all valid AoIs spanning the 219 flood events
of Sec. 3 (Copernicus EMS activations EMSR151–EMSR871), producing per-
manent water layers at 10 m resolution, three times finer than the JRC Global
Surface Water product (30 m) and without requiring access to a multi-decadal
Landsat archive.

GEOID-Flood: Multi-Modal Flood Segmentation Benchmark
23
Fig. 6: Qualitative permanent water delineation on an ESW test tile. Rows correspond
to the four embedding models (TESSERA and AEF, each with a linear probe and an
MLP decoder); columns show the Sentinel-2 RGB composite, a PCA projection of the
annual embedding, the ground-truth water mask, and the model prediction.
