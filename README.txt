This project contains a heuristic approach for automatic keyword extraction using PageRank.
In this means, data samples of very different nature were added and investigated
to mime the cleaning and scaling problem of extremely heterogeneous data.
These data samples are open-source and can be found under http://www.nltk.org/nltk_data/, further information is given in the project paper.

For each text kind an own parser was implemented and timed.

For a proof-of-concept, the PageRank and TextRank algorithms were called with .txt files.

The file "keywords.txt" contains exemplifying outputs of the TextRank algorithm, yet before data cleaning.

Not provided is deprecated code that was implemented during the project and lead to the genesis of the final result.
They ran, however, did not yield the correct results.

The PageRank-implementation in the file pagerank_mapreduce was not adaptable for a textual input.
In the file PageRank.py, an own implementation of an older project has been reused and
called in the file textrank.py. This project focussed on automatic text summarisation
hence the output of textrank.py are summaries.

The initial implementaion of building a taxonomy modelled the wrong parent-child relationship,
hence yielding in a tree with a one-levelled tree, containing one node (node 0),
meaning, that all other nodes are children of this node, thus being a flat hierarchy.

These both isseues have been fixed in the methods of the adjusted file keyword_textrank.py


Sources of code-snippets:
map-reduce.py && pagerank_mapreduce: 
http://michaelnielsen.org/blog/using-mapreduce-to-compute-pagerank/


keyword_textrank.py: 
https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0

Source and inspiration for building a tree algo from a parent array:
https://www.techiedelight.com/build-binary-tree-given-parent-array/
https://www.geeksforgeeks.org/construct-a-binary-tree-from-parent-array-representation/

PageRank.py
https://github.com/ikiraschielke/Automatic-Text-Summarisation.git
