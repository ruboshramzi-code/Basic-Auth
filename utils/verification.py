"""
Verification Code Utilities
"""
import random
from datetime import datetime, timedelta
from config import config

def generate_verification_code(length: int = 6) -> str:
    """
    Generate a random numeric verification code
    """
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])


def send_email_verification(email: str, code: str) -> bool:
    """
    Send email verification code
    For now, just log to console (testing mode)
    TODO: Implement AWS SES integration
    """
    print(f"\n{'='*60}")
    print(f"📧 EMAIL VERIFICATION CODE")
    print(f"{'='*60}")
    print(f"To: {email}")
    print(f"Code: {code}")
    print(f"Expires: {config.VERIFICATION_CODE_EXPIRY // 60} minutes")
    print(f"{'='*60}\n")
    
    return True


def send_sms_verification(phone: str, code: str) -> bool:
    """
    Send SMS verification code
    For now, just log to console (testing mode)
    TODO: Implement AWS SNS integration
    """
    print(f"\n{'='*60}")
    print(f"📱 SMS VERIFICATION CODE")
    print(f"{'='*60}")
    print(f"To: {phone}")
    print(f"Code: {code}")
    print(f"Expires: {config.VERIFICATION_CODE_EXPIRY // 60} minutes")
    print(f"{'='*60}\n")
    
    return True


def create_verification_record(user_id: str, code_type: str) -> dict:
    """
    Create a verification code record
    Returns dict with code and expiry
    """
    code = generate_verification_code()
    expires_at = datetime.utcnow() + timedelta(seconds=config.VERIFICATION_CODE_EXPIRY)
    
    return {
        'user_id': user_id,
        'code_type': code_type,  # 'email' or 'sms'
        'code': code,
        'created_at': datetime.utcnow().isoformat(),
        'expires_at': expires_at.isoformat()
    }
