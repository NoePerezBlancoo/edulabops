# EduLabOps

**Laboratorio reproducible de backend, workers y observabilidad** construido para practicar una arquitectura de operaciones moderna alrededor de FastAPI, Celery, PostgreSQL, Redis, Prometheus y Grafana.

El repositorio empaqueta API, procesamiento asíncrono, persistencia, reverse proxy y monitorización en un único entorno Docker Compose, de forma que toda la plataforma pueda levantarse y analizarse localmente.

## Arquitectura

```text
                +------------------+
                |   Nginx / Web    |
                +---------+--------+
                          |
                          v
                   +------+------+
                   |   FastAPI   |
                   +------+------+ 
                          |
              +-----------+-----------+
              |                       |
              v                       v
        PostgreSQL                  Redis
                                      |
                                      v
                                Celery Worker
                                      |
                                      v
                                   Flower

Observabilidad:
Prometheus <- API / cAdvisor / Redis Exporter / PostgreSQL Exporter
     |
     v
  Grafana
```

## Servicios incluidos

- **FastAPI** como API principal.
- **PostgreSQL 16** para persistencia.
- **Redis 7** como infraestructura de mensajería.
- **Celery worker** para ejecución asíncrona.
- **Flower** para inspección de tareas.
- **Nginx** como capa web/reverse proxy.
- **Prometheus** para recolección de métricas.
- **Grafana** para visualización.
- **cAdvisor** para métricas de contenedores.
- Exporters específicos para PostgreSQL y Redis.

## Qué demuestra

- Orquestación de múltiples servicios con Docker Compose.
- Healthchecks y dependencias entre servicios.
- Separación entre API y procesamiento asíncrono.
- Métricas de aplicación, infraestructura y base de datos.
- Observabilidad reproducible en entorno local.
- Configuración mediante variables de entorno.
- Uso de componentes habituales en arquitecturas backend y DevOps.

## Puesta en marcha

```bash
cp .env.example .env
docker compose up -d --build
```

Servicios principales:

```text
API / OpenAPI     http://localhost:8000/docs
Web / Proxy       http://localhost:8088
Flower            http://localhost:5555
Prometheus        http://localhost:9090
Grafana           http://localhost:3001
cAdvisor          http://localhost:8081
```

> Las credenciales y valores de ejemplo son únicamente para laboratorio local. Revísalos antes de reutilizar esta arquitectura fuera de un entorno de desarrollo.

## Stack

`Python` · `FastAPI` · `Celery` · `PostgreSQL` · `Redis` · `Nginx` · `Prometheus` · `Grafana` · `Docker Compose`

## Enfoque

EduLabOps no pretende ser un producto SaaS terminado. Es un **laboratorio técnico** para entender cómo se conectan una API, workers, almacenamiento, colas, métricas y herramientas de operación en una arquitectura distribuida pequeña pero observable.

## Autor

**Noé Pérez Blanco**  
IT Lead · Full-Stack Developer · Industrial Software · SaaS & Automation

[GitHub](https://github.com/NoePerezBlancoo) · [Portfolio](https://portfolio-noe-zeta.vercel.app/) · [LinkedIn](https://www.linkedin.com/in/no%C3%A9-p%C3%A9rez-blanco-b79228187/)