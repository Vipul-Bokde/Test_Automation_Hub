from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login
import GP.utilities.Repo as Repo
from GP.pages.main_page import MainPage
from libraries import generics
from GP.pages.global_file_template_page import FileTemplatePage
from GP.pages.global_new_mapping_page import NewMappingPage
from GP.pages.approvals_page import ApprovalsPage

class FileTemplate(EnvironmentSetup):

    @given(u'I upload file template using overview screen and validate its status')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.login = Login(self.driver)
        logger.info("Uploaded new file template using overview screen")
        self.file_type = self.td_set['File_Type']
        self.IconName = self.td_set['IconName']
        self.file_to_upload = self.td_set['File To Upload']
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.file_to_upload_path = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_to_upload))
        self.file_temp_page.upload_file_temp_and_validate_status(
            self.file_type, self.file_to_upload_path, self.IconName, self.uploaded_file_name)
        logger.info("Sucessfully validated the status of uploaded file template")

    @given(u'I validate file template screen buttons')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.file_temp_page.validate_template_screen_buttons(self.uploaded_file_name)
        logger.info("Successfully validated the options available in template screen")

    @when(u'I validate new fields screen and perform deletion of added field')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.field_name = self.td_set['field_name']
        self.field_value = self.td_set['field_value']
        self.IconName = self.td_set['IconName']
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.file_temp_page.validate_new_field_screen_elements(self.field_name, self.field_value)
        self.file_temp_page.delete_added_fields_using_x_icon(self.field_name)
        logger.info("Successfully created, delted and validated new field in template screen")

    @when(u'I validate manage test files elements')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.IconName = self.td_set['IconName']
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.file_temp_page.validate_manage_test_file_elements(
            self.IconName, self.uploaded_file_name)
        logger.info("Successfully validated the options available in manage test files")

    @when(u'I validate and edit advanced option elements')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.file_format = self.td_set['file_format']
        self.header = self.td_set['header']
        self.file_temp_page.validate_advanced_fields_elements(self.file_format, self.header)
        logger.info("Sucessfully validated advanced option elements")

    @when(u'I click on submit for approval')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.file_temp_page.validate_submit_for_approval(self.uploaded_file_name)
        logger.info("Sucessfully submitted file template for approval")  

    @then(u'I validate X icon availability for active or pending status')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.IconName = self.td_set['IconName']
        self.field_name = self.td_set['field_name']
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.expected_status = self.td_set['expected_status']
        self.file_temp_page.select_gp_filetemp_submenu_from_global_menu()
        self.file_temp_page.verify_x_icon_availability(
            self.IconName, self.uploaded_file_name, self.field_name, self.expected_status)
        logger.info("Successfully validated x icon availability when status is pending and active")

    @then(u'Select template name for approval and approve')
    def step_impl(self):
        logger.info("Select given value and approve")
        self.New_Mapping = NewMappingPage(self.driver)
        self.template_name = self.td_set['FileTemplateName']
        self.New_Mapping.Approve_Template(self.template_name)
        self.Approvals = ApprovalsPage(self.driver)
        self.Approvals.click_on_approve_button()
    
    @then(u'I validate template history values')
    def step_impl(self):
        self.file_temp_page = FileTemplatePage(self.driver)
        self.IconName = self.td_set['IconName']
        self.uploaded_file_name = self.td_set['uploaded_file_name']
        self.file_temp_page.validate_history_section_elements(self.IconName, self.uploaded_file_name)
        logger.info("Successfully validated template history columns informations")