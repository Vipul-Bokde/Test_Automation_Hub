from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from libraries.waits_config import DEFAULT_TIMEOUT, TEXT_TIMEOUT


def get_element(self, locator, wait=DEFAULT_TIMEOUT):
    """finds a specific element"""
    try:
        return WebDriverWait(self.driver, wait).until(EC.presence_of_element_located(locator))
    except TimeoutException:
        return None


def get_elements(self, locator, wait=DEFAULT_TIMEOUT):
    """finds a set of elements"""
    try:
        return WebDriverWait(self.driver, wait).until(EC.presence_of_all_elements_located(locator))
    except TimeoutException:
        return None


def get_element_from_element(element, by, locator):
    """finds an element inside another element"""
    try:
        return element.find_element(by, locator)
    except NoSuchElementException:
        return None


def get_text_on_element(self, locator):
    """Gets the element text"""
    element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    return element.text


def interpolate(locator, valor):
    """Interpolates a value on a locator for CSS and XPATH"""
    if locator[0] in ["xpath", "css selector"]:
        return locator[0], locator[1].format(valor)


def wait_element_is_not_visible(self, locator, wait=TEXT_TIMEOUT):
    """Wait until an element is not visible in the DOM"""
    element = WebDriverWait(self.driver, wait).until(EC.invisibility_of_element_located(locator))
    return element


def wait_element_is_visible(self, locator, wait=TEXT_TIMEOUT):
    """Wait until an element is visible in the DOM"""
    element = WebDriverWait(self.driver, wait).until(EC.visibility_of_element_located(locator))
    return element


def wait_element_is_clickable(self, locator, wait=TEXT_TIMEOUT):
    """Wait until an element is clickable, i.e enabled"""
    element = WebDriverWait(self.driver, wait).until(EC.element_to_be_clickable(locator))
    return element


def element_exists(self, locator):
    """Check if an element exist in the DOM"""
    elements = self.driver.find_elements(*locator)
    if len(elements) > 0:
        return True
    return False
