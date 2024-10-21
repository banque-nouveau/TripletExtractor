


## Steps

- Downlaod the kaggle dataset from Kaggle `https://www.kaggle.com/datasets/jeet2016/us-financial-news-articles` and unzip it into a folder 
- start a .env file with the variable `KAGGLE_DATASET_PATH` pointing to this folder.
- create a subset folder in this directory
- Activate an env with the requirements file
- run `copy.py` to obtain the subset data (100 files) in the subset subdirectory.
- run `rephrase.ipynb` 
- run `write_triplets.ipynb`

## Takeaways
- copy/rephrase worked on most of 99% of files 
- write_triplets apparently failed on 14 files (13 of which is due to max length exception on gpt4-o)

