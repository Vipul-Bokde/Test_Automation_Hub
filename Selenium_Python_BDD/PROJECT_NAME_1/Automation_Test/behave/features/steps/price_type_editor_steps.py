from pydoc import locate
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.price_type_editor_page import PriceTypePage
import allure
from allure_commons.types import AttachmentType
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from GP.pages.approvals_page import ApprovalsPage
from libraries import generics

class PriceTypeEditor(EnvironmentSetup):

    @When(u'I select price type editor from burger menu')
    def step_impl(self):
        self.PriceType = PriceTypePage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for pricetypepage class in pricetypeeditor steps")
        self.PriceType.select_price_type_editor_from_burger_menu()
      
    # Create new price type
    @When(u'Create new price type')
    def step_impl(self):
        self.PriceType.click_on_new_price_button()
        self.Name = self.td_set['Price_Type']
        self.Price_type_category = self.td_set['Price_type_category']
        self.PriceType.add_price_type_name(self.Name)
        self.PriceType.select_price_type_category_from_dropdown(self.Price_type_category)
        self.PriceType.click_on_effective_start_date_input()
        self.effective_start_date = self.td_set['Effective Start Date_01']
        self.PriceType.select_date_from_calender(self.effective_start_date)
        self.PriceType.click_on_effective_end_date_input()
        self.effective_end_date = self.td_set['Effective End Date_01']
        self.PriceType.select_date_from_calender(self.effective_end_date)
        generics.capture_screenshot_allure(self.PriceType, 'New Price Type Created')

    @then(u'I click on the submit')
    def step_impl(self):
        status_var = self.PriceType.click_on_submit()
        if status_var == "Price Type Name is already in use":
            logger.info("Price Type Name is already in use please try with differnt name")
            allure.attach("Price Type Name is already in use please try with differnt name : ",attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info("Price Type Created")

    @then(u'Select a price type and approve')
    def step_impl(self):
        self.Approvals = ApprovalsPage(self.driver)
        self.login = Login(self.driver)
        self.Name = self.td_set['Price_Type']
        self.Approvals.select_price_type_name(self.Name,"GP Price Type",0,0)
        self.Approvals.click_on_approve_button_from_approvals()
        
# Open created price type

    @Then(u'Open the created price type')
    def step_impl(self):
        self.PriceType_Name = self.td_set['Price_Type']
        self.PriceType.select_added_price_type(self.PriceType_Name)
        logger.info("Opened the created price type")

# Import created price type
    @then(u'import the price type file')
    def step_impl(self):
        self.PriceType.click_on_hamburger_Menu()
        self.PriceType.click_on_import_button()
        self.file_To_Import = self.td_set['File Name To Import']
        self.PriceType.choose_file(self.file_To_Import)
        self.PriceType.click_on_upload_button()

# Update created price type
    @then(u'update the price type editor details')
    def step_impl(self):
        self.PriceType.click_reportable_flag()
        self.Filter_Col_Value_DS = self.td_set['Filter_Col_Value_DS']
        self.Filter_Col_Value_CBK = self.td_set['Filter_Col_Value_CBK']
        self.Dollar_Logic = self.td_set['Dollar_Logic']
        self.Unit_Logic = self.td_set['Unit_Logic']
        self.PriceType.update_bucket_filter(self.Filter_Col_Value_DS,self.Filter_Col_Value_CBK)
        self.PriceType.update_dollar_unit_logic(self.Dollar_Logic,self.Unit_Logic)
        self.Comment = self.td_set['Comment']
        self.PriceType.click_on_hamburger_Menu()
        self.PriceType.click_on_export_button_from_burger_menu()
        self.PriceType.click_onexecute_submit(self.Comment)

# Download the report template from Output tab and export
    # @When(u'Download the report template file')
    # def step_impl(self):
    #     self.PriceType.select_price_type_editor_from_burguer_menu()
    #     self.PriceType.select_added_price_type(self.Table_Name)
        
    @then(u'Click on output tab under the price type')
    def step_impl(self):
        self.PriceType.click_on_output_tab()
        # self.PriceType.click_on_output_tab_hamburger_button()    
    
    @then(u'Export the report template file')
    def step_impl(self):
        self.PriceType.click_on_export_button()
    
# Confirm revision history post approval of price type

    @then(u'Click on changes tab under the price type')
    def step_impl(self):
        self.PriceType.click_on_changes_tab()

    @Then(u'I verify uploaded file')
    def step_impl(self):
        self.hamburger_menu_uploads = self.td_set['Hamburger Menu Uploads']
        self.PriceType.wait_for_screen_to_load(self.hamburger_menu_uploads)
        self.filter_column_name_file_name = self.td_set['Filter Column Name']
        self.PriceType.click_on_any_filter_icon(self.filter_column_name_file_name)
        self.file_To_Import = self.td_set['File Name To Import']
        self.PriceType.enter_text_on_any_filter_icon_searchbox(self.file_To_Import)
        self.uploads_page = self.td_set['Screen Name']
        self.PriceType.click_on_uploads_page(self.uploads_page)
        self.file_To_Import = self.td_set['File Name To Import']
        self.PriceType.verify_file_is_uploaded(self.file_To_Import)

    @Then(u'I verify price type is created')
    def step_impl(self):
        self.PriceType.verify_price_type_created(self.Name)
    
    @Then(u'verify data is present for updated bucket')
    def step_impl(self):
        self.filter_column_name_outputtab_name = self.td_set['Filter Column Name OutputTab Name']
        self.PriceType.click_on_any_filter_icon(self.filter_column_name_outputtab_name)
        self.bucket_name = self.td_set['Bucket Name']
        self.PriceType.enter_text_on_any_filter_icon_searchbox(self.bucket_name)
        self.PriceType.click_on_column_name(self.filter_column_name_outputtab_name)
        self.PriceType.verify_bucket_is_displayed(self.bucket_name)

    @Then(u'Upload the report template file')
    def step_impl(self):
        self.PriceType.click_on_hamburger_menu_from_output_tab()
        self.file_template_to_upload = self.td_set['File Template To Upload']
        self.PriceType.choose_file_in_output_tab_for_template_upload(self.file_template_to_upload)

    @When(u'user add logic for bucket')
    def step_impl(self):
        self.PriceType.click_on_add_logic_button_from_logic_tab()
        self.type_dropdown_field_bucket = self.td_set['Type_Field_Bucket']
        self.PriceType.select_type_from_add_logic_popup_page(self.type_dropdown_field_bucket)
        self.PriceType.click_on_add_logic_text_from_add_logic_popup_page()
        self.PriceType.click_on_name_dropdown_from_add_logic_popup_page()
        self.name_dropdown_field_bucket = self.td_set['Name_Field_Bucket']
        self.PriceType.add_name_for_bucket_and_formula_logic(self.name_dropdown_field_bucket)
        self.PriceType.click_on_add_logic_text_from_add_logic_popup_page()
        self.source_dropdown_field_bucket = self.td_set['Bucket_Source']
        self.PriceType.click_source_dropdown_from_add_logic_popup_page(self.source_dropdown_field_bucket)
        self.PriceType.add_source_for_bucket_logic(self.source_dropdown_field_bucket)
        self.PriceType.click_on_add_logic_text_from_add_logic_popup_page()
        self.PriceType.click_submit_button_from_add_logic_popup_page()

    @When(u'user add logic for formula')
    def step_impl(self):
        self.PriceType.click_on_add_logic_button_from_logic_tab()
        self.type_dropdown_field_formula = self.td_set['Type_Field_Formula']
        self.PriceType.select_type_from_add_logic_popup_page(self.type_dropdown_field_formula)
        self.PriceType.click_on_add_logic_text_from_add_logic_popup_page()
        self.PriceType.click_on_name_dropdown_from_add_logic_popup_page()
        self.name_dropdown_field_formula = self.td_set['Name_Field_Formula']
        self.PriceType.add_name_for_bucket_and_formula_logic(self.name_dropdown_field_formula)
        self.PriceType.click_on_add_logic_text_from_add_logic_popup_page()
        self.PriceType.click_submit_button_from_add_logic_popup_page()

    @Then(u'user verify disable action for formula and bucket')
    def step_impl(self):
        self.name_dropdown_field_bucket = self.td_set['Name_Field_Bucket']
        self.PriceType.click_on_checkbox_from_logic_tab(self.name_dropdown_field_bucket)
        self.PriceType.click_on_action_button_from_logic_tab()
        self.btn_disable = self.td_set['Button_Name_Disable']
        self.PriceType.click_on_any_button_from_action_buttons_menu(self.btn_disable)
        self.disable_hexcode = self.td_set['Disable_HexCode']
        self.PriceType.verify_background_color_of_disabled_field_and_verify_field_disabled(self.name_dropdown_field_bucket,self.disable_hexcode )
        self.name_dropdown_field_formula = self.td_set['Name_Field_Formula']
        self.PriceType.click_on_checkbox_from_logic_tab(self.name_dropdown_field_formula)
        self.PriceType.click_on_action_button_from_logic_tab()
        self.PriceType.click_on_any_button_from_action_buttons_menu(self.btn_disable)
        self.PriceType.verify_background_color_of_disabled_field_and_verify_field_disabled(self.name_dropdown_field_formula,self.disable_hexcode)
    
    @Then(u'user verify enable action for formula and bucket')
    def step_impl(self):
        self.name_dropdown_field_bucket = self.td_set['Name_Field_Bucket']
        self.PriceType.click_on_checkbox_from_logic_tab(self.name_dropdown_field_bucket)
        self.PriceType.click_on_action_button_from_logic_tab()
        self.btn_enable = self.td_set['Button_Name_Enable']
        self.PriceType.click_on_any_button_from_action_buttons_menu(self.btn_enable)
        self.enable_hexcode = self.td_set['Enable_HexCode']
        self.PriceType.verify_background_color_of_enabled_field_and_verify_field_enabled(self.name_dropdown_field_bucket,self.enable_hexcode)
        self.name_dropdown_field_formula = self.td_set['Name_Field_Formula']
        self.PriceType.click_on_checkbox_from_logic_tab(self.name_dropdown_field_formula)
        self.PriceType.click_on_action_button_from_logic_tab()
        self.PriceType.click_on_any_button_from_action_buttons_menu(self.btn_enable)
        self.enable_hexcode_for_formula = self.td_set['Enable_HexCode_For_Formula']
        self.PriceType.verify_background_color_of_enabled_field_and_verify_field_enabled(self.name_dropdown_field_formula,self.enable_hexcode_for_formula)
    

    @When(u'user delete the formula and bucket')
    def step_impl(self):
        self.name_dropdown_field_bucket = self.td_set['Name_Field_Bucket']
        self.name_dropdown_field_formula = self.td_set['Name_Field_Formula']
        self.PriceType.click_on_checkbox_from_logic_tab(self.name_dropdown_field_bucket)
        self.PriceType.click_on_checkbox_from_logic_tab(self.name_dropdown_field_formula)
        self.PriceType.click_on_action_button_from_logic_tab()
        self.btn_delete = self.td_set['Button_Name_Delete']
        self.PriceType.click_on_any_button_from_action_buttons_menu(self.btn_delete)

    @Then(u'user verify undo and redo functionality')
    def step_impl(self):
        self.PriceType.click_on_undo_button()
        self.name_dropdown_field_bucket = self.td_set['Name_Field_Bucket']
        self.PriceType.verify_bucket_and_formula_is_displayed(self.name_dropdown_field_bucket)
        self.name_dropdown_field_formula = self.td_set['Name_Field_Formula']
        self.PriceType.verify_bucket_and_formula_is_displayed(self.name_dropdown_field_formula)
        self.PriceType.click_on_redo_button()
        
    @Then(u'user gets effective start and end date  and comment from changes tab')
    def step_impl(self):
        self.get_txt_effective_start_date=self.PriceType.get_effective_start_date()
        self.get_txt_effective_end_date=self.PriceType.get_effective_end_date()
        self.comment = self.td_set['Comment']
        self.version = self.td_set['Version']

    @Then(u'Download the report template file and click on run report button')
    def step_impl(self):
        self.PriceType.wait_for_min_time()
        self.PriceType.click_on_download_report_template()
        self.PriceType.click_on_run_report_button()

    @Then(u'Confirm the revision history')
    def step_impl(self):
        self.Modified_by = self.td_set['UserID']
        self.Approved_by = self.td_set['UserID_2']
        self.PriceType.confirm_history(self.Modified_by,self.Approved_by,self.comment,self.get_txt_effective_start_date,self.get_txt_effective_end_date,self.version)

    @When(u'I click on edit button')
    def step_impl(self):
        self.PriceType.click_on_edit_button_from_logic_tab()

    @Then(u'I verify price type is in edit mode with pencil icon')
    def step_impl(self):
        self.PriceType.verify_price_type_is_in_edit_mode_with_pencil_icon()

    @When(u'I get version 1 effective start date and end date')
    def step_impl(self):
        self.version_no = self.td_set['Version No 1']
        self.get_effective_start_date = self.PriceType.get_effective_start_date_of_any_version(self.version_no)
        self.get_effective_end_date = self.PriceType.get_effective_end_date_of_any_version(self.version_no)
        allure.attach("User can get effective start date for version 1: "+self.get_effective_start_date,attachment_type=allure.attachment_type.TEXT)
        allure.attach("User can get effective start end start for version 1: "+self.get_effective_end_date,attachment_type=allure.attachment_type.TEXT)


    @Then(u'I select effective start date and end date as end of time for version 2')
    def step_impl(self):
        self.PriceType.click_on_pencil_icon()
        self.PriceType.click_on_effective_start_date_input()
        self.effective_start_date = self.td_set['Effective Start Date_02_version']
        self.PriceType.select_date_from_calender(self.effective_start_date)
        self.PriceType.click_on_effective_end_date_input()
        self.effective_end_date = self.td_set['Effective End Date_02_Version']
        self.PriceType.select_date_from_calender(self.effective_end_date)
        generics.capture_screenshot_allure(self.PriceType, 'New Version Effective start and end date')

    @When(u'I submit the effective date changes')
    def step_impl(self):
        self.PriceType.click_on_save_button()

    @Then(u'I get version 2 effective start date and end date')
    def step_impl(self):
        self.PriceType.wait_for_min_time()
        self.version_no_2 = self.td_set['Version No 2']
        self.get_effective_start_date_version_2 = self.PriceType.get_effective_start_date_of_any_version_for_edit_mode(self.version_no_2)
        self.get_effective_end_date_version_2 = self.PriceType.get_effective_end_date_of_any_version(self.version_no_2)
        allure.attach("User can get effective start date for version 2: "+self.get_effective_start_date_version_2,attachment_type=allure.attachment_type.TEXT)
        allure.attach("User can get effective start end start for version 2: "+self.get_effective_end_date_version_2,attachment_type=allure.attachment_type.TEXT)

    @When(u'I click on logic tab')
    def step_impl(self):
        self.PriceType.click_on_logic_tab()

    @Then(u'I submit price type for approval')
    def step_impl(self):
        self.Comment = self.td_set['Comment']
        self.PriceType.click_on_submit_for_approval_button(self.Comment)

    @Then(u'I verify previous version effective end date is updated')
    def step_impl(self):
        self.version_no = self.td_set['Version No 1']
        self.calculated_effective_end_date_of_previous_version=self.PriceType.calculate_effective_end_date(self.get_effective_start_date_version_2,self.version_no)
        self.PriceType.verify_previous_version_effective_end_date_isupdated_to_oneday_minusof_nextversion_eff_startdate(self.calculated_effective_end_date_of_previous_version,self.version_no)
    
    @Then(u'I verify note column is updated')
    def step_impl(self):
        self.PriceType.verify_previous_version_note(self.calculated_effective_end_date_of_previous_version)
        
    @When(u'I click on revision history tab')
    def step_impl(self):
        self.PriceType.click_on_revision_history_tab()

    @Then(u'I verify modified on and modified by should also change')
    def step_impl(self):
        self.Modified_by = self.td_set['UserID']
        self.PriceType.confirm_history_for_version_1(self.Modified_by)

    @When(u'I get version 3 effective start date and end date')
    def step_impl(self):
        self.version_no_3 = self.td_set['Version No 3']
        self.get_effective_start_date_3 = self.PriceType.get_effective_start_date_of_any_version(self.version_no_3)
        self.get_effective_end_date_3 = self.PriceType.get_effective_end_date_of_any_version(self.version_no_3)
        allure.attach("User can get effective start date for version 3: "+self.get_effective_start_date_3,attachment_type=allure.attachment_type.TEXT)
        allure.attach("User can get effective start end start for version 3: "+self.get_effective_end_date_3,attachment_type=allure.attachment_type.TEXT)

    @Then(u'I select effective start date and keep effective end date as blank for version 3')
    def step_impl(self):
        self.PriceType.click_on_pencil_icon()
        self.PriceType.click_on_effective_start_date_input()
        self.effective_start_date = self.td_set['Effective Start Date_02_version']
        self.PriceType.select_date_from_calender(self.effective_start_date)
        self.PriceType.click_on_effective_end_date_input_cross_mark()
        generics.capture_screenshot_allure(self.PriceType, 'New version effective start date and end date kept blank')

    @Then(u'I verify version 2 and version 3 effective start and end date is same')
    def step_impl(self):
        if self.get_effective_start_date_version_2 == self.get_effective_start_date_3 and self.get_effective_end_date_version_2 == self.get_effective_end_date_3:
            allure.attach("User can see version 2 and 3 have same effective start date: "+self.get_effective_start_date_version_2+"  "+self.get_effective_start_date_3,attachment_type=allure.attachment_type.TEXT)
            allure.attach("User can see version 2 and 3 have same effective end date: "+self.get_effective_end_date_version_2+"  "+self.get_effective_end_date_3,attachment_type=allure.attachment_type.TEXT)

    @Then(u'I verify version 3 effective end date is updated to end of time')
    def step_impl(self):
        self.effective_end_date = self.td_set['Effective End Date_02_Version']
        self.converted_date = self.PriceType.convert_date_fromat(self.effective_end_date)
        if self.converted_date == self.get_effective_end_date_3:
            allure.attach("User can see version 3 has effective end date as end of time: "+self.get_effective_end_date_3,attachment_type=allure.attachment_type.TEXT)
