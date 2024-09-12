# TripletExtractor

This repository contains various scipts on Triplet Extraction (llm approach, REBEL model - ) from a given text (along with identification of the subject and object types) and natural language processing techniques on the extracted relations (e.g. semantic similarity, clustering).

The repository contains a python package which can be used for the Triplet Extraction. To install the package:

```
python setup.py install
```

Extracting Triplet extraction using the BlackRock prompts is demonstrated in [demo_triplet_extraction](examples/demo_kgtrip.ipynb)

## Scratch

```
curl -X 'POST' \
  'http://127.0.0.1:8000/trextract_post' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "chunk": "Apple introduced Iphone",
  "output_path": "tmp",
  "use_minio": "true",
  "minio_bucket": "kgtriplets",
  "model": "gpt-4o"
}'
```

Alternative ways to do the Triplet Extraction can be found in the `preprocessing` directory.

## Directories

`TripletExtractor/rebel`: Contains example script for extracting triplets from a given text paragraph using the REBEL model.

`TripletExtractor/preprocessing/filter_relations.ipynb`: An exploration notebook on finding pairs of relations that are semantically similar.

`TripletExtractor/preprocessing/cluster_relations.ipynb`: A notebook on clustering relations in an attempt to control the coarsness of the KG.
