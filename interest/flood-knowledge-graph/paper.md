---
title: 'From social media to flood 3D scenes: leveraging large language models and
  knowledge graphs for floo'
authors: ''
year: '2026'
venue: ''
---

International Journal of Geographical Information
Science
ISSN: 1365-8816 (Print) 1362-3087 (Online) Journal homepage: www.tandfonline.com/journals/tgis20
From social media to ﬂood 3D scenes: leveraging
large language models and knowledge graphs for
ﬂood spatiotemporal evolution representation
Qingqing Ran , Weilian Li , Juan Liu , Huiqin Li , Pei Dang , Jun Zhu , Qing Zhu
& Youness Dehbi
To cite this article: Qingqing Ran , Weilian Li , Juan Liu , Huiqin Li , Pei Dang , Jun Zhu ,
Qing Zhu & Youness Dehbi (03 Nov 2026): From social media to ﬂood 3D scenes:
leveraging large language models and knowledge graphs for ﬂood spatiotemporal
evolution representation, International Journal of Geographical Information Science, DOI:
10.1080/13658816.2026.2749047
To link to this article:  https://doi.org/10.1080/13658816.2026.2749047
Published online: 03 Nov 2026.
Submit your article to this journal 
View related articles 
View Crossmark data
Full Terms & Conditions of access and use can be found at
https://www.tandfonline.com/action/journalInformation?journalCode=tgis20

RESEARCH ARTICLE                                                                   
From social media to flood 3D scenes: leveraging large 
language models and knowledge graphs for flood 
spatiotemporal evolution representation
Qingqing Rana, Weilian Lia, Juan Liua, Huiqin Lia, Pei Danga, Jun Zhua,  
Qing Zhua and Youness Dehbib 
aFaculty of Geosciences and Engineering, Southwest Jiaotong University, Chengdu, China; 
bComputational Methods Lab, HafenCity University Hamburg, Hamburg, Germany 
ABSTRACT 
Flood disaster evolution exhibits strong spatiotemporal coupling 
and complex causality. Intuitive representations of flood disaster 
evolution can help the public better understand disaster proc­
esses and their underlying evolution mechanisms, thereby 
enhancing risk awareness. However, most existing studies focus 
on numerical modeling of flood disaster evolution, which has lim­
ited capability in effectively capturing and representing the evolv­
ing processes of flood disasters. Social media posts generated 
during floods contain rich information and provide valuable 
insights into the evolution of flood events. In this context, this 
study leverages large language models (LLMs) and knowledge 
graphs (KGs) to extract flood spatiotemporal knowledge from 
social media, thereby reconstructing the disaster evolution path­
way for representation as 3D scenes. Specifically, ontology-con­
strained LLMs for flood knowledge extraction, evolutionary 
pathway reconstruction and 3D representation are introduced in 
detail. We collected a total of 34,731 tweets related to the 2021 
European floods for experimental analysis and developed a proto­
type system for 3D flood representation. The experimental results 
demonstrate that the proposed method achieves reliable perform­
ance in disaster knowledge extraction and evolutionary pathway 
reconstruction. Moreover, the augmented 3D representation 
improves the interpretability and clarity of flood disaster evolu­
tion, thereby facilitating a better understanding of disaster proc­
esses and supporting disaster prevention and mitigation.
ARTICLE HISTORY 
Received 5 February 2026 
Accepted 10 October 2026 
KEYWORDS 
Flood spatiotemporal 
evolution; social media; 
knowledge graphs; 
large language models; 
3D representation   
1. Introduction
Flood disasters, characterized by sudden onset, wide spatial extent and severe 
impacts, pose persistent threats to global societal safety and sustainable development. 
The United Nations Office for Disaster Risk Reduction (UNDRR1) reports that floods are 
the most frequent and widely affecting natural disasters worldwide (UNDRR 2020). 
According to the report of the European Environment Agency (EEA), floods accounted 
CONTACT Weilian Li 
vgewilliam@my.swjtu.edu.cn 
ß 2026 Informa UK Limited, trading as Taylor & Francis Group
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE 
https://doi.org/10.1080/13658816.2026.2749047

for more than 40% of the economic losses caused by weather and climate-related 
extreme events in Europe between 1980 and 2022. Particularly, the extreme floods of 
July 2021 caused widespread damage in Germany, Belgium, the Netherlands and 
neighboring countries, ranking among the most severe basin-scale flood disasters in 
Europe in recent decades (European Environment Agency 2023). Under ongoing cli­
mate change, the increasing occurrence of extreme rainfall has further intensified the 
uncertainty and complexity of flood risk (Mantovani et al. 2024). Enhancing flood resili­
ence through modern information technologies has therefore become a critical priority 
for global disaster risk reduction (Peng et al. 2022).
Understanding flood disaster evolution is essential for leveraging information tech­
nologies to support disaster prevention and mitigation (Saunders et al. 2025). Flood 
disasters are inherently dynamic processes characterized by strong spatiotemporal 
coupling and interactions among multiple events. Their evolution can be described as 
a sequence of interconnected stages involving onset, propagation, emergency 
response and secondary impacts (Zhu et al. 2022). Therefore, accurate characterization 
of flood spatiotemporal evolution and key events provides a scientific basis for flood 
prevention and management (Gao et al. 2025, Chen et al. 2026). However, most exist­
ing studies rely on hydrodynamic models to simulate flood processes and integrate 
the results into GIS platforms for visualization (Kumar et al. 2023). Although these 
approaches can describe physical processes in detail, they have limited ability to 
coherently represent semantic relationships and event evolution structures, which con­
strains a comprehensive understanding of flood spatiotemporal evolution (Hofmeister 
et al. 2024).
Within networked information environments represented by social media, large vol­
umes of user-generated data provide new insights to characterize the evolution of 
flood disasters. Compared with traditional monitoring methods, social media data offer 
high timeliness, broad coverage and strong public participation. During flood events, 
large numbers of users continuously publish disaster textual information. Although 
individual posts generally reflect only local phenomena or personal perceptions, the 
continuous accumulation of such fragmented information across temporal and spatial 
dimensions can support the identification of relationships among disaster events and 
the reconstruction of disaster evolution processes (Karmegam et al. 2021, Li et al. 
2023). However, this information is typically scattered across large volumes of text in a 
fragmented and unstructured form, and therefore cannot be readily used to support 
systematic analysis or an integrated representation of flood disaster evolution 
(Phengsuwan et al. 2021). This limitation highlights the need for methods that can 
effectively organize and semantically connect dispersed disaster-related information 
from social media.
Knowledge graphs (KGs) are widely used to organize and represent complex enti­
ties, events, and their relationships, providing an effective means to structure and 
associate large volumes of disaster information (Kejriwal 2022, Peng et al. 2023). In 
recent years, a new generation of large language models (LLMs), represented by 
ChatGPT, Gemini, DeepSeek and Qwen, has demonstrated strong capabilities in natural 
language understanding, contextual modeling and complex reasoning. These capabil­
ities provide new opportunities for automatically extracting disaster entities, relations 
2
Q. RAN ET AL.

and events from unstructured social media texts (Xue et al. 2023, Dang et al. 2025, Xu 
et al. 2025). Therefore, integrating LLMs with KGs can enable the structured organiza­
tion of disaster knowledge from fragmented social media information and further 
support relational analysis and reconstruction of flood disaster evolution. However, 
node- and relation-centered graph representations alone remain insufficient to support 
intuitive public understanding of flood disaster evolution (Zajac et al. 2025). 
Geovisualization is widely recognized as an effective approach for understanding the 
evolution of complex geographic phenomena. Through spatial mapping and dynamic 
representation, abstract semantic logic can be transformed into perceptible spatiotem­
poral evolution processes (Guo et al. 2005, Lin et al. 2020, Bae and Dodge 2023).
In this context, this study leverages LLMs and KGs to extract flood spatiotemporal 
knowledge from social media, reconstruct the flood disaster evolution pathway, and 
present it in the form of 3D scenes. The study workflow is shown in Figure 1. This 
method exploits the semantic understanding and reasoning capabilities of LLMs to 
extract entities and relationships from large volumes of flood tweets, thereby con­
structing a flood KG. Based on this graph, the evolution pathway of flood is recon­
structed under spatiotemporal and semantic constraints, and the corresponding 
entities and relationships are instantiated to generate 3D flood scenes, which in turn 
enhance public understanding of the development of floods. The main contributions 
of this study are summarized as follows.
Figure 1. Overall framework for flood spatiotemporal evolution representation from social media. 
The framework integrates multimodal data, ontology-constrained flood knowledge extraction, flood 
spatiotemporal evolution pathway reconstruction, 3D flood representation and validation–optimiza­
tion feedback. Social media data are used to construct an evidence-grounded flood knowledge 
graph through few-shot CoT prompting and FO constraints. Based on the graph, spatiotemporal 
and semantic constraints, ontology-guided event importance evaluation, and spatiotemporal com­
pletion are applied to reconstruct flood evolution pathway, which is further mapped into dynamic 
3D geographic scenes.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
3

