"""
Role-based Access Control Configuration
"""

# Role hierarchy (higher number = more privileges)
ROLE_HIERARCHY = {
    'master': 8,
    'admin': 7,
    'manager': 6,
    'moderator': 5,
    'teacher': 4,
    'accountant': 3,
    'student': 2,
    'user': 1
}

# Valid roles list
VALID_ROLES = list(ROLE_HIERARCHY.keys())

# Permissions mapping: endpoint -> minimum required role
PERMISSIONS = {
    # Auth endpoints (public)
    'POST:/auth/register': None,
    'POST:/auth/register-master': None,  # Requires secret key
    'POST:/auth/verify': None,
    'POST:/auth/login': None,
    'POST:/auth/refresh': None,
    
    # Auth endpoints (authenticated)
    'POST:/auth/logout': 'user',  # Any authenticated user
    'GET:/auth/me': 'user',
    'PUT:/auth/me': 'user',
    
    # User management endpoints
    'GET:/users': 'admin',  # List all users
    'GET:/users/:id': 'admin',  # Get specific user
    'PUT:/users/:id/role': 'admin',  # Change user role
    'DELETE:/users/:id': 'master',  # Delete user (master only)
}

def has_permission(user_role: str, required_role: str) -> bool:
    """
    Check if user_role has permission for required_role
    Returns True if user_role is equal to or higher than required_role
    """
    if required_role is None:
        return True
    
    user_level = ROLE_HIERARCHY.get(user_role, 0)
    required_level = ROLE_HIERARCHY.get(required_role, 0)
    
    return user_level >= required_level

def can_modify_role(modifier_role: str, target_role: str, new_role: str) -> bool:
    """
    Check if modifier can change target's role to new_role
    Rules:
    - Master can modify anyone
    - Admin can modify anyone except master
    - Cannot promote someone to a role higher than or equal to your own
    """
    modifier_level = ROLE_HIERARCHY.get(modifier_role, 0)
    target_level = ROLE_HIERARCHY.get(target_role, 0)
    new_level = ROLE_HIERARCHY.get(new_role, 0)
    
    # Master can do anything
    if modifier_role == 'master':
        return True
    
    # Cannot modify master users
    if target_role == 'master':
        return False
    
    # Cannot promote to master (only master can do that)
    if new_role == 'master':
        return False
    
    # Can only modify users below your level
    if target_level >= modifier_level:
        return False
    
    # Cannot promote to your level or higher
    if new_level >= modifier_level:
        return False
    
    return True
