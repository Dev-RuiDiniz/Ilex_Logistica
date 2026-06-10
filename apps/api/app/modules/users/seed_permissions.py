"""Seed permissions for RBAC roles."""

from sqlalchemy.orm import Session

from app.modules.users.models import Role, Permission


def seed_role_permissions(db: Session) -> None:
    """Seed permissions for beta roles."""
    
    # Create permissions if they don't exist
    permission_names = [
        ("shipments:read", "Read shipments", "shipments", "read"),
        ("shipments:write", "Write shipments", "shipments", "write"),
        ("imports:read", "Read imports", "imports", "read"),
        ("imports:write", "Write imports", "imports", "write"),
        ("sla:read", "Read SLA rules", "sla", "read"),
        ("sla:write", "Write SLA rules", "sla", "write"),
        ("alerts:read", "Read alerts", "alerts", "read"),
        ("alerts:write", "Write alerts", "alerts", "write"),
        ("reports:read", "Read reports", "reports", "read"),
        ("reports:write", "Write reports", "reports", "write"),
        ("audit:read", "Read audit logs", "audit", "read"),
        ("users:read", "Read users", "users", "read"),
        ("users:write", "Write users", "users", "write"),
    ]
    
    for name, description, resource, action in permission_names:
        existing = db.query(Permission).filter(Permission.name == name).first()
        if not existing:
            perm = Permission(name=name, description=description, resource=resource, action=action)
            db.add(perm)
    db.commit()
    
    # Get all permissions
    permissions = db.query(Permission).all()
    perm_map = {p.name: p for p in permissions}
    
    # Define role permissions matrix
    role_permissions_map = {
        "admin": list(perm_map.values()),  # Admin has all permissions
        "manager": [
            perm_map["shipments:read"],
            perm_map["imports:read"],
            perm_map["sla:read"],
            perm_map["alerts:read"],
            perm_map["alerts:write"],
            perm_map["reports:read"],
            perm_map["reports:write"],
            perm_map["audit:read"],
        ],
        "operator": [
            perm_map["shipments:read"],
            perm_map["shipments:write"],
            perm_map["imports:read"],
            perm_map["imports:write"],
            perm_map["alerts:read"],
            perm_map["alerts:write"],
        ],
        "viewer": [
            perm_map["shipments:read"],
            perm_map["imports:read"],
            perm_map["sla:read"],
            perm_map["alerts:read"],
            perm_map["reports:read"],
        ],
        "logistica": [
            perm_map["shipments:read"],
            perm_map["shipments:write"],
            perm_map["imports:read"],
            perm_map["imports:write"],
        ],
        "gestor": [
            perm_map["shipments:read"],
            perm_map["imports:read"],
            perm_map["sla:read"],
            perm_map["alerts:read"],
            perm_map["reports:read"],
        ],
        "auditoria": [
            perm_map["audit:read"],
            perm_map["shipments:read"],
            perm_map["imports:read"],
        ],
    }
    
    # Assign permissions to roles
    for role_name, permissions_list in role_permissions_map.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if role:
            role.permissions = permissions_list
    
    db.commit()
