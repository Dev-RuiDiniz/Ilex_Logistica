"""Seed demo data for local presentation."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.base import Base
from app.database.session import engine, SessionLocal
from app.core.security import hash_password
from app.modules.users.models import Role, User
from app.modules.users.seed_permissions import seed_role_permissions
from app.modules.carriers.models import Carrier
from app.modules.sla.models import SlaRule
from app.modules.shipments.models import Shipment
from datetime import datetime, timedelta


def run_seed():
    print("Criando tabelas...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    if db.query(User).filter(User.email == "admin@ilex.com").first():
        print("Banco ja possui dados de demo. Pulando seed.")
        db.close()
        return

    print("Criando roles...")
    for role_name in ["admin", "logistica", "gestor", "auditoria", "manager", "operator", "viewer"]:
        db.add(Role(name=role_name))
    db.commit()

    print("Criando permissoes...")
    seed_role_permissions(db)

    print("Criando usuarios demo...")
    users_data = [
        ("admin@ilex.com", "Administrador", "123456", ["admin"]),
        ("logistica@ilex.com", "Usuario Logistica", "123456", ["logistica"]),
        ("gestor@ilex.com", "Gestor", "123456", ["gestor"]),
        ("auditoria@ilex.com", "Auditoria", "123456", ["auditoria"]),
    ]
    for email, full_name, password, roles in users_data:
        user = User(
            email=email,
            full_name=full_name,
            password_hash=hash_password(password),
            is_active=True,
        )
        db.add(user)
        db.commit()
        for role_name in roles:
            role = db.query(Role).filter(Role.name == role_name).first()
            if role:
                user.roles.append(role)
        db.commit()
        print(f"  Usuario: {email} / {password} - roles: {roles}")

    print("Criando transportadoras demo...")
    carriers_data = ["Braspress", "Jadlog", "Correios", "Total Express"]
    carriers = []
    for name in carriers_data:
        carrier = Carrier(name=name, is_active=True)
        db.add(carrier)
        db.commit()
        db.refresh(carrier)
        carriers.append(carrier)
        print(f"  Transportadora: {name}")

    print("Criando regras SLA demo...")
    sla_rules_data = [
        (carriers[0].id, 5, 3, 7),
        (carriers[1].id, 7, 5, 10),
        (carriers[2].id, 10, 7, 15),
    ]
    for carrier_id, transit_days, warning, critical in sla_rules_data:
        rule = SlaRule(
            carrier_id=carrier_id,
            transit_days=transit_days,
            warning_threshold_days=warning,
            critical_delay_days=critical,
            is_active=True,
        )
        db.add(rule)
    db.commit()
    print(f"  {len(sla_rules_data)} regras SLA criadas")

    print("Criando shipments demo...")
    today = datetime.now()
    shipments_data = [
        ("BRP001", "in_transit", carriers[0].id, today + timedelta(days=2), "normal", "Cliente Alpha", "SP", 1500.00, "NF001", 1500.00, 150.00),
        ("BRP002", "in_transit", carriers[0].id, today - timedelta(days=3), "alta", "Cliente Beta", "RJ", 2800.00, "NF002", 2800.00, 280.00),
        ("JAD001", "delivered", carriers[1].id, today - timedelta(days=1), "normal", "Cliente Gamma", "MG", 950.00, "NF003", 950.00, 95.00),
        ("JAD002", "pending", carriers[1].id, today + timedelta(days=5), "media", "Cliente Delta", "PR", 3200.00, "NF004", 3200.00, 320.00),
        ("COR001", "in_transit", carriers[2].id, today - timedelta(days=8), "alta", "Cliente Epsilon", "RS", 5100.00, "NF005", 5100.00, 510.00),
        ("COR002", "delivered", carriers[2].id, today - timedelta(days=2), "normal", "Cliente Zeta", "SC", 1800.00, "NF006", 1800.00, 180.00),
        ("TOT001", "in_transit", carriers[3].id, today + timedelta(days=1), "baixa", "Cliente Eta", "BA", 750.00, "NF007", 750.00, 75.00),
        ("TOT002", "failed", carriers[3].id, today - timedelta(days=5), "alta", "Cliente Theta", "PE", 4200.00, "NF008", 4200.00, 420.00),
        ("BRP003", "pending", carriers[0].id, today + timedelta(days=4), "media", "Cliente Iota", "SP", 2200.00, "NF009", 2200.00, 220.00),
        ("JAD003", "in_transit", carriers[1].id, today - timedelta(days=6), "alta", "Cliente Kappa", "RJ", 3100.00, "NF010", 3100.00, 310.00),
    ]
    for tracking, status, carrier_id, est_delivery, criticality, customer, uf, amount, inv_num, inv_val, freight_val in shipments_data:
        shipment = Shipment(
            tracking_code=tracking,
            status=status,
            carrier_id=carrier_id,
            estimated_delivery=est_delivery,
            criticality=criticality,
            customer_name=customer,
            destination_uf=uf,
            amount=amount,
            invoice_number=inv_num,
            invoice_value=inv_val,
            freight_value=freight_val,
            due_date=est_delivery + timedelta(days=30),
            recipient_name=customer,
            recipient_phone="(11) 99999-9999",
            origin_address="Rua Origem, 100 - Sao Paulo, SP",
            destination_address=f"Rua Destino, 200 - {uf}",
        )
        db.add(shipment)
    db.commit()
    print(f"  {len(shipments_data)} shipments criados")

    db.close()
    print("\n" + "=" * 50)
    print("SEED CONCLUIDO!")
    print("=" * 50)
    print("ACESSOS DE DEMO:")
    print("  admin@ilex.com      / 123456  (Administrador)")
    print("  logistica@ilex.com  / 123456  (Logistica)")
    print("  gestor@ilex.com     / 123456  (Gestor)")
    print("  auditoria@ilex.com  / 123456  (Auditoria)")
    print("=" * 50)


if __name__ == "__main__":
    run_seed()
