import time
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .utils.custom_logger import CustomLogger
logger = CustomLogger(__name__).logger

def register_middleware(app: FastAPI):
    
    @app.middleware("http")
    async def custom_logging(request: Request, call_next):
        start_time = time.perf_counter()
        
        response = await call_next(request)
        
        client_ip = request.client.host
        client_port = request.client.port
        method = request.method
        path = request.url.path
        status_code = response.status_code
        
        if status_code < 400:
            processing_time = time.perf_counter() - start_time
            message = f"Client: {client_ip}:{client_port} | Method {method} | Path: {path} | Status: {status_code} | Time: completed after {processing_time:.5f}s"
            logger.info(message)
            
        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
    
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1", "0.0.0.0", "calm-goshawk-pleasantly.ngrok-free.app"]
    )