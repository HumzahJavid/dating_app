from selenium.webdriver.common.by import By


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

    def get_search_results_count(self):
        # add timer here to prevent no such element exception
        search_results = self._driver.find_element(By.ID, "searchResults")
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
        # add timer here to prevent no such element exception
        or_element.click()
