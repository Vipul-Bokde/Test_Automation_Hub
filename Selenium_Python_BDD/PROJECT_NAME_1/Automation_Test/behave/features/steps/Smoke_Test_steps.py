from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
import allure
from allure_commons.types import AttachmentType
from GP.utilities.logs_util import logger
from GP.pages.data_overview_page import DataOverviewPage
from GP.pages.Smoke_Test_page import Smoke_Test_page
from GP.pages.gp_run_creation_page import RunCreationPage
from GP.pages.analysis_page import AnalysisPage
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from GP.tests.test_login import TestLogin


class Smoke_Test(EnvironmentSetup):
    @when(u'select FileType from dropdown and click on Submit for the given "{TC_ID}"')
    def step_impl(self,TC_ID):
        self.TC_ID = TC_ID 
        self.overview = DataOverviewPage(self.driver)
        self.FileType = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data',self.TC_ID,'FileType')
        self.overview.select_file_type(self.FileType)
        self.source_value = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data',self.TC_ID,'Source_Value')
        self.file_template = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data',self.TC_ID,'File_Template')
        self.overview.click_on_checkbox(self.source_value, self.file_template)
        self.file_name = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data',self.TC_ID,'File_to_Upload')
        self.file_to_upload = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_name))
        logger.info(self.file_to_upload)
        self.overview.upload_file(self.file_to_upload)
        self.overview.click_on_submit_button()
        logger.info("Uploed file and clicked on submit")

    @when(u'user should be navigate to upload screen then I see the product file that was uploaded')
    def step_impl(self):
        logger.info("user should redirect to upload screen")   
        self.file_name = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data',self.TC_ID,'File_to_Upload')
        self.overview.check_uploaded_file(self.file_name)

    @when(u'I navigate back to view data screen')
    def step_impl(self):
        self.View_data_dropdown_value = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data',self.TC_ID,'View_data_dropdown_value')
        self.overview.select_viewdata_from_burger_menu(self.View_data_dropdown_value)
        logger.info('navigated to view data screen')

    @then(u'I crosscheck the data')
    def step_impl(self):
        self.overview.crosscheck_data()
        logger.info('crosschecked data')
    
    @when(u'I click on the Select Run')
    def step_impl(self):
        self.smoke_test = Smoke_Test_page(self.driver)
        self.login = Login(self.driver)
        self.smoke_test.select_run_option()
        logger.info("clicked on select run button")
    
    @given(u'Check for Validation errors')
    def step_impl(self):
        self.smoke_test = Smoke_Test_page(self.driver)
        self.smoke_test.validation_errors()

    @when(u'I select the run name')
    def step_impl(self):
        self.run_creation = RunCreationPage(self.driver)
        self.run_name_select = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Select_Run_Name')
        self.run_creation.select_run_name(self.run_name_select)
        logger.info("selected the given run name")
        logger.info(self.run_name_select)
    
    @when(u'I enter new run Detail')
    def step_impl(self):
        self.run_name = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Run Name')
        self.run_year = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Run Year')
        self.run_period = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Run Period')
        self.run_creation.new_run_details(self.run_name, self.run_year, self.run_period) 
        logger.info("entered new run details")

    @then(u'I submit the new run')
    def step_impl(self):
        self.run_creation.click_on_submit()
        logger.info("submitted new run")

    @then(u'I confirm that all results are ready')
    def step_impl(self):
        self.run_creation.confirm_all_result_ready()
        logger.info("confirmed that all runs are in results are ready status")

    @when(u'I select the price type')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for analysis class in analysis steps")
        self.price_type_name = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Price Type')
        self.analysis.Select_price_type_name(self.price_type_name)
        logger.info(self.price_type_name)
        logger.info("Price Type Selected under the Run page")
    
    @when(u'I Perform operations on Summary Tab')
    def step_impl(self):
        self.Message = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Note Message')
        self.analysis.Summary_buttons_Operation(self.Message)
        logger.info("Summary Tab Button Operations Performed")
        
    @when(u'I Perform the operations on Summary Tab')
    def step_impl(self):
        self.Message = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Note Message')
        self.smoke_test = Smoke_Test_page(self.driver)        
        self.smoke_test.Summary_buttons_Operation(self.Message)
        logger.info("Summary Tab Button Operations Performed")
    
    @when(u'I select the NDC9, bucket & Add Comment')           
    def step_impl(self):
        self.NDC9 = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'NDC')
        self.Bucket_Name_Select = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Bucket_Name')
        self.Message = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Note Message')
        self.analysis.detail_tab_operation(self.NDC9, self.Bucket_Name_Select, self.Message)
        logger.info("NDC Filter & Comment Button opeartions Performed on Details Tab")
    
    @when(u'I click on the Variance & Add comment, Export')
    def step_impl(self):
        self.Message = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Note Message')
        self.smoke_test = Smoke_Test_page(self.driver)         
        self.smoke_test.click_on_the_variance_button(self.Message)
        logger.info("Variance button opeartions Performed on Details Tab")

    @then(u'I Confirm the Bucket Export')
    def step_impl(self):
        self.analysis.confirm_bucket_export()
        logger.info("performed Export on Bucket tab")

    @then(u'I add new override detail')
    def step_impl(self):
        self.dollars = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Dollars')
        self.units = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Units')
        self.min_value = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Min Value')
        self.note = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Note')
        self.analysis.override_details(self.dollars,self.units,self.min_value,self.note)
        logger.info("added new override detail")

    @when(u'I select the override and click on edit override')
    def step_impl(self):
        self.Edit_Override_Name = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Edit_Override_Name')
        self.Edit_Override_period = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Edit_Override_period')
        self.Edit_Override_ndc = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Edit_Override_ndc')
        self.analysis.select_override_and_click_on_edit_override(self.Edit_Override_Name, self.Edit_Override_ndc, self.Edit_Override_period)
        logger.info("selected the override and click on edit override")

    @then(u'I edit the override details')
    def step_impl(self):
        self.dollars = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'edit_Dollars')
        self.units = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'edit_Units')
        self.min_value = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'edit_Min Value')
        self.note = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'edit_Note')
        self.analysis.edit_override_details(self.dollars,self.units,self.min_value,self.note)
        logger.info("Edited the override details")
    
    @then(u'I select the override and delete Overide')
    def step_impl(self):
        self.Delete_Override_Name = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Delete_Override_Name')
        self.Delete_Override_period = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Delete_Override_period')
        self.Delete_Override_ndc = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Delete_Override_ndc')
        self.analysis.select_override_and_click_on_delete(self.Delete_Override_Name, self.Delete_Override_ndc, self.Delete_Override_period)
        logger.info("selected the override and deleted Overide")

    @then(u'I click on the Rollback')
    def step_impl(self):
        self.analysis.click_on_Rollback_btn()
        logger.info("I clicked on Rollback button")

    @when(u'I login with the different User')
    def step_impl(self):
        environment = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Environment')
        self.login = TestLogin()
        self.login.setUp()
        self.login.open_sparc(environment)
        self.driver = self.login.driver   
        self.user = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC2','UserID')
        self.password = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC2','Password')
        self.login.test_login(self.user, self.password)
        self.client = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Client')
        self.service = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Service')
        self.login.test_config_environment(self.client, self.service)
        logger.info("Logged in as different user for Approval")
    
    @then(u'I click the Final Delivered')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.analysis.click_on_Delivered()
        logger.info("I clicked on Prior Delivered button under Finalization tab")

    @when(u'I login with the original User')
    def step_impl(self):
        environment = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Environment')
        self.login = TestLogin()
        self.login.setUp()
        self.login.open_sparc(environment)
        self.driver = self.login.driver   
        self.user = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','UserID')
        self.password = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Password')
        self.login.test_login(self.user, self.password)
        self.client = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Client')
        self.service = ExclUtlty.dataReader(Repo.testDataSheet_GP,'Smoke_Test_Data','TC1','Service')
        self.login.test_config_environment(self.client, self.service)
        logger.info("loged back with the original User")
         
    @when(u'I enter new run Details for Assessment Run')
    def step_impl(self):
        self.run_name = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1','Assessment_Only_Run_Name')
        self.run_year = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1','Assessment_Only_Run_Year')
        self.run_period = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1','Assessment_Only_Run_Period')
        self.run_creation.new_run_details_with_assessment_run(self.run_name, self.run_year, self.run_period) 
        logger.info("entered new run Details for Assessment Run")

    @when(u'I select the assessment only run name')
    def step_impl(self):
        self.assessment_run_name_select = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Assessment_Only_Run_Name')
        self.run_creation = RunCreationPage(self.driver)
        self.run_creation.select_assessment_run_name(self.assessment_run_name_select)
        logger.info("selected the assessment only run name")

    @when(u'I select the result ready price type and click on it')
    def step_impl(self):
        self.price_type = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Price Type')
        self.run_creation.checking_result_ready_status(self.price_type) 
        logger.info("I selected the result ready price type and clicked on it")

    @then(u'I check that Assessment run can not be approved')
    def step_impl(self):
        self.run_creation.check_assessment_run_can_not_be_approved()
        logger.info("I checked that Assessment run can not be approved")
    
    @when(u'I select the run name with closed status')
    def step_impl(self):
        self.close_name_select = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Close_Run_Name')
        self.run_creation.select_run_name_with_close_status(self.close_name_select)
        logger.info("I selected the run name with closed status")

    @then(u'I click on the create restatement')
    def step_impl(self):
        self.run_creation.click_on_restatement()
        logger.info("I clicked on the create restatement")
    
    @then(u'I ensure the restatement execution')
    def step_impl(self):
        self.restatement_name = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Close_Run_Name')
        self.run_creation.select_restatement_run_name(self.restatement_name)
        logger.info("I ensured the restatement execution")

    @then(u'I select the delete run name and delete')
    def step_impl(self):
        self.run_name_select_delete = ExclUtlty.dataReader(Repo.testDataSheet_GP, 'Smoke_Test_Data', 'TC1', 'Run_Name_to_Delete')
        self.run_creation.select_delete_run_name(self.run_name_select_delete)
        logger.info("I selected the delete run name and clicked on delete button")

  

