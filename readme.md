# Taxonomies-Embeddings

Make theoretical taxonomies applicable using programmable embeddings and develop new and relevant taxonomies.

Although the visualization community has come up with many visualization taxonomies, it is unclear how to evaluate a taxonomy. That is, it is hard to understand which taxonomy is best for a given interaction log dataset, or even how to apply the taxonomy to a set of interaction log datasets. We present a two-stage approach to assess whether existing taxonomies are generalizable enough to automate the way we analyze real-world interaction log datasets.
1. We leverage Gotz and Zhou’s multi-tier characterization of user’s analytic activities to create a general-purpose framework that clusters 30 different visualization taxonomies by the kinds of interaction log analyses they can support. Our framework has four levels: *interaction level*, *sequence level*, *task level* and *reason level*.
2. We present a novel process for programmatically mapping different taxonomies to interaction log datasets. Specifically, we develop programmable templates that can label interaction logs with their corresponding categories from a given taxonomy. We refer to these templates as **embeddings**.

## Installation

Ensure you are in the main directory. It will be easier to create a virtual environment and install the requirements.
```
pip install virtualenv
virtualenv venv
source venv/bin/activate

pip3 install -r requirements.txt
```

## Codes
All codes must be run simply using:

```
python <name_of_file>.py
```
1. The Interaction Logs directory consists of the three interaction log datasets: _Battle and Heer_, _Liu and Heer_ and Wall that are analyzed here. It also consists of script that informs the statistics of the datasets.
2. The Embeddings directory consists of two JSON files that contain the interaction level and sequence level embeddings of four interaction level taxonomies: _Amar et al._, _Brehmer and Munzner_, _Gotz and Zhou_ and _Yi et al._ and three sequence level taxonomies: _Guo et al._, _Shneiderman_, _Gotz and Wen_ for the three interaction log datasets.
3. The Interaction Coverage directory provides the coverage analysis of interaction level taxonomies.
4. The Sequence Coverage directory provides the coverage analysis of sequence level taxonomies.
