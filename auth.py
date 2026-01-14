import os
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from logger import logger

API_KEY_NAME = "X-API-KEY"
API_KEY_HEADER = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
SERVER_API_KEY = os.environ.get("SERVER_API_KEY")


async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)) -> str:
    """Validate API key from header"""
    if api_key_header == SERVER_API_KEY:
        return api_key_header
    else:
        logger.warning("Failed API key validation attempt")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials"
        )