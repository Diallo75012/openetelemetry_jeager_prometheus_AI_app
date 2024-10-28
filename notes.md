# OPEN TELEMETRY

## Components
- Receiver: A Receiver is the interface that allows the OpenTelemetry Collector to receive telemetry data from your application. 
  Receivers collect data from multiple different protocols (e.g., OTLP, Jaeger, Prometheus, etc.).
  They serve as the entry point for data into the Collector.
- Collector: an agent that runs within your infrastructure and gathers observability data from your applications
- Propagator: traces from different microservices to form a coherent view of an entire request's journey. 
  Propagators typically work with HTTP headers, gRPC metadata, or similar communication mechanisms.
- Exporter: responsible for sending telemetry data to the backend of your choice. 
  This backend could be Prometheus for metrics or Jaeger for traces. 
  The Exporter pushes the collected and processed data to external services for visualization and analysis.

## What is Observability?
- traces + metrics + logs

## Scenario Workflow
A simple distributed system consisting of a frontend service and a backend service. 
The frontend makes requests to the backend service, and you want to collect telemetry to understand system performance and behavior. 

Here's how OpenTelemetry integrates into this system:

1. **Application Instrumentation:**
First, instrument your frontend and backend applications with OpenTelemetry SDK.
The OpenTelemetry SDK will generate trace and metric data for important operations (e.g., handling requests).
The Propagator will propagate the trace context from the frontend to the backend so that you can correlate the spans across services.

2. **Collector:**
Deploy the OpenTelemetry Collector as part of your infrastructure. 
It will receive the telemetry data from the frontend and backend services through the Receivers.
The Collector might process the data (e.g., filtering or aggregating) before exporting it.

3. **Exporters:**
Use the Collector to export the telemetry data to Prometheus and/or Jaeger.
Prometheus receives metrics data, while Jaeger receives traces.

4. **Visualization with Grafana:**
Finally, use Grafana to visualize the telemetry data.

Grafana can pull metrics from Prometheus to create dashboards, and you can use the Jaeger plugin in Grafana to visualize the distributed traces.

## ASCII Diagram
```code
+---------------------+        +---------------------+        +---------------------+
|  Frontend Service   |        |   Backend Service   |        |   OpenTelemetry     |
| (Instrumented App)  |        | (Instrumented App)  |        |      Collector      |
+---------+-----------+        +----------+----------+        +---------+-----------+
          |                           |                            |             
          | Trace Context Propagation |                            | Receives Data 
          +-------------------------->|                            |  from Frontend and Backend 
          |                           |                            |
          |   Generate Traces/Metrics |                            |
          +-------------------------->+                            |
                                      |                            |
                                      +                            v
                                      +----------------------->+---------+
                                                               | Exporter |
                                                               +-----+----+
                                                                     |
                                                   +-----------------+-----------------+
                                                   |                                   |
                                      +------------v----------+             +----------v------------+
                                      |        Prometheus     |             |       Jaeger           |
                                      |    (Metrics Storage)  |             |  (Tracing Backend)     |
                                      +------------+----------+             +----------+------------+
                                                   |                                   |
                                         +---------v---------+                    +----v-----+
                                         |     Grafana       |                    |  Grafana  |
                                         |   (Dashboard)     |                    |  (Traces) |
                                         +-------------------+                    +----------+

```

## installation:
```python
pip install opentelemetry-sdk opentelemetry-instrumentation
```

- opentelemetry-sdk: The core SDK to create and manage traces.
- opentelemetry-instrumentation: Provides tools for automatically instrumenting your Python code.
- opentelemetry-exporter-console: An exporter that allows you to see the trace output in your console.


## Summary of the Existing Integration
- Instrumentation:
We added OpenTelemetry tracing to a Python backend.
The function llm_call_with_telemetry() starts a span before calling the LLM API. This span records telemetry data about the request, like its start and end times, status, and additional custom attributes.

- Exporter to Console:
We used ConsoleSpanExporter, which prints trace details to the console. This is good for basic testing but isn’t practical for production use.

- Tracing Example:
When calling the API with the question, the trace included details like the request time, status, and a custom attribute (llm.api.response_length).
The result included a joke, an informative text, and a follow-up question, showing the LLM's response while tracing each step for analysis.

```bash
python3 app.py 
How can I help You Today? What is the biggest capital city in Asia?
System message: 
 ('system', "Answer to user query.\n- Put your answer in this schema:\n{\n'query': <The user initial query>,\n'joke': <a small joke about the subject of the query>,\n'text': <answer user query>,\n'question': <ask to the user a question to create an interaction like a conversation and be pertinent>\n}\nAnswer only with the schema in markdown between ```markdown ```.") 
Human message:  ('human', 'What is the biggest capital city in Asia?')
Messages before llm call:  [('system', "Answer to user query.\n- Put your answer in this schema:\n{\n'query': <The user initial query>,\n'joke': <a small joke about the subject of the query>,\n'text': <answer user query>,\n'question': <ask to the user a question to create an interaction like a conversation and be pertinent>\n}\nAnswer only with the schema in markdown between ```markdown ```."), ('human', 'What is the biggest capital city in Asia?')]
{
    "name": "call_llm_api",
    "context": {
        "trace_id": "0x70bff61c9438c76c506ed08b53df5812",
        "span_id": "0x5ae3af1fe3c0fa6d",
        "trace_state": "[]"
    },
    "kind": "SpanKind.INTERNAL",
    "parent_id": null,
    "start_time": "2024-10-28T22:37:07.277369Z",
    "end_time": "2024-10-28T22:37:08.259473Z",
    "status": {
        "status_code": "UNSET"
    },
    "attributes": {
        "llm.api.url": "<eample url of api: http://groq.api/v2/chat/completion/stuff>",
        "llm.api.response_length": 457
    },
    "events": [],
    "links": [],
    "resource": {
        "attributes": {
            "telemetry.sdk.language": "python",
            "telemetry.sdk.name": "opentelemetry",
            "telemetry.sdk.version": "1.27.0",
            "service.name": "unknown_service"
        },
        "schema_url": ""
    }
}
{
'query': 'What is the biggest capital city in Asia?',
'joke': 'Why did the capital city get a ticket? Because it was driving too Tokyo-drift!',
'text': 'The biggest capital city in Asia by land area is Beijing, the capital of China. It spans over 16,800 square kilometers, making it the largest capital city in the world!',
'question': 'Did you know that Beijing is also home to the largest public square in the world? It’s called the Tiananmen Square!'
}

```

