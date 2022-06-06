import pytest
from fastapi.testclient import TestClient

from dating_app.main import app
from pages.search import SearchPage


@pytest.fixture
def client():
    """Creates a stateless FastAPI test_client

    :yields: A FastAPI Test Client
    """

    with TestClient(app) as client:
        yield client


@pytest.fixture
def driver():
    """Setup the selenium driver (chrome) in headless mode, teardown after use

    :yields: A Chome driven selenium driver
    """
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service

    # Setup chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensure GUI is off
    chrome_options.add_argument("--no-sandbox")

    # Set path to chromedriver as per your configuration
    webdriver_service = Service("chromedriver")

    # Choose Chrome Browser
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    yield driver
    # teardown driver
    driver.quit()


# test fastapi w/o testclient
def test_index_gui(driver):
    driver.get("http://127.0.0.1:8001")
    title = driver.title
    print(f"{title}")

    assert title == "Dating App"


def test_when_search_without_setting_search_logic__then_display_error_message(driver):
    """Searching without setting search logic returns error"""
    search_page = SearchPage(driver)

    search_page.click_search_button()

    assert search_page.get_title() == "Dating App"
    assert search_page.get_error_message_text() == "Search logic must have a value"


def test_when_search_with_default_fields_using_or_logic_then_results_returned(driver):
    """Searching returns some results (setting required search logic to OR, age fields
    are set by default if unchanged)
    """
    search_page = SearchPage(driver)

    search_page.select_search_logic_type("or")
    search_page.click_search_button()
    number_of_results = search_page.get_search_results_count()
    error_message = search_page.get_error_message_text()

    assert error_message != "Search logic must have a value"
    assert number_of_results > 0
