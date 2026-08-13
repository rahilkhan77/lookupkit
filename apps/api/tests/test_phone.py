from tests.conftest import signup


def test_phone_never_invents_carrier(client):
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    res = client.post("/v1/phone", json={"phone": "+12025550123"}, headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["meta"]["provider"] == "libphonenumber"
    assert "twilio" not in body["meta"]["adapters"]
    carrier = body.get("carrier")
    assert carrier not in {"Example Wireless", "example wireless"}
    if carrier is None:
        assert body["carrier_status"] == "unknown"
    else:
        assert body["carrier_status"] in {"prefix_metadata", "unknown"}


def test_phone_invalid(client):
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    res = client.post("/v1/phone", json={"phone": "abc"}, headers=headers)
    assert res.status_code == 200
    body = res.json()
    assert body["valid"] is False
    assert body["carrier"] is None
    assert body["carrier_status"] == "unknown"
    assert body["carrier"] != "Example Wireless"


def test_phone_valid_us_number(client):
    data = signup(client)
    headers = {"Authorization": f"Bearer {data['api_key']}"}
    res = client.post("/v1/phone", json={"phone": "+16502530000"}, headers=headers)
    body = res.json()
    assert body["e164"] == "+16502530000"
    assert body["region"] == "US"
    assert body["valid"] is True
    assert body.get("carrier") != "Example Wireless"