# Step-by-Step Tutorial: Adding Prometheus or Jaeger Exporters

## Step 1: Install Necessary Packages

To integrate with Jaeger or Prometheus, you'll need to install their respective OpenTelemetry exporters:
```bash
pip install opentelemetry-exporter-jaeger opentelemetry-exporter-prometheus
```

opentelemetry-exporter-jaeger: Sends trace data to Jaeger for viewing distributed traces.
opentelemetry-exporter-prometheus: Sends metrics data to Prometheus.

## Step 2: Add Exporters in Your Code

Modify the OpenTelemetry setup in app.py to use the new exporters.
Here is how you could modify the existing code to add Jaeger and Prometheus.
Jaeger Integration (for Distributed Tracing)
```python
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Step 1: Set up Jaeger Exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",  # Jaeger agent hostname
    agent_port=6831,  # Default UDP port for Jaeger agent
)

# Step 2: Use BatchSpanProcessor for better performance in production
jaeger_span_processor = BatchSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(jaeger_span_processor)
```

Prometheus Integration (for Metrics)
```python
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from prometheus_client import start_http_server

# Step 1: Set up Prometheus Exporter
prometheus_exporter = PrometheusMetricsExporter()
metric_reader = PeriodicExportingMetricReader(prometheus_exporter)

# Step 2: Set up Meter Provider with Prometheus Metrics Exporter
meter_provider = MeterProvider(metric_readers=[metric_reader])

# Step 3: Start Prometheus Metrics HTTP server (accessible at localhost:8000/metrics)
start_http_server(port=8000)
```
Full Integration in app.py
Integrate both Prometheus and Jaeger into your existing code as follows:
```python
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.exporter.prometheus import PrometheusMetricsExporter
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from prometheus_client import start_http_server

# Step 1: Set up the TracerProvider
trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()

# Step 2: Set up the Jaeger Exporter
jaeger_exporter = JaegerExporter(
    agent_host_name="localhost",
    agent_port=6831,
)
jaeger_span_processor = BatchSpanProcessor(jaeger_exporter)
tracer_provider.add_span_processor(jaeger_span_processor)

# Step 3: Set up Prometheus Metrics Exporter
prometheus_exporter = PrometheusMetricsExporter()
metric_reader = PeriodicExportingMetricReader(prometheus_exporter)
meter_provider = MeterProvider(metric_readers=[metric_reader])

# Start Prometheus Metrics HTTP server (for metrics visualization)
start_http_server(port=8000)

# Step 4: Create a Tracer
tracer = trace.get_tracer(__name__)

# Rest of your llm_call_with_telemetry code...
```

## How to Use Jaeger and Prometheus

### **Jaeger:**

Run a Jaeger instance using Docker:
```bash
docker run -d --name jaeger -e COLLECTOR_ZIPKIN_HTTP_PORT=9411 -p 5775:5775/udp -p 6831:6831/udp -p 6832:6832/udp -p 5778:5778 -p 16686:16686 -p 14268:14268 -p 14250:14250 -p 9411:9411 jaegertracing/all-in-one:latest
```
Access Jaeger UI at http://localhost:16686. You can view the traces and understand the flow of requests across different services.

### **Prometheus:**

Run Prometheus using Docker:
```bash
docker run -p 9090:9090 prom/prometheus
```
Configure Prometheus to scrape the metrics endpoint (localhost:8000/metrics).
Access Prometheus UI at http://localhost:9090. You can set alerts and monitor metrics in real-time.

### **Grafana (Optional):**
Grafana can be used to visualize data from both Prometheus (metrics) and Jaeger (traces) for better insights.

## Why This is Important for SREs

- **Better Observability:**
Tracing (Jaeger): Helps you understand the end-to-end flow of requests in distributed systems. This is particularly useful for identifying bottlenecks and improving system reliability.
Metrics (Prometheus): Real-time metrics help in understanding system performance (e.g., latency, throughput).

- **Quick Troubleshooting:**
With distributed tracing, you can identify which microservice is causing a failure, helping SREs quickly resolve incidents.

- **Scalable Monitoring:**
Adding metrics and tracing with OpenTelemetry is scalable, enabling standardized observability across diverse microservices.

- **Standardization:**
OpenTelemetry is becoming the industry standard for instrumentation. Using it makes your infrastructure and observability stack future-proof and easier to integrate with multiple observability tools.
