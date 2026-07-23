def calculate_fibonacci(n: int) -> int:
    """
    Returns the nth Fibonacci number.

    Time Complexity: O(n)
    Space Complexity: O(1)
    """

    if n < 0:
        raise ValueError("n must be greater than or equal to 0")

    if n == 0:
        return 0

    if n == 1:
        return 1

    previous = 0
    current = 1

    for _ in range(2, n + 1):
        previous, current = current, previous + current

    return current