import pytest
from fastapi.testclient import TestClient
from selenium.webdriver.common.by import By

from dating_app.main import app


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
    # Run selenium and chrome driver to scrape data from cloudbytes.dev
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


def test_searchpage_gui(driver):

    driver.get("http://127.0.0.1:8001/searchpage")

    title = driver.title
    print(f"{title}")
    sub_title = driver.find_element(By.TAG_NAME, "h2").text

    assert "Search page" in sub_title
