from pydantic import BaseModel
import numpy as np
from typing import Union
class Image(BaseModel):
    image:Union[str,np.ndarray]

from fastapi import FastAPI

app = FastAPI()

@app.post("/books/")
def create_book(book: Image):
    # return book
    print book.image.