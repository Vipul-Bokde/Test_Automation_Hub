from libraries import mouse, browser, locators
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime
import GP.utilities.Repo as Repo
from GP.utilities.logs_util import logger
import os
from datetime import date
from libraries import forms
import random
import string
import allure
from libraries import generics
from GP.pages.login_page import Login
from GP.utilities.database_connection import SqlConnection
import json
import secrets

class MainPage:

    #locators
    burger = "//div[@class='btn-group']/button[@data-toggle='dropdown']/i[@class='fa fa-bars']"
    gp_item = "//li[contains(.,'{}')]"
    gp_sub_item = "//li[contains(.,'{}')]/ul/li[contains(.,'{}')]"
    load_bar = "//div[@class='load-bar']/div[@class='bar'][1]"
    render = "//div[@class='card-body']/div/i"
    ui_client_name = "//div[@id='header-client']/h4"
    validation_render = "//div[@id='no-validations']/p/i"
    error_msg = "//alert/div[@class='alert alert-warning alert-dismissible']"
    date_warning = "//alert/div[@id='alert'][contains(.,'Select start and end date.')]"
    source_warning = "//alert/div[@id='alert'][contains(.,'Select at least 1 validation source.')]"
    greater_date_warning  = "//alert/div[@id='alert'][contains(.,'End date must be greater than start date.')]" 
    validate_pop_up_button = "//div[@class='sparq-modal-footer upper-margin ']/button[@id="'{}'"]"
    search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"

    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(self.driver)                 

    def select_gp_option(self, item, sub_item=None):
        if sub_item is None:
            self.open_burger_menu()
            mouse.click_on_element(self, 'XPATH', self.gp_item.format(item))
        else:
            self.open_burger_menu()
            mouse.scroll_to_element(self, 'XPATH', self.gp_item.format(item))
            mouse.click_on_element(self, 'XPATH', self.gp_sub_item.format(item, sub_item))

    def open_burger_menu(self):
        MainPage.wait_until_element_is_present(self, 5, By.XPATH, self.burger,"Burger menu not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.burger)

    def refresh(self):
        browser.refresh(self)

    def wait_until_element_is_present(self, timeout, locator_type, locator,message):
        WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((locator_type, locator)),message)
    
    # To Create Client name folder and file
    def file_name(self):
        element = self.driver.find_element_by_xpath(self.ui_client_name)
        self.client_name_ui = forms.get_text_on_element(self,"XPATH",self.ui_client_name)
        self.client_name =r'\{}'.format(self.client_name_ui)
        cur_date = date.today()
        cur_date = str(cur_date).replace("-","")
        if not os.path.exists((Repo.QA_GP_Client+self.client_name)):
              os.mkdir(Repo.QA_GP_Client+self.client_name)
        self.client_file_name = self.client_name+self.client_name+'_'+str(cur_date)+'_'+str(datetime.datetime.today().strftime("%I_%p"))+'.txt'
        self.download_file_loc = Repo.QA_GP_Client+self.client_file_name
        self.download_file_loc= r"{}".format(self.download_file_loc)
        return self.download_file_loc
    
    # To capture screen load time and store into file
    def screen_load_time(self,page_name):
        self.page_name = page_name
        self.start_time = time.perf_counter()
        locators.wait_until_invisibility_of_element(self, By.XPATH, self.load_bar)
        self.end_time = time.perf_counter()
        self.total_time =self.end_time-self.start_time
        list = {"Page Name " : self.page_name,"Start Time ":self.start_time,"End Time ":self.end_time,"Total Load Time ":datetime.timedelta(seconds=self.total_time)}
        self.download_file_loc = self.file_name()
        with open(self.download_file_loc, 'a') as f:
            for key, value in list.items(): 
                f.write('%s:%s\n' % (key, value))
                logger.info('%s:%s' % (key, value))
            f.write('\n')

    # For Smoke Test Data Overview-> validation error render icon time capture
    def kick_off_render(self,page_name):
        self.page_name = page_name
        self.start_time = time.perf_counter()
        locators.wait_until_invisibility_of_element(self, By.XPATH, self.render)
        self.end_time = time.perf_counter()
        self.total_time =self.end_time-self.start_time
        list = {"Page Name " : self.page_name,"Start Time ":self.start_time,"End Time ":self.end_time,"Total Load Time ":datetime.timedelta(seconds=self.total_time)}
        self.download_file_loc = self.file_name()
        with open(self.download_file_loc, 'a') as f:
            for key, value in list.items(): 
                f.write('%s:%s\n' % (key, value))
                logger.info('%s:%s' % (key, value))
            f.write('\n')
            


    def get_random_string(self,length):
        self.int_length=int(length)
        self.random_string = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k = self.int_length))
        return self.random_string
    
    def get_system_current_date(self,date_format):
        system_current_date = date.today()
        system_date = system_current_date.strftime(date_format)
        return system_date
    
    # Validation Time capture and Error message handling 
    def validation_time_capture(self,page_name):
        self.page_name = page_name
        self.start_time = time.perf_counter()
        try:
            self.element =  self.driver.find_element_by_xpath(self.error_msg)
            if self.element.is_displayed() == True:
                try:
                    self.source_warning_msg =  self.driver.find_element_by_xpath(self.source_warning)
                    if self.source_warning_msg.is_displayed() == True:
                        self.warning = forms.get_text_on_element(self,By.XPATH,self.source_warning)
                        logger.info("Error Message: "+ self.warning)
                        mouse.click_on_element(self,"XPATH",self.validate_pop_up_button.format("'validate-cancel-btn'"))   
                except:
                    logger.info("Source selected Correctly") 
                    
                try:    
                    self.date_warning_msg =  self.driver.find_element_by_xpath(self.date_warning)
                    if self.date_warning_msg.is_displayed() == True :
                        self.warning = forms.get_text_on_element(self,By.XPATH,self.date_warning)
                        logger.info("Error Message: "+ self.warning) 
                        mouse.click_on_element(self,"XPATH",self.validate_pop_up_button.format("'validate-cancel-btn'"))
                except:
                    logger.info("Period selected Correctly") 
                
                try:    
                    self.greater_date_warning_msg =  self.driver.find_element_by_xpath(self.greater_date_warning)
                    if self.greater_date_warning_msg.is_displayed() == True :
                        self.warning = forms.get_text_on_element(self,By.XPATH,self.greater_date_warning)
                        logger.info("Error Message: "+ self.warning) 
                        mouse.click_on_element(self,"XPATH",self.validate_pop_up_button.format("'validate-cancel-btn'"))
                except:
                    logger.info("Date Range selected Correctly") 
        except:
            logger.info("No Error message")
            locators.wait_until_invisibility_of_element(self, By.XPATH, self.load_bar)
            locators.wait_until_invisibility_of_element(self, By.XPATH, self.validation_render)
            self.end_time = time.perf_counter()
            self.total_time =self.end_time-self.start_time
            list = {"Page Name " : self.page_name,"Start Time ":self.start_time,"End Time ":self.end_time,"Total Load Time ":datetime.timedelta(seconds=self.total_time)}
            self.download_file_loc = self.file_name()
            with open(self.download_file_loc, 'a') as f:
                for key, value in list.items(): 
                    f.write('%s:%s\n' % (key, value))
                    logger.info('%s:%s' % (key, value))
                f.write('\n')
                
        return self.error_msg
    
    def click_on_any_filter_icon(self,column_name):
        self.column_name = column_name
        self.icon_filter = "//span[text()='"+self.column_name+"']/ancestor::div[contains(@class,'ag-cell-label-container')]/span"
        mouse.click_on_element(self,"XPATH",self.icon_filter)
        allure.attach("User can click on filter icon for column : "+self.column_name,attachment_type=allure.attachment_type.TEXT)
    
    def enter_text_on_any_filter_icon_search_box(self,filter_text):
        self.txt_to_enter_in_filter = filter_text
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.txt_to_enter_in_filter)
        allure.attach("User can enter data as : "+self.txt_to_enter_in_filter,attachment_type=allure.attachment_type.TEXT)
        return self.txt_to_enter_in_filter
    
    """Author : Sadiya Kotwal
       Description : This method verify the  screen name
       Arguments : screen_name(EG: screen_name="Runs")
       Returns : NA""" 
    def verify_screen_name(self,screen_name):
        self.screen_name = screen_name
        self.bln_flag=False
        self.txt_screen_name = "//span[text()='"+self.screen_name+"']"
        self.bln_flag = locators.element_is_displayed(self,"XPATH", self.txt_screen_name)
        if self.bln_flag == True:
            allure.attach("User is on "+screen_name+" screen",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the "+screen_name+" screen"
    
    """Author : Sadiya Kotwal
       Description : This method clicks on text of any screen
       Arguments : screen_name (Eg: Price type editor,Runs Screen)
       Returns : NA"""
    def click_on_any_screen_text(self,screen_name):
        self.screen_name = screen_name
        self.txt_page_name = "//span[text()='"+self.screen_name+"']"
        mouse.click_on_element(self, "XPATH", self.txt_page_name)
        allure.attach("User can click on screen : "+self.screen_name,attachment_type=allure.attachment_type.TEXT)

    
    """Author : Pooja Jundhare
       Description : This method returns the client id from md.client table based on given client name
       Arguments :  sql query from testdata sheet (Eg: select id from md.client c where pretty_name ='${client_name}';)
       Returns : client_id"""
    def get_client_id(self,sql_query):
        self.client_name_ui = forms.get_text_on_element(self,"XPATH",self.ui_client_name)
        self.updated_query = sql_query.replace('${client_name}', self.client_name_ui)
        logger.info("Client id query is:"+self.updated_query)
        allure.attach("SQL Query Updated  : "+self.updated_query,attachment_type=allure.attachment_type.TEXT)
        self.query_result = SqlConnection.connection(self.updated_query) 
        query_json_result = json.dumps(self.query_result, default=str, sort_keys=True)
        allure.attach("SQL Result Set: " +query_json_result, attachment_type=allure.attachment_type.JSON)
        return self.query_result

    """Author : Sadiya Kotwal
       Description : This method generates a random string of numbers
       Arguments : length (Eg: length= 4 or 5)
       Returns : self.random_string_of_numbers(random_string_of_numbers='12345')"""
    def get_random_string_of_numbers(self,length):
        self.int_length=int(length)
        self.random_string_of_numbers = ''.join(secrets.choice(string.digits) for x in range(self.int_length)) 
        return self.random_string_of_numbers
   