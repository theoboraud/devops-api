import os
import time
import logging
from fastapi import FastAPI, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest, Counter, Histogram

APP_NAME = os.getenv("APP_NAME", "devops-api")
APP_VERSION = os.getenv("APP_VERSION", "0.1.0")

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(APP_NAME)

app = FastAPI(title=APP_NAME, version=APP_VERSION)

REQUESTS = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "path", "status"],
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency (seconds)",
    ["path"],
)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    path = request.url.path
    LATENCY.labels(path=path).observe(duration)
    REQUESTS.labels(
        method=request.method,
        path=path,
        status=str(response.status_code),
    ).inc()
    return response

@app.get("/")
def root():
    return {"name": APP_NAME, "version": APP_VERSION}

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.get("/readyz")
def readyz():
    # Pour plus tard: check DB/queue/etc. Ici, on est toujours prêt.
    return {"status": "ready"}

@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)
