from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import time
import os
from selenium.webdriver.common.by import By
from libraries import generics



class ViewDataPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators
        self.Page = "//div[@id= 'output-controls']/div[1]/select"
        self.DatatypeDropdown = "//div[@id= 'output-controls']/div[2]/select/option"
        self.DataType = "//div[@id= 'output-controls']/div[3]/select"
        self.Export = "//button[@title='Export']"
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        #buttons
        self.icon_calender = "//span[@class='mydpicon icon-mydpcalendar']"
        self.btn_export = "//button[@title='Export']"

        
    def select_product_from_burger_menu(self):
        self.main.select_gp_option('VIEW DATA')
        self.main.screen_load_time('View Data Screen')
        allure.attach("User see select view data menu : ",attachment_type=allure.attachment_type.TEXT)
        
    def click_on_view_data_dropdown(self, Pages, Data):
        self.Pages = Pages
        self.Data = Data
        forms.select_option_by_text(self, "XPATH", self.Page , self.Pages)
        allure.attach("Selected Page count is: "+self.Pages,attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self, "XPATH", self.DataType, self.Data)
        allure.attach("Selected Data is: "+self.Data,attachment_type=allure.attachment_type.TEXT)
        
    def click_on_product_download_button(self):
        mouse.click_action_on_element(self, "XPATH", self.Export)
        allure.attach("Clicked on Export",attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time("View Data->Export")
        
    """Author : Sadiya Kotwal
       Description : This method verify the calender icon
       Arguments : 
       Returns : NA""" 
    def verify_calender_icon(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.icon_calender)
        if self.bln_flag == True:
            allure.attach("User see calender icon : ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the Calender Icon"

    """Author : Sadiya Kotwal
       Description : This method verify the export button
       Arguments : 
       Returns : NA""" 
    def verify_export_button(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.btn_export)
        if self.bln_flag == True:
            allure.attach("User see export button : ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the Export Button"