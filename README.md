# TripletExtractor

This repository contains various scipts on Triplet Extraction (llm approach, REBEL model - ) from a given text (along with identification of the subject and object types) and natural language processing techniques on the extracted relations (e.g. semantic similarity, clustering).

The repository contains a python package which can be used for the Triplet Extraction using openai LLMs. To install the package (better to be in a fresh environment and we have tested this in python=3.10):

```
pip install -r requirements.txt
python setup.py install

```
A simple example of how to use this is demonstrated in [demo_triplet_extraction](examples/demo_kgtrip.ipynb)

The code uses a slightly modified version of the prompt that has been used in some previous work to construct such knowledge graphs like [this one from Blackrock and NVIDIA](https://arxiv.org/abs/2408.04948). We have used `instructor` to get structured outputs from the LLM conforming to a pydantic model.

The workflow summary is:
- rephrase the document replaceing pronouns by entity names. While co-reference resolution has been done before in different ways, we have just resorted to an LLM and it seems to work quite well. A challenge is having the same agreed upon set of entity names.
- send chunks of the document for triplet etraction
- postprocess to obtain a csv file ready for Neo4j ingestion.

## Evaluation

Currently, we have been doing qualitative evaluation, mostly using spot checks com[paring the input text and the triplets constructed. This has some examples in the `qual_evals` directory. Larger scale statistical evluation through metrics is a goal we would like to work to.

There are simple UI scripts that we have to look at the extraction and also compare between models.

The summary is that the spot checks show that the methods  are not very robust (at least in the way we have used them).  This can be improved in several ways and motivate such study.

## Alternatives

### Towards better ontologies 

Lacking a predefined ontology (entity lists, relation lists, entity tyoes) in combination with using llms to generate triplets can lead to arbitrarily large number of different entities and relations. Consequently, the size of the constructed graph can easily explode if the different entities and relations are too granular. To coarsen the Knowledge Graph one can control the number of different types of entities and relation. The following notebooks are attempts to control the number of different relations.


Here are some examples of methods used to etract ontologies from text
`TripletExtractor/preprocessing/filter_relations.ipynb`: An exploration notebook on finding pairs of relations that are semantically similar.

`TripletExtractor/preprocessing/cluster_relations.ipynb`: A notebook on clustering relations in an attempt to control the coarsness of the KG.

###  Alternative Methods of Constructing Knowledge Graphs
Alternative ways to do the Triplet Extraction can be found in the `preprocessing` directory.

### Alternative methods of building KG and Consensus
- An idea to building better knowledge graphs is by studying some form of consensus between different methods. We have experimented with openAI / Mistral /Triplex (will be discussed) and also considered some of the smaller / oldeer models that were state of the art before GPT3 came out. Such a model was REBEL and we have some examples on how to use it.

The REBEL (Relation Extraction By End-to-end Language generation) model is a pre-trained Encoder-Decoder Transformer (BART) that is finetuned on an array of Relation Extraction and Relation Classification benchmarks. The key idea is that the (subject, relation, object) triplets are treated as sequences of text ([paper](https://aclanthology.org/2022.emnlp-demos.34/)).

`TripletExtractor/rebel`: Contains example script for extracting triplets from a given text paragraph using the REBEL model.

