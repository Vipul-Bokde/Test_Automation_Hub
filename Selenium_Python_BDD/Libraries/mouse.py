import time
from selenium.webdriver.common.action_chains import ActionChains
from libraries import locators
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ---------------
# Mouse Functions
# ---------------

def click_on_element(self, locator_type, locator, times=1):
    """Click on an element"""
    time.sleep(0.5)
    element = locators.locator_element(self, locator_type, locator)
    try:
        locators.highlight(self, element)
    except:
        pass
    for i in range(times):
        element.click()
        time.sleep(0.5)

def click_action_on_element(self, locator_type, locator, times=1):
    element = locators.locator_element(self, locator_type, locator)
    locators.highlight(self, element)
    for i in range(times):
        actions = ActionChains(self.driver)
        actions.move_to_element(element).click(element).perform()

def click_js_on_element(self, locator_type, locator):
    element = locators.locator_element(self, locator_type, locator)
    self.driver.execute_script("arguments[0].click();", element)


def double_click_on_element(self, locator_type, locator):
    time.sleep(0.5)
    element = locators.locator_element(self, locator_type, locator)
    locators.highlight(self, element)
    actions = ActionChains(self.driver)
    actions.double_click(element).perform()

# -----------------
# Scrolls Functions
# -----------------

def scroll_to_element(self, locator_type, locator):
    time.sleep(0.5)
    element = locators.locator_element(self, locator_type, locator)
    locators.highlight(self, element)
    try:
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
    except:
        return


def scroll_to_element_javascript(self, locator_type, locator):
    time.sleep(0.5)
    element = locators.locator_element(self, locator_type, locator)
    self.driver.execute_script("arguments[0].scrollIntoView();", element)


def scroll_in_web_page(self, position_x, position_y):
    """Scroll in web page, in the position (x,y) [vertical and horizontal]"""
    variable = "window.scrollBy(" + position_x + "," + position_y + ")"
    self.driver.execute_script(variable)

def scroll_to_down_the_web_page(self):
    variable = "window.scrollTo(0, document.body.scrollHeight)"
    self.driver.execute_script(variable)

# ---------------
# Description: Scroll function to perform inner scroll
#             inside a table. Pass the length of how many times the right arrow can be pressed.
#             First click on the first row first cell and then use this method to scroll right in table.
# ---------------
def scroll_to_right_using_send_keyboard_keys(self,length):
    try:
        loopcount = 0
        while loopcount < length:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ARROW_RIGHT).perform()
            loopcount = loopcount+1
        return True
    except:
        return False

"""Author : Sadiya Kotwal
       Description : Scroll function to perform inner scroll inside a table. Pass the length 
                    of how many times the right arrow can be pressed
       Arguments : length (length= 15)
       Returns : NA"""
def scroll_to_down_using_send_keyboard_keys(self,length):
    try:
        loopcount = 0
        while loopcount < length:
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.ARROW_DOWN).perform()
            loopcount = loopcount+1
        return True
    except:
        return False

def check_element_displayed(self, locator_type, locator):
    time.sleep(0.5)
    element = locators.locator_element(self, locator_type, locator)
    locators.highlight(self, element)
    actions = ActionChains(self.driver)
    actions.move_to_element(element).perform()
    return element.is_displayed()