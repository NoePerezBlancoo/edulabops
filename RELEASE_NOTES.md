# Release Notes

## v0.1.0 — Operations Lab Foundation

Primera versión funcional del laboratorio EduLabOps.

### Incluye

- API basada en FastAPI con endpoints de health y métricas.
- Worker asíncrono con Celery.
- Redis como infraestructura de mensajería.
- PostgreSQL como base de datos persistente.
- Flower para inspección del worker.
- Nginx como capa web y reverse proxy.
- Prometheus como sistema de recolección de métricas.
- Grafana para visualización.
- cAdvisor para métricas de contenedores.
- Redis Exporter y PostgreSQL Exporter.
- Orquestación completa mediante Docker Compose.

### Arranque

```bash
cp .env.example .env
docker compose up -d --build
```

### Servicios locales

- API / OpenAPI: `http://localhost:8000/docs`
- Web / Proxy: `http://localhost:8088`
- Flower: `http://localhost:5555`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3001`
- cAdvisor: `http://localhost:8081`

### Objetivo de la release

Establecer una base pequeña y reproducible para experimentar con API, procesamiento asíncrono y observabilidad sin depender de infraestructura externa.
