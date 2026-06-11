#!/usr/bin/env python3
"""
Script auxiliar para preparar PRs pendentes de forma automatizada.

Este script é seguro por padrão (dry-run) e só executa comandos se:
1. --execute for especificado
2. gh auth status estiver OK
3. Nunca faz merge
4. Nunca habilita auto-merge
5. Nunca usa force push
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, dry_run=True):
    """Executa comando se dry_run=False, senão imprime."""
    if dry_run:
        print(f"[DRY-RUN] {cmd}")
        return True
    else:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"[OK] {cmd}")
                return True
            else:
                print(f"[FAIL] {cmd}")
                print(f"  Error: {result.stderr}")
                return False
        except Exception as e:
            print(f"[ERROR] {cmd}")
            print(f"  Exception: {e}")
            return False

def check_gh_auth():
    """Verifica se gh auth status está OK."""
    result = subprocess.run("gh auth status", shell=True, capture_output=True, text=True)
    return result.returncode == 0

def check_branch_exists(branch):
    """Verifica se branch existe no remoto."""
    result = subprocess.run(f"git ls-remote --heads origin {branch}", shell=True, capture_output=True, text=True)
    return result.returncode == 0 and result.stdout.strip()

def main():
    dry_run = "--execute" not in sys.argv
    
    print("=" * 60)
    print("BETA-021C — Preparação Automatizada de PRs Pendentes")
    print("=" * 60)
    
    if dry_run:
        print("[MODE] DRY-RUN (nenhum comando será executado)")
        print("[INFO] Use --execute para executar comandos reais")
    else:
        print("[MODE] EXECUTE (comandos serão executados)")
        if not check_gh_auth():
            print("[ERROR] gh auth status não está OK")
            print("[INFO] Execute: gh auth login")
            sys.exit(1)
    
    print()
    
    # Definição dos PRs pendentes
    prs = [
        {
            "name": "BETA-020A",
            "title": "[BETA-020A] Segurança e RBAC Backend/API",
            "base": "main",
            "head": "feature/beta-020a-security-rbac-backend-api",
            "body_file": "docs/prs/BETA_020A_PR_BODY.md",
            "comment_file": "docs/prs/BETA_020A_FINAL_COMMENT.md",
            "pr_exists": True  # PR #39 já existe
        },
        {
            "name": "BETA-020B",
            "title": "[BETA-020B] RBAC Backend para Endpoints Operacionais Restantes",
            "base": "feature/beta-020a-security-rbac-backend-api",
            "head": "feature/beta-020b-rbac-operational-endpoints-backend",
            "body_file": "docs/prs/BETA_020B_PR_BODY.md",
            "comment_file": "docs/prs/BETA_020B_FINAL_COMMENT.md",
            "pr_exists": True  # PR #40 já existe
        },
        {
            "name": "BETA-020C",
            "title": "[BETA-020C] Frontend de Segurança e RBAC",
            "base": "feature/beta-020b-rbac-operational-endpoints-backend",
            "head": "feature/beta-020c-security-rbac-frontend",
            "body_file": "docs/prs/BETA_020C_PR_BODY.md",
            "comment_file": "docs/prs/BETA_020C_FINAL_COMMENT.md",
            "pr_exists": True  # PR #41 já existe
        },
        {
            "name": "BETA-021A",
            "title": "[BETA-021A] QA/CI/CD Final e Readiness Beta",
            "base": "feature/beta-020c-security-rbac-frontend",
            "head": "feature/beta-021a-qa-ci-cd-beta-readiness",
            "body_file": "docs/prs/BETA_021A_PR_BODY.md",
            "comment_file": "docs/prs/BETA_021A_FINAL_COMMENT.md",
            "pr_exists": False  # PR não existe por bloqueio técnico
        },
        {
            "name": "BETA-021B",
            "title": "[BETA-021B] Auditoria Final de Integração e Release Candidate",
            "base": "feature/beta-021a-qa-ci-cd-beta-readiness",
            "head": "feature/beta-021b-final-integration-release-candidate",
            "body_file": "docs/prs/BETA_021B_PR_BODY.md",
            "comment_file": "docs/prs/BETA_021B_FINAL_COMMENT.md",
            "pr_exists": False  # PR não existe por bloqueio técnico
        },
    ]
    
    # Verificar branches
    print("[STEP 1] Verificando branches no remoto...")
    for pr in prs:
        if check_branch_exists(pr["head"]):
            print(f"  [OK] {pr['head']}")
        else:
            print(f"  [FAIL] {pr['head']} (não encontrado)")
    
    print()
    
    # Gerar comandos de criação de PR
    print("[STEP 2] Comandos de criação de PR (Draft)...")
    for pr in prs:
        if not pr["pr_exists"]:
            body_path = Path(pr["body_file"])
            if body_path.exists():
                body_content = body_path.read_text(encoding="utf-8")
                cmd = f'gh pr create --base "{pr["base"]}" --head "{pr["head"]}" --title "{pr["title"]}" --body-file "{pr["body_file"]}" --draft'
                run_command(cmd, dry_run)
            else:
                print(f"  [SKIP] {pr['name']}: body file não encontrado ({pr['body_file']})")
        else:
            print(f"  [SKIP] {pr['name']}: PR já existe")
    
    print()
    
    # Gerar comandos de comentário final
    print("[STEP 3] Comandos de comentário final...")
    for pr in prs:
        comment_path = Path(pr["comment_file"])
        if comment_path.exists():
            cmd = f'gh pr comment {pr["head"]} --body-file "{pr["comment_file"]}"'
            run_command(cmd, dry_run)
        else:
            print(f"  [SKIP] {pr['name']}: comment file não encontrado ({pr['comment_file']})")
    
    print()
    print("=" * 60)
    print("[INFO] Para executar comandos reais, use:")
    print("  python scripts/prepare_pending_prs.py --execute")
    print("[INFO] Certifique-se de que gh auth status está OK")
    print("=" * 60)

if __name__ == "__main__":
    main()
