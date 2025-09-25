import pytest
import allure
from utils.mocks import KinopoiskMockClient


@allure.feature("API Tests")
class TestKinopoiskAPI:
    @pytest.fixture
    def api_client(self):
        return KinopoiskMockClient()

    @allure.story("Поиск фильмов")
    def test_search_movies(self, api_client):
        response = api_client.search_movies("Интерстеллар")
        assert response.status_code == 200
        assert any(m["name"] == "Интерстеллар" for m in response.json()["films"])

    @allure.story("Детали фильма")
    def test_movie_details(self, api_client):
        response = api_client.get_movie(123)
        data = response.json()
        assert data["film"]["id"]
        assert "name" in data["film"]
        assert "rating" in data["film"]

    @allure.story("Фильтры поиска")
    def test_search_filters(self, api_client):
        response = api_client.search_movies("", {"year": 2020, "rating": 7})
        assert len(response.json()["films"]) > 0

    @allure.story("Ошибка 404")
    def test_not_found(self, api_client):
        api_client.set_mock_response(
            status_code=404,
            json_data={
                "error": {
                    "code": 404,
                    "message": "Фильм не найден"
                }
            }
        )
        response = api_client.get_movie(999999)
        assert response.status_code == 404
        assert "error" in response.json()

    @allure.story("Похожие фильмы")
    def test_similar_movies(self, api_client):
        response = api_client.get_similar_movies(123)
        assert len(response.json()["similar_films"])
