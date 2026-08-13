from app.config import stripe_key_allowed
from tests.conftest import signup


def test_live_stripe_key_refused_without_flag():
    ok, reason = stripe_key_allowed("sk_live_example_not_real", "0")
    assert ok is False
    assert reason == "live_key_refused"


def test_test_stripe_key_allowed():
    ok, reason = stripe_key_allowed("sk_test_example_not_real", "0")
    assert ok is True
    assert reason == "test"


def test_live_allowed_only_with_flag():
    ok, reason = stripe_key_allowed("sk_live_example_not_real", "1")
    assert ok is True
    assert reason == "live"


def test_checkout_unconfigured(client):
    signup(client)
    res = client.post("/billing/checkout", json={"plan": "starter"})
    assert res.status_code == 503
    assert "not configured" in res.json()["detail"].lower()


def test_plans_match_pricing(client):
    res = client.get("/billing/plans")
    plans = {p["id"]: p for p in res.json()["plans"]}
    assert plans["starter"] == {"id": "starter", "name": "Starter", "usd": 99, "credits": 20_000}
    assert plans["growth"]["usd"] == 299 and plans["growth"]["credits"] == 85_000
    assert plans["pro"]["usd"] == 799 and plans["pro"]["credits"] == 250_000
    assert plans["enterprise"]["usd"] == 1999 and plans["enterprise"]["credits"] == 1_000_000
    assert res.json()["stripe_ready"] is False
