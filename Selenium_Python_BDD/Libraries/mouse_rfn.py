from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sparc_pages.decorators import wait_for_loader
from libraries.waits_config import *
from libraries import locators
import traceback
import time

# ---------------
# Mouse Functions
# ---------------

@wait_for_loader
def click_on_element(self, locator):
    time.sleep(0.5)
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    element.click()


@wait_for_loader
def click_on_not_visible_element(self, locator):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.presence_of_element_located(locator)
    )
    element.click()


@wait_for_loader
def click_js_on_element(self, locator):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    self.driver.execute_script("arguments[0].click();", element)


@wait_for_loader
def double_click_on_element(self, locator):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()


def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    actions = ActionChains(self.driver)
    actions.drag_and_drop_by_offset(element, xoffset, yoffset).perform()


def is_element_displayed(self, locator):
    try:
        element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
            EC.visibility_of_element_located(locator)
        )
        locators.highlight(self, element)
        return element.is_displayed()
    except:
        traceback.print_exc()
        return False


def is_element_enabled(self, locator):
    try:
        element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
            EC.visibility_of_element_located(locator)
        )
        return element.is_enabled()
    except:
        return False


def mouse_hover(self, locator):
    try:
        element = WebDriverWait(self.driver, SCROLL_TIMEOUT).until(
            EC.presence_of_element_located(locator)
        )
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        return True
    except:
        return False


# -----------------
# Scrolls Functions
# -----------------

def scroll_to_element(self, locator):
    element = WebDriverWait(self.driver, SCROLL_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()


def scroll_horizontally(self, scroll_locator, target_locator):
    """Scroll horizontally"""
    scroll_element = WebDriverWait(self.driver, SCROLL_TIMEOUT).until(
        EC.visibility_of_element_located(scroll_locator)
    )
    scroll_width = scroll_element.rect['width']
    for x in range(1, scroll_width, 300):
        try:
            WebDriverWait(self.driver, HORIZONTAL_SCROLL_TIMEOUT).until(
                EC.visibility_of_element_located(target_locator)
            )
        except TimeoutException:
            self.driver.execute_script(f"arguments[0].scrollLeft += {x}", scroll_element)


# ----------------------------
# Verification methods
# -----------------------------

def check_element_displayed(self, locator):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    return element.is_displayed()


def get_text(self, locator):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    return element.text


def check_element_not_displayed(self, locator):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(
        EC.invisibility_of_element_located(locator))
    return element


@wait_for_loader
def Javascript_click_on_element(self, locator):
    element = WebDriverWait(self.driver, CLICK_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
    self.driver.execute_script("arguments[0].click();", element)
