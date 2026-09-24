from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Dict
import time

class RateLimiter:
    """
    A basic in-memory token bucket rate limiter to protect the API.
    In production, this connects to Redis.
    """
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.clients: Dict[str, list] = {}

    def is_rate_limited(self, ip_address: str) -> bool:
        current_time = time.time()
        
        if ip_address not in self.clients:
            self.clients[ip_address] = [current_time]
            return False
            
        # Remove timestamps older than 60 seconds
        self.clients[ip_address] = [t for t in self.clients[ip_address] if current_time - t < 60]
        
        if len(self.clients[ip_address]) >= self.requests_per_minute:
            return True
            
        self.clients[ip_address].append(current_time)
        return False

# Global instance
limiter = RateLimiter(requests_per_minute=20) # Stricter for AI endpoints

async def rate_limit_middleware(request: Request):
    """
    Dependency to inject into FastAPI routes.
    """
    client_ip = request.client.host if request.client else "unknown"
    if limiter.is_rate_limited(client_ip):
        raise HTTPException(
            status_code=429, 
            detail="Too many requests. Please try again later."
        )
