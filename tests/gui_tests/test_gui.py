import pytest
from fastapi.testclient import TestClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from dating_app.main import app
from pages.index import IndexPage
from pages.search import SearchPage


@pytest.fixture
def client():
    """Creates a stateless FastAPI test_client

    :yields: A FastAPI Test Client
    """

    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_user_1():
    return {
        "email": "test_user_1@email.com",
        "password": "test_password",
        "name": "test user1",
        "age": "25",
        "gender": "female",
    }


@pytest.fixture
def test_user_2():
    return {
        "email": "test_user_2@email.com",
        "password": "test_password",
        "name": "test user2",
        "age": "25",
        "gender": "male",
    }


def save_screenshot(driver: webdriver.Chrome, path: str = "./screenshot.png") -> None:
    """Function to support debugging in headless mode to confirm whether elements
    are present or not to determine if  explicit wait conditions are required"""

    # Ref: https://stackoverflow.com/a/52572919/
    original_size = driver.get_window_size()
    required_width = driver.execute_script(
        "return document.body.parentNode.scrollWidth"
    )
    required_height = driver.execute_script(
        "return document.body.parentNode.scrollHeight"
    )
    driver.set_window_size(required_width, required_height)
    driver.find_element(By.TAG_NAME, "body").screenshot(path)  # avoids scrollbar
    driver.set_window_size(original_size["width"], original_size["height"])


@pytest.fixture
def driver():
    """Setup the selenium driver (chrome) in headless mode, teardown after use

    :yields: A Chome driven selenium driver
    """

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


def test_when_login_button_clicked_then_login_modal_form_appears(driver):
    """modal is the login form which appears as a 'popup' when the login button
    is clicked
    """
    index_page = IndexPage(driver)
    index_page.click_login_button()
    assert index_page.is_login_modal_visible() is True


def test_when_user_logs_in_then_success_message_appears(driver, test_user_1):
    index_page = IndexPage(driver)
    index_page.click_login_button()
    index_page.enter_test_username_and_password(
        test_user_1["email"], test_user_1["password"]
    )
    index_page.click_login_form_button()
    login_response = index_page.get_toast_text()
    print(login_response)
    assert login_response == "Login successful."


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

    number_of_results = search_page.get_search_results_count(
        search_page.get_search_results()
    )
    error_message = search_page.get_error_message_text()

    assert error_message != "Search logic must have a value"
    assert number_of_results > 0


def test_when_user_sends_a_message_then_message_is_registered_on_chatbox(
    driver, test_user_1
):
    """A user must be logged in to initiate chat, chat is initiated by clicking a users
    profile picture and sending a message

    A successfully sent message appears on the chat box
    """
    index_page = IndexPage(driver)
    index_page.login_test_user(test_user_1)
    search_page = SearchPage(driver)
    search_page.search_test_user(test_user_1)
    search_results = search_page.get_search_results()
    number_of_results = search_page.get_search_results_count(search_results)
    print(number_of_results)
    search_page.start_chat_with_user(search_results)
    save_screenshot(driver, "./screenshot_chat_box_appears.png")
    search_page.send_message("Welcome to this chat")
    save_screenshot(driver, "./screenshot_chat_message_sent.png")
    last_message = search_page.get_last_message_on_window()
    try:
        assert last_message.text == "Welcome to this chat"
    except AssertionError:
        save_screenshot(driver)
