from fastapi import FastAPI
from services import get_knowledge_graph_representation
from openai import OpenAI
from dotenv import load_dotenv


app = FastAPI()


@app.get("/")
def get_all():
    return {"message": "Hello World\n"}

@app.get("/trextract/{chunk}")
async def return_list(chunk:str):
    load_dotenv()
    client = OpenAI()
    ll = get_knowledge_graph_representation(client, chunk)

    return ll

@app.post("trextract_post")
async def write_triplets(chunk:str, path:str):
    load_dotenv()
    client = OpenAI()
    ll = get_knowledge_graph_representation(client, chunk)
    write_to_parquet(ll, path)
    return {"message": "File written successfully"} 

import uvicorn
uvicorn.run(app)