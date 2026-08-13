from tests.conftest import signup


def test_skip_trace_people_transcription_are_501(client):
    paths = [
        "/v1/skip-trace",
        "/v1/people",
        "/v1/people-search",
        "/v1/transcription",
        "/v1/audio-transcription",
    ]
    for path in paths:
        res = client.post(path, json={"query": "Jane Doe"})
        assert res.status_code == 501, path
        body = res.json()
        assert body["error"] == "unavailable"
        assert "fabricated" in body["message"].lower()
        blob = str(body).lower()
        assert "jane doe" not in blob
        assert "ssn" not in blob


def test_credits_decrement_and_402(client, monkeypatch):
    from app.services import email_verify

    monkeypatch.setattr(email_verify, "lookup_mx", lambda domain, timeout=2.5: (True, ["mx.example.com"], None))
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    start = data["credits"]
    res = client.post("/v1/email", json={"email": "ok@example.com"}, headers=headers)
    assert res.json()["credits_remaining"] == start - 1
    # burn remaining credits
    for _ in range(start - 1):
        client.post("/v1/email", json={"email": "ok@example.com"}, headers=headers)
    depleted = client.post("/v1/email", json={"email": "ok@example.com"}, headers=headers)
    assert depleted.status_code == 402


def test_adapters_off_without_keys(client):
    status = client.get("/v1/status").json()
    assert status["email"]["millionverifier"] is False
    assert status["phone"]["twilio"] is False
    assert status["ip"]["maxmind"] is False
    assert status["email"]["mx_dns"] is True
