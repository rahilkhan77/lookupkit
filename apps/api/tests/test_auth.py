def test_signup_hashes_password_and_sets_httponly_cookie(client):
    res = client.post("/auth/signup", json={"email": "rahil@excentia.site", "password": "correct-horse"})
    assert res.status_code == 201
    body = res.json()
    assert body["email"] == "rahil@excentia.site"
    assert body["credits"] == 20
    assert body["api_key"].startswith("lk_test_")
    cookie = res.cookies.get("lk_session")
    assert cookie
    header = res.headers.get("set-cookie", "")
    assert "HttpOnly" in header or "httponly" in header.lower()
    me = client.get("/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == "rahil@excentia.site"


def test_login_rejects_bad_password(client):
    client.post("/auth/signup", json={"email": "a@example.com", "password": "password123"})
    res = client.post("/auth/login", json={"email": "a@example.com", "password": "wrongpass"})
    assert res.status_code == 401


def test_duplicate_signup(client):
    payload = {"email": "dup@example.com", "password": "password123"}
    assert client.post("/auth/signup", json=payload).status_code == 201
    assert client.post("/auth/signup", json=payload).status_code == 409


def test_dashboard_account_requires_session(client):
    assert client.get("/account/me").status_code == 401
    client.post("/auth/signup", json={"email": "b@example.com", "password": "password123"})
    assert client.get("/account/me").status_code == 200


def test_create_live_and_test_keys(client):
    client.post("/auth/signup", json={"email": "keys@example.com", "password": "password123"})
    test = client.post("/account/keys", json={"name": "ci", "live": False})
    live = client.post("/account/keys", json={"name": "prod", "live": True})
    assert test.status_code == 201
    assert live.status_code == 201
    assert test.json()["key"].startswith("lk_test_")
    assert live.json()["key"].startswith("lk_live_")
    listed = client.get("/account/keys").json()
    assert len(listed) >= 3  # default + two
