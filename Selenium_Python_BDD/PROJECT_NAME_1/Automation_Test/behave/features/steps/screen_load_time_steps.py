from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
import allure
from allure_commons.types import AttachmentType
from GP.utilities.logs_util import logger
from GP.pages.view_data_page import ViewDataPage
from GP.pages.Smoke_Test_page import Smoke_Test_page
from GP.pages.gp_run_creation_page import RunCreationPage
from GP.pages.analysis_page import AnalysisPage
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from GP.tests.test_login import TestLogin
from GP.pages.screen_load_time_page import Load_Time_Page
from GP.pages.global_new_mapping_page import NewMappingPage
 
class PageLoad(EnvironmentSetup):


    @when(u'I navigate to run screen')
    def step_impl(self):
        self.run_creation = RunCreationPage(self.driver)
        self.run_name_select = self.td_set['Select_Run_Name']
        self.run_creation.select_run_name(self.run_name_select)
        logger.info("selected the given run name")
        logger.info(self.run_name_select)
    
    @when(u'I select to price type and go to summary tab')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for analysis class in analysis steps")
        self.price_type_name = self.td_set['Price Type']
        self.analysis.Select_price_type_name(self.price_type_name)
        logger.info(self.price_type_name)
        logger.info("Price Type Selected under the Run page")
    
    @then(u'I click on file templates')
    def step_impl(self):
        self.load_time = Load_Time_Page(self.driver)
        self.load_time.select_template_name()

    @then(u'I click on GP mappings')
    def step_impl(self):
        self.New_Mapping = NewMappingPage(self.driver)
        self.New_Mapping.click_on_gp_mappings()
        logger.info("Click on GP Mappings option")

    @then(u'I navigate to global price type')  
    def step_impl(self):  
        self.load_time = Load_Time_Page(self.driver)
        self.load_time.select_global_price_type()
        
    @then(u'I navigate to all screens under client')
    def step_impl(self): 
        self.load_time.select_screens_under_client()

    @then(u'I navigate to all screens under users')
    def step_impl(self): 
        self.load_time.select_screens_under_users()

    @then(u'I navigate to clients')
    def step_impl(self): 
        self.load_time.select_clients_screen()
    
    @then(u'I click on data dictionary table')
    def step_impl(self): 
        self.load_time.select_data_dictionary_table_screen()
    
    @Then(u'I navigate to all tabs under price type editor')
    def step_impl(self):
        self.load_time.select_price_type()
   
    @when(u'I navigate through all resources of view data screen')
    def step_impl(self):
        self.load_time = Load_Time_Page(self.driver)
        self.load_time.click_on_view_data_sources()

    @Then(u'I navigate to Uploads Screen')
    def step_impl(self):
        self.load_time.uploads_screen()

    @Then(u'I navigate to run tracker')
    def step_impl(self):
        self.load_time.run_tracker()
    