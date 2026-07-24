from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


SERVICE_NAME = "fibonacci-api"


def configure_telemetry():

    resource = Resource.create(
        {
            "service.name": SERVICE_NAME,
            "service.version": "1.0.0",
            "deployment.environment": "development"
        }
    )

    provider = TracerProvider(resource=resource)

    processor = BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint="http://localhost:4318/v1/traces"
        )
    )

    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)