import os
import shutil
import allure
from deepdiff import DeepDiff
from allure_commons.types import AttachmentType
from libraries import locators
import random
import string
import json
from sparc_pages.decorators import wait_for_loader


# ---------------
# Allure Reports
# ---------------

@wait_for_loader
def capture_screenshot_allure(page_object, image_name):
    allure.attach(page_object.driver.get_screenshot_as_png(), name=f"{image_name}.png",
                  attachment_type=AttachmentType.PNG)


def delete_allure_specific_folder(self, folder):  ## Send the name folder or path of the folder to delete
    while True:
        try:
            if self.attempts_allure == 0:
                for x in os.walk(os.getcwd()):
                    is_folder = x[0].find(folder)
                    is_allure = x[0].find("%allure_result_folder%")
                    if is_folder != -1 and is_allure != -1:
                        shutil.rmtree(x[0])
                        if not os.path.exists(x[0]):
                            os.makedirs(x[0])
                            break
                self.attempts_allure += 1
                return self.attempts_allure
            else:
                self.attempts_allure = 1
                return self.attempts_allure
                break
        except:
            self.attempts_allure = 0


def allure_logs(text):
    with allure.step(text):
        pass

# ----------------
# Browser Drivers
# ----------------


def get_path_driver(self):
    self.path_to_cut = os.getcwd()
    self.temp1 = self.path_to_cut.find("framework/")
    if self.temp1 != -1:
        self.temp1 = self.path_to_cut.find("framework") + 10
        self.length = len(self.path_to_cut)
        self.path = self.path_to_cut[self.temp1:self.legth]
        self.path_driver = self.path_to_cut.replace(self.path, "Drivers/chromedriver")
        return self.path_driver
    else:
        path_behave = self.path_to_cut + "/Drivers/chromedriver"
        return path_behave


# ----------------
# HTML Elements
# ----------------

def set_attribute_value_by_javascript(self, locator_type, locator, attribute, value):
    web_element = locators.locator_element(self, locator_type, locator)
    self.driver.execute_script("arguments[0].setAttribute('" + attribute + "', '" + value + "')", web_element)


def set_text_value_by_javascript(self, locator_type, locator, value):
    web_element = locators.locator_element(self, locator_type, locator)
    self.driver.execute_script('arguments[0].textContent = "' + value + '"', web_element)


# -----------------------
# Dictionaries
# -----------------------

def get_list_of_attribute_values(object_list, attribute):
    new_list = [element[attribute] for element in object_list]
    return new_list


def compare_dicts(dict1, dict2):
    differences = DeepDiff(dict1, dict2, ignore_order=True)
    if len(differences) == 0:
        return True
    else:
        return differences


def remove_dict_key(d, key):
    new_dict = dict(d)
    del new_dict[key]
    return new_dict


def get_random_string(lenght):
    int_lenth=int(lenght)
    randon_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = int_lenth))   
    return randon_string