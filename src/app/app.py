from logging import getLogger

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.configurations import APIConfigurations
from src.app.routers.sam import routers


logger = getLogger(__name__)

app = FastAPI(
    title=APIConfigurations.title,
    description=APIConfigurations.description,
    version=APIConfigurations.version,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routers.router)
