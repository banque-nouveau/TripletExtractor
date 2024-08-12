# TripletExtractor

The main functionality of this code is to take in a chunk of txet and produce Entity, Relation, Entity Triplets (along with identification of the subject and object types)

To install the package:
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
