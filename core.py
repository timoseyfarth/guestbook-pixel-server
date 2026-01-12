import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from database import create_db_and_tables
from routes import router
from logger import setup_logger

EXTERNAL_ORIGIN = os.getenv("EXTERNAL_ORIGIN", "")

logger = setup_logger()

app_kwargs = {
    "title": "Github Guestbook API",
    "version": "0.1.0",
    "docs_url": None,
    "redoc_url": None,
    "openapi_url": None
}

app = FastAPI(**app_kwargs)

# CORS configuration
origins = [
    "http://localhost:5173",
    EXTERNAL_ORIGIN,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["POST", "GET", "PUT", "OPTIONS"],
    allow_headers=["*"],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status {response.status_code} for {request.method} {request.url}")
    return response


app.include_router(router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}

create_db_and_tables()
logger.info("Database initialized")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8001)