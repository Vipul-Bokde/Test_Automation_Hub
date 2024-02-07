from libraries import forms, mouse
import time
from GP.pages.main_page import MainPage
from selenium.webdriver.common.by import By


class SparcServices:

    #locators
    client = "(//div[@class='form-group']/label)[1]"
    client_name = "client-selector"
    service_name = "service-selector"
    submit_button = "//button[contains(.,'Submit')]"

    def __init__(self, driver):
        self.driver = driver


    def select_client(self, client):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.client,"Client element not found on Webpage in given wait time.")
        forms.select_option_by_text(self, "ID", self.client_name, client)

    def select_service(self, service):
        forms.select_option_by_text(self, "ID", self.service_name, service)

    def click_on_submit_button(self):
        mouse.click_on_element(self, "XPATH", self.submit_button)