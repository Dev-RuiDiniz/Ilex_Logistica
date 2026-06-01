from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_token, decode_token, verify_password
from app.modules.users.models import User


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = db.query(User).filter(User.email == email, User.is_active.is_(True)).first()
    if user is None:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user


def build_tokens(user: User) -> dict[str, str]:
    roles = [role.name for role in user.roles]
    return {
        "access_token": create_token(str(user.id), roles, settings.jwt_access_minutes, "access"),
        "refresh_token": create_token(str(user.id), roles, settings.jwt_refresh_minutes, "refresh"),
    }


def refresh_access_token(refresh_token: str) -> dict[str, str] | None:
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        return None
    return {
        "access_token": create_token(
            payload["sub"],
            payload.get("roles", []),
            settings.jwt_access_minutes,
            "access",
        ),
        "refresh_token": refresh_token,
    }
