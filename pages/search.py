from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SearchPage:
    URL = "http://127.0.0.1:8001/searchpage"

    def __init__(self, driver):
        self._driver = driver
        self._load()

    def _load(self):
        self._driver.get(self.URL)

    def _click_logic_element_dropdown_list(self):
        logic_element = self._driver.find_element(
            By.CSS_SELECTOR, ".ui.selection.dropdown"
        )
        logic_element.click()

    def click_search_button(self):
        search_button = self._driver.find_element(By.ID, "searchFormButton")
        search_button.click()

    def get_error_message_text(self):
        return self._driver.find_element(By.CSS_SELECTOR, ".ui.error.message").text

    def get_title(self):
        return self._driver.title

    def get_search_results(self):
        WebDriverWait(self._driver, 2).until(
            EC.visibility_of_element_located((By.ID, "searchResults"))
        )
        return self._driver.find_element(By.ID, "searchResults")

    def get_search_results_count(self, search_results):
        number_of_results = len(
            search_results.find_elements(By.CSS_SELECTOR, ".ui.card")
        )
        return number_of_results

    def select_search_logic_type(self, search_logic):
        self._click_logic_element_dropdown_list()
        logic_element_xpath = (
            f"/html/body/form/div/div[1]/div/div[2]/div[@data-value='{search_logic}']"
        )
        or_element = self._driver.find_element(By.XPATH, logic_element_xpath)
        WebDriverWait(self._driver, 1).until(EC.element_to_be_clickable(or_element))
        or_element.click()

    def search_test_user(self, test_user):
        self.select_search_logic_type("and")
        name_field = self._driver.find_element(
            By.CSS_SELECTOR, "#searchForm input[name=name]"
        )
        email_field = self._driver.find_element(
            By.CSS_SELECTOR, "#searchForm input[name=email]"
        )
        name_field.send_keys(test_user["name"])
        email_field.send_keys(test_user["email"])
        self.click_search_button()

    def start_chat_with_user(self, search_results):
        image_user = search_results.find_elements(By.CLASS_NAME, "imageChat")
        print(len(image_user))
        print(image_user[0].get_attribute("data-email"))
        WebDriverWait(self._driver, 2).until(EC.element_to_be_clickable(image_user[0]))
        image_user[0].click()
        WebDriverWait(self._driver, 2).until(
            EC.visibility_of_element_located((By.ID, "chatModal"))
        )

    def send_message(self, message):
        WebDriverWait(self._driver, 1).until(
            EC.visibility_of_element_located((By.ID, "chatModal"))
        )
        chat_field = self._driver.find_element(By.ID, "chat-input")
        chat_field.send_keys(message)
        self._driver.find_element(By.ID, "send").click()

    def get_last_message_on_window(self):
        chat_window = self._driver.find_element(By.ID, "chatModal")
        messages = chat_window.find_elements(By.TAG_NAME, "p")
        return messages[len(messages) - 1]
