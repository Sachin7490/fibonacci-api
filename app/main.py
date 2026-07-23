from fastapi import FastAPI

app = FastAPI(
    title="Fibonacci API",
    description="REST API to calculate the nth Fibonacci number",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Fibonacci API"
    }