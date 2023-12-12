import httpx
from logging import getLogger

from fastapi import BackgroundTasks
from src.app.backend import background_job
from src.configurations import EncodeModelConfigurations

logger = getLogger(__name__)
ENCODE_URL = f"http://{EncodeModelConfigurations.address}:{EncodeModelConfigurations.rest_port}/{EncodeModelConfigurations.signature_name}/{EncodeModelConfigurations.model_spec_name}"
    

class ImageEncoder(object):
    def __init__(
        self,
        encode_url: str,
    ):
        self.encode_url = encode_url
        
    def predict(
        self,
        byte_string: str,
        img_shape: tuple,
        session_id: str,
        background_tasks: BackgroundTasks,
    ):
        payload = {}
        cache_data = background_job.get_data_redis(key=session_id)
        if cache_data is None:
            logger.info(f"registering cache: {session_id}")
            payload = {
            'encoded_image': byte_string,
            'image_embedding': None,
            'image_shape': img_shape[:2],
            'input_point': [],
            'input_label': [],
            'input_box': None,
            }
            
            try:
                response = httpx.post(self.encode_url, json=payload, timeout=None)
                payload['image_embedding'] = response.json()['image_embedding']
            except (BrokenPipeError, httpx.RemoteProtocolError, ConnectionResetError) as e:
                print("wait and try again")
            
            background_job.save_data_job(data=payload, item_id=session_id, background_tasks=background_tasks)
        else:
            logger.info(f"cache hit: {session_id}")


imageencoder = ImageEncoder(
    encode_url=ENCODE_URL
)