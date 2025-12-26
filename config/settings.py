"""
Application Configuration
"""
import os
from typing import Optional

class Config:
    # AWS Configuration
    AWS_REGION: str = os.getenv('AWS_REGION', 'eu-north-1')
    TABLE_PREFIX: str = os.getenv('DYNAMODB_TABLE_PREFIX', 'dev')
    
    # Table Names
    USERS_TABLE: str = f"{TABLE_PREFIX}_users"
    REFRESH_TOKENS_TABLE: str = f"{TABLE_PREFIX}_refresh_tokens"
    VERIFICATION_CODES_TABLE: str = f"{TABLE_PREFIX}_verification_codes"
    LOGIN_ATTEMPTS_TABLE: str = f"{TABLE_PREFIX}_login_attempts"
    RATE_LIMITS_TABLE: str = f"{TABLE_PREFIX}_rate_limits"
    
    # JWT Configuration
    JWT_SECRET: str = os.getenv('JWT_SECRET', 'change-this-secret-key')
    REFRESH_TOKEN_SECRET: str = os.getenv('REFRESH_TOKEN_SECRET', 'change-this-refresh-secret')
    ACCESS_TOKEN_EXPIRY: int = int(os.getenv('ACCESS_TOKEN_EXPIRY', '1800'))  # 30 minutes
    REFRESH_TOKEN_EXPIRY: int = int(os.getenv('REFRESH_TOKEN_EXPIRY', '2592000'))  # 30 days
    
    # Master Secret
    MASTER_SECRET_KEY: str = os.getenv('MASTER_SECRET_KEY')
    
    # Verification
    VERIFICATION_CODE_EXPIRY: int = int(os.getenv('VERIFICATION_CODE_EXPIRY', '600'))  # 10 minutes
    
    # Rate Limiting
    LOGIN_RATE_LIMIT: int = int(os.getenv('LOGIN_RATE_LIMIT', '10'))  # per hour
    REGISTER_RATE_LIMIT: int = int(os.getenv('REGISTER_RATE_LIMIT', '100'))  # per hour per IP
    API_RATE_LIMIT: int = int(os.getenv('API_RATE_LIMIT', '100'))  # per minute per user
    MAX_FAILED_LOGIN_ATTEMPTS: int = int(os.getenv('MAX_FAILED_LOGIN_ATTEMPTS', '5'))
    
    # Password Requirements
    MIN_PASSWORD_LENGTH: int = 4
    
    # Email/SMS (for future use)
    EMAIL_FROM: Optional[str] = os.getenv('EMAIL_FROM')
    SMS_SENDER_ID: Optional[str] = os.getenv('SMS_SENDER_ID')

config = Config()
