# Changelog

## v0.1.0
- MVP stack: API (FastAPI), worker (Celery), observability (Prometheus/Grafana/Exporters/cAdvisor), reverse proxy (Nginx)
- Hardening DX: LF normalization via .gitattributes, .env.example + .gitignore
- Safety: pre-commit hook blocks UTF-8 BOM; fix script available

### Commits
1b31b60 chore: initial commit 974327a chore: enforce LF via gitattributes d9af2e0 chore: stop tracking .env; add .env.example 1656bdc chore: normalize line endings (LF) and avoid BOM 4f700e1 chore: add editorconfig (utf-8, lf) c940ebb chore: add pre-commit hook to block UTF-8 BOM 47c4a04 chore: add script to remove UTF-8 BOM from config files 9d29b4d chore: pre-commit suggests fix-bom script 9ec4c9b chore: remove UTF-8 BOM from configs d020cbb (HEAD -> master, tag: v0.1.0) chore: enforce LF for scripts and configs