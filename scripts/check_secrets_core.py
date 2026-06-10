#!/usr/bin/env python3
"""
Secret scan - lógica real de verificação de secrets
"""

import argparse
import re
import sys
from pathlib import Path


# Allowlist segura
ALLOWLIST = [
    "fake",
    "test",
    "example",
    "ilex.test",
    "changeme",
    "dummy",
    "placeholder",
    "FakePassword123!",
    "fake-jwt-token-for-e2e-tests",
    "fake-jwt-token",
    "fake-refresh-token",
    "localhost",
    "127.0.0.1",
    "os.",  # código Python
    "environ",  # código Python
]

# Denylist forte
DENYLIST = [
    (r"-----BEGIN\s+(RSA\s+)?PRIVATE\s+KEY-----", "private key real"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub token real"),
    (r"Bearer\s+[a-zA-Z0-9]{30,}", "Bearer token real"),
    (r"DATABASE_URL\s*=\s*postgres://[^f][^a][^k][^e]", "DATABASE_URL real"),
    (r"SMTP_PASSWORD\s*=\s*[^f][^a][^k][^e]", "SMTP password real"),
    (r"password\s*=\s*[^f][^a][^k][^e][^t][^e][^x][^a][^m][^p][^l][^e][^c][^h][^a][^n][^g][^e][^m][^e]", "senha hardcoded"),
    (r"refresh_token\s*=\s*[^f][^a][^k][^e]", "refresh token real"),
    (r"authorization\s*=\s*Bearer\s+[a-zA-Z0-9]{30,}", "authorization header real"),
    (r"AWS_ACCESS_KEY_ID\s*=\s*AKIA[0-9A-Z]{16}", "AWS access key"),
]

# Diretórios a ignorar
IGNORE_DIRS = {
    "node_modules",
    ".next",
    ".git",
    "__pycache__",
    ".pytest_cache",
    "venv",
    ".venv",
    "htmlcov",
    "coverage",
    "playwright-report",
    "test-results",
    ".self_test_temp",
}

# Arquivos a ignorar
IGNORE_FILES = {
    ".pyc",
    ".pyo",
    ".pyd",
    ".db",
    ".sqlite",
    ".sqlite3",
    ".log",
}

# Exceções para scripts de teste
SCRIPT_EXCEPTIONS = {
    "check_secrets.py",
    "check_secrets.sh",
    "check_secrets.ps1",
    "check_secrets_core.py",  # self-test usa este arquivo
    "validate_docs.py",  # contains secret patterns for validation
}

# Arquivos a ignorar
IGNORE_FILE_NAMES = {
    ".env.example",
}


def is_ignored(path):
    """Verifica se o caminho deve ser ignorado."""
    for part in path.parts:
        if part in IGNORE_DIRS:
            return True
        if part.startswith("."):
            return True
    for ext in IGNORE_FILES:
        if path.name.endswith(ext):
            return True
    if path.name in IGNORE_FILE_NAMES:
        return True
    return False


def check_secrets_in_file(file_path):
    """Verifica secrets em um arquivo."""
    issues = []
    
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except:
        return issues
    
    # Verificar se é um script de teste (exceção)
    if file_path.name in SCRIPT_EXCEPTIONS:
        return issues
    
    for pattern, rule_name in DENYLIST:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line_num = content[:match.start()].count("\n") + 1
            line_content = content.split("\n")[line_num - 1].strip()
            
            # Verificar se está na allowlist
            is_allowed = False
            for allowed in ALLOWLIST:
                if allowed.lower() in line_content.lower():
                    is_allowed = True
                    break
            
            if not is_allowed:
                value = match.group()[:20] + "..." if len(match.group()) > 20 else match.group()
                issues.append({
                    "file": str(file_path.relative_to(args.repo_root)),
                    "line": line_num,
                    "rule": rule_name,
                    "value": value,
                })
    
    return issues


def main():
    parser = argparse.ArgumentParser(description="Secret scan")
    parser.add_argument("--repo-root", required=True, help="Root do repositório")
    parser.add_argument("--self-test", action="store_true", help="Executar self-test")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    args = parser.parse_args()
    
    repo_root = Path(args.repo_root)
    
    if args.self_test:
        # Self-test real
        print("Self-test started")
        
        # Criar diretório temporário para self-test
        temp_dir = repo_root / ".self_test_temp"
        temp_dir.mkdir(exist_ok=True)
        
        try:
            # Cenário A: fake permitido (deve passar)
            print("  Testing fake allowed values...")
            fake_file = temp_dir / "fake_allowed.txt"
            fake_file.write_text("fake-jwt-token-for-e2e-tests\nFakePassword123!\nexample\nchangeme")
            issues = check_secrets_in_file(fake_file)
            fake_file.unlink()
            
            if issues:
                print("  FAIL: Fake values were detected incorrectly")
                for issue in issues:
                    print(f"    {issue['file']}:{issue['line']} - {issue['rule']}: {issue['value']}")
                return 1
            print("  OK: Fake values allowed")
            
            # Cenário B: secret simulado bloqueante (deve falhar)
            print("  Testing blocked secrets...")
            secret_file = temp_dir / "secret_blocked.txt"
            secret_file.write_text("-----BEGIN PRIVATE KEY-----\n")  # Private key pattern
            issues = check_secrets_in_file(secret_file)
            secret_file.unlink()
            
            if not issues:
                print("  FAIL: Simulated secret was not detected")
                return 1
            print("  OK: Simulated secret detected")
            
            print("Self-test completed successfully")
            return 0
        finally:
            # Cenário C: cleanup
            if temp_dir.exists():
                import shutil
                shutil.rmtree(temp_dir)
    
    if args.debug:
        print(f"Scanning repo: {repo_root}")
    
    all_issues = []
    
    for file_path in repo_root.rglob("*"):
        if not file_path.is_file():
            continue
        if is_ignored(file_path):
            continue
        
        issues = check_secrets_in_file(file_path)
        all_issues.extend(issues)
    
    if all_issues:
        print(f"Found {len(all_issues)} potential secrets:")
        for issue in all_issues:
            print(f"  {issue['file']}:{issue['line']} - {issue['rule']}: {issue['value']}")
        return 1
    
    print("OK: No potential secrets found")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secret scan")
    parser.add_argument("--repo-root", required=True, help="Root do repositório")
    parser.add_argument("--self-test", action="store_true", help="Executar self-test")
    parser.add_argument("--debug", action="store_true", help="Modo debug")
    args = parser.parse_args()
    sys.exit(main())
