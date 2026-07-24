import os

from opentelemetry import trace, metrics

from opentelemetry.sdk.resources import Resource

# ---------- Tracing ----------
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

# ---------- Metrics ----------
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter


SERVICE_NAME = os.getenv("OTEL_SERVICE_NAME", "fibonacci-api")
SERVICE_VERSION = os.getenv("OTEL_SERVICE_VERSION", "1.0.0")
DEPLOYMENT_ENV = os.getenv("DEPLOYMENT_ENV", "development")

OTEL_ENDPOINT = os.getenv(
    "OTEL_EXPORTER_OTLP_ENDPOINT",
    "http://localhost:4318"
)


def configure_telemetry():

    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.version": SERVICE_VERSION,
            "deployment.environment": DEPLOYMENT_ENV,
        }
    )

    # ----------------------------
    # Traces
    # ----------------------------

    tracer_provider = TracerProvider(resource=resource)

    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(
                endpoint=f"{OTEL_ENDPOINT}/v1/traces"
            )
        )
    )

    trace.set_tracer_provider(tracer_provider)

    # ----------------------------
    # Metrics
    # ----------------------------

    metric_exporter = OTLPMetricExporter(
        endpoint=f"{OTEL_ENDPOINT}/v1/metrics"
    )

    metric_reader = PeriodicExportingMetricReader(
        exporter=metric_exporter,
        export_interval_millis=5000,
    )

    meter_provider = MeterProvider(
        resource=resource,
        metric_readers=[metric_reader],
    )

    metrics.set_meter_provider(meter_provider)