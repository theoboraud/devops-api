# devops-api (FastAPI + Prometheus)

A small “DevOps-ready” Python API:
- Health/readiness endpoints for Kubernetes probes
- /metrics endpoint compatible with Prometheus
- Easy to run locally and with Docker

## Endpoints
- GET / : app info (name/version)
- GET /healthz : liveness
- GET /readyz : readiness
- GET /metrics : Prometheus metrics
- GET /docs : Swagger UI

---

## Requirements
- Python 3.12+
- (Optional) Docker Desktop

---

## Run locally (Windows PowerShell)

### 1) Create and activate a virtual environment

    py -m venv .venv
    .\.venv\Scripts\Activate.ps1

If PowerShell blocks script execution:

    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

### 2) Install dependencies

    pip install -r requirements.txt

### 3) Start the API

    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload

---

## Quick tests

### PowerShell

    Invoke-RestMethod http://127.0.0.1:8000/healthz
    Invoke-RestMethod http://127.0.0.1:8000/readyz

### Prometheus metrics

    (Invoke-WebRequest -UseBasicParsing http://127.0.0.1:8000/metrics).Content | Select-Object -First 20

### Browser
- http://127.0.0.1:8000/healthz
- http://127.0.0.1:8000/readyz
- http://127.0.0.1:8000/docs

---

## Tests

    pytest -q

---

## Docker

### Build

    docker build -t devops-api:local .

### Run

    docker run --rm -p 8000:8000 devops-api:local

### Test

    Invoke-RestMethod http://127.0.0.1:8000/healthz

---

## Environment variables (optional)
- APP_NAME (default: devops-api)
- APP_VERSION (default: 0.1.0)
- LOG_LEVEL (default: INFO)

Example:

    $env:APP_NAME="devops-api"
    $env:APP_VERSION="0.1.0"
    python -m uvicorn app.main:app --host 127.0.0.1 --port 8000

---

## Kubernetes probes (snippet)

    livenessProbe:
      httpGet:
        path: /healthz
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10

    readinessProbe:
      httpGet:
        path: /readyz
        port: 8000
      initialDelaySeconds: 5
      periodSeconds: 10
