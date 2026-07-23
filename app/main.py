from fastapi import FastAPI, HTTPException

from app.fibonacci import calculate_fibonacci
from app.models import FibonacciResponse

app = FastAPI(
    title="Fibonacci API",
    description="REST API to calculate the nth Fibonacci number",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "application": "Fibonacci API",
        "version": "1.0.0",
        "status": "Running"
    }


@app.get(
    "/fibonacci",
    response_model=FibonacciResponse,
    tags=["Fibonacci"]
)
def get_fibonacci(n: int):

    try:
        result = calculate_fibonacci(n)

        return FibonacciResponse(
            n=n,
            value=result
        )

    except ValueError as ex:
        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )