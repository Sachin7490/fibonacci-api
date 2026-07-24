from fastapi import FastAPI, HTTPException, Query

from app.fibonacci import calculate_fibonacci
from app.models import FibonacciResponse
from app.logger import logger
from app.telemetry import configure_telemetry
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from app.observability import RequestLoggingMiddleware

app = FastAPI(
    title="Fibonacci API",
    description="REST API to calculate the nth Fibonacci number.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(RequestLoggingMiddleware)
configure_telemetry()
FastAPIInstrumentor.instrument_app(app)


@app.get("/", tags=["Home"])
def home():
    """
    Root endpoint.
    """
    #logger.info("Home endpoint accessed")

    return {
        "application": "Fibonacci API",
        "version": "1.0.0",
        "status": "Running"
    }


@app.get(
    "/fibonacci",
    response_model=FibonacciResponse,
    tags=["Fibonacci"],
    summary="Calculate nth Fibonacci number"
)
def get_fibonacci(
        n: int = Query(
            ...,
            ge=0,
            description="Position in Fibonacci sequence (must be >= 0)"
        )
):
    """
    Returns the nth Fibonacci number.

    Example:
        /fibonacci?n=10
    """

    #logger.info(f"Received Fibonacci request for n={n}")

    try:
        value = calculate_fibonacci(n)

        #logger.info(f"Returning Fibonacci value={value}")

        return FibonacciResponse(
            n=n,
            value=value
        )

    except ValueError as ex:
        logger.error(str(ex))
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )


@app.get("/health", tags=["Health"])
def health():
    """
    Health endpoint.
    Used to determine whether the service is healthy.
    """
    return {
        "status": "UP"
    }


@app.get("/ready", tags=["Health"])
def readiness():
    """
    Readiness endpoint.
    Used by Kubernetes readiness probe.
    """
    return {
        "status": "READY"
    }


@app.get("/live", tags=["Health"])
def liveness():
    """
    Liveness endpoint.
    Used by Kubernetes liveness probe.
    """
    return {
        "status": "ALIVE"
    }