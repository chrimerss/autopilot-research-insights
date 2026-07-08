---
title: 'StefaLand: An Efficient Geoscience Foundation Model That Improves Dynamic
  Land-Surface Predictions'
authors: Nicholas Kraabel; Jiangtao Liu; Yuchen Bian; Daniel Kifer; Chaopeng Shen
year: '2026'
venue: ''
---

StefaLand: An Efficient Geoscience Foundation Model That Improves Dynamic
Land-Surface Predictions
Nicholas Kraabel * 1 Jiangtao Liu * 1 Daniel Kifer 2 Yuchen Bian 3 Chaopeng Shen 1
Abstract
Managing natural resources and mitigating risks
from floods, droughts, wildfires, and landslides
require models that can accurately predict climate-
driven land–surface responses. Traditional mod-
els often struggle with spatial generalization be-
cause they are trained/calibrated on limited obser-
vations and can degrade under concept drift. Re-
cently proposed vision foundation models trained
on satellite imagery demand massive compute,
and they are not designed for dynamic land sur-
face prediction tasks. We introduce StefaLand,
a generative spatiotemporal Earth representation
learning model centered on learning cross-domain
interactions to suppress overfitting. StefaLand
demonstrates especially strong spatial generaliza-
tion on five datasets across four important tasks:
streamflow, soil moisture, soil composition and
landslides, compared to previous state-of-the-art
methods. The domain-inspired design choices in-
clude a location-aware masked autoencoder that
fuses static and time-series inputs, an attribute-
based rather than image-based representation that
drastically reduces compute demands, and resid-
ual fine-tuning adapters that strengthen knowl-
edge transfer across tasks. StefaLand can be pre-
trained and finetuned on commonly-available aca-
demic compute resources, yet consistently outper-
forms state-of-the-art supervised learning base-
lines, fine-tuned vision foundation models and
commercially-available embeddings, highlighting
the previously overlooked value of cross-domain
interactions and providing assistance to data-poor
regions of the world.
*Equal contribution 1Department of Civil and Environmental
Engineering, The Pennsylvania State University, University Park,
PA 16802-1408, USA 2Department of Computer Science and En-
gineering, The Pennsylvania State University, University Park, PA
16802-1408, USA 3Amazon.com, Inc.. Correspondence to: Shen
Chaopeng <cxs1024@psu.edu>.
Preprint. February 3, 2026.
1. Introduction
Climate change is ushering in strong and widespread
changes on the land surface, including higher frequencies of
floods, droughts, wildfires and other geohazards (Ebi et al.,
2021; IPCC, 2021). To mitigate the impact of these disasters,
there are urgent needs for models that can accurately predict
land surface dynamics such as streamflow, soil moisture,
soil composition, landslides, snow water equivalent, ground-
water levels, and vegetation carbon content. Among these,
soil moisture controls ecosystem health and influences land-
atmosphere interactions (Dorigo et al., 2013a). Streamflow
is the flow rate of water running in the rivers, the most
accessible water resource to humans, and too high or too
low streamflow can cause flooding or hydrologic drought,
respectively. Soil composition (sand, silt, clay fractions)
governs infiltration capacity and root-zone storage, while
slope–soil-vegetation interactions directly influence land-
slide hazards. Here, we limit our scope to the predictions of
dynamical or static land surface processes that represent the
impacts of climate change.
Traditionally, these tasks were undertaken by physics-based
models that take atmospheric forcings (precipitation, tem-
perature) as inputs and sequentially calculate the physical
processes that eventually lead to the variables of interest (Li
et al., 2015). In recent years, there has been a proliferation
of data-driven machine learning (ML) models (Solomatine
& Ostfeld, 2008). These models are often set up to accept
forcing (dynamic weather) and landscape characteristics
(static) data as inputs, and are trained to directly predict
the natural land surface variables given the weather inputs.
However, up to now, most of the geoscientific ML models
have been supervised ML approaches trained specifically
for a narrow set of tasks.
Large vision foundation models have been trained on satel-
lite imagery of earth to facilitate mapping (Tseng et al.,
2025), weather prediction (Schmude et al., 2024), air quality
(Bodnar et al., 2025) and other geoscientific tasks (Jakubik
et al., 2023; 2025). A particularly notable observation is
that they have not focused on the interactions among land-
scape domains (climate, soil, vegetation, terrain, geology).
The catchment coevolution hypothesis (Troch et al., 2015)
states that terrain, soil, vegetation and climate all coevolve,
1
arXiv:2509.17942v3  [cs.LG]  2 Feb 2026

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
shaping the landscape we have today. Knowing parts of the
landscape domains often allow us to predict the others. This
implies that their joint distributions can greatly inform latent
processes relevant to the transport of water and materials in
the catchments. However, valuable temporal datasets and
ground-based observations remain underutilized (Xie et al.,
2023), and to our knowledge, no foundation model has yet
been developed with a primary focus on dynamical land
surface modeling.
A Grand Challenge for geoscientific ML models is to im-
prove their spatial generalization, because a frequent issue
facing them is the sparsity and spatial imbalance of obser-
vational data. Satellite data are often coarse in resolution
and uncertain compared to in-situ measurements. SMAP,
for example, provides global soil moisture observations at
9–36 km resolution every 2–3 days, which are useful for
regional climate and hydrologic research but far less valu-
able than in-situ probes for operational field tasks such as
irrigation scheduling or crop stress monitoring (Entekhabi
et al., 2010; Liu et al., 2022; 2023b). However, in-situ data,
due to the cost of installing instruments and varying poli-
cies on data sharing, is only available in high density in
certain regions of some developed nations. For example,
streamflow gauge data are abundant in the United States,
Europe, Australia and Japan, but remain sparse in Africa,
South America, and much of Asia (Global Runoff Data
Centre, 2020). As quantified in many studies (Feng et al.,
2023), a deep network trained on data from some regions
can face substantial performance degradation when applied
in data-scarce regions. This occurs partly because there are
not enough sites to learn the true dependencies of the targets
on static land surface characteristics, and partly because
of systematic data discrepancies across regions (concept
drift). While such limitations hinder traditional supervised
ML models, foundation or representation learning models
offer a potential path forward: by jointly learning from
broad, heterogeneous datasets (including temporal records
and ground observations where available), they may transfer
useful representations to data-scarce regions where task-
specific training data are limited.
Related Work: In hydrologic and ecosystem predictions,
supervised long short-term memory (LSTM) networks
(Hochreiter & Schmidhuber, 1997) remain a highly pop-
ular architecture, in part because land surface processes
often behave like Markov processes where LSTMs’ gating
mechanisms handle noisy continuous inputs well (Kratzert
et al., 2018). Attempts to adopt transformers, so success-
ful in natural language processing, have generally found
it difficult to noticeably surpass LSTM in time series re-
gression tasks (Xue et al., 2023; Liu et al., 2024; 2025b),
with evidence of overfitting on continuous signals (Zeng
et al., 2022). Nonetheless, recent studies show that with
task-specific modifications and careful fine-tuning, trans-
formers can achieve competitive results in extreme event
prediction (Wen et al., 2023), precisely the areas where
current hydrologic models struggle most with.
Traditional hydrologic research on ”prediction in ungauged
basins” (PUB) have examined regionalization and spatial
interpolation approaches including clustering or classifying
catchments and transferring parameters from donor catch-
ments in the same class (Hrachowitz et al., 2013; Yang et al.,
2023). Such an expert-derived design represents a crude
practice of unsupervised learning that indicates the impor-
tance of understanding the joint data distribution. How-
ever, modern weakly-supervised foundation models can, in
general, much better grasp the joint data distribution than
expert-driven approaches. Representation learning models
offer a promising approach to address these spatial general-
ization challenges. By pretraining on large-scale datasets to
learn generalizable representations, these models can poten-
tially transfer knowledge across regions and geoscientific
domains (Zhang et al., 2024).
Recent progress in geoscientific foundation models has been
driven by the increasing availability of global Earth system
datasets and advances in self-supervised learning, enabling
pretrained representations that transfer across tasks and re-
gions (Bommasani et al., 2022; Lacoste et al., 2023). Be-
yond vision-based approaches, recent work on structured
data has shown that foundation models such as TabPFN
can learn transferable priors over tabular regression tasks
without task-specific training. (Hollmann et al., 2025).
Most existing Earth observation foundation models, includ-
ing TerraMind (Jakubik et al., 2025), Prithvi (Hsu et al.,
2024), Aurora (Bodnar et al., 2025), AlphaEarth (Brown
et al., 2025), and Galileo (Tseng et al., 2025), are pretrained
primarily on remote sensing imagery and related EO prod-
ucts. These models are effective at capturing surface appear-
ance and spatial patterns, and their representations often
act as static or slowly varying landscape descriptors. In
particular, AlphaEarth learns global, high-resolution spatial
embeddings from large-scale Earth observation data that
capture consistent landscape structure across climate and
biome gradients, and these embeddings have been shown to
transfer effectively as fixed spatial features for a wide range
of downstream Earth system prediction tasks, including
hydrology. Because AlphaEarth embeddings are globally
available and independent of task-specific labels, they pro-
vide a strong and widely applicable baseline for evaluating
spatial generalization in data-limited settings. However,
many variables central to land-surface and hydrologic dy-
namics, including subsurface properties, storage processes,
and long-term temporal interactions, are not directly observ-
able from space and therefore cannot be reliably inferred
from imagery alone. Moreover, EO foundation models are
typically optimized for surface-level semantic consistency
2

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
and invariance to transient atmospheric or observational
effects, which can further suppress signals that are infor-
mative for hydrologic processes, such as moisture-related
variability or persistence.
Our contributions: We present the Spatial-Temporal Earth
Foundation model with Attributes for the Land Surface (Ste-
faLand), a land-focused geoscientific representation learn-
ing model for dynamic land–surface prediction. StefaLand
is evaluated on streamflow, soil moisture, soil composition,
and landslide susceptibility under spatial holdout regimes.
It shows strong spatial generalization across diverse land-
scapes and data-scarce regions for a wide variety of tasks.
StefaLand’s attribute-based rather than image-based design
(with the potential to link to image-like inputs in the future)
incorporates a variety of ground-based measurement data,
emphasizes relevant land-surface physical processes, drasti-
cally reduces compute requirements while retaining global
coverage, making it accessible to researchers with modest
resources. Pretraining our model required only about 720
V100 GPU hours (could be shorter with more advanced
GPUs). The model builds on a masked autoencoder back-
bone, a location-aware fusion of static and time-series inputs,
grouped masking to promote cross-domain interactions, and
residual fine-tuning adapters, into a coherent design guided
by geoscientific knowledge. Taken together, these contri-
butions establish StefaLand as an efficient and accessible
complement to vision-based foundation models.
2. Methods
Dynamic land–surface prediction requires combining het-
erogeneous information: static landscape attributes such as
topography, soils, vegetation, and geology, together with
dynamic forcings such as precipitation and temperature. Ste-
faLand addresses this challenge with a transformer-based
masked autoencoder that jointly embeds static and dynamic
variables, pretrained with a cross-variable masking strategy,
and then adapted for specific prediction tasks with task-
specific heads.
2.1. Stefaland Structure
StefaLand is a transformer-based masked autoencoder in-
spired by bidirectional language models such as BERT (De-
vlin et al., 2018), designed to jointly embed static land-
scape attributes and dynamic time-varying forcings within a
unified representation. During pretraining, StefaLand ran-
domly masks subsets of the input variables and learns to
reconstruct the masked components using the remaining
unmasked information. Masking may affect static attributes,
temporal variables, or entire variable groups, encouraging
the model to learn the joint distribution over heterogeneous
land-surface controls rather than relying on any single data
source.
A key design choice in StefaLand is cross-variable group
masking, in which physically or statistically related vari-
ables are masked together rather than independently. This
prevents trivial reconstruction through correlated inputs and
encourages the model to capture cross-domain linkages,
such as interactions between soil texture and climate sea-
sonality or between topography and hydrologic response.
Grouped masking strategies have previously been explored
in multimodal learning settings, including Presto (Tseng
et al., 2023), and here we adapt this idea using a recon-
struction loss applied to masked inputs, normalized by
variable-wise standard deviations when available. The at-
tention mechanism naturally accommodates missing inputs
by suppressing attention weights for masked tokens, allow-
ing StefaLand to flexibly reason over arbitrarily incomplete
input configurations. Although more recent masked-model
formulations exist, we adopt a BERT-style design for its sim-
plicity, interpretability, and robustness across heterogeneous
inputs.
Following pretraining, the encoder produces contextualized
embeddings for both static attributes and dynamic forc-
ings, which are reused across downstream tasks through
lightweight task-specific heads and residual adaptation path-
ways, as illustrated in Figure 1.
2.2. Pretraining Details
The pretraining dataset is a derived global attribute dataset
spanning ∼8,634 locations (basins) over 40 years. Variables
were chosen to represent the key controls on fluxes of water,
energy, momentum, sediment, and nutrients. A complete list
of variables, their group assignments, and their sources is
provided in Appendix C. A visualization of the pretraining
dataset coverage is provided in Appendix C Figure 4.
The cross-variable group masking (CVGM) scheme is de-
signed so that variables with reciprocal or bidirectional
relationships are masked together, preventing them from
acting as direct predictors for one another. Most group-
ings are straightforward and common sense, such as mask-
ing silt and clay fractions jointly, while a few variables re-
quire domain-specific treatment; for example, soil depth is
grouped with terrain attributes due to its strong dependence
on topographic derivations. The complete set of variables
and their group assignments is provided in Table 16. By
masking and reconstructing variables at the group level,
the model is encouraged to capture cross-domain interac-
tions, such as couplings between soil texture and climate
seasonality.
2.3. Finetuning for Prediction Tasks
We adapt the pretrained StefaLand encoder to downstream
prediction tasks using lightweight task-specific heads while
keeping the main model weights frozen. This strategy, il-
3

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Figure 1. Conceptual overview of the StefaLand Structure. Static landscape attributes and dynamic forcings are jointly embedded using a
transformer-based masked autoencoder with cross-variable group masking. With relevant dimensionality included.
lustrated in Figure 1, preserves the general-purpose repre-
sentations learned during pretraining and reduces the risk of
overfitting when finetuning on limited task-specific data.
Our primary finetuning configuration, StefaLand-resConn,
integrates pretrained embeddings with raw meteorological
forcings through a residual adaptation pathway via addi-
tive fusion prior to the recurrent decoder. Let Et denote
the StefaLand embedding at time t, and let xt denote the
corresponding raw forcing inputs. We compute:
rt = fconv+linear(xt),
(1)
ht = LSTM(Et + rt),
(2)
ˆyt = Woht + bo,
(3)
where fconv+linear(·) denotes a shallow convolutional and
linear projection block. Residual connections propagate
both the pretrained embedding Et and the task-specific sig-
nal rt into the recurrent decoder, allowing general spatial
knowledge captured during pretraining to be iteratively re-
fined using task-specific temporal information. This design
strengthens spatial generalization while retaining flexibility
to adapt to local dynamics.
We employ an LSTM decoder for tasks with explicit tem-
poral structure, such as streamflow and soil moisture pre-
diction. For non-temporal or spatially structured tasks, in-
cluding soil property inference and landslide susceptibil-
ity mapping, the temporal decoder is replaced with a task-
appropriate adapter head, such as a multilayer perceptron or
two-dimensional convolutional neural network (CNN2D).
In these cases, frozen StefaLand embeddings are used as
contextual features. Across all tasks, only the adapter mod-
ules and task heads are updated during finetuning, while
the pretrained StefaLand encoder remains frozen, ensur-
ing computational efficiency and stable transfer from the
representation learning model.
3. Experiments
We tested the value of foundation model pretraining on 5
datasets and 6 experiments, including, streamflow on the
CAMELS dataset on USA (a widely used benchmark dataset
in hydrology), CAMELS streamflow prediction with hybrid
model, global streamflow on Caravan, global in-situ soil
moisture, global soil properties, and landslide susceptibility
in Oregon, USA. For all experiments, hyperparameters were
tuned with Ray Tune and kept consistent across model con-
figurations within each experimental case (e.g., CAMELS
streamflow, soil moisture, etc). Because we compare spatial
generalization, we used temporal validation splits for hyper-
parameter optimization. Complete details of hyperparam-
eters, forcings, and static features for all four experiments
are in Appendix C.
Model variants and baselines.
We evaluate StefaLand
alongside established baselines commonly used in hydro-
logic and geophysical time series modeling. As supervised
baselines, we include LSTM-SL, which remains the domi-
nant architecture for streamflow prediction and follows the
same core model class used in prior large scale hydrology
studies (Kratzert et al., 2019; Feng et al., 2021; Sabzipour
et al., 2023). We additionally evaluate Informer (Zhou et al.,
2021), Reformer (Kitaev et al., 2020), and DLinear (Zeng
et al., 2022), which, although originally proposed for fore-
casting, are applied here in a sequence to sequence set-
ting and are commonly included in recent hydrologic and
geophysical modeling studies as representative transformer-
based baselines.
To assess pretrained Earth representations, we include Al-
phaEarth LSTM and AlphaEarth ResConn, which feed pre-
trained AlphaEarth embeddings into an LSTM decoder with
and without a residual task adapter, respectively (Brown
et al., 2025). Because our task periods do not fully overlap
AlphaEarth’s 2017–2024 temporal coverage, AlphaEarth
4

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
embeddings are spatially aggregated over each basin and
collapsed into a fixed set of 64 static features per site. For
CAMELS streamflow and soil moisture, we additionally
evaluate TabPFN, a tabular foundation model (Hollmann
et al., 2025). Since TabPFN is non sequential and con-
strained by a fixed context window, we provide it with com-
pact statistical summaries of each historical window while
preserving identical data splits and evaluation protocols.
We also conducted an exploratory evaluation of additional
Earth observation and atmospheric foundation models to
assess their viability for land–surface prediction under
matched adaptation strategies; these limited-scope results
are reported in B.3
Our proposed method, StefaLand resConn (residual connec-
tion), combines a pretrained encoder with a residual adapter
and LSTM decoder.
3.1. CAMELS Streamflow Prediction
To compare spatial generalization on a well benchmarked
dataset, we follow (Feng et al., 2021), testing prediction
in ungauged basins (PUB, random spatial K-fold) and un-
gauged regions (PUR, regional spatial K-fold). We use
CAMELS (Addor et al., 2017; Newman et al., 2014), re-
stricted to the 531-basin subset with clear watershed bound-
aries (Newman et al., 2017). Basins were divided into 10
random groups for PUB and 7 contiguous regions for PUR,
employing leave-one-out in both cases. To avoid leakage,
all CAMELS-overlapping stations were removed during
pretraining for PUB, and entire regions were excluded for
PUR. The success at these tasks would mean better flood
forecasting information for populations in the world who do
not have as many gauging stations around them.
The results in Tables 1 and 2 demonstrate that foundation-
model pretraining substantially improves spatial general-
ization relative to purely supervised approaches under both
PUB and PUR evaluation. StefaLand-resConn achieves the
strongest performance across all reported metrics, reducing
RMSE by approximately 20% relative to the supervised
LSTM baseline under PUB and by about 16 to 17% under
PUR, while also yielding consistently higher correlation and
NSE. Among the baselines, the supervised LSTM remains
competitive and outperforms linear and transformer-based
sequence models, while TabPFN performs poorly with sub-
stantially higher RMSE and lower NSE despite moderate
correlation, indicating that a tabular formulation fails to
capture key temporal structure in rainfall runoff dynamics.
AlphaEarth-based variants provide notable improvements
over the supervised LSTM, particularly in correlation, but
remain well below StefaLand-resConn across all metrics,
even with residual feature reuse.
We ran additional experiments that hybridize StefaLand with
Table 1. CAMELS streamflow performance under PUB evaluation
(random spatial holdout; ungauged basins). Values are median ±
standard error across folds.
Model
RMSE ↓
ubRMSE ↓
Corr ↑
NSE ↑
LSTM SL
1.402 ± 0.04
1.360 ± 0.04
0.762 ± 0.01
0.636 ± 0.04
DLinear
2.012 ± 0.06
2.000 ± 0.06
0.598 ± 0.01
0.302 ± 0.48
Informer
2.262 ± 0.07
2.237 ± 0.08
0.521 ± 0.01
0.104 ± 0.08
Reformer
1.908 ± 0.09
1.871 ± 0.09
0.718 ± 0.00
0.270 ± 0.18
TabPFN
2.727 ± 0.09
2.725 ± 0.09
0.718 ± 0.01
0.509 ± 0.014
AlphaEarth LSTM
1.409 ± 0.10
1.393 ± 0.10
0.837 ± 0.11
0.618 ± 0.05
AlphaEarth resConn
1.361 ± 0.09
1.345 ± 0.09
0.859 ± 0.01
0.647 ± 0.04
StefaLand resConn
1.111 ± 0.04
1.068 ± 0.04
0.869 ± 0.01
0.717 ± 0.16
Table 2. CAMELS streamflow performance (PUR: regional spatial
holdout; ungauged regions). Values are median ± standard error
across folds.
Model
RMSE ↓
ubRMSE ↓
Corr ↑
NSE ↑
LSTM SL
1.609 ± 0.24
1.457 ± 0.22
0.743 ± 0.02
0.554 ± 0.13
DLinear
2.019 ± 0.35
1.983 ± 0.34
0.597 ± 0.03
0.290 ± 0.99
Informer
2.332 ± 0.41
2.295 ± 0.37
0.497 ± 0.01
0.046 ± 0.27
Reformer
2.074 ± 0.33
1.978 ± 0.31
0.686 ± 0.02
0.257 ± 1.17
TabPFN
2.709 ± 1.08
2.501 ± 0.89
0.576 ± 0.11
0.328 ± 0.12
AlphaEarth LSTM
1.724 ± 0.85
1.685 ± 0.82
0.780 ± 0.07
0.456 ± 0.15
AlphaEarth resConn
1.727 ± 0.74
1.684 ± 0.71
0.790 ± 0.06
0.520 ± 0.10
StefaLand resConn
1.344 ± 0.21
1.334 ± 0.19
0.801 ± 0.02
0.635 ± 0.25
the HBV1.1 physics backbone on the same PUB/PUR splits,
testing its ability to parameterize physics-based models.
These hybrids achieved up to a 13% RMSE reduction and
a 10% correlation gain compared to the LSTM–HBV1.1
baseline, showing StefaLand’s . By constraining predictions
with physics while leveraging StefaLand features, these
hybrids further improve upon the general results above and
highlight the versatility of the approach. Full results are
provided in Appendix B, Table 9.
On a related note, the supervised LSTM is not an easy bench-
mark to surpass. The original multi-basin LSTM and subse-
quent large-scale comparisons (Kratzert et al., 2019; Feng
et al., 2021) showed that vanilla Transformers generally
failed to outperform LSTMs on rainfall–runoff prediction
and modified transforms essentially tied LSTM (Liu et al.,
2024, Table 1 therein). The LSTM NSE values reported here
are very similar to those in the domain literature (Feng et al.,
2021). Google’s global flood-forecasting system adopts an
encoder–decoder LSTM backbone (Nearing et al., 2024).
The gains demonstrated are also substantial: to provide
some context, when LSTM raised NSE from 0.64 to 0.73
(without ensemble), it was considered a generational change
in predictive performance (Nearing et al., 2021; Feng et al.,
2021), and no method other than ensembling more models
cleanly surpassed default LSTM on the PUB test.
3.2. Caravan Global Streamflow
We designed a global-scale runoff prediction experiment to
assess spatial robustness and generalization across diverse
hydroclimatic regimes. We use the open-source Caravan
dataset (Kratzert et al., 2023), a global community dataset
5

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Table 3. Caravan streamflow performance under random spatial
holdout. Values are median ± standard error across folds
Model
RMSE ↓
ubRMSE ↓
Corr ↑
NSE ↑
LSTM SL
1.623 ± 0.87
1.589 ± 0.84
0.496 ± 0.08
0.398 ± 0.74
DLinear
1.605 ± 0.99
1.453 ± 0.99
0.512 ± 0.07
0.412 ± 0.81
Informer
1.562 ± 1.04
1.471 ± 0.98
0.435 ± 0.07
0.256 ± 0.92
Reformer
1.574 ± 1.06
1.507 ± 0.97
0.451 ± 0.08
0.378 ± 0.87
AlphaEarth LSTM
1.533 ± 0.97
1.495 ± 0.89
0.523 ± 0.09
0.489 ± 0.89
AlphaEarth resConn
1.424 ± 1.03
1.406 ± 1.00
0.541 ± 0.07
0.514 ± 0.79
StefaLand resConn
1.457 ± 0.87
1.401 ± 0.83
0.589 ± 0.06
0.533 ± 0.70
that integrates meteorological forcings, catchment attributes,
and observed streamflow for river basins worldwide. From
the full Caravan archive (16,300 basins), we restricted our
evaluation to the official CAMELS-family datasets, yielding
3,278 basins with relatively fuller streamflow records. From
this set, we constructed a curated subset of 3,026 basins by
excluding those with more than 75% missing streamflow ob-
servations during the 10-year evaluation period from 2010
to 2020, ensuring sufficient data quality for model training
and testing. This filtering removes sparsely observed basins
while preserving substantial geographic, climatic, and phys-
iographic diversity. We employed a five-fold random spatial
holdout protocol to evaluate generalization to unseen basins
at the global scale.
Across the global Caravan benchmark (Table 3), StefaLand-
resConn achieves the highest correlation and NSE among
all evaluated models, indicating improved agreement with
observed runoff dynamics under substantial spatial het-
erogeneity.
While error-based metrics such as RMSE
and ubRMSE vary considerably across basins, StefaLand-
resConn consistently improves correlation relative to both
supervised sequence models and alternative pretrained rep-
resentations. AlphaEarth-based variants yield noticeable
gains over purely supervised baselines, but remain below
StefaLand-resConn across most metrics. The Caravan is a
more noisy dataset due to global inconsistencies in data col-
lection. These results suggest that attribute-centric pretrain-
ing combined with residual temporal adaptation provides a
foundation to improve global hydrologic services.
3.3. Global Soil Moisture
We evaluated finetuning StefaLand for soil moisture pre-
dictions following (Liu et al., 2023a), using ISMN (Dorigo
et al., 2011; 2013a). Even though there is a globally cover-
ing satellite-based product for soil moisture, the data quality
can hardly match that of in-situ moisture sensors; thus the
ability to generalize in-situ data is valuable. ISMN consists
of 1,316 ground-based stations. We performed five-fold
spatial cross-validation for random holdout and a regional
holdout on Europe, training on all other continents while
excluding European sites (129) for testing. LSTM again
serves as the established state-of-the-art baseline (Wang
et al., 2024; Liu et al., 2023b).
Table 4. Soil moisture prediction across ISMN (random location
holdout). Values are median ± standard error across folds.
Model
RMSE ↓
ubRMSE ↓
Corr ↑
LSTM SL
0.073 ± 0.002
0.055 ± 0.001
0.764 ± 0.006
DLinear
0.088 ± 0.001
0.065 ± 0.001
0.612 ± 0.007
Informer
0.102 ± 0.002
0.082 ± 0.001
0.232 ± 0.012
Reformer
0.090 ± 0.002
0.071 ± 0.001
0.568 ± 0.015
TabPFN
0.068 ± 0.004
0.057 ± 0.003
0.404 ± 0.016
AlphaEarth LSTM
0.075 ± 0.001
0.062 ± 0.001
0.427 ± 0.019
AlphaEarth resConn
0.082 ± 0.001
0.067 ± 0.001
0.406 ± 0.012
StefaLand resConn
0.068 ± 0.001
0.054 ± 0.001
0.783 ± 0.005
Table 5. Soil moisture prediction across ISMN cross-continental
validation on Europe (129 sites).
Model
RMSE ↓
ubRMSE ↓
Corr ↑
LSTM SL
0.112
0.053
0.510
DLinear
0.093
0.051
0.623
Informer
0.088
0.063
0.358
Reformer
0.087
0.058
0.553
TabPFN
0.081
0.054
0.401
AlphaEarth LSTM
0.087
0.068
0.313
AlphaEarth resConn
0.090
0.071
0.308
StefaLand resConn
0.090
0.059
0.638
Against these baselines, the soil moisture experiments
demonstrate advantages of the StefaLand-resConn archi-
tecture (Tables 4 and 5).
For random spatial holdout,
StefaLand-resConn attains the highest correlation (0.783)
while also achieving the lowest ubRMSE (0.054) and match-
ing the best RMSE (0.068), outperforming the LSTM
baseline across all metrics. Although TabPFN achieves
comparable RMSE, its substantially lower correlation indi-
cates weaker agreement with temporal variability relative to
sequence-based models.
The regional holdout on Europe represents a more challeng-
ing cross-continental generalization setting. In this case,
StefaLand-resConn again achieves the highest correlation
(0.638), exceeding all baselines including LSTM and linear
or transformer-based models, while maintaining competitive
RMSE and ubRMSE. In contrast, AlphaEarth-based vari-
ants show limited transfer performance, with both LSTM
and residual-connection formulations yielding lower corre-
lations despite similar error magnitudes.
Overall, these results highlight that residual adaptation on
top of geoscience-pretrained representations is critical for
robust soil moisture prediction, particularly under strong
spatial distribution shift.
3.4. Soil Property Prediction
There are different soil datasets, each collected with differ-
ent protocols and data processing techniques, resulting in
significant discrepancies. In this test, we finetuned Stefa-
6

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Table 6. Soil composition prediction (clay). Values are median ±
standard error across folds.
Model
Corr ↑
R2 ↑
Random Forest
0.456 ± 0.02
0.207 ± 0.01
Linear Regression
0.138 ± 0.01
0.019 ± 0.01
AlphaEarth RF
0.462 ± 0.03
0.205 ± 0.02
StefaLand finetuned
0.509 ± 0.01
0.259 ± 0.01
Table 7. Soil composition prediction (sand). Values are median ±
standard error across folds.
Model
Corr ↑
R2 ↑
Random Forest
0.585 ± 0.01
0.342 ± 0.01
Linear Regression
0.347 ± 0.01
0.120 ± 0.01
AlphaEarth RF
0.615 ± 0.01
0.373 ± 0.01
StefaLand finetuned
0.704 ± 0.01
0.495 ± 0.01
Land to predict in situ soil profile data from another dataset
(ISRIC). This application can produce a seamless dataset
that is consistent with a set of in situ data, improving data
availability and addressing systematic biases. In addition, it
helps us understand the noise associated with each dataset.
StefaLand’s pretraining soils dataset is HWSD, which has
some overlap but also extensive differences from ISRIC,
which is larger and potentially noisier. We finetuned Ste-
faLand to predict one soil texture property (e.g., clay per-
centage) in ISRIC while masking the corresponding comple-
mentary attribute (e.g., sand) from the same profile to avoid
information leakage, probing how easy it is to infer soil
properties using other attributes such as climate, terrain, and
land cover. We compared StefaLand finetuning against Al-
phaEarth features incorporated into a random forest model,
as well as supervised random forest and linear regression
baselines. Train test splits can be found here C.5.
StefaLand finetuning achieves the strongest performance for
both clay and sand prediction, outperforming linear regres-
sion, random forest, and AlphaEarth RF baselines in terms
of both correlation and R2. While AlphaEarth RF improves
over standard random forest baselines, it remains consis-
tently below StefaLand finetuned across both soil properties.
These results indicate that StefaLand’s pretrained represen-
tations are particularly effective when adapted to infer soil
texture attributes from complementary variables and static
environmental context.
3.5. Landslide Susceptibility Prediction
Landslide is a geohazard that kill thousands each year. We
next evaluated StefaLand for landslide susceptibility pre-
diction using the SLIDO dataset from the State of Oregon,
which provides detailed landslide occurrence records. Fol-
lowing (Liu et al., 2025a), this is a binary classification task
indicating the presence or absence of landslides in a 30m by
30m patch.
Table 8. Landslide susceptibility prediction results on the Oregon
SLIDO dataset.
Model
Accuracy ↑
Precision ↑
Recall ↑
F1 ↑
ROC AUC ↑
Logistic Regression 2D
0.744
0.720
0.795
0.756
0.823
Random Forest 2D
0.765
0.737
0.822
0.777
0.849
CNN2D
0.880
0.896
0.858
0.877
0.954
StefaLand + CNN2D
0.903
0.859
0.963
0.908
0.911
Note: All baseline results (Logistic Regression 2D, Random Forest 2D, CNN2D) are
taken from previously published 10m-resolution experiments in (Liu et al., 2025a),
except for StefaLand + CNN2D, which represents our proposed method.
We finetuned StefaLand by extracting frozen hidden features
and concatenating them with a 2D CNN, then retrained
the CNN classifier to assess StefaLand’s ability to provide
generalizable geoscience features.
Results show that StefaLand’s pretrained features improved
the CNN’s generalization, yielding modest gains across
most metrics. This is a particularly difficult baseline to im-
prove, so even modest gains are rare. Recall increased from
0.858 to 0.963, and accuracy rose from 0.880 to 0.903, re-
flecting fewer misclassifications overall. While the random
forest achieves high precision in this particular run, it does
so at the cost of lower recall. Overall, StefaLand produces
well-rounded predictions, with both higher accuracy and
recall than CNN2D.
3.6. Ablations
To isolate the contributions of pretraining and task adapta-
tion in StefaLand, we conduct a structured ablation study
across multiple tasks and spatial evaluation protocols, com-
paring four variants against the proposed pretrained model
with task adapter.
Direct prediction removes pretraining entirely and treats the
target as an additional input channel, training the model
end to end only on downstream data. Scratch training uses
the full StefaLand architecture but trains all parameters
from random initialization, isolating the effect of large-scale
pretraining. No adapter removes the task-specific adapter
and feeds pretrained embeddings directly to the task decoder,
testing whether simple feature reuse is sufficient. Linear
probing freezes the pretrained encoder and applies only a
linear prediction head, representing the weakest form of
adaptation.
Across streamflow, soil moisture, and global Caravan exper-
iments, performance degradation relative to the full model is
dominated by the removal of pretraining. Direct prediction
and scratch training consistently yield the largest errors, es-
pecially under spatial generalization. In contrast, removing
or simplifying the adapter produces smaller but consistent
performance drops, indicating that task adaptation improves
results but cannot compensate for the absence of pretrained
representations.
7

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Figure 2. Ablation impact matrix across evaluation settings using
RMSE. Each cell shows the percent RMSE increase relative to the
full StefaLand ResConn model (lower is better), highlighting the
contributions of pretraining and task adaptation. Blank or hatched
cells indicate ablations not evaluated for that setting.
These trends are consistent across random and regional
holdouts and across tasks with differing data characteris-
tics, highlighting pretrained land-surface representations as
the primary driver of StefaLand’s performance. Numerical
results for ablations, are provided in Appendix B.4.
4. Discussion
4.1. Key Findings and Contributions
Methods that reliably improve spatial generalization to data-
scarce regions remain rare in the literature (Beery et al.,
2018; Gacu et al., 2025). In contrast, StefaLand combined
with lightweight task-specific heads achieves state-of-the-
art or competitive performance across four broad problem
classes: streamflow prediction (both CAMELS and global),
soil moisture, soil composition, and landslide susceptibility,
while also strengthening the parameterization of differen-
tiable process-based models. Across tasks, the strongest
gains arise from architectures that combine pretrained Stefa-
Land representations with explicit temporal modeling via
residual connections, indicating that attribute-centric pre-
training captures problem-relevant structure while down-
stream sequence models resolve task-specific dynamics. To-
gether, these results support the premise that foundation
models can improve out-of-domain transfer and help de-
mocratize prediction quality in data-scarce regions.
Across five dynamic prediction settings, evaluated against
benchmark models that reproduce state-of-the-art results re-
ported in prior work, a consistent pattern emerges. Pretrain-
ing StefaLand on landscape attributes yields deep representa-
tions that are highly relevant to hydrologic and land-surface
prediction tasks, enabling stronger spatial generalization
than purely supervised approaches such as LSTM-based
models or training from scratch. Comparisons with alterna-
tive pretrained representations further suggest that problem
relevance of the pretraining signal is at least as important
as scale alone, particularly for tasks governed by physical
and environmental processes rather than visual appearance.
We emphasize that this attribute-based approach is com-
plementary to satellite-centric foundation models: while
image-based models excel at extracting large-scale visual
patterns, StefaLand focuses on structured environmental at-
tributes that are directly aligned with land-surface processes,
offering a more targeted and efficient alternative.
A key practical advantage of StefaLand is computational
efficiency. The attribute-based pretraining strategy avoids
pixel-wise processing and large image volumes, resulting in
a compact transformer with roughly 12 million parameters
and substantially lower data-management requirements. As
a result, StefaLand pretraining can be performed on modest
computational budgets, making large-scale spatial general-
ization experiments feasible without access to specialized
infrastructure. While additional adapter and finetuning vari-
ants could be explored, the current results already demon-
strate strong performance across diverse tasks, and further
expansion must balance marginal gains against growing
computational and storage costs.
4.2. Limitations and Future Work
Several limitations remain. The selection of geological-
or ecologically-focused attributes is limited and more can
be added to further characterize the subsurface.
Two-
dimensional (or image-like) data like elevation map can
be selectively incorporated using vision transformer heads
in the future. Expanding the range of targets to include
variables such as evapotranspiration, snow water equiva-
lent, and groundwater levels would broaden its applicability.
Methodologically, advances such as uncertainty-aware pre-
diction heads, and tighter integration with additional process
models offer promising avenues to improve calibration and
interpretability while preserving efficiency. Overall, Stefa-
Land shows that attribute-centric pretraining combined with
lightweight temporal or physics heads can deliver strong
spatial generalization across geoscientific tasks while re-
maining computationally accessible. This points toward a
practical path for high-quality predictions in regions where
they are most needed but data are most limited.
References
Addor, N., Newman, A. J., Mizukami, N., and Clark,
M. P. The CAMELS data set: Catchment attributes and
8

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
meteorology for large-sample studies. Hydrology and
Earth System Sciences, 21(10):5293–5313, 2017. doi:
10.5194/hess-21-5293-2017.
Aghakouchak, A. and Habib, E. Application of a conceptual
hydrologic model in teaching hydrologic processes. Inter-
national Journal of Engineering Education, 26:963–973,
2010.
Amatulli, G., Domisch, S., Tuanmu, M.-N., Parmentier,
B., Ranipeta, A., Malczyk, J., and Jetz, W.
A suite
of global, cross-scale topographic variables for envi-
ronmental and biodiversity modeling. Scientific Data,
5(1):180040, March 2018.
ISSN 2052-4463.
doi:
10.1038/sdata.2018.40. URL https://www.na
ture.com/articles/sdata201840. Number: 1
Publisher: Nature Publishing Group.
Batjes, N. H., Ribeiro, E., and van Oostrum, A. Standardised
soil profile data to support global mapping and modelling
(WoSIS snapshot 2019). Earth System Science Data, 12:
299–320, 2020. doi: 10.5194/essd-12-299-2020.
Beck, H. E., Wood, E. F., Pan, M., Fisher, C. K., Miralles,
D. G., van Dijk, A. I. J. M., McVicar, T. R., and Adler,
R. F.
MSWEP v2 global 3-hourly 0.1 precipitation:
Methodology and quantitative assessment. Bulletin of
the American Meteorological Society, 100(3):473–500,
2019. doi: 10.1175/BAMS-D-17-0138.1.
Beck, H. E., Pan, M., Lin, P., Seibert, J., van Dijk, A. I.
J. M., and Wood, E. F. Global fully distributed parameter
regionalization based on observed streamflow from 4,229
headwater catchments. Journal of Geophysical Research:
Atmospheres, 125:e2019JD031485, 2020. doi: 10.1029/
2019JD031485.
Beck, H. E., Pan, M., and et al. Mswx: A multi-source
weather and climate forcing dataset. Bulletin of the Amer-
ican Meteorological Society, 103(3):E710–E732, 2022.
doi: 10.1175/BAMS-D-21-0145.1.
Beery, S., Van Horn, G., and Perona, P. Recognition in terra
incognita. In Proceedings of the European Conference
on Computer Vision (ECCV), September 2018.
Bergstr¨om, S. Development and application of a concep-
tual runoff model for Scandinavian catchments. PhD
thesis, Swedish Meteorological and Hydrological Insti-
tute (SMHI), Norrk¨oping, Sweden, 1976. URL http:
//urn.kb.se/resolve?urn=urn:nbn:se:
smhi:diva-5738.
Bergstr¨om, S. The HBV model—its structure and applica-
tions. Technical report, Swedish Meteorological and Hy-
drological Institute (SMHI), Norrk¨oping, Sweden, 1992.
URL https://www.smhi.se/en/publicati
ons/the-hbv-model-its-structure-and
-applications-1.83591.
Bodnar, C., Bruinsma, W. P., Lucic, A., Stanley, M.,
Allen, A., Brandstetter, J., Garvan, P., Riechert, M.,
Weyn, J. A., Dong, H., Gupta, J. K., Thambiratnam, K.,
Archibald, A. T., Wu, C.-C., Heider, E., Welling, M.,
Turner, R. E., and Perdikaris, P. A foundation model for
the earth system. Nature, 641(8004):1180–1187, 2025.
doi: 10.1038/s41586-025-09005-y. URL https:
//doi.org/10.1038/s41586-025-09005-y.
Bommasani, R., Hudson, D. A., Adeli, E., Altman, R.,
Arora, S., von Arx, S., Bernstein, M. S., Bohg, J., Bosse-
lut, A., Brunskill, E., Brynjolfsson, E., Buch, S., Card,
D., Castellon, R., Chatterji, N., Chen, A., Creel, K.,
Davis, J. Q., Demszky, D., Donahue, C., Doumbouya,
M., Durmus, E., Ermon, S., Etchemendy, J., Ethayarajh,
K., Fei-Fei, L., Finn, C., Gale, T., Gillespie, L., Goel,
K., Goodman, N., Grossman, S., Guha, N., Hashimoto,
T., Henderson, P., Hewitt, J., Ho, D. E., Hong, J., Hsu,
K., Huang, J., Icard, T., Jain, S., Jurafsky, D., Kalluri, P.,
Karamcheti, S., Keeling, G., Khani, F., Khattab, O., Koh,
P. W., Krass, M., Krishna, R., Kuditipudi, R., Kumar, A.,
Ladhak, F., Lee, M., Lee, T., Leskovec, J., Levent, I., Li,
X. L., Li, X., Ma, T., Malik, A., Manning, C. D., Mirchan-
dani, S., Mitchell, E., Munyikwa, Z., Nair, S., Narayan,
A., Narayanan, D., Newman, B., Nie, A., Niebles, J. C.,
Nilforoshan, H., Nyarko, J., Ogut, G., Orr, L., Papadim-
itriou, I., Park, J. S., Piech, C., Portelance, E., Potts, C.,
Raghunathan, A., Reich, R., Ren, H., Rong, F., Roohani,
Y., Ruiz, C., Ryan, J., R´e, C., Sadigh, D., Sagawa, S.,
Santhanam, K., Shih, A., Srinivasan, K., Tamkin, A.,
Taori, R., Thomas, A. W., Tram`er, F., Wang, R. E., Wang,
W., Wu, B., Wu, J., Wu, Y., Xie, S. M., Yasunaga, M.,
You, J., Zaharia, M., Zhang, M., Zhang, T., Zhang, X.,
Zhang, Y., Zheng, L., Zhou, K., and Liang, P. On the
opportunities and risks of foundation models, 2022. URL
https://arxiv.org/abs/2108.07258.
Brown, C. F., Kazmierski, M. R., Pasquarella, V. J., Ruck-
lidge, W. J., Samsikova, M., Zhang, C., Shelhamer, E.,
Lahera, E., Wiles, O., Ilyushchenko, S., Gorelick, N.,
Zhang, L. L., Alj, S., Schechter, E., Askay, S., Guinan,
O., Moore, R., Boukouvalas, A., and Kohli, P. Alphaearth
foundations: An embedding field model for accurate and
efficient global mapping from sparse label data, 2025.
URL https://arxiv.org/abs/2507.22291.
Chaney, N. W., Minasny, B., Herman, J. D., Nauman, T. W.,
Brungard, C. W., Morgan, C. L. S., McBratney, A. B.,
Wood, E. F., and Yimam, Y. POLARIS Soil Proper-
ties: 30-m Probabilistic Maps of Soil Properties Over the
Contiguous United States. Water Resources Research,
55(4):2916–2938, April 2019. ISSN 0043-1397. doi:
9

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
10/ggj68b. URL https://onlinelibrary.wile
y.com/doi/abs/10.1029/2018WR022797.
CIESIN.
Gridded Population of the World, Version 4
(GPWv4): Administrative Unit Center Points with Pop-
ulation Estimates, 2016. URL https://beta.sed
ac.ciesin.columbia.edu/data/set/gpw-v
4-admin-unit-center-points-populatio
n-estimates.
Danielson, J. J. and Gesch, D. B. Global multi-resolution
terrain elevation data 2010 (GMTED2010). Technical
Report 2011-1073, U.S. Geological Survey, 2011. URL
https://pubs.usgs.gov/publication/of
r20111073. ISSN: 2331-1258 Publication Title: Open-
File Report.
Devlin, J., Chang, M.-W., Lee, K., and Toutanova, K. N.
Bert: Pre-training of deep bidirectional transformers for
language understanding. In Proceedings of the 2019 Con-
ference of the North American Chapter of the Association
for Computational Linguistics: Human Language Tech-
nologies, Volume 1 (Long and Short Papers), 2018. URL
https://arxiv.org/abs/1810.04805.
Dewitz, J. National Land Cover Dataset (NLCD) 2016
Products (ver. 2.0, July 2020), 2019. URL https://
www.sciencebase.gov/catalog/item/5d4
c6a1de4b01d82ce8dfd2f. Website Title: United
States Geological Survey.
Didan, K. MOD13A2: MODIS/Terra Vegetation Indices
16-Day L3 Global 1km SIN Grid version 6, 2015a. URL
https://lpdaac.usgs.gov/products/mod
13a2v006/.
Website Title: NASA EOSDIS Land
Processes DAAC.
Didan, K. MOD13Q1 MODIS/Terra Vegetation Indices
16-Day L3 Global 250m SIN Grid V006, 2015b. URL
https://lpdaac.usgs.gov/products/mod
13q1v006/.
Didan, K., Huete, A., and MODAPS SIPS - NASA.
MOD13C2: MODIS/Terra Vegetation Indices Monthly
L3 Global 0.05Deg CMG version 6, 2015. URL https:
//lpdaac.usgs.gov/products/mod13c2v0
06/. tex.ids= didankamel2015mod13c2.
Dorigo, W. A., Wagner, W., Hohensinn, R., Hahn, S., Paulik,
C., Xaver, A., Gruber, A., Drusch, M., Mecklenburg, S.,
van Oevelen, P., Robock, A., and Jackson, T. The Inter-
national Soil Moisture Network: A data hosting facility
for global in situ soil moisture measurements. Hydrology
and Earth System Sciences, 15(5):1675–1698, May 2011.
ISSN 1027-5606. doi: 10.5194/hess-15-1675-2011. URL
https://hess.copernicus.org/articles
/15/1675/2011/. Publisher: Copernicus GmbH
tex.ids= dorigo2011internationala.
Dorigo, W. A., Xaver, A., Vreugdenhil, M., Gruber, A.,
Hegyiov´a, A., Sanchis-Dufau, A. D., Zamojski, D.,
Cordes, C., Wagner, W., and Drusch, M. Global auto-
mated quality control of in situ soil moisture data from the
international soil moisture network. Vadose Zone Journal,
12(3):vzj2012.0097, 2013a. doi: 10.2136/vzj2012.0097.
Dorigo, W. A., Xaver, A., Vreugdenhil, M., Gruber,
A., Hegyiov´a, A., Sanchis-Dufau, A., Zamojski, D.,
Cordes, C., Wagner, W., and Drusch, M.
Global
automated quality control of in situ soil moisture
data from the international soil moisture network.
Vadose Zone Journal,
12(3):vzj2012.0097,
2013b.
ISSN 1539-1663. doi: 10.2136/vzj2012.0097. URL
https://onlinelibrary.wiley.com/
doi/abs/10.2136/vzj2012.0097.
eprint:
https://onlinelibrary.wiley.com/doi/pdf/10.2136/vzj2012.0097
tex.ids= dorigo2013globala.
Ebi, K. L., Vanos, J., Baldwin, J. W., Bell, J. E., Hondula,
D. M., Errett, N. A., Hayes, K., Reid, C. E., Saha, S.,
Spector, J., and Berry, P. Extreme weather and climate
change: Population health and health system implications.
Annual Review of Public Health, 42:293–315, April 2021.
doi: 10.1146/annurev-publhealth-012420-105026.
PMID: 33406378; PMCID: PMC9013542.
Entekhabi, D., Njoku, E. G., O’Neill, P. E., Kellogg, K. H.,
Crow, W. T., Edelstein, W. N., Entin, J. K., Good-
man, S. D., Jackson, T. J., Johnson, J., Kimball, J.,
Piepmeier, J. R., Koster, R. D., Martin, N., McDonald,
K. C., Moghaddam, M., Moran, S., Reichle, R., Shi,
J. C., Spencer, M. W., Thurman, S. W., Tsang, L., and
Van Zyl, J. The soil moisture active passive (smap) mis-
sion. Proceedings of the IEEE, 98(5):704–716, 2010. doi:
10.1109/JPROC.2010.2043918.
ESA. Land Cover CCI Product User Guide Version 2, 2017.
URL maps.elie.ucl.ac.be/CCI/viewer/d
ownload/ESACCI-LC-Ph2-PUGv2_2.0.pdf.
FAO, IIASA, ISRIC, ISSCAS, and JRC. Harmonized World
Soil Database (version 1.2), 2012. URL http://www.
fao.org/soils-portal/data-hub/soil-m
aps-and-databases/harmonized-world-s
oil-database-v12/en/. Website Title: United
Nations Food and Agriculture Organization.
Feng, D., Lawson, K., and Shen, C. Mitigating prediction
error of deep learning streamflow models in large data-
sparse regions with ensemble modeling and soft data.
Geophysical Research Letters, 48(12):e2021GL092999,
2021. doi: 10.1029/2021GL092999.
Feng, D., Beck, H., Lawson, K., and Shen, C.
The
suitability of differentiable, physics-informed machine
learning hydrologic models for ungauged regions and
10

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
climate change impact assessment.
Hydrology and
Earth System Sciences, 27(12):2357–2373, 2023. doi:
10.5194/hess-27-2357-2023.
Franczyk, J. J, Burns, W. J, and Calhoun, N. C. Statewide
landslide information database for Oregon, release 4
(SLIDO-4.4), 2020.
Gacu, J. G., Monjardin, C. E. F., Mangulabnan, R. G. T.,
and Mendez, J. C. F. Application of artificial intelligence
in hydrological modeling for streamflow prediction in
ungauged watersheds: A review. Water, 17(18):2722,
2025. ISSN 2073-4441. doi: 10.3390/w17182722. URL
https://www.mdpi.com/2073-4441/17/18/
2722.
Gesch, D. B., Evans, G. A., Oimoen, M. J., and Arundel,
S. The National Elevation Dataset. In American Society
for Photogrammetry and Remote Sensing (ed.), Manual
of Photogrammetry, pp. 83–110. American Society for
Photogrammetry and Remote Sensing, 2018. URL http
s://pubs.usgs.gov/publication/702015
72. tex.ids= gesch2018nationala.
Gleeson, T., Moosdorf, N., Hartmann, J., and van Beek,
L. P. H. A glimpse beneath earth’s surface: GLobal
HYdrogeology MaPS (GLHYMPS) of permeability and
porosity. Geophysical Research Letters, 41(11):3891–
3898, June 2014. ISSN 00948276. doi: 10.1002/2014GL
059856. URL http://doi.wiley.com/10.100
2/2014GL059856.
Global Runoff Data Centre. Global runoff database, 2020.
URL https://www.bafg.de/GRDC/. Accessed:
2020-04-12.
GRDC. The Global Runoff Data Centre, 2024. URL http
s://grdc.bafg.de/.
Hartmann, J. and Moosdorf, N. The new global lithological
map database GLiM: A representation of rock properties
at the Earth surface. Geochemistry, Geophysics, Geosys-
tems, 13(12):2012GC004370, December 2012. ISSN
1525-2027, 1525-2027. doi: 10.1029/2012GC004370.
URL https://agupubs.onlinelibrary.wi
ley.com/doi/10.1029/2012GC004370.
Hochreiter, S. and Schmidhuber, J. Long short-term memory.
Neural Computation, 9(8):1735–1780, 1997. doi: 10.116
2/neco.1997.9.8.1735. URL https://doi.org/10
.1162/neco.1997.9.8.1735.
Hollmann, N., M¨uller, S., Purucker, L., et al. Accurate
predictions on small data with a tabular foundation model.
Nature, 637:319–326, January 2025. doi: 10.1038/s415
86-024-08328-6. URL https://doi.org/10.103
8/s41586-024-08328-6.
Hrachowitz, M., Savenije, H. H. G., Bl¨oschl, G., McDonnell,
J. J., Sivapalan, M., Pomeroy, J. W., Arheimer, B., Blume,
T., Clark, M. P., Ehret, U., Fenicia, F., Freer, J. E., Gelfan,
A., Gupta, H. V., Hughes, D. A., Hut, R. W., Montanari,
A., Pande, S., Tetzlaff, D., Troch, P. A., Uhlenbrook, S.,
Wagener, T., Winsemius, H. C., Woods, R. A., Zehe, E.,
and Cudennec, C. A decade of predictions in ungauged
basins (pub)—a review. Hydrological Sciences Journal,
58(6):1198–1255, 2013. doi: 10.1080/02626667.2013.80
3183.
Hsu, C.-Y., Li, W., and Wang, S. Geospatial foundation
models for image analysis: Evaluating and enhancing
NASA-IBM Prithvi’s domain adaptability. International
Journal of Geographical Information Science, pp. 1–30,
2024. doi: 10.1080/13658816.2024.2397441.
Huffman, G. J., Stocker, E. F., Bolvin, D. T., Nelkin, E. J.,
and Tan, J. Gpm imerg final precipitation l3 1 month 0.1
degree x 0.1 degree v06, 2019.
IPCC. Summary for policymakers. In Masson-Delmotte, V.,
Zhai, P., Pirani, A., Connors, S. L., P´ean, C., Berger, S.,
Caud, N., Chen, Y., Goldfarb, L., Gomis, M. I., Huang,
M., Leitzell, K., Lonnoy, E., Matthews, J. B. R., Maycock,
T. K., Waterfield, T., Yelekc¸i, O., Yu, R., and Zhou, B.
(eds.), Climate Change 2021: The Physical Science Ba-
sis. Contribution of Working Group I to the Sixth Assess-
ment Report of the Intergovernmental Panel on Climate
Change. Cambridge University Press, 2021.
Jakubik, J., Roy, S., Phillips, C. E., Fraccaro, P., Godwin,
D., Zadrozny, B., Szwarcman, D., Gomes, C., Nyirjesy,
G., Edwards, B., Kimura, D., Simumba, N., Chu, L.,
Mukkavilli, S. K., Lambhate, D., Das, K., Bangalore, R.,
Oliveira, D., Muszynski, M., et al. Foundation models for
generalist geospatial artificial intelligence, 2023. URL
https://arxiv.org/abs/2310.18660.
Jakubik, J., Yang, F., Blumenstiel, B., Scheurer, E., Se-
dona, R., Maurogiovanni, S., Bosmans, J., Dionelis, N.,
Marsocci, V., Kopp, N., Ramachandran, R., Fraccaro,
P., Brunschwiler, T., Cavallaro, G., Bernabe-Moreno,
J., and Long´ep´e, N.
TerraMind: Large-scale genera-
tive multimodality for Earth observation, 2025. URL
https://arxiv.org/abs/2504.11171.
Kitaev, N., Kaiser, L., and Levskaya, A. Reformer: The
efficient transformer. In International Conference on
Learning Representations, 2020. URL https://open
review.net/forum?id=rkgNKkHtvB.
Kratzert, F., Klotz, D., Brenner, C., Schulz, K., and
Herrnegger, M. Rainfall–runoff modelling using long
short-term memory (lstm) networks.
Hydrology and
Earth System Sciences, 22(11):6005–6022, 2018. doi:
10.5194/hess-22-6005-2018.
11

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Kratzert, F., Klotz, D., Brenner, C., Schulz, K., and Herrneg-
ger, M. Toward learning universal, regional, and local
hydrological behaviors via machine learning. Hydrology
and Earth System Sciences, 23(12):5089–5110, 2019. doi:
10.5194/hess-23-5089-2019.
Kratzert, F., Nearing, G., Addor, N., Erickson, T., Gauch,
M., Gilon, O., Gudmundsson, L., Hassidim, A., Klotz, D.,
Nevo, S., et al. Caravan-a global community dataset for
large-sample hydrology. Scientific Data, 10(1):61, 2023.
Kummu, M., Taka, M., and Guillaume, J. H. A.
Grid-
ded global miscs for gross domestic product and human
development index over 1990–2015.
Scientific Data,
5(1):180004, February 2018.
ISSN 2052-4463.
doi:
10.1038/sdata.2018.4. URL https://www.nature
.com/articles/sdata20184. Publisher: Nature
Publishing Group.
Lacoste, A., Lehmann, N., Rodriguez, P., Sherwin, E. D.,
Kerner, H., L¨utjens, B., Irvin, J. A., Dao, D., Alemoham-
mad, H., Drouin, A., Gunturkun, M., Huang, G., Vazquez,
D., Newman, D., Bengio, Y., Ermon, S., and Zhu, X. X.
Geo-bench: Toward foundation models for earth monitor-
ing, 2023. URL https://arxiv.org/abs/2306
.03831.
Lehner, B. and Grill, G. Global river hydrography and net-
work routing: baseline data and new approaches to study
the world’s large river systems. Hydrological Processes,
27(15):2171–2186, 2013.
Li, H.-Y., Leung, L. R., Getirana, A., Huang, M., Wu,
H., Xu, Y., Guo, J., and Voisin, N. Evaluating global
streamflow simulations by a physically based routing
model coupled with the community land model. Jour-
nal of Hydrometeorology, 16(2):948–971, 2015.
doi:
10.1175/JHM-D-14-0079.1.
Liu, J., Rahmani, F., Lawson, K., and Shen, C. A multiscale
deep learning model for soil moisture integrating satellite
and in situ data. Geophysical Research Letters, 49(7):
e2021GL096847, 2022.
Liu, J., Hughes, D., Rahmani, F., Lawson, K., and Shen, C.
Evaluating a global soil moisture misc from a multitask
model (GSM3 v1.0) with potential applications for crop
threats. Geoscientific Model Development, 16(5):1553–
1567, 2023a. doi: 10.5194/gmd-16-1553-2023.
Liu, J., Hughes, D., Rahmani, F., Lawson, K., and Shen, C.
Evaluating a global soil moisture misc from a multitask
deep learning model. Geoscientific Model Development,
16(5):1553–1567, 2023b. doi: 10.5194/gmd-16-1553-2
023.
Liu, J., Bian, Y., and Shen, C. Probing the limit of hydro-
logic predictability with the transformer network. Journal
of Hydrology, 2024. doi: 10.1016/j.jhydrol.2024.131389.
Liu, J., Pei, T., Shen, C., , Kifer, D., and Lawson, K.
The value of terrain pattern, high-resolution data and
ensemble modeling for landslide susceptibility predic-
tion. ESS Open Archive preprint, June 2025a. URL
http://dx.doi.org/10.22541/essoar.175
130065.56738480/v1.
Liu, J., Shen, C., O’Donncha, F., Song, Y., Zhi, W., Beck,
H. E., Bindas, T., Kraabel, N., and Lawson, K. From
rnns to transformers: benchmarking deep learning archi-
tectures for hydrologic prediction. Hydrology and Earth
System Sciences, 29(23):6811–6828, 2025b.
Mu˜noz-Sabater, J., Dutra, E., Agust´ı-Panareda, A., et al.
ERA5-Land: A state-of-the-art global reanalysis misc
for land applications. Earth System Science Data, 13(9):
4349–4383, 2021. doi: 10.5194/essd-13-4349-2021.
Mu˜noz Sabater, J. ERA5-Land hourly data from 1950 to
present, Copernicus Climate Change Service (C3S) Cli-
mate Data Store (CDS) [data set], 2019. URL https:
//doi.org/10.24381/cds.e2161bac.
Nearing, G., Cohen, D., Dube, V., Gauch, M., Gilon, O.,
Harrigan, S., Hassidim, A., Klotz, D., Kratzert, F., Met-
zger, A., Nevo, S., Pappenberger, F., Prudhomme, C.,
Shalev, G., Shenzis, S., Tekalign, T. Y., Weitzner, D.,
and Matias, Y. Global prediction of extreme floods in
ungauged watersheds. Nature, 2024. doi: 10.1038/s415
86-024-07145-1.
Nearing, G. S., Kratzert, F., Sampson, A. K., Pelissier,
C. S., Klotz, D., Frame, J. M., Prieto, C., and Gupta,
H. V. What role does hydrological science play in the
age of machine learning?
Water Resources Research,
57(3):e2020WR028091, 2021.
doi: https://doi.org/
10.1029/2020WR028091.
URL https://agup
ubs.onlinelibrary.wiley.com/doi/ab
s/10.1029/2020WR028091.
e2020WR028091
10.1029/2020WR028091.
Newman, A. J., Sampson, K., Clark, M. P., Bock, A., Viger,
R. J., and Blodgett, D. A large-sample watershed-scale
hydrometeorological misc for the contiguous USA, 2014.
URL https://doi.org/10.5065/D6MW2F4D.
Data set.
Newman, A. J., Mizukami, N., Clark, M. P., Wood, A. W.,
Nijssen, B., and Nearing, G. Benchmarking of a physi-
cally based hydrologic model. Journal of Hydrometeorol-
ogy, 18:2215–2225, 2017. doi: 10.1175/JHM-D-16-028
4.1.
12

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Pelletier, J. D., Broxton, P. D., Hazenberg, P., Zeng, X.,
Troch, P. A., Niu, G., Williams, Z. C., Brunke, M. A.,
and Gochis, D. Global 1-km Gridded Thickness of Soil,
Regolith, and Sedimentary Deposit Layers. ORNL DAAC,
February 2016. doi: 10.3334/ORNLDAAC/1304. URL
https://daac.ornl.gov/cgi-bin/dsviewe
r.pl?ds_id=1304.
Potapov, P., Hansen, M. C., Laestadius, L., Turubanova,
S., Yaroshenko, A., Thies, C., Smith, W., Zhuravleva, I.,
Komarova, A., Minnemeyer, S., and Esipova, E. The
last frontiers of wilderness: Tracking loss of intact forest
landscapes from 2000 to 2013. Science Advances, 3(1):
e1600821, January 2017. ISSN 2375-2548. doi: 10.112
6/sciadv.1600821. URL https://www.science.
org/doi/10.1126/sciadv.1600821.
PRISM Climate Group. PRISM Climate Data, February
2014. URL https://prism.oregonstate.edu.
Ramcharan, A., Hengl, T., Nauman, T., Brungard, C., Walt-
man, S., Wills, S., and Thompson, J. Soil property and
class maps of the conterminous united states at 100 m
resolution. Soil Science Society of America Journal, 82
(1):186–201, 2018. doi: 10.2136/sssaj2017.04.0122.
Sabzipour, B., Arsenault, R., Troin, M., Martel, J.-L.,
Brissette, F., Brunet, F., and Mai, J.
Comparing a
long short-term memory (lstm) neural network with
a physically-based hydrological model for streamflow
forecasting over a canadian catchment. Journal of Hy-
drology, 627:130380, 2023.
ISSN 0022-1694.
doi:
https://doi.org/10.1016/j.jhydrol.2023.130380. URL
https://www.sciencedirect.com/scienc
e/article/pii/S0022169423013227.
Schaaf, Crystal and Wang, Zhuosen. MODIS/Terra+Aqua
BRDF/Albedo Daily L3 Global - 500m V061, 2021. URL
https://lpdaac.usgs.gov/products/mcd
43a3v061/.
Website Title: NASA EOSDIS Land
Processes DAAC.
Schmude, J., Roy, S., Trojak, W., Jakubik, J., Salles Civ-
itarese, D., Singh, S., Kuehnert, J., Ankur, K., Gupta, A.,
Phillips, C. E., Kienzler, R., Szwarcman, D., Gaur, V.,
Shinde, R., Lal, R., Da Silva, A., Diaz, J. L. G., Jones,
A., Pfreundschuh, S., Lin, A., Sheshadri, A., Nair, U.,
Anantharaj, V., Hamann, H., Watson, C., Maskey, M.,
Lee, T. J., Moreno, J. B., and Ramachandran, R. Prithvi
wxc: Foundation model for weather and climate, 2024.
URL https://arxiv.org/abs/2409.13598.
Seibert, J. and Vis, M. J. P. Teaching hydrological modeling
with a user-friendly catchment-runoff-model software
package. Hydrology and Earth System Sciences, 16:3315–
3325, 2012. doi: 10.5194/hess-16-3315-2012.
Shen, C., Appling, A. P., Gentine, P., Bandai, T., Gupta, H.,
Tartakovsky, A., Baity-Jesi, M., Fenicia, F., Kifer, D., Li,
L., Liu, X., Ren, W., Zheng, Y., Harman, C. J., Clark, M.,
Farthing, M., Feng, D., Kumar, P., Aboelyazeed, D., and
Lawson, K. Differentiable modelling to unify machine
learning and physical models for geosciences. Nature
Reviews Earth & Environment, 4(8):552–567, 2023. doi:
10.1038/s43017-023-00450-9.
Solomatine, D. P. and Ostfeld, A. Data-driven modelling:
Some past experiences and new approaches. Journal of
Hydroinformatics, 10(1):3–22, 2008. doi: 10.2166/hydro.
2008.015.
Song, Y., Sawadekar, K., Frame, J. M., and Pan, M. Physics-
informed, differentiable hydrologic models for capturing
unseen extreme events. ESS Open Archive, March 2025.
URL https://essopenarchive.org/doi/10.
22541/essoar.172304428.82707157/v2.
Troch, P. A., Lahmers, T., Meira, A., Mukherjee, R., Ped-
ersen, J. W., Roy, T., and Vald´es-Pineda, R.
Catch-
ment coevolution:
A useful framework for improv-
ing predictions of hydrological change?
Water Re-
sources Research, 51(7):4903–4922, 2015. doi: https:
//doi.org/10.1002/2015WR017032. URL https:
//agupubs.onlinelibrary.wiley.com/do
i/abs/10.1002/2015WR017032.
Tseng, G., Cartuyvels, R., Zvonkov, I., Purohit, M., Rolnick,
D., and Kerner, H. Lightweight, pre-trained transformers
for remote sensing timeseries, 2023.
Tseng, G., Fuller, A., Reil, M., Herzog, H., Beukema,
P., Bastani, F., Green, J. R., Shelhamer, E., Kerner, H.,
and Rolnick, D. Galileo: Learning global & local fea-
tures of many remote sensing modalities. arXiv preprint
arXiv:2502.09356, 2025.
Vergopolan, N., Chaney, N. W., Beck, H., Pan, M., Sheffield,
J., and Wood, E. F. SMAP-HydroBlocks, a 30-m satellite-
based soil moisture misc for the conterminous us. Scien-
tific Data, 8(1):254, 2021. doi: 10.1038/s41597-021-010
50-2.
Wan, Z., Hook, S., and Hulley, G. Myd11a1 modis/aqua
land surface temperature/emissivity daily l3 global 1km
sin grid v061, 2021.
Wang, Y. et al. A comprehensive study of deep learning for
soil moisture prediction. Hydrology and Earth System
Sciences, 28:917–936, 2024. doi: 10.5194/hess-28-917
-2024.
Wen, Q., Zhou, T., Zhang, C., Chen, W., Ma, Z., Yan, J.,
and Sun, L. Transformers in time series: A survey, 2023.
URL https://arxiv.org/abs/2202.07125.
13

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Xie, Y., Wang, Z., Mai, G., Li, Y., Jia, X., Gao, S., and
Wang, S. Geo-foundation models: Reality, gaps and op-
portunities. In Proceedings of the 31st ACM International
Conference on Advances in Geographic Information Sys-
tems, pp. 1–4, 2023. doi: doi/10.1145/3589132.3625616.
Xue, W., Li, T., Zhou, L., Liu, P., Qiao, Y., and Zhang, L.
Make transformer great again for time series forecasting.
arXiv preprint arXiv:2305.12095, 2023. URL https:
//arxiv.org/abs/2305.12095.
Yang, X., Li, F., Qi, W., Zhang, M., Yu, C., and Xu, C.-
Y. Regionalization methods for PUB: a comprehensive
review of progress after the PUB decade. Hydrology
Research, 54(7):885–900, July 2023. doi: 10.2166/nh.2
023.027.
Zeng, A., Chen, M., Zhang, L., and Xu, Q. Are transformers
effective for time series forecasting?
arXiv preprint
arXiv:2205.13504, 2022. URL https://arxiv.or
g/abs/2205.13504.
Zhang, H., Xu, J.-J., Cui, H.-W., Li, L., Yang, Y., Tang,
C.-S., and Boers, N. When geoscience meets foundation
models: Toward a general geoscience artificial intelli-
gence system. IEEE Geoscience and Remote Sensing
Magazine, pp. 2–41, 2024. doi: 10.1109/MGRS.2024.34
96478.
Zhou, H., Zhang, S., Peng, J., Zhang, S., Li, J., Xiong, H.,
and Zhang, W. Informer: Beyond efficient transformer
for long sequence time-series forecasting. In Proceedings
of the Thirty-Fifth AAAI Conference on Artificial Intelli-
gence, volume 35, pp. 11106–11115. AAAI Press, 2021.
URL https://ojs.aaai.org/index.php/A
AAI/article/view/17325.
14

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
A. Detailed Model Architecture
This appendix provides the complete mathematical formulation of the StefaLand model architecture.
A.1. Embedding Dynamic and Static Inputs
StefaLand independently embeds each dynamic and static variable into a latent space. Specifically, for each dynamic
variable c at each time step t, a two-step nonlinear embedding is applied individually:
zt,c = GELU(xt,cW1,c + b1,c)W2,c + b2,c
(4)
where W1,c ∈R1×64 and W2,c ∈R64×256 are embedding parameters. After embedding all dynamic variables individually,
embeddings are stacked and summed across the variable dimension, resulting in a single embedding vector per time step:
zt =
C
X
c=1
zt,c
(5)
Similarly, static attributes are embedded individually:
zstatic,i = GELU(siW1,i + b1,i)W2,i + b2,i
(6)
where separate embedding layers are used for static features. These individual static embeddings are then concatenated with
dynamic embeddings along the temporal dimension, resulting in a unified embedding tensor:
Z = [z1; z2; . . . ; zT ; zstatic]
(7)
This static embedding acts as a global learnable token, allowing the model to incorporate basin-specific context into temporal
dynamics at any depth of the Transformer layers.
A.2. Location-aware Cross-Variable Group Masking
StefaLand introduces Cross-Variable Group Masking (CVGM), a masking strategy that forces the model to capture
interactions among correlated hydrologic variables rather than treating them independently. Given a predefinition of
hydrological variables into groups G = {g1, g2, . . . , gk}, masking occurs as follows:
1. A temporal masking window [τ, τ + ℓ) is randomly sampled with length ℓ∼U(Lmin, Lmax).
2. For each variable group gk, a Bernoulli mask indicator mk ∼Bernoulli(pmask) determines whether the group is masked.
3. For each time step t within the masked temporal window and each variable c belonging to masked groups, the embedded
feature vector is replaced by a learned mask vector mc.
Each hydrologic variable c has its own trainable mask embedding vector mc ∈R256. This CVGM procedure creates
reconstruction targets that require modeling cross-variable dependencies and physical interactions.
A.3. Learnable Positional Encoding
To provide positional information, StefaLandemploys learnable positional encoding. Each position i, corresponding to
each time step and the appended static embedding, is assigned a trainable embedding vector pi. The encoded embedding
becomes:
˜Z = Z + P
(8)
where P = [p1; . . . ; pT +1].
15

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
A.4. Transformer Encoder
The embeddings enriched by positional encoding are processed through an N-layer Transformer encoder, where each
Transformer block successively applies Multi-Head Self-Attention (MHA) with h attention heads, followed by a residual
connection and Layer Normalization. Subsequently, a position-wise Feedforward Network (FFN) is applied, also followed
by another residual connection and Layer Normalization:
A(ℓ) = MHA(H(ℓ−1))
(9)
˜H(ℓ) = LayerNorm(H(ℓ−1) + A(ℓ))
(10)
F (ℓ) = FFN( ˜H(ℓ))
(11)
H(ℓ) = LayerNorm( ˜H(ℓ) + F (ℓ))
(12)
A.5. Reconstruction of Original Inputs
The final hidden states from the Transformer encoder, H(N), are linearly projected and passed through a single-layer
bidirectional LSTM to capture the local temporal dependencies and continuity:
U = LSTM(H(N)Wenc-proj + benc-proj)
(13)
The outputs U are then separated into dynamic and static components, Ut and Ustatic, corresponding to the temporal sequence
and static attributes:
Ut, Ustatic = U1:T , UT +1
(14)
Finally, both dynamic and static representations are individually projected back to their original dimensions through separate
embedding layers, reconstructing the masked portions of the inputs. Dynamic variables are restored via:
ˆxt = DynamicDecEmbedding(Ut)
(15)
while static attributes are restored by:
ˆs = StaticDecEmbedding(Ustatic)
(16)
The projections leverage the learned latent representations to reconstruct the original hydrologic inputs.
16

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
B. Additional Experiments
B.1. Physics-Based Differentiable Modeling
To leverage domain knowledge and physical constraints inherent in hydrological systems, we implemented physics-based
models that explicitly represent hydrological processes through mathematical formulations. These differentiable versions
can be trained end-to-end within neural network frameworks, combining process understanding with machine learning
flexibility (Shen et al., 2023).
For the process-based backbone, we employed the Hydrologiska Byr˚ans Vattenbalansavdelning (HBV) model (Aghakouchak
& Habib, 2010; Beck et al., 2020; Bergstr¨om, 1976; 1992; Seibert & Vis, 2012), a relatively simple bucket-type conceptual
hydrologic model. HBV has state variables like snow storage, soil water, and subsurface storage, and can simulate flux
variables such as evapotranspiration (ET), recharge, surface runoff, shallow subsurface flow, and groundwater flow. We used
an updated modern version, HBV1.1 (Song et al., 2025), which includes modifications such as increased parallel storage
components to represent heterogeneity within basins and dynamic parameterization capabilities.
The hybrid model employs a differentiable parameter learning (dPL) framework where neural networks generate parameters
for HBV1.1, and errors are backpropagated through the entire system. A machine learning network takes basin attributes
and meteorological forcings as inputs and outputs HBV parameters—both static (e.g., recession coefficients) and dynamic
parameters that vary daily. Because HBV1.1 supports automatic differentiation, it serves as the physical backbone: during
training, loss is calculated between simulated and observed streamflow, gradients are backpropagated through HBV equations,
and neural network weights are updated. This differs from traditional calibration because parameters are learned regionally
across all basins simultaneously rather than individually, allowing the network to capture generalizable relationships between
basin characteristics and optimal parameters while maintaining mass balance constraints. The system uses 16 parallel
response units for spatial heterogeneity and outputs diagnostic variables (e.g., evapotranspiration, soil moisture, baseflow)
not directly trained on, providing interpretability with competitive performance.
For physics-based configurations, we tested: (1) a baseline LSTM–HBV1.1 configuration as a standard reference, (2)
StefaLand HBV1.1 with resConn, which combines the physics-based approach with our residual connection architecture, and
(3) StefaLand HBV1.1 without resConn. These physics-based approaches incorporate hydrological process understanding
while maintaining the ability to learn from data..
Table 9. CAMELS Streamflow PUB and PUR Results (Physics-Based Models)
Model
Random holdout (ungauged basins)
Regional holdout (ungauged regions)
RMSE ↓
µbRMSE ↓
Corr ↑
NSE ↑
RMSE ↓
µbRMSE ↓
Corr ↑
NSE ↑
LSTM - HBV1.1
1.325
1.298
0.857
0.672
1.561
1.521
0.746
0.578
StefaLand - resConn HBV1.1
1.234
1.216
0.863
0.714
1.345
1.332
0.842
0.643
StefaLand - no resConn HBV1.1
1.315
1.302
0.848
0.707
1.401
1.379
0.835
0.623
StefaLand Ablation - resConn HBV1.1
1.310
1.306
0.842
0.693
1.465
1.432
0.607
0.512
B.2. Linear Regression baselines
To justify the use of complex neural networks over traditional methods, we have conducted baseline comparisons using
linear regression models. As shown in the table below, linear regression performs poorly across all tasks by a fair margin
when compared to our neural network approaches.
Table 10. Additional experiments with linear regression baselines.
Experiment
Random holdout
Regional holdout
RMSE ↓
µbRMSE ↓
Corr ↑
RMSE ↓
µbRMSE ↓
Corr ↑
Camels Streamflow Linear Regression
2.190
2.180
0.500
2.260
2.250
0.500
Caravan Streamflow Linear Regression
2.612
2.431
0.142
–
–
–
Soil Moisture Linear Regression
0.120
0.101
0.188
0.121
0.103
0.187
17

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
B.3. External Foundation Model Comparisons
For completeness, we explored several existing foundation models developed for Earth observation and atmospheric
applications, including TerraMind, PrithviWxC, and Galileo (Jakubik et al., 2025; Hsu et al., 2024; Tseng et al., 2025). All
models were evaluated using consistent downstream protocols, with pretrained encoders either frozen or minimally adapted
and paired with task-specific heads comparable to those used for StefaLand. These experiments were intended to probe the
extent to which representations learned from large-scale EO or atmospheric data transfer to land–surface and hydrologic
prediction tasks.
These experiments are not intended as exhaustive benchmarks or as performance upper bounds for the evaluated models, but
rather as feasibility probes to understand whether their pretrained representations can be directly repurposed for land–surface
and geohazard tasks under lightweight adaptation
Because these models differ substantially in their native input formats and pretraining objectives, task-specific adaptations
were required. TerraMind and PrithviWxC were coupled with the same residual adaptation architecture used for StefaLand,
with only the added adaptation units trained. Due to the intensive data and storage requirements of PrithviWxC, inputs were
restricted to surface-level variables most directly related to land–surface interactions, together with static attributes, while
multi-level atmospheric variables were excluded. For context, StefaLand, TerraMind, and PrithviWxC were pretrained on
approximately 2, 11, and 27 terabytes of data, respectively.
Galileo was evaluated in the landslide susceptibility setting, where inputs consist of multichannel static environmental
attributes rather than multispectral time series. To accommodate this difference, we applied an input adaptation strategy that
pooled spatial features along one dimension, projected the 17 environmental channels to 12 channels via a linear layer, and
treated the remaining spatial dimension as pseudo-temporal input. We initialized Galileo using its pretrained Transformer
encoder (768-dimensional embeddings, four attention layers with 12 heads each, and a feed-forward dimension of 3072),
followed by a two-layer classification head (768→256→1) with ReLU activation and dropout (rate 0.3). The resulting
model was fine-tuned end-to-end using AdamW (learning rate 10−4, weight decay 0.01), with a batch size of 128 for 1000
epochs on the same train–test split as other landslide experiments, using gradient clipping with a maximum norm of 1.0.
Collectively, these experiments provide a broad exploratory comparison of how foundation models pretrained on EO imagery
or atmospheric data behave when adapted to land–surface and geohazard prediction tasks.
Table 11. Performance of external foundation model baselines across tasks. All models use frozen pretrained encoders with the same
residual adaptation head.
Task
Model
RMSE ↓
µbRMSE ↓
Corr ↑
CAMELS Streamflow (PUB)
TerraMind-resConn
1.332 ± 0.0410
1.301 ± 0.0375
0.777 ± 0.0071
CAMELS Streamflow (PUR)
TerraMind-resConn
1.420 ± 0.2021
1.398 ± 0.1932
0.763 ± 0.0172
Soil Moisture (Random)
TerraMind-resConn
0.083 ± 0.0021
0.062 ± 0.0007
0.694 ± 0.0289
PrithviWxC-resConn
0.081 ± 0.0019
0.060 ± 0.0004
0.703 ± 0.0390
Soil Moisture (Europe)
TerraMind-resConn
0.101
0.080
0.519
PrithviWxC-resConn
0.103
0.079
0.523
Table 12. Landslide susceptibility prediction using the Galileo foundation model compared with published and proposed baselines on the
Oregon SLIDO dataset.
Model (10m)
Accuracy ↑
Precision ↑
Recall ↑
F1 ↑
ROC AUC ↑
Logistic Regression 2D
0.744
0.720
0.795
0.756
0.823
Random Forest 2D
0.765
0.737
0.822
0.777
0.849
CNN2D
0.880
0.896
0.858
0.877
0.854
Galileo + CNN2D
0.750
0.764
0.720
0.742
0.834
StefaLand + CNN2D
0.903
0.859
0.963
0.908
0.911
18

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
B.4. Ablations
Table 13. StefaLand ablations on CAMELS streamflow under random (PUB) and regional (PUR) spatial holdout.
Variant
PUB: random holdout (ungauged basins)
PUR: regional holdout (ungauged regions)
RMSE ↓
ubRMSE ↓
Corr ↑
NSE ↑
RMSE ↓
ubRMSE ↓
Corr ↑
NSE ↑
StefaLand direct
1.882 ± 0.0901
1.849 ± 0.0691
0.538 ± 0.0105
0.395 ± 0.1431
1.982 ± 0.4012
1.949 ± 0.3871
0.230 ± 0.0784
0.201 ± 1.2201
StefaLand scratch
1.355 ± 0.0394
1.332 ± 0.0368
0.801 ± 0.0031
0.661 ± 0.0372
1.516 ± 0.3723
1.378 ± 0.3496
0.771 ± 0.0211
0.560 ± 0.3120
StefaLand noResConn
1.171 ± 0.0325
1.154 ± 0.0319
0.823 ± 0.0022
0.706 ± 0.3260
1.376 ± 0.1987
1.356 ± 0.1712
0.798 ± 0.0195
0.610 ± 0.1345
StefaLand linear
1.452 ± 0.0542
1.366 ± 0.0533
0.751 ± 0.0127
0.661 ± 0.0430
1.484 ± 0.2588
1.453 ± 0.2402
0.672 ± 0.0391
0.542 ± 0.3100
StefaLand resConn
1.111 ± 0.0378
1.068 ± 0.0374
0.869 ± 0.0067
0.717 ± 0.1600
1.344 ± 0.2097
1.334 ± 0.1873
0.801 ± 0.0220
0.635 ± 0.2460
Table 14. StefaLand ablation study on soil moisture prediction under random and regional holdout.
Variant
Random location holdout
Regional holdout (Europe)
RMSE ↓
ubRMSE ↓
Corr ↑
RMSE ↓
ubRMSE ↓
Corr ↑
StefaLand direct
0.140 ± 0.0431
0.103 ± 0.0041
0.637 ± 0.0352
0.135
0.112
0.503
StefaLand scratch
0.074 ± 0.0011
0.058 ± 0.0003
0.749 ± 0.0172
0.108
0.064
0.528
StefaLand noResConn
0.075 ± 0.0009
0.057 ± 0.0001
0.741 ± 0.0201
0.095
0.058
0.545
StefaLand linear
0.084 ± 0.0010
0.061 ± 0.0002
0.720 ± 0.0192
0.100
0.063
0.393
StefaLand resConn (proposed)
0.068 ± 0.0013
0.054 ± 0.0004
0.783 ± 0.0054
0.090
0.059
0.638
Figure 3. Adapter ablation on streamflow random spatial splits (PUB). Boxplots summarize per-basin performance distributions for five
adapter designs (Feedforward, Bottleneck, MoE, Gated, Residual). We report RMSE (lower is better), correlation (higher is better), and
NSE (higher is better) across held-out basins, showing that the Residual adapter yields the most consistent gains, particularly in Corr and
NSE.
19

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
C. Experimental Details
C.1. Model Configurations and Hyperparameters
Table 15. StefaLand pretraining configuration.
Parameter
Value
General Settings
Task
pretrain
Model
Stefaland dec LSTM
Random seed
111
Time Period
1980/1/1–2018/12/31
Sequence Configuration
Sequence length
365
Label length
365
Prediction length
365
Sampling stride
1
Minimum window size
30
Maximum window size
90
Model Architecture
Input dimension (enc in)
32
Decoder input (dec in)
6
Output dimension (c out)
6
Model dimension
256
Number of heads
4
Encoder layers
4
Decoder layers
2
Feed-forward dimension
512
Dropout
0.1
Activation
gelu
Training Configuration
Optimizer
AdamW
Loss criterion
MaskedNSE
Epochs
25
Batch size
256
Learning rate
0.0001
Weight decay
0.0
Patience
30
Gradient clipping
5.0
Number of workers
10
Loss Weights
Time series loss ratio
1.0
Static loss ratio
0.5
Table 16. Attribute groups used in group masking pretraining.
Group
Variables
Topography
meanelevation, meanslope
Soil
HWSD clay, HWSD sand, HWSD silt, HWSD gravel, SoilGrids1km sand, SoilGrids1km clay, SoilGrids1km silt
Geology
permeability, Porosity, glaciers, permafrost
Vegetation
NDVI, FW
Climate
aridity, meanP, ETPOT Hargr, meanTa, seasonality P, seasonality PET, snow fraction, snowfall fraction
20

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Table 17. CAMELS streamflow HBV model hyperparameters.
Parameter
Value
General Settings
Random seed
111111
Data sampler
finetune sampler
Training Configuration
Time period
1989/10/01–2008/09/30
Optimizer
Adadelta
Batch size
64
Epochs
25
Neural Model Configuration
Sequence length
365
Hidden size
512
Dropout
0.2
Encoder layers
4
Decoder layers
2
Feed-forward dimension
512
Physical Model (HBV-1.1)
Model type
HBV 1 1p
Number of runs (nmul)
16
Warm-up period
365 days
Warm-up states
True
Dynamic dropout
0.0
Use routing
True
Dynamic parameters
parBETA, parK0, parBETAET
Near-zero threshold
1e-05
Loss Function
Type
RmseLoss
Table 18. Soil moisture model configuration.
Parameter
Value
General Settings
Mode
traintest
Random seed
111111
Data loader
onlylstmloader
Data sampler
finetuningnoHBV
Training Configuration
Time period
2015/04/01–2020/12/31
Target
soil moisture
Optimizer
Adadelta
Batch size
128
Epochs
50
Save frequency
Every 25 epochs
Neural Network Configuration
Hidden size
128
Dropout
0.3
Learning rate
1.2
Encoder layers
16
Decoder layers
12
Feed-forward dimension
512
Rho
365
Loss Function
Type
RmseLoss
21

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
C.2. Variables and Data Sources
Table 19. StefaLand pretraining variables and sources.
Variable Type
Variable Name
Source
Time Series Forcings
Precipitation, Short-wave solar radiation downwards,
Relative humidity, Maximum temperature, Mini-
mum temperature, Potential evapotranspiration
from Multi-Source Weather (MSWX) and Multi-
Source Weighted-Ensemble Precipitation (MSWEP)
(Beck et al., 2022; 2019)
Static Attributes
Forest cover fraction, grassland cover fraction
Climate Change Initiative (CCI) land cover dataset
(ESA, 2017)
Normalized Difference Vegetation Index (NDVI)
Terra Moderate Resolution Imaging Spectroradiome-
ter (MODIS) Vegetation Indices (MOD13A3) (Di-
dan, 2015a)
Sand, silt, clay fractions
Harmonized World Soil Database (HWSD) (FAO
et al., 2012)
Elevation, slope, aspect
Global Multi-resolution Terrain Elevation Data
(GMTED) (Danielson & Gesch, 2011; Ramcharan
et al., 2018)
Soil depth
Global 1-km Gridded Thickness of Soil, Regolith,
and Sedimentary Deposit Layers (Pelletier et al.,
2016)
Carbonate sedimentary rock fraction
Global Lithological Map (GLiM) (Hartmann &
Moosdorf, 2012)
Rock porosity, permeability
GLobal HYdrogeology MaPS (GLHYMPS) (Glee-
son et al., 2014)
Population density
Gridded Population of the World (GPW) v4 dataset
(CIESIN, 2016)
GDP per capita; population density
Gross Domestic Product and Human Development
Index over 1990-2015 (Kummu et al., 2018)
Forest intact fraction
Intact Forest Landscapes Data (Potapov et al., 2017)
Outputs
None (self-supervised pretraining)
—
Table 20. CAMELS streamflow variables and sources.
Variable Type
Variable Name
Source
Time Series Forcings
Precipitation, Temperature, Potential evapotranspira-
tion, Solar radiation, Vapor pressure
Catchment Attributes and Meteorology for Large-
sample Studies (CAMELS) (Addor et al., 2017; New-
man et al., 2014)
Static Attributes
Elevation, slope, catchment area, forest cover, LAI,
GVF, soil depth, porosity, conductivity, sand, silt,
clay fractions, carbonate fraction, permeability, arid-
ity, snow fraction, precipitation extremes
CAMELS
Outputs
Streamflow
CAMELS gauge records
22

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Table 21. Soil moisture variables and sources.
Variable Type
Variable Name
Source
Time Series Forcings
Albedo (BSA, WSA)
Moderate Resolution Imaging Spectroradiometer
(MODIS) MCD43A3 version 6 (Schaaf, Crystal &
Wang, Zhuosen, 2021)
LST (Day, Night)
MODIS Land Surface Temperature/Emissivity Daily
(MYD11A1) Version 6.1 (Wan et al., 2021)
Precipitation
Global Precipitation Measurement (GPM), MSWEP,
and ERA5 precipitation (Huffman et al., 2019; Beck
et al., 2019; Mu˜noz Sabater, 2019)
Forecast albedo, LAI (high/low vegetation), soil tem-
perature (layer 1), surface pressure, solar radiation,
2 m temperature, evaporation, precipitation, U/V
wind (10 m)
ECMWF Reanalysis v5 (ERA5) (Mu˜noz Sabater,
2019)
Static Attributes
elevation, slope, aspect, roughness, curvature
Global 1/5/10/100-km topography derivatives (Am-
atulli et al., 2018)
Sand, clay, silt, bulk density
HWSD v1.2 (FAO et al., 2012)
Land cover; urban; open water; snow/ice
ESA CCI Land Cover (ESA, 2017)
NDVI
Vegetation Indices Monthly L3 Global 0.05Deg
CMG (Didan et al., 2015)
Outputs
Soil moisture
International
Soil
Moisture
Network
(ISMN)
(Dorigo et al., 2013b; 2011)
Table 22. Streamflow input variables and attributes used from the Caravan dataset.
Variable Type
Variable Name
Source
Time Series Forcings
Precipitation (P), Air temperature (Ta), Potential
evapotranspiration (PET)
ERA5-Land via Caravan (Kratzert et al., 2023;
Mu˜noz-Sabater et al., 2021)
Surface pressure, 10 m wind components (u, v)
ERA5-Land via Caravan (Kratzert et al., 2023;
Mu˜noz-Sabater et al., 2021)
Net solar radiation, net thermal radiation
ERA5-Land via Caravan (Kratzert et al., 2023;
Mu˜noz-Sabater et al., 2021)
Snow water equivalent, soil moisture (4 layers)
ERA5-Land via Caravan (Kratzert et al., 2023;
Mu˜noz-Sabater et al., 2021)
Static Basin Attributes
Latitude, longitude, catchment area
Caravan metadata (Kratzert et al., 2023)
Aridity indices (ERA5-Land,
FAO Penman–
Monteith)
Caravan derived attributes (Kratzert et al., 2023)
Mean precipitation, precipitation seasonality
Caravan derived attributes (Kratzert et al., 2023)
Mean air temperature, PET seasonality
Caravan derived attributes (Kratzert et al., 2023)
Elevation, slope
Global terrain products via Caravan (Kratzert et al.,
2023)
Soil texture fractions (sand, silt, clay)
Harmonized World Soil Database (HWSD) via Car-
avan (FAO et al., 2012; Kratzert et al., 2023)
Soil erosion index
Global soil datasets via Caravan (Kratzert et al.,
2023)
Forest cover fraction
Global land cover products via Caravan (Kratzert
et al., 2023)
Outputs
Streamflow
Gauge observations compiled in Caravan (Kratzert
et al., 2023)
23

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Table 23. Landslide (SLIDO, Oregon) variables and sources.
Variable Type
Variable Name
Source
Input data
Elevation
National Elevation Dataset (NED) (Gesch et al., 2018)
Soil sand, silt, clay, bulk density, saturated hydraulic
conductivity
Probabilistic Remapping of SSURGO (POLARIS)
(Chaney et al., 2019)
Lithology
Global Lithological Map (GLiM) (Hartmann & Moos-
dorf, 2012)
Rainfall
PRISM (PRISM Climate Group, 2014)
NDVI
Moderate
Resolution
Imaging
Spectroradiometer
(MODIS) Vegetation Indices Monthly L3 (Didan, 2015b)
Landcover
National Land Cover Database (NLCD) 2016 (Dewitz,
2019)
Soil moisture
SMAP-HydroBlocks (SMAP-HB) (Vergopolan et al.,
2021)
slope, aspect, curvature, TWI, SPI
DEM-derived
Outputs
Landslide occurrence (binary)
Statewide Landslide Information Database for Oregon
(SLIDO) (Franczyk, J. J et al., 2020)
Table 24. Soil composition (ISRIC) variables and sources.
Variable Type
Variable Name
Source
Time Series Forcings
Same as Table 21
—
Static Attributes
Same as Table 21
—
Outputs
Soil property (clay; sand; silt)
World Soil Information Service (WoSIS) (Batjes
et al., 2020)
24

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Figure 4. Spatial distribution of the global streamflow dataset. Basins are categorized according to the availability of runoff observations:
basins with relatively abundant runoff records (blue), basins with sparse runoff records (orange), and basins without runoff data (green).
Marker size corresponds to basin area, classified into three categories based on the 33rd and 67th percentiles of catchment areas.
C.3. Computational Resources
Table 25. Computation Resources for StefaLand and Comparison Models
Model
Seconds/Epoch
#GPUs
GPU Type
Memory
StefaLand (Pretraining)
16,000
6
NVIDIA V100
240 GB
StefaLand ResConn
30
2
NVIDIA V100
80 GB
StefaLand no Adapter
26
2
NVIDIA V100
80 GB
LSTM Baseline
12
2
NVIDIA V100
80 GB
LSTM-HBV1.1
280
2
NVIDIA V100
80 GB
StefaLand-resConn HBV1.1
320
2
NVIDIA V100
80 GB
StefaLand-no Adapter HBV1.1
300
2
NVIDIA V100
80 GB
Note: All values except pretraining are for the CAMELS benchmark experiment. Relative computational differences are consistent across
other experiments.
C.4. Pretraining Data Handling
A global dataset was constructed for model pretraining, including 8,634 catchments and designed to characterize climatic,
ecological, soil, topographic, geological, and socioeconomic conditions. The dataset includes both daily meteorological
forcings and long-term averaged static attributes. Daily meteorological variables comprise precipitation, downward
shortwave radiation, relative humidity, maximum temperature, and minimum temperature, derived from the Multi-Source
Weather (MSWX) and Multi-Source Weighted-Ensemble Precipitation (MSWEP) datasets at a spatial resolution of 0.1°
(Beck et al., 2022; 2019). Potential evapotranspiration was estimated using the Hargreaves method.
The study catchments are divided into three groups: 3,434 GRDC catchments with relatively abundant historical runoff
records, 3,248 GRDC catchments with sparse runoff records, and 1,952 HydroBasins level-8 catchments without runoff
observations (GRDC, 2024; Lehner & Grill, 2013). Ecosystem states are represented by forest and grassland cover fractions
derived from the Climate Change Initiative (CCI) land cover dataset (ESA, 2017), along with the Normalized Difference
Vegetation Index (NDVI) from MODIS (Didan, 2015a). Soil properties include sand, silt, and clay fractions from the
Harmonized World Soil Database (HWSD) (FAO et al., 2012).
25

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
Topographic attributes include elevation, slope, and aspect obtained from the Global Multi-resolution Terrain Elevation Data
(GMTED) (Danielson & Gesch, 2011; Ramcharan et al., 2018), as well as terrain-derived soil depth from the Global 1-km
Gridded Thickness of Soil, Regolith, and Sedimentary Deposit Layers dataset (Pelletier et al., 2016). Geological attributes
comprise carbonate sedimentary rock fractions from the Global Lithological Map (GLiM) (Hartmann & Moosdorf, 2012)
and rock porosity and permeability from the GLobal HYdrogeology MaPS (GLHYMPS) dataset (Gleeson et al., 2014).
Socioeconomic conditions are characterized using population density from the Gridded Population of the World (GPW) v4
dataset (CIESIN, 2016), gross domestic product and population data from the gridded global GDP and Human Development
Index datasets (Kummu et al., 2018), and forest intactness from the Intact Forest Landscapes dataset (Potapov et al., 2017).
All static attributes were mapped to a common 0.01° grid prior to basin-scale aggregation to ensure spatial consistency
across data sources and improve spatial averaging over irregular basin geometries. A complete list of variables is provided
in Table 19.
C.5. Dataset Splitting
For the WoSIS soil dataset, we collected soil property data from 106,503 locations. After removing low-quality records
(e.g., sand values greater than 1 or negative values), we randomly sampled 5,000 soil points to reduce computational cost.
We then applied 5-fold cross-validation (k=5) on this subset.
For the landslide dataset at 30 m resolution, we used 14,604 historical landslide points. We split the dataset into 70% for
training, 20% for validation, and 10% for testing.
26

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
D. Additional Figures
Figure 5. Fine-tuning pipeline used in our downstream experiments. Static attributes and meteorological forcings are encoded by the
pretrained StefaLand encoder (frozen), then passed through a task adapter and sequence model (LSTM), followed by projection layers to
generate predictions optimized with a task loss against ground truth.
Figure 6. Adapter architectures evaluated in our experiments. We compare a gated adapter, a bottleneck adapter with compression
and expansion stages, A mixture of Experts and a basic feedforeward and a residual adapter that injects pretrained features via a skip
connection.
27

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
E. Metric Calculations
This appendix details the calculation of the evaluation metrics used in our experiments. All metrics presented in the main
paper tables are the median values across test basins or stations, as computed using the following formulations.
E.1. Primary Evaluation Metrics
E.1.1. ROOT MEAN SQUARE ERROR (RMSE)
RMSE measures the average magnitude of prediction errors. Lower values indicate better performance.
RMSE =
v
u
u
t 1
n
n
X
i=1
(ypred,i −ytarget,i)2
(17)
E.1.2. UNBIASED ROOT MEAN SQUARE ERROR (µBRMSE)
µbRMSE removes the bias component from the error calculation, focusing on the error’s random component. It is calculated
by first computing anomalies from the mean for both predictions and targets.
y′
pred,i = ypred,i −ypred
(18)
y′
target,i = ytarget,i −ytarget
(19)
µbRMSE =
v
u
u
t 1
n
n
X
i=1
(y′
pred,i −y′
target,i)2
(20)
E.1.3. CORRELATION (CORR)
Correlation quantifies the linear relationship between predictions and targets. Values range from -1 to 1, with 1 indicating
perfect positive correlation.
Corr =
Pn
i=1(ypred,i −ypred)(ytarget,i −ytarget)
qPn
i=1(ypred,i −ypred)2 Pn
i=1(ytarget,i −ytarget)2
(21)
This is calculated using Pearson’s correlation coefficient between predicted and observed values.
E.2. Secondary Metrics
The following metrics are used in our comprehensive evaluation but may not appear directly in the main tables.
E.2.1. NASH-SUTCLIFFE EFFICIENCY (NSE) / R2
NSE evaluates the predictive skill relative to using the mean of observations as a predictor. Values range from −∞to 1,
with 1 indicating perfect prediction.
NSE = 1 −
Pn
i=1(ytarget,i −ypred,i)2
Pn
i=1(ytarget,i −ytarget)2
(22)
E.2.2. MEAN ABSOLUTE ERROR (MAE)
MAE measures the average absolute difference between predictions and targets.
MAE = 1
n
n
X
i=1
|ypred,i −ytarget,i|
(23)
28

StefaLand: Efficient Geoscience Representation Learning Model for Dynamic Land-Surface Prediction
E.2.3. FLOW DURATION CURVE RMSE (RMSE FDC)
RMSE FDC evaluates errors in the statistical distribution of flows rather than in their timing.
RMSE FDC =
v
u
u
t 1
100
100
X
j=1
(FDCpred,j −FDCtarget,j)2
(24)
where FDCj represents the j-th percentile of the sorted flow values.
E.2.4. FLOW BIASES
Several flow-specific biases were computed to evaluate performance across different flow regimes:
• FLV (Low Flow Volume Bias): Percent bias in the lowest 30% of flows
• FHV (High Flow Volume Bias): Percent bias in the highest 2% of flows
• PBIAS (Percent Bias): Overall percent bias across all flows
The general form for these biases is:
PBIASregime =
P(ypred,regime −ytarget,regime)
P ytarget,regime
× 100%
(25)
E.2.5. KLING-GUPTA EFFICIENCY (KGE)
KGE combines correlation, bias, and variability components:
KGE = 1 −
s
(r −1)2 +
 σpred
σtarget
−1
2
+
 µpred
µtarget
−1
2
(26)
where r is the correlation coefficient, σ represents standard deviation, and µ represents the mean.
E.3. Metric Aggregation
For each evaluation scenario (Random Holdout and Regional Holdout), metrics were calculated for each individual basin or
station and then aggregated using median values to provide a robust measure of central tendency less sensitive to outliers.
All metrics shown in tables throughout the paper represent these median values across the test set.
E.4. Implementation Details
All metrics were implemented in Python using NumPy for numerical computations and SciPy’s statistical functions for
correlation coefficients. Special care was taken to handle missing values (NaNs) appropriately in all calculations. For time
series with missing values, only timestamps where both predicted and target values were available were used in metric
calculations.
29
