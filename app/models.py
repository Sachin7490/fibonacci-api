from pydantic import BaseModel


class FibonacciResponse(BaseModel):
    n: int
    value: int