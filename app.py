from flask import Flask, jsonify, Response
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

app = Flask(__name__)

provider = TracerProvider(resource=Resource.create({}))
trace.set_tracer_provider(provider)
exporter = OTLPSpanExporter()  # Usa variables de entorno OTEL_*
provider.add_span_processor(BatchSpanProcessor(exporter))
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

CLICK_COUNT = 0

@app.get("/")
def index() -> Response:
    return Response("""<!doctype html>
<html><head><meta charset="utf-8"><title>Hola Botón</title></head>
<body>
  <h1>Hola Botón</h1>
  <button id="btn">Decir "Hola mundo"</button>
  <p id="out"></p>
  <script>
    const btn = document.getElementById('btn'); const out = document.getElementById('out');
    btn.onclick = async () => { const r = await fetch('/api/hola'); const j = await r.json();
      out.textContent = `Servidor: ${j.mensaje} (clicks=${j.clicks})`; };
  </script>
</body></html>""", mimetype="text/html")

@app.get("/api/hola")
def hola():
    global CLICK_COUNT
    CLICK_COUNT += 1
    return jsonify({"mensaje": "Hola mundo", "clicks": CLICK_COUNT})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
