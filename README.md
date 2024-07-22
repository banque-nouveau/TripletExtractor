


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
