## Release v0.1.0

**What’s included**
- FastAPI API + /health + /metrics
- Celery worker + Flower
- Prometheus + Grafana + exporters + cAdvisor
- Nginx reverse proxy (web) on :8088

**Quickstart**
- Copy .env.example to .env
- docker compose up -d --build
- API: http://localhost:8000/docs
- Proxy: http://localhost:8088/health
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)
- Flower: http://localhost:5555

**Notes**
- Repo enforces LF and blocks UTF-8 BOM in config files.
- If a commit is blocked: powershell -ExecutionPolicy Bypass -File .\scripts\fix-bom.ps1
"@
[System.IO.File]::WriteAllText((Join-Path (Get-Location) "RELEASE_NOTES.md"), , (New-Object System.Text.UTF8Encoding(False)))

git add RELEASE_NOTES.md
git commit -m "docs: add release notes for v0.1.0"

# 4) Retag v0.1.0 para que apunte al commit final (changelog + notes)
git tag -d v0.1.0
git tag -a v0.1.0 -m "v0.1.0 - MVP (API + worker + observability + nginx proxy)"

# 5) Conecta remoto GitHub (pega tu URL)
# Ejemplo: https://github.com/<user>/edulabops.git
 = "https://github.com/TU_USUARIO/edulabops.git"
git remote add origin 

# 6) Push rama + tags
git push -u origin master
git push origin --tags "@