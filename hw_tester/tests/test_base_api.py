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
        payload = [{"id": "linear_model_1", "X": [[4.0, 5.0]]}]
        response = client.post("/predict", json=payload)
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)    


    def test_list_models_endpoint(self, client):
        response = client.get("/list_models")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)



    def test_remove_all_endpoint(self, client):
        response = client.delete("/remove_all")
        assert response.status_code == HTTPStatus.OK
        assert isinstance(response.json(),list)
        assert response.json()[0]["message"]
