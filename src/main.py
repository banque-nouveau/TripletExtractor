from fastapi import FastAPI
from fastapi.responses import JSONResponse
from services import KGTriplets


app = FastAPI()


@app.get("/")
def get_all():
    return {"message": "Hello World\n"}

@app.get("/trextract/{chunk}")
async def return_triplets(chunk:str):
    kgtriplets = KGTriplets()
    response = kgtriplets.get_knowledge_graph_representation(chunk)
    input_df, output_df = kgtriplets.wrap(response)
    return {"input_df":input_df, "output_df":output_df}

from pydantic import BaseModel
class MyPayload(BaseModel):
    chunk: str
    output_path: str
    use_minio: str = "false"
    minio_bucket: str = "kgtriplets"
    model: str = "gpt-4o"


@app.post("/trextract_write")
async def write_triplets(mypayload: MyPayload):
    chunk = mypayload.chunk
    output_path = mypayload.output_path
    kgtriplets = KGTriplets(use_minio=mypayload.use_minio, miniobucket=mypayload.minio_bucket)
    kgtriplets.serialize_kg(chunk, output_path, model=mypayload.model) 
    return {"status": "ok", "content":mypayload.model_dump()}




@app.post('/test')
def test(mypayload: MyPayload):
    return {'payload': mypayload.model_dump(), 'status':'ok'}

import uvicorn
uvicorn.run(app) --reload