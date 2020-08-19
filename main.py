import io
from PIL import Image

from fastapi import FastAPI, status, File, Response
from myticon.model import load_model
from myticon.utils import pre_prop, post_prop, image_loader

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = load_model()

class Item(BaseModel):
    base64: str

@app.post('/draw', status_code=status.HTTP_200_OK)
async def drawMyticon(
    input_file: bytes = File(...)
    ):
    image = Image.open(io.BytesIO(input_file)).convert('RGB')
    image = pre_prop(image)
    image = image_loader(image)
    
    output = model.draw_fake(image)
    pil_img = post_prop(output)
    imgByteArr = io.BytesIO()
    pil_img.save(imgByteArr, format='JPEG')
    
    return Response(content=base64.b64encode(imgByteArr.getvalue()), media_type="image/jpeg")