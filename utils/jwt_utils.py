"""
JWT Token Utilities
"""
import jwt
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from config import config

def generate_access_token(user_id: str, email: str, role: str) -> str:
    """
    Generate JWT access token
    """
    payload = {
        'user_id': user_id,
        'email': email,
        'role': role,
        'type': 'access',
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=config.ACCESS_TOKEN_EXPIRY)
    }
    
    return jwt.encode(payload, config.JWT_SECRET, algorithm='HS256')


def generate_refresh_token(user_id: str) -> str:
    """
    Generate JWT refresh token
    """
    payload = {
        'user_id': user_id,
        'type': 'refresh',
        'jti': str(uuid.uuid4()),  # Unique token ID
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(seconds=config.REFRESH_TOKEN_EXPIRY)
    }
    
    return jwt.encode(payload, config.REFRESH_TOKEN_SECRET, algorithm='HS256')


def verify_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode access token
    Returns payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=['HS256'])
        
        # Verify token type
        if payload.get('type') != 'access':
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verify_refresh_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode refresh token
    Returns payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, config.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
        
        # Verify token type
        if payload.get('type') != 'refresh':
            return None
        
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def extract_token_from_header(authorization_header: Optional[str]) -> Optional[str]:
    """
    Extract token from Authorization header
    Expected format: "Bearer <token>"
    """
    if not authorization_header:
        return None
    
    parts = authorization_header.split()
    
    if len(parts) != 2 or parts[0].lower() != 'bearer':
        return None
    
    return parts[1]
