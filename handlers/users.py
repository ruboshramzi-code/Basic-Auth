"""
User Management Handlers (Admin/Master)
"""
import json
from datetime import datetime
from config import can_modify_role
from utils import (
    UserDB,
    validate_role,
    success_response,
    error_response,
    not_found_response,
    forbidden_response,
    validation_error_response
)
from middleware import require_auth, get_current_user

@require_auth(required_role='admin')
def list_users(event, context):
    """
    GET /users
    List all users (admin+)
    """
    try:
        # Get query parameters for pagination (optional)
        query_params = event.get('queryStringParameters') or {}
        limit = int(query_params.get('limit', 100))
        
        # Get users
        users = UserDB.list_users(limit=limit)
        
        # Remove sensitive data
        users_response = []
        for user in users:
            users_response.append({
                'user_id': user['user_id'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'phone': user.get('phone', ''),
                'role': user['role'],
                'is_verified': user.get('is_verified', False),
                'is_locked': user.get('is_locked', False),
                'created_at': user.get('created_at')
            })
        
        return success_response(
            data={
                'users': users_response,
                'count': len(users_response)
            }
        )
        
    except Exception as e:
        print(f"List users error: {str(e)}")
        return error_response("Failed to list users", status_code=500)


@require_auth(required_role='admin')
def get_user(event, context):
    """
    GET /users/:id
    Get specific user (admin+)
    """
    try:
        user_id = event['pathParameters']['id']
        
        # Get user
        user = UserDB.get_user_by_id(user_id)
        
        if not user:
            return not_found_response("User not found")
        
        # Remove sensitive data
        user_response = {
            'user_id': user['user_id'],
            'email': user['email'],
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'phone': user.get('phone', ''),
            'role': user['role'],
            'is_verified': user.get('is_verified', False),
            'is_locked': user.get('is_locked', False),
            'email_verified': user.get('email_verified', False),
            'phone_verified': user.get('phone_verified', False),
            'failed_login_attempts': user.get('failed_login_attempts', 0),
            'created_at': user.get('created_at'),
            'updated_at': user.get('updated_at')
        }
        
        return success_response(data=user_response)
        
    except Exception as e:
        print(f"Get user error: {str(e)}")
        return error_response("Failed to get user", status_code=500)


@require_auth(required_role='admin')
def update_user_role(event, context):
    """
    PUT /users/:id/role
    Update user role (admin/master)
    """
    try:
        current_user = get_current_user(event)
        user_id = event['pathParameters']['id']
        body = json.loads(event.get('body', '{}'))
        
        new_role = body.get('role')
        
        # Validate role
        is_valid, error = validate_role(new_role)
        if not is_valid:
            return validation_error_response(error)
        
        # Get target user
        target_user = UserDB.get_user_by_id(user_id)
        if not target_user:
            return not_found_response("User not found")
        
        # Check if current user can modify target user's role
        can_modify = can_modify_role(
            current_user['role'],
            target_user['role'],
            new_role
        )
        
        if not can_modify:
            return forbidden_response(
                "You don't have permission to change this user's role to the specified role"
            )
        
        # Update role
        updates = {
            'role': new_role,
            'updated_at': datetime.utcnow().isoformat()
        }
        
        updated_user = UserDB.update_user(user_id, updates)
        
        return success_response(
            data={
                'user_id': updated_user['user_id'],
                'email': updated_user['email'],
                'role': updated_user['role'],
                'updated_at': updated_user['updated_at']
            },
            message=f"User role updated to {new_role}"
        )
        
    except json.JSONDecodeError:
        return error_response("Invalid JSON in request body")
    except Exception as e:
        print(f"Update role error: {str(e)}")
        return error_response("Failed to update user role", status_code=500)


@require_auth(required_role='master')
def delete_user(event, context):
    """
    DELETE /users/:id
    Delete user (master only)
    """
    try:
        current_user = get_current_user(event)
        user_id = event['pathParameters']['id']
        
        # Prevent self-deletion
        if user_id == current_user['user_id']:
            return error_response("Cannot delete your own account")
        
        # Get target user
        target_user = UserDB.get_user_by_id(user_id)
        if not target_user:
            return not_found_response("User not found")
        
        # Delete user
        UserDB.delete_user(user_id)
        
        # Also delete associated refresh tokens
        from utils import RefreshTokenDB
        RefreshTokenDB.delete_user_tokens(user_id)
        
        return success_response(
            message="User deleted successfully"
        )
        
    except Exception as e:
        print(f"Delete user error: {str(e)}")
        return error_response("Failed to delete user", status_code=500)
