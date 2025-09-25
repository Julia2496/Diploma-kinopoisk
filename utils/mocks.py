from unittest.mock import MagicMock


class MockDriver(MagicMock):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title = "КиноПоиск - фильмы и сериалы"
        self.current_url = "https://www.kinopoisk.ru/"
        self.find_element.return_value = MagicMock(text="")
        self.execute_script.return_value = None

    def get(self, url):
        self.current_url = url
        return None

    def set_mock_element(self, text="", **kwargs):
        mock = MagicMock()
        mock.text = text
        for key, value in kwargs.items():
            setattr(mock, key, value)
        self.find_element.return_value = mock
        return mock


class KinopoiskMockClient:
    def __init__(self):
        self.mock_response = None
        self.reset_mocks()

    def reset_mocks(self):
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.json.return_value = {
            "films": [
                {"id": 123, "name": "Интерстеллар", "rating": 8.6, "year": 2014},
                {"id": 124, "name": "Начало", "rating": 8.7, "year": 2010}
            ],
            "total": 2
        }

    def set_mock_response(self, status_code=200, json_data=None):
        self.mock_response = MagicMock()
        self.mock_response.status_code = status_code
        if json_data:
            self.mock_response.json.return_value = json_data
        else:
            self.mock_response.json.return_value = {
                "error": {
                    "code": status_code,
                    "message": "Default error message"
                }
            }
        return self.mock_response

    def search_movies(self, query, filters=None):
        return self.mock_response

    def get_movie(self, movie_id):
        if self.mock_response.status_code == 200:
            movie_mock = MagicMock()
            movie_mock.status_code = 200
            movie_mock.json.return_value = {
                "film": {
                    "id": movie_id,
                    "name": "Интерстеллар",
                    "rating": 8.6,
                    "year": 2014
                }
            }
            return movie_mock
        return self.mock_response

    def get_similar_movies(self, movie_id):
        similar_mock = MagicMock()
        similar_mock.status_code = 200
        similar_mock.json.return_value = {
            "similar_films": [
                {"id": 125, "name": "Гравитация", "rating": 7.8},
                {"id": 126, "name": "Марсианин", "rating": 8.0}
            ]
        }
        return similar_mock
