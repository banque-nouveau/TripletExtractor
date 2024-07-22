

from pydantic import BaseModel
from typing import List, Union

class TripletResponse(BaseModel):
    input: str
    subject : List[str] 
    object: List[str]  
    relation: List[str]
    subject_type: List[str]
    object_type: List[str]

