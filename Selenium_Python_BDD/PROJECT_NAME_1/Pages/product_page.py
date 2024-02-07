from cmath import log
import imp
from lib2to3.pgen2 import driver
import re
# from curses.ascii import TAB
from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from GP.pages.approvals_page import ApprovalsPage
from selenium.webdriver.common.keys import Keys
from GP.utilities.logs_util import logger
import allure
from allure_commons.types import AttachmentType
import os
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from GP.utilities.logs_util import logger
# from selenium.webdriver.support.ui import WebDriverWait
from datetime import date
from selenium.webdriver.common.by import By
from libraries import generics




class ProductPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        # locators
        self.Upload = "//div[@class='float-right']/button[@class='btn btn-primary']"
        self.File_Type = "//div[@class='sparq-modal']/form/div[2]/div[2]/select"
        self.UseTempleteCheckbox = "//div[@formgroupname='gp']/input[@id='use_template']"
        self.FileUpload = "//div[@class='form-group']/input[@id='upload-file-chooser']"
        self.Submit = "//div[@class='sparq-modal-footer']/button[@id='upload-submit-btn']"
        self.green_stack  = "//div[@row-index='0']/div[@col-id='status']/span/span/i[@class='text-success fa fa-database']"
        self.FileName = "//div[@class='ag-center-cols-container']/div[@row-index='0']/div[@col-id='filename']"
        self.ndc11 = "//div[@row-index='0']/div[@col-id='ndc11']"
        self.product_name = "//div[@row-index='0']/div[@col-id='product_summary_name']"
        self.hamburger_icon = "(//div[@class='btn-group']/button[@class='btn btn-secondary menu-btn-group'])[1]"
        self.approval = "//div[@class='btn-group show']/ul/li/a[contains(text(),'APPROVALS')]"
        self.client = "(//div[@class='btn-group show']/ul/li/a/span)[2]"
        self.upload_wait_screen = "(//div[@class='ag-header-cell'])[1]"
        self.product = "//div[@class='btn-group show']/ul/li/ul/li/a[contains(text(),'PRODUCT')]"
        self.ndc_search = "//div[@col-id='ndc11']/div[contains(@class,'ag-cell-label-container')]/span"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']" 
        self.changes_tab = "//ul[@class='nav nav-tabs']/li/a/strong[contains(text(),'Revision History')]"
        self.modified_by = "//div[@row-index='0']/div[@col-id='0']"
        self.modified_on = "//div[@row-index='0']/div[@col-id='modified_on']"
        self.approved_by = "//div[@row-index='0']/div[@col-id='1']"
        self.approved_on = "//div[@row-index='0']/div[@col-id='approved_on']"
        self.user_icon = "(//div[@class='btn-group']/button[@class='btn btn-secondary menu-btn-group'])[2]"
        self.log_out_btn = "(//div[@class='btn-group show']/ul[@class='dropdown-menu dropdown-menu-right show']/li/a)[5]"
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        #buttons
        self.btn_export = "//export//button[@title='Export']/i"
        self.btn_upload = "//button//i[@title='Upload file']"

    def select_upload_from_burguer_menu(self):
        self.main.screen_load_time('Data Overview Screen')
        self.main.select_gp_option('UPLOADS')
        self.main.screen_load_time('UPLOADS Screen')
        allure.attach("User can select uploads menu: ",attachment_type=allure.attachment_type.TEXT)

    
    def click_on_upload_button(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Upload,"Upload Button element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.Upload)
        self.driver.execute_script("$(arguments[0]).click();", element)  

    def select_file_type(self):
        self.main.screen_load_time('Upload ->File Type')
        self.FileType = "Product"
        forms.select_option_by_text(self, "XPATH", self.File_Type , self.FileType)
        logger.info("Select Filetype from dropdown : " + self.FileType)

    def click_on_checkbox(self):
        forms.uncheck_checkbox(self, "XPATH" , self.UseTempleteCheckbox)

    def upload_file(self,file_to_upload):
        self.file_to_upload = file_to_upload
        file_up = self.driver.find_element_by_xpath(self.FileUpload)
        file_up.send_keys(self.file_to_upload)

    def click_on_submit_button(self):
        mouse.click_on_element(self,"XPATH", self.Submit)
        self.main.screen_load_time('UPLOADS Submit')

    def get_ndc11_and_product_name(self):
        upload_list=[]
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.green_stack,"Green Stack icon not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.FileName)
        self.driver.execute_script("$(arguments[0]).click();", element) 
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.upload_wait_screen,"Upload wait screen element not found on Webpage in given wait time.")
        self.ndc11_value = forms.get_text_on_element(self,"XPATH",self.ndc11)
        upload_list.append(self.ndc11_value)
        self.product_name_value = forms.get_text_on_element(self,"XPATH",self.product_name)
        upload_list.append(self.product_name_value)
        logger.info(self.ndc11_value)
        logger.info(self.product_name_value)
        return upload_list
        
    def log_out(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.user_icon,"User icon not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.user_icon)
        mouse.click_on_element(self,"XPATH",self.log_out_btn)

    def goto_changes_tab(self,ndc11_value):
        self.ndc11_value = ndc11_value
        self.main.select_gp_option('CLIENT',sub_item="PRODUCTS")
        self.main.screen_load_time('CLIENT->PRODUCTS')
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.ndc_search,"NDC search element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.ndc_search)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.ndc11_value)
        mouse.click_on_element(self, "XPATH",self.ndc11)
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.changes_tab,"Changes tab element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.changes_tab)

    def validate_changes_tab(self,approved_by,modified_by):
        self.modified_by_xl = modified_by
        self.approved_by_xl = approved_by
        logger.info("XL modified by",self.modified_by_xl)
        logger.info("XL Approved by",self.approved_by_xl)
        self.modified_on_xl = date.today()
        self.approved_on_xl = date.today()
        self.modified_by = forms.get_text_on_element(self,"XPATH",self.modified_by)
        logger.info("UI modified by",self.modified_by)
        self.modified_on = forms.get_text_on_element(self,"XPATH",self.modified_on)
        self.approved_by = forms.get_text_on_element(self,"XPATH",self.approved_by)
        logger.info("UI approved by",self.approved_by)
        self.approved_on = forms.get_text_on_element(self,"XPATH",self.approved_on)
        assert str(self.modified_by) == str(self.modified_by_xl) , "Modified_by does not match"
        assert str(self.modified_on) == str(self.modified_on_xl) , "modified_on does not match"
        assert str(self.approved_by) == str(self.approved_by_xl) , "approved_by does not match"
        assert str(self.approved_on) == str(self.approved_on_xl) , "approved_on does not match"

    """Author : Sadiya Kotwal
       Description : This method select sub menu products
       Arguments : screen_name(screen_name="Uploads")
       Returns : NA""" 
    def select_products_submenu_from_burguer_menu(self):
        self.main.select_gp_option('CLIENT', sub_item='PRODUCTS')
        self.main.screen_load_time('CLIENT->PRODUCTS Screen')
        allure.attach("User can select clients menu and products as sub menu: ",attachment_type=allure.attachment_type.TEXT)
    
    """Author : Sadiya Kotwal
       Description : This method verify the export button on product page
       Arguments : 
       Returns : NA""" 
    def verify_export_button(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.btn_export)
        if self.bln_flag == True:
            allure.attach("User see export button on product page: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the Export Button"

    """Author : Sadiya Kotwal
       Description : This method verify the upload button on product page
       Arguments : 
       Returns : NA""" 
    def verify_upload_button(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.btn_upload)
        if self.bln_flag == True:
            allure.attach("User see upload button on product page: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the Upload Button"