from re import S
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators,forms_rfn
from GP.utilities.logs_util import logger
import allure
from allure_commons.types import AttachmentType
import time
import os
from selenium.webdriver.common.by import By
from libraries import generics
from libraries import switch_windows_tabs


class AnalysisPage(EnvironmentSetup):
    
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        
    # locators
        self.Filter_Icon = "//div[@col-id='price_type.name']/div/span"
        self.Search_box = "//div/input[@class= 'ag-filter-filter']"
        self.Price_type = "(//div[@role='gridcell'][@col-id='price_type.name'])[1]"
        self.validation_msg = "//div/button[@data-dismiss='alert']"
        
    # search filter and textbox
        self.filter_icon = "//div[@col-id='name']/div[contains(@class,'ag-cell-label-container')]/span"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"
        self.run_filter_icon = "//div[@col-id='price_type.name']/div[contains(@class,'ag-cell-label-container')]/span"
        self.result_ready = "//div[@col-id='status']/div[contains(@class,'ag-cell-label-container')]/span"
        self.runtime_error = "//modal[@id='price-type-runtime-error']/div[@class='sparq-modal']/div[@class='sparq-modal-header']"
        self.runtime_error_accept = "//div[@class='sparq-modal']/div[@class='sparq-modal-footer']/button[@class='btn btn-primary w-75']"
        self.run_click = "//div[@row-index='0']/div[@col-id='name']" 
              
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
        self.Summay_File_Upload_Btn = "(//div/button[@type='submit'])[4]"
        #self.Summay_Attachments_close_Btn = "(//div/button[@type='button'])[20]"
        self.Summay_Attachments_close_Btn = "(//button[@type='button'][contains(.,'Close')])[2]"

        self.Summary_Comments_btn = "//div/button[@id= 'restore-sort']"
        self.Summary_Add_Note_btn = "//div/button[@id='add-note-button']"
        self.Summary_Message_Txt_Box= "//tbody/tr/td[@class='col-md-7']/textarea[@type='text']"
        self.Summay_Save_Note_Btn = "//td/button[@id='save-note']"
        self.Summay_Cancel_Note_Btn = "//div/button[@id='hide-note-button']"        
        self.Summay_Run_Report_Btn = "//div[@class= 'btn-toolbar']/div/button[@title='Run Report']"
        self.Summay_Export_Btn = "//div[@class= 'btn-toolbar']/div/button[@title='Export']"
        self.msg_an_error_occuredon_output_tab = "//div[contains(.,'An error occured while generating report')]"

    # Details Tab
        self.Detail_Tab = "//div/uL[@id='run-price-type-tabs']/li[2]"
        self.NDC9_DropDown = "(//div[@class='col-auto']/select[@class= 'form-control ng-untouched ng-pristine ng-valid'])[2]"   
        self.Bucket_Filter_Icon = "(//div/span/span[@class= 'ag-icon ag-icon-menu'])[1]"
        self.Bucket_Search_Box = "//div/input[@id='filterText']"
        self.Bucket_Check_Box = "//span/span[@class='ag-selection-checkbox']"
        self.Detail_Comment_Btn = "(//button[@id= 'restore-sort'])[2]"
        self.Detail_Note_Add_Btn = "//div/button[@id= 'add-note-button']"
        self.Detail_Note_Text_Box = "(//tbody/tr/td[@class='col-md-7']/textarea[@type='text'])[1]"
        self.Detail_Note_Save_Btn = "//td/button[@id='save-note']"
        self.Detail_Note_cancel_btn = "//div/button[@id= 'hide-note-button']"
        self.btn_request_ndc9_report = "//button[@title='ExportNDC9']"
        self.btn_delete_note_detail_tab = "//button[@id='delete-note']"
        self.txt_data_detail_tab_first_row = "(//span[@ref = 'eCellValue'])[1]"

    # Var
    # Variance Button 
        self.Variance_Btn = "//div/button[@id= 'var-failure-btn']"
        self.V_Bucket_Check_Box= "((//div[@ref= 'eCenterContainer'])[2]/div/div/span/span)[1]"
        self.V_Comment_Btn = "//div/button[@id = 'show-notes']"
        self.V_Add_Note_Btn = "//div/button[@id='add-note-button']"
        self.V_Note_Text_Box = "//tbody/tr/td[@class='col-md-7']/textarea[@type='text']"
        self.V_Note_Save_Btn = "//td/button[@id='save-note']"
        self.V_Note_cancel_btn = "//div/button[@id= 'hide-note-button']"
        self.V_Cancel_btn = "//div/button[@id='hide-var-failures-button']"
        self.V_Export = "//div/button[@title='Export']"
        
    # bucket tab
        self.bucket_tab = "(//div/ul[@class='nav nav-tabs mt-1 ml-2']/li[@class='nav-item']/a)[3]"
        self.bucket_dropdown = "//div[@class='col-auto']/select"
        self.bucket_export = "//div[@id='bucket-options']/button[@class='btn btn-secondary']"
        self.t_ids = "//div[@role='row']/div[@col-id='tid']"
        self.t_id_wait = "(//div[@col-id='tid'])[1]"
        self.bucket_source_first_row_data = "(//div[@col-id='tid'])[4]"
        self.bucket_source_first_row_exclude_status= "(//div[@col-id='Excluded']/span)[2]"
        self.Bucket_chkbox = "//input[@id='exclude-transaction']"
        self.Bucket_Note_Text_Box = "(//tbody/tr/td[@class='col-md-7']/textarea[@type='text'])[2]"
        self.Bucket_Note_Save_Btn = "(//td/button[@id='save-note'])[2]"
        self.drp_source_ndc9_buckets = "//label[text()='Source']/parent::div/child::select"
        self.drp_click_ndc9 = "//div[@class='multiselect-dropdown']"
        self.btn_submit_ndc9_buckets_popup = "(//button[contains(.,'Submit')])[3]"
        self.bucket_source_filtered_data = "(//div[@col-id='tid'])[2]"
        self.txt_get_ndc11_column_override_tab = "(//div[@col-id = 'ndc11'])[2]"
    
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
        self.btn_Export_override_tab = "//button[@title='Export']"
        self.icon_red_triangle = "//i[@class='fa fa-exclamation-triangle text-danger']"
        self.txt_count_on_override_tab = "//strong[text()='Overrides (1)']"


     # runs screen
        self.price_type_select = "(//div[@class='ag-cell ag-cell-not-inline-editing ag-cell-with-height ag-cell-no-focus ag-cell-value'])[1]"
        self.checkbox = "//div/checkbox-renderer/input[@type='checkbox']"
        self.execute_all_btn = "//div[@class='btn-group']/button[@id='execute-price-type-btn']"
        self.execution_status_xpath = "//div/div[@class='ag-center-cols-container']/div"
        self.hyperlink_runs_screen = "//span[text()='Runs']"
        self.get_list_of_overview_screen_stage_count = "(//div[@col-id='overview'])[2]/child::span/child::span"


    # restatement
        self.run_status = "//div[@class='ag-center-cols-container']/div[@row-index='0']/div[@col-id='status']"
        self.restatement_btn = "//div[@class='btn-group']/button[@id='restate-price-type-btn']"
        self.reexecution_status = "//div[@row-index='0']/div[@col-id='status']"
        
    # Approvals Loactors
        self.Approval = "//span[@id='container']/span[4]"
        self.Finalization = "//span[@id='container']/span[5]"
        self.btn_execute_approval_tab = "//button[@tooltip='Execute']"
        self.btn_ok_approval_tab = "//div[contains(.,'Only Price Types in queued or analysis may be run')][@id='runtime-error-well']/parent::div/following-sibling::div/child::button"
        self.popup_error_msg = "//div[contains(.,'Only Price Types in queued or analysis may be run')][@id='runtime-error-well']"
        self.popup_error_manager_cannot_approve = "//div[contains(.,'Manager cannot perform both approvals.')]"
        self.btn_disable_from_approval_tab = "(//div[@col-id='enabled']/child::checkbox-renderer/child::input)[1]"
        self.txt_stage_disabled = "(//div[@col-id='stage'][text()='DISABLED']/following-sibling::div[text()='Disabled for this run'])[1]"
        self.popup_error_msg_overriden = "//div[contains(.,'Only Price Types in queued or analysis may be overridden')]"
        self.popup_error_msg_overriden_altered = "//div[contains(.,'Only Price Types in queued or analysis may have their overrides altered')]"


     #Analysis Locators
        self.Analysis = "//span[@id='container']/span[3]"
        self.column_enabled = "(//div[@col-id='enabled'])[2]"
        self.txt_column_bucket_row_first = "(//div[@col-id='reportable_name']/child::span[@class='ag-cell-wrapper']/descendant::span[@class='ag-cell-value'])[1]"
        self.get_list_of_price_type = "//div[@col-id='stage']"
        self.icon_pencil_for_filtered_item = "(//i[@class='fa fa-pencil'])[1]"
        self.txt_lastest_version_count = "(//div[@col-id='version'])[2]"

    #Aalysis Screen ---> Price type Settings
        self.txt_field_data_Start_date = "//label[text()='Data Start Date']"
        self.txt_field_data_End_date = "//label[text()='Data End Date']"
        self.txt_field_data_Effective_date = "//label[text()='Data Effective Date']"
        self.drp_list_of_options_for_version_field = (By.XPATH,"(//select[@id='price-type-version'])[1]")
        self.drp_select_latest_option = (By.XPATH,"(//select[@id='price-type-version'])[1]")
        self.btn_save_from_popup = "//button[contains(.,'Save')]"

     #Aalysis Screen ---> Detail Tab---> Lower Grid Options
        self.icon_close_panel = "//button[@title='Close Panel']"
        self.icon_new_tab = "//button[@title='New Tab']"
        self.icon_export = "(//button[@title='Export'])[2]"
     
     #Aalysis Screen ---> Detail Tab---> Lower Grid--->New Tab Options
        self.icon_export_new_tab = "//button[@title='Export']"

     #Finalization Tab
        self.btn_execute = "//button[@tooltip='Execute'][@disabled]"
        self.btn_mark_as_delivered = "//button[@title='Deliver'][@disabled]"
        self.btn_rollback = "//button[@title='Rollback'][@disabled]"
        self.btn_version_selection = "//div[@col-id='version']/child::template-renderer/child::div/child::button"
        self.btn_execute = "//button[@tooltip='Execute'][@disabled]"

                        
    def Select_price_type_name(self,Price_Type_Name):
        self.Price_Type_Name = Price_Type_Name
        mouse.click_on_element(self,"XPATH", self.Filter_Icon)
        allure.attach("User can click on filter icon : ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.Search_box,self.Price_Type_Name)
        allure.attach("User can filter the price type as : "+self.Price_Type_Name,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH",self.Price_type)
        self.main.screen_load_time('Run->Price Type->Summary Screen')
        allure.attach("User clicked on the price type : "+self.Price_Type_Name,attachment_type=allure.attachment_type.TEXT)

    # Summary tab
    def Click_on_Summary_tab(self):
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Summary_Tab,"Summaty Tab element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH", self.Summary_Tab)
        self.main.screen_load_time('Summary tab Screen')
        allure.attach("User click on summary tab : ",attachment_type=allure.attachment_type.TEXT)


    def Summary_buttons_Operation(self, Message):
        self.Message = Message
        mouse.click_on_element(self, "XPATH", self.Summay_Prior_Delivered_Btn)
        allure.attach("User can click on prior delivery button from summary tab: ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Summay_Prior_Close_Btn)
        allure.attach("User can click prior close button from summary tab: ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Summay_Attachments_btn)
        allure.attach("User can click attachment button from summary tab: ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH", self.Summay_Attachments_Add_Btn)
        allure.attach("User can click attachment add button from summary tab: ",attachment_type=allure.attachment_type.TEXT)
        file_up = self.driver.find_element_by_xpath(self.Summay_Choose_File)
        file_up.send_keys(os.getcwd() + "/GP/automation_test/uploadfiles/Data_Summary_Report.xlsm") 
        mouse.click_on_element(self, "XPATH", self.Summay_File_Upload_Btn)
        allure.attach("User can upload data summary file: "+str(os.getcwd() + "/GP/automation_test/uploadfiles/Data_Summary_Report.xlsm"),attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Summay_Attachments_close_Btn)
        allure.attach("User can click on close button from attachment: ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH", self.Summary_Comments_btn)
        allure.attach("User can click on summary comments button: ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Summary_Add_Note_btn)
        allure.attach("User can click on summary add note button: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Summary_Message_Txt_Box, self.Message)
        allure.attach("User can type message as : "+self.Message,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH", self.Summay_Save_Note_Btn)
        allure.attach("User can click on summary save note button : ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH", self.Summay_Cancel_Note_Btn)
        allure.attach("User can click on summary cancel note button : ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH", self.Summay_Run_Report_Btn)
        allure.attach("User can click on summary run report button : ",attachment_type=allure.attachment_type.TEXT)
        if (locators.element_is_displayed(self,"XPATH",self.msg_an_error_occuredon_output_tab))==True:
            assert False, "An error occured while generating report msg popup appears"
        else:
            MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Summay_Export_Btn,"Summary Export element not found on Webpage in given wait time.")
            mouse.click_on_element(self,"XPATH", self.Summay_Export_Btn)
            allure.attach("User can click on summary export button : ",attachment_type=allure.attachment_type.TEXT)
        
     # Detail tab
    def Click_on_Detail_tab(self):
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Detail_Tab,"Detail Tab element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH", self.Detail_Tab)
        self.main.screen_load_time('Run->Price Type->Detail Screen')
        allure.attach("User can click on details tab : ",attachment_type=allure.attachment_type.TEXT)
            
    def detail_tab_operation_foredit_and_delete(self, NDC9, Bucket_Name_Select, Message,edited_message):
        self.NDC9 = NDC9
        self.Bucket_Name_Select = Bucket_Name_Select
        self.Message = Message
        self.edited_message = edited_message
        forms.select_option_by_text(self, "XPATH", self.NDC9_DropDown, self.NDC9)
        allure.attach("User can select NDC9 as: "+self.NDC9,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Bucket_Filter_Icon)
        allure.attach("User can click on bucket filter icon: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Bucket_Search_Box, self.Bucket_Name_Select)
        allure.attach("User can enter text in filter container as: "+self.Bucket_Name_Select,attachment_type=allure.attachment_type.TEXT)
        mouse.click_action_on_element(self, "XPATH", self.Bucket_Check_Box)
        allure.attach("User can click the bucket checkbox :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Comment_Btn)
        allure.attach("User can click on comment button from details tab :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Add_Btn)
        allure.attach("User can click on add note button :",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Detail_Note_Text_Box, Message)
        allure.attach("User can add note as :"+Message,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Save_Btn)
        allure.attach("User can click on save button :",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Detail_Note_Text_Box, edited_message)
        allure.attach("User can edit note as :"+self.edited_message,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Save_Btn)
        allure.attach("User can click on save button :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.btn_delete_note_detail_tab)
        allure.attach("User can click on delete button :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_cancel_btn)
        allure.attach("User can click on cancel button :",attachment_type=allure.attachment_type.TEXT)

    def click_on_variance_button(self, Message):
        self.Message = Message
        mouse.click_on_element(self, "XPATH", self.Variance_Btn)
        allure.attach("User can click on variance button :",attachment_type=allure.attachment_type.TEXT)
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
            # self.login.close_browser()
        except AttributeError:
            mouse.click_on_element(self, "XPATH", self.V_Cancel_btn)
            mouse.click_action_on_element(self, "XPATH", self.V_Export)
        
     # bucket tab
    def select_bucket_tab(self):
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.bucket_tab,"Bucket Tab element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.bucket_tab)
        self.main.screen_load_time('Run->Price Type->Bucket Screen')
        allure.attach("User can click on bucket tab :",attachment_type=allure.attachment_type.TEXT)
    
    def switch_between_buckets(self):
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"DirectSales")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Direct Sales')
        allure.attach("User can switch to bucket : DirectSales",attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"Chargebacks")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Chargeback')
        allure.attach("User can switch to bucket : Chargeback",attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"Rebates")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Rebates')
        allure.attach("User can switch to bucket : Rebates",attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"Tricare")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Tricare')
        allure.attach("User can switch to bucket : Tricare",attachment_type=allure.attachment_type.TEXT)


    def confirm_bucket_export(self):
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"DirectSales")
        self.main.screen_load_time('Run->Price Type->Summary tab->Direct Sales')
        # MainPage.wait_until_element_is_present(self,60,By.XPATH,self.t_id_wait,"t_id element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.bucket_export) 
        self.main.screen_load_time('Run->Price Type->Summary tab->Direct Sales->Export')
        allure.attach("User can click on export button: ",attachment_type=allure.attachment_type.TEXT)

    def confirm_bucket_filter_sort(self):
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"DirectSales")
        MainPage.wait_until_element_is_present(self,60,By.XPATH,self.t_id_wait,"t_id element not found on Webpage in given wait time.")
        self.tid_list = []
        self.tid_list = self.driver.find_elements_by_xpath(self.t_ids)
        self.list_length =len(self.tid_list)
        self.list_tid=[]
        for i in range(self.list_length,0,-1):
            self.tid = "(//div[@role='row']/div[@col-id='tid'])["+str(i)+"]"   
            self.column_text = forms.get_text_on_element(self, "XPATH", self.tid)
            self.list_tid.append(self.column_text)  
        logger.info(self.list_tid)
        sorted_elements = [self.list_tid[index] >= self.list_tid[index+1] for index in range(len(self.list_tid)-1)]
        is_sorted = all(sorted_elements)
        if is_sorted == True:
            logger.info("Yes, List is sorted.")
        else:
            logger.info("No, List is not sorted.")
    
    # override
    def select_override_tab(self):
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.bucket_tab,"Bucket Tab element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.override_tab)
        self.main.screen_load_time('Run->Price Type->Override Screen')
        allure.attach("User can click on override tab: ",attachment_type=allure.attachment_type.TEXT)

    def override_details(self,dollars,units,min_value,note,NDC11,period_month):
        self.sheet_dollars = dollars
        self.sheet_units = units
        self.sheet_min_value = min_value
        self.sheet_note = note
        self.NDC11 = NDC11
        self.period_month = period_month
        mouse.click_on_element(self,"XPATH",self.new_override_btn)
        allure.attach("User can click on new override button:",attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_index(self,"XPATH",self.override_name,0)
        allure.attach("User can select new override name :",attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self,"XPATH",self.ndc11,self.NDC11)
        allure.attach("User can select NDC11:"+self.NDC11,attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self,"XPATH",self.override_period,self.period_month)
        allure.attach("User can select period:"+self.period_month,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.dollar,self.sheet_dollars)
        allure.attach("User can enter dollars as :"+self.sheet_dollars,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.units,self.sheet_units)
        allure.attach("User can enter Units as :"+self.sheet_units,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.min_value,self.sheet_min_value)
        allure.attach("User can enter Min value as :"+self.sheet_min_value,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.note,self.sheet_note)
        allure.attach("User can enter sheet note as :"+self.sheet_note,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Edit Override details")
        mouse.click_on_element(self,"XPATH",self.override_submit)
        allure.attach("User click on submitt button :",attachment_type=allure.attachment_type.TEXT)

    
    def select_override_and_click_on_edit_override(self,Edit_Override_Name,Edit_Override_ndc,Edit_Override_period):
        self.edit_override_name = Edit_Override_Name 
        self.edit_override_ndc = Edit_Override_ndc
        self.edit_override_period = Edit_Override_period
        mouse.click_on_element(self,"XPATH",self.filter_icon)
        allure.attach("User click on filter icon :",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.edit_override_name)
        allure.attach("User can enter filter name as :"+self.edit_override_name,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH",self.ndc_filter)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.edit_override_ndc)
        mouse.click_on_element(self,"XPATH",self.period_filter)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.edit_override_period)
        mouse.click_on_element(self,"XPATH",self.component)
        mouse.click_on_element(self,"XPATH",self.edit_override_btn)
        generics.capture_screenshot_allure(self.main, "Edit Override details")
        allure.attach("User can click on edit override button :",attachment_type=allure.attachment_type.TEXT)

            
    def edit_override_details(self,dollars,units,min_value,note):
        self.sheet_dollars = dollars
        self.sheet_units = units
        self.sheet_min_value = min_value
        self.sheet_note = note
        forms.select_option_by_index(self,"XPATH",self.override_name,0)
        allure.attach("User can edit override name :",attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_index(self,"XPATH",self.ndc11,0)
        forms.select_option_by_index(self,"XPATH",self.override_period,0)
        forms.enter_text_on_element(self,"XPATH",self.dollar,self.sheet_dollars)
        forms.enter_text_on_element(self,"XPATH",self.units,self.sheet_units)
        forms.enter_text_on_element(self,"XPATH",self.min_value,self.sheet_min_value)
        forms.enter_text_on_element(self,"XPATH",self.note,self.sheet_note)
        allure.attach("User can edit override note :"+self.sheet_note,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Edit Override details")
        mouse.click_on_element(self,"XPATH",self.override_submit)
    
    def select_override_and_click_on_delete(self,Delete_Override_Name,Delete_Override_ndc,Delete_Override_period):
        self.delete_override_name = Delete_Override_Name 
        self.delete_override_ndc = Delete_Override_ndc
        self.delete_override_period = Delete_Override_period
        mouse.click_on_element(self,"XPATH",self.filter_icon)
        allure.attach("User can click on filter icon to delete override:",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.delete_override_name)
        allure.attach("User can enter override name in filter to delete override:"+self.delete_override_name,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH",self.ndc_filter)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.delete_override_ndc)
        mouse.click_on_element(self,"XPATH",self.period_filter)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.delete_override_period)
        mouse.click_on_element(self,"XPATH",self.component)
        generics.capture_screenshot_allure(self.main, "Delate Override Details")
        mouse.click_on_element(self,"XPATH",self.delete_override_btn)
        
    def summary_asks_to_re_execute(self,price_type):
        self.re_execution_status = "Re-execution Required"
        self.price_type = price_type
        mouse.click_on_element(self, "XPATH", self.result_ready)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.re_execution_status)
        self.checkbox_exist = self.driver.find_element_by_xpath(self.checkbox)  
        assert self.checkbox_exist.is_enabled() == True
        mouse.click_on_element(self, "XPATH", self.run_filter_icon)
        forms.enter_text_on_element(self, "XPATH", self.search_box, self.price_type)  
        self.re_execution = forms.get_text_on_element(self,"XPATH",self.reexecution_status)
        assert self.re_execution == self.re_execution_status
        
    def click_on_Approve_btn(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Summary_Approve_Btn,"Summary tab Approve Button element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.Summary_Approve_Btn)
        allure.attach("User can click on approve button to submitt the price type: ",attachment_type=allure.attachment_type.TEXT)
        
    def click_on_Rollback_btn(self):
        mouse.click_on_element(self, "XPATH", self.Summary_Rollback_Btn) 
        self.main.screen_load_time('Rollback')
        allure.attach("User can click on rollback button : ",attachment_type=allure.attachment_type.TEXT)

    def click_on_Approval_tab(self):
        # time.sleep(3)
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Approval,"Approval Button element not found on Webpage in given wait time.")
        ApprovalScreen = self.driver.find_element_by_xpath(self.Approval)
        self.driver.execute_script("$(arguments[0]).click();", ApprovalScreen)
        self.main.screen_load_time('Approval Screen')
        allure.attach("User can click on approval tab : ",attachment_type=allure.attachment_type.TEXT)

              
    def click_on_Finalization_tab(self):
        # MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Finalization,"Finilization Button element not found on Webpage in given wait time.")
        FinalizationScreen = self.driver.find_element_by_xpath(self.Finalization)
        self.driver.execute_script("$(arguments[0]).click();", FinalizationScreen)
        # mouse.click_on_element(self, "XPATH", self.Finalization)
        self.main.screen_load_time('Finilization Screen')
        allure.attach("User can click on Finalization tab : ",attachment_type=allure.attachment_type.TEXT)

  
    def click_on_Delivered(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Finalization_Delivered,"Finilization Delevered button element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH", self.Finalization_Delivered)
        allure.attach("User can click on Mark as delivered : ",attachment_type=allure.attachment_type.TEXT)

    def get_splitted_file_for_downloades_for_summary_tab(self,file_list):
        self.file_list =file_list
        self.exported_file = self.file_list[0]
        self.exported_file_Split = self.exported_file.split("/")
        self.exported_file_name = self.exported_file_Split[4]
        self.run_report_file = self.file_list[1]
        self.run_report_file_Split = self.run_report_file.split("/")
        self.run_report_file_name = self.run_report_file_Split[4]
        allure.attach("User can see exported file as : "+str(self.exported_file_name),attachment_type=allure.attachment_type.TEXT)
        allure.attach("User can see run report file as : "+str(self.run_report_file_name),attachment_type=allure.attachment_type.TEXT)
        
    def get_splitted_file_for_downloades_for_tab(self,file_list):
        self.file_list =file_list
        self.exported_file = self.file_list[0]
        self.exported_file_Split = self.exported_file.split("/")
        self.exported_file_name = self.exported_file_Split[4]
        allure.attach("User can see exported file as : "+str(self.exported_file_name),attachment_type=allure.attachment_type.TEXT)
        
    def verify_comments_for_detail_tab(self, NDC9, Bucket_Name_Select, Message):
        self.NDC9 = NDC9
        self.Bucket_Name_Select = Bucket_Name_Select
        self.Message = Message
        forms.select_option_by_text(self, "XPATH", self.NDC9_DropDown, self.NDC9)
        allure.attach("User can select NDC9 as: "+self.NDC9,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Bucket_Filter_Icon)
        allure.attach("User can click on bucket filter icon: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Bucket_Search_Box, self.Bucket_Name_Select)
        allure.attach("User can enter text in filter container as: "+self.Bucket_Name_Select,attachment_type=allure.attachment_type.TEXT)
        mouse.click_action_on_element(self, "XPATH", self.Bucket_Check_Box)
        allure.attach("User can click the bucket checkbox :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Comment_Btn)
        allure.attach("User can click on comment button from details tab :",attachment_type=allure.attachment_type.TEXT)
        self.txtarea_msg_note = "//textarea[@type='text']"
        self.get_txt = forms.get_input_text(self,"XPATH",self.txtarea_msg_note)
        if self.get_txt == self.Message:
            allure.attach("User can verify note added as : "+self.get_txt,attachment_type=allure.attachment_type.TEXT)
            mouse.click_on_element(self, "XPATH", self.Detail_Note_cancel_btn)
            allure.attach("User can click on cancel button :",attachment_type=allure.attachment_type.TEXT)

    def click_on_export_button_on_override_tab(self):
        mouse.click_on_element(self, "XPATH", self.btn_Export_override_tab)
        allure.attach("User can click on export button from override tab :",attachment_type=allure.attachment_type.TEXT)

    def verify_stage(self,stage,index):
        self.index = index
        self.stage = stage
        self.stage_verify = "(//div[@col-id='stage'][text()='"+self.stage+"'])["+str(self.index)+"]"
        locators.element_is_displayed(self,"XPATH",self.stage_verify)
        allure.attach("User can see stage as : "+self.stage,attachment_type=allure.attachment_type.TEXT)

    def verify_submitted_by_column(self,submitted_by,index):
        self.index = index
        self.submitted_by = submitted_by
        self.submitted_by_verify = "(//div[@col-id='ASB'][text()='"+self.submitted_by+"'])["+str(self.index)+"]"
        locators.element_is_displayed(self,"XPATH",self.submitted_by_verify)
        allure.attach("User can submitted by as : "+self.submitted_by,attachment_type=allure.attachment_type.TEXT)

    def verify_submitted_on_column(self,system_current_date,index):
        self.index = index
        self.system_current_date = system_current_date
        self.submitted_on_for_data_summary = "(//div[@col-id='ASO'])["+str(self.index)+"]"
        mouse.click_action_on_element(self, "XPATH", self.column_enabled)
        mouse.scroll_to_right_using_send_keyboard_keys(self,5)
        self.get_application_submitted_date = forms.get_text_on_element(self,"XPATH",self.submitted_on_for_data_summary)
        if self.get_application_submitted_date == self.system_current_date:
            allure.attach("User can  see submitted on date same for system and application : "+self.system_current_date,attachment_type=allure.attachment_type.TEXT)
            self.driver.refresh()
            self.main.screen_load_time('Approval Screen')
        else:
            assert False,"System date and application date is not same"

    def get_current_system_date(self,date_format):
        self.date_format = date_format
        self.system_current_date = MainPage.get_system_current_date(self,self.date_format)
        allure.attach("User can see current system date as : "+self.system_current_date,attachment_type=allure.attachment_type.TEXT)
        return self.system_current_date
    
    def click_on_Analysis_tab(self):
        AnalysisScreen = self.driver.find_element_by_xpath(self.Analysis)
        self.driver.execute_script("$(arguments[0]).click();", AnalysisScreen)
        self.main.screen_load_time('Analysis Screen')
        allure.attach("User can click on analysis tab : ",attachment_type=allure.attachment_type.TEXT)

    def verify_rollback_by_column(self,rollback_by,index):
        self.index = index
        self.rollback_by = rollback_by
        self.rollback_by_verify = "(//div[@col-id='rollbackedBy.name'][text()='"+self.rollback_by+"'])["+str(self.index)+"]"
        mouse.click_action_on_element(self, "XPATH", self.column_enabled)
        mouse.scroll_to_right_using_send_keyboard_keys(self,10)
        locators.element_is_displayed(self,"XPATH",self.rollback_by_verify)
        allure.attach("User can see rollback by as : "+self.rollback_by,attachment_type=allure.attachment_type.TEXT)

    def verify_rollback_on_column(self,system_current_date,index):
        self.index = index
        self.system_current_date = system_current_date
        self.rollback_on = "(//div[@col-id='rollbacked_on'])["+str(self.index)+"]"
        self.get_application_rollback_date = forms.get_text_on_element(self,"XPATH", self.rollback_on)
        if self.get_application_rollback_date == self.system_current_date:
            allure.attach("User can  see rollback on date same for system and application : "+self.system_current_date,attachment_type=allure.attachment_type.TEXT)
        else:
            assert False,"System date and application date is not same"
    
    def verify_approved_by_column(self,approved_by,index):
        self.index = index
        self.approved_by = approved_by
        self.approved_by_verify = "(//div[@col-id='AB'][text()='"+self.approved_by+"'])["+str(self.index)+"]"
        mouse.click_action_on_element(self, "XPATH", self.column_enabled)
        mouse.scroll_to_right_using_send_keyboard_keys(self,8)
        locators.element_is_displayed(self,"XPATH",self.approved_by_verify)
        allure.attach("User can see approved by as : "+self.approved_by,attachment_type=allure.attachment_type.TEXT)

    def verify_approved_on_column(self,system_current_date,index):
        self.index = index
        self.system_current_date = system_current_date
        self.approved_on = "(//div[@col-id='AO'])["+str(self.index)+"]"
        self.get_application_approved_on_date = forms.get_text_on_element(self,"XPATH", self.approved_on)
        if self.get_application_approved_on_date == self.system_current_date:
            allure.attach("User can see  approved on date same for system and application : "+self.system_current_date,attachment_type=allure.attachment_type.TEXT)
        else:
            assert False,"System date and application date is not same"

    def verify_data_present_for_any_of_the_bucket_sources(self):
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"DirectSales")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Direct Sales')
        if (locators.element_is_displayed(self,"XPATH",self.bucket_source_first_row_data))== True:
            allure.attach("Data is present for direct sales bucket source : ",attachment_type=allure.attachment_type.TEXT)
            return "DirectSales"
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"Chargebacks")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Chargeback')
        if (locators.element_is_displayed(self,"XPATH",self.bucket_source_first_row_data))== True:
            allure.attach("Data is present for Chargeback bucket source : ",attachment_type=allure.attachment_type.TEXT)
            return "Chargebacks"
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"Rebates")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Rebates')
        if (locators.element_is_displayed(self,"XPATH",self.bucket_source_first_row_data))== True:
            allure.attach("Data is present for Rebates bucket source : ",attachment_type=allure.attachment_type.TEXT)
            return "Rebates"
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,"Tricare")
        self.main.screen_load_time('Run->Price Type->Bucket tab->Tricare')
        if (locators.element_is_displayed(self,"XPATH",self.bucket_source_first_row_data))== True:
            allure.attach("Data is present for Tricare bucket source : ",attachment_type=allure.attachment_type.TEXT)
            return "Tricare"
        else:
            assert False,"Data is not present for buckets tab for any source. Please select another run or another client"
        
    def select_bucket_data_source(self,bucket_data_source_name):
        self.bucket_data_source_name = bucket_data_source_name
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,self.bucket_data_source_name)
        self.main.screen_load_time('Run->Price Type->Bucket tab->'+self.bucket_data_source_name)
        allure.attach("Bucket data source selected is  : "+self.bucket_data_source_name,attachment_type=allure.attachment_type.TEXT)

    def verify_exclude_functionality(self,column_name_tid,message):
        self.message = message
        self.column_name_tid = column_name_tid
        self.get_tid_on_bucket_tab = forms.get_text_on_element(self, "XPATH", self.bucket_source_first_row_data)
        MainPage.click_on_any_filter_icon(self,self.column_name_tid)
        MainPage.enter_text_on_any_filter_icon_search_box(self,self.get_tid_on_bucket_tab)
        self.get_exclude_column_status = forms.get_text_on_element(self, "XPATH", self.bucket_source_first_row_exclude_status)
        mouse.click_on_element(self,"XPATH",self.bucket_source_filtered_data)
        allure.attach("Click on the tid to add note  : ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Add_Btn)
        allure.attach("User can click on add note button :",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Detail_Note_Text_Box, self.message)
        allure.attach("User can add note as :"+self.message,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Bucket_chkbox)
        allure.attach("User clicks on checkbox :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Save_Btn)
        allure.attach("User can click on save button :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_cancel_btn)
        allure.attach("User clicks on cancel button :"+self.message,attachment_type=allure.attachment_type.TEXT)
        self.exclude_column_status = forms.get_text_on_element(self, "XPATH", self.bucket_source_first_row_exclude_status)
        if self.exclude_column_status == "Y":
            allure.attach("The tid is been excluded :"+self.get_tid_on_bucket_tab,attachment_type=allure.attachment_type.TEXT)

    def verify_include_functionality(self,column_name_tid,message):
        self.message = message
        self.column_name_tid = column_name_tid
        self.get_tid_on_bucket_tab = forms.get_text_on_element(self, "XPATH", self.bucket_source_first_row_data)
        MainPage.click_on_any_filter_icon(self,self.column_name_tid)
        MainPage.enter_text_on_any_filter_icon_search_box(self,self.get_tid_on_bucket_tab)
        self.get_exclude_column_status = forms.get_text_on_element(self, "XPATH", self.bucket_source_first_row_exclude_status)
        mouse.click_on_element(self,"XPATH",self.bucket_source_first_row_data)
        allure.attach("Click on the tid to add note  : ",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Add_Btn)
        allure.attach("User can click on add note button :",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Bucket_Note_Text_Box, self.message)
        allure.attach("User can add note as :"+self.message,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Bucket_chkbox)
        allure.attach("User clicks on checkbox :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Bucket_Note_Save_Btn)
        allure.attach("User can click on save button :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_cancel_btn)
        allure.attach("User clicks on cancel button :"+self.message,attachment_type=allure.attachment_type.TEXT)
        self.exclude_column_status = forms.get_text_on_element(self, "XPATH", self.bucket_source_first_row_exclude_status)
        if self.exclude_column_status == "N":
            allure.attach("The tid is been included :"+self.get_tid_on_bucket_tab,attachment_type=allure.attachment_type.TEXT)

    def verify_delivered_by_column(self,delivered_by,index):
        self.index = index
        self.delivered_by = delivered_by
        self.delivered_by_verify = "(//div[@col-id='DB'][text()='"+self.delivered_by+"'])["+str(self.index)+"]"
        mouse.click_action_on_element(self, "XPATH", self.column_enabled)
        mouse.scroll_to_right_using_send_keyboard_keys(self,8)
        locators.element_is_displayed(self,"XPATH",self.delivered_by_verify)
        allure.attach("User can see delivered by as : "+self.delivered_by,attachment_type=allure.attachment_type.TEXT)

    def verify_delivered_on_column(self,system_current_date,index):
        self.index = index
        self.system_current_date = system_current_date
        self.delivered_on = "(//div[@col-id='DO'])["+str(self.index)+"]"
        self.get_application_delivered_date = forms.get_text_on_element(self,"XPATH",self.delivered_on)
        if self.get_application_delivered_date == self.system_current_date:
            allure.attach("User can  see delivered on date same for system and application : "+self.system_current_date,attachment_type=allure.attachment_type.TEXT)
            self.driver.refresh()
            self.main.screen_load_time('Finilization Screen')
        else:
            assert False,"System date and application date is not same"

    def click_on_first_bucket_element(self):
        mouse.click_action_on_element(self, "XPATH", self.txt_column_bucket_row_first)
        allure.attach("User can click on first row of bucket column: ",attachment_type=allure.attachment_type.TEXT)

    def verify_lower_grid_options(self):
        locators.element_is_displayed(self,"XPATH",self.icon_close_panel)
        allure.attach("User can see close panel icon in lower grid: ",attachment_type=allure.attachment_type.TEXT)
        locators.element_is_displayed(self,"XPATH",self.icon_new_tab)
        allure.attach("User can see new tab icon in lower grid : ",attachment_type=allure.attachment_type.TEXT)
        locators.element_is_displayed(self,"XPATH",self.icon_export)
        allure.attach("User can see export icon  in lower grid: ",attachment_type=allure.attachment_type.TEXT)

    def click_on_close_panel_from_lower_grid(self):
        mouse.click_action_on_element(self, "XPATH", self.icon_close_panel)
        allure.attach("User can click on close panel from lower grid: ",attachment_type=allure.attachment_type.TEXT)

    def filter_bucket_name_on_detail_tab(self, NDC9, Bucket_Name_Select):
        self.NDC9 = NDC9
        self.Bucket_Name_Select = Bucket_Name_Select
        forms.select_option_by_text(self, "XPATH", self.NDC9_DropDown, self.NDC9)
        allure.attach("User can select NDC9 as: "+self.NDC9,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Bucket_Filter_Icon)
        allure.attach("User can click on bucket filter icon: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Bucket_Search_Box, self.Bucket_Name_Select)
        allure.attach("User can enter text in filter container as: "+self.Bucket_Name_Select,attachment_type=allure.attachment_type.TEXT)
    
    def click_on_export_button_on_lower_grid(self):
        self.main.screen_load_time('Run->Price Type->Summary Screen->Detail Tab')
        mouse.click_on_element(self, "XPATH", self.icon_export)
        allure.attach("User can click on export button on from lower grid: ",attachment_type=allure.attachment_type.TEXT)

    def click_on_new_tab_button_on_lower_grid(self):
        mouse.click_action_on_element(self, "XPATH", self.icon_new_tab)
        allure.attach("User can click on new tab button on from lower grid: ",attachment_type=allure.attachment_type.TEXT)

    def switch_to_child_tab(self):
        switch_windows_tabs.switch_to_child_window(self)
        self.main.screen_load_time('Run Screen')
        allure.attach("User can switch to child tab: ",attachment_type=allure.attachment_type.TEXT)

    def verify_new_tab_options(self):
        locators.element_is_displayed(self,"XPATH",self.icon_export_new_tab)
        allure.attach("User can see export icon new tab : ",attachment_type=allure.attachment_type.TEXT)
    
    def click_on_export_button_on_new_tab_options(self):
        mouse.click_action_on_element(self,"XPATH",self.icon_export_new_tab)
        allure.attach("User can click on export button on new tab : ",attachment_type=allure.attachment_type.TEXT)
    
    def get_splitted_file_for_downloades_for_lower_grid(self,file_list):
        self.file_list =file_list
        self.exported_file_Split = self.file_list.split("/")
        self.exported_file_name = self.exported_file_Split[4]
        allure.attach("User can see exported file as : "+str(self.exported_file_name),attachment_type=allure.attachment_type.TEXT)
    
    def select_on_any_bucket(self,bucket_name):
        self.bucket_name = bucket_name
        forms.select_option_by_text(self,"XPATH",self.bucket_dropdown,self.bucket_name)
        self.main.screen_load_time('Run->Price Type->Bucket tab->'+self.bucket_name+'')
        allure.attach("User can switch to bucket: " +self.bucket_name,attachment_type=allure.attachment_type.TEXT)

    def click_on_request_ndc9_report_button(self):
        mouse.click_action_on_element(self,"XPATH",self.btn_request_ndc9_report)
        allure.attach("User can click on request ndc9 report button on detail tab : ",attachment_type=allure.attachment_type.TEXT)

    def select_any_source(self,source_name):
        self.source_name = source_name
        forms.select_option_by_text(self,"XPATH",self.drp_source_ndc9_buckets,self.source_name)
        allure.attach("User can select source: " +self.source_name,attachment_type=allure.attachment_type.TEXT)

    def click_on_ndc9_dropdown(self):
        mouse.click_action_on_element(self,"XPATH",self.drp_click_ndc9)
        allure.attach("User can click on ndc9 dropdown: ",attachment_type=allure.attachment_type.TEXT)

    def click_on_ndc9_from_list(self,NDC9):
        self.NDC9 = NDC9
        self.chkbox_ndc9 = "//li[@class='multiselect-item-checkbox']/child::div[text()='"+self.NDC9+"']"
        mouse.click_action_on_element(self,"XPATH",self.chkbox_ndc9)
        allure.attach("User can click on ndc9 checkbox: "+self.NDC9,attachment_type=allure.attachment_type.TEXT)

    def click_on_submit_button(self):
        mouse.click_action_on_element(self,"XPATH",self.btn_submit_ndc9_buckets_popup)
        allure.attach("User can click on submit button: ",attachment_type=allure.attachment_type.TEXT)

    def click_on_attachments_button(self):
        mouse.click_on_element(self, "XPATH", self.Summay_Attachments_btn)
        allure.attach("User can click attachment button from summary tab: ",attachment_type=allure.attachment_type.TEXT)

    def verify_report_in_attachments_popup(self,NDC9,price_type_name):
        self.NDC9 = NDC9
        self.price_type_name = price_type_name
        self.bln_flag_for_NDC = False
        self.int_count=0
        self.report_name = "//td[text()='Bucketed DS Transactions for "+self.NDC9+"']"
        while self.bln_flag_for_NDC==False:
            if(locators.element_is_displayed(self,"XPATH",self.report_name)):
                allure.attach("User can see report as : "+"Bucketed Transactions for "+self.NDC9+"",attachment_type=allure.attachment_type.TEXT)
                mouse.click_on_element(self, "XPATH", self.Summay_Attachments_close_Btn)
                allure.attach("User can click on close button from attachment: ",attachment_type=allure.attachment_type.TEXT)
                self.bln_flag_for_NDC = True
                break
            else:
                self.driver.refresh()
                self.Select_price_type_name(self.price_type_name)
                self.click_on_attachments_button()
                self.bln_flag_for_NDC = False
            self.int_count = self.int_count+1
            if self.int_count > 25:
                break

    def click_on_export_button_on_bucket_tab(self):
        mouse.click_on_element(self, "XPATH", self.bucket_export)
        allure.attach("User can click on export button on bucket tab: ",attachment_type=allure.attachment_type.TEXT)

    def verify_red_triangle_on_override_tab(self):
        locators.element_is_displayed(self,"XPATH",self.icon_red_triangle)
        allure.attach("User can see the red triangle in override tab: ",attachment_type=allure.attachment_type.TEXT)

    def get_ndc11_from_override_tab(self):
        self.ndc11_column_text = forms.get_text_on_element(self, "XPATH", self.txt_get_ndc11_column_override_tab)
        allure.attach("User can get NDC11 from override tab as: "+self.ndc11_column_text,attachment_type=allure.attachment_type.TEXT)
        return self.ndc11_column_text

    def verify_dollar_and_unit_amount_on_summary_tab(self,unit_amount,dollar_amount):
        self.unit_amount = unit_amount
        self.dollar_amount = dollar_amount
        self.txt_dollar_and_unit_Amount = "(//div[@col-id = 'ndc11']/following-sibling::div[@col-id='ramp_dollars'][contains(.,'"+self.dollar_amount+"')]/following-sibling::div[text()='"+self.unit_amount+"'])[1]"
        locators.element_is_displayed(self,"XPATH",self.txt_dollar_and_unit_Amount)
        allure.attach("User can see dollar and unit amount in summary tab: "+self.dollar_amount +" "+self.unit_amount,attachment_type=allure.attachment_type.TEXT)

    def verify_red_triangle_on_override_tab_is_removed(self):
        if (locators.element_is_displayed(self,"XPATH",self.icon_red_triangle)):
            pass
        else:
            allure.attach("User can see the red triangle in override tab is removed: ",attachment_type=allure.attachment_type.TEXT)

    def verify_count_on_override_tab_is_removed(self):
        if (locators.element_is_displayed(self,"XPATH",self.txt_count_on_override_tab)):
            pass
        else:
            allure.attach("User can see the count from override tab is removed: ",attachment_type=allure.attachment_type.TEXT)

    def detail_tab_operation(self, NDC9, Bucket_Name_Select, Message):
        self.NDC9 = NDC9
        self.Bucket_Name_Select = Bucket_Name_Select
        self.Message = Message
        forms.select_option_by_text(self, "XPATH", self.NDC9_DropDown, self.NDC9)
        allure.attach("User can select NDC9 as: "+self.NDC9,attachment_type=allure.attachment_type.TEXT)
        locators.element_is_displayed(self,"XPATH",self.txt_data_detail_tab_first_row)
        allure.attach("User can see data as per selection on detail tab: "+self.NDC9,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Detail Tab After Selection of NDC,Period Month")
        mouse.click_on_element(self, "XPATH", self.Bucket_Filter_Icon)
        allure.attach("User can click on bucket filter icon: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Bucket_Search_Box, self.Bucket_Name_Select)
        allure.attach("User can enter text in filter container as: "+self.Bucket_Name_Select,attachment_type=allure.attachment_type.TEXT)
        mouse.click_action_on_element(self, "XPATH", self.Bucket_Check_Box)
        allure.attach("User can click the bucket checkbox :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Comment_Btn)
        allure.attach("User can click on comment button from details tab :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Add_Btn)
        allure.attach("User can click on add note button :",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Detail_Note_Text_Box, Message)
        allure.attach("User can add note as :"+Message,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_Save_Btn)
        allure.attach("User can click on save button :",attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.Detail_Note_cancel_btn)
        allure.attach("User can click on cancel button :",attachment_type=allure.attachment_type.TEXT)

    def click_on_execute_button_from_approval_tab(self):
        mouse.click_on_element(self, "XPATH", self.btn_execute_approval_tab)
        allure.attach("User can click on execute button :",attachment_type=allure.attachment_type.TEXT)

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

    def verify_error_message_popup_displayed(self):
        if (locators.element_is_displayed(self,"XPATH",self.popup_error_msg)):
            allure.attach("Only Price Types in queued or analysis may be run is displayed: ",attachment_type=allure.attachment_type.TEXT)
            mouse.click_on_element(self, "XPATH", self.btn_ok_approval_tab)
            self.driver.refresh()
        else:
            assert False , "Only Price Types in queued or analysis may be run is not displayed"

    def verify_error_message_manager_cannot_approve(self):
        if (locators.element_is_displayed(self,"XPATH",self.popup_error_manager_cannot_approve)):
            allure.attach("Manager cannot perform both approvals popup is displayed: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Manager cannot perform both approvals is not displayed"

    def click_on_disable_enable_button_from_approval_tab(self):
        mouse.click_on_element(self, "XPATH", self.btn_disable_from_approval_tab)
        allure.attach("User can click on enable/disable button :",attachment_type=allure.attachment_type.TEXT)

    def verify_stage_as_disabled_and_status_As_disabled_for_run(self):
        if (locators.element_is_displayed(self,"XPATH",self.txt_stage_disabled)):
            allure.attach("Stage is disabled and status is disabled for this run for price type: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Stage is disabled and status is disabled for this run is not displayed"

    def filter_price_type_name(self,Price_Type_Name):
        self.Price_Type_Name = Price_Type_Name
        mouse.click_on_element(self,"XPATH", self.Filter_Icon)
        allure.attach("User can click on filter icon : ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH",self.Search_box,self.Price_Type_Name)
        allure.attach("User can filter the price type as : "+self.Price_Type_Name,attachment_type=allure.attachment_type.TEXT)

    def verify_error_message_popup_on_override_tab_displayed(self):
        if (locators.element_is_displayed(self,"XPATH",self.popup_error_msg_overriden)):
            allure.attach("Only Price Types in queued or analysis may be overridden is displayed: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Only Price Types in queued or analysis may be overridden is not displayed"

    def verify_error_message_popup_on_override_tab_altered_displayed(self):
        if (locators.element_is_displayed(self,"XPATH",self.popup_error_msg_overriden_altered)):
            allure.attach("Only Price Types in queued or analysis may have their overrides altered is displayed: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Only Price Types in queued or analysis may have their overrides altered is not displayed"

    def verify_execute_button_is_disabled_in_finalization_tab(self):
        if (locators.element_is_displayed(self,"XPATH",self.btn_execute)):
            allure.attach("Execute button is disabled in finalization tab ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Execute button is not disabled in finalization tab"

    def verify_mark_as_delivered_and_rollback_is_disabled_in_finalization_tab(self):
        locators.element_is_displayed(self,"XPATH",self.btn_mark_as_delivered)
        allure.attach("Mark as delivered button is disabled in finalization tab ",attachment_type=allure.attachment_type.TEXT)
        locators.element_is_displayed(self,"XPATH",self.btn_rollback)
        allure.attach("Rollback button is disabled in finalization tab ",attachment_type=allure.attachment_type.TEXT)

    def get_analysis_stage_price_type_stage_count_at_initial(self,pending_approved_delivered_stage):
        self.driver.refresh()
        time.sleep(5)
        self.pending_approved_delivered_stage = pending_approved_delivered_stage
        self.get_list_count_of_price_type = self.driver.find_elements_by_xpath(self.get_list_of_price_type)
        self.list_length_of_price_type =len(self.get_list_count_of_price_type)+1
        allure.attach("Price type List length is : "+str(self.list_length_of_price_type),attachment_type=allure.attachment_type.TEXT)
        self.list_of_stage_count_dict = {}
        self.existing_count = 1
        self.new_dict_of_stages_inside_run = {}
        self.zero_count = 0
        for i in range(2,self.list_length_of_price_type):
            self.price_type_stage_status = "(//div[@col-id='stage'])["+str(i)+"]"
            self.get_stage_type = forms.get_text_on_element(self, "XPATH", self.price_type_stage_status)
            if self.get_stage_type in self.list_of_stage_count_dict:
                self.new_count = self.existing_count+1
                self.list_of_stage_count_dict[self.get_stage_type] = self.new_count
            elif self.get_stage_type not in  self.list_of_stage_count_dict:
                self.list_of_stage_count_dict.update([(self.get_stage_type,self.existing_count)])
        self.new_dict_of_stages_inside_run.update(self.list_of_stage_count_dict)
        self.new_dict_of_stages_inside_run[self.pending_approved_delivered_stage[0]] = self.zero_count
        self.new_dict_of_stages_inside_run[self.pending_approved_delivered_stage[1]] = self.zero_count
        self.new_dict_of_stages_inside_run[self.pending_approved_delivered_stage[2]] = self.zero_count
        allure.attach("Inside Run Stage count Dictionary : "+str(self.new_dict_of_stages_inside_run),attachment_type=allure.attachment_type.TEXT)
        return self.new_dict_of_stages_inside_run

    def click_on_runs_hyperlink(self):
        mouse.click_on_element(self, "XPATH", self.hyperlink_runs_screen)
        allure.attach("User can click on runs screen :",attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time('Run Screen')

    def get_overview_screen_stage_count_at_initial(self,queued_analysis_pending_approved_delivered_stage):
        self.queued_analysis_pending_approved_delivered_stage = queued_analysis_pending_approved_delivered_stage
        self.list_of_stage_count_dict_on_overview = {}
        self.get_list_count_of_overview_screen_stage = self.driver.find_elements_by_xpath(self.get_list_of_overview_screen_stage_count)
        self.list_length_of_overview =len(self.get_list_count_of_overview_screen_stage)
        allure.attach("Overview Stage List Length Is : "+str(self.list_length_of_overview),attachment_type=allure.attachment_type.TEXT)
        for i in range(0,self.list_length_of_overview):
            self.get_overview_stage_count = "((//div[@col-id='overview'])[2]/child::span/child::span)["+str(i+1)+"]"
            self.get_stage_count = forms.get_text_on_element(self, "XPATH", self.get_overview_stage_count)
            self.list_of_stage_count_dict_on_overview[self.queued_analysis_pending_approved_delivered_stage[i]] = self.get_stage_count
        allure.attach("Overview Screen Stage Count Dictionary : "+str(self.list_of_stage_count_dict_on_overview),attachment_type=allure.attachment_type.TEXT)
        return self.list_of_stage_count_dict_on_overview

    def get_analysis_stage_price_type_stage_count_when_data_summary_sent_for_approval(self):
        self.driver.refresh()
        time.sleep(5)
        self.get_list_count_of_price_type = self.driver.find_elements_by_xpath(self.get_list_of_price_type)
        self.list_length_of_price_type =len(self.get_list_count_of_price_type)+1
        allure.attach("Price type List length is : "+str(self.list_length_of_price_type),attachment_type=allure.attachment_type.TEXT)
        self.list_of_stage_count_dict = {}
        self.existing_count = 1
        self.new_dict_of_stages_inside_run = {}
        self.zero_count = 0
        for i in range(2,self.list_length_of_price_type):
            self.price_type_stage_status = "(//div[@col-id='stage'])["+str(i)+"]"
            self.get_stage_type = forms.get_text_on_element(self, "XPATH", self.price_type_stage_status)
            if self.get_stage_type in self.list_of_stage_count_dict:
                self.new_count = self.existing_count+1
                self.list_of_stage_count_dict[self.get_stage_type] = self.new_count
            elif self.get_stage_type not in  self.list_of_stage_count_dict:
                self.list_of_stage_count_dict.update([(self.get_stage_type,self.existing_count)])
        self.new_dict_of_stages_inside_run.update(self.list_of_stage_count_dict)
        allure.attach("Analysis Stage : "+str(self.new_dict_of_stages_inside_run),attachment_type=allure.attachment_type.TEXT)
        return self.new_dict_of_stages_inside_run
    

    def get_approval_stage_price_type_stage_count_when_data_summary_sent_for_approval(self):
        self.driver.refresh()
        time.sleep(5)
        self.get_list_count_of_price_type = self.driver.find_elements_by_xpath(self.get_list_of_price_type)
        self.list_length_of_price_type =len(self.get_list_count_of_price_type)+1
        allure.attach("Price type List length is : "+str(self.list_length_of_price_type),attachment_type=allure.attachment_type.TEXT)
        self.list_of_stage_count_dict = {}
        self.existing_count = 1
        self.new_dict_of_stages_inside_run = {}
        self.zero_count = 0
        for i in range(2,self.list_length_of_price_type):
            self.price_type_stage_status = "(//div[@col-id='stage'])["+str(i)+"]"
            self.get_stage_type = forms.get_text_on_element(self, "XPATH", self.price_type_stage_status)
            if self.get_stage_type in self.list_of_stage_count_dict:
                self.new_count = self.existing_count+1
                self.list_of_stage_count_dict[self.get_stage_type] = self.new_count
            elif self.get_stage_type not in  self.list_of_stage_count_dict:
                self.list_of_stage_count_dict.update([(self.get_stage_type,self.existing_count)])
        self.new_dict_of_stages_inside_run.update(self.list_of_stage_count_dict)
        allure.attach("Approval Stage : "+str(self.new_dict_of_stages_inside_run),attachment_type=allure.attachment_type.TEXT)
        return self.new_dict_of_stages_inside_run
    
    def click_on_pencil_icon_for_any_filtered_item(self):
        locators.element_is_displayed(self,"XPATH",self.icon_pencil_for_filtered_item)
        allure.attach("User can see pencil icon for assessmenet run: ",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Pencil Icon For Assessment Run")
        mouse.click_on_element(self, "XPATH", self.icon_pencil_for_filtered_item)
        self.main.screen_load_time('Run->Price Type->Analysis Screen')
        allure.attach("User can click on pencil icon :",attachment_type=allure.attachment_type.TEXT)
      
    def verify_price_type_Settings_popup_with_all_headers_renamed(self):
        if (locators.element_is_displayed(self,"XPATH",self.txt_field_data_Start_date)):
            allure.attach("Start Date Is renamed as Data Start Date on popup: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Start Date Is not renamed as Data Start Date on popup"
        if (locators.element_is_displayed(self,"XPATH",self.txt_field_data_End_date)):
            allure.attach("End Date Is renamed as Data End Date: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "End Date Is not renamed as Data End Date on popup"
        if (locators.element_is_displayed(self,"XPATH",self.txt_field_data_Effective_date)):
            allure.attach("Effective Date Is renamed as Data Effective Date: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert False , "Effective Date Is not renamed as Data Effective Date on popup"

    def get_latest_version_count(self):
        self.get_text_version_count = forms.get_text_on_element(self, "XPATH", self.txt_lastest_version_count)
        allure.attach("User can get latest version count : "+self.get_text_version_count,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Versions')
        return self.get_text_version_count

    def verify_versions_list_of_price_type_with_dropdown_values(self,version_no):
        self.version_no = version_no
        self.list_of_dropdown_values = []
        self.list_of_dropdown_values = forms_rfn.get_all_no_blank_options(self,self.drp_list_of_options_for_version_field)
        allure.attach("User can get list of version as  : "+str(self.list_of_dropdown_values),attachment_type=allure.attachment_type.TEXT)
        if self.version_no in self.list_of_dropdown_values[0]:
            allure.attach("Price type editor version list is same as dropdown version list  : "+str(self.list_of_dropdown_values),attachment_type=allure.attachment_type.TEXT)

    def select_latest_dropdown_version_and_click_on_save_button(self):
        forms_rfn.select_option_by_index(self,self.drp_select_latest_option,0)
        allure.attach("User can see selected version as  : ",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Latst Versions')
        mouse.click_on_element(self, "XPATH", self.btn_save_from_popup)
        self.main.screen_load_time('Run->Price Type->Analysis Screen')
        allure.attach("User can click on save button :",attachment_type=allure.attachment_type.TEXT)
      
    def verify_versions_and_execution_in_approved_and_finalized_stage_is_not_possible(self):
        if (locators.check_element_not_displayed(self,"XPATH",self.btn_version_selection)):
            allure.attach("Version change is not possible in stage: ",attachment_type=allure.attachment_type.TEXT)
            generics.capture_screenshot_allure(self.main, 'Version Change Not Possible')
        if (locators.check_element_not_displayed(self,"XPATH",self.btn_execute)):
            allure.attach("Execution not possible in stage: ",attachment_type=allure.attachment_type.TEXT)
            generics.capture_screenshot_allure(self.main, 'Execution Change Not Possible')