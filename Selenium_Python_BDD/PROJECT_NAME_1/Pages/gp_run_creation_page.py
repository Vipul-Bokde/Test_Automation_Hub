from libraries.environment_setup import EnvironmentSetup
from selenium.webdriver.support import expected_conditions as EC
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators,mouse_rfn,forms_rfn
from GP.utilities.logs_util import logger
import allure
from allure_commons.types import AttachmentType
import time
import os
import datetime
from selenium.webdriver.common.by import By
from datetime import date
from libraries import generics


class RunCreationPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

    # locators
        # select run screen 
        self.select_run = "(//span[@id='container']/span)[2]"
        self.new_run = "//div[@id='run-new']/button[@id='run-new-btn']"
        self.delete_run_checkbox = "(//span/span[@class='ag-selection-checkbox'])[1]"
        self.delete_run_btn = "//div[@id='run-new']/button[@id='run-delete-btn']"
        self.price_type_wait = "//div[@row-index='0']/div[@col-id='status']"
        self.btn_close = "//button[@id='run-close-btn']"
        self.filtered_run_selection = "(//div[@col-id='name'])[2]"

        # new run details
        self.name = "//div[@class='form-group']/input[@id='run-name']"
        self.year = "//div[@class='col-6']/select[@id='run-year']"
        self.period = "//div[@class='col-6']/select[@id='run-period']"
        self.assessment_checkbox = "//div[@class='col-12 col-lg-6']/input[@id='assessment']"    
        self.submit_btn = "//div[@class='sparq-modal-footer']/button[@id='run-submit-btn']"
        self.btn_cancel = "//div[@class='sparq-modal-footer']/button[@id='run-cancel-btn'][contains(.,'Cancel')]"
        self.msg_name_already_in_use = "//div[contains(.,'Name is already in use.')][@class='invalid-feedback']"
        self.msg_run_already_exists = "//div[@id='alert'][contains(.,'Run already exists')]"
        self.txt_created_on_column= "(//div[@col-id='created_on'])[2]"
        self.txt_runs = "//span[text()='Runs']"

        # search filter and textbox
        self.filter_icon = "//div[@col-id='name']/div[contains(@class,'ag-cell-label-container')]/span"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"
        self.run_filter_icon = "//div[@col-id='price_type.name']/div[contains(@class,'ag-cell-label-container')]/span"
        self.result_ready = "//div[@col-id='status']/div[contains(@class,'ag-cell-label-container')]/span"
        self.runtime_error = "//modal[@id='price-type-runtime-error']/div[@class='sparq-modal']/div[@class='sparq-modal-header']"
        self.runtime_error_accept = "//div[@class='sparq-modal']/div[@class='sparq-modal-footer']/button[@class='btn btn-primary w-75']"
        self.run_click = "//div[@row-index='0']/div[@col-id='name']"
        # runs screen
        self.price_type_select = "(//div[@class='ag-pinned-left-cols-container']//div[@col-id='price_type.name'])[1]"
        self.checkbox = "//div/checkbox-renderer/input[@type='checkbox']"
        self.execute_all_btn = "//div[@class='btn-group']/button[@id='execute-price-type-btn']"
        self.execution_status_xpath = "//div/div[@class='ag-center-cols-container']/div"
        # restatement
        self.run_status = "//div[@class='ag-center-cols-container']/div[@row-index='0']/div[@col-id='status']"
        self.restatement_btn = "//div[@class='btn-group']/button[@id='restate-price-type-btn']"
        self.reexecution_status = "//div[@row-index='0']/div[@col-id='status']"

        # summary tab
        self.approve_btn = "//div[@class='btn-toolbar']/div/button[@title= 'Approve']"
        self.btn_rollback_summary_tab = "//button[@title='Rollback'][@disabled]"
        self.column_version_verify = "(//div[@col-id='version'])[1]"
        self.Filter_Icon = "//div[@col-id='price_type.name']/div/span"
        self.Search_box = "//div/input[@class= 'ag-filter-filter']"
        self.txt_price_type_first_row = "(//div[@col-id='price_type.name']/child::span)[2]"
        self.txt_version_first_row = "(//div[@col-id='version']/child::template-renderer/child::span)[1]"


        # bucket tab
        self.bucket_tab = "(//div/ul[@class='nav nav-tabs mt-1 ml-2']/li[@class='nav-item']/a)[3]"
        self.bucket_dropdown = "//div[@class='col-auto']/select"
        self.bucket_export = "//div[@id='bucket-options']/button[@class='btn btn-secondary']"
        self.t_ids = "//div[@role='row']/div[@col-id='tid']"
        self.t_id_wait = "(//div[@col-id='tid'])[1]"
        # override tab
        self.override_tab = "(//div/ul[@class='nav nav-tabs mt-1 ml-2']/li[@class='nav-item']/a)[4]"
        self.ndc_filter = "//div[@col-id='ndc11']/div[contains(@class,'ag-cell-label-container')]/span"
        self.period_filter = "//div[@col-id='period']/div[contains(@class,'ag-cell-label-container')]/span"
        self.new_override_btn = "//div[@id='override-edit']/button[@class='btn btn-outline-success']"
        self.override_name = "//div[@class='col']/select[@id='name']"
        self.ndc11 = "//div[@class='col']/select[@id='ndc11']"
        self.override_period = "//div[@class='col']/select[@id='period']"
        self.dollar = "//div[@class='col']/input[@id='dollars']"
        self.units = "//div[@class='col']/input[@id='units']"
        self.min_value = "//div[@class='col']/input[@id='min_value']"
        self.note = "//div[@class='col']/textarea[@id='note']"
        self.override_submit = "//div[@class='sparq-modal-footer']/button[@id='submit-btn']"
        self.delete_override_btn ="//div[@row-index='0']/div[@col-id='delete']/page-action/button[@class='no-style']"
        self.edit_override_btn = "//div[@id='override-edit']/button[@class='btn btn-outline-info']"
        self.component = "//div[@class='ag-cell ag-cell-not-inline-editing ag-cell-with-height ag-cell-no-focus ag-cell-value'][1]"
    
        #Confirm all popupus
        self.popup_confirmation_execute_all = "//modal[@id='confirm-execute-all']/child::div/child::div[text()='Confirmation: Execute All']"
        self.btn_execute_all = "//button[@id='execute-price-type-btn']"
        self.btn_confirmation_execute_all_yes ="//div[contains(.,'Price type calculations will be')][@class='sparq-modal-body']/following-sibling::div/child::button[text()='Yes']"
        self.popup_runtime_error_with_invalid_version = "//div[contains(.,'Runtime Error')][@class='sparq-modal-header']/parent::div/child::div/child::div[contains(.,'Current version selection is invalid')]"
        self.btn_ok = "//div[contains(.,'Runtime Error')][@class='sparq-modal-header']/parent::div/child::div/child::div[contains(.,'Current version selection is invalid')]/parent::div/following-sibling::div/child::button"
        self.msg_price_type_name_invalid = "//div[contains(.,'Runtime Error')][@class='sparq-modal-header']/parent::div/child::div/child::div"
        self.popup_select_version = "//div[contains(.,'Select amp version')][@class='sparq-modal-header']"
        self.popup_current_version_selection_is_invalid = "//div[contains(.,'Currently assigned price type version is invalid, please select eligible version to proceed')][@class='card card-body bg-light']"
        self.btn_ok_popup_assigned_version_invalid = "//div[contains(.,'Currently assigned price type version is invalid, please select eligible version to proceed')][@class='card card-body bg-light']/parent::div/following-sibling::div/child::button[contains(.,'OK')]"
        self.popup_current_version_selection_is_invalid_for_price_type = "//div[@id='runtime-error-well']"
        self.run_row = "(//div[@col-id='name'])[2]"
        self.popup_restatement_already_exists = "//div[contains(.,'Restatement already exists')]"
        self.run_name_to_get = "//div[@class='crumbs']/child::span[3]/child::span"

    # Run Creation   
    def select_run_option(self):
        element = self.driver.find_element_by_xpath(self.select_run)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Select Run Screen')
        allure.attach("User can select run screen: ",attachment_type=allure.attachment_type.TEXT)

    def select_new_run(self):
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.new_run,"New Run element not found on Webpage in given wait time.")
        self.main.screen_load_time('New Run Pop Up')
        element = self.driver.find_element_by_xpath(self.new_run)
        self.driver.execute_script("$(arguments[0]).click();", element)
        allure.attach("User can click on new run button: ",attachment_type=allure.attachment_type.TEXT)

    def new_run_details(self, run_name, run_year, run_period):
        self.run_name = run_name  
        self.run_year = run_year
        self.run_period = run_period  
        forms.enter_text_on_element(self, "XPATH", self.name,self.run_name) 
        forms.select_option_by_text(self, "XPATH", self.year,self.run_year) 
        forms.select_option_by_text(self, "XPATH", self.period,self.run_period)
        allure.attach("User can enter new run details as "+"run name ="+self.run_name+" run year = "+self.run_year+" run period = "+self.run_period,attachment_type=allure.attachment_type.TEXT)
 
    def click_on_submit(self):
        mouse.click_on_element(self, "XPATH", self.submit_btn)
        allure.attach("User can click on submit button: ",attachment_type=allure.attachment_type.TEXT)

    def select_run_name(self, run_name_select):
        self.run_name_select = run_name_select
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.filter_icon,"Filter Icon element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.filter_icon)
        allure.attach("User can click on filter icon on run screen: ",attachment_type=allure.attachment_type.TEXT)
        self.driver.execute_script("$(arguments[0]).click();", element)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.run_name_select)
        allure.attach("User can enter run name in filter container as: "+self.run_name_select,attachment_type=allure.attachment_type.TEXT)
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.run_click,"Run Click element not found on Webpage in given wait time.")
        time.sleep(5)
        element = self.driver.find_element_by_xpath(self.run_click)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Run Screen')

    def execute_all(self):
        mouse.click_on_element(self, "XPATH", self.execute_all_btn) 
        self.main.screen_load_time('Run->Execute all button')
        allure.attach("User can click on execute all button : ",attachment_type=allure.attachment_type.TEXT)

    def confirm_all_result_ready(self):
        self.execution_status = "Results Ready" 
        self.execution_status_list = []
        self.execution_status_list = self.driver.find_elements_by_xpath(self.execution_status_xpath)
        logger.info(len(self.execution_status_list))
        self.list_length =len(self.execution_status_list)
        allure.attach("List length is : "+str(self.list_length),attachment_type=allure.attachment_type.TEXT)
        # Added implicit wait because after clicking on execute all button page reloads but all data is visible in background so not found any element to wait for. 
        time.sleep(10)
        for i in range(self.list_length,0,-1):
            time.sleep(2)
            self.execution_list = "(//div[@class='ag-center-cols-container']/div/div[@col-id='status'])["+str(i)+"]"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.execution_list)
            allure.attach("Status is : "+self.column_text,attachment_type=allure.attachment_type.TEXT)
            if self.column_text == self.execution_status:
                logger.info("result ready "+str(i)+"")
            else:
                # Added implicit wait because runtime error pop up at any time which fails script.
                time.sleep(200)
                self.driver.refresh()
                time.sleep(3)
                self.column_text = forms.get_text_on_element(self, "XPATH", self.execution_list)
                if self.column_text == self.execution_status:
                    logger.info("result ready "+str(i)+"")

                # self.column_text = forms.get_text_on_element(self, "XPATH", self.runtime_error)
                # mouse.click_on_element(self, "XPATH", self.runtime_error_accept)
                
    def checking_result_ready_status(self,price_type):
        self.result_ready_status = "Results Ready"
        self.price_type = price_type
        # time.sleep(100)
        # self.driver.refresh()
        mouse.click_on_element(self, "XPATH", self.result_ready)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.result_ready_status)
        self.checkbox_exist = self.driver.find_element_by_xpath(self.checkbox)  
        assert self.checkbox_exist.is_enabled() == True
        mouse.click_on_element(self, "XPATH", self.run_filter_icon)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.price_type)
        allure.attach("User can enter text for filter as : "+self.price_type,attachment_type=allure.attachment_type.TEXT)
        self.price_type_name = forms.get_text_on_element(self, "XPATH", self.price_type_select)
        logger.info(self.price_type_name)
        logger.info(self.price_type)
        if self.price_type_name == self.price_type:
            element = self.driver.find_element_by_xpath(self.price_type_select)
            self.driver.execute_script("$(arguments[0]).click();", element)
        
    # Assessment run
    def new_run_details_with_assessment_run(self, run_name, run_year, run_period):
        self.run_name = run_name  
        self.run_year = run_year
        self.run_period = run_period  
        forms.enter_text_on_element(self, "XPATH", self.name,self.run_name) 
        forms.select_option_by_text(self, "XPATH", self.year,self.run_year) 
        forms.select_option_by_text(self, "XPATH", self.period,self.run_period) 
        forms.check_checkbox(self, "XPATH", self.assessment_checkbox)
    
    def disable_bp_BPA_price_type(self):
        mouse.click_on_element(self, "XPATH", self.run_filter_icon)
        forms.enter_text_on_element(self, "XPATH", self.search_box, "bp (BPA)")
        forms.uncheck_checkbox(self, "XPATH", self.checkbox)

    def select_assessment_run_name(self,assessment_run_name_select):
        self.main.screen_load_time('Run Screen')
        self.run_name_select = assessment_run_name_select
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.filter_icon,"Filter Icon element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.filter_icon)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.run_name_select)
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.run_click,"Run Click element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.run_click)
        self.driver.execute_script("$(arguments[0]).click();", element)

    def check_assessment_run_can_not_be_approved(self):
        self.approve = self.driver.find_element_by_xpath(self.approve_btn) 
        assert self.approve.is_displayed() == False
        logger.info("This is Assessment run, can not approve")
        
    def select_delete_run_name(self, run_name_select_delete):
        self.run_name_select_delete = run_name_select_delete
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.filter_icon,"Filter Icon element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.filter_icon)
        self.run_name_delete = self.run_name_select_delete
        self.run_name_to_delete = self.run_name_delete.replace(" (Assessment)","")
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.run_name_to_delete)
        mouse.click_on_element(self, "XPATH", self.delete_run_checkbox)
        element = self.driver.find_element_by_xpath(self.delete_run_btn)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Delete Run Button')

        
    # Restatement
    def select_run_name_with_close_status(self,close_name_select):
        self.close_name_select = close_name_select
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.filter_icon,"Filter Icon element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.filter_icon)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.close_name_select)
        self.status = forms.get_text_on_element(self,"xpath",self.run_status)
        if self.status == "CLOSED":
            element = self.driver.find_element_by_xpath(self.run_click)
        self.driver.execute_script("$(arguments[0]).click();", element)  

    def click_on_restatement(self):
        mouse.click_on_element(self,"XPATH",self.restatement_btn)
        self.main.screen_load_time('Run->Close Run->Restatement Button')
        allure.attach("User clicked on restatement button:",attachment_type=allure.attachment_type.TEXT)
        if (locators.element_is_displayed(self,"XPATH",self.popup_restatement_already_exists)) == True:
            assert False,"Restatement already exists select another client or another closed run"
        else:
            self.get_run_name = forms.get_text_on_element(self,"xpath",self.run_name_to_get)
            allure.attach("Restatement created with run name as:"+ self.get_run_name,attachment_type=allure.attachment_type.TEXT)

    
    def select_restatement_run_name(self,restatement_name):
        self.restatement_name = restatement_name
        today = datetime.datetime.now()
        self.date_time = today.strftime(f'%Y-%m-%d')
        logger.info(self.date_time)
        mouse.click_on_element(self, "XPATH", self.filter_icon)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.restatement_name)
        self.assessment_run_name_list = []
        self.assessment_run_name_list = self.driver.find_elements_by_xpath(self.execution_status_xpath)
        logger.info(len(self.assessment_run_name_list))
        self.list_length =len(self.assessment_run_name_list)
        for i in range(1,self.list_length):
            self.run_names = "(//div[@ref='eCenterContainer']/div/div[@col-id='name'])["+str(i)+"]"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.run_names)
            logger.info(self.column_text)
            if self.column_text == self.restatement_name+" ("+self.date_time+")":
                logger.info(self.restatement_name+" ("+self.date_time+")")
                self.restatement_run_name = self.restatement_name+" ("+self.date_time+")"
                allure.attach("Restatement Run name is : "+str(self.restatement_name+" ("+self.date_time+")"),attachment_type=allure.attachment_type.TEXT)
                break
        return self.restatement_run_name

    #Delete Existing Run
    def name_already_in_use_msg_popup_is_displayed(self):
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.msg_name_already_in_use)
        logger.info("Name already in use message popup is displayed")
        logger.info(self.bln_flag)
        return self.bln_flag
    
    def click_on_cancel_button_from_new_run_popup(self):
        mouse.click_on_element(self, "XPATH", self.btn_cancel)
        logger.info("User is able to click on cancel button")
    
    def generate_random_run_name(self,run_name,length):
        self.run_name = run_name 
        self.length = length 
        self.random_str = self.run_name+"_"+MainPage.get_random_string(self,self.length)
        logger.info(self.random_str)
        return self.random_str
    
    def run_already_exists_msg_popup_is_displayed(self):
        self.list_of_element =[]
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.msg_run_already_exists)
        logger.info("Run already exists popup is displayed")
        logger.info(self.bln_flag)
        if self.bln_flag ==True:
            self.get_popup_msg = forms.get_text_on_element(self,"XPATH",self.msg_run_already_exists)
            logger.info(self.get_popup_msg)
            self.msg_splitted = self.get_popup_msg.split(':')
            logger.info("Splitted String is :")
            self.run_name = self.msg_splitted[1].strip()
            logger.info(self.run_name)
            self.list_of_element.append(self.bln_flag)
            self.list_of_element.append(self.run_name)
            return self.list_of_element
        else:
            logger.info("In else block")
            self.list_of_element.append(self.bln_flag)
            self.list_of_element.append("Null")
            return self.list_of_element
        
    def verify_new_run_is_displayed(self,run_name):
        self.run_name = run_name
        self.verify_run_name = "//div[@col-id='name'][text()='"+self.run_name+"']"
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.verify_run_name.format(self.run_name))
        logger.info("User can see new run")
        logger.info(self.bln_flag)
        logger.info(self.run_name)
        return self.bln_flag


    def get_text_of_created_on_Column(self):
        self.get_application_date = forms.get_text_on_element(self,"XPATH",self.txt_created_on_column)
        logger.info("Application date is: ")
        logger.info(self.get_application_date)
        return self.get_application_date

    def click_on_runs_page(self):
        mouse.click_on_element(self, "XPATH", self.txt_runs)
        logger.info("User can click on runs page")

    def filter_run_name(self, run_name):
        self.run_name = run_name
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.filter_icon,"Filter Icon element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.filter_icon)
        self.run_name_new = self.run_name
        self.run_name_to_filter = self.run_name_new.replace(" (Assessment)","")
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.run_name_to_filter)
        
    def verify_run_is_deleted(self,run_name):
        self.run_name = run_name
        self.verify_run_name = "//div[@col-id='name'][text()='"+self.run_name+"']"
        self.element= locators.check_element_not_displayed(self, self.verify_run_name)
        logger.info("User cannot see the run name")
        logger.info(self.element)
    
    def get_current_system_date(self,date_format):
        self.date_format = date_format
        self.system_current_date = MainPage.get_system_current_date(self,self.date_format)
        logger.info("User can see current system date as")
        logger.info(self.system_current_date )
        return self.system_current_date
    
    def verify_name_already_in_use_or_run_already_exists(self,run_name,run_length,run_year,run_period,run_name_to_delete,new_run_name):
        self.run_year = run_year
        self.run_period = run_period
        self.bln_flag_and_run_already_exists =self.run_already_exists_msg_popup_is_displayed()
        logger.info(self.bln_flag_and_run_already_exists)
        self.bln_flag_run_already_exists = self.bln_flag_and_run_already_exists[0]
        logger.info(self.bln_flag_run_already_exists)
        self.get_run_name = self.bln_flag_and_run_already_exists[1]
        self.bln_flag_for_name_already_in_use=self.name_already_in_use_msg_popup_is_displayed()
        logger.info(self.bln_flag_run_already_exists)
        if self.bln_flag_run_already_exists==True:
            self.run_name = run_name
            self.run_length = run_length
            logger.info("In run already exists ")
            self.click_on_cancel_button_from_new_run_popup()
            self.select_delete_run_name(self.get_run_name)
            self.select_new_run()
            self.random_run_name = self.generate_random_run_name(self.run_name,self.run_length)
            self.new_run_details(self.random_run_name, self.run_year, self.run_period)
            self.click_on_submit() 
            self.filter_run_name(self.random_run_name)
            self.click_on_runs_page()
            self.verify_new_run_is_displayed(self.random_run_name)
            self.system_date = self.get_current_system_date("%Y-%m-%d")
            self.application_date = self.get_text_of_created_on_Column()
            if self.system_date==self.application_date:
                logger.info("System date is equal to application date for unique run")
                self.select_delete_run_name(self.random_run_name)
                self.click_on_runs_page()
                self.filter_run_name(self.random_run_name)
                self.verify_run_is_deleted(self.random_run_name)
        elif self.bln_flag_for_name_already_in_use==True:
            logger.info("In name already in use ")
            self.run_name_to_delete = run_name_to_delete
            self.new_run_name = new_run_name
            self.click_on_cancel_button_from_new_run_popup()
            self.select_delete_run_name(self.run_name_to_delete)
            self.select_new_run()
            self.new_run_details(self.new_run_name, self.run_year, self.run_period)
            self.click_on_submit() 
            self.filter_run_name(self.new_run_name)
            self.click_on_runs_page()
            self.verify_new_run_is_displayed(self.new_run_name)
            self.system_date = self.get_current_system_date("%Y-%m-%d")
            self.application_date = self.get_text_of_created_on_Column()
            if self.system_date==self.application_date:
                logger.info("System date is equal to application date")
                self.select_delete_run_name(self.new_run_name)
                self.click_on_runs_page()
                self.filter_run_name(self.new_run_name)
                self.verify_run_is_deleted(self.new_run_name)
        else:
            logger.info("No Popup")

    def confirm_result_ready_and_handle_all_popup(self,price_type_list):
        self.execution_status = "Results Ready" 
        self.price_type_list = []
        self.standard_price_type_list = price_type_list
        allure.attach("Standard list is : "+str(self.standard_price_type_list),attachment_type=allure.attachment_type.TEXT)
        self.all_price_type_list = "(//div[@class='ag-pinned-left-cols-container']//child::div[@col-id='price_type.name'])/span"
        self.price_type_list = self.driver.find_elements_by_xpath(self.all_price_type_list)
        self.list_length =len(self.price_type_list)+1
        allure.attach("Length of price type list is : "+str(self.list_length),attachment_type=allure.attachment_type.TEXT)
        time.sleep(10)
        for i in range(1,self.list_length):
            time.sleep(2)
            logger.info("In For Loop")
            self.specific_price_type = "(//div[@class='ag-pinned-left-cols-container']//child::div[@col-id='price_type.name'])["+str(i)+"]/span"
            self.txt_get_price_type_name = forms.get_text_on_element(self, "XPATH",  self.specific_price_type)
            allure.attach("Price Type Is: "+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)
            self.specific_price_type_status = "(//span[text()='"+self.txt_get_price_type_name+"']/ancestor::div[@class='ag-pinned-left-cols-container']/following-sibling::div[@class='ag-center-cols-clipper']/descendant::div[@col-id='status'])["+str(i)+"]"
            self.txt_get_price_type_status = forms.get_text_on_element(self, "XPATH",  self.specific_price_type_status)
            if self.txt_get_price_type_name in self.standard_price_type_list:
                if self.txt_get_price_type_status == self.execution_status:
                    allure.attach("Result ready status is shown for price type "+self.txt_get_price_type_name+"  and index as: "+str(i),attachment_type=allure.attachment_type.TEXT)
                elif self.txt_get_price_type_status == "Running":
                    allure.attach("Price type is already in running state :",attachment_type=allure.attachment_type.TEXT)
                else:
                    self.btn_execute = "(//span[text()='"+self.txt_get_price_type_name+"']/ancestor::div[@class='ag-pinned-left-cols-container']/following-sibling::div[@class='ag-center-cols-clipper']/descendant::div[@col-id='execute'])["+str(i)+"]/descendant::button/i"
                    mouse.click_on_element(self, "XPATH", self.btn_execute)
                    allure.attach("User can click on execute button :",attachment_type=allure.attachment_type.TEXT)
                    if self.verify_confirmation_popup_is_displayed(self.txt_get_price_type_name) == True:
                        self.click_on_yes_button_from_confirmation_execution_popup(self.price_type)
                        if self.verify_runtime_error_with_current_version_selection_as_invalid() == True:
                            mouse.click_on_element(self, "XPATH", self.btn_ok_popup_assigned_version_invalid)
                            allure.attach("User can click on ok button from invalid popup :",attachment_type=allure.attachment_type.TEXT)
                            self.icon_pencil = "(//span[text()='"+self.txt_get_price_type_name+"']/ancestor::div[@class='ag-pinned-left-cols-container']/following-sibling::div[@class='ag-center-cols-clipper']/descendant::div[@col-id='version'])["+str(i)+"]/child::template-renderer/descendant::i"
                            mouse.click_on_element(self, "XPATH", self.icon_pencil)
                            allure.attach("User can click on pencil icon for price type :"+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)
                            self.popup_invalid_effective_version = "//div[@id='alert'][contains(.,'No effective version found for "+self.txt_get_price_type_name+" price type!')]"
                            self.popup_current_price_type_invalid = "//div[contains(.,' Current "+self.txt_get_price_type_name+" price type version selection is invalid!')]"
                            if self.verify_select_version_popup_is_displayed(self.txt_get_price_type_name) == True or (locators.element_is_displayed(self,"XPATH",self.popup_current_price_type_invalid)):
                                self.select_latest_version(self.txt_get_price_type_name)
                                self.btn_ok = "//div[contains(.,'Select "+self.txt_get_price_type_name+" version')]/child::div[3]/child::button[1][contains(.,'OK')]"
                                mouse.click_on_element(self, "XPATH", self.btn_ok)
                                allure.attach("User can click on ok button from select version popup  for price type:"+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)
                                mouse.click_on_element(self, "XPATH", self.btn_execute)
                                allure.attach("User can click on execute button:"+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)
                                if self.verify_confirmation_popup_is_displayed(self.txt_get_price_type_name) == True:
                                    self.click_on_yes_button_from_confirmation_execution_popup(self.price_type)
                                    self.blnFlag_status = False
                                    while self.blnFlag_status == False:
                                        self.count =0
                                        self.txt_get_price_type_status = forms.get_text_on_element(self, "XPATH",  self.specific_price_type_status)
                                        if self.txt_get_price_type_status == "Running":
                                            self.driver.refresh()
                                            self.main.screen_load_time('Run Screen')
                                            self.blnFlag_status = False
                                        elif self.txt_get_price_type_status == self.execution_status:
                                            self.blnFlag_status =True
                                            allure.attach("Status column is updated to results ready for price type : "+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)
                                            break
                                        if self.count >= 30:
                                            break
                            elif (locators.element_is_displayed(self,"XPATH",self.popup_invalid_effective_version)) == True:
                                assert False,"No effective version found for "+self.txt_get_price_type_name+" price type!"
                    self.blnFlag_status = False
                    while self.blnFlag_status == False:
                        self.count =0
                        self.txt_get_price_type_status = forms.get_text_on_element(self, "XPATH",  self.specific_price_type_status)
                        if self.txt_get_price_type_status == "Running":
                            self.driver.refresh()
                            self.main.screen_load_time('Run Screen')
                            self.blnFlag_status = False
                        elif self.txt_get_price_type_status == self.execution_status:
                            self.blnFlag_status =True
                            allure.attach("Status column is updated to results ready : "+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)
                            break
                        elif self.txt_get_price_type_status == "Awaiting Execution":
                            self.blnFlag_status =True
                            break
                        if self.count >= 30:
                            break
            elif self.txt_get_price_type_name not in self.standard_price_type_list:
                allure.attach("Price type is not a standard price type : "+self.txt_get_price_type_name,attachment_type=allure.attachment_type.TEXT)


    def verify_confirmation_popup_is_displayed(self,price_type):
        self.price_type = price_type
        self.blnFlag = False
        self.popup_confirmation = "//div[text()='Confirmation: "+self.price_type+" execution']"
        self.bln_flag_popup_confirmation_execution = locators.element_is_displayed(self,"XPATH",self.popup_confirmation)
        if self.bln_flag_popup_confirmation_execution == True:
            allure.attach("Execution confirmation popup is displayed: ",attachment_type=allure.attachment_type.TEXT)
            self.blnFlag = True
            return self.blnFlag
        else:
            assert self.bln_flag_popup_confirmation_execution , "Execution confirmation popup does not appear"
            return self.blnFlag
        
    def click_on_yes_button_from_confirmation_execution_popup(self,price_type):
        self.price_type= price_type
        self.btn_yes = "//div[text()='Confirmation: "+self.price_type+" execution']//parent::div/child::div/button[text()='Yes']"
        mouse.click_on_element(self, "XPATH", self.btn_yes)
        allure.attach("User can click on yes button from confirmation execution popup :",attachment_type=allure.attachment_type.TEXT)

    def verify_runtime_error_with_current_version_selection_as_invalid(self):
        self.blnFlag = False
        if (locators.element_is_displayed(self,"XPATH",self.popup_current_version_selection_is_invalid)) == True:
            self.blnFlag = True
            allure.attach("User can see run time error popup with current version invalid :",attachment_type=allure.attachment_type.TEXT)
            return self.blnFlag
        else:
            self.blnFlag = False
            return self.blnFlag
    
    def verify_select_version_popup_is_displayed(self,price_type):
        self.price_type = price_type
        self.popup_version = "//div[contains(.,'Select "+self.price_type+" version')][@class='sparq-modal-header']"
        if (locators.element_is_displayed(self,"XPATH",self.popup_version)) == True:
            allure.attach("Version Selection popup is displayed: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Version Selection popup is not displayed"

    def click_on_execute_all(self):
        mouse.click_on_element(self, "XPATH", self.btn_execute_all)
        allure.attach("User can click on execute button: ",attachment_type=allure.attachment_type.TEXT)

    def verify_confirmation_execute_all_popup_is_displayed(self):
        self.blnFlag = False
        self.bln_flag_popup_confirmation_execution_all = locators.element_is_displayed(self,"XPATH",self.popup_confirmation_execute_all)
        if self.bln_flag_popup_confirmation_execution_all == True:
            allure.attach("Execution confirmation all popup is displayed: ",attachment_type=allure.attachment_type.TEXT)
            self.blnFlag = True
            return self.blnFlag
        else:
            assert self.bln_flag_popup_confirmation_execution_all , "Execution confirmation  all popup does not appear"
            return self.blnFlag
        
    def verify_execute_all_popups(self,price_type_list):
        self.standard_PT_list = price_type_list
        if self.verify_confirmation_execute_all_popup_is_displayed() == True:
            mouse.click_on_element(self, "XPATH", self.btn_confirmation_execute_all_yes)
            allure.attach("User can click on yes button from confirmation all execution popup: ",attachment_type=allure.attachment_type.TEXT)
            if (locators.element_is_displayed(self,"XPATH",self.popup_current_version_selection_is_invalid_for_price_type)) == True:
                allure.attach("User can see current version  selection invalid popup for price types for execution all button: ",attachment_type=allure.attachment_type.TEXT)
                self.get_msg = forms.get_text_on_element(self,"XPATH",self.popup_current_version_selection_is_invalid_for_price_type)
                self.remove_leading_and_trailing_spaces = self.get_msg.strip()
                self.split_and_get_price_type = self.remove_leading_and_trailing_spaces.split(" ")
                self.standard_PT = self.split_and_get_price_type[6]
                self.non_standard_PT = self.split_and_get_price_type[8]
                self.btn_ok_current_invalid_version = "//div[@id='runtime-error-well']/parent::div/following-sibling::div/child::button"
                mouse.click_on_element(self, "XPATH", self.btn_ok_current_invalid_version)
                allure.attach("User can click on ok button from confirmation all execution popup: ",attachment_type=allure.attachment_type.TEXT)


    def select_latest_version(self,price_type_name):
        self.price_type_name = price_type_name
        self.drp_select_version = "//div[contains(.,'Select "+self.price_type_name+" version')][@class='sparq-modal-header']/parent::div/child::div[2]/descendant::select"
        self.version_list = self.driver.find_elements_by_xpath(self.drp_select_version)
        self.version_size_list = len(self.version_list)
        self.version_option_number = self.version_size_list-1
        self.drp_select_version_option = "//div[contains(.,'Select "+self.price_type_name+" version')][@class='sparq-modal-header']/parent::div/child::div[2]/descendant::select/child::option["+str(self.version_size_list)+"]"
        self.version_number = forms.get_text_on_element(self,"XPATH",self.drp_select_version_option)
        allure.attach("Version has a list of  "+str(self.version_size_list),attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_index(self, "XPATH", self.drp_select_version,self.version_size_list) 
        allure.attach("Version selected is  "+self.version_number,attachment_type=allure.attachment_type.TEXT)

    def get_closed_status_run(self,closed_status,column_name):
        self.column_name = column_name
        self.closed_status = closed_status
        MainPage.click_on_any_filter_icon(self,self.column_name)
        MainPage.enter_text_on_any_filter_icon_search_box(self,self.closed_status)
        if (locators.element_is_displayed(self,"XPATH",self.run_row)) == True:
            self.run_name = forms.get_text_on_element(self,"XPATH",self.run_row)
            allure.attach("Run Name With Closed status is:"+self.run_name,attachment_type=allure.attachment_type.TEXT)
            return self.run_name
        else:
            assert False,"Select another client no run with closed status present"

    def confirm_result_ready_and_handle_all_popup_for_price_type(self,column_name,price_type_name):
        self.column_name = column_name
        self.price_type_name = price_type_name
        MainPage.click_on_any_filter_icon(self,self.column_name)
        self.status = "(//div[@col-id='status'])[2]"
        MainPage.enter_text_on_any_filter_icon_search_box(self,self.price_type_name)
        self.btn_execute = "(//span[text()='"+self.price_type_name+"']/ancestor::div[@class='ag-pinned-left-cols-container']/following-sibling::div[@class='ag-center-cols-clipper']/descendant::div[@col-id='execute'])[1]/descendant::button/i"
        mouse.click_on_element(self, "XPATH", self.btn_execute)
        allure.attach("User can click on execute button :",attachment_type=allure.attachment_type.TEXT)
        if self.verify_confirmation_popup_is_displayed(self.price_type_name) == True:
            self.click_on_yes_button_from_confirmation_execution_popup(self.price_type_name)
            time.sleep(200)
            self.driver.refresh()
            time.sleep(3)

    """Author : Sadiya Kotwal
       Description : This method verify the rollback button is disabled
       Arguments : 
       Returns : NA""" 
    def verify_rollback_button_is_disabled_in_summary_tab(self):
        locators.element_is_displayed(self,"XPATH",self.btn_rollback_summary_tab)
        allure.attach("Rollback button is disabled in summary tab :",attachment_type=allure.attachment_type.TEXT)

    def filter_run_name_on_run_screen(self, run_name_select):
        self.run_name_select = run_name_select
        element = self.driver.find_element_by_xpath(self.filter_icon)
        allure.attach("User can click on filter icon on run screen: ",attachment_type=allure.attachment_type.TEXT)
        self.driver.execute_script("$(arguments[0]).click();", element)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.run_name_select)
        allure.attach("User can enter run name in filter container as: "+self.run_name_select,attachment_type=allure.attachment_type.TEXT)

    def click_on_run_name_checkbox_and_click_on_close_button(self,run_name_select):
        self.run_name_select = run_name_select
        self.run_name_checkbox = "(//div[text()='"+self.run_name_select+"']/preceding-sibling::div/child::span/child::span/child::span[2])[1]"
        mouse.click_on_element(self, "XPATH", self.run_name_checkbox)
        allure.attach("User can click on checkbox to close run :",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Run Screen')
        mouse.click_on_element(self, "XPATH", self.btn_close)
        self.main.screen_load_time('Run Screen')
        allure.attach("User can click on close button :",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Run Screen Close')

    def verify_run_name_with_closed_status(self,run_name_select):
        self.run_name_select = run_name_select
        self.txt_verify_status = "(//div[text()='"+self.run_name_select+"']/following::div[text()='CLOSED'])[1]"
        locators.element_is_displayed(self,"XPATH",self.txt_verify_status)
        allure.attach("Run is having closed status :",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Run Screen Closed Status')

    def filter_assessment_run(self,assessment_run_name):
        self.assessment_run_name = assessment_run_name
        mouse.click_on_element(self,"XPATH", self.filter_icon)
        allure.attach("User can click on filter icon : ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.assessment_run_name)
        allure.attach("User can filter the assessment run as : "+self.assessment_run_name,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH",self.filtered_run_selection)
        self.main.screen_load_time('Select Run Screen')
        allure.attach("User clicked on the Run Name : "+self.assessment_run_name,attachment_type=allure.attachment_type.TEXT)

    def get_price_type_and_version_from_closed_run(self):
        self.list_of_closed_run = []
        self.get_txt_of_price_type = forms.get_text_on_element(self,"XPATH",self.txt_price_type_first_row)
        self.list_of_closed_run.append(self.get_txt_of_price_type)
        self.get_txt_of_version = forms.get_text_on_element(self,"XPATH",self.txt_version_first_row)
        self.list_of_closed_run.append(self.get_txt_of_version)
        allure.attach("List of price type for closed run : "+str(self.list_of_closed_run),attachment_type=allure.attachment_type.TEXT)
        return self.list_of_closed_run
    
    def filter_price_type_name(self,Price_Type_Name):
        self.Price_Type_Name = Price_Type_Name
        mouse.click_on_element(self,"XPATH", self.Filter_Icon)
        allure.attach("User can click on filter icon : ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.Search_box,self.Price_Type_Name)
        allure.attach("User can filter the price type as : "+self.Price_Type_Name,attachment_type=allure.attachment_type.TEXT)

    def select_run_name_with_exact_one_match(self, run_name_select):
        self.run_name_select = run_name_select
        element = self.driver.find_element_by_xpath(self.filter_icon)
        allure.attach("User can click on filter icon on run screen: ",attachment_type=allure.attachment_type.TEXT)
        self.driver.execute_script("$(arguments[0]).click();", element)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.run_name_select)
        allure.attach("User can enter run name in filter container as: "+self.run_name_select,attachment_type=allure.attachment_type.TEXT)
        time.sleep(3)
        self.txt_run_name = "//div[@col-id='name'][text()='"+self.run_name_select+"']"
        mouse.click_on_element(self,"XPATH",self.txt_run_name)
        self.main.screen_load_time('Run Screen')

    def verify_version_column_inside_run(self):
        locators.element_is_displayed(self,"XPATH",self.column_version_verify)
        allure.attach("Run is having version column :",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Run With Version Column')
