
from app import create_app


def test_homepage_returns_success():
    app = create_app()
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"Shaheer Munawar" in response.data


def test_health_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "healthy"}


def test_metrics_endpoint():
    app = create_app()
    client = app.test_client()

    response = client.get("/metrics")

    assert response.status_code == 200
    assert b"portfolio_http_requests_total" in response.data
