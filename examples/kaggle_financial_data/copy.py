"""
Change the path variable so that `/Users/rbiswas/doc/sebx/data/`to point to the location of the  
"""
from pathlib import Path
from dotenv import load_dotenv
import glob
import shutil
import os

load_dotenv()
kaggle_data_path_str = os.getenv('KAGGLE_DATASET_PATH')
kaggle_data_path = Path(kaggle_data_path_str)
path = kaggle_data_path/'2018_01*/*.json'



fnames = glob.glob(str(path))
for i, fname in enumerate(fnames):
    shutil.copy(fname, kaggle_data_path/'subset')
    #print(fname)
    #print(kaggle_data_path/'subset')
    if i == 100:
        break