1.1. A geographic scene knowledge-constrained LLM approach for flood 
knowledge extraction and spatiotemporal evolution pathway reconstruction
Taking flood tweets as the basis, this study follows the concept of the six elements of 
geographic scenes, namely time, place, character, object, event and phenomenon, 
which are modeled as an ontology and injected into LLMs as prior knowledge to con­
strain hallucinations. By adopting different prompting strategies, including zero-shot 
prompting, few-shot Chain-of-Thought (CoT) prompting and few-shot CoT prompting 
with Flood Ontology (FO) constraints, the proposed approach improves the quality of 
structured flood knowledge extraction. Furthermore, the extracted knowledge is used 
to reconstruct the spatiotemporal evolution pathway of flood disaster under temporal, 
spatial and semantic constraints, which serve as the storyline for subsequent 3D 
dynamic representation of flood disaster evolution.
1.2. A knowledge-guided 3D dynamic representation method for flood 
spatiotemporal evolution
Following the above-mentioned spatiotemporal evolution pathway, this study further 
maps flood event nodes and relations into 3D geographic scenes from a geospatial 
storytelling perspective that integrates the syntax–semantics–pragmatics framework, 
enabling a full-process representation from social media information to 3D flood 
scenes. The proposed method intuitively presents the occurrence, development, 
impacts and evolutionary logic of flood disasters, thereby enhancing the interpretabil­
ity of flood disaster evolution, improving the effectiveness of flood information dis­
semination, and potentially strengthening public flood risk awareness.
The remainder of this article is organized as follows. Section 2 reviews related work. 
Section 3 presents the methodology. Section 4 describes the experiments and results. 
Section 5 discusses the findings, limitations and future directions. Section 6 concludes 
the article.
2. Related work
Social media has become an important data source for flood disaster perception and 
analysis. Existing studies have used platforms such as Twitter for disaster topic identifi­
cation and public sentiment analysis during flood events (Bryan-Smith et al. 2023, 
Li et al. 2023). Topic modeling and feature extraction methods have also been applied 
to monitor disaster impacts from social media streams (Mihunov et al. 2022). Beyond 
textual semantic analysis, Twitter information has been used for rapid flood mapping 
and for analyzing disaster resilience and public responses (Li et al. 2018, Zou et al. 
2018). Furthermore, event modeling of social media data has been employed to 
describe flood development from prewarning through emergency response to post- 
disaster recovery (Liu et al. 2022). These studies demonstrate that social media data 
can not only reflect local disaster conditions and public perceptions but also provide 
valuable support for analyzing flood disaster evolution. However, conventional topic 
models, feature engineering approaches and event modeling methods often rely on 
predefined rules or task-specific models, limiting their ability to adequately handle 
4
Q. RAN ET AL.

noisy expressions, abbreviations, non-standard place names, missing context and 
implicit semantic relationships in social media texts (Wang et al. 2020, Chen and Lim 
2021).
With the development of GeoAI, LLMs have increasingly been applied to geo­
graphic text understanding and disaster knowledge acquisition (Hu et al. 2023, Yang 
et al. 2026, Zhao et al. 2026). Compared with traditional rule matching methods (Li 
et al. 2022a), LLMs provide stronger contextual modeling and semantic understanding 
capabilities, making them better suited to handling noisy expressions, abbreviations, 
non-standard place names and missing context in social media texts. Nevertheless, 
existing GeoAI studies involving LLMs have primarily focused on entity recognition, 
semantic question answering or local relation extraction, with limited capacity to 
organize disaster events distributed across different times and locations into coherent 
evolution processes (Wang et al. 2024, Li et al. 2025). Moreover, without explicit geo­
graphic semantic constraints, LLMs may still generate semantically inconsistent or 
unreliable knowledge in complex disaster scenarios, thereby reducing the reliability of 
disaster knowledge modeling (Ji et al. 2025).
To strengthen the structured organization and semantic association of disaster 
knowledge, some studies have further integrated LLMs with KGs, using structured 
semantic constraints to improve knowledge organization and semantic consistency 
(Zhu et al. 2024). However, existing KG construction methods primarily adopt static 
entity–relation modeling and provide insufficient support for systematically represent­
ing the temporal sequence, spatial associations and dynamic evolution of disaster 
events (Zheng et al. 2022, Zhao et al. 2023). Many existing methods also rely on expert 
defined ontology structures and rule systems, which limits their adaptability when 
processing fragmented and continuously changing disaster information from social 
media (van Cauter and Yakovets 2024). Consequently, these methods still struggle to 
organize event information dispersed across different times and locations into coher­
ent evolution sequences. Therefore, effectively integrating fragmented social media 
information and reconstructing the spatiotemporal evolution pathway of flood disas­
ters while maintaining the semantic consistency and reliability of disaster knowledge 
remains an important research challenge.
3. Methodology
3.1. Knowledge-constrained LLMs for flood knowledge extraction
In this section, we present an LLM-based approach for extracting disaster-related enti­
ties and relationships. A FO integrated with geographic scene semantics is employed 
to constrain the extraction process and enhance the reliability of flood knowledge 
extraction.
3.1.1. Ontology modeling integrating geographic scene knowledge
To capture the spatiotemporal evolution of flood disasters and the coupling of mul­
tiple factors, this study constructs a Flood Scene Schema (FSS) centered on the Scene 
Unit. Based on geographic scene knowledge, the schema integrates six categories of 
semantic elements, including character, event, object, location, time and phenomenon, 
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
5

