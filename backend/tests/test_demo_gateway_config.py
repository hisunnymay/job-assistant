from pathlib import Path


def test_demo_gateway_allows_the_bounded_two_attempt_ai_workflow() -> None:
    repository_root = Path(__file__).resolve().parents[2]
    nginx_config = (repository_root / "deploy" / "nginx.demo.conf").read_text(
        encoding="utf-8"
    )

    api_location = nginx_config.split("location /api/ {", maxsplit=1)[1].split(
        "}", maxsplit=1
    )[0]
    assert "proxy_connect_timeout 10s;" in api_location
    assert "proxy_send_timeout 400s;" in api_location
    assert "proxy_read_timeout 400s;" in api_location
