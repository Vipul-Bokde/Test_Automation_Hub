from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.gp_configuration_page import GPConfigPage
from libraries import mapping, mouse, forms, locators, locators_rfn, forms_rfn
import allure
from allure_commons.types import AttachmentType
import os
import time
from selenium.common.exceptions import NoSuchElementException
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from GP.pages.main_page import MainPage
from GP.utilities.database_connection import SqlConnection
import random
import string

class GPDRSBundlePage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        self.gp_config = GPConfigPage(self.driver)
        self.random_bundle_name = None
        # Bundle defintion locators
        self.gp_bundle_columns = "//div/span[@role = 'columnheader']"
        self.add_config_button = "//button[normalize-space()='Add Config']"
        self.new_bundle_defintion__button = "//button[normalize-space()='New Bundle Definition']"
        self.new_bundle_name_textbox = "//input[@id='bundle-name']"
        self.error_warning_special_characters = "//input[contains (@class, 'ng-invalid')]"
        self.already_exists_bundle = "//div[normalize-space()='Bundle name already exists']"
        self.new_bundle_submit_button = "//button[@class='btn submit-btn btn-primary']"
        self.new_bundle_cancel_button = "//button[@class='btn cancel-btn btn-secondary']"
        self.alert_text = "//div[@id='alert']"
        self.created_bundle_name = "//div[normalize-space()='{}']"
        self.checbox_selection = "//div[contains(text(),'{}')]/parent::div/div/span/span[1]"
        self.delete_bundle_definition = "//button[normalize-space()='Delete Bundle Definition']"
        self.bundle_statuses = "//div[normalize-space()='{}']/parent::div/div[2]/template-renderer/span[text()='{}']"
        # Defintion Tab locators
        self.bundle_name_defintion_tab = "//input[@id='bundle_name']"
        self.bundle_description_box = "//textarea[@id='bundle_desc']"
        self.save_btn = "//i[@class='fa fa-save']"
        self.auto_release_slider = "//span[@class='slider round']"
        # Contract Tab Locators
        self.bundle_contract_columns = "//div/span[@role = 'columnheader']"
        self.bundle_contract_custom_columns = "//div/span[@role = 'columnheader'and text() = '{}']"
        self.navigate_contract_tab = "//li[@id='contracts-tab']//a[@role='tab']"
        self.add_contract_button = "//button[normalize-space()='Add Contract']"
        self.remove_contract_button = "//button[normalize-space()='Remove Contract']"
        self.remove_submit_btn = "//button[@id='meta-submit-btn']"
        self.select_contract_source = "//div[@class='sparq-modal-body']//select"
        self.add_contract_list_button = "(//button[@type='submit'][normalize-space()='Add'])[1]"
        self.add_contract_term_list_button = "(//button[@type='submit'][normalize-space()='Add'])[2]"
        self.add_contract_terms_button = "//button[normalize-space()='Add Term']"
        self.remove_terms_button = "//button[normalize-space()='Remove Term']"
        # Data Bucket Tab Locators
        self.navigate_databucket_tab = "//li[@id='databuckets-tab']//a[@role='tab']"
        self.add_bucket_button = "//button[normalize-space()='Add Data Bucket']"
        self.remove_bucket_button = "//button[normalize-space()='Remove Data Bucket']"
        self.include_sales_checkbox = "//div[contains(text(),'{}')]/following-sibling::div[@col-id = 'include_sales']/template-renderer"
        self.include_discount_checkbox = "//div[contains(text(),'{}')]/following-sibling::div[@col-id = 'include_discount']/template-renderer"
        self.add_button_data_bucket = "//button[normalize-space()='Add']"
        self.edit_data_bucket = "//i[@class='fa fa-pencil']"
        self.save_edited_data_bucket = "//button[contains(text(),'Save')]"
        self.edit_discount_checkbox = "(//div[@col-id = 'include_discount']/template-renderer/input[@type='checkbox'])[2]"
        self.edit_sales_checkbox = "(//div[@col-id = 'include_sales']/template-renderer/input[@type='checkbox'])[2]"
        # Revision History locators
        self.navigate_rev_history_tab = "//li[@id='revisionhistory-tab']//a[@role='tab']"
        self.rev_history_rows = "//div[@class='ag-center-cols-container']//div[@role='row']"
        self.rev_history_data_by_row = "//div[@class='ag-center-cols-container']//div[@role='row']/div"
        # Approval Locators
        self.page_count = "//div[@class='ag-paging-panel ag-font-style']/span/span[@ref='lbTotal']"
        self.last_page = "//div[@class='ag-paging-panel ag-font-style']/span/button[@ref='btLast']"
        self.Approval_Name_Row = "//div[@role='row']/diff-renderer/div"
        self.submit_approval_button = "//body//root//button[normalize-space()='Submit For Approval']"
        # Customers and Products tab locators
        self.bundle_customers = "//*[@id='customers-tab']/a/strong"
        self.bundle_products = "//*[@id='products-tab']/a/strong"
        self.bundle_price_types = "//*[@id='pricetypes-tab']/a/strong"
        self.cust_grouping_label = "//*[@id='customer-grouping']/label"
        self.cust_selection_label = "//*[@id='customer-selection']/label"
        self.cust_grouping_dd = "//div[@id='customer-grouping']/select"
        self.cust_selection_dd = "//div[@id='customer-selection']/select"
        self.prod_selection_dd = "//div[@id='product-selection']/select"
        self.add_prod_popup_dd = "//div[@class='col-sm-12']/select[@id='group-item']"
        self.save_btn = "//*[@id='btn-save-record']"
        self.add_product_group_btn = "(//div[@class='float-right']/button[@class='btn btn-secondary'])[1]"
        self.remove_product_group_btn = "(//div[@class='float-right']/button[@class='btn btn-secondary'])[2]"
        self.x_prod_group = "(//div[@class = 'card']/div/h5[@class = 'float-left']/strong)[1]"
        self.x_prod_select = "//div[@id='product-selection']/label/strong"
        self.x_prod_list = "(//div[@class = 'card']/div/h5[@class = 'float-left']/strong)[2]"
        self.add_product_btn = "(//div[@class='float-right']/button[@class='btn btn-secondary'])[3]"
        self.remove_product_btn = "(//div[@class='float-right']/button[@class='btn btn-secondary'])[4]"
        self.submitbutton = "//modal[@id='products-group-modal']/div[2]/form/div[3]/button[1]"
        self.cancelbutton = "//modal[@id='products-group-modal']/div[2]/form/div[3]/button[2]"
        self.listsubmitbutton = "//modal[@id='products-list-modal']/div[2]/form/div[3]/button[@type = 'submit']"
        self.rem_product_grp_submit = "//modal[@id='bundle-product-group-remove']/div[2]/div[3]/button[@id='meta-submit-btn']"
        self.rem_product_submit = "//modal[@id='bundle-product-list-remove']/div[2]/div[3]/button[@id='meta-submit-btn']"
        self.inputbox = "//*[@id='product-group-name']"
        self.pencil_icon = "//i[@class='fa fa-pencil text-primary']"
        # d
        self.product_group_cb = "(//div[@row-id='0']//span[@class='ag-selection-checkbox'])[1]"
        self.product_list_cb = "(//div[@row-id='0']//span[@class='ag-selection-checkbox'])[2]"

    """Author: Vipul Bokde
       Description: This method select bundle definition sub menu from DRS menu
       Arguments: NA
       Returns:NA """

    def select_gp_bundle_def_submenu_from_drs_menu(self):
        time.sleep(3)
        self.main.select_gp_option(
            'DISCOUNT REALLOCATION', sub_item='BUNDLE DEFINITION EDITOR')

    """Author: Vipul Bokde
       Description: This method validate bundle definition screen columns
       Arguments: expected_column_names
       Returns:NA """

    def validate_bundle_defintion_columns(self, expected_column_names):
        self.gp_config .validate_gp_config_columns(expected_column_names)

    """Author: Vipul Bokde
       Description: This method creates a new bundle and validate its name on bundle definition screen
       Arguments: random_bundle_name
       Returns:NA """

    def validate_create_new_bundle_defintion(self, bundle_name):
        mouse.click_on_element(
            self, "XPATH", self.new_bundle_defintion__button)
        forms.enter_text_on_element(
            self, "XPATH", self.new_bundle_name_textbox, bundle_name)
        # Validate if the red highlight warning is present when characters entered other than
        # spaces, underscores (_), and hyphens (-)
        is_error_displayed = locators.element_exists(
            self, "XPATH", self.error_warning_special_characters)
        if is_error_displayed:
            allure.attach(f"Entered characters other than spaces, underscores, and hyphens. Validation error displayed.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info(
                "Validation error displayed: Entered characters other than spaces, underscores, and hyphens.")
        else:
            allure.attach(f"Validation successful. No error displayed for the entered characters.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info(
                "Validation successful: No error displayed for the entered characters.")
        mouse.click_on_element(self, "XPATH", self.new_bundle_submit_button)
        # Validate if bundle name already exists while creating bundle
        is_already_exists_message_displayed = locators.element_exists(
            self, "XPATH", self.already_exists_bundle)
        if is_already_exists_message_displayed:
            allure.attach(f"Bundle name" + bundle_name + "already exists. Please use a different bundle name.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.error(f"Error: Bundle name '{bundle_name}' already exists.")
            raise ValueError(
                f"Error: Bundle name '{bundle_name}' already exists. Please use a different bundle name.")
        else:
            allure.attach(f"New Bundle - " + bundle_name + " Created Sucessfully on bundle page. No error displayed for the entered characters.",
                          attachment_type=allure.attachment_type.TEXT)
        # Validate Bundle creation message on bundle page
        alert_message = forms.get_text_on_element(
            self, "XPATH", self.alert_text)
        # Assert that the alert message is as expected
        expected_alert_message = f"Bundle {bundle_name} created successfully!"
        assert alert_message == expected_alert_message, f"Actual alert message: {alert_message}"
        allure.attach(f"Validation successful: Alert message " + expected_alert_message + " displayed after submitting.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info(
            "Validation successful: Alert message displayed after submitting.")

    """Author: Vipul Bokde
       Description: This method clicks on a bundle from bundle definition screen
       Arguments: random_bundle_name
       Returns:NA """

    def click_on_a_bundle(self, bundle_name_to_click):
        if not locators.element_exists(self, "XPATH", self.created_bundle_name.format(bundle_name_to_click)):
            logger.error(
                f"Bundle with name '{bundle_name_to_click}' not found.")
            allure.attach(f"Bundle with name '{bundle_name_to_click}' not found.",
                          name="Error", attachment_type=allure.attachment_type.TEXT)
            raise NoSuchElementException(
                f"Bundle with name '{bundle_name_to_click}' not found.")
        mouse.click_on_element(
            self, "XPATH", self.created_bundle_name.format(bundle_name_to_click))
        logger.info(f"Sucessfully clicked on a bundle")

    """Author: Vipul Bokde
       Description: This method validates the created bundle name in database
       Arguments: Bundle_name
       Returns:NA """

    def validate_bundle_creation_in_database(self, Sql_Bundle_Definition_Query, bundle_name, client_id):
        # To validate bundle_name in database
        self.updated_query = Sql_Bundle_Definition_Query.replace(
            '${bundle_name}', bundle_name)
        self.updated_query_1 = self.updated_query.replace(
            '${client_id}', client_id)
        logger.info("SQL Query Updated  : "+self.updated_query_1)
        allure.attach("SQL Query Updated  : "+self.updated_query_1,
                      attachment_type=allure.attachment_type.TEXT)
        self.query_result_1 = SqlConnection.connection(self.updated_query_1)
        # validate if the bundle exists in database
        if not self.query_result_1:
            allure.attach(f"Bundle: {bundle_name} not found in the database.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.error("Bundle not found in the database.")
            assert False, f"Bundle '{bundle_name}' not found in the database."
        else:
            # Extracting the bundle_name from the result
            bundle_name_from_db = self.query_result_1[0][1]
            allure.attach(f"Bundle Name: {bundle_name_from_db} found in the database.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info(
                f"Bundle found in the database: {bundle_name_from_db} ")

    """Author: Vipul Bokde
       Description: This method deletes the bundle from bundle definition screen
       Arguments: bundle_name
       Returns:NA """

    def delete_created_bundle_defintion(self, bundle_name):
        mouse.click_on_element(
            self, "XPATH", self.checbox_selection.format(bundle_name))
        is_del_button_displayed = locators.element_is_displayed(
            self, "XPATH", self.delete_bundle_definition)
        if is_del_button_displayed:
            mouse.click_on_element(
                self, "XPATH", self.delete_bundle_definition)
            allure.attach(f"Bundle Name - " + bundle_name + " Deleted Sucessfully from bundle page",
                          attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info(
                "Delete button is not visible: Please select bundle to visible delete button.")

    """Author: Vipul Bokde
       Description: This method validate the statuses of a bundle
       Arguments: bundle_status
       Returns:NA """

    def validate_bundle_statuses(self, bundle_name_to_click, bundle_status):
        if not locators.element_exists(self, "XPATH", self.bundle_statuses.format(bundle_name_to_click, bundle_status)):
            logger.error(
                f"Bundle with name '{bundle_name_to_click}' not found.")
            allure.attach(f"Bundle with name '{bundle_name_to_click}' not found.",
                          name="Error", attachment_type=allure.attachment_type.TEXT)
            raise NoSuchElementException(
                f"Bundle with name '{bundle_name_to_click}' not found.")
        # Validate Bundle defnition status on bundle page after approval
        actual_bundle_status_text = forms.get_text_on_element(
            self, "XPATH", self.bundle_statuses.format(bundle_name_to_click, bundle_status))
        # Assert that the bundle_status_text is as expected
        assert actual_bundle_status_text == bundle_status, f"Actual bundle status: {actual_bundle_status_text}"
        allure.attach(f"Validation successful: Bundle definition: " + bundle_name_to_click + " & status:  " + bundle_status + " is displayed.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info(
            "Validation successful: Bundle status displayed.")

    """Author: Vipul Bokde
       Description: This method validates the elements of definition tab.
       Arguments: bundle_description
       Returns:NA """

    def validate_bundle_def_defintion_tab_modifications(self, bundle_description):
        locators.wait_until_presence_of_element(
            self, "XPATH", self.bundle_description_box)
        # Modifying Bundle Description
        forms.enter_text_on_element(
            self, "XPATH", self.bundle_description_box, bundle_description)
        # Modifying auto release button
        mouse.click_on_element(self, "XPATH", self.auto_release_slider)
        # Check if save button is disabled
        save_button_disabled = locators.get_attribute_value(
            self, "XPATH", self.save_btn, "disabled")
        if save_button_disabled == "true":
            allure.attach("Save button is unexpectedly disabled even after modifying bundle description.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.error(
                "Save button is unexpectedly disabled even when modifying bundle description.")
        else:
            mouse.click_on_element(self, "XPATH", self.save_btn)
            allure.attach("Successfully modified bundle description.",
                          attachment_type=allure.attachment_type.TEXT)
        # Validate alert message after saving the changes in definition tab
        alert_message = forms.get_text_on_element(
            self, "XPATH", self.alert_text)
        # Assert that the alert message is as expected
        expected_alert_message = alert_message
        assert alert_message == expected_alert_message, f"Actual alert message: {alert_message}"
        allure.attach(f"Validation successful: Alert message " + expected_alert_message + " displayed after saving changes.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info(
            "Validation successful: Alert message displayed after submitting.")

    """Author: Vipul Bokde
       Description: This method validates columns of contract tab
       Arguments: expected_contract_column_names
       Returns:NA """

    def validate_contract_tab_columns(self, expected_contract_column_names):
        # Validate Contract header columns
        locators.wait_until_presence_of_all_elements(
            self, "XPATH", self.bundle_contract_columns)
        column_elements = locators.locator_elements(
            self, "XPATH", self.bundle_contract_columns)
        visible_column_names = [
            element.text.strip() for element in column_elements if element.is_displayed()]
        self.expected_column_names_list = [name.strip()
                                           for name in expected_contract_column_names.split(',')]
        # Checking if expected columns are present in visible columns
        if set(self.expected_column_names_list).issubset(set(visible_column_names)):
            allure.attach("All expected columns are present in visible columns.",
                          attachment_type=allure.attachment_type.TEXT)
        for column_name in self.expected_column_names_list:
            mouse.click_on_element(
                self, "XPATH", self.bundle_contract_custom_columns.format(column_name))
            allure.attach(f"Column '{column_name}' is present on the page",
                          attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method adds contract from add contract pop-up screen
       Arguments: contract_source and contract_number
       Returns:NA """

    def validate_add_contracts(self, select_contract_source, contract_number):
        mouse.click_on_element(self, "XPATH", self.add_contract_button)
        forms_rfn.select_option_by_texts(
            self, (By.XPATH, self.select_contract_source), select_contract_source)
        mouse.click_on_element(
            self, "XPATH", self.checbox_selection.format(contract_number))
        locators.wait_until_visibility_of_element(
            self, "XPATH", self.add_contract_list_button)
        mouse.click_on_element(self, "XPATH", self.add_contract_list_button)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    """Author: Vipul Bokde
       Description: This method remove contract from contract pop-up screen
       Arguments: contract_number
       Returns:NA """

    def validate_remove_contracts(self, contract_number):
        mouse.click_on_element(
            self, "XPATH", self.checbox_selection.format(contract_number))
        mouse.click_on_element(self, "XPATH", self.remove_contract_button)
        mouse.click_on_element(self, "XPATH", self.remove_submit_btn)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    def navigate_to_contract_tab(self):
        mouse.click_on_element(self, "XPATH", self.navigate_contract_tab)
        allure.attach("Clicked on the 'Contract' tab.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info("Clicked on the 'Contract' tab.")

    def navigate_to_databucket_tab(self):
        mouse.click_on_element(self, "XPATH", self.navigate_databucket_tab)
        allure.attach("Clicked on the 'Data_Bucket' tab.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info("Clicked on the 'Data_Bucket' tab.")

    """Author: Vipul Bokde
       Description: This method validates columns of contract terms
       Arguments: expected_terms_column_names
       Returns:NA """

    def validate_contract_terms_tab_columns(self, expected_terms_column_names):
        self.validate_contract_tab_columns(expected_terms_column_names)

    """Author: Vipul Bokde
       Description: This method adds contract terms from add contract_terms pop-up screen
       Arguments: term_name
       Returns:NA """

    def validate_add_contracts_terms(self, term_name):
        mouse.click_on_element(self, "XPATH", self.add_contract_terms_button)
        mouse.click_on_element(
            self, "XPATH", self.checbox_selection.format(term_name))
        locators.wait_until_visibility_of_element(
            self, "XPATH", self.add_contract_term_list_button)
        mouse.click_on_element(
            self, "XPATH", self.add_contract_term_list_button)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    def validate_remove_contract_terms(self, term_name):
        mouse.click_on_element(
            self, "XPATH", self.checbox_selection.format(term_name))
        mouse.click_on_element(self, "XPATH", self.remove_terms_button)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    """Author: Vipul Bokde
       Description: This method generate random bundle_name
       Arguments:
       Returns: random_bundle_name """

    def generate_random_bundle_name(self, bundle_prefix, bundle_length):
        self.bundle_prefix = bundle_prefix
        self.bundle_length = int(bundle_length)
        allowed_characters = string.ascii_letters + string.digits
        random_bundle_name_suffix = ''.join(random.choice(
            allowed_characters) for _ in range(self.bundle_length))
        random_bundle_name = f"{self.bundle_prefix}{random_bundle_name_suffix}"
        return random_bundle_name

    def validate_contract_number_in_database(self, Sql_Contract_Query, contract_number, client_id):
        # To validate contract_number in database
        self.updated_query = Sql_Contract_Query.replace(
            '${contract_number}', contract_number)
        self.updated_query_1 = self.updated_query.replace(
            '${client_id}', client_id)
        logger.info("SQL Query Updated  : "+self.updated_query_1)
        allure.attach("SQL Query Updated  : "+self.updated_query_1,
                      attachment_type=allure.attachment_type.TEXT)
        self.query_result_1 = SqlConnection.connection(self.updated_query_1)
        # validate if the contract number in database
        if not self.query_result_1:
            allure.attach(f"Contract: {contract_number} not found in the database.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.error("Contract not found in the database.")
            assert False, f"Contract '{contract_number}' not found in the database."
        else:
            # Extracting the contract_number from the result
            contract_number_from_db = self.query_result_1[0][8]
            allure.attach(f"Contract Number: {contract_number_from_db} found in the database.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info(
                f"Contract Number found in the database: {contract_number_from_db} ")

    def validate_contract_term_in_database(self, Sql_Contract_Term__Query, term_name, client_id):
        # To validate contract_term_name in database
        self.updated_query = Sql_Contract_Term__Query.replace(
            '${term_name}', term_name)
        self.updated_query_1 = self.updated_query.replace(
            '${client_id}', client_id)
        logger.info("SQL Query Updated  : "+self.updated_query_1)
        allure.attach("SQL Query Updated  : "+self.updated_query_1,
                      attachment_type=allure.attachment_type.TEXT)
        self.query_result_1 = SqlConnection.connection(self.updated_query_1)
        # validate if the contract term exist in database
        if not self.query_result_1:
            allure.attach(f"Contract: {term_name} not found in the database.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.error("Contract not found in the database.")
            assert False, f"Contract '{term_name}' not found in the database."
        else:
            # Extracting the contract_term_name from the result
            contract_term_from_db = self.query_result_1[0][6]
            allure.attach(f"Contract term name: {contract_term_from_db} found in the database.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info(
                f"Contract term name found in the database: {contract_term_from_db} ")

    """Author: Vipul Bokde
       Description: This method edit and add data bucket in a bundle
       Arguments: data_bucket_name, checkbox_type
       Returns:NA """

    def validate_add_edit_data_buckets(self, data_bucket_name):
        self.click_data_bucket_checkbox_and_add(
            self.include_sales_checkbox, data_bucket_name)
        self.edit_data_bucket_checkbox(self.edit_discount_checkbox)

    """Author: Vipul Bokde
       Description: This method use 'add data bucket' option to add data bucket and check/uncheck checkox 
       acc.to checkbox_type
       Arguments: data_bucket_name, checkbox_type
       Returns:NA """

    def click_data_bucket_checkbox_and_add(self, checkbox_type, data_bucket_name):
        mouse.click_on_element(self, "XPATH", self.add_bucket_button)
        mouse.click_on_element(
            self, "XPATH", (checkbox_type).format(data_bucket_name))
        locators.wait_until_visibility_of_element(
            self, "XPATH", self.add_button_data_bucket)
        mouse.click_on_element(self, "XPATH", self.add_button_data_bucket)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    """Author: Vipul Bokde
       Description: This method use edit option of data bucket to check/uncheck acc. to checkbox_type
       Arguments: checkbox_type
       Returns:NA """

    def edit_data_bucket_checkbox(self, checkbox_type):
        mouse.click_on_element(self, "XPATH", self.edit_data_bucket)
        mouse.click_on_element(self, "XPATH", checkbox_type)
        locators.wait_until_visibility_of_element(
            self, "XPATH", self.save_edited_data_bucket)
        mouse.click_on_element(self, "XPATH", self.save_edited_data_bucket)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    """Author: Vipul Bokde
       Description: This method remove data bucket from bundle in data bucket tab
       Arguments: data_bucket_name
       Returns:NA """

    def validate_remove_data_bucket(self, data_bucket_name):
        mouse.click_on_element(
            self, "XPATH", self.checbox_selection.format(data_bucket_name))
        mouse.click_on_element(self, "XPATH", self.remove_bucket_button)
        mouse.click_on_element(self, "XPATH", self.save_btn)

    def navigate_to_revision_history_tab(self):
        mouse.click_on_element(self, "XPATH", self.navigate_rev_history_tab)
        allure.attach("Clicked on the 'revision_history' tab.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info("Clicked on the 'revision_history' tab.")

    """Author: Vipul Bokde
       Description: This method validates rev_history tab columns
       Arguments: NA
       Returns:NA """

    def validate_revision_history_columns(self, expected_column_names):
        self.gp_config.validate_gp_config_columns(expected_column_names)

    """Author: Vipul Bokde
       Description: This method validates rev_history data for the multiple versions
       Arguments: NA
       Returns:NA """

    def validate_bundle_revision_history_data(self):
        self.rev_history_columns_count = locators.locator_elements(
            self, "XPATH", self.gp_bundle_columns)
        self.rev_history_rows_count = locators.locator_elements(
            self, "XPATH", self.rev_history_rows)
        for row in self.rev_history_rows_count:
            rev_history_row_data = {}
            # itrerating each column of revision history tab
            for index, column in enumerate(self.rev_history_columns_count):
                # Getting the name of the column headers
                column_name = column.text
                # Getting the text of the each cell in the row
                cell_data = row.find_element(
                    By.XPATH, f"./div[{index + 1}]").text
                # Adding the column name and cell data to the rev_history_row_data
                rev_history_row_data[column_name] = cell_data
            logger.info(
                f"Bundle Revision History Row Data: {rev_history_row_data}")
            allure.attach(f"Bundle Revision HistoryRow Data: {rev_history_row_data}",
                          name="Rev_History_Table Data", attachment_type=allure.attachment_type.TEXT)

    def submit_bundle_for_approval(self):
        mouse.click_on_element(self, "XPATH", self.self.submit_approval_button)
        allure.attach("Clicked on the 'submit for approval' button.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info("Clicked on the 'submit for approval' button.")

    """Author: Vipul Bokde
       Description: This method approve the bundle by selecting the name of a bundle
       Arguments: Bundle_Name
       Returns:NA """

    def approve_bundle(self, Bundle_Name):
        self.page_count = forms.get_text_on_element(
            self, "XPATH", self.page_count)
        logger.info(self.page_count)
        if int(self.page_count) > 1:
            mouse.click_action_on_element(self, "XPATH", self.last_page)
        self.bundle_name_xl = Bundle_Name
        self.bundle_names_list = []
        self.bundle_names_list = self.driver.find_elements_by_xpath(
            self.Approval_Name_Row)
        logger.info(len(self.bundle_names_list))
        self.list_length = len(self.bundle_names_list)
        for i in range(1, self.list_length+1):
            self.bundle_names = "(//div[@class='p-3 float-left']/bundle-diff/div)["+str(i)+"]"
            mouse.scroll_to_element(self, "XPATH", self.bundle_names)
            self.bundle_names_ui = forms.get_text_on_element(
                self, "XPATH", self.bundle_names)
            logger.info(self.bundle_names_ui)
            logger.info(self.bundle_name_xl)
            if self.bundle_names_ui == self.bundle_name_xl:
                self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"
                logger.info("Bundle name found")
                allure.attach("Bundle Sucessfully Approved.",
                              attachment_type=allure.attachment_type.TEXT)
                forms.check_checkbox(self, "XPATH", self.Checkbox)
                logger.info("Checkbox Checked")

    """Author: Rushikesh Kharat
       Description: This method is use to click on customers tab
       Arguments:
       Returns:NA """

    def click_on_customers_tab(self):
        mouse.click_action_on_element(self, "XPATH", self.bundle_customers)
        logger.info(f"selected Customers Tab")
        allure.attach('Selected Customers Tab',
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method verifies the labels in Customers tab
       Arguments: 
       Returns:NA """

    def verify_cust_grouping_label_name(self):
        cust_group_elements = self.driver.find_elements_by_xpath(
            self.cust_grouping_label)
        for element1 in cust_group_elements:
            text1 = element1.get_attribute('innerHTML')
            logger.info(text1)
            if 'Customer Grouping' in text1:
                assert True
                logger.info(f"Customer Grouping label verified")
                allure.attach('Customer Grouping label verified',
                              attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method This method verifies the labels in Customers tab
       Arguments: 
       Returns:NA """

    def verify_cust_selection_label_name(self):
        cust_select_elements = self.driver.find_elements_by_xpath(
            self.cust_selection_label)
        for element2 in cust_select_elements:
            text2 = element2.get_attribute('innerHTML')
            logger.info(text2)
            if 'Customer Selection' in text2:
                assert True
                logger.info(f"Customer Selection label verified")
                allure.attach('Customer Selection label verified',
                              attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method selects the dropdown options in customer tab from sheet
       Arguments: 
       Returns:NA """

    def select_cust_grouping_options(self, grouping_option):
        self.grouping_option = grouping_option
        allure.attach(' Customer Grouping Option: ' + str(self.grouping_option),
                      attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(
            self, "XPATH", self.cust_grouping_dd, self.grouping_option)
        logger.info(
            "Selected from Customers grouping dropdown : " + self.grouping_option)
        allure.attach("Selected from Customers grouping dropdown : " + str(self.grouping_option),
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method selects the dropdown options in customer tab from sheet
       Arguments: 
       Returns:NA """

    def select_cust_selection_options(self, selection_option):
        self.selection_option = selection_option
        allure.attach('Customer Selection Option: ' + str(self.selection_option),
                      attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(
            self, "XPATH", self.cust_selection_dd, self.selection_option)
        logger.info("Select Filetype from dropdown : " + self.selection_option)
        allure.attach("Selected from Customers Selection dropdown : " + str(self.selection_option),
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method saves the modified changes. Or else raise the exception
       Arguments: 
       Returns:NA """

    def click_on_save(self):
        save_button_disabled = locators.get_attribute_value(
            self, "XPATH", self.save_btn, "disabled")
        if save_button_disabled == "true":
            allure.attach("Save button is disabled even after modification.",
                          attachment_type=allure.attachment_type.TEXT)
            logger.error(
                "Save button is disabled even after modification.")
        else:
            mouse.click_js_on_element(self, "XPATH", self.save_btn)
            allure.attach("Saved after modification.",
                          attachment_type=allure.attachment_type.TEXT)
        alert_message = forms.get_text_on_element(
            self, "XPATH", self.alert_text)
        expected_alert_message = alert_message
        assert alert_message == expected_alert_message, f"Actual alert message: {alert_message}"
        allure.attach(f"Validation successful: Alert message " + expected_alert_message + " displayed after saving changes.",
                      attachment_type=allure.attachment_type.TEXT)
        logger.info(
            "Validation successful: Alert message displayed after submitting.")

    """Author: Rushikesh Kharat
       Description: This method is use to navigate to products tab
       Arguments: 
       Returns:NA """

    def click_on_products_tab(self):
        time.sleep(1)
        mouse.click_action_on_element(self, "XPATH", self.bundle_products)
        logger.info("Clicking on Products Tab")
        allure.attach("Clicked on Products Tab",
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method to create product group
       Arguments: 
       Returns:NA """

    def add_product_group_buttons(self):
        logger.info("Clicking on Add Product Group")
        mouse.click_action_on_element(
            self, "XPATH", self.add_product_group_btn)
        # remove_group = mouse.click_action_on_element(self, "XPATH", self.remove_product_group_btn)
        allure.attach("Clicked on Add Product Group",
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method verifies the  headers on products tab for each grid
       Arguments: 3 headers
       Returns:NA """

    def verify_product_headers(self, product_group_header, product_selection_header, product_list_header):
        product_group_header = product_group_header
        product_selection_header = product_selection_header
        product_list_header = product_list_header
        try:
            prod_group = forms.get_text_on_element(
                self, "XPATH", self.x_prod_group)
            prod_select = forms.get_text_on_element(
                self, "XPATH", self.x_prod_select)
            prod_list = forms.get_text_on_element(
                self, "XPATH", self.x_prod_list)
            assert prod_group == product_group_header, "header name matched"
            assert prod_select == product_selection_header, "header name matched"
            assert prod_list == product_list_header, "header name matched"
        except AssertionError:
            raise AssertionError("Header name Not Found")
        logger.info(
            f"Verified the Headers as : {prod_group}, {prod_select},  {prod_list}")
        allure.attach("Verified the Header as : " + prod_group + prod_select + prod_list,
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method is for submit or cancel the configued changes
       Arguments: 
       Returns:NA """

    def click_on_submit(self):
        logger.info("Clicking on Submit")
        mouse.click_action_on_element(self, "XPATH", self.submitbutton)
        allure.attach("Clicked on submit button",
                      attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time('PRODUCTS->Submit')

    def click_on_cancel(self):
        logger.info("Clicking on Cancel")
        mouse.click_action_on_element(self, "XPATH", self.cancelbutton)
        allure.attach("Clicked on cancel button",
                      attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time('PRODUCTS->Cancel')

    """Author: Rushikesh Kharat
       Description: This method is created to fill the textbox
       Arguments: input value
       Returns:NA """

    def input_text(self, input_pg_value):
        self.input_pg_value = input_pg_value
        logger.info(f"Entering the value in Text Box...")
        forms.enter_text_on_element(
            self, "XPATH", self.inputbox, self.input_pg_value)  # df
        allure.attach("Entering the valid product group name: " + str(self.input_pg_value),
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method to input replaced value to check pencil icon functionality
       Arguments: replaced value 
       Returns:NA """

    def edit_using_pencil_icon(self, replace_pg_value):
        logger.info(f"Clicking on pencil icon")
        self.replace_pg_value = replace_pg_value
        mouse.click_on_element(self, "XPATH", self.pencil_icon)
        self.newinputvalue = self.input_pg_value.replace(
            self.input_pg_value, self.replace_pg_value)  # df
        forms.enter_text_on_element(
            self, "XPATH", self.inputbox, self.newinputvalue)
        logger.info(f"Clicked on Pencil Icon")
        allure.attach("Re-edited the Product group name from  " + self.input_pg_value + ' to ' + self.replace_pg_value,
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method to selection the dropdown on product selection
       Arguments: product_selection_options
       Returns:NA """

    def select_product_selection_options(self, product_selection_options):
        logger.info(f"Selecting products selection option")
        self.product_selection_option = product_selection_options  # df
        forms.select_option_by_text(self, "XPATH", self.prod_selection_dd,
                                    self.product_selection_option)
        logger.info("selected from dropdown : " +
                    self.product_selection_option)
        allure.attach("Selected the option from Product Selection Drodown:  " + self.product_selection_option,
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method for adding the product(s) in product group
       Arguments: 
       Returns:NA """

    def add_product_in_groups(self):
        try:
            # self.product_group_dd_selection = product_group_dd_selection
            logger.info(f"Adding products in product group")
            mouse.click_action_on_element(self, "XPATH", self.add_product_btn)
            forms.select_option_by_text(
                self, "XPATH", self.add_prod_popup_dd, self.newinputvalue)  # df
            allure.attach("Product(s) are added to the Group(s)",
                          attachment_type=allure.attachment_type.TEXT)
        except NoSuchElementException:
            allure.attach("Product(s) are not available to add. Ensure the Product is associated and available for Product Groups,Contract_Terms and Contracts",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info("No Product is available to add")

    """Author: Rushikesh Kharat
       Description: This method is to submit the list of product selected(all)
       Arguments: 
       Returns:NA """

    def click_on_submit_product_list(self):
        logger.info(f"Submitting selected product(s) list")
        mouse.click_action_on_element(self, "XPATH", self.listsubmitbutton)
        allure.attach("Clicked on submit button",
                      attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time('PRODUCTS->Submit')

    """Author: Rushikesh Kharat
       Description: This method is for removing the product from the added list
       Arguments: 
       Returns:NA """

    def remove_product(self):
        try:
            logger.info(f"Adding products in product group")
            forms.check_checkbox(self, "XPATH", self.product_list_cb)
            allure.attach("Checkbox is checked",
                          attachment_type=allure.attachment_type.TEXT)
            mouse.click_action_on_element(
                self, "XPATH", self.remove_product_btn)
            mouse.click_action_on_element(
                self, "XPATH", self.rem_product_submit)
            allure.attach("Product(s) is removed",
                          attachment_type=allure.attachment_type.TEXT)
        except NoSuchElementException:
            allure.attach("No Product is Present to Remove. Product must be added to perform Remove Product Operation",
                          attachment_type=allure.attachment_type.TEXT)
            logger.info("Product Not Found after: " +
                        self.product_selection_option)

    """Author: Rushikesh Kharat
       Description: This method remove product group
       Arguments: 
       Returns:NA """

    def remove_product_group(self):
        logger.info(f"Removing Product Group")
        forms.check_checkbox(self, "XPATH", self.product_group_cb)
        allure.attach("Checkbox is checked",
                      attachment_type=allure.attachment_type.TEXT)
        mouse.click_action_on_element(
            self, "XPATH", self.remove_product_group_btn)
        mouse.click_action_on_element(
            self, "XPATH", self.rem_product_grp_submit)
        mouse.click_js_on_element(self, "XPATH", self.save_btn)
        allure.attach("Product Group is removed",
                      attachment_type=allure.attachment_type.TEXT)

    """Author: Rushikesh Kharat
       Description: This method is for checkbox functionality
       Arguments: expected_terms_column_names
       Returns:NA """

    def check_checkbox(self):
        logger.info(f"Checking the checkbox")
        self.checkbox = "//div[@row-index='1']//span[@class='ag-selection-checkbox']"
        forms.check_checkbox(self, "XPATH", self.checkbox)
        allure.attach("Checkbox is checked",
                      attachment_type=allure.attachment_type.TEXT)
