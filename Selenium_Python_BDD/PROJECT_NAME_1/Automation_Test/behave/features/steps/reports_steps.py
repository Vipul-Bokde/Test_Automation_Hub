from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.reports_page import reportpage
import allure
from allure_commons.types import AttachmentType
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from GP.pages.rebate_transfer_page import RebateTransferPage
from libraries import generics
from GP.pages.downloaded_files_page import DownloadedFilesPage

class reports(EnvironmentSetup):
    
    @given(u'I select credit balance report option under reports menu')
    def step_impl(self):
        self.reports = reportpage(self.driver)
        self.DownloadedFilesPage = DownloadedFilesPage(self.driver)
        self.login = Login(self.driver)
        self.reports.select_global_from_burger_menu()
        self.download_file_name = self.DownloadedFilesPage.copy_remote_file()
                
    @Then(u'I verify credit balance report data')
    def step_impl(self):
        ExclUtlty.open_excel_and_print_sheetnames(self.download_file_name)
        self.first_row_data = ExclUtlty.access_data_from_Specific_row_and_for_merged_columns(self.download_file_name,'Credit Balance',0,1,0)
        self.client_name = self.td_set['Client']
        if self.client_name in self.first_row_data :
            allure.attach("Credit Balance Report Excel report header and verified header are same : "+self.first_row_data,attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Credit Balance Report Excel report header and verified header are not same : "+self.first_row_data,attachment_type=allure.attachment_type.TEXT)
        self.credit_balance_report_column_headers_from_excel = ExclUtlty.access_data_from_single_specific_row_and_multiple_columns_for_that_specific_row(self.download_file_name,'Credit Balance',2)
        self.list_ofcolumn_headers_for_credit_balance_report = ['Contracting Entity',
        'Credit Invoice Year/Period','Credit Invoice ID','Credit Invoice Name','Original Credit Amount',
        'Updated Credit Balance','Applied Invoice Year/Period','Applied Invoice ID',
        'Applied Credit Invoice Name','Applied Credit Invoice Calc Amt','Applied Credit Amount',
        'Remaining Credit Balance']
        if self.list_ofcolumn_headers_for_credit_balance_report == self.credit_balance_report_column_headers_from_excel:
            allure.attach("Credit Balance Report Excel column headers and verified headers are same : "+str(self.credit_balance_report_column_headers_from_excel),attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Credit Balance Report Excel column headers and verified headers are not same : "+str(self.credit_balance_report_column_headers_from_excel) +"  "+str(self.list_ofcolumn_headers_for_credit_balance_report),attachment_type=allure.attachment_type.TEXT)

    @given(u'I select Control and Reasonability Report option under reports menu')
    def step_impl(self):
        self.reports = reportpage(self.driver)
        self.DownloadedFilesPage = DownloadedFilesPage(self.driver)
        self.reports.select_control_and_reasonability_report_menu_from_burger_menu()

    @When(u'I select current date and prior date')
    def step_impl(self):
        self.reports.verify_header_popup_for_control_and_reasonability_report()
        self.reports.click_on_current_date_input()
        self.current_date = self.td_set['Current Date']
        self.reports.select_date_from_calender(self.current_date)
        self.reports.click_on_prior_date_input()
        self.prior_date = self.td_set['Prior Date']
        self.reports.select_date_from_calender(self.prior_date)
        generics.capture_screenshot_allure(self.reports, 'Reports Date')

    @Then(u'I verify prior date is less than current date')
    def step_impl(self):
        self.prior_date = self.td_set['Prior Date']
        self.current_date = self.td_set['Current Date']
        self.reports.verify_prior_date_is_less_than_current_date(self.prior_date,self.current_date)

    @Then(u'I click on submit button')
    def step_impl(self):
        self.reports.click_on_submit_from_reports_popup()

    @Then(u'I verify headers and data from excel and DB')
    def step_impl(self):
        self.download_file_control_And_reasonability = self.DownloadedFilesPage.copy_remote_file()
        ExclUtlty.open_excel_and_print_sheetnames(self.download_file_control_And_reasonability)
        self.excel_header = ExclUtlty.access_single_data_from_specific_cell(self.download_file_control_And_reasonability,'C&R Detail Report','A1')
        self.verified_header = self.td_set['Control & Reasonability Header']
        if self.excel_header == self.verified_header:
            allure.attach("Control and Reasonability excel report header and verified header is same : "+self.excel_header,attachment_type=allure.attachment_type.TEXT)
        self.excel_company_name = ExclUtlty.access_single_data_from_specific_cell(self.download_file_control_And_reasonability,'C&R Detail Report','B2')
        self.verified_company_name = self.td_set['Client']
        if self.excel_company_name == self.verified_company_name:
            allure.attach("Control and Reasonability excel report company name and verified company name is same : "+self.excel_company_name,attachment_type=allure.attachment_type.TEXT)
        self.excel_report_name = ExclUtlty.access_single_data_from_specific_cell(self.download_file_control_And_reasonability,'C&R Detail Report','B3')
        self.verified_report_name = self.td_set['Report Name 1']
        if self.excel_report_name == self.verified_report_name:
            allure.attach("Control and Reasonability excel report name and verified report name is same : "+self.excel_report_name,attachment_type=allure.attachment_type.TEXT)
        self.get_dict = ExclUtlty.access_data_with_key_pair_value_for_headers_with_key_pair(self.download_file_control_And_reasonability,'C&R Detail Report',8,9)
        allure.attach("Control and Reasonability excel report key pair values : "+str(self.get_dict),attachment_type=allure.attachment_type.TEXT)
        if self.get_dict['Source'] == 'Rebate':
            self.get_query_for_rebate = self.td_set['Query For Rebate']
            self.get_client_ID = self.td_set['Client ID']
            self.get_period_month = self.get_dict.get('Period')
            self.returned_result = self.reports.data_base_connection_and_get_DB_record_for_control_and_reasonability_report(self.get_query_for_rebate,self.get_client_ID,self.get_period_month)
            allure.attach("Control and Reasonability DB record is : "+str(self.returned_result),attachment_type=allure.attachment_type.TEXT)
            self.get_NDC_11_for_source = self.get_dict.get('NDC11')
            self.get_product_description = self.get_dict.get('Product Description')
            if self.get_NDC_11_for_source or self.get_product_description in self.returned_result:
                allure.attach("Excel and DB records for NDC 11 and Product Description is same : "+self.get_NDC_11_for_source +" "+self.get_product_description,attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach("Excel and DB records for NDC 11 and Product Description is not same:  ",attachment_type=allure.attachment_type.TEXT)
        elif self.get_dict['Source'] == 'Chargeback':
            self.get_query_for_chargeback = self.td_set['Query For Chargeback']
            self.get_client_ID = self.td_set['Client ID']
            self.get_period_month = self.get_dict.get('Period')
            self.returned_result = self.reports.data_base_connection_and_get_DB_record_for_control_and_reasonability_report(self.get_query_for_chargeback,self.get_client_ID,self.get_period_month)
            self.get_NDC_11_for_source = self.get_dict.get('NDC11')
            self.get_product_description = self.get_dict.get('Product Description')
            if self.get_NDC_11_for_source or self.get_product_description in self.returned_result:
                allure.attach("Excel and DB records for NDC 11 and Product Description is same : "+self.get_NDC_11_for_source +" "+self.get_product_description,attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach("Excel and DB records for NDC 11 and Product Description is not same:  ",attachment_type=allure.attachment_type.TEXT)

    @given(u'I select Calc Audit Log Report option under reports menu')
    def step_impl(self):
        self.reports = reportpage(self.driver)
        self.DownloadedFilesPage = DownloadedFilesPage(self.driver)
        self.reports.select_calc_audit_report_menu_from_burger_menu()

    @When(u'I select Start date and end date')
    def step_impl(self):
        self.start_date = self.td_set['Start Date']
        self.reports.click_on_start_date_input(self.start_date)
        self.end_date = self.td_set['End Date']
        self.reports.click_on_end_date_input(self.end_date)
        generics.capture_screenshot_allure(self.reports, 'Reports Date')

    @Then(u'I click on submit button for cal audit log')
    def step_impl(self):
        self.reports.click_on_submit_from_calc_audit_reports_popup()

    @Then(u'I verify headers and data from excel and DB for cal audit log')
    def step_impl(self):
        self.download_file_calc_audit_log = self.DownloadedFilesPage.copy_remote_file()
        ExclUtlty.open_excel_and_print_sheetnames(self.download_file_calc_audit_log)
        self.header = ExclUtlty.access_single_data_from_specific_cell(self.download_file_calc_audit_log,'GP Calc Audit Log','A1')
        self.client_name = self.td_set['Client']
        if self.client_name in self.header:
            allure.attach("Calc Audit Log Excel report header and verified header are same : "+self.header,attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Calc Audit Log Excel report header and verified header are not same : "+self.header,attachment_type=allure.attachment_type.TEXT)
        self.column_headers_list = ['Name','Calc Id','Created On','Price Type','Price Type Version','Restatement',
            'Stage','Approval Submitted By','Approval Submitted Date','Approved By','Approved Date',
            'Mark as Delivered By','Mark as Delivered Date','Run Closed By','Run Closed Date',
            'Rolled Back By','Rolled Back Date','Restatement By','Restatement Date']
        self.excel_report_calc_audit_log_headers = ExclUtlty.access_data_from_single_specific_row_and_multiple_columns_for_that_specific_row(self.download_file_calc_audit_log,'GP Calc Audit Log',2)
        if self.column_headers_list == self.excel_report_calc_audit_log_headers:
            allure.attach("Calc Audit Log Report Column headers are same as verified : "+str(self.excel_report_calc_audit_log_headers),attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Calc Audit Log Report Column headers are not same as verified : "+str(self.excel_report_calc_audit_log_headers)+" "+str(self.column_headers_list),attachment_type=allure.attachment_type.TEXT)
        self.get_dict = ExclUtlty.access_data_with_key_pair_value_for_headers_with_key_pair(self.download_file_calc_audit_log,'GP Calc Audit Log',2,13)
        allure.attach("Calc Audit Log Excel Report Dictionary key pair value : "+str( self.get_dict),attachment_type=allure.attachment_type.TEXT)
        self.get_query_for_calc_audit_log = self.td_set['Calc Audit Log Query']
        self.get_client_ID = self.td_set['Client ID']
        self.get_start_date = self.td_set['Start Date for DB']
        self.get_end_date = self.td_set['End Date for DB']
        self.calc_audit_log_result = self.reports.data_base_connection_and_get_DB_record_for_calc_audit_log_report(self.get_query_for_calc_audit_log,self.get_client_ID,self.get_start_date,self.get_end_date)
        self.excel_report_run_name = ExclUtlty.access_single_data_from_specific_cell(self.download_file_calc_audit_log,'GP Calc Audit Log','A3')
        if self.excel_report_run_name in self.calc_audit_log_result:
            allure.attach("Calc Audit Log Excel Report Run name is same as DB : "+str(self.excel_report_run_name),attachment_type=allure.attachment_type.TEXT)

