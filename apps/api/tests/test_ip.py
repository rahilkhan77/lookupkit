from tests.conftest import signup


def test_private_ip_local_provider(client):
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    res = client.post("/v1/ip", json={"ip": "192.168.1.10"}, headers=headers)
    body = res.json()
    assert body["is_public"] is False
    assert body["classification"] == "private"
    assert body["meta"]["provider"] == "lookupkit.local"
    assert body["country"] is None


def test_public_ip_uses_ip_api_and_honest_provider(client, monkeypatch):
    from app.services import ip_lookup

    monkeypatch.setattr(
        ip_lookup,
        "_ip_api",
        lambda ip: {
            "country": "United States",
            "country_code": "US",
            "city": "Mountain View",
            "isp": "Google LLC",
            "hosting": True,
            "proxy": False,
        },
    )
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    res = client.post("/v1/ip", json={"ip": "8.8.8.8"}, headers=headers)
    body = res.json()
    assert body["is_public"] is True
    assert body["meta"]["provider"] == "ip-api.com"
    assert "maxmind" not in body["meta"]["adapters"]
    assert body["isp"] == "Google LLC"


def test_loopback_not_geolocated(client):
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    res = client.post("/v1/ip", json={"ip": "127.0.0.1"}, headers=headers)
    assert res.json()["classification"] == "loopback"
    assert res.json()["meta"]["provider"] == "lookupkit.local"
