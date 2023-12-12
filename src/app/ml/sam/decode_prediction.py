import httpx
from logging import getLogger

from fastapi import BackgroundTasks
from src.app.backend import background_job
from src.configurations import DecodeModelConfigurations

logger = getLogger(__name__)
DECODE_URL = f"http://{DecodeModelConfigurations.address}:{DecodeModelConfigurations.rest_port}/{DecodeModelConfigurations.signature_name}/{DecodeModelConfigurations.model_spec_name}"
    

class MaskDecoder(object):
    def __init__(
        self,
        decode_url: str,
    ):
        self.decode_url = decode_url
        
    def predict_click(
        self,
        request: dict,
        background_tasks: BackgroundTasks,
    ):
        cache_data = background_job.get_data_redis(key=request['session_id'])
        cache_data['input_point'].append(request['points'])
        cache_data['input_label'].append(request['labels'][0])
        
        decode_payload = {
            "image_embeddings": cache_data['image_embedding'],
            "image_shape": tuple(cache_data['image_shape']),
            "input_label": cache_data['input_label'],
            "input_point": cache_data['input_point'],
            "input_box": cache_data['input_box'],
        }
        
        try:
            response = httpx.post(self.decode_url, json=decode_payload, timeout=None)
            logger.info(f"decode cache click hit: {request['session_id']}")
            background_job.save_data_job(data=cache_data, item_id=request['session_id'], background_tasks=background_tasks)
            return response.json()['masks']
        except (BrokenPipeError, httpx.RemoteProtocolError, ConnectionResetError) as e:
            logger.info(f"decode cache click fail: {request['session_id']}")
            print("wait and try again")
    
    def predict_rect(
        self,
        coords: list,
        session_id: str,
        background_tasks: BackgroundTasks,
    ):
        cache_data = background_job.get_data_redis(key=session_id)
        cache_data['input_box'] = coords
        
        decode_payload = {
            "image_embeddings": cache_data['image_embedding'],
            "image_shape": cache_data['image_shape'],
            "input_label": None,
            "input_point": None,
            "input_box": cache_data['input_box'],
        }
        
        try:
            response = httpx.post(self.decode_url, json=decode_payload, timeout=None)
            logger.info(f"decode cache rect hit: {session_id}")
            background_job.save_data_job(data=cache_data, item_id=session_id, background_tasks=background_tasks)
            return response.json()['masks']
        except (BrokenPipeError, httpx.RemoteProtocolError, ConnectionResetError) as e:
            logger.info(f"decode cache rect fail: {session_id}")
            print("wait and try again")
    
    def reset(
        self,
        session_id: str,
        background_tasks: BackgroundTasks,
    ):
        cache_data = background_job.get_data_redis(key=session_id)
        cache_data['input_point'] = []
        cache_data['input_label'] = []
        cache_data['input_box'] = None
        background_job.save_data_job(data=cache_data, item_id=session_id, background_tasks=background_tasks)
        logger.info(f"decode cache coords reset hit: {session_id}")


maskdecoder = MaskDecoder(
    decode_url=DECODE_URL
)