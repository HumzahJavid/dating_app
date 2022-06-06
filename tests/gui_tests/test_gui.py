import pytest
from fastapi.testclient import TestClient
from selenium.webdriver.common.by import By

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


# Searching without setting search logic provides error
def test_search_without_setting_search_logic_display_error_message(driver):
    search_page = SearchPage(driver)
    search_page.load()
    title = driver.title
    print(f"{title}")

    search_button = driver.find_element(By.ID, "searchFormButton")
    search_button.click()

    error_message = driver.find_element(By.CSS_SELECTOR, ".ui.error.message").text
    assert title == "Dating App"
    first_label = driver.find_element(By.TAG_NAME, "label")
    assert first_label.text == "Search logic"
    assert error_message == "Search logic must have a value"
