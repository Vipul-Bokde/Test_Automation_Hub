import random

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from libraries.waits_config import *
import logging
from selenium.webdriver.common.action_chains import ActionChains
from libraries import locators

LOGGER = logging.getLogger(__name__)


# -----------------
# Text functions
# -----------------

def enter_text_on_element(self, locator, text):
    element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(EC.visibility_of_element_located(locator))
    element.clear()
    element.send_keys(text)


def enter_text_press_enter(self, locator, text):
    element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(EC.visibility_of_element_located(locator))
    element.clear()
    element.send_keys(text, Keys.ENTER)


def enter_text_press_escape(self, locator, text):
    element = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(locator))
    element.clear()
    element.send_keys(text, Keys.ESCAPE)


def enter_text_press_tab(self, locator, text):
    element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(EC.visibility_of_element_located(locator))
    element.clear()
    element.send_keys(text, Keys.TAB)


def get_text_on_element(self, locator):
    element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(EC.visibility_of_element_located(locator))
    return element.text

# ------------------
# Dropdown functions
# ------------------


def select_option_by_text(self, locator, text):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    Select(element).select_by_visible_text(text)

def select_option_by_texts(self, locator, text):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.presence_of_element_located(locator))
    locators.highlight(self, element)
    Select(element).select_by_visible_text(text)
        
def select_option_by_value(self, locator, value):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    Select(element).select_by_value(value)


def select_option_by_index(self, locator, index):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    Select(element).select_by_index(index)


def get_options(self, locator):
    options_list = []
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    options = Select(element).options
    for option in options:
        options_list.append(option.text)
    return options_list


def get_random_option(self, locator):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    options = Select(element).options
    option = random.choice([opt.text for opt in options if opt.text])
    return option


def get_option_id_by_value(self, locator, var_text):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    options = Select(element).options
    op_value = ""
    for option in options:
        if option.text == var_text:
            op_value = option.get_attribute('value')
    return op_value

"""
Author : Rushikesh Thakare
Description : This method returns the list of options from the dropdown and remove
the NONE options from the list.
Arguments : Locator
Returns : list of options
"""
def get_all_no_blank_options(self,locator):
    list_of_options=[]
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(
    EC.visibility_of_element_located(locator))
    all_options= Select(element)
    for opt in all_options.options:
        print(opt.text)
        list_of_options.append(opt.text)
    list_of_options=list(filter(None,list_of_options))
    return list_of_options

# ------------------
# Visibility functions
# ------------------

def check_element_displayed(self, locator):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    return element.is_displayed()

def check_element_disabled(driver, locator):
    element = WebDriverWait(driver, DD_TIMEOUT).until(EC.presence_of_element_located(locator))
    if not element.is_enabled():
        return True  # Element is not enabled
    else:
        raise Exception(" selected element is enabled, cannot proceed with further code.")

def check_element_enabled(driver, locator):
    element = WebDriverWait(driver, DD_TIMEOUT).until(EC.presence_of_element_located(locator))
    if element.is_enabled():
        return True
    else:
        raise Exception("selected element is not enabled, cannot proceed with further code.")


def check_element_not_displayed(self, locator):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.invisibility_of_element_located(locator))
    return element


def get_selected_option_from_dropdown(self, locator):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    option = Select(element)
    value = option.first_selected_option
    return value.text

def get_input_text(self, locator):
    element = WebDriverWait(self.driver, DD_TIMEOUT).until(EC.visibility_of_element_located(locator))
    return element.get_attribute('value')
# ------------------
# Send Keyboard Keys
# ------------------
def send_keyboard_keys(self,locator,key_name):
     element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(
        EC.visibility_of_element_located(locator)
    )
     try:
         if key_name == "backspace":
            element.send_keys(Keys.BACKSPACE)
         if key_name == "enter":
            element.send_Key(Keys.ENTER)
         if key_name == "tab":
            element.send_Key(Keys.TAB)
     except:
        print("Got an exception")


def upload_file(self, locator, path):
    element = WebDriverWait(self.driver, TEXT_TIMEOUT).until(EC.presence_of_element_located(locator))
    element.send_keys(path)


def get_option_value(self, locator, text):
    element = WebDriverWait(self.driver, DEFAULT_TIMEOUT).until(EC.visibility_of_element_located(locator))
    Select(element).select_by_visible_text(text)
    return element.get_attribute('value')

def press_end_key(self):
    actions = ActionChains(self.driver)
    actions.send_keys(Keys.END).perform()

def press_backspace_key(self):
    actions = ActionChains(self.driver)
    actions.send_keys(Keys.BACKSPACE).perform()

def press_ctrl_plus_key(self, key):
    actions = ActionChains(self.driver)
    actions.key_down(Keys.CONTROL).send_keys(key).key_up(Keys.CONTROL).perform()

def switch_to_active_element_and_enter_text(self, text):
    active_element = self.driver.switch_to.active_element
    active_element.send_keys(text)

def press_enter_key(self):
    actions = ActionChains(self.driver)
    actions.send_keys(Keys.ENTER).perform()