into a unified structured space (L€u et al. 2022). It further characterizes complex flood 
scenes across six dimensions, including spatial location, geometric form, attribute 
properties, semantic description, inter-element relationships and evolutionary proc­
esses. The FSS jointly represents the spatial distribution, temporal progression and 
semantic associations among flood events, providing a spatially consistent and process 
interpretable knowledge framework. Its semantic structure is abstracted into two lev­
els, namely entity and relation, as shown in Table 1.
Based on the FSS, a FO model is developed. The modeling process follows the prin­
ciples specified in ISO/IEC 21838-1:2021, Top-level ontologies (TLO) – Part 1: 
Requirements, which provide general requirements for the design of top-level ontolo­
gies (International Organization for Standardization 2021). Classical ontology engineer­
ing methodologies are adopted to guide the modeling process (Gr€uninger and Fox 
1995, Uschold and King 1995), and practical development guidelines are further 
applied to ensure interoperability, reusability and modularity (Noy and McGuinness 
2001).
Specifically, ontology construction begins with a requirement analysis to define the 
semantic scope that the ontology model should cover. To ensure that the modeling 
objectives are well targeted and verifiable, a set of competency questions is formu­
lated, which represents the key semantic questions that the ontology is expected to 
answer. On this basis, relevant concepts and relationships are derived from the attrib­
utes and relations defined in the FSS, and a structured ontology is modeled using the 
Web Ontology Language. The resulting flood ontology named FO structure can be for­
mally defined as shown in the following equation:
FO ¼ fC, R, Ag
R ¼ Rs [ Rt [ Re
AðcÞ ¼ fa1, a2, . . . , an j ai ¼ ðpi, viÞg
8
<
:
(1) 
where C denotes the set of concepts representing semantic entities in flood scenes, R 
denotes the set of semantic relations and A denotes the set of attributes. The relation 
set R includes spatial relations Rs; temporal relations Rt and event association relations 
Re; which jointly describe the spatial, temporal and semantic connections among enti­
ties and events in flood scenes. In the attribute set A, ai represents the ith attribute, pi 
denotes the attribute name and vi specifies the corresponding value domain. These 
attributes characterize semantic properties such as location, form, state and intensity.
Table 1. Semantic hierarchy of flood scene.
Level
Level description
Example
Entity layer
Define entity and event types in flood 
semantics based on six core semantic 
elements.
Entities: affected population, flood- 
inundated areas 
Events: dam breach, emergency 
response
Relation layer
Spatial relations: characterize spatial 
positions and topological relations
located in, adjacent to
Temporal relations: describe event 
chronology and persistence
before, during, after
Event association relations: describe 
semantic links among disaster events
rain !
trigger flood !
impact damage
6
Q. RAN ET AL.

3.1.2. Ontology-constrained knowledge graph construction driven by LLMs
This study introduces an ontology-constrained few-shot CoT strategy for LLM-driven 
KG construction, as shown in Figure 2. First, the extraction task is decomposed into 
ordered subtasks under the constraints of the FO. Accordingly, the original complex 
task is divided into subtasks with appropriate granularity and a clear logical order, 
including flood event identification, triggering relation extraction, and the extraction 
of affected objects and their attributes from social media data.
Next, few-shot prompting is employed with a small number of high-quality exam­
ples to help LLM recognize entity types, relations and structured output formats. CoT 
prompting is then used to guide step-by-step reasoning. The LLM first identifies and 
normalizes disaster-related entities, including events, locations and times, and gener­
ates node sets with unique identifiers. Based on these nodes, spatiotemporal and 
event relations are inferred to construct flood entity–relation triples, which are further 
linked back to the corresponding source tweets for evidence alignment. Candidate tri­
ples that lack explicit textual support are returned to the LLM for revision. This process 
Figure 2. Ontology-constrained construction of a flood knowledge graph using few-shot CoT 
knowledge extraction into a sequence of ontology-guided subtasks. Few-shot CoT prompting enfor­
ces structured reasoning over entity types, relations and attributes. Candidate knowledge units are 
iteratively validated against FO constraints and corrected when violations occur, resulting in a 
semantically consistent and ontology-compliant flood knowledge graph.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
7

ensures that evolutionary logic, temporal order and spatial associations are explicitly 
modeled during extraction, while keeping the extracted knowledge closely anchored 
to the original tweets and reducing hallucinated outputs.
Finally, candidate knowledge units are validated against the FO. In this process, 
entity types must conform to FO definitions, relation types are limited to spatial, tem­
poral and event association categories, and attribute values, including time and loca­
tion, are required to satisfy ontology constraints. If these constraints are violated, the 
corresponding candidates are returned to the LLM for correction until all subtasks 
pass ontology validation. After validation, the validated outputs are integrated to form 
a complete flood KG that supports querying and reasoning.
3.1.3. Cross-evaluation of LLMs for knowledge graph quality
The quality of flood KG extraction directly affects the reliability of subsequent evolution 
pathway reconstruction. Within the ‘LLM-as-a-Judge’ framework, this study designs an 
LLM cross-evaluation mechanism (Liu et al. 2023, Zheng et al. 2023). Evaluation is con­
ducted across three core dimensions, namely accuracy, completeness and consistency. 
Each dimension is rated on a five-point Likert scale from L1 to L5. The evaluation work­
flow is illustrated in Figure 3. The scoring criteria are provided in Table 2.
Accuracy and completeness are the primary factors determining the reliability and 
coverage of KG extraction. Therefore, these two dimensions are each assigned a 
weight of 0.4. Consistency plays a supporting role in aligning extraction results across 
different LLMs or extraction batches and is assigned a weight of 0.2. Overall score 
Stotal is calculated as a weighted sum, as defined in the following equation:
Stotal ¼ wa  Sacc þ wc  Scom þ ws  Scon
(2) 
where Sacc; Scom and Scon denote the scores for accuracy, completeness and consist­
ency, respectively. The corresponding weights wa; wc and ws are set to 0.4, 0.4 and 
0.2, respectively.
Figure 3. Cross-evaluation framework for assessing the quality of flood knowledge graphs gener­
ated by different LLMs. Knowledge graphs constructed by different LLMs are mutually evaluated 
within an LLM-as-a-Judge framework using three criteria: completeness, accuracy and consistency. 
Weighted aggregation yields overall quality scores and rankings. Friedman and Nemenyi tests are 
further applied to examine statistical significance and robustness, supporting the selection of the 
optimal LLM.
8
Q. RAN ET AL.

After scores are obtained for each dimension across all LLMs, the Friedman test is 
applied to assess overall differences among LLMs for both individual dimensions and 
the overall score. The Nemenyi post hoc test is then used to identify pairwise differen­
ces between LLMs. The corresponding formulations are provided in the following 
equations:
v2
F ¼
12
nkðk þ 1Þ
X
k
j¼1
R2
j −3nðk þ 1Þ
(3) 
CD ¼ qa
ffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffiffi
kðk þ 1Þ
6n
r
(4) 
where v2
F denotes the Friedman test statistic, n represents the number of evaluation 
instances, k is the number of compared LLMs, Rj denotes the sum of ranks for the jth 
LLM, CD denotes the critical difference, defined as the minimum average rank differ­
ence indicating a statistically significant difference in the Nemenyi post hoc test, qa 
denotes the critical value for the Nemenyi test derived from the Studentized range 
distribution at significance level a for k compared LLMs.
A statistically significant difference between two LLMs exists if the difference in 
their average ranks exceeds the critical difference. If the test reveals substantial biases 
in how LLMs evaluate the same results, the prompt design or scoring rubrics should 
be refined accordingly. Conversely, if the observed differences primarily reflect the 
inherent performance of the LLMs, the evaluation results can be regarded as reliable 
for further analysis.
Table 2. Flood knowledge graph quality assessment criteria.
Level
Dimension
Completeness
Accuracy
Consistency
L1 (5 points)
All core entities, events 
and relations are 
correctly identified, with 
complete coverage and 
no omissions.
Extracted content fully 
matches the source text 
in semantic meaning 
and factual accuracy, 
with no ambiguity.
Results remain consistent 
across semantic 
representation, 
ontology constraints 
and LLM outputs.
L2 (4 points)
Most key knowledge is 
correctly identified, with 
only minor secondary 
information missing.
Extraction accuracy is high, 
with very few minor 
deviations or synonym- 
level errors.
Results are largely 
consistent in semantics 
and format, with minor 
differences that do not 
affect understanding.
L3 (3 points)
Most major knowledge 
units are extracted, but 
some key entities or 
relations are missing.
A moderate level of 
semantic deviation or 
misidentification is 
observed.
Semantic differences 
appear across LLMs or 
extraction runs, 
requiring manual 
judgment.
L4 (2 points)
Only limited information is 
identified, with major 
content missing and 
insufficient coverage.
Misidentifications and 
factual inconsistencies 
are frequent.
Clear discrepancies occur 
across LLM outputs, 
leading to high 
semantic inconsistency.
L5 (1 point)
Extraction results are 
fragmented and contain 
little valid information 
or none.
Most extracted content 
does not align with the 
source semantics or 
contains serious errors.
Results are highly 
inconsistent and lack a 
coherent semantic 
framework.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
9

3.2. Reconstruction of main flood evolution pathway
3.2.1. Identification of main event chain in flood evolution
To identify the critical development pathway of flood disasters within the KG con­
structed in Section 3.1, multi-dimensional constraints are first integrated to generate 
candidate event chains. Subsequently, event importance is evaluated based on the 
structural characteristics of the FO. On this basis, the main event chain of flood evolu­
tion is further extracted from complex event associations, as shown in Figure 4.
First, candidate flood event chains are generated from the flood KG. Trigger-related 
phenomena or events are identified as starting nodes. From each starting node, a 
depth-first search (DFS) strategy is employed to traverse the graph, with the chains 
length incrementally expanded. Starting from node e1; a candidate event chain is 
defined as P ¼ he1, e2, . . . , eni: During traversal, chain extension from event ei to ej is 
constrained by a tri-constraint set C, including semantic, temporal and spatial con­
straints. Under constraints, resulting evolution event chain can be formally expressed 
as follows:
Figure 4. Identification of the main flood event chain from the flood knowledge graph. Trigger- 
type events are selected as starting points, and candidate chains are generated using depth-first 
search under event semantic and spatiotemporal constraints. Event importance is quantified by 
integrating ontology-based intrinsic hazard levels with cascading effects evaluated by LLMs. 
Candidate chains are ranked using a composite scoring function, yielding the dominant event chain 
that characterizes flood spatiotemporal evolution.
10
Q. RAN ET AL.

Ce represents the event semantic constraint, which restricts the semantic associa­
tions between candidate events. For any event pair ðei, ejÞ; a candidate connection sat­
isfies the semantic constraint only when an edge rðei, ejÞ exists in the KG and the 
relation belongs to the predefined types in the FO.
Ct represents the temporal constraint, which controls the chronological order and 
duration relationships between candidate events. For events with explicit timestamps, 
their occurrence times must satisfy TimeðeiÞ  TimeðejÞ: For events with durations, 
temporal relations such as before, meet, overlap and contain are further used.
Cs represents the spatial constraint, which determines whether candidate events are 
spatially 
relevant 
in 
the 
context 
of 
flood 
disaster 
evolution. 
Formally, 
IsRelevantðSðeiÞ, SðejÞÞ must be true, where SðeiÞ and SðejÞ denote the spatial locations 
or spatial extents of events ei and ej; respectively.
This study evaluates spatial relevance from three aspects: place-hierarchy consist­
ency, spatial-extent consistency and hydrological-unit consistency. The constraint defi­
nitions are summarized in Table 3.
Next, the importance of event nodes is evaluated. Traditional rule-based methods 
often struggle to capture implicit semantics and structural dependencies (Li et al. 
2022a). By contrast, LLMs are used here to support semantic assessment and con­
straint-based reasoning across event attributes, spatial contexts and topological con­
nections (Zhao et al. 2026). Accordingly, LLMs are employed to assess node 
importance and compute a comprehensive score, denoted as I(e), as defined in the fol­
lowing equation:
IðeÞ ¼ a  HinðeÞ þ b  EcaðeÞ
(5) 
where HinðeÞ denotes intrinsic hazard level derived from ontology model. EcaðeÞ 2 ½0, 1
represents cascading effect index, which is a normalized score generated by the LLM 
Table 3. Definition of constraints for evolution event chains expansion.
Constraint
Relationship
Formula
Description
Ce
Trigger
rðei, ejÞ 2 Re
Event ei triggers event ej:
Induce
Event ei induces event ej:
Cause
Event ei causes event ej:
Impact
Event ei impacts event ej:
Ct
Before
Beforeðei, ejÞ
Event ei occurs before event ej:
Meet
Meetðei, ejÞ
Event ei meets event ej at a time 
point, while ei occurs first.
Overlap
Overlapðei, ejÞ
Event ei overlaps with event ej for a 
certain period.
Contain
Containðei, ejÞ
The time period of event ei 
contains event ej:
Cs
Place-hierarchy consistency
IsRelevantðSðeiÞ, SðejÞÞ
Events occur in the same place or 
in geographically nested places, 
such as a country–city or basin– 
valley relation.
Spatial-extent consistency
IsRelevantðSðeiÞ, SðejÞÞ
The spatial extents of two events 
overlap, are adjacent, or belong 
to the same affected area.
Hydrological-unit consistency
IsRelevantðSðeiÞ, SðejÞÞ
Events belong to the same flood- 
related hydrological unit, such as 
the same river valley, river reach, 
catchment, drainage unit or 
inundation zone.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
11

based on semantic context and structural position of event e within the KG. Weights a 
and b reflect relative contributions of two components. Given chain-like propagation 
characteristics of flood disasters, these values are set to a ¼ 0:3 and b ¼ 0:7:
The complete procedure is summarized in Algorithm 1.
Finally, candidate chains are evaluated using a composite scoring function. At the 
chain level, each candidate chain receives a quantitative score to identify event chain 
that best represent the main evolutionary trajectory of flood disasters. The scoring 
function SðPÞ incorporates two factors: weighted accumulation of node importance 
and confidence constraints of relations, as defined in Equation (6). Candidate chains 
are ranked according to SðPÞ; and the highest-scoring chain is selected as the main 
evolution event chain of flood disasters.
SðPÞ ¼
X
n
i¼1
ci−1IðeiÞ
 
!

Y
n
i¼2
rcðei−1, eiÞ
 
!
(6) 
where c denotes decay coefficient of node importance ð0 < c  1Þ; which controls 
attenuation of node contributions as chain depth increases. When c is small, impor­
tance of upstream triggering events is amplified, whereas contributions of secondary 
events in the middle and later stages decrease rapidly with increasing depth. This for­
mulation emphasizes dominant role of driving and triggering events in flood disaster 
event chain. The term rcðei−1, eiÞ represents the confidence of the event association 
between two adjacent event nodes, which is jointly determined by temporal consist­
ency, spatial consistency and event semantic consistency.
12
Q. RAN ET AL.

3.2.2. Spatiotemporal completion of flood evolution pathway
The main evolution pathway inferred using the method described in Section 3.2.1
reveals the underlying logic and key structural patterns of flood disaster evolution. 
However, this pathway remains an abstract representation composed of symbolic 
nodes and semantic relationships, and its correspondence with real-world geographic 
spatiotemporal processes has not been explicitly established. To bridge this gap and 
endow the inferred results with locatable and evolvable physical characteristics, this 
section enriches event nodes with explicit spatiotemporal attributes. Through this 
enrichment, the main evolution pathway is extended from a purely semantic represen­
tation to the geographic semantic level.
Each event node ei in the main event chain is examined, and its pre-extracted spa­
tiotemporal attributes are retrieved from the flood KG. Temporal attributes include the 
event timestamp, start_time and end_time, while spatial attributes comprise the coun­
try and city of occurrence as well as the corresponding central geographic 
coordinates.
These spatiotemporal attributes are integrated with event types, textual descrip­
tions and event association. The integration yields a chronologically ordered sequence 
of structured data objects, which are defined as spatiotemporal evolution pathway, as 
formalized in the following equation:
Pst ¼ he1ðt1, s1Þ!
Re e2ðt2, s2Þ!
Re    !
Re enðtn, snÞi
(7) 
where ei represents the ith event node, ti and si denote its temporal and spatial attrib­
utes, respectively. Re denotes the semantic association between adjacent event nodes. 
The resulting pathway explicitly describes when and where events occur, as well as 
what happens during the disaster evolution process. In this way, semantic information 
is integrated with spatiotemporal information within a unified representation.
3.3. Augmented representation of flood disaster evolution
Narrative representation organizes complex dynamic processes through temporal 
order, event associations and semantic coherence. To intuitively present the recon­
structed main flood evolution pathway in 3D scenes, this study adopts narrative pro­
gression as the organizing logic and develops an augmented representation method 
integrating event symbols, temporal control and viewpoint scheduling (Li et al. 2021, 
2024).
First, a 3D symbol system is designed based on the syntax–semantics–pragmatics 
framework of semiotics (Morris 1938) and map-based storytelling (Roth 2021). Flood 
disaster evolution is represented as a sequence of discrete events using the following 
equation:
ei ¼ fti, si, aig,
si ¼ ðxi, yi, ziÞ,
ai ¼ fai1, ai2, . . .g
8
<
:
(8) 
where ti denotes the time at which an event occurs, si represents spatial location com­
posed of spatial coordinates and ai denotes event attribute vector.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
13

The symbol system comprises three levels. At the syntactic level, visual variables, 
including shape, color, size, transparency and motion, distinguish different flood 
events. At the semantic level, symbols are mapped to corresponding entities and 
encode specific flood information. At the pragmatic level, textual descriptions, images, 
chart summaries, flashing effects and annotations guide users to recognize event asso­
ciations and evolution trends.
Based on this symbol system, the reconstructed spatiotemporal evolution pathway 
is used as the primary narrative thread for organizing flood events. Time t serves as 
the driving variable, and a control function SðtÞ jointly regulates event visibility and 
observation viewpoints (Li et al. 2022b), as shown in the following equation:
SðtÞ ¼
Et0, Pðx, y, zÞ, Rðh, p, rÞ, t ¼ t0,
Et1, Pðx, y, zÞ, Rðh þ s, p, rÞ, t ¼ t1:

(9) 
where Et0 and Et1 denote the invisible and visible states of an event before and after 
its occurrence, respectively. Pðx, y, zÞ defines the viewpoint position, while Rðh, p, rÞ
specifies its yaw, pitch and roll. The parameter s controls the rotational increment of 
the viewpoint over time.
By coordinating event visibility and viewpoint transitions, the proposed method 
provides a continuous and controllable 3D representation of flood evolution pathway, 
as shown in Figure 5. It supports the structured presentation of flood events and facili­
tates the identification of key stages, spatial expansion patterns and event associations 
during disaster evolution.
Figure 5. Knowledge-guided 3D representation of flood spatiotemporal evolution. Flood events 
inferred from KG are mapped into a 3D scene through a symbol system spanning syntax, semantics 
and pragmatics. Events are organized along spatial, temporal and event dimensions. Dynamic event 
control and viewpoint scheduling ensure temporal coherence and narrative continuity, enabling an 
interpretable representation of flood disaster evolution.
14
Q. RAN ET AL.

4. Experiments and results
4.1. Case study and datasets
This study adopts the extreme European flood event of July 2021 as the case study. 
Semantic information on disaster evolution was obtained from flood tweets collected 
using Twint between 1 July 2021 and 31 July 2021. A total of 34,731 tweets were ini­
tially collected. After standardized preprocessing, including noise removal and NLTK 
stop-word filtering, 20,962 high quality texts were retained for knowledge extraction, 
as shown in Figure 6. To support 3D scene construction and process simulation, multi- 
source geographic environmental data were also integrated. These data include DEM 
data with one meter resolution for flood simulation and terrain modeling, administra­
tive boundary data for defining spatial extents, and ERA5 precipitation data for 
meteorological background analysis. Detailed descriptions of the datasets are provided 
in Table 4.
To further understand the composition of the cleaned tweet corpus, we conduct a 
content distribution analysis. At the ontology-element level, tweets containing disaster 
events or phenomena (event, phenomenon) account for 99.34%, tweets with explicit 
temporal or spatial references (time, location) are 98.75%, and 41.07% tweets involve 
specific affected objects or related people(object, character), indicating that social 
Table 4. Overview of research datasets.
Data type
Spatial and temporal 
coverage
Data source
Primary use
Tweet data
Europe, July 2021
Twitter
Extraction of disaster- 
related semantic 
information
DEM data
Ahr Valley, Rhineland– 
Palatinate, Germany, at 
1 m resolution
GeoShop Rheinland-Pfalza
Flood simulation and 
high-resolution 3D 
scene construction
Administrative boundaries
European country level
Eurostat GISCOb
Study area delineation and 
spatial referencing
Flood simulation results
Areas associated with 
disaster chains
Cellular automata model 
developed in this study
Characterization of flood 
spatiotemporal 
evolution
Precipitation data
Europe
Copernicus Climate Data 
Store ERA5 datasetc
Meteorological 
background analysis
ahttps://geoshop.rlp.de/.
bhttps://ec.europa.eu/eurostat/web/gisco/geodata.
chttps://cds.climate.copernicus.eu.
Figure 6. Word clouds of high-frequency expressions in the cleaned flood-tweet corpus. Panels 
(a)–(c) show frequent disaster events and phenomena, temporal and spatial references, and 
affected objects and populations, respectively. Word size is proportional to term frequency, illustrat­
ing the dominant semantic information contained in the tweets.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
15

media data provide dense event, spatiotemporal and affected object information that 
can support the identification of disaster spatiotemporal evolution.
4.2. Prototype system implementation
This study developed a 3D flood spatiotemporal representation system deployed on a 
Windows 11 Professional platform. The experimental setup includes an AMD Ryzen 7 
5800X processor operating at 3.8 GHz, an NVIDIA GeForce RTX 3070 graphics card and 
32 GB of DDR4 memory. The system adopts a modular architecture composed of a KG 
module, an evolution pathway reconstruction module and a disaster evolution repre­
sentation module. It supports front-end representation of the KG together with real- 
time evolution pathway reconstruction. Flood disaster evolution is presented from a 
spatiotemporal perspective. The prototype system interface is shown in Figure 7.
4.3. Experimental design
To systematically evaluate the reliability of the proposed method for disaster know­
ledge extraction and evolution pathway reconstruction, as well as the interpretability 
of the 3D flood representation, this study randomly sampled 1100 tweets from the 
cleaned twitter dataset for three progressive evaluation experiments.
4.3.1. Knowledge extraction performance evaluation and comparative experiments
This experiment evaluates the knowledge extraction method proposed in Section 3.1
and examines its applicability in real disaster contexts. Four representative LLMs from dif­
ferent model families, namely DeepSeek-V3.2, GPT-4o-Mini, Gemini-2.5-Flash and 
Qwen3.5-Flash, are selected for comparison. All models adopt the same FO-constrained 
Figure 7. Interface of the prototype 3D flood spatiotemporal representation system, integrating a 
globe scene viewer with a knowledge graph panel and an evolution pathway reconstruction work­
space for interactive analysis.
16
Q. RAN ET AL.

few-shot CoT prompting strategy to ensure a fair comparison of disaster semantic under­
standing and structured knowledge generation.
Comparative experiments are then conducted using the LLM with the best overall 
performance. Three prompting configurations are compared to analyze the effects of 
explicit reasoning and domain ontology constraints on knowledge extraction 
performance.
i. 
Zero-shot prompting without examples, reasoning chains or ontology constraints, 
serving as the baseline.
ii. 
Few-shot CoT prompting, which introduces expert-annotated examples from the 
separate development set. Specifically, 30 tweets with varying levels of informa­
tion content (10 low, 10 medium and 10 high) are selected, along with their cor­
responding extraction processes and results, to guide LLM-based knowledge 
extraction without applying domain ontology constraints.
iii. 
FO-constrained few-shot CoT prompting, which uses the same few-shot examples 
as (ii) and further embeds the conceptual system and relation constraints defined 
by the FO.
4.3.2. Expert-based validation of evolution pathway reconstruction
To assess the rationality and reliability of the disaster evolution pathway reconstruc­
tion method, an expert consensus-based evaluation experiment is conducted. Based 
on the constructed flood KG, an evaluation set containing 120 candidate evolution 
pathways is generated. Among them, 60 pathways are produced by the proposed con­
strained reconstruction mechanism and constitute the Constrained Group, while the 
remaining 60 pathways are obtained through unconstrained search and form the 
Unconstrained Baseline Group.
In addition to the three experts involved in knowledge annotation, two independ­
ent domain experts participate in the evaluation. All experts rate the evolution chains 
from both groups using a five-level Likert scale across three dimensions, including 
evolution logic soundness, completeness and spatiotemporal consistency. To avoid 
evaluation bias, all candidate pathways are anonymized and randomly shuffled before 
evaluation, so that experts do not know the group source of each pathway. Statistical 
comparison of the ratings is used to examine whether the proposed method more 
effectively identifies key disaster evolution pathway.
4.3.3. User evaluation of 3D representation
To assess the effectiveness of augmented 3D flood representation for disaster cogni­
tion and understanding, a questionnaire-based user study is conducted. The main 
flood disaster evolution pathway inferred in Section 3.2 serves as input for generating 
three different forms of disaster evolution representations. These representations are 
compared to evaluate their impact on user understanding of flood disaster evolution.
The experiment involves 90 participants aged between 20 and 50, with educational 
backgrounds ranging from high school to doctoral level. All participants come from 
non-specialist backgrounds and have not received systematic training in GIS, flood- 
related domains or 3D representation. A controlled experimental design is adopted, 
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
17

and participants are randomly assigned to three groups, each containing 30 
individuals.
i. 
Text-based Group, which provides only KG-based and text-based descriptions of 
flood disaster evolution chains.
ii. 
3D Process Group, which presents 3D dynamic flood disaster evolution without 
explicit event chain annotation.
iii. 
Full Representation Group, which applies the complete 3D flood disaster chain 
representation proposed in this study. Key event nodes, directional event associa­
tions and temporal relationships are explicitly annotated within the dynamic 
scene.
After completing the assigned tasks, participants rate Likert-scale questionnaire 
items related to disaster evolution understanding. The collected responses are ana­
lyzed to evaluate differences in perceived disaster cognition across the three informa­
tion presentation modes.
4.4. Results and analysis
4.4.1. Evaluation of knowledge extraction performance
Under a unified FO constraint and few-shot CoT prompting framework, four main­
stream LLMs are first evaluated for flood-related knowledge triple extraction from 
social media tweets. At the subjective evaluation level, the cross-evaluation mechan­
ism described in Section 3.1.3 is used to assess output quality across Accuracy, 
Completeness, Consistency and Aggregate Score. To avoid potential self-preference, 
self-evaluation results generated by the LLMs are excluded. As shown in Figure 8, scor­
ing trends across evaluating LLMs are largely consistent, indicating that the cross- 
evaluation mechanism is stable at the subjective level. Gemini-2.5-Flash obtains the 
highest overall score and leads in consistency and completeness, while DeepSeek-V3.2 
performs best in accuracy but shows lower consistency, which limits its overall know­
ledge extraction performance.
Figure 9 further validates differences among LLMs in Aggregate Score, Accuracy, 
Completeness and Consistency from a statistical perspective. Friedman test results 
indicate significant differences among models across all dimensions (p < 0:001). 
Nemenyi post hoc comparisons show that Gemini-2.5-Flash significantly outperforms 
GPT-4o-Mini, Qwen3.5-Flash and DeepSeek-V3.2 in Aggregate Score (p < 0:01).
At the objective evaluation level, a manually annotated benchmark dataset contain­
ing 1100 randomly sampled tweets is constructed. Three domain experts independ­
ently annotate flood-related triples according to a unified annotation protocol and 
ontology constraints. The inter-annotator agreement measured by Fleiss’ Kappa is 
0.76, indicating substantial agreement (Landis and Koch 1977). For samples with dis­
agreement, majority voting and expert discussion are used to form the final gold- 
standard dataset. Based on this dataset, Precision, Recall, F1-score and Hallucination 
Rate (HR) are calculated for each LLM, as shown in Figure 10. HR measures the propor­
tion of triples generated by the model but not supported by the source tweet 
18
Q. RAN ET AL.

evidence. Gemini-2.5-Flash achieves the best Precision, Recall and F1-score, while also 
obtaining the lowest HR (0.09), indicating strong overall knowledge extraction per­
formance. This result is consistent with the subjective evaluation trend.
Based primarily on the manually annotated benchmark results and objective met­
rics, and with the LLM cross-evaluation used as supplementary semantic evidence, 
Gemini-2.5-Flash is selected for comparative experiments. Zero-shot, few-shot CoT and 
few-shot CoT combined with FO constraints are compared to analyze the incremental 
contribution of each prompting strategy. The overall trend is shown in Figure 11, and 
detailed comparison results are reported in Table 5.
Results in Figure 11 and Table 5 show that, compared with zero-shot prompting, 
few-shot CoT clearly improves Recall (þ0.16) and F1-score (þ0.10), indicating that few- 
shot chain reasoning helps identify flood disaster semantic information more compre­
hensively. After FO constraints are further embedded, Precision (þ0.12) and Recall 
(þ0.10) continue to increase, the F1-score reaches 0.83, and HR decreases substantially 
to 0.09. This suggests that ontology constraints can effectively suppress hallucinated 
generation and enhance knowledge consistency. Bootstrap resampling with 1000 itera­
tions further estimates a 95% confidence interval of [0.81, 0.84] for the F1-score of the 
Figure 8. Cross-evaluation heatmaps of the quality of flood knowledge graphs generated by differ­
ent LLMs under the LLM-as-a-Judge framework. The four panels present the evaluation results for 
the knowledge graphs generated by Gemini-2.5-Flash, Qwen3.5-Flash, DeepSeek-V3.2 and GPT-4o- 
Mini, respectively, in terms of accuracy, completeness, consistency and aggregate score. Warmer 
colors indicate higher evaluation scores.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
19

Figure 9. Comparison of LLM performance under multiple evaluation dimensions. Panels illustrate 
the distributions of different LLMs across aggregated quality, completeness, accuracy and consist­
ency metrics.
Figure 10. Objective evaluation of knowledge extraction across LLMs on the gold-standard dataset, 
comparing Precision, Recall, F1-score and Hallucination Rate.
20
Q. RAN ET AL.

Gemini few-shot CoT þ FO strategy, indicating stable extraction performance under 
ontology constraints.
The subjective evaluation results show a consistent pattern. Few-shot CoT þ FO 
obtains the highest scores in Accuracy, Completeness and Consistency, with an 
Aggregate Score of 4.14, clearly outperforming the other two strategies. Overall, few- 
shot CoT improves knowledge reasoning, while ontology constraints define semantic 
boundaries, suppress hallucinations and enhance consistency. Their joint use enables 
more accurate, complete and consistent extraction of flood disaster knowledge.
Based on the optimal strategy, full-scale knowledge extraction and deduplication 
are performed on all flood tweets, resulting in a flood KG containing 9171 triples and 
6393 nodes across six core semantic categories (Table 6). This KG provides a data 
foundation for subsequent evolution pathway reconstruction and 3D scene 
representation.
Figure 11. Multi-dimensional comparison of prompting strategies for flood knowledge extraction 
across objective and LLM-evaluated metrics. The figure compares three prompting strategies, 
namely zero-shot, few-shot CoT and few-shot CoT with FO constraints. Results are arranged clock­
wise from zero-shot to few-shot CoT and few-shot CoT þ FO, reflecting increasing levels of reason­
ing complexity and ontology constraint.
Table 5. Comparative analysis of prompting strategies for knowledge graph construction.
Prompt strategy
Precision
Recall
F1-score
Hallucination Rate
Zero-shot
0.66
0.58
0.62
0.20
Few-shot CoT
0.70 (þ0.04)
0.74 (þ0.16)
0.72 (þ0.10)
0.17 (−0.03)
Few-shot CoT þ FO
0.82 (10.12)
0.84 (10.10)
0.83 (þ0.11)
0.09 (20.08)
Prompt strategy
Accuracy
Completeness
Consistency
Aggregate
Zero-shot
3.72
3.25
3.54
3.50
Few-shot CoT
4.01 (þ0.29)
3.68 (þ0.43)
3.87 (þ0.33)
3.85 (þ0.35)
Few-shot CoT þ FO
4.25 (10.24)
3.91 (10.23)
4.38 (10.51)
4.14 (10.29)
Note: Bold values indicate the best performance among the three prompting strategies for each metric.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
21

4.4.2. Results and analysis of flood evolution pathway reconstruction
Five domain experts independently evaluate the evolution chain reconstruction results 
of the Constrained Group and the Unconstrained Baseline Group, as shown in Figure 12. 
Overall, the Constrained Group outperforms the baseline group across evolution logic 
soundness, completeness and spatiotemporal consistency. The distribution of expert 
ratings also shows that the proposed method yields more concentrated high-score 
results, indicating substantially reduced reconstruction uncertainty and improved stabil­
ity and consistency.
To further examine the consistency of expert ratings, the intraclass correlation coeffi­
cient (ICC) is used to assess inter-expert agreement for the Constrained Group. As reported 
in Table 7, expert ratings show high consistency across all three evaluation dimensions.
Table 6. Semantic entity composition of the 
flood knowledge graph.
Type
Number
Event
2600
Location
1739
Object
1371
Character
428
Phenomenon
199
Time
56
Figure 12. Expert evaluation of evolution pathway reconstruction results. Boxplots compare the 
Constrained Group and the Unconstrained Baseline Group across evolution logic soundness, com­
pleteness and spatiotemporal consistency. Each overlaid scatter point represents the mean score of 
one candidate pathway averaged across the five experts.
Table 7. ICC results of expert ratings.
Dimension
ICC(2,1)
95% CI
p Value
Reliability
Evolution logic soundness
0.808
[0.73, 0.87]
p < 0:001
Good
Completeness
0.798
[0.71, 0.87]
p < 0:001
Good
Spatiotemporal consistency
0.903
[0.86, 0.94]
p < 0:001
Excellent
22
Q. RAN ET AL.

The reconstructed main flood disaster evolution pathway shows a clear event-level 
evolutionary structure and can be summarized as follows, with the corresponding 
attributes reported in Table 8.
To ensure the traceability of the reconstruction results, each event node was further 
linked back to the original tweet records for evidence alignment. After completing 
evolution pathway reconstruction based on the flood KG, post-event investigation 
reports and related event studies (Kreienkamp et al. 2021, Tradowsky et al. 2023) were 
further used for supplementary comparison. This comparison examined whether the 
reconstructed pathway was consistent with post-event synthesized understanding in 
terms of key stages and evolutionary logic. It serves as an external plausibility refer­
ence for interpreting the reasoning results. The results indicate that the proposed 
framework can organize fragmented real-time disaster information into a coherent 
flood disaster event structure under temporal, spatial and semantic constraints.
4.4.3. 3D representation and user evaluation results
This study integrates flood KG and evolution pathway reconstruction results, together 
with high-resolution terrain data and flood simulation outputs, to represent flood dis­
aster evolution in a 3D spatiotemporal space. The representation depicts key event- 
level stages, including persistent heavy rainfall, river level rise, river overflow and flash 
flooding, urban inundation, infrastructure and public facility disruption, affected resi­
dents and communities, emergency response, and post-flood recovery, through 
Table 8. Attributes of the main event nodes in the reconstructed flood disaster chain.
Event node
Main attributes
Persistent heavy rainfall
Time: 14–15 July 2021; Region: Western Europe; Phenomenon: persistent 
rain, heavy rainfall, severe weather
River level rise
Location: Ahr River and nearby affected valleys; Phenomenon: rising 
floodwaters, rapidly increasing water level; Spatial cue: river corridor 
and valley areas
River overflow and flash flooding
Location: Ahr Valley and riverside settlements; Event type: river 
overflow, flash flood, fast-moving floodwater; Spatial pattern: 
floodwater spreading from river channels into nearby settlements
Urban inundation
Affected areas: riverside towns, low-lying built-up areas, valley-floor 
settlements; Affected objects: streets, roads, houses, vehicles, bridges, 
public facilities
Infrastructure and public facilities
Damaged objects: roads, bridges, railways, residential buildings, 
transport facilities, power supply, communication services
Residents and communities
Affected people: trapped residents, missing persons, casualties, 
displaced households; Community impact: evacuation needs, shelter 
demand, disruption of daily life
Emergency response and evacuation
Actors: police, firefighters, rescue teams, local authorities, residents; 
Actions: evacuation warnings, rescue operations, search and rescue, 
temporary shelter support
Post-flood recovery
Stage: after floodwater recession; Actions: cleanup, mud removal, house 
repair, infrastructure restoration, community recovery
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
23

formalized symbols and dynamic inundation processes. Core event nodes are con­
nected according to temporal order and event evolutionary direction, as shown in 
Figure 13. To improve accessibility and facilitate understanding of the full flood disas­
ter evolution, the 3D representation is recorded as a video and shared via YouTube2
and Bilibili.3
Following the user experiment design in Section 4.3.3, this study presents flood dis­
aster evolution representations to participants using three information presentation 
modes, with examples shown in Figure 14. All three modes use identical data sources, 
flood simulation results and temporal coverage. They differ only in information organ­
ization and in how event semantics are conveyed. To ensure consistency in user per­
ception and comparison, the presentation duration of all three representation modes 
was standardized to 2 min 40 s, corresponding to the duration of the enhanced 3D 
representation.
The questionnaire evaluates overall understanding of flood disaster evolution, clar­
ity of evolutionary relationships, and comprehension of temporal consistency, as sum­
marized in Table 9.
As shown in Table 10, Cronbach’s a values for Q1, Q2 and Q3 are 0.693, 0.746 and 
0.691, respectively, indicating acceptable to good internal consistency. The Kaiser– 
Meyer–Olkin (KMO) value reaches 0.902, indicating excellent sampling adequacy; 
Bartlett’s test of sphericity is significant (p < 0:001), showing strong correlations 
among variables and supporting factor analysis. Overall, the questionnaire data show 
good reliability and structural suitability for subsequent analysis.
Figure 13. 3D spatiotemporal representation of the inferred flood disaster evolution. Panels (a)–(i) 
illustrate the progressive representation of the inferred event-level flood disaster chain within a 3D 
geographic scene, ranging from persistent heavy rainfall and hydrological response to urban inun­
dation, infrastructure disruption, affected communities, emergency response and post-flood 
recovery.
24
Q. RAN ET AL.

Figure 14. Representation examples used in the user study under three presentation modes. Panel 
(a) corresponds to Group A, which provides knowledge-graph and text-based evolutionary descrip­
tions. Panel (b) corresponds to Group B, which presents 3D flood disaster evolution representation 
without explicit annotation. Panel (c) corresponds to Group C, which applies the full evolutionary 
knowledge-enhanced 3D representation integrating event-chain cues and analytical panels.
Table 9. Questionnaire for evaluating flood disaster representation.
Dimension
Question description
Scale
Q1: Overall understanding
U1: I can understand the overall evolution of the flood disaster 
from onset to development 
U2: The representation facilitates identification of key stages in 
flood disaster evolution 
U3: I have formed a comprehensive understanding of flood disaster 
evolution
1: Not at all 
2: Slightly 
3: Moderately 
4: Fairly 
5: Very.
Q2: Evolutionary clarity
C1: I can clearly identify the primary triggering factors of the flood 
disaster 
C2: I can distinguish between causal events and resulting events 
during disaster evolution 
C3: The representation facilitates understanding of evolutionary 
relationships among disaster events
Q3: Temporal consistency
T1: I can correctly determine the temporal order of disaster-related 
events 
T2: The representation supports understanding of the temporal 
progression of disaster evolution 
T3: My understanding of event chronology is consistent with the 
representation
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
25

As shown in Table 11, different information presentation modes exhibit significant 
differences across all evaluation indicators, including the three cognitive dimensions 
and the overall evaluation (Kruskal–Wallis test, p < 0:001). The Bonferroni-adjusted 
Dunn’s post hoc tests further indicate that the scores of Group C are significantly 
higher than those of Group A in Q1, Q2, Q3 and the overall evaluation (all adjusted 
p < 0:001). In addition, Group C achieves significantly higher scores than Group B in 
Q1 (p ¼ 0:008), Q2 (p ¼ 0:012) and the overall evaluation (p ¼ 0:007). Group B also 
scores significantly higher than Group A in Q2 (p ¼ 0:032), Q3 (p ¼ 0:008) and the 
overall evaluation (p ¼ 0:010), whereas the difference between Groups A and B in Q1 
is not significant (p ¼ 0:066).
When only KGs and textual descriptions are provided (Group A), participants obtain 
relatively low scores in overall understanding, evolutionary clarity and spatiotemporal 
consistency, indicating the limited cognitive support provided by this information 
presentation mode. After introducing 3D representation without symbolic annotation 
(Group B), the mean scores across the three cognitive dimensions increase, suggesting 
that spatialized representation can enhance users’ understanding of disaster evolution 
to some extent. In comparison, the proposed knowledge-guided enhanced representa­
tion method (Group C) achieves the highest mean scores across all dimensions, with a 
particularly pronounced improvement in evolutionary clarity. These results suggest 
that the proposed method is especially effective in supporting users’ understanding of 
event relationships in disaster evolution, while also improving the overall cognitive 
evaluation.
Figure 15 presents the score distributions across cognitive dimensions for the three 
information presentation modes. Clear separation is observed among the methods, 
indicating systematic differences in users’ cognitive responses. Across all dimensions, 
the proportion of higher ratings increases progressively from Group A to Group C, 
while the proportion of lower ratings decreases accordingly. This trend suggests that 
the increasing integration of three-dimensional representation and event semantics 
enhances users’ understanding of flood disaster evolution. Overall, the proposed 3D 
augmented flood representation method strengthens the intuitive representation of 
Table 10. Reliability and factorability assessment of the questionnaire.
Category
Scale/test
Key statistics
Interpretation
Reliability
Q1
Cronbach’s a ¼ 0:693
Acceptable internal consistency
Q2
Cronbach’s a ¼ 0:746
Good internal consistency
Q3
Cronbach’s a ¼ 0:691
Acceptable internal consistency
Overall scale
Cronbach’s a ¼ 0:876
Excellent overall reliability
Validity
KMO measure
KMO ¼ 0:902
Sampling adequacy is meritorious
Bartlett’s test
v2 ¼ 291:88; df ¼ 36; p < 0:001
Correlation matrix suitable for factor analysis
Table 11. Mean scores of three participant groups across questionnaire dimensions.
Group
Q1, mean ± SD
Q2, mean ± SD
Q3, mean ± SD
Overall, mean ± SD
A
2.80 ± 0.71
2.98 ± 0.75
2.78 ± 0.74
2.85 ± 0.64
B
3.20 ± 0.60
3.56 ± 0.58
3.41 ± 0.54
3.39 ± 0.45
C
3.79 ± 0.58
4.03 ± 0.54
3.83 ± 0.65
3.89 ± 0.51
Kruskal–Wallis H
28.14
29.65
26.75
35.94
p Value
< 0:001
< 0:001
< 0:001
< 0:001
g2
0.30
0.32
0.28
0.39
26
Q. RAN ET AL.

the full flood disaster evolution and more effectively conveys event relationships, 
resulting in a marked improvement in users’ overall cognitive understanding of flood 
disasters.
5. Discussion
This study proposes an augmented representation method for the spatiotemporal evo­
lution of flood disasters based on large-scale fragmented social media data. It enables 
the automatic construction of a flood KG, reconstruction of the main disaster evolution 
pathway, and 3D representation of flood scenes, thereby providing a new technical 
approach for public understanding and risk communication of complex disaster proc­
esses. However, several limitations should also be noted.
First, social media data are essentially social sensing information. They often reflect 
local disaster conditions, public perception or news dissemination rather than com­
plete disaster evolution processes. Therefore, a single tweet can provide only limited 
spatiotemporal and evolutionary information, and the generation of disaster evolution 
chains depends strongly on large-scale data aggregation and relation identification 
under temporal, spatial and event semantic consistency constraints. When a disaster is 
small in scale, short in duration, or occurs in an area with low social media activity, 
key events may be missing and spatiotemporal links may be insufficient, which can 
affect the completeness and stability of inferred disaster evolution chains.
Second, the consistency between the reconstructed evolutionary chain and post- 
disaster reports should be interpreted within the broader information environment of 
disaster communication. During major flood events, social media posts, news reports, 
public warnings and official summaries may partially share information flows, which 
means that these sources cannot always be treated as fully independent. In this study, 
post-disaster reports are used as supplementary references for event-level plausibility 
analysis rather than as direct inputs for evolutionary chain generation. The reconstruc­
tion process itself is based on the tweet-derived KG, with event nodes further linked 
Figure 15. Distribution of user ratings across cognitive dimensions for the three participant groups 
(A–C). Stacked bars show the proportions of Likert-scale responses for overall understanding (Q1), 
evolutionary clarity (Q2) and temporal consistency (Q3).
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
27

back to source tweets for evidence alignment. Future work should further incorporate 
source provenance tracking and temporally separated information sources to better 
distinguish real-time social observations from information circulated through media 
and official channels.
Third, because LLMs are involved in knowledge extraction and result evaluation, 
model hallucination and potential bias remain unavoidable. To mitigate this issue, this 
study introduces FO constraints, an evidence-anchored few-shot CoT strategy, and a 
multi-model cross-evaluation mechanism, together with external validation using a 
manually annotated gold standard dataset, which can improve the consistency and 
reliability of knowledge extraction and reconstruction to some extent. However, 
because LLMs still rely on large-scale pretraining corpora and probabilistic generation 
mechanisms, their dependence on implicit prior knowledge and language patterns 
cannot be fully eliminated. Future work should further explore model bias calibration 
and trustworthy knowledge extraction and reconstruction mechanisms for LLM-driven 
GeoAI.
Finally, the proposed framework is currently designed mainly for flood disaster 
scenarios, but its methodological structure is extensible. By reconstructing domain 
ontologies, adjusting prompt templates, and replacing 3D scene representation rules, 
the method may be extended to other hazards, such as earthquakes, landslides, 
debris flows and urban pluvial flooding. However, different disasters vary substan­
tially in triggering mechanisms, evolution patterns and observation characteristics, 
and direct transfer may reduce knowledge extraction, evolution pathway reconstruc­
tion and scene representation performance. Future research will integrate multi- 
source observations and multi-hazard scenarios to further extend and optimize the 
framework.
6. Conclusions
This study develops an integrated framework for representing flood spatiotemporal 
evolution from social media information to knowledge extraction, evolution pathway 
reconstruction and 3D dynamic representation. By injecting FO constraints into LLM- 
driven knowledge extraction, fragmented social sensing information is transformed 
into a structured flood KG. Based on temporal, spatial and event semantic constraints, 
the main flood disaster evolution pathway is further reconstructed and mapped into a 
3D geographic scene, enabling a dynamic representation of flood occurrence, develop­
ment and impacts.
The experimental results show that the proposed ontology-constrained and evi­
dence-anchored few-shot CoT strategy improves the accuracy, completeness and con­
sistency of flood knowledge extraction, while reducing hallucinated generation. The 
reconstructed flood evolution pathway shows good stability in evolutionary logic, 
completeness and spatiotemporal consistency. User evaluation further indicates that 
the knowledge-guided 3D augmented representation performs better than textual 
descriptions or basic 3D representation in supporting overall understanding, evolution­
ary clarity and temporal consistency.
28
Q. RAN ET AL.

Overall, this work provides a new methodological approach for reconstructing flood 
disaster evolution pathway from large-scale social media data and communicating 
complex disaster processes through interpretable 3D geovisualization.
Notes 
1. https://www.undrr.org/publication/human-cost-disasters-overview-last-20-years-2000-2019
2. https://youtu.be/CWtj0VZUM6g
3. https://www.bilibili.com/video/BV1zHFKzaEPs/?share_source=copy_web
Acknowledgements
The authors would like to express their gratitude to the editor and anonymous reviewers for 
their careful reading and constructive suggestions.
Author contributions
CRediT: Qingqing Ran: Conceptualization, Data curation, Formal analysis, Investigation, 
Methodology, Validation, Visualization, Writing – original draft, Writing – review & editing; 
Weilian Li: Conceptualization, Funding acquisition, Investigation, Methodology, Project adminis­
tration, Supervision, Writing – original draft, Writing – review & editing; Juan Liu: Data curation, 
Methodology, Software, Visualization, Writing – review & editing; Huiqin Li: Data curation, 
Methodology, Software, Validation, Visualization, Writing – review & editing; Pei Dang: 
Conceptualization, Methodology, Supervision, Writing – original draft, Writing – review & editing; 
Jun Zhu: Methodology, Supervision, Writing – review & editing; Qing Zhu: Methodology, 
Supervision, Writing – review & editing; Youness Dehbi: Methodology, Supervision, Writing – 
review & editing.
Disclosure statement
No potential conflict of interest was reported by the author(s).
Funding
This work was supported by the National Natural Science Foundation of China (Grant Nos. 
42571503 and 42601750), the Chinese Postdoctoral Science Foundation (Grant Nos. 
2024T170742 and 2025M770237).
Notes on contributors
Qingqing Ran is currently a Ph.D. student at the Faculty of Geosciences and Engineering, 
Southwest Jiaotong University. She received her B.S. degree from Southwest University of 
Science and Technology in 2024. She has a strong interest in topics related to virtual geographic 
environments, geovisualization and intelligent disaster representation. In this study, she con­
ceived part of the study and contributed to this article’s methodology, implementation, valid­
ation, visualization and writing.
Weilian Li is an associate professor of the Faculty of Geosciences and Engineering at Southwest 
Jiaotong University. He completed his postdoctoral research in the Geoinformation Group at the 
University of Bonn in October 2023. Additionally, he spent one year as a senior research associ­
ate in the Computational Methods Lab at the HafenCity University Hamburg. He has a strong 
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
29

interest in topics related to smart cities, disaster management and digital twins. He proposed 
the idea and contributed to this article’s methodology, supervision, experiment, writing and 
review.
Juan Liu is currently a master’s student at the Faculty of Geosciences and Engineering, 
Southwest Jiaotong University. She received her B.S. degree from Southwest Petroleum 
University in 2025. Her research interests mainly focus on geographic information science and 
geovisualization. In this study, she contributed to the methodology, experiments, visualization 
and writing.
Huiqin Li is currently pursuing her master’s degree at the Faculty of Geosciences and 
Engineering, Southwest Jiaotong University. She obtained her B.S. degree from Wuhan 
University in 2024. Her research interests include geographic information science and geovisuali­
zation. She contributed to the methodology, experimental work, visualization and writing.
Pei Dang is currently an assistant professor at the Faculty of Geosciences and Engineering, 
Southwest Jiaotong University. He received his B.S. degree in GIS from Southwest Jiaotong 
University in 2016, followed by his M.S. degree in Surveying Engineering in 2022 and his Ph.D. 
degree in 2025 from the same university. His research interests include virtual geographic envi­
ronments, spatial cognition and GeoAI. In this study, he contributed to the methodology, writ­
ing and supervision.
Jun Zhu is a professor and the deputy dean of the Faculty of Geosciences and Engineering at 
Southwest Jiaotong University. He received his Ph.D. in Cartography and GIS from the Chinese 
Academy of Sciences. His research interests include computer vision, 3D GIS and virtual geo­
graphic environments. He contributed to the supervision, methodology and proofreading.
Qing Zhu is a professor at the Faculty of Geosciences and Engineering, Southwest Jiaotong 
University. He received his Ph.D. in railway engineering from North Jiaotong University. His 
research interests include photogrammetry, geographic information systems and virtual geo­
graphic environments. He played a crucial role in supervision, review and proofreading.
Youness Dehbi is a full professor and the Chair of the Computational Methods Lab at HafenCity 
University Hamburg. He received his Ph.D. degree in the Institute of Geodesy and 
Geoinformation at the University of Bonn in 2016. His research focuses on urban reasoning, ana­
lytics, pattern recognition and machine learning for spatio-temporal data. He contributed to this 
article’s supervision, methodology, review and proofreading.
Data and codes availability statement
The data and codes that support the findings of this study can be found online at https://doi. 
org/10.6084/m9.figshare.34025157.
References
Bae, C.J. and Dodge, S., 2023. Assessing the cognition of movement trajectory visualizations: 
interpreting speed and direction. Cartography and Geographic Information Science, 50 (2), 
143–161.
Bryan-Smith, L., et al., 2023. Real-time social media sentiment analysis for rapid impact assess­
ment of floods. Computers & Geosciences, 178, 105405.
Chen, L., et al., 2026. Spatiotemporal adaptive multiscale transformer for prediction. International 
Journal of Geographical Information Science, 40 (7), 2475–2499.
Chen, Z. and Lim, S., 2021. Social media data-based typhoon disaster assessment. International 
Journal of Disaster Risk Reduction, 64, 102482.
30
Q. RAN ET AL.

Dang, P., et al., 2025. A method for assessing urban flood impacts by combining hydrodynamic 
models with entity semantic evolution. International Journal of Digital Earth, 18 (1), 2515268.
European Environment Agency, 2023. Economic losses from weather- and climate-related 
extremes in Europe. 8th EAP Headline Indicator, 2023. European Environment Agency, 
Copenhagen, Denmark. https://www.eea.europa.eu/en/analysis/publications/european-union- 
8th-environment-action-programme/indicators/03-economic-losses-from-weather
Gao, X., et al., 2025. A review of urban flood disaster chain research: causes, identification, and 
assessment. Water, 17 (23), 3344.
Gr€uninger, M. and Fox, M.S., 1995. Methodology for the design and evaluation of ontologies. In: 
D. Skuce, ed. Proceedings of the IJCAI-95 workshop on basic ontological issues in knowledge 
sharing, 19–20 August 1995, Montreal, Canada. Menlo Park, CA: AAAI Press, 1–10.
Guo, D., et al., 2005. Multivariate analysis and geovisualization with an integrated geographic 
knowledge discovery approach. Cartography and Geographic Information Science, 32 (2), 113– 
132.
Hofmeister, M., et al., 2024. Semantic agent framework for automated flood assessment using 
dynamic knowledge graphs. Data-Centric Engineering, 5, e14.
Hu, Y., et al., 2023. Geo-knowledge-guided GPT models improve the extraction of location 
descriptions from disaster-related social media messages. International Journal of Geographical 
Information Science, 37 (11), 2289–2318.
International Organization for Standardization, 2021. ISO/IEC 21838-1:2021 information technol­
ogy—top-level ontologies (TLO)—part 1: requirements. Standard ISO/IEC 21838-1:2021. Geneva, 
Switzerland: International Organization for Standardization.
Ji, Y., et al., 2025. Foundation models for geospatial reasoning: assessing the capabilities of large 
language models in understanding geometries and topological spatial relations. International 
Journal of Geographical Information Science, 39 (9), 1866–1903.
Karmegam, D., Ramamoorthy, S., and Mappillairaju, B., 2021. Near real time flood inundation 
mapping using social media data as an information source: a case study of 2015 Chennai 
flood. Geoenvironmental Disasters, 8 (1), 25.
Kejriwal, M., 2022. Knowledge graphs: a practical review of the research landscape. Information, 
13 (4), 161.
Kreienkamp, F., et al., 2021. Rapid attribution of heavy rainfall events leading to the severe flooding 
in Western Europe during July 2021. Report. London, UK: World Weather Attribution.
Kumar, V., et al., 2023. Comprehensive overview of flood modeling approaches: a review of 
recent advances. Hydrology, 10 (7), 141.
Landis, J.R. and Koch, G.G., 1977. The measurement of observer agreement for categorical data. 
Biometrics, 33 (1), 159–174.
Li, H., et al., 2025. A question-answering framework for geospatial data retrieval enhanced by a 
knowledge graph and large language models. International Journal of Digital Earth, 18 (1), 
2510566.
Li, J., et al., 2022a. A survey on deep learning for named entity recognition. IEEE Transactions on 
Knowledge and Data Engineering, 34 (1), 50–70.
Li, W., et al., 2021. An augmented representation method of debris flow scenes to improve pub­
lic perception. International Journal of Geographical Information Science, 35 (8), 1521–1544.
Li, W., et al., 2022b. Three-dimensional virtual representation for the whole process of dam-break 
floods from a geospatial storytelling perspective. International Journal of Digital Earth, 15 (1), 
1637–1656.
Li, W., et al., 2023. Social media insights on public perception and sentiment during and after 
disasters: the European floods in 2021 as a case study. Transactions in GIS, 27 (6), 1766–1793.
Li, W., et al., 2024. Visual attention-guided augmented representation of geographic scenes: a 
case of bridge stress visualization. International Journal of Geographical Information Science, 38 
(3), 527–549.
Li, Z., et al., 2018. A novel approach to leveraging social media for rapid flood mapping: a case 
study of the 2015 South Carolina floods. Cartography and Geographic Information Science, 45 
(2), 97–110.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
31

Lin, H., et al., 2020. Cognitive transformation from geographic information system to virtual geo­
graphic environments. Journal of Geo-Information Science, 22, 662–672.
Liu, Y., et al., 2022. Deducing flood development process using social media: an event-based 
and multi-level modeling approach. ISPRS International Journal of Geo-Information, 11 (5), 306.
Liu, Y., et al., 2023. G-Eval: NLG evaluation using GPT-4 with better human alignment. In: 
H. Bouamor, J. Pino, and K. Bali, eds. Proceedings of the 2023 conference on empirical methods 
in natural language processing, 6–10 December 2023, Singapore. Singapore: Association for 
Computational Linguistics, 2511–2522.
L€u, G., Yuan, L., and Yu, Z., 2022. Information geography: a new fulcrum of geographic ternary 
world. Science China Earth Sciences, 65 (2), 383–386.
Mantovani, J., et al., 2024. Assessing flood risks in the Taquari-Antas Basin (Southeast Brazil) dur­
ing the September 2023 extreme rainfall surge. Npj Natural Hazards, 1 (1), 9.
Mihunov, V.V., et al., 2022. Disaster impacts surveillance from social media with topic modeling 
and feature extraction: case of Hurricane Harvey. International Journal of Disaster Risk Science, 
13 (5), 729–742.
Morris, C.W., 1938. Foundations of the theory of signs. Volume 1 of international encyclopedia of 
unified science. Chicago, IL: University of Chicago Press.
Noy, N.F. and McGuinness, D.L., 2001. Ontology development 101: a guide to creating your first 
ontology. Technical Report. Stanford, CA: Stanford Knowledge Systems Laboratory.
Peng, C., et al., 2023. Knowledge graphs: opportunities and challenges. Artificial Intelligence 
Review, 56, 13071–13102.
Peng, X., et al., 2022. From sponge cities to sponge watersheds: enhancing flood resilience in 
the Sishui River Basin in Zhengzhou, China. Water, 14 (19), 3084.
Phengsuwan, J., et al., 2021. Use of social media data in disaster management: a survey. Future 
Internet, 13 (2), 46.
Roth, R.E., 2021. Cartographic design as visual storytelling: synthesis and review of map-based 
narratives, genres, and tropes. Cartographic Journal, 58 (1), 83–114.
Saunders, K.R., et al., 2025. Data-driven recommendations for enhancing real-time natural hazard 
warnings. One Earth, 8 (5), 101274.
Tradowsky, J.S., et al., 2023. Attribution of the heavy rainfall events leading to severe flooding in 
Western Europe during July 2021. Climatic Change, 176 (7), 90.
UNDRR, 2020. The human cost of disasters: an overview of the last 20 years (2000–2019). Report. 
Geneva, Switzerland: United Nations Office for Disaster Risk Reduction.
Uschold, M. and King, M., 1995. Towards a methodology for building ontologies. In: D. Skuce, ed. 
Proceedings of the workshop on basic ontological issues in knowledge sharing, IJCAI-95, 19–20 
August 1995, Montreal, Canada. Edinburgh, UK: Artificial Intelligence Applications Institute, 
University of Edinburgh, 1–13.
van Cauter, Z. and Yakovets, N., 2024. Ontology-guided knowledge graph construction from 
maintenance short texts. In: R. Biswas, et al., eds. Proceedings of the 1st workshop on know­
ledge graphs and large language models (KaLLM 2024), 15 August 2024, Bangkok, Thailand. 
Kerrville, TX: Association for Computational Linguistics, 75–84.
Wang, J., Hu, Y., and Joseph, K., 2020. NeuroTPR: a neuro-net toponym recognition model for 
extracting locations from social media messages. Transactions in GIS, 24 (3), 719–735.
Wang, S., et al., 2024. GPT, large language models (LLMs) and generative artificial intelligence 
(GAI) models in geospatial science: a systematic review. International Journal of Digital Earth, 
17 (1), 2353122.
Xu, F., et al., 2025. Large language model applications in disaster management: an interdiscipli­
nary review. International Journal of Disaster Risk Reduction, 127, 105642.
Xue, Z., Xu, C., and Xu, X., 2023. Application of ChatGPT in natural disaster prevention and 
reduction. Natural Hazards Research, 3 (3), 556–562.
Yang, Y., et al., 2026. Automated extraction of spatiotemporal disaster knowledge for urban 
floods: a multimodal framework based on LLMs and agent. International Journal of Digital 
Earth, 19 (1), 2640706.
32
Q. RAN ET AL.

Zajac, M., et al., 2025. Unifying flood-risk communication: empowering community leaders 
through AI-enhanced, contextualized storytelling. Hydrology, 12 (8), 204.
Zhao, W.X., et al., 2026. A survey of large language models. Frontiers of Computer Science, 20 
(12), 2012627.
Zhao, X., et al., 2023. A hierarchical spatio-temporal object knowledge graph model for dynamic 
scene representation. Transactions in GIS, 27 (7), 1992–2016.
Zheng, K., et al., 2022. A knowledge representation model based on the geographic spatiotem­
poral process. International Journal of Geographical Information Science, 36 (4), 674–691.
Zheng, L., et al., 2023. Judging LLM-as-a-judge with MT-Bench and Chatbot Arena. In: A. Oh, 
et al., eds. Advances in neural information processing systems, 10–16 December 2023, New 
Orleans, LA, USA. Red Hook, NY: Curran Associates, Inc., 46595–46623.
Zhu, G., et al., 2022. Modeling the evolution of major storm-disaster-induced accidents in the 
offshore oil and gas industry. International Journal of Environmental Research and Public 
Health, 19 (12), 7216.
Zhu, J., et al., 2024. A flood knowledge-constrained large language model interactable with GIS: 
enhancing public risk perception of floods. International Journal of Geographical Information 
Science, 38 (4), 603–625.
Zou, L., et al., 2018. Mining Twitter data for improved understanding of disaster resilience. 
Annals of the American Association of Geographers, 108 (5), 1422–1441.
INTERNATIONAL JOURNAL OF GEOGRAPHICAL INFORMATION SCIENCE
33
