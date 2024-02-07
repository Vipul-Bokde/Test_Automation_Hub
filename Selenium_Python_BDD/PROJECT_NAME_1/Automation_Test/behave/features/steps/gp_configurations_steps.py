from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.gp_configuration_page import GPConfigPage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login
import GP.utilities.Repo as Repo
from GP.pages.main_page import MainPage
from GP.pages.rebate_transfer_page import RebateTransferPage
from libraries import generics


class GPConfig(EnvironmentSetup):

    @given(u'I select GP Configurations option under client from the burger menu')
    def step_impl(self):
        self.GPConfigPage = GPConfigPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for gp configurations client menu")
        self.GPConfigPage.select_gp_config_submenu_from_client_menu()
        logger.info("Successfully clicked on gp config under the client menu")

    @when(u'I validate GP Configurations Screen Columns')
    def step_impl(self):
        self.expected_column_names = self.td_set['expected_column_names']
        self.GPConfigPage.validate_gp_config_columns(self.expected_column_names)
        logger.info("Successfully Validated gp config screen columns")

    @when(u'I click on add config and create new GP Configuration')
    def step_impl(self):
        self.numeric_value = {
            'index_value': self.td_set['index_value'],
            'value_1': self.td_set['value_1'],
            'value_2': self.td_set['value_2'],
            'value_3': self.td_set['value_3']}
        self.reversal_source_value = self.td_set['reversal_source_value']
        self.pair_column_values = self.td_set['pair_column_values']
        self.reversal_column_values = self.td_set['reversal_column_values']
        self.GPConfigPage.add_gp_transaction_reversal_configuration(
            self.reversal_source_value, self.pair_column_values, self.reversal_column_values, self.numeric_value)
        logger.info("successfully added new gp transaction reversal config.")

    @then(u'I delete existing values of newly created gp config, check statuses and modify it by adding new values')
    def step_impl(self):
        self.reversal_source_value = self.td_set['reversal_source_value']
        self.pair_column_values = self.td_set['pair_column_values']
        self.reversal_column_values = self.td_set['reversal_column_values']
        self.GPConfigPage.delete_pair_rev_values(
            self.reversal_source_value, self.pair_column_values, self.reversal_column_values)
        self.GPConfigPage.validate_statuses_pair_and_rev_values(
            self.pair_column_values, self.reversal_column_values)
        self.GPConfigPage.modify_pair_rev_values(
            self.reversal_source_value, self.pair_column_values, self.reversal_column_values)
        logger.info(
            "Successfully deleted pair and reversal value, validated status and modified the values")

    @when(u'I upload a rebate file from upload screen')
    def step_impl(self):
        self.GPConfigPage = GPConfigPage(self.driver)
        self.source_file_name = self.td_set['source_file_name']
        self.file_type = self.td_set['file_type']
        self.file_to_upload = self.td_set['File To Upload']
        self.file_to_upload_path = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_to_upload))
        self.GPConfigPage.upload_rebate_file(
            self.source_file_name, self.file_type, self.file_to_upload_path, self.file_to_upload)
        logger.info("Successfully uploaded a file named: " + self.file_to_upload)

    @then('I verify view data and database of uploaded file for that source and period')
    def step_impl(self):
        self.GPConfigPage = GPConfigPage(self.driver)
        self.main_page = MainPage(self.driver)
        self.client_id_query = self.td_set['Client_id_query']
        self.data_count_query = self.td_set['Data_count_query']
        self.sql_query_2 = self.td_set['Sql_query_2']
        self.period_month = self.td_set['period_month']
        self.client_id = self.main_page.get_client_id(self.client_id_query)
        self.rebate_transfer = RebateTransferPage(self.driver)
        self.client_id = self.rebate_transfer.get_count_from_DB(self.client_id)
        logger.info("Client id is: "+self.client_id)
        self.GPConfigPage.validate_rebate_file_data_from_db(
            self.client_id, self.data_count_query, self.sql_query_2, self.period_month)

    @then('I validate transaction reversal job')
    def step_impl(self):
        self.GPConfigPage = GPConfigPage(self.driver)
        self.reversal_source_name = self.td_set['reversal_source_name']
        self.sql_query_3 = self.td_set['Sql_query_3']
        self.GPConfigPage.perform_validate_transaction_reversal_job(
            self.sql_query_3, self.reversal_source_name)
        logger.info("Successfully validated job id and status in db and ui")
