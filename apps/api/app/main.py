from fastapi import FastAPI
from . import models, schemas
from .db import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="EduLabOps API")

from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/")
def root():
    return {"name": "EduLabOps API"}
