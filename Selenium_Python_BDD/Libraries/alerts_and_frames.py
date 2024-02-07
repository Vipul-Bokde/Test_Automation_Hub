from libraries import locators
from selenium.webdriver.common.alert import Alert

# -----------------
# Frames functions
# -----------------


def switch_to_frame(self, locator_type, locator):
    element = locators.locator_element(self, locator_type, locator)
    self.driver.switch_to.default_content()
    self.driver.switch_to.frame(element)

def alert_ok(driver):
    Alert(driver).accept()

def alert_get_text(driver):
    return Alert(driver).text

def alert_dismiss(driver):
    Alert(driver).dismiss()