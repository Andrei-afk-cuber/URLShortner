from app.schemas import LinkPublic


# API test class
class TestAPI:
    # Test health endpoint
    async def test_health(self, client):
        response = await client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}

    # Test code generation
    async def test_main_api_endpoints(self, client):
        data = {"original_url": "https://www.google.com"}
        response = await client.post("/shorten", json=data)

        result = response.json()

        assert response.status_code == 201
        assert isinstance(result, (str, int))
        assert result == 1

        response = await client.get(f"/{result}")

        assert response.status_code == 307

        response = await client.get(f"/stats/{result}")

        output = response.json()

        LinkPublic(**output)

        assert response.status_code == 200

    # Test not found error
    async def test_404(self, client):
        response = await client.get("/1")

        assert response.status_code == 404

        response = await client.get("/stats/1")

        assert response.status_code == 404

    # Test unprocessable
    async def test_422(self, client):
        data = {"origin_url": "https://www.google.com"}

        response = await client.post("/shorten", json=data)

        assert response.status_code == 422
