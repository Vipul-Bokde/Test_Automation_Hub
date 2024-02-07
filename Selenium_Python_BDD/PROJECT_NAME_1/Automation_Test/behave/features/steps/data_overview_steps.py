from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.utilities.logs_util import logger
from GP.pages.data_overview_page import DataOverviewPage
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from libraries import generics
from GP.pages.main_page import MainPage
from GP.pages.rebate_transfer_page import RebateTransferPage
class DataOverview(EnvironmentSetup):

    @given('click on upload button on overview page')
    def step_impl(self):
        self.overview = DataOverviewPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for overview class in DataOverview step")
        self.overview.click_on_upload_button()

    @when('select file type, template and refresh option and click on Submit')
    def step_impl(self):
        self.overview = DataOverviewPage(self.driver)
        self.FileType = self.td_set['FileType']
        self.overview.select_file_type(self.FileType)
        self.use_template = self.td_set['Use_Template']
        self.source_value = self.td_set['Source_Value']
        self.file_template = self.td_set['File_Template']
        self.overview.select_source_template(self.source_value, self.file_template,self.use_template)
        self.full_refresh = self.td_set['Full_Refresh']
        self.file_template_refresh = self.td_set['File_Template_Refresh']
        self.overview.select_refresh_option(self.full_refresh, self.file_template_refresh)
        self.file_name = self.td_set['File_to_Upload']
        self.file_to_upload = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_name))
        logger.info(self.file_to_upload)
        self.overview.upload_file(self.file_to_upload)
        self.overview.click_on_submit_button()
        generics.capture_screenshot_allure(self.overview, 'Upload File pop-up')

    @when('user should navigate to upload screen then I see the file that was uploaded')
    def step_impl(self):
        logger.info("user should redirect to upload screen")   
        self.file_name = self.td_set['File_to_Upload']
        self.overview.check_uploaded_file(self.file_name)
        generics.capture_screenshot_allure(self.overview, 'Uploads Screen')

    @then('I take data from uploaded file')
    def step_impl(self):
        self.upload_column_value_list = self.overview.get_upload_screen_data()
        logger.info(self.upload_column_value_list)
        logger.info('took data from uploaded file')
        generics.capture_screenshot_allure(self.overview, 'Uploaded File Data')
    
    @then('I click on uploaded source and period value from overview screen')
    def step_impl(self):
        self.overview.navigate_to_overview_screen()
        self.FileType = self.td_set['FileType']
        self.period = self.overview.click_on_upload_period_and_source(self.FileType)
    
    @then('I verify view data and database count for that source and period')
    def step_impl(self):
        self.ui_record_count = self.overview.get_view_data_count()
        self.main_page = MainPage(self.driver)
        self.client_id_query = self.td_set['Client_id_query']
        self.data_count_query = self.td_set['Data_count_query']
        self.client_id = self.main_page.get_client_id( self.client_id_query)
        self.rebate_transfer = RebateTransferPage(self.driver)
        self.client_id = self.rebate_transfer.get_count_from_DB( self.client_id)
        logger.info("Client id is: "+self.client_id)
        self.overview = DataOverviewPage(self.driver)
        self.db_record_count = self.overview.get_view_data_db_count(self.client_id,self.data_count_query,self.period)
        self.rebate_transfer = RebateTransferPage(self.driver)
        self.db_record_count = self.rebate_transfer.get_count_from_DB( self.db_record_count)
        logger.info("DB record count: "+self.db_record_count)
        self.rebate_transfer.verify_UI_and_DB_records(self.ui_record_count,self.db_record_count)
        
        
    @when('I navigate to view data screen')
    def step_impl(self):
        self.View_data_dropdown_value = self.td_set['View_data_dropdown_value']
        self.overview.select_viewdata_from_burger_menu(self.View_data_dropdown_value)
        logger.info('navigated to view data screen')

    @then('I crosscheck data')
    def step_impl(self):
        self.overview = DataOverviewPage(self.driver)
        self.FileType = self.td_set['FileType']
        self.overview.crosscheck_data(self.FileType,self.upload_column_value_list)
        logger.info('crosschecked data')
        generics.capture_screenshot_allure(self.overview, 'View Data Results')
        self.login.close_browser()

    @given('I click on validate button on overview screen')
    def step_impl(self):
        self.overview = DataOverviewPage(self.driver)
        self.overview.validate()
        generics.capture_screenshot_allure(self.overview, 'Validate Button')

    @when('I select validation data source')
    def step_impl(self):
        self.source_all = self.td_set['Source_ALL']
        self.source_ds = self.td_set['Source_DS']
        self.source_cbk  = self.td_set['Source_CBK'] 
        self.source_reb = self.td_set['Source_REB']
        self.source_tri = self.td_set['Source_TRI']
        self.overview.select_validation_source(self.source_all, self.source_ds, self.source_cbk,self.source_reb,self.source_tri)
        generics.capture_screenshot_allure(self.overview, 'Validation Source')

    @when('I select validation period')
    def step_impl(self):
        self.validation_type = self.td_set['Validation_Type']
        self.custom_start_date = self.td_set['Custom_Start_Date']
        self.custom_end_date  = self.td_set['Custom_End_Date']
        self.overview.select_validation_type(self.validation_type,self.custom_start_date,self.custom_end_date)
        generics.capture_screenshot_allure(self.overview, 'Validation Period')

    @then('I click on validate button and wait till validation completes')
    def step_impl(self):
        self.overview.click_on_validate()
 
    @then('I Check validation Results status')
    def step_impl(self):
        self.overview.validation_results()
        generics.capture_screenshot_allure(self.overview, 'Validation Results')
        self.login.close_browser()
        
    @then('I click on cancel button')
    def step_impl(self):
        self.overview.click_on_cancel()
        generics.capture_screenshot_allure(self.overview, 'Click on Cancel Button')
        self.login.close_browser()
    
    @given('Check validation results exist or not')
    def step_impl(self):
        self.overview = DataOverviewPage(self.driver)
        self.overview.check_validation_results()
        generics.capture_screenshot_allure(self.overview, 'Validation Results')
        
    @when('I check "{missing_validation_header}" validation')
    def step_impl(self,missing_validation_header):
        self.overview.check_missing_join(missing_validation_header)
        
    @then('I download "{missing_validation_join_button}" file')
    def step_impl(self,missing_validation_join_button):
        self.overview.download_missing_join_file(missing_validation_join_button)