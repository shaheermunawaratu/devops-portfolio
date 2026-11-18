from flask import Flask, Response, jsonify, render_template, request
from prometheus_client import CONTENT_TYPE_LATEST, Counter, generate_latest

REQUEST_COUNT = Counter(
    "portfolio_http_requests_total",
    "Total number of HTTP requests received by the portfolio application",
    ["method", "endpoint"],
)


def create_app():
    app = Flask(__name__)

    @app.after_request
    def record_request(response):
        if request.endpoint != "metrics":
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.endpoint or "unknown",
            ).inc()

        return response

    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/health")
    def health():
        return jsonify({"status": "healthy"}), 200

    @app.route("/metrics")
    def metrics():
        return Response(
            generate_latest(),
            content_type=CONTENT_TYPE_LATEST,
        )

    return app
