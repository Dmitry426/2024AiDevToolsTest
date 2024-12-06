from http import HTTPStatus


class TestBaseApi:
    def test_fit_endpoint(self, client):
        payload = [
            {
                "X": [[1.0, 2.0], [3.0, 4.0]],
                "config": {
                    "hyperparameters": {"fit_intercept": True},
                    "id": "linear_model_1",
                },
                "y": [5.0, 6.0],
            }
        ]
        response = client.post("/fit", json=payload)
        assert response.status_code == HTTPStatus.CREATED
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]

    def test_load_endpoint(self, client):
        payload = {"id": "linear_model_1"}
        response = client.post("/load", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]

    def test_predict_endpoint(self, client):
        payload = {
            "id": "linear_model_1",
            "input_data": [4.0],
        }
        response = client.post("/predict", json=payload)
        assert response.status_code == HTTPStatus.OK
        json_response = response.json()[0]        
        assert json_response["message"] == "Prediction successful"
        assert "linear_model_1" in json_response["data"]
        assert "prediction" in json_response["data"]["linear_model_1"]

    def test_list_models_endpoint(self, client):
        response = client.get("/list_models")
        assert response.status_code == HTTPStatus.OK
        json_response = response.json()[0]
        assert "models" in json_response["data"]
        assert any(
            model["id"] == "linear_model_1" for model in json_response["data"]["models"]
        )

    def test_remove_all_endpoint(self, client):
        response = client.delete("/remove_all")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]
