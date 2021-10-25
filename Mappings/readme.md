# Contents of this directory

This directory stores four interaction and three sequence level embeddings for three interaction log datasets in individual JSON formats. There are two JSON files -- interaction_embeddings.json and sequence_embeddings.json that store individual embeddings of interaction level taxonomies in combination to interaction log datasets and interaction level taxonomies to sequence level taxonomies for the interaction log datasets.

The interaction level taxonomies are _Amar et al._, _Brehemer and Munzner_, _Gotz and Zhou_ and _Yi et al._ and the sequence level taxonomies are _Guo et al_, _Schneiderman's Information Seeking Mantra_ and _Gotz and Wen_.

1. interaction_embeddings.json consists of embeddings of the four interaction level taxonomies for each of the three interaction log datasets. An example of Brehmer and Munzner interaction level embedding for the Liu and Heer (LH) interaction log dataset embedding JSON structure is:
  ```
    "LH-brehmer-mapping":{
         "range select":{"mapping":"select","description":"click and drag over multiple bins in one or more dimensions"},
		     "zoom":{"mapping":"navigate","description":"navigate to higher or lower levels of data resolution"},
         ...
	}
  ```
Here, range select and zoom are distinct interactions seen in the Liu and Heer (LH) dataset. The corresponding Brehmer and Munzner (brehmer) interaction level embedding mappings are select and navigate. A description of how we come up with the embeddings is added to provide more context.
    
3. sequence_embeddings.json uses interaction level embeddings and maps them to three sequence level taxonomies for each of the three interaction log datasets in individual JSON elements which form sequence level embeddings. An example of the Brehmer and Munzner (brehmer) mapping to Shneiderman's information seeking mantra (ism) is expressed as the following JSON structure:
  ```
    "brehmer-ism-sequences":{
		     "select":"details-on-demand",
		     "navigate":"zoom",
         "encode":"null",
		     "arrange":"null",
		     "change":"null",
		     "filter":"filter",
		     "aggregate":"overview",
		     "annotate":"null",
		     "import":"null",
		     "derive":"details-on-demand",
		     "record":"null",
		     "null":"null"
	}
  ```
So, select and navigate Brehmer and Munzner interaction level embedding categories map to details-on-demand and zoom Shneiderman's ISM categories. Further, we provide a regular expression of mapping the interaction level embeddings to sequence level embeddings.
 ```
  "brehmer-ism-mapping":{
		"expression":"(aggregate)*(navigate|filter)+(select|derive)+",
		"patterns":["[aggregate*, navigate+, filter+, select+]",
					"[aggregate*, filter+, navigate+, select+]",
          ...
    }
  ```
Since the information seeking mantra is overview, zoom and filter then details on demand and from the _brehmer-ism-sequences_ embeddings, we find that aggregate, navigate, filter and derive or select correspond to the overview, zoom, filter and details on demand information seeking mantra categories. Hence, the regular expression forming the information seeking mantra is presented in expression in the JSON element -- _(aggregate)*(navigate|filter)+(select|derive)+_. To understand better, we also show few patterns that form the information seeking mantra in _patterns_.
