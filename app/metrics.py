from prometheus_client import Counter, Gauge, Histogram

# --------------------------------------------------
# Total Requests
# --------------------------------------------------

fibonacci_requests_total = Counter(
    "fibonacci_requests_total",
    "Total Fibonacci requests",
    ["status", "code"]
)

# --------------------------------------------------
# Active Requests
# --------------------------------------------------

fibonacci_current_requests = Gauge(
    "fibonacci_current_requests",
    "Current active Fibonacci requests"
)

# --------------------------------------------------
# Last Input
# --------------------------------------------------

fibonacci_last_input = Gauge(
    "fibonacci_last_input",
    "Last Fibonacci input received"
)

# --------------------------------------------------
# Largest Input
# --------------------------------------------------

fibonacci_largest_input = Gauge(
    "fibonacci_largest_input",
    "Largest Fibonacci input received"
)

# --------------------------------------------------
# Request Duration
# --------------------------------------------------

fibonacci_request_duration = Histogram(
    "fibonacci_request_duration_seconds",
    "Time spent processing Fibonacci requests",
    buckets=(
        0.005,
        0.01,
        0.025,
        0.05,
        0.1,
        0.25,
        0.5,
        1,
        2,
        5,
        10,
    ),
)

# --------------------------------------------------
# Fibonacci Value Generated
# --------------------------------------------------

fibonacci_last_result = Gauge(
    "fibonacci_last_result",
    "Last Fibonacci number calculated"
)