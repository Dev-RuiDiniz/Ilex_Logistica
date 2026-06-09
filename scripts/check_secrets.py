#!/usr/bin/env python3
"""
Script de verificação de secrets no código (Python)
Funciona em Windows, Linux e macOS
"""

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import List, Tuple

# Allowlist de valores fake/test permitidos
ALLOWED_PATTERNS = [
    r"fake",
    r"test",
    r"example",
    r"ilex\.test",
    r"changeme",
    r"dummy",
    r"placeholder",
    r"FakePassword123!",
    r"fake-jwt-token-for-e2e-tests",
    r"fake-jwt-token",
    r"fake-refresh-token",
    r"localhost",
    r"127\.0\.0\.1",
]

# Denylist de padrões perigosos
DANGEROUS_PATTERNS = [
    (r"BEGIN\s+.*\s+PRIVATE\s+KEY", "private key"),
    (r"BEGIN\s+.*\s+RSA\s+PRIVATE\s+KEY", "RSA private key"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub token"),
    (r"ya29\.[a-zA-Z0-9_-]{100,}", "Google token"),
    (r"Bearer\s+[a-zA-Z0-9_-]{20,}", "Bearer token real"),
    (r"DATABASE_URL\s*=\s*['\"][^'\"]*postgres", "DATABASE_URL real"),
    (r"SMTP.*password", "SMTP password"),
    (r"refresh_token\s*=\s*['\"][^'\"]{20,}", "refresh token real"),
    (r"authorization:\s*bearer\s+[a-zA-Z0-9_-]{20,}", "authorization header real"),
]

# Diretórios a excluir
EXCLUDE_DIRS = [
    ".git",
    "node_modules",
    ".next",
    "playwright-report",
    "test-results",
    "coverage",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "scripts",
]

# Extensões de arquivos para escanear
SCAN_EXTENSIONS = {".ts", ".tsx", ".js", ".jsx", ".py", ".yml", ".yaml", ".sh", ".ps1", ".md"}


def is_allowed(line: str) -> bool:
    """Verifica se uma linha contém apenas valores permitidos."""
    for pattern in ALLOWED_PATTERNS:
        if re.search(pattern, line, re.IGNORECASE):
            return True
    return False


def should_exclude_file(file_path: Path) -> bool:
    """Verifica se um arquivo deve ser excluído do scan."""
    # Excluir por diretório
    for dir_name in EXCLUDE_DIRS:
        if dir_name in file_path.parts:
            return True
    
    # Excluir por extensão
    if file_path.suffix not in SCAN_EXTENSIONS:
        return True
    
    # Excluir arquivos de teste/fixtures/mocks
    if any(keyword in file_path.name.lower() for keyword in ["test", "spec", "fixture", "mock"]):
        return True
    
    # Excluir arquivos de exemplo
    if "example" in file_path.name.lower() or "sample" in file_path.name.lower():
        return True
    
    return False


def mask_value(value: str, max_len: int = 20) -> str:
    """Mascara um valor sensível."""
    if len(value) <= 8:
        return "***"
    return f"{value[:4]}...{value[-4:]}"


def scan_file(file_path: Path) -> List[Tuple[int, str, str]]:
    """Escaneia um arquivo em busca de secrets."""
    findings = []
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return findings
    
    for line_num, line in enumerate(lines, 1):
        for pattern, rule_name in DANGEROUS_PATTERNS:
            if re.search(pattern, line, re.IGNORECASE):
                if not is_allowed(line):
                    masked = mask_value(line.strip(), max_len=30)
                    findings.append((line_num, rule_name, masked))
    
    return findings


def run_self_test(repo_root: Path) -> bool:
    """Executa testes controlados do secret scan."""
    print("Running self-test of secret scan...")
    
    # Teste 1: fake token permitido deve passar
    print("  Test 1: fake token allowed should pass")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, dir=repo_root) as f:
        f.write("FAKE_TOKEN = 'fake-jwt-token-for-e2e-tests'\n")
        fake_file = f.name
    
    try:
        findings = scan_file(Path(fake_file))
        if findings:
            print(f"    FAIL: fake token was blocked incorrectly")
            return False
        print(f"    PASS")
    finally:
        os.unlink(fake_file)
    
    # Teste 2: secret simulado realista deve falhar
    print("  Test 2: simulated realistic secret should fail")
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, dir=repo_root) as f:
        f.write("SECRET_TOKEN = 'ya29.a0AfH6SMBxL8Kq9aZ1bY2cX3dW4eV5fG6hI7jK8lM9nO0pQ1rS2tU3vW4xY5z'\n")
        secret_file = f.name
    
    try:
        findings = scan_file(Path(secret_file))
        if not findings:
            print(f"    FAIL: simulated secret was not detected")
            return False
        print(f"    PASS")
    finally:
        os.unlink(secret_file)
    
    print("Self-test completed successfully")
    return True


