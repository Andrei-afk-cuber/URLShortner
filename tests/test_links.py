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