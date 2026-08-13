from tests.conftest import signup


def test_email_syntax_mx_disposable(client, monkeypatch):
    from app.services import email_verify

    def fake_mx(domain, timeout=2.5):
        if domain == "mailinator.com":
            return True, ["mx.mailinator.com"], None
        if domain == "example.com":
            return True, ["example.com"], None
        return False, [], "nxdomain"

    monkeypatch.setattr(email_verify, "lookup_mx", fake_mx)
    data = signup(client)
    key = data["api_key"]
    headers = {"Authorization": f"Bearer {key}"}

    bad = client.post("/v1/email", json={"email": "not-an-email"}, headers=headers)
    assert bad.status_code == 200
    assert bad.json()["syntax_valid"] is False

    disp = client.post("/v1/email", json={"email": "throwaway@mailinator.com"}, headers=headers)
    body = disp.json()
    assert body["syntax_valid"] is True
    assert body["disposable"] is True
    assert body["mx_found"] is True
    assert body["meta"]["provider"] == "lookupkit.local"
    assert "millionverifier" not in body["meta"]["adapters"]

    ok = client.post("/v1/email", json={"email": "hello@example.com"}, headers=headers)
    assert ok.json()["disposable"] is False
    assert ok.json()["mx_records"] == ["example.com"]


def test_email_requires_api_key(client):
    res = client.post("/v1/email", json={"email": "a@example.com"})
    assert res.status_code == 401
