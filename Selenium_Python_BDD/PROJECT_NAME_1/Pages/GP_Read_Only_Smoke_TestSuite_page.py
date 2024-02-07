from libraries.environment_setup import EnvironmentSetup
from selenium.webdriver.support import expected_conditions as EC
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from GP.utilities.logs_util import logger
import allure
from allure_commons.types import AttachmentType
import time
import os
import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from libraries import generics


class ReadOnlySmokeTestSuitePage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        
        # locators
        
  
    """Author : Sadiya Kotwal
       Description : This method verify the selected Screen
       Arguments : screen_name(Eg: screen_name="Approval")
       Returns : NA""" 
    def verify_selected_screen(self,screen_name):
        self.screen_name = screen_name
        MainPage.verify_screen_name(self,self.screen_name)
        generics.capture_screenshot_allure(self.main, screen_name)

    """Author : Sadiya Kotwal
       Description : This method verify the selected Screen
       Arguments : screen_name(Eg: screen_name="Approval")
       Returns : NA""" 
    def verify_screen_name(self,screen_name):
        self.screen_name = screen_name
        self.bln_flag=False
        self.txt_screen_name = "//ul[@role='tablist']//li/child::a[@class='nav-link active'][contains(.,'"+self.screen_name+"')]"
        self.bln_flag = locators.element_is_displayed(self,"XPATH", self.txt_screen_name)
        if self.bln_flag == True:
            allure.attach("User is on "+screen_name+" screen",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the "+screen_name+" screen"
        generics.capture_screenshot_allure(self.main, screen_name)