def main():
    parser = argparse.ArgumentParser(description="Secret scan for repository")
    parser.add_argument("--repo-root", type=str, help="Repository root")
    parser.add_argument("--debug", action="store_true", help="Debug mode with diagnostics")
    parser.add_argument("--self-test", action="store_true", help="Run controlled tests")
    args = parser.parse_args()
    
    # Resolver repo root
    if args.repo_root:
        repo_root = Path(args.repo_root).resolve()
    else:
        # Fallback: usar diretório do script
        script_dir = Path(__file__).parent.resolve()
        repo_root = script_dir.parent.resolve()
    
    # Mudar para repo root
    os.chdir(repo_root)
    
    if args.debug:
        print("Secret Scan Diagnostics")
        print(f"  System: {os.name}")
        print(f"  Python: {sys.version}")
        print(f"  Repo root: {repo_root}")
        print(f"  Current directory: {os.getcwd()}")
    
    # Executar self-test se solicitado
    if args.self_test:
        if not run_self_test(repo_root):
            sys.exit(1)
        sys.exit(0)
    
    # Verificar arquivos .env
    if args.debug:
        print("Checking .env files...")
    
    env_files = list(repo_root.glob(".env"))
    env_files = [f for f in env_files if not f.name.endswith(".example") and not f.name.endswith(".sample")]
    
    if env_files:
        for env_file in env_files:
            print(f"ERROR: .env file found: {env_file}")
            print("   Should be in .gitignore or use .env.example")
        sys.exit(1)
    
    if args.debug:
        print("  OK: No real .env file found")
    
    # Escanear arquivos
    if args.debug:
        print("Scanning code files...")
    
    total_files = 0
    scanned_files = 0
    all_findings = []
    
    for file_path in repo_root.rglob("*"):
        if not file_path.is_file():
            continue
        
        total_files += 1
        
        if should_exclude_file(file_path):
            continue
        
        scanned_files += 1
        findings = scan_file(file_path)
        if findings:
            all_findings.append((file_path, findings))
    
    if args.debug:
        print(f"  Total files: {total_files}")
        print(f"  Scanned files: {scanned_files}")
        print(f"  Ignored directories: {', '.join(EXCLUDE_DIRS)}")
        print(f"  Findings: {len(all_findings)}")
    
    # Imprimir achados
    if all_findings:
        print(f"ERROR: {len(all_findings)} potential secrets found:")
        for file_path, findings in all_findings:
            relative_path = file_path.relative_to(repo_root)
            for line_num, rule_name, masked in findings:
                print(f"  File: {relative_path}:{line_num}")
                print(f"  Rule: {rule_name}")
                print(f"  Masked value: {masked}")
                print()
        print("Please review and remove real secrets from code")
        sys.exit(1)
    
    print("OK: No potential secrets found")
    sys.exit(0)


if __name__ == "__main__":
    main()
