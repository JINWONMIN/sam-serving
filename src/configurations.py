import os
from logging import getLogger

from src.constants import PLATFORM_ENUM


logger = getLogger(__name__)


class PlatformConfigurations:
    platform = os.getenv("PLATFORM", PLATFORM_ENUM.DOCKER.value)
    if not PLATFORM_ENUM.has_value(platform):
        raise ValueError(f"PLATFORM must be one of {[v.value for v in PLATFORM_ENUM.__members__.values()]}")


class CacheConfigurations:
    cache_host = os.getenv("CACHE_HOST", "redis")
    cache_port = int(os.getenv("CACHE_PORT", 6379))
    queue_name = os.getenv("QUEUE_NAME", "queue")


class RedisCacheConfigurations(CacheConfigurations):
    redis_db = int(os.getenv("REDIS_DB", 0))
    redis_decode_responses = bool(os.getenv("REDIS_DECODE_RESPONSES", True))


class APIConfigurations:
    title = os.getenv("API_TITLE", "SamServing API")
    description = os.getenv("API_DESCRIPTION", "This is SAM Model Inference API")
    version = os.getenv("API_VERSION", "1.0.0")


class EncodeModelConfigurations:
    model_spec_name = os.getenv("MODEL_SPEC_NAME", "sam_vit_h_encode")
    signature_name = os.getenv("SIGNATURE_NAME", "predictions")
    address = os.getenv("API_ADDRESS", "gpu")
    rest_port = int(os.getenv("REST_API_PORT", 8080))


class DecodeModelConfigurations:
    model_spec_name = os.getenv("MODEL_SPEC_NAME", "sam_vit_h_decode")
    signature_name = os.getenv("SIGNATURE_NAME", "predictions")
    address = os.getenv("API_ADDRESS", "cpu")
    rest_port = int(os.getenv("REST_API_PORT", 7080))


logger.info(f"{PlatformConfigurations.__name__}: {PlatformConfigurations.__dict__}")
logger.info(f"{CacheConfigurations.__name__}: {CacheConfigurations.__dict__}")
logger.info(f"{RedisCacheConfigurations.__name__}: {RedisCacheConfigurations.__dict__}")
logger.info(f"{APIConfigurations.__name__}: {APIConfigurations.__dict__}")
logger.info(f"{EncodeModelConfigurations.__name__}: {EncodeModelConfigurations.__dict__}")
logger.info(f"{DecodeModelConfigurations.__name__}: {DecodeModelConfigurations.__dict__}")