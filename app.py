from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.trace import set_tracer_provider
import requests
from langchain_groq import ChatGroq
from llms import (
  groq_llm_mixtral_7b,
  groq_llm_llama3_8b,
  groq_llm_llama3_8b_tool_use,
  groq_llm_llama3_70b,
  groq_llm_llama3_70b_tool_use,
  groq_llm_gemma_7b,
)
from prompts import llm_call_api_prompt
from call_llm import call_llm_api
from dotenv import load_dotenv
from typing import Dict


# load env vars
load_dotenv(dotenv_path='.env', override=False)

# Step 1: Set up the TracerProvider
trace.set_tracer_provider(TracerProvider())
tracer_provider = trace.get_tracer_provider()

# Step 2: Set up a Console Exporter (outputs to stdout)
console_exporter = ConsoleSpanExporter() # this could be replaced by jeagearExporter or prometheusExporter
span_processor = SimpleSpanProcessor(console_exporter) # can use BatchSpanProcessor() for higher performance
tracer_provider.add_span_processor(span_processor)

# Step 3: Create a Tracer
tracer = trace.get_tracer(__name__)

# Sample backend function calling an LLM API
def llm_call_with_telemetry(llm: ChatGroq, query: str, prompt: Dict):
  # Create a span for the LLM API call
  with tracer.start_as_current_span("call_llm_api") as span:
    try:
      # Example API request to an LLM endpoint
      response = call_llm_api(llm, query, prompt)

      # Adding attributes to the span to store useful data
      span.set_attribute("llm.api.url", "<eample url of api: http://groq.api/v2/chat/completion/stuff>")
      span.set_attribute("llm.api.response_length", len(response))

      return response
    except requests.exceptions.RequestException as e:
      # Record exception in the span
      span.record_exception(e)
      span.set_status(trace.Status(trace.StatusCode.ERROR, description=str(e)))
      raise

# Example usage
if __name__ == "__main__":
  query = input("How can I help You Today? ").strip()
  try:
    result = llm_call_with_telemetry(groq_llm_mixtral_7b, query , llm_call_api_prompt)
    print(result)
  except Exception as e:
    print(f"Error occurred: {e}")
