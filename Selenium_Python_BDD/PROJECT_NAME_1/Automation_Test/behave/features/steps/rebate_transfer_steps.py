from behave import *
from GP.pages.rebate_transfer_page import RebateTransferPage
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
import allure

class RebateTransfer(EnvironmentSetup):
  
    @when(u'I select price rebate transfter from hamburger menu')
    def step_impl(self):
        self.rebatetransfer = RebateTransferPage(self.driver)
        self.login = Login(self.driver)
        self.rebatetransfer.select_rebate_transfer_from_burger_menu()
        
    @when(u'Click on transfer button')
    def step_impl(self):
        self.Invoice_Name = self.td_set['Invoice Name']
        self.rebatetransfer.click_on_transfer_button(self.Invoice_Name)        

    @then(u'Add the period Date')
    def step_impl(self):
        self.Date = self.td_set['Date']
        self.rebatetransfer.select_period_date(self.Date)
        
    @then(u'Click on a submit button')
    def step_impl(self):
        self.rebatetransfer.click_on_submit_from_transfer_options_popup_page()

    @given(u'I click on Export of File')
    def step_impl(self):
        self.Record_count_UI = self.rebatetransfer.click_on_export_btn()
        self.download_file_loc = self.rebatetransfer.copy_remote_file()

    @then(u'I validate export of grid in Rebate transfer screen')
    def step_impl(self):
        self.rebatetransfer.navigate_back_to_screen()
        self.rebatetransfer.validate_exported_file(self.download_file_loc,self.Record_count_UI)

    @When(u'I filter the status column for unsettled invoice')
    def step_impl(self):
        self.column_name = self.td_set['Column Name Status To Filter']
        self.txt_status = self.td_set['Status Filter Text']
        self.rebatetransfer.click_on_any_filter_icon(self.column_name)
        self.rebatetransfer.enter_text_on_any_filter_icon_search_box(self.txt_status)
        self.rebatetransfer.click_on_rebate_transfer_page()

    @Then(u'I verify the status column for unsettled invoice')
    def step_impl(self):
        self.txt_status = self.td_set['Status Filter Text']
        self.rebatetransfer.verify_status_column_for_unsettled_invoice(self.txt_status)
    
    @Then(u'I get data for Dollar Amount column')
    def step_impl(self):
        self.txt_column_name_dollar_amount = self.td_set['Column Name Dollar Amount']
        self.txt_column_index_dollar_amount = self.td_set['Column Index Dollar Amount']
        self.get_data_of_column_dollar_amount = self.rebatetransfer.get_text_of_first_row_for_column(self.txt_column_name_dollar_amount,self.txt_column_index_dollar_amount)
        allure.attach("Dollar Amount Is : "+self.get_data_of_column_dollar_amount,attachment_type=allure.attachment_type.TEXT)

    @When(u'I verify Dollar Amount and get data for column Internal ID and rebate source I click on transfer button in rebate transfer page')
    def step_impl(self):
        self.txt_data_column_name_rebate_source = self.td_set['Column Name Rebate Source']
        self.txt_column_index_rebate_source = self.td_set['Column Index Rebate Source']
        self.txt_data_column_name_internal_id = self.td_set['Column Name Internal ID']
        self.txt_column_index_internal_id = self.td_set['Column Index Internal ID']
        self.txt_row_index_1 = self.td_set['Row Index 1']
        self.txt_row_index_2 = self.td_set['Row Index 2']
        self.txt_row_index_1_for_rebate_transfer = self.td_set['Row Index for RebateTransfer']
        self.internal_id_and_rebate_source = self.rebatetransfer.verify_dollar_amount_and_get_data_and_click_on_rebate_transfer_button(self.get_data_of_column_dollar_amount,self.txt_data_column_name_rebate_source,self.txt_column_index_rebate_source,self.txt_data_column_name_internal_id,self.txt_column_index_internal_id,self.txt_row_index_1,self.txt_row_index_2,self.txt_row_index_1_for_rebate_transfer,self.txt_data_column_name_internal_id)
        allure.attach("Internal Id and Rebate Source Is : "+self.internal_id_and_rebate_source,attachment_type=allure.attachment_type.TEXT)
        self.get_internal_id = self.rebatetransfer.split_internal_id_and_get_internal_id(self.internal_id_and_rebate_source)
        self.get_rebate_source = self.rebatetransfer.split_rebate_source_and_get_rebate_source(self.internal_id_and_rebate_source)

    @Then(u'I Add the period Date')
    def step_impl(self):
        self.txt_get_date_of_rebate_transfer = self.rebatetransfer.get_current_system_date("%m/%d/%Y")
        allure.attach("User can get current system date as : "+self.txt_get_date_of_rebate_transfer,attachment_type=allure.attachment_type.TEXT)
        self.rebatetransfer.select_period_date(self.txt_get_date_of_rebate_transfer)
        allure.attach("User select current system date as : "+self.txt_get_date_of_rebate_transfer,attachment_type=allure.attachment_type.TEXT)
    
    @Then(u'I verify the rebate transfer is successfully done on rebate transfer page')
    def step_impl(self):
        self.txt_hamburger_menu_rebate_transfer = self.td_set['Hamburger Menu Rebate Transfer']
        self.column_name = self.td_set['Column Name Internal ID']
        self.rebatetransfer.wait_for_screen_to_load(self.txt_hamburger_menu_rebate_transfer)
        self.rebatetransfer.wait_for_min_time()
        self.rebatetransfer.click_on_any_filter_icon(self.column_name)
        self.rebatetransfer.enter_text_on_any_filter_icon_search_box(self.get_internal_id)
        self.rebatetransfer.click_on_rebate_transfer_page()
        self.rebatetransfer.verify_rebate_transfer_successfully_done_and_internal_id_not_displayed(self.get_internal_id)
    

    @When(u'I select view data from hamburger menu')
    def step_impl(self):
        self.txt_hamburger_menu_view_data = self.td_set['Hamburger Menu View Data']
        self.rebatetransfer.select_any_menu_from_burger_menu(self.txt_hamburger_menu_view_data)
        
    @When(u'I select combobox dropdown')
    def step_impl(self):
        self.txt_combobox_menu_rebate = self.td_set['Combobox Menu Rebate']
        self.rebatetransfer.select_any_menu_from_combobox_menu(self.txt_combobox_menu_rebate)
        self.txt_page_size = self.td_set['Pages']
        self.rebatetransfer.select_page_size_from_dropdown(self.txt_page_size)
    
    @Then(u'I filter the settlement number and period month')
    def step_impl(self):
        self.length = self.td_set['LoopLength']
        self.rebatetransfer.scroll_to_view(self.length)
        self.column_name_settlement_num = self.td_set['Column Name Settlement Num']
        self.rebatetransfer.click_on_any_filter_icon(self.column_name_settlement_num)
        self.rebatetransfer.enter_text_on_any_filter_icon_search_box(self.get_internal_id)
        self.rebatetransfer.click_on_view_data_page()
        self.column_name_period_month = self.td_set['Column Name Period Month']
        self.rebatetransfer.click_on_any_filter_icon(self.column_name_period_month)
        self.txt_date_of_period_month = self.rebatetransfer.get_date_of_period_month(self.txt_get_date_of_rebate_transfer)
        self.rebatetransfer.enter_text_on_any_filter_icon_search_box(self.txt_date_of_period_month)
        self.rebatetransfer.click_on_view_data_page()

    @Then(u'I verify settlement number period month and rebate source is same as selected in rebate transfer page')
    def step_impl(self):
        self.column_col_id_settlement_num = self.td_set['Column Col ID Settlement Num']
        self.column_col_id_period_month = self.td_set['Column Col ID Period Month']
        self.column_col_id_rebate_source = self.td_set['Column Col ID Rebate Soutrce']
        self.rebatetransfer.verify_filtered_data_is_displayed(self.column_col_id_settlement_num,self.get_internal_id)
        self.rebatetransfer.verify_filtered_data_is_displayed(self.column_col_id_period_month,self.txt_date_of_period_month)
        self.rebatetransfer.verify_filtered_data_is_displayed(self.column_col_id_rebate_source,self.get_rebate_source)

    @Then(u'I verify records of UI and DB are equal for selected settlement number')
    def step_impl(self):
        self.get_record_count_of_UI = self.rebatetransfer.get_record_count_of_UI()
        allure.attach("Get Record Count from UI : "+self.get_record_count_of_UI,attachment_type=allure.attachment_type.TEXT)
        self.client = self.td_set['Client']
        self.sql_query = self.td_set['SQL_Query_Rebate_Transfer']
        logger.info(self.sql_query)
        allure.attach("Client is : "+self.client,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Settlement No: "+self.get_internal_id,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Period Month: "+self.txt_date_of_period_month,attachment_type=allure.attachment_type.TEXT)
        self.DB_count = self.rebatetransfer.data_base_connection_and_get_DB_record_count(self.sql_query,self.client,self.get_internal_id,self.txt_date_of_period_month)
        self.get_DB_count = self.rebatetransfer.get_count_from_DB(self.DB_count)
        self.rebatetransfer.verify_UI_and_DB_records(self.get_record_count_of_UI,self.get_DB_count)
    
    @Then(u'I check data is available for filtered settlement number')
    def step_impl(self):
        self.length = self.td_set['LoopLength']
        self.column_name_settlement_num = self.td_set['Column Name Settlement Num']
        self.column_col_id_settlement_num= self.td_set['Column Col ID Settlement Num']
        self.txt_hamburger_menu_view_data= self.td_set['Hamburger Menu View Data']
        self.txt_page_size = self.td_set['Pages']
        self.rebatetransfer.verify_data_for_settlement_num(self.length,self.column_name_settlement_num,self.get_internal_id,self.column_col_id_settlement_num,self.txt_hamburger_menu_view_data,self.txt_page_size)