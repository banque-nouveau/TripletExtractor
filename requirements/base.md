Basic logic 
----------

1. [] Use a choice of static prompts to do extraction
1. [] Use Open AI keys passed as parameters
1. [X] Use Open AI model names
1. [X] Use OpenAI package
1. Ideally use the llm class of nvnlp as this abstracts the llm into different cases.
1. [X] Obtain all triplets without any similiarity checks
1. [X] Add types of entity to the triplets. So 
1. [] Add similarity collapse logic
1. [] Add ability to choose entities from a list
1. [] Add ability to choose relationships from a list
1. [] Add ability to choose entity types from a list
1. [] Add ability to choose relationship types from a list
1. [] Add ability to choose entities and relations from a schema
1. [] return list of triplets 
1. [] return list of triplets converted to strings as keys and original text chunk ?
1. [X] write list of triplets to disk on a bucket

Parameters
----------

- [X]text chunk from which extraction must take place ?
- [] bucket url from which extraction must take place?
- [x] open AI model name
- [] open AI keys 
- [X] use .env file for openai keys
- [X] path on disk to write out parquet file


Returns
-------
Exception /Done 


Changes
-------

- write list of triplets (could have duplicates) to bucket

