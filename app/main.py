from fastapi import FastAPI, HTTPException, Query
import time

from prometheus_client import make_asgi_app

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from app.fibonacci import calculate_fibonacci
from app.models import FibonacciResponse
from app.logger import logger
from app.telemetry import configure_telemetry
from app.observability import RequestLoggingMiddleware

from app.metrics import (
    fibonacci_requests_total,
    fibonacci_current_requests,
    fibonacci_last_input,
    fibonacci_largest_input,
    fibonacci_last_result,
    fibonacci_request_duration,
)

# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="Fibonacci API",
    description="REST API to calculate nth Fibonacci number",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# --------------------------------------------------
# OpenTelemetry
# --------------------------------------------------

configure_telemetry()
FastAPIInstrumentor.instrument_app(app)

# --------------------------------------------------
# Middleware
# --------------------------------------------------

app.add_middleware(RequestLoggingMiddleware)

# --------------------------------------------------
# Prometheus Metrics Endpoint
# --------------------------------------------------

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# --------------------------------------------------
# Home
# --------------------------------------------------

@app.get("/", tags=["Home"])
def home():
    return {
        "application": "Fibonacci API",
        "version": "1.0.0",
        "status": "Running",
    }


# --------------------------------------------------
# Fibonacci Endpoint
# --------------------------------------------------

@app.get(
    "/fibonacci",
    response_model=FibonacciResponse,
    tags=["Fibonacci"],
    summary="Calculate nth Fibonacci Number",
)
def get_fibonacci(
    n: int = Query(
        ...,
        ge=0,
        description="Position in Fibonacci sequence"
    )
):

    fibonacci_current_requests.inc()

    start_time = time.time()

    logger.info(f"Calculating Fibonacci for n={n}")

    try:

        # --------------------------------------------------
        # Artificial latency (Demo)
        # --------------------------------------------------

        if n >= 45:
            time.sleep(2)

        elif n >= 40:
            time.sleep(1)

        elif n >= 35:
            time.sleep(0.5)

        # --------------------------------------------------
        # Business Logic
        # --------------------------------------------------

        value = calculate_fibonacci(n)

        duration = time.time() - start_time

        # --------------------------------------------------
        # Prometheus Business Metrics
        # --------------------------------------------------

        fibonacci_requests_total.labels(
            status="success",
            code="200"
        ).inc()

        fibonacci_last_input.set(n)

        fibonacci_last_result.set(value)

        fibonacci_request_duration.observe(duration)

        if n > fibonacci_largest_input._value.get():
            fibonacci_largest_input.set(n)

        logger.info(
            f"Completed Fibonacci calculation "
            f"n={n}, value={value}, duration={duration:.3f}s"
        )

        return FibonacciResponse(
            n=n,
            value=value,
        )

    except ValueError as ex:

        fibonacci_requests_total.labels(
            status="error",
            code="400"
        ).inc()

        logger.exception(str(ex))

        raise HTTPException(
            status_code=400,
            detail=str(ex),
        )

    except Exception as ex:

        fibonacci_requests_total.labels(
            status="error",
            code="500"
        ).inc()

        logger.exception(str(ex))

        raise HTTPException(
            status_code=500,
            detail="Internal Server Error",
        )

    finally:

        fibonacci_current_requests.dec()


# --------------------------------------------------
# Health Endpoints
# --------------------------------------------------

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "UP"
    }


@app.get("/ready", tags=["Health"])
def readiness():
    return {
        "status": "READY"
    }


@app.get("/live", tags=["Health"])
def liveness():
    return {
        "status": "ALIVE"
    }