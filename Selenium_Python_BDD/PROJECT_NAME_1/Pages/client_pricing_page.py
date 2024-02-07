from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import os
from GP.utilities.logs_util import logger
from libraries import mouse
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from libraries import generics



class ClientPricingPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators
        self.btn_export = "//div[@class='btn-group float-right']/button/i"
        self.btn_upload = "//button//i[@title='File Upload']"

    """Author : Sadiya Kotwal
       Description : This method verify the client ->pricing Screen
       Arguments : screen_name(Eg: screen_name="Pricing")
       Returns : NA""" 
    def select_pricing_sub_menu_from_burguer_menu(self):
        self.main.select_gp_option('CLIENT', sub_item='PRICING')
        self.main.screen_load_time('CLIENT->PRICING Screen')
        allure.attach("User can select client menu and pricing as sub menu: ",attachment_type=allure.attachment_type.TEXT)
        
    """Author : Sadiya Kotwal
       Description : This method verify the export button on pricing page
       Arguments : 
       Returns : NA""" 
    def verify_export_button(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.btn_export)
        if self.bln_flag == True:
            allure.attach("User see export button on pricing page: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the Export Button"

    """Author : Sadiya Kotwal
       Description : This method verify the upload button on pricing page
       Arguments : 
       Returns : NA""" 
    def verify_upload_button(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.btn_upload)
        if self.bln_flag == True:
            allure.attach("User see upload button on pricing page: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the Upload Button"