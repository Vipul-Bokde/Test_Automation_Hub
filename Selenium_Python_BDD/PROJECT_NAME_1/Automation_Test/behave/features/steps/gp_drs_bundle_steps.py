from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.gp_drs_bundle_page import GPDRSBundlePage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import generics
from libraries import files
import allure
from GP.pages.approvals_page import ApprovalsPage


class GP_DRS_Bundle(EnvironmentSetup):

    @staticmethod
    def get_random_bundle_name(self):
        if not hasattr(self, "get_random_bundle_name"):
            self.get_random_bundle_name = None
        return self.get_random_bundle_name

    @staticmethod
    def set_random_bundle_name(self, value):
        self.get_random_bundle_name = value

    @given(u'I select Bundle Definition Editor option under DRS from the burger menu')
    def step_impl(self):
        self.GPDRSBundlePage = GPDRSBundlePage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for gp drs bundle def editor sub menu")
        self.GPDRSBundlePage.select_gp_bundle_def_submenu_from_drs_menu()
        logger.info(
            "Successfully clicked on bundle definition editor under the drs menu")

    @when(u'I validate Bundle Definition Screen Columns')
    def step_impl(self):
        self.expected_column_names = self.td_set['expected_column_names']
        self.GPDRSBundlePage.validate_bundle_defintion_columns(
            self.expected_column_names)
        logger.info("Successfully Validated bundle defintion screen columns")

    @then(u'I create and validate new bundle definition on bundle definition page')
    def step_impl(self):
        self.bundle_prefix = self.td_set['bundle_prefix']
        self.bundle_length = self.td_set['bundle_length']
        self.generated_random_bundle_name = self.GPDRSBundlePage.generate_random_bundle_name(
            self.bundle_prefix, self.bundle_length)
        # read/write scenario by using json file
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_bundle_name = self.td_set['Key As Bundle Name']
        files.write_into_json_file(self.service_name, self.json_file_name,
                                   self.key_as_bundle_name, self.generated_random_bundle_name)
        GP_DRS_Bundle.set_random_bundle_name(self, files.read_from_json_file(
            self.service_name, self.json_file_name, self.key_as_bundle_name))
        self.GPDRSBundlePage.validate_create_new_bundle_defintion(
            GP_DRS_Bundle.get_random_bundle_name(self))
        logger.info("Successfully created new bundle on bundle page")

    @when(u'I validate bundle definition name in database')
    def step_impl(self):
        self.Sql_Bundle_Definition_Query = self.td_set['Sql_Bundle_Definition_Query']
        self.client_id = self.td_set['client_id']
        self.GPDRSBundlePage.validate_bundle_creation_in_database(
            self.Sql_Bundle_Definition_Query, GP_DRS_Bundle.get_random_bundle_name(self), self.client_id)
        logger.info("Successfully validated bundle name in database")

    @then(u'I click on a bundle')
    def step_impl(self):
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_bundle_name = self.td_set['Key As Bundle Name']
        self.GPDRSBundlePage = GPDRSBundlePage(self.driver)
        GP_DRS_Bundle.set_random_bundle_name(self, files.read_from_json_file(
            self.service_name, self.json_file_name, self.key_as_bundle_name))
        self.GPDRSBundlePage.click_on_a_bundle(
            GP_DRS_Bundle.get_random_bundle_name(self))
        logger.info("Successfully clicked on a bundle from bundle page")

    @then(u'I submit bundle for approval')
    def step_impl(self):
        self.GPDRSBundlePage.submit_bundle_for_approval()
        logger.info("Successfully submitted bundle for approval")

    @then(u'I validate bundle status after approval')
    def step_impl(self):
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_bundle_name = self.td_set['Key As Bundle Name']
        self.Bundle_status = self.td_set['Bundle_status']
        GP_DRS_Bundle.set_random_bundle_name(self, files.read_from_json_file(
            self.service_name, self.json_file_name, self.key_as_bundle_name))
        self.GPDRSBundlePage.validate_bundle_statuses(
            GP_DRS_Bundle.get_random_bundle_name(self), self.Bundle_status)
        logger.info("Successfully validated the status of a bundle")

    @then(u'I delete bundle definition from bundle definition page')
    def step_impl(self):
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_bundle_name = self.td_set['Key As Bundle Name']
        self.GPDRSBundlePage = GPDRSBundlePage(self.driver)
        GP_DRS_Bundle.set_random_bundle_name(self, files.read_from_json_file(
            self.service_name, self.json_file_name, self.key_as_bundle_name))
        self.GPDRSBundlePage.delete_created_bundle_defintion(
            GP_DRS_Bundle.get_random_bundle_name(self))
        logger.info("Successfully deleted bundle from bundle page")

    @when(u'I entered bundle defnition tab and validate its elements')
    def step_impl(self):
        self.bundle_description = self.td_set['bundle_description']
        self.GPDRSBundlePage.validate_bundle_def_defintion_tab_modifications(
            self.bundle_description)
        logger.info(
            "Successfully modified bundle definition description from definition tab")

    @when(u'I navigate and click on contract tab')
    def step_impl(self):
        self.GPDRSBundlePage.navigate_to_contract_tab()
        logger.info("Successfully clicked on a contract tab")

    @when(u'I entered contract tab and validate its elements')
    def step_impl(self):
        self.contract_number = self.td_set['contract_number']
        self.contract_source = self.td_set['contract_source']
        self.GPDRSBundlePage.validate_add_contracts(
            self.contract_source, self.contract_number)
        logger.info("Successfully validated contract tab and its elements")

    @when(u'I entered contract tab and validate its columns')
    def step_impl(self):
        self.expected_contract_column_names = self.td_set['expected_contract_column_names']
        self.GPDRSBundlePage.validate_contract_tab_columns(
            self.expected_contract_column_names)
        logger.info("Successfully validated contract tab columns")

    @when(u'I entered contract_term tab and validate its columns')
    def step_impl(self):
        self.expected_terms_column_names = self.td_set['expected_terms_column_names']
        self.GPDRSBundlePage.validate_contract_terms_tab_columns(
            self.expected_terms_column_names)
        logger.info("Successfully validated contract terms columns")

    @when(u'I navigate contract terms tab and validate its elements')
    def step_impl(self):
        self.term_name = self.td_set['term_name']
        self.GPDRSBundlePage.validate_add_contracts_terms(self.term_name)
        logger.info(
            "Successfully validated contract terms tab and its elements")

    @when(u'I remove contract from contract tab')
    def step_impl(self):
        self.contract_number = self.td_set['contract_number']
        self.GPDRSBundlePage.validate_remove_contracts(self.contract_number)
        logger.info("Successfully removed contract from contract tab")

    @when(u'I remove contract terms from contract tab')
    def step_impl(self):
        self.term_name = self.td_set['term_name']
        self.GPDRSBundlePage.validate_remove_contract_terms(self.term_name)
        logger.info("Successfully removed contract terms from contract tab")

    @when(u'I validate contract number in database')
    def step_impl(self):
        self.Sql_Contract_Query = self.td_set['Sql_Contract_Query']
        self.contract_number = self.td_set['contract_number']
        self.client_id = self.td_set['client_id']
        self.GPDRSBundlePage.validate_contract_number_in_database(
            self.Sql_Contract_Query, self.contract_number, self.client_id)
        logger.info("Successfully validated contract number in database")

    @when(u'I validate contract_term name in database')
    def step_impl(self):
        self.Sql_Contract_Term__Query = self.td_set['Sql_Contract_Term__Query']
        self.term_name = self.td_set['term_name']
        self.client_id = self.td_set['client_id']
        self.GPDRSBundlePage.validate_contract_term_in_database(
            self.Sql_Contract_Term__Query, self.term_name, self.client_id)
        logger.info("Successfully validated term_name in database")

    @when(u'I navigate and click on data_bucket tab')
    def step_impl(self):
        self.GPDRSBundlePage.navigate_to_databucket_tab()
        logger.info("Successfully clicked on a data_bucket tab")

    @when(u'I navigate data bucket tab and validate its elements')
    def step_impl(self):
        self.data_bucket_name = self.td_set['data_bucket_name']
        self.GPDRSBundlePage.validate_add_edit_data_buckets(
            self.data_bucket_name)
        logger.info("Successfully added data bucket in a bundle")

    @when(u'I remove specific data bucket from data bucket tab')
    def step_impl(self):
        self.data_bucket_name = self.td_set['data_bucket_name']
        self.GPDRSBundlePage.validate_remove_data_bucket(self.data_bucket_name)
        logger.info("Successfully removed data bucket from bundle")

    @when(u'I navigate and click on revision history tab')
    def step_impl(self):
        self.GPDRSBundlePage.navigate_to_revision_history_tab()
        logger.info("Successfully clicked on a revision history tab")

    @when(u'I validate revision history tab columns')
    def step_impl(self):
        self.revision_history_columns = self.td_set['revision_history_columns']
        self.GPDRSBundlePage.validate_revision_history_columns(
            self.revision_history_columns)
        logger.info("Successfully Validated revision history tab columns")

    @when(u'I validate revision history data')
    def step_impl(self):
        self.GPDRSBundlePage.validate_bundle_revision_history_data()
        logger.info("Successfully Validated revision history data")

    @then(u'I select bundle name for approval and approve')
    def step_impl(self):
        logger.info("Select given value and approve")
        self.GPDRSBundlePage = GPDRSBundlePage(self.driver)
        self.service_name = self.td_set['Service Name']
        self.json_file_name = self.td_set['JSON File Name']
        self.key_as_bundle_name = self.td_set['Key As Bundle Name']
        GP_DRS_Bundle.set_random_bundle_name(self, files.read_from_json_file(
            self.service_name, self.json_file_name, self.key_as_bundle_name))
        self.GPDRSBundlePage.approve_bundle(
            GP_DRS_Bundle.get_random_bundle_name(self))
        self.Approvals = ApprovalsPage(self.driver)
        self.Approvals.click_on_approve_button()

    @then(u'I go to Customers tab')
    def step_impl(self):
        self.GPDRSBundlePage.click_on_customers_tab()
        logger.info("Selected the Customers Tab")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Clustomers Tab")

    @then(u'I verify the headers of dropdowns')
    def step_impl(self):
        self.GPDRSBundlePage.verify_cust_grouping_label_name()
        self.GPDRSBundlePage.verify_cust_selection_label_name()
        logger.info(
            "Dropdown Lebel VERIFIED for 'Customer Grouping' and 'Customer Selection'")
        generics.capture_screenshot_allure(self.GPDRSBundlePage, "Dropdowns")

    @then(u'I select the dropdown menu for Customer Grouping')
    def step_impl(self):
        self.grouping_option = self.td_set['CUSTOMER GROUPING']
        self.GPDRSBundlePage.select_cust_grouping_options(self.grouping_option)
        logger.info(
            f"Dropdown selected for Customer Grouping: {self.grouping_option}")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Customer Grouping")

    @then(u'I select the dropdown menu for Customer Selection')
    def step_impl(self):
        self.selection_option = self.td_set['CUSTOMER SELECTION']
        self.GPDRSBundlePage.select_cust_selection_options(
            self.selection_option)
        logger.info(
            f"Dropdown selected for Customer Selection: {self.selection_option}")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Customer Selection")

    @then(u'I click on save')
    def step_impl(self):
        self.GPDRSBundlePage.click_on_save()
        logger.info("Clicked on SAVE")

    @then(u'I go to Products tab')
    def step_impl(self):
        self.GPDRSBundlePage.click_on_products_tab()
        logger.info("Selected the Products Tab")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Products Tab")

    @then(u'I verify the headers in products tab')
    def step_impl(self):
        product_group_header = 'Product Groups'
        product_selection_header = 'Product Selection'
        product_list_header = 'Product List'
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Header Verification")
        self.GPDRSBundlePage.verify_product_headers(
            product_group_header, product_selection_header, product_list_header)
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Header Verification")

    @then(u'I click on Add Products Group')
    def step_impl(self):
        self.GPDRSBundlePage.add_product_group_buttons()
        logger.info("Clicked on Add Product Group")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Add Product Group")

    @then(u'I click on Cancel')
    def step_impl(self):
        self.GPDRSBundlePage.click_on_cancel()
        logger.info("Clicked on Cancel")

    @then(u'I enter the valid Product Group name')
    def step_impl(self):
        self.input_pg_value = self.td_set['PRODUCT GROUP NAME']
        self.GPDRSBundlePage.input_text(self.input_pg_value)
        logger.info(
            f"Entering the valid product group name: {self.input_pg_value}")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Product group Name")

    @then(u'I click on submit button in products group tab')
    def step_impl(self):
        self.GPDRSBundlePage.click_on_submit()
        logger.info("Clicked on Submit")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Submit Product Group Name")

    @then(u'I remove the product group')
    def step_impl(self):
        self.GPDRSBundlePage.remove_product_group()
        logger.info(f"Removed the product group: {self.input_pg_value}")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Remove Product Group")

    @then(u'I edit the product group name using pencil icon')
    def step_impl(self):
        self.replace_pg_value = self.td_set['REPLACED PRODUCT GROUP NAME']
        self.GPDRSBundlePage.edit_using_pencil_icon(self.replace_pg_value)
        logger.info(
            f"Re-edited the Product group name from {self.input_pg_value} to {self.replace_pg_value} using pencil icon")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Pencil Icon Edit functionality")

    @then(u'I select the option from Product selection dropdown')
    def step_impl(self):
        self.product_selection_options = self.td_set['PRODUCT SELECTION OPTIONS']
        self.GPDRSBundlePage.select_product_selection_options(
            self.product_selection_options)
        logger.info(
            f"Selected the option from Product Selection dropdown: {self.product_selection_options}")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Product Selection dropdown")

    @when(u'I click on Add Product')
    def step_impl(self):
        self.GPDRSBundlePage.add_product_in_groups()
        logger.info("Clicked on Add Product button")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Add Product pop up")

    @then(u'I click on submit button in products list tab')
    def step_impl(self):
        self.GPDRSBundlePage.click_on_submit_product_list()
        logger.info("Clicked on Submit button to add selected products")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Submit products to add")

    @then(u'I click on Remove Product')
    def step_impl(self):
        self.GPDRSBundlePage.remove_product()
        logger.info("Selected product is successfully removed")
        generics.capture_screenshot_allure(
            self.GPDRSBundlePage, "Remove Product")
