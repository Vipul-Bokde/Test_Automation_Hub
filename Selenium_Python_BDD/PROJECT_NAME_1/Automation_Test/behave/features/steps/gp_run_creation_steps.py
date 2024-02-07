from behave import *
from GP.pages.gp_run_creation_page import RunCreationPage
from GP.pages.analysis_page import AnalysisPage
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.tests.test_login import TestLogin
from GP.pages.main_page import MainPage
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from libraries import generics
from libraries import files
import allure

class RunCreation(EnvironmentSetup):

    @when(u'I click on Select Run')
    def step_impl(self):
        self.run_creation = RunCreationPage(self.driver)
        self.login = Login(self.driver)
        self.run_creation.select_run_option()

    @when(u'I click on new Run')
    def step_impl(self):  
        self.run_creation = RunCreationPage(self.driver)
        self.run_creation.select_new_run()

    @when(u'I enter new run Details')
    def step_impl(self):
        self.run_name = self.td_set['Run Name']
        self.run_year = self.td_set['Run Year']
        self.run_period = self.td_set['Run Period']
        self.run_creation.new_run_details(self.run_name, self.run_year, self.run_period) 
    
    @then(u'I submit new run')
    def step_impl(self):
        generics.capture_screenshot_allure(self.run_creation, 'New Run Details')
        self.run_creation.click_on_submit()
        generics.capture_screenshot_allure(self.run_creation, 'New Run Created')
        
    @when(u'I select run name')
    def step_impl(self):
        self.run_name_select = self.td_set['Select_Run_Name']
        self.run_creation.select_run_name(self.run_name_select)
        
    @when(u'I enter new run Details with Assessment Run')
    def step_impl(self):
        self.run_name = self.td_set['Run Name']
        self.run_year = self.td_set['Run Year']
        self.run_period = self.td_set['Run Period']
        self.run_creation.new_run_details_with_assessment_run(self.run_name, self.run_year, self.run_period) 
   
    @when(u'I select assessment only run name')
    def step_impl(self):
        self.assessment_run_name_select = self.td_set['Select_Run_Name']
        self.run_creation.select_assessment_run_name(self.assessment_run_name_select)
    
    @then(u'I disable bp (BPA) price type')
    def step_impl(self):
        self.run_creation.disable_bp_BPA_price_type()
      
    @then(u'I check Assessment run can not be approved')
    def step_impl(self):
        self.run_creation.check_assessment_run_can_not_be_approved()
        self.login.close_browser()
        
    @then(u'I select delete run name and delete')
    def step_impl(self):
        self.run_name_select_delete = self.td_set['Run Name']
        self.run_creation.select_delete_run_name(self.run_name_select_delete)
        self.login.close_browser()
        
    @then(u'I click on execute all')
    def step_impl(self):
        self.run_creation.execute_all()
    
    @then(u'I confirm all result ready')
    def step_impl(self):
        self.standard_price_type_list = ['data_summary','amp','bp (BPI)','bp (BPA)','ura','phs','cppd','asp','iff','nfamp','anfamp','fcp','tempnfamp','permnfamp']
        self.run_creation.confirm_result_ready_and_handle_all_popup(self.standard_price_type_list)
        # self.run_creation.confirm_all_result_ready()
        # self.login.close_browser()
        
    @when(u'I select result ready price type and click on it')
    def step_impl(self):
        self.price_type = self.td_set['Price Type']
        self.run_creation.checking_result_ready_status(self.price_type)     
    
    # restatement
    @when(u'I select run name with closed status')
    def step_impl(self):
        # self.close_status = self.td_set['Status Closed']
        # self.column_name_status = self.td_set['Column Name Status']
        # self.run_name = self.run_creation.get_closed_status_run(self.close_status,self.column_name_status)
        self.run_name = self.td_set['Select_Run_Name']
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_run_name_closed_status = self.td_set['Key As Run Name With Closed Status']
        files.write_into_json_file(self.service_name,self.json_file_name,self.key_as_run_name_closed_status,self.run_name)
        self.get_json_run_name_with_closed_status = files.read_from_json_file(self.service_name,self.json_file_name,self.key_as_run_name_closed_status)
        allure.attach("User can get closed run name as: "+str(self.get_json_run_name_with_closed_status),attachment_type=allure.attachment_type.TEXT)
        self.run_creation.select_run_name_with_close_status(self.run_name)

    @then(u'I click on create restatement')
    def step_impl(self):
        self.run_creation.click_on_restatement()
        self.login.close_browser()
    
    @then(u'I ensure restatement execution')
    def step_impl(self):
        self.restatement_name = self.td_set['Select_Run_Name']
        self.restatement_run_name = self.run_creation.select_restatement_run_name(self.restatement_name)
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_restatement_run_name = self.td_set['Key As Restatement Run Name']
        files.write_into_json_file(self.service_name,self.json_file_name,self.key_as_restatement_run_name,self.restatement_run_name)
        self.get_json_run_name_with_restatement = files.read_from_json_file(self.service_name,self.json_file_name,self.key_as_restatement_run_name)
        allure.attach("User can get re-statement run name as:  "+str(self.get_json_run_name_with_restatement),attachment_type=allure.attachment_type.TEXT)

    @Then(u'if I see name already exists or run already exists in new run popup page I delete the existing run and create new run')
    def step_impl(self):
        self.run_name_unique = self.td_set['Unique_Run_Name']
        self.length = self.td_set['Random_Length']
        self.run_name = self.td_set['Run Name']
        self.run_year = self.td_set['Run Year']
        self.run_period = self.td_set['Run Period']
        self.run_name_select_delete = self.td_set['Select_Run_Name']
        self.run_creation.verify_name_already_in_use_or_run_already_exists(self.run_name_unique,self.length,self.run_year,self.run_period,self.run_name_select_delete,self.run_name)
        
    @Then(u'I verify new run and created on date')
    def step_impl(self):
        self.run_name = self.td_set['Run Name']
        self.run_creation.filter_run_name(self.run_name)
        self.run_creation.click_on_runs_page()
        if self.run_creation.verify_new_run_is_displayed(self.run_name)==True:
            self.system_date = self.run_creation.get_current_system_date("%Y-%m-%d")
            self.application_date = self.run_creation.get_text_of_created_on_Column()
            if self.system_date==self.application_date:
                logger.info("System date is equal to application date")   

    @Then(u'I delete run')
    def step_impl(self):
        self.run_name = self.td_set['Run Name']
        if self.run_creation.verify_new_run_is_displayed(self.run_name)==True:
            self.run_creation.select_delete_run_name(self.run_name)
            self.run_creation.click_on_runs_page()
            self.run_creation.filter_run_name(self.run_name)
            self.run_creation.verify_run_is_deleted(self.run_name)

    @Then(u'I verify result ready for price type and all popups')
    def step_impl(self):
        self.standard_price_type_list = ['data_summary','amp','bp (BPI)','bp (BPA)','ura','phs','cppd','asp','iff','nfamp','anfamp','fcp','tempnfamp','permnfamp']
        self.run_creation.confirm_result_ready_and_handle_all_popup(self.standard_price_type_list)

    @Then(u'I verify execute all confirmation popups')
    def step_impl(self):
        self.standard_price_type_list = ['data_summary','amp','bp (BPI)','bp (BPA)','ura','phs','cppd','asp','iff','nfamp','anfamp','fcp','tempnfamp','permnfamp']
        self.run_creation.verify_execute_all_popups(self.standard_price_type_list)
        
    @Then(u'I verify result ready for selected price type and all popups')
    def step_impl(self):
        self.price_type = self.td_set['Price Type']
        self.column_name = self.td_set['Column Name Name']
        self.run_creation.confirm_result_ready_and_handle_all_popup_for_price_type(self.column_name,self.price_type)

    @Then(u'I verify rollback button is disabled in summary tab')
    def step_impl(self):
        self.run_creation.verify_rollback_button_is_disabled_in_summary_tab()
        generics.capture_screenshot_allure(self.run_creation, 'Summary Tab')

    @when(u'I filter run name')
    def step_impl(self):
        self.run_creation = RunCreationPage(self.driver)
        self.login = Login(self.driver)
        self.run_name_select = self.td_set['Select_Run_Name']
        self.run_creation.filter_run_name_on_run_screen(self.run_name_select)

    @when(u'I click on checkbox and close run')
    def step_impl(self):
        self.run_name_select = self.td_set['Select_Run_Name']
        self.run_creation.click_on_run_name_checkbox_and_click_on_close_button(self.run_name_select)
       
    @Then(u'I verify run name is having closed status')
    def step_impl(self):
        self.run_name_select = self.td_set['Select_Run_Name']
        self.run_creation.verify_run_name_with_closed_status(self.run_name_select)

    @when(u'I filter assessment run name')           
    def step_impl(self):
        self.filter_assessment_run_name = self.td_set['Run Name']
        self.run_creation.filter_assessment_run(self.filter_assessment_run_name)

    @when(u'I get price type and version from closed run')           
    def step_impl(self):
        self.list_of_closed_run_price_type_and_version = self.run_creation.get_price_type_and_version_from_closed_run()

    @when(u'I select re-statement run name')
    def step_impl(self):
        self.run_creation.select_run_name(self.get_json_run_name_with_restatement)
    
    @when(u'I filter price type for restatement')
    def step_impl(self):
        self.run_creation.filter_price_type_name(self.list_of_closed_run_price_type_and_version[0])

    @Then(u'I verify re-statement newly created run should show same tagged version as original one')
    def step_impl(self):
        self.list_of_restatement_run_price_type_and_version = self.run_creation.get_price_type_and_version_from_closed_run()
        if self.list_of_closed_run_price_type_and_version == self.list_of_restatement_run_price_type_and_version:
            allure.attach("Restatement run shows same tagged version as original run and price type: "+str(self.list_of_closed_run_price_type_and_version) +" "+str(self.list_of_restatement_run_price_type_and_version),attachment_type=allure.attachment_type.TEXT)

    @When(u'I select run name with closed status filter')
    def step_impl(self):
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_run_name_closed_status = self.td_set['Key As Run Name With Closed Status']
        self.get_json_run_name_with_closed_status = files.read_from_json_file(self.service_name,self.json_file_name,self.key_as_run_name_closed_status)
        self.run_creation.select_run_name_with_exact_one_match(self.get_json_run_name_with_closed_status)

    @Then(u'I see version column is displayed')
    def step_impl(self):
        self.run_creation.verify_version_column_inside_run()