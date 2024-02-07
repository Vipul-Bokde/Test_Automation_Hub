from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from libraries import mapping, mouse, forms, locators, locators_rfn, forms_rfn
import allure
from allure_commons.types import AttachmentType
import os
import time
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from selenium.webdriver.common.by import By
from GP.pages.main_page import MainPage
from CBK.pages.Products_Page import ProductsPage
from CBK.utilities.excelUtility import create_csv_file
import GP.utilities.Repo as Repo
from CBK.pages.upload_844file_page import Upload844FilePage
from GP.pages.uploads_screen_page import UploadPage
from GP.pages.client_joins_page import NewJoinPage
from GP.utilities.database_connection import SqlConnection
from GP.pages.data_overview_page import DataOverviewPage
import json
from datetime import datetime, timezone, timedelta
ist_timezone_offset = timedelta(hours=5, minutes=30)


class GPConfigPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        self.cbk_product = ProductsPage(self.driver)
        self.upload_screen = UploadPage(self.driver)
        self.upload844file = Upload844FilePage(self.driver)
        self.upload_file = NewJoinPage(self.driver)
        self.data_ov_page = DataOverviewPage(self.driver)
        # locators
        self.gp_config_custom_columns = "//div/span[@role = 'columnheader'and text() = '{}']"
        self.gp_config_columns = "//div/span[@role = 'columnheader']"
        self.add_config_button = "//button[normalize-space()='Add Config']"
        self.show_all_button = "//span[@class='slider round']"
        self.reversal_source_dropdown = "//select[@id='rev-source']"
        self.pair_columns_dropdown = "(//span[@class='dropdown-btn'])[1]"
        self.pair_column_values = "//div[normalize-space()= '{}']"
        self.reversal_column_values = "//*[@id='reversal-columns']//div[contains(text(),'{}')]"
        self.reversal_columns_dropdown = "(//span[@class='dropdown-btn'])[2]"
        self.config_submit_btn = "//button[@id='config-submit-btn']"
        self.cancel_btn = "//button[@id='run-cancel-btn']"
        self.pair_column_search = "(//input[@placeholder = 'Search'])[1]"
        self.reversal_column_search = "(//input[@placeholder = 'Search'])[2]"
        self.delete_value_by_row = "//div[@class ='ag-center-cols-container']/div[@row-id]/div[text()='{}']/following-sibling::div[@title='Delete']"
        self.pair_and_reversal_value_element = "//div[@role='gridcell' and text()= '{}']"
        self.inactive_element_check = "//div[@class ='ag-center-cols-container']/div[@row-id]/div[text()='{}']/following-sibling::div[text()='ACTIVE']"
        self.file_source_dropdown = "//select[@id='file-source']"
        self.uploaded_file_name = "//div[text()='{}']"
        self.upload_file_button = "//button[@id='upload-file-btn']"
        self.reversal_job_id = "//div[@row-id = '0']/div[@col-id='job_id']"
        self.reversal_job_source = "//div[@row-id = '0']/div[@col-id='job_id']/following-sibling::div[@col-id='log_1']"

    def select_gp_config_submenu_from_client_menu(self):
        time.sleep(2)
        self.main.select_gp_option('CLIENT', sub_item='GP CONFIGURATIONS')
        time.sleep(5)

    """Author: Vipul Bokde
       Description: This method va;idates the columns of GP Configuration Screen
       Arguments: GP Config Columns Names 
       Returns:NA """

    def validate_gp_config_columns(self, expected_column_names):
        try:
            locators.wait_until_presence_of_all_elements(self, "XPATH", self.gp_config_columns)
            column_elements = locators.locator_elements(self, "XPATH", self.gp_config_columns)
            visible_column_names = [
                element.text for element in column_elements if element.is_displayed()]
            self.expected_column_names_list = expected_column_names.split(',')
            assert sorted(visible_column_names) == sorted(
                self.expected_column_names_list), "Visible column names mismatch"
            for column_name in visible_column_names:
                mouse.click_on_element(
                    self, "XPATH", self.gp_config_custom_columns.format(column_name))
                allure.attach(f"Column '{column_name}' is present on the page",
                              attachment_type=allure.attachment_type.TEXT)
        except Exception as e:
            print("An error occurred while validating columns:", str(e))

    """Author: Vipul Bokde
       Description: This method add GP Transaction Config by adding source, pair 
       and reversal columns values
       Arguments: mandatory values in dropdown 
       Returns:NA """

    def add_gp_transaction_reversal_configuration(self, reversal_source_value, pair_column_values, reversal_column_values, numeric_value):
        self.index_value = numeric_value['index_value']
        self.value_1 = numeric_value['value_1']
        self.value_2 = numeric_value['value_2']
        self.value_3 = numeric_value['value_3']
        self.pair_column_values_list = pair_column_values.split(',')
        self.reversal_column_values_list = reversal_column_values.split(',')
        self.click_on_addconfig_and_source(reversal_source_value)
        mouse.click_on_element(self, "XPATH", self.pair_columns_dropdown)
        # Choosing the first three pair values from pair column dropdown
        for pair_value in self.pair_column_values_list[:int(self.value_3)]:
            mouse.click_on_element(self, "XPATH", self.pair_column_values.format(pair_value))
        fourth_pair_value = self.pair_column_values_list[int(self.value_3)]
        # Entering the 4th pair value using search functionality and clicking on checkbox
        forms.enter_text_on_element(self, "XPATH", self.pair_column_search, fourth_pair_value)
        mouse.click_on_element(self, "XPATH", self.pair_column_values.format(fourth_pair_value))
        # Clicking it again on Pair Column dropdown to close it
        mouse.click_on_element(self, "XPATH", self.pair_columns_dropdown)
        mouse.click_on_element(self, "XPATH", self.reversal_columns_dropdown)
        # Choosing the first two reversal values
        for rev_value in self.reversal_column_values_list[:int(self.value_2)]:
            mouse.click_on_element(self, "XPATH", self.reversal_column_values.format(rev_value))
        # Clicking it again on reversal Column dropdown to close it
        mouse.click_on_element(self, "XPATH", self.reversal_columns_dropdown)
        mouse.click_on_element(self, "XPATH", self.config_submit_btn)

    """Author: Vipul Bokde
       Description: This method delete GP Transaction Config pair and reversal values
       Arguments: pair and reversal values 
       Returns:NA """

    def delete_pair_rev_values(self, reversal_source_value, pair_column_values, reversal_column_values):
        self.pair_column_values_list = pair_column_values.split(',')
        self.reversal_column_values_list = reversal_column_values.split(',')
        # deleting the existing two pair values from configuration screen
        for index in range(len(self.pair_column_values_list[:int(self.value_2)])):
            pair_value = self.pair_column_values_list[index]
            self.delete_locator = self.delete_value_by_row.format(pair_value)
            mouse.click_on_element(self, "XPATH", self.delete_locator)
            allure.attach(
                f"Sucessfully deleted pair value: '{pair_value}' from config screen", attachment_type=allure.attachment_type.TEXT)
        # deleting the existing two reversal values from configuration screen
        for index in range(len(self.reversal_column_values_list[:int(self.value_2)])):
            rev_value = self.reversal_column_values_list[index]
            self.delete_locator = self.delete_value_by_row.format(rev_value)
            mouse.click_on_element(self, "XPATH", self.delete_locator)
            allure.attach(
                f"Sucessfully deleted pair value: '{rev_value}' from config screen", attachment_type=allure.attachment_type.TEXT)

    """Author: Vipul Bokde
       Description: This method validate the status "Active" and 'Inactive' of 
       GP Transaction Config pair and reversal values
       Arguments: pair and reversal values 
       Returns:NA """

    def validate_statuses_pair_and_rev_values(self, pair_column_values, reversal_column_values):
        mouse.click_on_element(self, "XPATH", self.show_all_button)
        for index in range(len(self.pair_column_values_list[:int(self.value_2)])):
            pair_value = self.pair_column_values_list[index]
            self.status_check_locator = self.inactive_element_check.format(pair_value)
            is_inactive = not locators.element_exists(self, "XPATH", self.status_check_locator)
            assert is_inactive, f"The status for '{pair_value}' is 'ACTIVE'"
            allure.attach(f"Status of '{pair_value}' is INACTIVE on the show all config page",
                          attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, "XPATH", self.show_all_button)

    """Author: Vipul Bokde
       Description: This Method clicks on add config button and select source from dropdown
       Arguments: pair and reversal values 
       Returns:NA """

    def click_on_addconfig_and_source(self, reversal_source_value):
        self.reversal_source_value = reversal_source_value
        mouse.click_on_element(self, "XPATH", self.add_config_button)
        # Selecting the reversal source value
        forms_rfn.select_option_by_texts(
            self, (By.XPATH, self.reversal_source_dropdown), self.reversal_source_value)

    """Author: Vipul Bokde
       Description: This method modify GP Transaction Config pair and reversal values by 
       adding it from dropdown
       Arguments: pair and reversal values 
       Returns:NA """

    def modify_pair_rev_values(self, reversal_source_value, pair_column_values, reversal_column_values):
        # adding those two deleted pair values from pair value dropdown
        self.click_on_addconfig_and_source(reversal_source_value)
        mouse.click_on_element(self, "XPATH", self.pair_columns_dropdown)
        for pair_value in self.pair_column_values_list[:int(self.value_2)]:
            mouse.click_on_element(self, "XPATH", self.pair_column_values.format(pair_value))
        mouse.click_on_element(self, "XPATH", self.pair_columns_dropdown)
        # again adding one reversal values from reversal value dropdown)
        mouse.click_on_element(self, "XPATH", self.reversal_columns_dropdown)
        for rev_value in self.reversal_column_values_list[:int(self.value_1)]:
            mouse.click_on_element(self, "XPATH", self.reversal_column_values.format(rev_value))
        mouse.click_on_element(self, "XPATH", self.reversal_columns_dropdown)
        mouse.click_on_element(self, "XPATH", self.config_submit_btn)

    def upload_rebate_file(self, source_file_name, file_type, file_to_upload_path, file_to_upload):
        self.source_file_name = source_file_name
        self.file_type = file_type
        self.file_to_upload = file_to_upload
        self.file_to_upload_path = file_to_upload_path
        self.upload844file.select_uploads_from_burguer_menu()
        mouse.click_on_element(self, "XPATH", self.upload_file_button)
        forms_rfn.select_option_by_texts(
            self, (By.XPATH, self.upload_screen.File_Type), self.file_type)
        locators.wait_until_visibility_of_element(self, "XPATH", self.file_source_dropdown)
        forms_rfn.select_option_by_texts(
            self, (By.XPATH, self.file_source_dropdown), self.source_file_name)
        self.upload_file.upload_file(self.file_to_upload_path)
        self.upload844file.click_submit_button()
        time.sleep(12)
        locators.wait_until_visibility_of_element(
            self, "XPATH", self.uploaded_file_name.format(self.file_to_upload))
        mouse.click_on_element(self, "XPATH", self.uploaded_file_name.format(self.file_to_upload))

    """Author: Vipul Bokde
       Description: This method validate data from db to check entry created 
       in gp.rebate and gp.trans_reversal_summary table
       Arguments: pair and reversal values 
       Returns:NA """

    def validate_rebate_file_data_from_db(self, client_id, sql_query, sql_query_2, period_month):
        expected_period = period_month
        # To validate data in gp.rebate database
        self.updated_query = sql_query.replace('${period_month}', period_month)
        self.updated_query_1 = self.updated_query.replace('${client_id}', client_id)
        logger.info("SQL Query Updated  : "+self.updated_query_1)
        allure.attach("SQL Query Updated  : "+self.updated_query_1,
                      attachment_type=allure.attachment_type.TEXT)
        self.query_result_1 = SqlConnection.connection(self.updated_query_1)
        # query result
        logger.info("SQL Result Set:")
        for row in self.query_result_1:
            logger.info(row)
        query_json_result = json.dumps(self.query_result_1, default=str, sort_keys=True)
        allure.attach("SQL Result Set: item, st_num, quantity, rebate_amount, period_month " +
                      query_json_result, attachment_type=allure.attachment_type.JSON)
        # To validate data in gp trans_reversal_summary database
        self.updated_query_new = sql_query_2.replace('${period_month}', period_month)
        self.updated_query_new_1 = self.updated_query_new.replace('${client_id}', client_id)
        logger.info("SQL Query2 Updated  : "+self.updated_query_new_1)
        allure.attach("SQL Query2 Updated  : "+self.updated_query_new_1,
                      attachment_type=allure.attachment_type.TEXT)
        self.query_result_2 = SqlConnection.connection(self.updated_query_new_1)
        for row in self.query_result_2:
            logger.info(row)
            period = row[int(self.index_value)]
            if period != expected_period:
                error_message = "Validation failed:"
                error_message += f" period: Expected {expected_period}, Actual {period};"
                allure.attach(error_message, attachment_type=allure.attachment_type.TEXT)
                logger.error(error_message)
                raise AssertionError("Validation failed.")
        query_json_result_2 = json.dumps(self.query_result_2, default=str, sort_keys=True)
        allure.attach("SQL Result Set_2: " + query_json_result_2,
                      attachment_type=allure.attachment_type.JSON)
        allure.attach("Validation succeeded: period matched the expected period",
                      attachment_type=allure.attachment_type.TEXT)
        return self.query_result_1, self.query_result_2

    """Author: Vipul Bokde
       Description: This method validate GP Transaction Job by running only on after 3PM IST and extract 
       the job_id and check the status in md.job table to validate status
       Arguments: reversal_source name to validate the source name 
       Returns:NA """

    def perform_validate_transaction_reversal_job(self, sql_query_3, reversal_source_name):
        if self.transaction_reversal_job_time_ist():
            self.main.select_gp_option('TRANSACTION REVERSAL JOB TRACKER', sub_item=None)
            self.job_id = forms.get_text_on_element(self, "XPATH", self.reversal_job_id)
            time.sleep(2)
            self.reversal_source_value = forms.get_text_on_element(
                self, "XPATH", self.reversal_job_source)
            if self.reversal_source_value == reversal_source_name:
                self.updated_query = sql_query_3.replace('${job_id}', self.job_id)
                logger.info("SQL Query Updated  : "+self.updated_query)
                allure.attach("SQL Query Updated  : "+self.updated_query,
                              attachment_type=allure.attachment_type.TEXT)
                self.query_result = SqlConnection.connection(self.updated_query)
                for row in self.query_result:
                    logger.info(row)
                    status = row[int(self.index_value)]
                    status_str = str(status)
                    status_message = self.get_status_message(status_str)
                    allure.attach(f"Status: {status} - {status_message}",
                                  attachment_type=allure.attachment_type.TEXT)
                    if str(status) != '3':
                        raise Exception(
                            f"Reversal Job Status is not showing 'Complete': {status} - {status_message}")
                query_json_result = json.dumps(self.query_result, default=str, sort_keys=True)
                allure.attach("SQL Result Set: " + query_json_result,
                              attachment_type=allure.attachment_type.JSON)
        else:
            print("You can not execute the reversal job before 3pm, it will only be executed after 3 PM IST")

    """Author: Vipul Bokde
       Description: This method use to add time specific run of script by comparing current time
       Arguments: NA
       Returns:NA """

    def transaction_reversal_job_time_ist(self):
        current_time_utc = datetime.now(timezone.utc)
        current_time_ist = current_time_utc + ist_timezone_offset
        return current_time_ist.hour >= 15

    """Author: Vipul Bokde
       Description: This method added gp transaction job statuses
       Arguments: NA
       Returns:NA """

    def get_status_message(self, status):
        status_dict = {
            '1': 'Queued',
            '2': 'Running',
            '3': 'Complete',
            '4': 'Error'
        }
        return status_dict.get(status, f'Unknown Status: {status}')
