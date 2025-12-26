"""
Response Utilities
"""
from typing import Any, Dict, Optional

def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Dict:
    """
    Create a success response
    """
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': {
            'success': True,
            'message': message,
            'data': data
        }
    }


def error_response(message: str, status_code: int = 400, error_code: Optional[str] = None) -> Dict:
    """
    Create an error response
    """
    body = {
        'success': False,
        'message': message
    }
    
    if error_code:
        body['error_code'] = error_code
    
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type,Authorization',
            'Access-Control-Allow-Methods': 'GET,POST,PUT,DELETE,OPTIONS'
        },
        'body': body
    }


def unauthorized_response(message: str = "Unauthorized") -> Dict:
    """
    Create an unauthorized (401) response
    """
    return error_response(message, status_code=401, error_code='UNAUTHORIZED')


def forbidden_response(message: str = "Forbidden") -> Dict:
    """
    Create a forbidden (403) response
    """
    return error_response(message, status_code=403, error_code='FORBIDDEN')


def not_found_response(message: str = "Not found") -> Dict:
    """
    Create a not found (404) response
    """
    return error_response(message, status_code=404, error_code='NOT_FOUND')


def rate_limit_response(message: str = "Rate limit exceeded") -> Dict:
    """
    Create a rate limit (429) response
    """
    return error_response(message, status_code=429, error_code='RATE_LIMIT_EXCEEDED')


def validation_error_response(message: str, errors: Optional[Dict] = None) -> Dict:
    """
    Create a validation error (422) response
    """
    response = error_response(message, status_code=422, error_code='VALIDATION_ERROR')
    if errors:
        response['body']['errors'] = errors
    return response
