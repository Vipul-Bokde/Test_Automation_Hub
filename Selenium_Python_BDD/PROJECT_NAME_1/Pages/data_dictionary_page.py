# from _typeshed import Self
from libraries.environment_setup import EnvironmentSetup
from selenium.webdriver.common.by import By
from GP.pages.main_page import MainPage
from libraries import mouse, forms
from GP.utilities.logs_util import logger
from libraries import mouse
from libraries import forms_rfn, mouse_rfn
from selenium.webdriver.common.by import By
import allure

class DataDictionaryPage(EnvironmentSetup):
    #locators
    new_table = "//div[@id='table-new']/button[@class='btn btn-secondary']"
    delete_table = "//div[@id='table-new']/button[@class='btn btn-danger']" 
    # NEW_TABLE = (By.ID, "table-new-btn")
    TRANSACTION_DATA = "//*[@id='table-transactional']"  
    SOURCE = (By.ID, "table-source") 
    NAME = (By.ID, "table-name") 
    VALUE = (By.ID, "table-value")
    SUBMIT_BUTTON = "//div[@class='sparq-modal-footer']/button[@id='table-submit-btn']"
    NEW_COLUMN = (By.ID, "column-new-btn")
    new_column = "//div[@id='column-new']/button[@id='column-new-btn']"
    rowxpath_3 = "//*[@id='page-container']/table-dictionary/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div"
    # DELETE_TABLE = (By.ID, "table-delete-btn")
    COLUMN_NAME = (By.ID, "column-name")
    COLUMN_VALUE = (By.ID, "column-value")
    AGGREGRATE = "//*[@id='column-aggregate']"
    VALIDATION_KEY = "//*[@id='column-validation-key']"
    ALWS_IN_BKT = "//*[@id='column-in-buckets']"
    SUBMIT_BUTTON_COLUMN = (By.ID, "column-submit-btn")
    column_tablexpath = "//div[@class='ag-center-cols-container']/div[@role='row']"
    column_name = "//div[@row-index='0']/div[@col-id='name']"
    DELETE_COLUMN = "//div[@id='column-new']/button[@id='column-delete-btn']"
    wait = "//h3[@class='display-4 text-center']"
    
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

    def select_global_from_burger_menu(self):
        self.main.select_gp_option('DATA DICTIONARY', sub_item=None)
        self.main.screen_load_time('DATA DICTIONARY')
        allure.attach("User see select data dictionary menu : ",attachment_type=allure.attachment_type.TEXT)
        
    def click_on_new_table(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.new_table,"New table element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.new_table)
        self.driver.execute_script("$(arguments[0]).click();", element)

    def create_new_table(self, Source, Name, Value):
        self.Source = Source
        self.Name = Name
        self.Value = Value
        logger.info(Source)
        forms.check_checkbox(self, "XPATH", self.TRANSACTION_DATA)
        forms_rfn.select_option_by_text(self, self.SOURCE, self.Source)
        allure.attach("Table Source is : "+self.Source,attachment_type=allure.attachment_type.TEXT)
        forms_rfn.enter_text_on_element(self, self.NAME, self.Name)
        allure.attach("Table Name is : "+self.Name,attachment_type=allure.attachment_type.TEXT)
        forms_rfn.enter_text_on_element(self, self.VALUE, self.Value)
        allure.attach("Table Value is : "+self.Value,attachment_type=allure.attachment_type.TEXT)

    def click_on_submit(self):
        mouse.click_on_element(self, "XPATH",self.SUBMIT_BUTTON)
        self.main.screen_load_time('DATA DICTIONARY=>Table Submit')
        allure.attach("Table is Created.",attachment_type=allure.attachment_type.TEXT)

# Add new column

    def select_added_table(self,Table_Name):
        self.Table_Name = Table_Name
        self.list_of_elem = []
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.new_table,"New Table element not found on Webpage in given wait time.")
        self.list_of_elem = self.driver.find_elements_by_xpath(self.rowxpath_3)
        logger.info("Element lisyt is:")
        logger.info(self.list_of_elem)
        logger.info(len(self.list_of_elem))
        self.listLength = len(self.list_of_elem)
        for i in range(self.listLength, 1, -1):
            self.TableList = "//*[@id='page-container']/table-dictionary/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div["+str(i)+"]/div[4]"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.TableList)
            logger.info("return value:")
            logger.info(self.column_text)
            if self.column_text == self.Table_Name:
                # self.ROWTOCLICK = (By.XPATH, self.TableList)
                mouse.double_click_on_element(self, "XPATH", self.TableList)
                break

    def create_new_column(self, Column_Name, Column_Value):
        MainPage.wait_until_element_is_present(self, 60,By.XPATH,self.new_column,"New Column element not found on Webpage in given wait time.")
        mouse_rfn.click_on_element(self, self.NEW_COLUMN)
        self.Column_Name = Column_Name
        self.Column_Value = Column_Value
        forms_rfn.enter_text_on_element(self, self.COLUMN_NAME, self.Column_Name)
        allure.attach("Column Name is : "+self.Column_Name,attachment_type=allure.attachment_type.TEXT)
        forms_rfn.enter_text_on_element(self, self.COLUMN_VALUE, self.Column_Value)
        allure.attach("Column Value is : "+self.Column_Value,attachment_type=allure.attachment_type.TEXT)
        forms.check_checkbox(self, "XPATH", self.AGGREGRATE)
        # forms.check_checkbox(self, "XPATH", self.VALIDATION_KEY)
        # forms.check_checkbox(self, "XPATH", self.ALWS_IN_BKT)

    def click_on_submit_button(self):
        mouse_rfn.click_on_element(self, self.SUBMIT_BUTTON_COLUMN)
        self.main.screen_load_time('Column Created')
        allure.attach("Column is Created.",attachment_type=allure.attachment_type.TEXT)

