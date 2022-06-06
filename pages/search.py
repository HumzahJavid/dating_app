from selenium.webdriver.common.by import By


class SearchPage:
    URL = "http://127.0.0.1:8001/searchpage"

    SEARCH_INPUT = (By.ID, "search_form_input_homepage")

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    # selector
    # select = Select(self.driver.find_element_by_id("fruits01"))
