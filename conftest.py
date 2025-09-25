import pytest
from unittest.mock import patch
from utils.mocks import MockDriver, KinopoiskMockClient


@pytest.fixture
def driver():
    """Фикстура для мок-драйвера Selenium"""
    return MockDriver()


@pytest.fixture
def api_client():
    """Фикстура для мок-клиента API Кинопоиска"""
    client = KinopoiskMockClient()
    yield client
    client.reset_mocks()


@pytest.fixture(autouse=True)
def mock_webdriver(monkeypatch):
    """Монкипатч для WebDriver"""
    monkeypatch.setattr(
        "selenium.webdriver.Chrome",
        lambda *args, **kwargs: MockDriver()
    )
