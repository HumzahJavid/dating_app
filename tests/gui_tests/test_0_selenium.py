"""
Tests the selenium framework is running
"""

import pytest


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


def test_selenium_via_google(driver):
    driver.get("https://google.com")
    title = driver.title
    print(f"{title}")
    assert title == "Google"


# test selenium can connect to fastapi server
def test_server_correctly_serves_page(driver):
    driver.get("http://127.0.0.1:8001")
    title = driver.title
    print(f"{title}")

    assert title == "Dating App"
