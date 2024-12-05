from http import HTTPStatus


class TestHwPro:
    """Test pro hw"""

    def test_health_endpoint(self, client):
        response = client.get("/")
        assert response.status_code == HTTPStatus.OK
        assert response.json()

    def test_fit_model(self, client):
        payload =[ {
            "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]],
            "y": [5.0, 7.0, 9.0],
            "config": {
                "id": "linear_123",
                "ml_model_type": "linear",
                "hyperparameters": {},
            },
        }]
        response = client.post("/api/v1/models/fit", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]["message"]

    def test_list_models(self, client):
        response = client.get("/api/v1/models/list_models")
        assert response.status_code == HTTPStatus.OK
        response = response.json()[0].get("models", [])
        assert isinstance(response, list)

    def test_load_model(self, client):
        payload = {"id": "linear_123"}
        response = client.post("/api/v1/models/load", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]["message"]

    def test_predict(self, client):
        payload = [{"id": "linear_123", "X": [[4.0, 5.0]]}]
        response = client.post("/api/v1/models/predict", json=payload)
        assert response.status_code == HTTPStatus.OK
        result = response.json()
        assert isinstance(result,list)
        assert "predictions" in result[0]

    def test_unload_model(self, client):
        payload = {"id": "linear_123"}
        response = client.post("/api/v1/models/unload/", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]

    def test_remove_model(self, client):
        response = client.delete("/api/v1/models/remove/linear_123")
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]["message"]

    def test_remove_all_models(self, client):
        response = client.delete("/api/v1/models/remove_all")
        assert response.status_code == HTTPStatus.OK
        assert response.json()[0]["message"]
