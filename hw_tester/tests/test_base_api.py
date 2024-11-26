from http import HTTPStatus


class TestBaseApi:
    def test_fit_endpoint(self, client):
        payload = {
            "config": {"id": "linear_model_1"},
            "train_data": {"X": [1.0, 2.0, 3.0], "y": [2.0, 4.0, 6.0]},
        }
        response = client.post("/fit", json=payload)
        assert response.status_code == HTTPStatus.CREATED
        assert response.json()["message"]

    def test_load_endpoint(self, client):
        payload = {"id": "linear_model_1"}
        response = client.post("/load", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"]

    def test_predict_endpoint(self, client):
        payload = {
            "id": "linear_model_1",
            "input_data": [4.0],
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == HTTPStatus.OK
        json_response = response.json()
        assert json_response["message"] == "Prediction successful"
        assert "linear_model_1" in json_response["data"]
        assert "prediction" in json_response["data"]["linear_model_1"]

    def test_list_models_endpoint(self, client):
        response = client.get("/list_models")
        assert response.status_code == HTTPStatus.OK
        json_response = response.json()
        assert json_response["message"] == "List of models"
        assert "models" in json_response["data"]
        assert any(model["id"] == "linear_model_1" for model in json_response["data"]["models"])

    def test_remove_all_endpoint(self, client):
        response = client.delete("/remove_all")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"]
