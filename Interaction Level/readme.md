# Code
1. interaction_coverage.py informs the coverage of all four interaction level taxonomies for each of the three interaction log datasets. To run the code -
```
python interaction_coverage.py
```
That is the percentage of distinct interactions being non-null.
Example of Amar et al. interaction level coverage is - 
```
Amar et al. embedding coverage:
Battle and Heer: 50.0%
Liu and Heer: 75.0%
Wall: 90.909%
Average Amar et al. embedding coverage:  71.96966666666667%
```
Also, shows the distribution of individual taxonomy categories for each of the datasets to understand which taxonomy categories are really relevant or not.
Example of percentage of Battle and Heer interaction log dataset that is of various Amar et al. categories such as characterize-distribution, filter, etc. is 41.989%, 21.989%, etc. 
```
Amar et al. Inverse Coverage -->
Battle and Heer
characterize-distribution --> 41.989%
filter --> 21.989%
determine-range --> 17.569%
sort --> 13.149%
compute-derived-value --> 2.762%
correlate --> 1.326%
cluster --> 0.773%
retrieve-value --> 0.442%
find-extremum --> 0.0%
characterize-range --> 0.0%
find-anomalies --> 0.0%
```

2. interactions.py outputs a interaction_embeddings.txt file with all the mappings of a specific interaction log dataset and interaction level taxonomy. To run the code -

```
python interactions.py
```
The input needed is name of the interaction level taxonomy and dataset that you want the interaction embeddings for. The interaction embeddings are stored as a text interaction_embeddings.txt file.
