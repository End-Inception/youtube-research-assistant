
from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="YouTube AI Research Assistant",
    description="A RAG-powered YouTube research application",
    version="1.0.0"
)

app.include_router(
    router,
    tags=["Research"]
)


@app.get("/")
def root():

    return {
        "message": "YouTube AI Research Assistant API is running!"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }
