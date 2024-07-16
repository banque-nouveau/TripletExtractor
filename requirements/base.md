Basic logic 
----------

1. [] Use a choice of static prompts to do extraction
1. [] Use Open AI keys passed as parameters
1. [X] Use Open AI model names
1. [X] Use OpenAI package
1. Ideally use the llm class of nvnlp as this abstracts the llm into different cases.
1. [X] Return all triplets without any similiarity checks
1. [] Add similarity collapse logic
1. [] Add ability to choose entities from a list
1. [] Add ability to choose relationships from a list
1. [] Add ability to choose entities and relations from a schema
1. [] return list of triplets 
1. [] return list of triplets converted to strings as keys and original text chunk ?

Parameters
----------

- [X]text chunk from which extraction must take place ?
- [] bucket url from which extraction must take place?
- [x] open AI model name
- [] open AI keys (or use .env file)


Returns
-------
list of triplets (could have duplicates)

