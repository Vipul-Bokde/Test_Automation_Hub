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

class Smoke_Test_page(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        
        # locators
        self.missing_customerid = "//div[@class='card m-2 d-lg-inline-flex']/div[contains(text(),'Missing CustomerIDs')]"
        self.missing_phs = "//div[@class='card m-2 d-lg-inline-flex']/div[contains(text(),'Missing PHSResults')]"
        self.missing_contract = "//div[@class='card m-2 d-lg-inline-flex']/div[contains(text(),'Missing Contracts')]"
        self.kickoff_cot = "//div[@class='card-body']/button[contains(text(),'Kickoff COT Research')]"
        self.kickoff_phs = "//div[@class='card-body']/button[contains(text(),'Kickoff PHS Research')]"
        self.create_record_for_contract = "//div[@class='card-body']/button[contains(text(),'Create Records for Contract')]"
        self.render = "//div[@class='card-body']/div/i"
        self.download_results = "//div[@class='card-body']/button[contains(text(),'Download Results')]"
        self.select_run = "(//span[@id='container']/span)[2]"
        self.Variance_Btn = "//div/button[@id= 'var-failure-btn']"
        self.V_Bucket_Check_Box= "((//div[@ref= 'eCenterContainer'])[2]/div/div/span/span)[1]"
        self.V_Comment_Btn = "//div/button[@id = 'show-notes']"
        self.V_Add_Note_Btn = "//div/button[@id='add-note-button']"
        self.V_Note_Text_Box = "//tbody/tr/td[@class='col-md-7']/textarea[@type='text']"
        self.V_Note_Save_Btn = "//td/button[@id='save-note']"
        self.V_Note_cancel_btn = "//div/button[@id= 'hide-note-button']"
        self.V_Cancel_btn = "//div/button[@id='hide-var-failures-button']"
        self.V_Export = "//div/button[@title='Export']"
        # Summary Tab  
        self.Summary_Tab = "//div/uL[@id='run-price-type-tabs']/li[1]"
        self.Summary_Approve_Btn = "//div[@class= 'btn-toolbar']/div/button[@title= 'Approve']"
        self.Summary_Rollback_Btn = "//div[@class= 'btn-toolbar']/div/button[@title= 'Rollback']"
        self.Summay_Prior_Delivered_Btn = "//div[@class= 'btn-toolbar']/div/button[@title= 'Prior Delivered']"
        self.Summay_Prior_Close_Btn = "(//div/button[@class='btn btn-primary'][@type='button'])[1]"
        self.Finalization_Delivered = "//div[@class= 'btn-toolbar']/div/button[@title= 'Deliver']"
        
        self.Summay_Attachments_btn = "//div[@class= 'btn-toolbar']/div/button[@id= 'run-attachment-btn']"
        self.Summay_Attachments_Add_Btn = "(//div/button[@class='btn btn-primary'][@type='button'])[2]"
        self.Summay_Choose_File = "//div/input[@id= 'attachment-file']"
        self.Summay_File_Upload_Btn = "(//div/button[@type='submit'])[2]"
        self.Summay_Attachments_close_Btn = "(//div/button[@class='btn btn-secondary'][@type='button'])[3]"
        
        self.Summary_Comments_btn = "//div/button[@id= 'restore-sort']"
        self.Summary_Add_Note_btn = "//div/button[@id='add-note-button']"
        self.Summary_Message_Txt_Box= "(//tbody/tr/td[@class='col-md-7']/textarea[@type='text'])[2]"
        self.Summay_Save_Note_Btn = "(//td/button[@id='save-note'])[2]"
        self.Summay_Cancel_Note_Btn = "//div/button[@id='hide-note-button']"        
        self.Summay_Run_Report_Btn = "//div[@class= 'btn-toolbar']/div/button[@title='Run Report']"
        self.Summay_Export_Btn = "//div[@class= 'btn-toolbar']/div/button[@title='Export']"
  
    def select_run_option(self):
        self.main.screen_load_time('Data Overview Screen')
        element = self.driver.find_element_by_xpath(self.select_run)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Select Run Screen')

    
    def click_on_the_variance_button(self, Message):
        self.Message = Message
        mouse.click_on_element(self, "XPATH", self.Variance_Btn) 
        self.login = Login(self.driver)
        try:
            forms.check_checkbox(self, "XPATH", self.V_Bucket_Check_Box)
            mouse.click_on_element(self, "XPATH", self.V_Comment_Btn)
            mouse.click_on_element(self, "XPATH", self.V_Add_Note_Btn)
            forms.enter_text_on_element(self, "XPATH", self.V_Note_Text_Box, Message)
            mouse.click_on_element(self, "XPATH", self.V_Note_Save_Btn)
            mouse.click_on_element(self, "XPATH", self.V_Note_cancel_btn)
            mouse.click_on_element(self, "XPATH", self.V_Cancel_btn)
            mouse.click_action_on_element(self, "XPATH", self.V_Export)
        except AttributeError:
            mouse.click_on_element(self, "XPATH", self.V_Cancel_btn)

    def Summary_buttons_Operation(self, Message):
        self.Message = Message
        mouse.click_on_element(self, "XPATH", self.Summay_Prior_Delivered_Btn)
        mouse.click_on_element(self, "XPATH", self.Summay_Prior_Close_Btn)
        mouse.click_on_element(self, "XPATH", self.Summay_Attachments_btn)
        mouse.click_on_element(self,"XPATH", self.Summay_Attachments_Add_Btn)
        file_up = self.driver.find_element_by_xpath(self.Summay_Choose_File)
        file_up.send_keys(os.getcwd() + "/GP/automation_test/uploadfiles/Data_Summary_Report.xlsm") 
        mouse.click_on_element(self, "XPATH", self.Summay_File_Upload_Btn)
        mouse.click_on_element(self, "XPATH", self.Summay_Attachments_close_Btn)
              
        mouse.click_on_element(self,"XPATH", self.Summary_Comments_btn)
        mouse.click_on_element(self, "XPATH", self.Summary_Add_Note_btn)
        forms.enter_text_on_element(self, "XPATH", self.Summary_Message_Txt_Box, Message)
        mouse.click_on_element(self,"XPATH", self.Summay_Save_Note_Btn)
        mouse.click_on_element(self,"XPATH", self.Summay_Cancel_Note_Btn)  
        mouse.click_on_element(self,"XPATH", self.Summay_Run_Report_Btn)
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Summay_Export_Btn,"Summary Export element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH", self.Summay_Export_Btn)
        
    def validation_errors(self):
        self.main.screen_load_time('Data Overview Wait')
        try:
            self.element = self.driver.find_element_by_xpath(self.missing_contract)
            if self.element.is_displayed() == True:
                mouse.click_on_element(self,"XPATH", self.create_record_for_contract)
                self.main.screen_load_time('Create Records for Contract')
                locators.wait_until_invisibility_of_element(self, By.XPATH, self.render)
                self.main.screen_load_time('Download results for Create Records for Contract')
        except :
            pass   
        try:
            element = self.driver.find_element_by_xpath(self.missing_phs)
            if  element.is_displayed() == True:
                mouse.click_on_element(self,"XPATH", self.kickoff_phs)
                self.main.screen_load_time('Kickoff PHS Research')
                self.main.kick_off_render('Kickoff PHS Research->Render')
                mouse.click_on_element(self,"XPATH", self.download_results)
                self.main.screen_load_time('Download results for Kickoff PHS Research')
        except:
            pass            
        try:
            element = self.driver.find_element_by_xpath(self.missing_customerid)
            if  element.is_displayed() == True:
                mouse.click_on_element(self,"XPATH", self.kickoff_cot)
                self.main.screen_load_time('Kicjoff COT Research')
                self.main.kick_off_render('Kickoff COT Research->Render')
                mouse.click_on_element(self,"XPATH", self.download_results)
                self.main.screen_load_time('Download results for Kickoff COT Research')
        except :
            pass
        


