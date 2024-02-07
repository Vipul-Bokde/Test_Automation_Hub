from libraries.environment_setup import EnvironmentSetup
from GP.pages.main_page import MainPage
from libraries import forms
from GP.utilities.logs_util import logger
from selenium.webdriver.common.by import By
import allure
class DeletePriceTypePage(EnvironmentSetup):
    
    
    # locators
    burger_menu = "//*[@id='header-right']/div[1]/button"
    price_type_editor = "//*[@id='header-right']/div[1]/ul/li[7]"
    rowxpath_price_type = "//*[@id='page-container']/price-types/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div"
    delete_btn = "//div[@id='price-type-new']/button[@id='price-type-delete-btn']"
    price_type_wait= "//div[@row-index='0']/div[@col-id='name']"

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

    def select_a_price_type_editor_from_burguer_menu(self):
        self.main.select_gp_option('PRICE TYPE EDITOR', sub_item=None)
        self.main.screen_load_time('PRICE TYPE EDITOR Screen')
    
    def delete_price_type(self,price_type):
        self.price_type = price_type
        self.price_type_name_list = []
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.price_type_wait,"Price Type wait element not found on Webpage in given wait time.")
        self.price_type_name_list = self.driver.find_elements_by_xpath(self.rowxpath_price_type)
        logger.info(self.price_type_name_list)
        logger.info(len(self.price_type_name_list))
        self.list_length =len(self.price_type_name_list)
        for i in range(self.list_length,1,-1):
            logger.info("Inside for loop",)
            self.price_name_list = "//*[@id='page-container']/price-types/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div["+str(i)+"]/div[3]"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.price_name_list)
            if self.column_text == self.price_type:
                logger.info("Price type found")
                self.Checkbox_list = "//*[@id='page-container']/price-types/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div["+str(i)+"]/div[1]/span/span[2]/span[2]"
                forms.check_checkbox(self,'XPATH',self.Checkbox_list)
                allure.attach("Price Type to Delete is: "+self.column_text,attachment_type=allure.attachment_type.TEXT)
                break
   
    def click_on_delete_btn(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.delete_btn,"Delete button element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.delete_btn)
        self.driver.execute_script("$(arguments[0]).click();", element)
        allure.attach("Clicked on Delete Button",attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time('CLIENT->JOINS Screen')
    


     
