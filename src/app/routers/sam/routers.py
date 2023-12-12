from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import JSONResponse
import base64
import numpy as np
from io import BytesIO
from PIL import Image
from logging import getLogger

from src.app.routers.sam.schema import ClickList, Add, Rectangle, ImageRequests
from src.app.ml.sam.encode_prediction import imageencoder
from src.app.ml.sam.decode_prediction import maskdecoder

logger = getLogger(__name__)

router = APIRouter(
    prefix="/api/sam"
)


@router.post("/image")
async def process_images(
    background_tasks: BackgroundTasks,
    requests: ImageRequests,
):
    request = dict(requests)
    
    byte_string = base64.b64decode(request['image'])
    
    image_data = BytesIO(byte_string)
    img = np.array(Image.open(image_data))
    
    imageencoder.predict(byte_string=request['image'],
                        img_shape=img.shape,
                        session_id=request['session_id'],
                        background_tasks=background_tasks)
        
    # Return a JSON response
    return JSONResponse(
        content={
            "message": "Images received successfully",
        },
        status_code=200,
    )
    
    
@router.post("/click")
async def click_images(
    background_tasks: BackgroundTasks,
    request: ClickList,
):
    request = dict(request)

    response = maskdecoder.predict_click(
        request=request,
        background_tasks=background_tasks,
    )
    
    return JSONResponse(
        content={
            "masks": response,
            "message": "Images processed successfully"
        },
        status_code=200,
    )
    
    
@router.post("/rect")
async def rect_images(
    background_tasks: BackgroundTasks,
    requests: Rectangle,
):
    request = dict(requests)
    coords = [request['startX'], request['startY'], request['endX'], request['endY']]
    response = maskdecoder.predict_rect(
        coords=coords,
        session_id=request['session_id'],
        background_tasks=background_tasks,
    )
    
    return JSONResponse(
        content={
            "masks": response,
            "message": "Images processed successfully"
        },
        status_code=200,
    )


@router.post('/finish_click')
async def adds(
    background_tasks: BackgroundTasks,
    request: Add,
):
    request = dict(request)

    maskdecoder.reset(
        session_id=request['session_id'],
        background_tasks=background_tasks,
    )
    
    return JSONResponse(
        content={
            "message": "Finish successfully",
        },
        status_code=200,
    )
