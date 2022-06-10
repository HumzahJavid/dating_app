from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class IndexPage:
    URL = "http://127.0.0.1:8001/"

    def __init__(self, driver):
        self._driver = driver
        self._load()

    def _load(self):
        self._driver.get(self.URL)

    def click_login_button(self):
        login_button = self._driver.find_element(By.ID, "loginButton")
        login_button.click()

    def click_login_form_button(self):
        login_form_button = self._driver.find_element(By.ID, "loginFormButton")
        login_form_button.click()

    def is_login_modal_visible(self):
        login_modal = self._driver.find_element(By.ID, "loginModal")
        return login_modal.is_displayed()

    def enter_test_username_and_password(self, username, password):
        login_modal = self._driver.find_element(By.ID, "loginModal")
        if self.is_login_modal_visible():
            print("modal visible so look for field")
            user_field = login_modal.find_element(By.ID, "loginFormEmail")
            user_field.send_keys(username)
        else:
            print("not visible, cause of error?")
        pass_field = login_modal.find_element(By.ID, "loginFormPassword")
        pass_field.send_keys(password)

    def get_toast_text(self):
        WebDriverWait(self._driver, 1).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "toast-container"))
        )
        toast = self._driver.find_element(By.CLASS_NAME, "toast-container")
        return toast.find_element(By.CLASS_NAME, "content").text

    def login_test_user(self, test_user):
        self.click_login_button()
        self.enter_test_username_and_password(test_user["email"], test_user["password"])
        self.click_login_form_button()
