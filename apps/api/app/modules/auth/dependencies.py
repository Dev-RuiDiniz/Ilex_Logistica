from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from app.core.security import decode_token
from app.database.session import get_db
from app.modules.users.models import User

auth_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(auth_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="nao autenticado")
    try:
        payload = decode_token(credentials.credentials)
    except InvalidTokenError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalido") from exc
    if payload.get("type") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalido")

    user = db.get(User, int(payload["sub"]))
    if user is None or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="usuario inativo")
    if payload.get("ver", 0) != user.token_version:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token revogado")
    return user


def require_roles(*allowed: str):
    def checker(user: User = Depends(get_current_user)) -> User:
        role_names = [role.name for role in user.roles]
        if any(role_name in allowed for role_name in role_names):
            return user
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="sem permissao")

    return checker


def require_permission(permission: str):
    """Require a specific permission for the user.
    
    Args:
        permission: Permission string in format "resource:action" (e.g., "audit:read")
    
    Returns:
        Dependency function that checks if user has the permission
    """
    def checker(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        # Admin role has all permissions
        if any(role.name == "admin" for role in user.roles):
            return user
        
        # Check if user has the specific permission through any role
        resource, action = permission.split(":")
        for role in user.roles:
            for perm in role.permissions:
                if perm.resource == resource and perm.action == action:
                    return user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"sem permissao: {permission}"
        )
    
    return checker


def require_any_permission(*permissions: str):
    """Require any of the specified permissions for the user.
    
    Args:
        permissions: Permission strings in format "resource:action"
    
    Returns:
        Dependency function that checks if user has any of the permissions
    """
    def checker(user: User = Depends(get_current_user), db: Session = Depends(get_db)) -> User:
        # Admin role has all permissions
        if any(role.name == "admin" for role in user.roles):
            return user
        
        # Check if user has any of the permissions through any role
        for permission in permissions:
            resource, action = permission.split(":")
            for role in user.roles:
                for perm in role.permissions:
                    if perm.resource == resource and perm.action == action:
                        return user
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"sem permissao: {', '.join(permissions)}"
        )
    
    return checker
