from time import time
from behave import *
from GP.automation_test.behave.features.steps import gp_run_creation_steps
from GP.pages.analysis_page import AnalysisPage
from GP.pages.gp_run_creation_page import RunCreationPage
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
import time
from GP.pages.rebate_transfer_page import RebateTransferPage
from GP.pages.downloaded_files_page import DownloadedFilesPage
import allure
from libraries import generics


class Analysis(EnvironmentSetup):
    
    @when(u'I select price type')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.rebatetransfer = RebateTransferPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for analysis class in analysis steps")
        self.price_type_name = self.td_set['Price Type']
        self.analysis.Select_price_type_name(self.price_type_name)
        logger.info("Price Type Selected under the Run page")
    
    @when(u'Click on Data Summary and Approve')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for analysis class in analysis steps")
        self.analysis.Select_price_type_name('Data Summary')
        self.analysis.click_on_Approve_btn()
        logger.info("Price Type Selected under the Run page")
         
    @when(u'Perform operations on Summary Tab and verify downloaded file')
    def step_impl(self):
        self.Message = self.td_set['Note Message']
        self.analysis.Summary_buttons_Operation(self.Message)
        self.downloaded_files = self.rebatetransfer.get_downloaded_files()
        self.file_name = self.analysis.get_splitted_file_for_downloades_for_summary_tab(self.downloaded_files)
        logger.info(self.downloaded_files)
    
    @When(u'I click on Summary Tab')
    def step_impl(self):
        self.analysis.Click_on_Summary_tab()
        logger.info("Clicked on Summary Tab")
             
    @when(u'I click on Detail tab')
    def step_impl(self):
        self.analysis.Click_on_Detail_tab()
        logger.info("Clicked on Detail Tab")
        
    @when(u'I select NDC9, bucket & Add Comment and verify added comment and verify data is valid as per selection')           
    def step_impl(self):
        self.NDC9 = self.td_set['NDC']
        self.Bucket_Name_Select = self.td_set['Bucket_Name']
        self.Message = self.td_set['Note Message']
        self.analysis.detail_tab_operation(self.NDC9, self.Bucket_Name_Select, self.Message)
        self.analysis.verify_comments_for_detail_tab(self.NDC9, self.Bucket_Name_Select, self.Message)
       
    @when(u'I click on Variance & Add comment, Export and verify downloaded file')
    def step_impl(self):
        self.Message = self.td_set['Note Message']
        self.analysis.click_on_variance_button(self.Message)
        self.downloaded_files = self.rebatetransfer.get_downloaded_files()
        self.file_name = self.analysis.get_splitted_file_for_downloades_for_tab(self.downloaded_files)
        logger.info(self.downloaded_files)
                  
    # Bucket tab
    @when(u'I select Bucket Tab')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.analysis.select_bucket_tab()

    @then(u'I Confirm user Can Switch Between Buckets')
    def step_impl(self):
        self.analysis.switch_between_buckets()

    @then(u'I Confirm Bucket Export and verify downloaded file')
    def step_impl(self):
        self.analysis.confirm_bucket_export()
        self.downloaded_files = self.rebatetransfer.get_downloaded_files()
        self.file_name = self.analysis.get_splitted_file_for_downloades_for_tab(self.downloaded_files)
        logger.info(self.downloaded_files)
    
    @then(u'I Confirm Bucket Filter/Sort')
    def step_impl(self):
        self.analysis.confirm_bucket_filter_sort()
        
    # Override tab
    @when(u'I select override Tab')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.analysis.select_override_tab()
    
    @then(u'I add new override details')
    def step_impl(self):
        self.dollars = self.td_set['Dollars']
        self.units = self.td_set['Units']
        self.min_value = self.td_set['Min Value']
        self.note = self.td_set['Note']
        self.NDC11 = self.td_set['NDC']
        self.period_month = self.td_set['Period Month']
        self.analysis.override_details(self.dollars,self.units,self.min_value,self.note,self.NDC11,self.period_month)
        
    @when(u'I select override and click on edit override')
    def step_impl(self):
        self.Edit_Override_Name = self.td_set['Edit_Override_Name']
        self.Edit_Override_period = self.td_set['Edit_Override_period']
        self.Edit_Override_ndc = self.td_set['Edit_Override_ndc']
        self.analysis.select_override_and_click_on_edit_override(self.Edit_Override_Name, self.Edit_Override_ndc, self.Edit_Override_period)

    @then(u'I edit override details')
    def step_impl(self):
        self.dollars = self.td_set['edit_Dollars']
        self.units = self.td_set['edit_Units']
        self.min_value = self.td_set['edit_Min Value']
        self.note = self.td_set['edit_Note']
        self.analysis.edit_override_details(self.dollars,self.units,self.min_value,self.note)

    @then(u'I select override and delete Overide')
    def step_impl(self):
        self.Delete_Override_Name = self.td_set['Delete_Override_Name']
        self.Delete_Override_period = self.td_set['Delete_Override_period']
        self.Delete_Override_ndc = self.td_set['Delete_Override_ndc']
        self.analysis.select_override_and_click_on_delete(self.Delete_Override_Name, self.Delete_Override_ndc, self.Delete_Override_period)
    
    @then(u'I Confirm Summary Asks to re execute')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.price_type = self.td_set['Price Type']
        self.analysis.summary_asks_to_re_execute(self.price_type)    
         
    @When(u'I click on Approve')
    def step_impl(self):
        self.analysis.click_on_Approve_btn()
        logger.info("I clicked on Approve button")
        
    @then(u'I click on Rollback')
    def step_impl(self):
        self.analysis.click_on_Rollback_btn()
        logger.info("I clicked on Rollback button")
        
    @when(u'I click on Approval Tab')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver) 
        self.analysis.click_on_Approval_tab()
        logger.info("I clicked on Approval tab")
        
    @when(u'I click on Finalization Tab')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver) 
        self.analysis.click_on_Finalization_tab()
        logger.info("I clicked on Finalization tab")
    
    @then(u'I click Final Delivered')
    def step_impl(self):
        # self.analysis = AnalysisPage(self.driver)
        self.analysis.click_on_Delivered()
        logger.info("I clicked on Prior Delivered button under Finalization tab")

    @Then(u'I click on Export')
    def step_impl(self):
        self.analysis.click_on_export_button_on_override_tab()
        
    @Then(u'I verify downloaded file')
    def step_impl(self):
        self.downloaded_files = self.rebatetransfer.get_downloaded_files()
        self.file_name = self.analysis.get_splitted_file_for_downloades_for_tab(self.downloaded_files)
        logger.info(self.downloaded_files)

    @Then(u'I verify stage as pending approval for data summary')
    def step_impl(self):
        self.stage_pending_approval = self.td_set['Stage Pending Approval']
        self.index_data_summary = self.td_set['Data Summary Index']
        self.analysis.verify_stage(self.stage_pending_approval,self.index_data_summary)

    @Then(u'I verify submitted by and submitted on column for data summary')
    def step_impl(self):
        self.user_1 = self.td_set['UserID']
        self.index_data_summary_submitted_by = self.td_set['Data Summary Index Submitted By']
        self.analysis.verify_submitted_by_column(self.user_1,self.index_data_summary_submitted_by)
        self.get_system_current_date= self.analysis.get_current_system_date("%Y-%m-%d")
        self.index_data_summary_submitted_on = self.td_set['Data Summary Index Submitted On']
        self.analysis.verify_submitted_on_column(self.get_system_current_date,self.index_data_summary_submitted_on)

    @Then(u'I verify stage as pending approval for selected price type')
    def step_impl(self):
        self.stage_pending_approval = self.td_set['Stage Pending Approval']
        self.index_amp = self.td_set['AMP Index']
        self.analysis.verify_stage(self.stage_pending_approval,self.index_amp)

    @Then(u'I verify submitted by and submitted on column for selected price type')
    def step_impl(self):
        self.user_1 = self.td_set['UserID']
        self.index_amp_submitted_by = self.td_set['AMP Index Submitted By']
        self.analysis.verify_submitted_by_column(self.user_1,self.index_amp_submitted_by)
        self.get_system_current_date= self.analysis.get_current_system_date("%Y-%m-%d")
        self.index_amp_submitted_on = self.td_set['AMP Index Submitted On']
        self.analysis.verify_submitted_on_column(self.get_system_current_date,self.index_amp_submitted_on)

    @when(u'I click on Analysis Tab')
    def step_impl(self):
        self.analysis.click_on_Analysis_tab()
    
    @Then(u'I verify rollback by and rollback on column for selected price type')
    def step_impl(self):
        self.user_1 = self.td_set['UserID']
        self.index_amp_rollback_by = self.td_set['AMP Index Rollback By']
        self.analysis.verify_rollback_by_column(self.user_1,self.index_amp_rollback_by)
        self.get_system_current_date= self.analysis.get_current_system_date("%Y-%m-%d")
        self.index_amp_rollback_on = self.td_set['AMP Index Rollback On']
        self.analysis.verify_rollback_on_column(self.get_system_current_date,self.index_amp_rollback_on)

    @Then(u'I verify stage as approved for selected price type')
    def step_impl(self):
        self.stage_approved = self.td_set['Stage Approved']
        self.index_amp = self.td_set['Finalization Tab Stage Amp Index']
        self.analysis.verify_stage(self.stage_approved,self.index_amp)

    @Then(u'I verify approved by and approved on column for selected price type')
    def step_impl(self):
        self.user_2 = self.td_set['UserID_2']
        self.index_amp_approved_by = self.td_set['Finalization Tab Amp Index Approved By']
        self.analysis.verify_approved_by_column(self.user_2,self.index_amp_approved_by)
        self.get_system_current_date= self.analysis.get_current_system_date("%Y-%m-%d")
        self.index_amp_approved_on= self.td_set['Finalization Tab Amp Index Approved On']
        self.analysis.verify_approved_on_column(self.get_system_current_date,self.index_amp_approved_on)

    @when(u'Perform operations on Summary Tab')
    def step_impl(self):
        self.Message = self.td_set['Note Message']
        self.analysis.Summary_buttons_Operation(self.Message)

    @Then(u'I verify rollback by and rollback on column for selected price type for approval stage')
    def step_impl(self):
        self.user_1 = self.td_set['UserID']
        self.index_amp_rollback_by = self.td_set['AMP Index Rollback By Approval Tab']
        self.analysis.verify_rollback_by_column(self.user_1,self.index_amp_rollback_by)
        self.get_system_current_date= self.analysis.get_current_system_date("%Y-%m-%d")
        self.index_amp_rollback_on = self.td_set['AMP Index Rollback On Approval Tab']
        self.analysis.verify_rollback_on_column(self.get_system_current_date,self.index_amp_rollback_on)

    @Then(u'I exclude record and verify record excluded')
    def step_impl(self):
        self.Message = self.td_set['Note Message']
        self.column_name_tid = self.td_set['Column Name Tid']
        self.bucket_source_name = self.analysis.verify_data_present_for_any_of_the_bucket_sources()
        self.list_of_bucket_source_name = ["DirectSales","Chargebacks","Rebates","Tricare"]
        if self.bucket_source_name in self.list_of_bucket_source_name:
            self.analysis.select_bucket_data_source(self.bucket_source_name)
            self.analysis.verify_exclude_functionality(self.column_name_tid,self.Message)

    @Then(u'I include record and verify record included')
    def step_impl(self):
        self.Message = self.td_set['Note Message']
        self.column_name_tid = self.td_set['Column Name Tid']
        self.bucket_source_name = self.analysis.verify_data_present_for_any_of_the_bucket_sources()
        self.list_of_bucket_source_name = ["DirectSales","Chargebacks","Rebates","Tricare"]
        if self.bucket_source_name in self.list_of_bucket_source_name:
            self.analysis.select_bucket_data_source(self.bucket_source_name)
            self.analysis.verify_include_functionality(self.column_name_tid,self.Message)

    @Then(u'I verify stage as delivered for selected price type')
    def step_impl(self):
        self.stage_delivered = self.td_set['Stage Delivered']
        self.index_delivered = self.td_set['Amp Delivered Index']
        self.analysis.verify_stage(self.stage_delivered,self.index_delivered)

    @Then(u'I verify delivered by and delivered on column for selected price type')
    def step_impl(self):
        self.user_2 = self.td_set['UserID_2']
        self.index_amp_delivered_by = self.td_set['Amp Index Delivered By']
        self.analysis.verify_delivered_by_column(self.user_2,self.index_amp_delivered_by)
        self.get_system_current_date= self.analysis.get_current_system_date("%Y-%m-%d")
        self.index_amp_delivered_by = self.td_set['Amp Index Delivered On']
        self.analysis.verify_delivered_on_column(self.get_system_current_date,self.index_amp_delivered_by)

    @When(u'I click on a bucket')
    def step_impl(self):
        self.downloadfiles = DownloadedFilesPage(self.driver)
        self.analysis.click_on_first_bucket_element()

    @Then(u'I verify lower grid has close panel,new tab and export option')
    def step_impl(self):
     self.analysis.verify_lower_grid_options()

    @Then(u'I verify lower grid close panel working properly')
    def step_impl(self):
        self.analysis.click_on_close_panel_from_lower_grid()

    @when(u'I select NDC9, bucket')           
    def step_impl(self):
        self.NDC9 = self.td_set['NDC']
        self.Bucket_Name_Select = self.td_set['Bucket_Name']
        self.analysis.filter_bucket_name_on_detail_tab(self.NDC9, self.Bucket_Name_Select)

    @when(u'I click on Export button on lower grid tab')           
    def step_impl(self):
        self.analysis.click_on_export_button_on_lower_grid()

    @when(u'I click on new tab button on lower grid tab')           
    def step_impl(self):
        self.analysis.click_on_new_tab_button_on_lower_grid()
        self.analysis.switch_to_child_tab()
    
    @Then(u'I verify new tab is having export functionality')
    def step_impl(self):
        self.analysis.verify_new_tab_options()
        self.analysis.click_on_export_button_on_new_tab_options()
        self.downloaded_files = self.downloadfiles.get_downloaded_files()
        allure.attach("User can see exported file as : "+str(self.downloaded_files),attachment_type=allure.attachment_type.TEXT)
        self.file_name_1 = self.analysis.get_splitted_file_for_downloades_for_lower_grid(self.downloaded_files[0])
        self.file_name_2 = self.analysis.get_splitted_file_for_downloades_for_lower_grid(self.downloaded_files[1])

    @when(u'I select any bucket and click on request NDC9 report')           
    def step_impl(self):
        self.Bucket_Name = self.td_set['Bucket Name Detail Tab']
        self.analysis.select_on_any_bucket(self.Bucket_Name)
        self.analysis.click_on_request_ndc9_report_button()

    @When(u'I select source and NDC9 and submit the request')
    def step_impl(self):
        self.source = self.td_set['Source']
        self.analysis.select_any_source(self.source)
        self.analysis.click_on_ndc9_dropdown()
        self.NDC9 = self.td_set['NDC']
        self.analysis.click_on_ndc9_from_list(self.NDC9)
        self.analysis.click_on_submit_button()

    @when(u'I click on summary tab and click on attachments button')           
    def step_impl(self):
        self.analysis.Click_on_Summary_tab()
        self.analysis.click_on_attachments_button()

    @Then(u'I verify report is generated in attachments popup')           
    def step_impl(self):
         self.NDC9 = self.td_set['NDC']
         self.price_type_name = self.td_set['Price Type']
         self.analysis.verify_report_in_attachments_popup(self.NDC9,self.price_type_name)
    
    @Then(u'I click on export button and verify comments from exported file')           
    def step_impl(self):
        self.analysis.click_on_export_button_on_bucket_tab()
        self.DownloadedFilesPage = DownloadedFilesPage(self.driver)
        self.download_file_name = self.DownloadedFilesPage.copy_remote_file()
        self.get_dict = ExclUtlty.access_data_with_key_pair_value_for_headers_with_key_pair(self.download_file_name,'2022_Q3_CMS_VA Data Summary Cha',1,2)
        allure.attach("User can see exported file data as : "+str(self.get_dict),attachment_type=allure.attachment_type.TEXT)
        if 'Test_Message' in self.get_dict['Notes'] :
            allure.attach("User can see exported file notes and UI notes same : "+str(self.get_dict['Notes']),attachment_type=allure.attachment_type.TEXT)

    @Then(u'I verify red triangle on override tab')           
    def step_impl(self):
        self.analysis.verify_red_triangle_on_override_tab()
        self.get_ndc11_from_override_tab = self.analysis.get_ndc11_from_override_tab()

    @Then(u'I verify dollar and unit amounts')           
    def step_impl(self):
        self.dollars = self.td_set['Dollars']
        self.units = self.td_set['Units']
        self.analysis.verify_dollar_and_unit_amount_on_summary_tab(self.units,self.dollars)

    @Then(u'I verify after re-execution red triangle should be removed')           
    def step_impl(self):
        self.analysis.verify_red_triangle_on_override_tab_is_removed()

    @Then(u'I verify count on override button should be removed')           
    def step_impl(self):
        self.analysis.verify_count_on_override_tab_is_removed()
    
    @when(u'I select NDC9, bucket & Add Comment and edit the comment , and delete the comment')           
    def step_impl(self):
        self.NDC9 = self.td_set['NDC']
        self.Bucket_Name_Select = self.td_set['Bucket_Name']
        self.Message = self.td_set['Note Message']
        self.Message_Edited = self.td_set['Note Message Edited']
        self.analysis.detail_tab_operation_foredit_and_delete(self.NDC9, self.Bucket_Name_Select, self.Message,self.Message_Edited)

    @when(u'I click on execute button')           
    def step_impl(self):
        self.analysis.click_on_execute_button_from_approval_tab()
    
    @Then(u'I verify confirmation popup and click on yes button')           
    def step_impl(self):
        self.price_type_name = self.td_set['Price Type']
        self.analysis.verify_confirmation_popup_is_displayed(self.price_type_name)
        self.analysis.click_on_yes_button_from_confirmation_execution_popup(self.price_type_name)
    
    @Then(u'I verify message popup only price type in queue or analysis may be run and click on ok button')           
    def step_impl(self):
        self.analysis.verify_error_message_popup_displayed()
        
    @Then(u'I verify message popup manager cannot approve both approvals')           
    def step_impl(self):
        self.analysis.verify_error_message_manager_cannot_approve()

    @when(u'I click the disable button')           
    def step_impl(self):
        self.analysis.click_on_disable_enable_button_from_approval_tab()
    
    @Then(u'I verify stage as disabled and execution status as disabled for this run')           
    def step_impl(self):
        self.analysis.verify_stage_as_disabled_and_status_As_disabled_for_run()
    
    @when(u'I click the enable button')           
    def step_impl(self):
        self.analysis.click_on_disable_enable_button_from_approval_tab()
    
    @when(u'I filter price type')
    def step_impl(self):
        self.price_type_name = self.td_set['Price Type']
        self.analysis.filter_price_type_name(self.price_type_name)

    @Then(u'I verify popup Only Price Types in queued or analysis may be overridden')           
    def step_impl(self):
        self.analysis.verify_error_message_popup_on_override_tab_displayed()

    @Then(u'I verify message Only Price Types in queued or analysis may have their overrides altered')           
    def step_impl(self):
        self.analysis.verify_error_message_popup_on_override_tab_altered_displayed()
    
    @Then(u'I verify execute button is disabled in finalization tab')           
    def step_impl(self):
        self.analysis.verify_execute_button_is_disabled_in_finalization_tab()
    
    @Then(u'I verify buttons mark as delivered and rollback are disabled')           
    def step_impl(self):
        self.analysis.verify_mark_as_delivered_and_rollback_is_disabled_in_finalization_tab()

    @When(u'I get analysis price type stage count')           
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        self.list_of_other_stages = ['PENDING_APPROVAL','APPROVED','DELIVERED']
        self.get_dict = self.analysis.get_analysis_stage_price_type_stage_count_at_initial(self.list_of_other_stages)
        generics.capture_screenshot_allure(self.analysis, 'Run Screen')
        self.analysis.click_on_runs_hyperlink()

    @Then(u'I verify analysis price type stage count with run overview screen count')           
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        self.analysis.click_on_runs_hyperlink()
        self.list_of_stages_on_overview_screen = ['QUEUED','ANALYSIS','PENDING_APPROVAL','APPROVED','DELIVERED']
        self.get_dict_of_overview_screen = self.analysis.get_overview_screen_stage_count_at_initial(self.list_of_stages_on_overview_screen)
        if self.get_dict == self.get_dict_of_overview_screen :
            allure.attach("Overview Screen Stage  count is equal for each execution status : "+str(self.get_dict_of_overview_screen),attachment_type=allure.attachment_type.TEXT)

        
    @When(u'I get analysis and approval price type stage count for data summary when sent for approval')           
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        self.get_dict_for_analysis_tab_for_datasummary = self.analysis.get_analysis_stage_price_type_stage_count_when_data_summary_sent_for_approval()
        generics.capture_screenshot_allure(self.analysis, 'Run Screen Inside Run')
        self.analysis.click_on_Approval_tab()
        self.get_dict_for_approval_tab_for_datasummary = self.analysis.get_approval_stage_price_type_stage_count_when_data_summary_sent_for_approval()
        self.get_dict_for_analysis_tab_for_datasummary.update(self.get_dict_for_approval_tab_for_datasummary)
        self.list_of_stages_on_overview_screen = {'APPROVED':0,'DELIVERED':0}
        self.get_dict_for_analysis_tab_for_datasummary.update(self.list_of_stages_on_overview_screen)
        self.analysis.click_on_runs_hyperlink()

    @Then(u'I verify analysis and approval price type stage count with run overview screen count for data summary when sent for approval')           
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        self.analysis.click_on_runs_hyperlink()
        self.list_of_stages_on_overview_screen = ['QUEUED','ANALYSIS','PENDING_APPROVAL','APPROVED','DELIVERED']
        self.get_dict_of_overview_screen_for_datasummary_forapproval = self.analysis.get_overview_screen_stage_count_at_initial(self.list_of_stages_on_overview_screen)
        allure.attach("Overview Screen Stage Count Dictionary  and Inside Run Screen Stage count is same: "+str(self.get_dict_of_overview_screen_for_datasummary_forapproval)+" "+str(self.get_dict_for_analysis_tab_for_datasummary),attachment_type=allure.attachment_type.TEXT)

    @when(u'I verify pencil icon is displayed and click on pencil icon')           
    def step_impl(self):
        self.analysis.click_on_pencil_icon_for_any_filtered_item()
    
    @Then(u'I verify label under price type setting popup')           
    def step_impl(self):
        self.analysis.verify_price_type_Settings_popup_with_all_headers_renamed()

    @When(u'I get the version count')
    def step_impl(self):
        self.analysis = AnalysisPage(self.driver)
        self.login = Login(self.driver)
        self.get_latest_version_count = self.analysis.get_latest_version_count()

    @Then(u'I verify user can see all versions of that price type')           
    def step_impl(self):
        self.analysis.verify_versions_list_of_price_type_with_dropdown_values(self.get_latest_version_count)
        
    @When(u'I select the latest price type and click on save button')           
    def step_impl(self):
        self.analysis.select_latest_dropdown_version_and_click_on_save_button()
    
    @Then(u'I verify version in stage cannot be changed and execution of price type is also not possible')           
    def step_impl(self):
        self.analysis.verify_versions_and_execution_in_approved_and_finalized_stage_is_not_possible()
       