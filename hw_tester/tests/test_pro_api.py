from http import HTTPStatus

import pytest


@pytest.mark.asyncio
class TestDummy:
    async def test_health(self, ):
        response = await make_request(method="GET", url="/")
        assert response.status == HTTPStatus.OK

    async def test_fit_model(self, make_request):
        payload = {
            "X": [[1.0, 2.0], [2.0, 3.0], [3.0, 4.0]],
            "y": [5.0, 7.0, 9.0],
            "config": {
                "id": "linear_123",
                "ml_model_type": "linear",
                "hyperparameters": {}
            }
        }
        response = await make_request(method="POST", url="/api/v1/models/fit", json=payload)
        assert response.status == HTTPStatus.CREATED

    async def test_list_models(self, make_request):
        response = await make_request(method="GET", url="/api/v1/models/list_models")
        assert response.status == HTTPStatus.OK

    async def test_load_model(self, make_request):
        payload = {"id": "linear_123"}
        response = await make_request(method="POST", url="/api/v1/models/load", json=payload)
        assert response.status == HTTPStatus.OK

    async def test_predict(self, make_request):
        payload =[ {'id':'linear_123','X':[[4.0, 5.0]]}]
        response = await make_request(method="POST", url="/api/v1/models/predict", json=payload)
        assert response.status == HTTPStatus.OK
        result = response.json()
        assert "predictions" in result

    async def test_unload_model(self, make_request):
        payload = {"id": "linear_123"}
        response = await make_request(method="POST", url="/api/v1/models/unload/", json=payload)
        assert response.status == HTTPStatus.OK

    async def test_remove_model(self, make_request):
        response = await make_request(method="DELETE", url="/api/v1/models/remove/linear_123")
        assert response.status == HTTPStatus.OK

    async def test_remove_all_models(self, make_request):
        response = await make_request(method="DELETE", url="/api/v1/models/remove_all")
        assert response.status == HTTPStatus.OK
