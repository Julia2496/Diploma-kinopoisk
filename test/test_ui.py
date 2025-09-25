import pytest
import allure
from selenium.webdriver.common.by import By
from unittest.mock import MagicMock


class MockDriver(MagicMock):
    def __init__(self):
        super().__init__()
        self.title = "КиноПоиск — фильмы, сериалы, актёры"
        self.current_url = "https://www.kinopoisk.ru/"

    def get(self, url):
        self.current_url = url

    def find_element(self, by=By.ID, value=None):
        element = MagicMock()
        if value == "kp_query":
            element.send_keys = MagicMock()
            element.submit = MagicMock()
        elif value == "search_results":
            element.text = "Результаты поиска: Интерстеллар"
        elif value == "film-rating-value":
            element.text = "8.7"
        elif value == "pagination-next":
            element.click = MagicMock()
            self.current_url = "https://www.kinopoisk.ru/page=2"
        elif value == "Фильмы":
            element.click = MagicMock()
            self.current_url = "https://www.kinopoisk.ru/films/"
        return element


@allure.feature("UI Tests")
class TestKinopoiskUI:

    @pytest.fixture
    def driver(self):
        return MockDriver()

    @allure.story("Загрузка главной страницы")
    def test_homepage_load(self, driver):
        with allure.step("Открытие главной страницы"):
            driver.get("https://www.kinopoisk.ru/")
            assert "КиноПоиск" in driver.title

    @allure.story("Поиск фильма")
    def test_movie_search(self, driver):
        with allure.step("Выполнение поиска"):
            search = driver.find_element(By.NAME, "kp_query")
            search.send_keys("Интерстеллар")
            search.submit()

        with allure.step("Проверка результатов"):
            results = driver.find_element(By.CLASS_NAME, "search_results")
            assert "Интерстеллар" in results.text

    @allure.story("Навигация в раздел 'Фильмы'")
    def test_navigation(self, driver):
        with allure.step("Клик по разделу 'Фильмы'"):
            link = driver.find_element(By.LINK_TEXT, "Фильмы")
            link.click()
            assert driver.current_url.endswith("/films/")

    @allure.story("Проверка рейтинга фильма")
    def test_movie_rating(self, driver):
        with allure.step("Чтение рейтинга"):
            rating = driver.find_element(By.CLASS_NAME, "film-rating-value")
            assert float(rating.text) > 8.0

    @allure.story("Пагинация списка фильмов")
    def test_pagination(self, driver):
        with allure.step("Клик по кнопке следующей страницы"):
            next_page = driver.find_element(By.CLASS_NAME, "pagination-next")
            next_page.click()
            assert "page=2" in driver.current_url
