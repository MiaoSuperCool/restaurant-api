"""门店接口测试。写法和你 Flask 项目里的 test_stores.py 几乎一样，
区别只是把 client 的来源从 app.test_client() 换成 TestClient(app)。
"""


def test_health(client):
    r = client.get("/api/v1/health")
    assert r.status_code == 200
    body = r.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_create_and_get_store(client):
    r = client.post("/api/v1/stores", json={"name": "望京店", "address": "望京 SOHO"})
    assert r.status_code == 201
    created = r.json()["data"]
    assert created["name"] == "望京店"

    r2 = client.get(f"/api/v1/stores/{created['id']}")
    assert r2.status_code == 200
    assert r2.json()["data"]["address"] == "望京 SOHO"


def test_list_stores(client):
    client.post("/api/v1/stores", json={"name": "A 店"})
    client.post("/api/v1/stores", json={"name": "B 店"})
    r = client.get("/api/v1/stores")
    assert len(r.json()["data"]) == 2


def test_update_store_partial(client):
    store_id = client.post("/api/v1/stores", json={"name": "旧名字"}).json()["data"]["id"]
    r = client.patch(f"/api/v1/stores/{store_id}", json={"name": "新名字"})
    assert r.status_code == 200
    assert r.json()["data"]["name"] == "新名字"


def test_duplicate_name_conflict(client):
    client.post("/api/v1/stores", json={"name": "同名店"})
    r = client.post("/api/v1/stores", json={"name": "同名店"})
    assert r.status_code == 409
    assert r.json()["code"] == "conflict"


def test_not_found_envelope(client):
    r = client.get("/api/v1/stores/9999")
    assert r.status_code == 404
    body = r.json()
    assert body["success"] is False
    assert body["code"] == "not_found"


def test_validation_error_envelope(client):
    r = client.post("/api/v1/stores", json={"name": ""})
    assert r.status_code == 422
    assert r.json()["code"] == "validation_error"


def test_delete_store(client):
    store_id = client.post("/api/v1/stores", json={"name": "要删的店"}).json()["data"]["id"]
    assert client.delete(f"/api/v1/stores/{store_id}").status_code == 200
    assert client.get(f"/api/v1/stores/{store_id}").status_code == 404
