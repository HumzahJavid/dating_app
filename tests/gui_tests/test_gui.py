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


def test_when_search_without_setting_search_logic__then_display_error_message(driver):
    """Searching without setting search logic returns error"""
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


def test_when_search_with_default_fields_plus_OR_logic_then_results_returned(driver):
    """Searching returns some results (setting required search logic to OR, age fields
    are set by default if unchanged)
    """
    search_page = SearchPage(driver)
    search_page.load()

    logic_element = driver.find_elements(By.CSS_SELECTOR, ".ui.selection.dropdown")[0]
    logic_element.click()
    or_element = driver.find_element(
        By.XPATH, "/html/body/form/div/div[1]/div/div[2]/div[@data-value='or']"
    )
    or_element.click()

    search_button = driver.find_element(By.ID, "searchFormButton")
    search_button.click()

    search_results = driver.find_element(By.ID, "searchResults")
    number_of_results = len(search_results.find_elements(By.CSS_SELECTOR, ".ui.card"))

    error_message = driver.find_element(By.CSS_SELECTOR, ".ui.error.message").text
    assert error_message != "Search logic must have a value"
    assert number_of_results > 0
