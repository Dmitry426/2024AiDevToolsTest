from http import HTTPStatus


class TestMLService:
    """Test suite for the ml_service_hw FastAPI app."""

    def test_health_endpoint(self, client):
        """Test the health status endpoint."""
        response = client.get("/")
        assert response.status_code == HTTPStatus.OK
        assert response.json()

    def test_fit_model(self, client):
        """Test fitting a model."""
        payload = [{
            "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]],
            "y": [5.0, 7.0, 9.0],
            "config": {
                "id": "linear_123",
                "ml_model_type": "linear",
                "hyperparameters": {"fit_intercept": True},
            },
        }]
        response = client.post("/api/v1/models/fit", json=payload)
        assert response.status_code == HTTPStatus.CREATED
        assert isinstance(response.json(),list)

    def test_list_models(self, client):
        """Test listing all models."""
        response = client.get("/api/v1/models/list_models")
        assert response.status_code == HTTPStatus.OK
        models = response.json()
        assert isinstance(models, list)

    def test_load_model(self, client):
        """Test loading a model."""
        payload = {"id": "linear_123"}
        response = client.post("/api/v1/models/load", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"] == "Model 'linear_123' loaded"

    def test_predict(self, client):
        """Test making predictions."""
        payload = {"id": "linear_123", "X": [[4.0, 5.0]]}
        response = client.post("/api/v1/models/predict", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        result = response.json()[0]
        assert "predictions" in result

    def test_unload_model(self, client):
        """Test unloading a model."""
        payload = {"id": "linear_123"}
        response = client.post("/api/v1/models/unload", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]

    def test_remove_model(self, client):
        """Test removing a specific model."""
        response = client.delete("/api/v1/models/remove/linear_123")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]

    def test_remove_all_models(self, client):
        """Test removing all models."""
        payload = [{
            "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]],
            "y": [5.0, 7.0, 9.0],
            "config": {
                "id": "linear_123",
                "ml_model_type": "linear",
                "hyperparameters": {"fit_intercept": True},
            },
        }]
        response = client.post("/api/v1/models/fit", json=payload)
        response = client.delete("/api/v1/models/remove_all")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]
