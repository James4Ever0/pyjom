from pydantic import BaseModel
import numpy as np
from typing import Union
class Image(BaseModel):
    image:Union[str,np.ndarray]