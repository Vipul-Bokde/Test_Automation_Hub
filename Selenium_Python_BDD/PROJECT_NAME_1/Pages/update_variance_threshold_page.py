from ast import keyword
import time
import behave
import random
from libraries.environment_setup import EnvironmentSetup
from GP.pages.main_page import MainPage
from libraries import mouse, forms
from GP.utilities.logs_util import logger
from GP.pages.price_type_delete_page import DeletePriceTypePage
from GP.pages.login_page import Login
from selenium.webdriver.common.by import By
import allure

class UpdateVarianceThresholdPage(EnvironmentSetup):
    
    
    # locators
    rules_tab = "//*[@id='rules-tab']/a"
    submit_btn = "//div[@class='p-5']/button[contains(text(),'Submit')]"
    x = "/html/body/div[2]/div[1]/button" # need to remove after merge
    variance_threshold_name = "//*[@id='top-container']/split/split-area[1]/rule-editor/div/div[3]/div[1]/div"
    edit_button ="//div[@class='pl-5 pr-5 pt-5 mb-2']/button[@id='btn-save-record']"

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        self.login = Login(self.driver)
    
    def click_on_price_type(self,price_type):
        self.price_type = price_type
        self.price_type_name_list = []
        self.rowxpath_price_type = DeletePriceTypePage.rowxpath_price_type 
        self.price_type_name_list = self.driver.find_elements_by_xpath(self.rowxpath_price_type)  
        logger.info(self.price_type_name_list)
        logger.info(len(self.price_type_name_list))
        self.list_length = len(self.price_type_name_list)
        for i in range(0,self.list_length):
            self.price_name_list = "//div[@class='ag-center-cols-container']/div[@row-id="+str(i)+"]/div[@col-id='name']"
            logger.info(self.price_name_list)
            self.column_text = forms.get_text_on_element(self, "XPATH", self.price_name_list)
            logger.info(self.price_name_list)
            if self.column_text == self.price_type:
                mouse.click_on_element(self,'Xpath',self.price_name_list)
                allure.attach("Selected Price Type is: "+self.column_text,attachment_type=allure.attachment_type.TEXT)
                self.main.screen_load_time('Price Type')
                break
    
    def click_on_rules_tab(self):
        mouse.click_on_element(self,'Xpath',self.edit_button)
        self.main.screen_load_time('Price Type->Edit')
        mouse.click_on_element(self,'Xpath',self.rules_tab)
        allure.attach("Clicked on Rules Tab.",attachment_type=allure.attachment_type.TEXT)
    
    def update_threshold(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.x,"x element not found on Webpage in given wait time.")
        mouse.click_on_element(self,'XPATH',self.x) # need to remove after merge
        self.variance_threshold_name_list = []
        self.rowxpath_variance_threshold_type = self.variance_threshold_name 
        self.variance_threshold_name_list = self.driver.find_elements_by_xpath(self.rowxpath_variance_threshold_type)
        logger.info(len(self.variance_threshold_name_list))
        self.list_length = len(self.variance_threshold_name_list)
        if(self.list_length>0):
            for i in range(self.list_length):
                allure.attach("Loop is: "+str(i),attachment_type=allure.attachment_type.TEXT)
                self.dollar_threshold = "(//*[@id='dollar-threshold'])["+str(i+1)+"]"
                logger.info(self.dollar_threshold)
                dollar_threshold = random.randint(0,9)
                forms.enter_text_on_element(self,'XPATH',self.dollar_threshold,str(dollar_threshold))
                allure.attach("Entered Dollar threshold value is: "+str(dollar_threshold),attachment_type=allure.attachment_type.TEXT)
                self.unit_threshold = "(//*[@id='unit-threshold'])["+str(i+1)+"]"
                logger.info(self.unit_threshold)
                unit_threshold = random.randint(0,9)
                forms.enter_text_on_element(self,'XPATH',self.unit_threshold,str(unit_threshold))
                allure.attach("Entered Unit threshold value is: "+str(unit_threshold),attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info("Variance Threshold not found")
            allure.attach("Variance Threshold not found",attachment_type=allure.attachment_type.TEXT)
            self.login.close_browser()
            exit(0)        
            
    def click_on_submit(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.submit_btn,"Submit Button element not found on Webpage in given wait time.")
        mouse.click_on_element(self,'XPATH',self.submit_btn)
        allure.attach("Submitted Variance Threshold values",attachment_type=allure.attachment_type.TEXT)



    



    
        


    
    
