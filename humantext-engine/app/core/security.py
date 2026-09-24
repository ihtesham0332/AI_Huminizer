from fastapi import Request, HTTPException
import time

# Basic In-Memory Rate Limiter (For Production, this would be Redis)
RATE_LIMIT_DB = {}
MAX_REQUESTS_PER_MINUTE = 50

async def rate_limit_middleware(request: Request):
    """
    Production Hardening: Protects the LLM Endpoints from cost exhaustion.
    """
    client_ip = request.client.host
    current_time = time.time()
    
    if client_ip not in RATE_LIMIT_DB:
        RATE_LIMIT_DB[client_ip] = []
        
    # Clean old requests
    RATE_LIMIT_DB[client_ip] = [req_time for req_time in RATE_LIMIT_DB[client_ip] if current_time - req_time < 60]
    
    if len(RATE_LIMIT_DB[client_ip]) >= MAX_REQUESTS_PER_MINUTE:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Try again in a minute.")
        
    RATE_LIMIT_DB[client_ip].append(current_time)