# Delete column
    def select_added_column(self,Column_Name):
        self.Column_Name = Column_Name
        self.list_of_elem = []
        self.main.screen_load_time('Table->Column')
        self.list_of_elem = self.driver.find_elements_by_xpath(self.column_tablexpath)
        logger.info("Element list is:")
        logger.info(self.list_of_elem)
        self.listLength = len(self.list_of_elem)
        logger.info(self.listLength)
        for i in range(0, self.listLength):
            logger.info(i)
            self.column_list = "//div[@class='ag-center-cols-viewport']//div[@row-id="+str(i)+"]/div[@col-id='name']"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.column_list)
            logger.info("return value:")
            logger.info(self.column_text)
            if self.column_text == self.Column_Name:
                self.ROWTOCLICK = "//div[@class='ag-center-cols-container']/div[@row-id="+str(i)+"]//span[@class='ag-selection-checkbox']"
                forms.check_checkbox(self, "XPATH", self.ROWTOCLICK)
                allure.attach("Deleted column Value is : "+self.column_text,attachment_type=allure.attachment_type.TEXT)
                break

    def click_on_column_delete(self):
        element = self.driver.find_element_by_xpath(self.DELETE_COLUMN)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Table->Column Delete')
        allure.attach("Column Deleted :",attachment_type=allure.attachment_type.TEXT)

# Delete added table
    def select_added_table_to_delete(self,Table_Name):
        self.Table_Name = Table_Name
        self.list_of_elem = []
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.new_table,"New Table element not found on Webpage in given wait time.")
        self.list_of_elem = self.driver.find_elements_by_xpath(self.rowxpath_3)
        logger.info("Element list is:")
        logger.info(self.list_of_elem)
        logger.info(len(self.list_of_elem))
        self.listLength = len(self.list_of_elem)
        for i in range(self.listLength, 1, -1):
            self.TableList = "//*[@id='page-container']/table-dictionary/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div["+str(i)+"]/div[4]"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.TableList)
            logger.info("return value:")
            logger.info(self.column_text)
            if self.column_text == self.Table_Name:
                self.ROWTOCLICK = "//*[@id='page-container']/table-dictionary/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div["+str(i)+"]/div[1]/span/span[1]/span[2]"
                forms.check_checkbox(self, "XPATH", self.ROWTOCLICK)
                allure.attach("Deleted Table Value is : "+self.column_text,attachment_type=allure.attachment_type.TEXT)
                break

    def click_on_delete(self):
        element = self.driver.find_element_by_xpath(self.delete_table)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('DATA DICTIONARY-Table Delete')
        allure.attach("Table Deleted :",attachment_type=allure.attachment_type.TEXT)



    


        