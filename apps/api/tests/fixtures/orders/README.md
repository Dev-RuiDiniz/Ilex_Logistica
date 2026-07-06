# Fixtures sanitizadas de pedidos

`generate_fixtures.py` produz pares CSV/XLSX determinísticos de 10, 1.000 e 10.000 linhas. Os dados são inteiramente fictícios e exercitam o contrato da SPEC-12 sem fórmulas ou conteúdo ativo.

Execute `python apps/api/tests/fixtures/orders/generate_fixtures.py` na raiz quando os artefatos precisarem ser regenerados. Os arquivos versionados permitem repetir os gates funcional e de desempenho sem depender de dados externos.
