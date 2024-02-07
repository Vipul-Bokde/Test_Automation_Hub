from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators, forms_rfn
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import os
import time
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from selenium import webdriver
from selenium.webdriver.common.by import By
from GP.pages.login_page import Login
from libraries import generics
from GP.pages.client_joins_page import NewJoinPage
from Common.pages.products_page import GPProductsPage


class FileTemplatePage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        self.upload_file = NewJoinPage(self.driver)
        self.products_page = GPProductsPage(self.driver)

        # locators
        self.overview_upload_button = "//button[normalize-space()='Upload']"
        self.select_file_type = "//select[@id='file-type-select']"
        self.upload_file_chooser = "//input[@id='upload-file-chooser']"
        self.upload_submit_btn = "//button[@id='upload-submit-btn']"
        self.manage_test_files = "//button[normalize-space()='Manage Test File']"
        self.download_file = "//a[normalize-space()='Download File']"
        self.download_template = "//a[normalize-space()='Download Template']"
        self.re_apply_template = "//a[normalize-space()='Re-apply Template']"
        self.file_template_status = "//span[normalize-space()='{}']"
        self.open_file_template = "//div[normalize-space()='{}']"
        self.sbmt_for_approval = "//button[@id='btn-save-record']"
        self.del_draft_btn = "//button[@id='draft-delete-btn']"
        self.new_field = "//button[normalize-space()='New Field']"
        self.manage_test_files = "//button[normalize-space()='Manage Test File']"
        self.advanced = "//button[normalize-space()='Advanced']"
        self.history = "//button[normalize-space()='History']"
        self.history_column_headers = "//span[normalize-space()='{}']"
        self.new_field_name = "//input[@formcontrolname = 'name']"
        self.new_field_value = "//input[@formcontrolname = 'value']"
        self.field_sbmt_btn = "//button[@id='field-submit-btn']"
        self.created_field = "//div[contains(text(),'{}')]"
        self.del_created_field = "//div[contains(text(),'{}')]/following-sibling::div[@class='deleteLabel']"
        self.manage_tf_upload_option = "//template-designer//li[1]"
        self.manage_tf_download_file_option = "//template-designer//li[2]"
        self.manage_tf_download_temp_option = "//template-designer//li[3]"
        self.manage_tf_re_apply_temp_option = "//template-designer//li[4]"
        self.advanced_file_format = "//select[@formcontrolname='file_format']"
        self.advanced_header = "//select[@formcontrolname='includes_header']"
        self.edit_custom_logic = "//button[@id='custom-logic']"
        self.logic_cancel_btn = "//button[@id='logic-cancel-btn']"
        self.use_custom_logic = "//input[@formcontrolname='use_custom_logic']"
        self.extract_customer = "//input[@formcontrolname='extract_customers']"
        self.file_excluder = "//input[@formcontrolname='file_excluder']"
        self.header_row = "//input[@formcontrolname='header_row']"
        self.adv_submt_btn = "//button[@id='template-submit-btn']"
        self.adv_cancel_btn = "//button[@id='template-cancel-btn']"
        self.horizontal_scroll_element = "//div[@id='grid-container']//div[@class='ag-body-horizontal-scroll-viewport']"
        self.sbmt_approval_note = "//textarea[@id='approval-note']"
        self.sbmt_approval_btn = "//button[@class='btn submit-btn btn-primary']"
        self.validate_advanced_field = "//button[contains(normalize-space(),'{}')]"
        self.edit_record_button = "(//button[normalize-space()='Edit Record'])[1]"
        self.modified_by_name = "(//div[@col-id='0' and text()])[{}]"
        self.modified_on_date = "(//div[@col-id='modified_on' and text()])[{}]"
        self.version = "(//div[@col-id='version' and text()])[{}]"
        self.comment_note = "(//div[@tabindex and @col-id='note']/span)[{}]"
        self.history_rows = "(//div[@class='ag-center-cols-container'])[3]/div"

    def select_gp_filetemp_submenu_from_global_menu(self):
        time.sleep(2)
        self.main.select_gp_option('GLOBAL', sub_item='FILE TEMPLATE')

    """Author: Vipul Bokde
       Description: This method upload file template file and validate its status 
       in GP File Template Screen
       Arguments: File to upload 
       Returns:NA """

    def upload_file_temp_and_validate_status(self, file_type, file_to_upload_path, IconName, uploaded_file_name):
        self.IconName = IconName
        self.IconText = uploaded_file_name
        self.file_type = file_type
        self.file_to_upload_path = file_to_upload_path
        time.sleep(5)
        self.element_exist = locators.element_exists(self, "XPATH", self.overview_upload_button)
        if self.element_exist == True:
            mouse.click_on_element(self, "XPATH", self.overview_upload_button)
        else:
            logger.info("Upload option does not exist on overview screen")
            self.login = Login(self.driver)
            self.login.close_browser()
            exit(0)
        forms_rfn.select_option_by_texts(
            self, (By.XPATH, self.select_file_type), self.file_type)
        self.upload_file.upload_file(self.file_to_upload_path)
        mouse.click_on_element(self, "XPATH", self.upload_submit_btn)
        time.sleep(5)
        self.select_gp_filetemp_submenu_from_global_menu()
        self.products_page.click_and_enter_text_on_filter_icons(self.IconName, self.IconText)
        expected_file_template_status = "DRAFT"
        actual_status = forms.get_text_on_element(
            self, "XPATH", self.file_template_status.format(expected_file_template_status))
        if actual_status == expected_file_template_status:
            allure.attach(f"Uploaded File template status showing '{actual_status}' is present on the page",
                          attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method validates file tenplate option in a file template screen
       Arguments: NA 
       Returns:NA """

    def validate_template_screen_buttons(self, uploaded_file_name):
        self.file_name = uploaded_file_name
        elements_to_validate = [
            self.sbmt_for_approval,
            self.del_draft_btn,
            self.new_field,
            self.manage_test_files,
            self.advanced,
            self.history
        ]
        mouse.click_on_element(self, "XPATH", self.open_file_template.format(self.file_name))
        time.sleep(2)
        for element_locator in elements_to_validate:
            button_name = forms.get_text_on_element(self, "XPATH", element_locator)
            allure.attach(f"File template screen showing '{button_name}' button on the page",
                          attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method add new fields and validates newly created field
       Arguments: NA 
       Returns:NA """

    def validate_new_field_screen_elements(self, field_name, field_value):
        self.field_name = field_name
        self.field_value = field_value
        time.sleep(2)
        mouse.click_on_element(self, "XPATH", self.new_field)
        forms.enter_text_on_element(self, "XPATH", self.new_field_name, self.field_name)
        forms.enter_text_on_element(self, "XPATH", self.new_field_value, self.field_value)
        mouse.click_on_element(self, "XPATH", self.field_sbmt_btn)
        time.sleep(2)
        self.scroll_horizontally(self.horizontal_scroll_element, 2800)
        self.validate_element(self.created_field.format(self.field_name))
        allure.attach(f"Successfully created new field '{self.field_name}' in the template screen",
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method delete newly created field
       Arguments: NA 
       Returns:NA """

    def delete_added_fields_using_x_icon(self, field_name):
        del_element_field = self.del_created_field.format(field_name)
        self.scroll_horizontally(self.horizontal_scroll_element, 2800)
        if locators.element_exists(self, "XPATH", del_element_field):
            mouse.click_on_element(self, "XPATH", del_element_field)
            time.sleep(2)
            if locators.element_exists(self, "XPATH", del_element_field):
                raise Exception(f"field '{field_name}' was not deleted.")
            else:
                allure.attach(f"field '{field_name}' was deleted successfully and not found in template columns",
                              attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach(f"field '{field_name}' was not found in the first place, so no deletion was performed.",
                          attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method verify if x icon for deletion is available or not 
       for pending and active status
       Arguments: NA 
       Returns:NA """

    def verify_x_icon_availability(self, IconName, IconText, field_name, expected_status):
        self.products_page.click_and_enter_text_on_filter_icons(IconName, IconText)
        template_status = forms.get_text_on_element(
            self, "XPATH", self.file_template_status.format(expected_status))
        if template_status in ["ACTIVE", "PENDING"]:
            mouse.click_on_element(self, "XPATH", self.open_file_template.format(IconText))
            self.scroll_horizontally(self.horizontal_scroll_element, 2800)
            time.sleep(2)
            element_locator = self.del_created_field.format(field_name)
            if not locators.element_exists(self, "XPATH", element_locator):
                allure.attach(f"'X' icon is not available for '{field_name}' in {template_status} status.",
                              attachment_type=allure.attachment_type.TEXT)
            else:
                raise Exception(
                    f"'X' icon is available for '{field_name}' in {template_status} template.")
        else:
            allure.attach(f"Not validating 'X' icon because the template status is not in Active or Pending status.",
                          attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method verify manage test files elements 
       Arguments: NA 
       Returns:NA """

    def validate_manage_test_file_elements(self, IconName, IconText):
        mouse.click_on_element(self, "XPATH", self.manage_test_files)
        elements_to_validate = [
            self.manage_tf_upload_option,
            self.manage_tf_download_file_option,
            self.manage_tf_download_temp_option,
            self.manage_tf_re_apply_temp_option,
        ]
        for element_locator in elements_to_validate:
            option_name = forms.get_text_on_element(self, "XPATH", element_locator)
            allure.attach(f"File template screen showing '{option_name}' button on the page",
                          attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method verify advanced functionality elements 
       Arguments: NA 
       Returns:NA """

    def validate_advanced_fields_elements(self, file_format, header):
        mouse.click_on_element(self, "XPATH", self.advanced)
        forms_rfn.select_option_by_texts(self, (By.XPATH, self.advanced_file_format), file_format)
        forms_rfn.select_option_by_texts(self, (By.XPATH, self.advanced_header), header)
        mouse.click_on_element(self, "XPATH", self.edit_custom_logic)
        mouse.click_on_element(self, "XPATH", self.logic_cancel_btn)
        mouse.click_on_element(self, "XPATH", self.use_custom_logic)
        mouse.click_on_element(self, "XPATH", self.adv_submt_btn)
        self.validate_element(self.validate_advanced_field.format(file_format))
        allure.attach(f"Successfully Validated Advanced field {file_format}' button present on the page",
                      attachment_type=allure.attachment_type.TEXT)

    def validate_submit_for_approval(self, IconText):
        mouse.click_on_element(self, "XPATH", self.sbmt_for_approval)
        forms.enter_text_on_element(self, "XPATH", self.sbmt_approval_note, IconText)
        mouse.click_on_element(self, "XPATH", self.sbmt_approval_btn)

    def validate_history_section_elements(self, IconName, IconText):
        self.navigate_to_file_template(IconName, IconText)
        mouse.click_on_element(self, "XPATH", self.history)
        time.sleep(5)
        no_history_rows = locators.locator_elements(self, "XPATH", self.history_rows)
        for index, no_history_rows in enumerate(no_history_rows, start=1):
            modified_by = forms.get_text_on_element(
                self, "XPATH", self.modified_by_name.format(index))
            modified_date = forms.get_text_on_element(
                self, "XPATH", self.modified_on_date.format(index))
            version_value = forms.get_text_on_element(self, "XPATH", self.version.format(index))
            comment = forms.get_text_on_element(self, "XPATH", self.comment_note.format(index))
            allure.attach(f"History Row {index} - Modified By: {modified_by}, Modified On: {modified_date}, Version: {version_value}, Comment/Note: {comment}",
                          attachment_type=allure.attachment_type.TEXT)
        logger.info("Successfully Captured info. of template history")


    # GP FILE TEMPLATE RELATED REUSABLE METHODS DEFINED HERE TO CALL WHENEVER REQUIRED

    def validate_element(self, locator):
        time.sleep(2)
        element_exists = locators.element_exists(self, "XPATH", locator)
        if element_exists:
            self.highlight_element(locator)
        else:
            raise Exception(f"Element not found for locator: {locator}")

    def highlight_element(self, locator):
        try:
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].style.border = '3px solid red'", element)
            time.sleep(2)
        except NoSuchElementException:
            raise Exception(f"Element not found for locator: {locator}")

    def navigate_to_file_template(self, IconName, IconText):
        self.select_gp_filetemp_submenu_from_global_menu()
        self.products_page.click_and_enter_text_on_filter_icons(IconName, IconText)
        mouse.click_on_element(self, "XPATH", self.open_file_template.format(IconText))
        time.sleep(2)

    def scroll_horizontally(self, element_locator, scroll_amount):
        horizontal_scroll_element = self.driver.find_element(By.XPATH, element_locator)
        self.driver.execute_script(
            f"arguments[0].scrollLeft = {scroll_amount};", horizontal_scroll_element)
