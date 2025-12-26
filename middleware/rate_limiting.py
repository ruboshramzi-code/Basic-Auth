"""
Rate Limiting Middleware
"""
from functools import wraps
from typing import Callable
from utils import RateLimitDB, rate_limit_response
from config import config

def rate_limit(limit: int, window_seconds: int, key_prefix: str = ""):
    """
    Decorator to apply rate limiting
    
    Args:
        limit: Maximum number of requests
        window_seconds: Time window in seconds
        key_prefix: Prefix for the rate limit key
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(event, context):
            # Get identifier for rate limiting
            # Use IP address for unauthenticated endpoints
            # Use user_id for authenticated endpoints
            
            user = event.get('user')
            if user:
                identifier = f"user:{user['user_id']}"
            else:
                # Get IP address from request context
                ip_address = event.get('requestContext', {}).get('identity', {}).get('sourceIp', 'unknown')
                identifier = f"ip:{ip_address}"
            
            # Create rate limit key
            rate_limit_key = f"{key_prefix}:{identifier}" if key_prefix else identifier
            
            # Check rate limit
            allowed = RateLimitDB.check_and_increment(rate_limit_key, limit, window_seconds)
            
            if not allowed:
                return rate_limit_response(
                    f"Rate limit exceeded. Maximum {limit} requests per {window_seconds} seconds."
                )
            
            return func(event, context)
        
        return wrapper
    return decorator


def login_rate_limit():
    """Rate limit for login endpoint"""
    return rate_limit(
        limit=config.LOGIN_RATE_LIMIT,
        window_seconds=3600,  # 1 hour
        key_prefix="login"
    )


def register_rate_limit():
    """Rate limit for registration endpoint"""
    return rate_limit(
        limit=config.REGISTER_RATE_LIMIT,
        window_seconds=3600,  # 1 hour
        key_prefix="register"
    )


def api_rate_limit():
    """Rate limit for general API endpoints"""
    return rate_limit(
        limit=config.API_RATE_LIMIT,
        window_seconds=60,  # 1 minute
        key_prefix="api"
    )
