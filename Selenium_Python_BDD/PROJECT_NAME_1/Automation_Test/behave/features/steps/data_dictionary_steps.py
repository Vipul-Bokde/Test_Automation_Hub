from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.data_dictionary_page import DataDictionaryPage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login

class dataDictionary(EnvironmentSetup):

    @given(u'I select data dictionary option under client from the burger menu')
    def step_impl(self):
        self.DataDictionary = DataDictionaryPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for new dataDictionary class in data_Dictionary steps")
        self.DataDictionary.select_global_from_burger_menu()
        logger.info("Click on data dictionary under the global menu")

    @given(u'Click on new table and create a new table')
    def step_impl(self):
        self.DataDictionary.click_on_new_table()
        logger.info("Click on new table button")

    @when(u'Select details for new table')
    def step_impl(self):
        self.Table_Source = self.td_set['Table_Source']
        self.Table_Name = self.td_set['Table_Name']
        self.Table_Value = self.td_set['Table_Value']
        self.DataDictionary.create_new_table(self.Table_Source, self.Table_Name, self.Table_Value)
        
    @then(u'click on submit')
    def step_impl(self):
        self.DataDictionary.click_on_submit()
        self.login.close_browser()


# Add new column
    @given(u'Select any table row')
    def step_impl(self):
        self.Table_Name = self.td_set['Table_Name']
        self.DataDictionary.select_added_table(self.Table_Name)

    @when(u'Click on new column and select details')
    def step_impl(self):
        self.Column_Name = self.td_set['Column_Name']
        self.Column_Value = self.td_set['Column_Value']
        self.DataDictionary.create_new_column(self.Column_Name, self.Column_Value)
        logger.info("New column details entered successfully")

    @then(u'click on submit button')
    def step_impl(self):
        self.DataDictionary.click_on_submit_button()
        self.login.close_browser()

# Delete added column
    @given(u'Select table row to delete column')
    def step_impl(self):
        self.Table_Name = self.td_set['Table_Name']
        self.DataDictionary.select_added_table(self.Table_Name)

    @when(u'Select column to delete')
    def step_impl(self):
        self.Column_Name = self.td_set['Column_Name']
        self.DataDictionary.select_added_column(self.Column_Name)

    @then(u'Click on column delete')
    def step_impl(self):
        self.DataDictionary.click_on_column_delete()
        self.login.close_browser()


# Delete added table
    @when(u'Select added table row')
    def step_impl(self):
        self.Table_Name = self.td_set['Table_Name']
        self.DataDictionary.select_added_table_to_delete(self.Table_Name)

    @then(u'Click on delete')
    def step_impl(self):
        self.DataDictionary.click_on_delete()
        logger.info("Table Deleted")
        self.login.close_browser()



   