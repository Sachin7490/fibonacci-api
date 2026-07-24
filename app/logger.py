import logging
import os

from opentelemetry import trace


LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)


class TraceFormatter(logging.Formatter):

    def format(self, record):

        span = trace.get_current_span()

        span_context = span.get_span_context()

        if span_context.is_valid:

            record.trace_id = format(span_context.trace_id, "032x")

            record.span_id = format(span_context.span_id, "016x")

        else:

            record.trace_id = "-"

            record.span_id = "-"

        return super().format(record)


logger = logging.getLogger("fibonacci-api")

logger.setLevel(logging.INFO)

formatter = TraceFormatter(
    "%(asctime)s | %(levelname)s | trace=%(trace_id)s | span=%(span_id)s | %(message)s"
)

console = logging.StreamHandler()

console.setFormatter(formatter)

file_handler = logging.FileHandler(f"{LOG_DIR}/app.log")

file_handler.setFormatter(formatter)

logger.addHandler(console)

logger.addHandler(file_handler)