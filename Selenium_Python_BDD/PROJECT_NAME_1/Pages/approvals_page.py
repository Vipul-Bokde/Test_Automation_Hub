from libraries.environment_setup import EnvironmentSetup
from GP.pages.main_page import MainPage
from libraries import mouse, forms, locators,forms_rfn
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
from selenium.webdriver.common.by import By
import GP.utilities.Repo as Repo
import allure
from libraries import generics
import time

class ApprovalsPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        self.column = "(//div[@class='ag-header-container']//div[@col-id='name0'])[1]"
        self.client = "//*[@id='page-container']/approval/div[2]/div/div/div[1]/select"
        self.type = "//*[@id='page-container']/approval/div[2]/div/div/div[2]/select"
        self.Approval_Name_Row = "//div[@role='row']/diff-renderer/div"
        self.Approve_button = "(//button[@class='btn btn-success'][@id='approve-btn'])[3]"
        self.Reject_button = "(//button[@class='btn btn-danger'][@id='reject-btn'])"
        self.btn_approve = "//button[@class='btn btn-success'][contains(.,'Approve')]"

    def select_approval_from_burger_menu(self):
        time.sleep(2)
        self.main.select_gp_option('APPROVALS')
        # self.main.screen_load_time('APPROVALS')
        allure.attach("User can select approvals from menu : ",attachment_type=allure.attachment_type.TEXT)

    def select_client_from_approvals(self, Approval_Client):
        self.main.screen_load_time('APPROVALS')
        forms.select_option_by_text(self, 'XPATH', self.client, Approval_Client)
        self.main.screen_load_time('APPROVALS')
        allure.attach("User can select client as: "+Approval_Client,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Approval Client")

    def select_type_from_approvals(self, Type):
        forms.select_option_by_text(self,'XPATH', self.type, Type)
        self.main.screen_load_time('APPROVALS->Type')
        allure.attach("User can select client type as : "+Type,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Type")

    def select_price_type_name(self, price_type_name, Type, ndc_11_xl, unit_price_xl):
        self.pricetypename_xl = price_type_name
        self.Type = Type
        self.ndc_11_xl = ndc_11_xl
        self.unit_price_xl = unit_price_xl
        self.price_type_name_list = []
        self.price_type_name_list = self.driver.find_elements_by_xpath(self.Approval_Name_Row)
        self.list_length = len(self.price_type_name_list)
        if self.Type == "GP Price Type":
            for i in range( 1, self.list_length+1):
                allure.attach("Loop is:"+ str(i),attachment_type=allure.attachment_type.TEXT)
                self.price_list = "(//*[@id='contractName'])["+str(i)+"]"
                mouse.scroll_to_element(self,"XPATH",self.price_list)
                self.pricetypename_ui = forms.get_text_on_element(self, "XPATH", self.price_list)
                self.pricetypename_ui = self.pricetypename_ui.upper()
                logger.info('pricetypename_ui '+self.pricetypename_ui)
                allure.attach("Price Type name on UI is : "+self.pricetypename_ui,attachment_type=allure.attachment_type.TEXT)
                self.pricetypename_xl = self.pricetypename_xl.upper()
                logger.info('pricetypename_xl '+self.pricetypename_xl)
                allure.attach("Price Type name in XL is : "+self.pricetypename_xl,attachment_type=allure.attachment_type.TEXT)
                if self.pricetypename_ui == self.pricetypename_xl:
                    self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"
                    logger.info("Price type name found")
                    forms.check_checkbox(self, "XPATH", self.Checkbox)
                    logger.info("Checkbox Checked")
                    allure.attach("Checkbox is Checked",attachment_type=allure.attachment_type.TEXT)
                    break
        elif self.Type == "Pricing":
            logger.info(self.list_length)
            self.pricing_name_initial = 1
            self.pricing_name_initial_new = 1
            for i in range( 1, self.list_length+1):
                    logger.info(str(i))
                    allure.attach("Loop is : "+str(i),attachment_type=allure.attachment_type.TEXT)
                    self.pricing_status = "(//div[@class='ag-full-width-container']/div/diff-renderer//div/span[@class='diff-title'])["+str(i)+"]"
                    self.status = forms.get_text_on_element(self, "XPATH",self.pricing_status)
                    if self.status == "Pricing (Updated)":
                        logger.info('status '+self.status)
                        logger.info(str(self.pricing_name_initial))
                        self.price_type = "(//div[@row-index='0']/div[@col-id='new']/diff-field-renderer)["+str(self.pricing_name_initial)+"]"
                        self.ndc11 = "(//div[@row-index='1']/div[@col-id='new']/diff-field-renderer)["+str(self.pricing_name_initial)+"]"
                        self.price = "(//div[@row-index='3']/div[@col-id='new']/diff-field-renderer)["+str(self.pricing_name_initial)+"]"
                        mouse.scroll_to_element(self,"XPATH",self.price_type)
                        self.price_type_ui =forms.get_text_on_element(self, "XPATH",self.price_type)
                        self.price_type_ui = self.price_type_ui.upper()
                        self.ndc_name_ui =forms.get_text_on_element(self, "XPATH",self.ndc11)
                        self.price_ui =forms.get_text_on_element(self, "XPATH",self.price)
                        logger.info('price_type_ui '+self.price_type_ui)
                        allure.attach("Price Type name on UI is : "+self.price_type_ui,attachment_type=allure.attachment_type.TEXT)
                        self.pricetypename_xl = self.pricetypename_xl.upper()
                        logger.info('price_type_xl '+self.pricetypename_xl)
                        allure.attach("Price Type name in XL is : "+self.pricetypename_xl,attachment_type=allure.attachment_type.TEXT)
                        logger.info('ndc_name_ui '+self.ndc_name_ui)
                        allure.attach("NDC11 name on UI is : "+self.ndc_name_ui,attachment_type=allure.attachment_type.TEXT)
                        logger.info('ndc_11_xl '+self.ndc_11_xl)
                        allure.attach("NDC11 name in XL is : "+self.ndc_11_xl,attachment_type=allure.attachment_type.TEXT)
                        logger.info('price_ui '+self.price_ui)
                        allure.attach("Price on UI is : "+self.price_ui,attachment_type=allure.attachment_type.TEXT)
                        logger.info('price_xl '+self.unit_price_xl)
                        allure.attach("Price in XL is : "+self.unit_price_xl,attachment_type=allure.attachment_type.TEXT)
                        if self.price_type_ui == self.pricetypename_xl and self.ndc_name_ui == self.ndc_11_xl and self.price_ui == self.unit_price_xl:
                            self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"
                            forms.check_checkbox(self, "XPATH", self.Checkbox)
                            allure.attach("Checkbox is Checked",attachment_type=allure.attachment_type.TEXT)
                            logger.info("Checkbox Checked")
                            break
                        else:
                            self.pricing_name_initial = self.pricing_name_initial + 1                    
                    elif self.status == "Pricing (New)":
                            logger.info('status '+self.status)
                            logger.info(str(self.pricing_name_initial_new))
                            self.price_type = "(//div[@row-index='0']/div[@col-id='value0'])["+str(self.pricing_name_initial_new)+"]"
                            self.ndc11 = "(//div[@row-index='0']/div[@col-id='value1'])["+str(self.pricing_name_initial_new)+"]"
                            self.price = "(//div[@row-index='0']/div[@col-id='value3'])["+str(self.pricing_name_initial_new)+"]"
                            mouse.scroll_to_element(self,"XPATH",self.price_type)
                            self.price_type_ui =forms.get_text_on_element(self, "XPATH",self.price_type)
                            self.price_type_ui = self.price_type_ui.upper()
                            self.ndc_name_ui =forms.get_text_on_element(self, "XPATH",self.ndc11)
                            self.price_ui =forms.get_text_on_element(self, "XPATH",self.price)
                            logger.info('price_type_ui '+self.price_type_ui)
                            self.pricetypename_xl = self.pricetypename_xl.upper()
                            allure.attach("Price Type name on UI is : "+self.price_type_ui,attachment_type=allure.attachment_type.TEXT)
                            logger.info('price_type_xl '+self.pricetypename_xl)
                            allure.attach("Price Type name in XL is : "+self.pricetypename_xl,attachment_type=allure.attachment_type.TEXT)
                            logger.info('ndc_name_ui '+self.ndc_name_ui)
                            allure.attach("NDC11 name on UI is : "+self.ndc_name_ui,attachment_type=allure.attachment_type.TEXT)
                            logger.info('ndc_11_xl '+self.ndc_11_xl)
                            allure.attach("NDC11 name in XL is : "+self.ndc_11_xl,attachment_type=allure.attachment_type.TEXT)
                            logger.info('price_ui '+self.price_ui)
                            allure.attach("Price on UI is : "+self.price_ui,attachment_type=allure.attachment_type.TEXT)
                            logger.info('price_xl '+self.unit_price_xl)
                            allure.attach("Price in XL is : "+self.unit_price_xl,attachment_type=allure.attachment_type.TEXT)
                            if self.price_type_ui == self.pricetypename_xl and self.ndc_name_ui == self.ndc_11_xl and self.price_ui == self.unit_price_xl:
                                self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"
                                forms.check_checkbox(self, "XPATH", self.Checkbox)
                                allure.attach("Checkbox is Checked",attachment_type=allure.attachment_type.TEXT)
                                logger.info("Checkbox Checked")
                                break
                            else:
                                self.pricing_name_initial_new = self.pricing_name_initial_new + 1                    
        elif self.Type == "Product":
            logger.info(self.list_length)
            self.prod_name_initial = 1
            self.prod_name_initial_new = 1
            for i in range( 1, self.list_length+1):
                    allure.attach("Loop is : "+str(i),attachment_type=allure.attachment_type.TEXT)
                    logger.info(str(i))
                    self.product_status = "(//div[@class='ag-full-width-container']/div/diff-renderer//div/span[@class='diff-title'])["+str(i)+"]"
                    self.status = forms.get_text_on_element(self, "XPATH",self.product_status)
                    if self.status == "Product (Updated)":
                        logger.info('status '+self.status)
                        logger.info(str(self.prod_name_initial))
                        self.ndc_name = "(//div[@row-index='0']/div[@col-id='new'])["+str(self.prod_name_initial)+"]"
                        mouse.scroll_to_element(self,"XPATH",self.ndc_name)
                        self.ndc_name_ui =forms.get_text_on_element(self, "XPATH",self.ndc_name)   
                        logger.info('ndc_name_ui '+self.ndc_name_ui)
                        allure.attach("NDC11 on UI is : "+self.ndc_name_ui,attachment_type=allure.attachment_type.TEXT)
                        logger.info('ndc_11_xl '+self.ndc_11_xl)
                        allure.attach("NDC11 in XL is : "+self.ndc_11_xl,attachment_type=allure.attachment_type.TEXT)
                        if self.ndc_name_ui == self.ndc_11_xl:
                            self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"
                            forms.check_checkbox(self, "XPATH", self.Checkbox)
                            logger.info("Checkbox Checked")
                            allure.attach("Checkbox is Checked",attachment_type=allure.attachment_type.TEXT)
                            break
                        else:
                            self.prod_name_initial = self.prod_name_initial + 1                    
                    elif self.status == "Product (New)":
                            logger.info('status '+self.status)
                            logger.info(str(self.prod_name_initial_new))
                            self.ndc_name = "(//div[@row-index='0']/div[@col-id='value0'])["+str(self.prod_name_initial_new)+"]"
                            self.product_name = "(//div[@row-index='1']/div[@col-id='value1'])["+str(self.prod_name_initial_new)+"]"
                            mouse.scroll_to_element(self,"XPATH",self.ndc_name)
                            self.ndc_name_ui =forms.get_text_on_element(self, "XPATH",self.ndc_name)
                            self.product_name_ui =forms.get_text_on_element(self, "XPATH",self.product_name)
                            logger.info('product_name_ui:'+self.product_name_ui)
                            allure.attach("Product name on UI is : "+self.product_name_ui,attachment_type=allure.attachment_type.TEXT)
                            logger.info('product name xl:'+self.pricetypename_xl)
                            allure.attach("Product name in XL is : "+self.pricetypename_xl,attachment_type=allure.attachment_type.TEXT)
                            logger.info('ndc_11_ui '+self.ndc_name_ui)
                            allure.attach("NDC11 on UI is : "+self.ndc_name_ui,attachment_type=allure.attachment_type.TEXT)
                            logger.info('ndc_11_xl '+self.ndc_11_xl)
                            allure.attach("NDC11 in XL is : "+self.ndc_11_xl,attachment_type=allure.attachment_type.TEXT)
                            if self.ndc_name_ui == self.ndc_11_xl and self.product_name_ui == self.pricetypename_xl:
                                self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"   
                                forms.check_checkbox(self, "XPATH", self.Checkbox)
                                allure.attach("Checkbox is Checked",attachment_type=allure.attachment_type.TEXT)
                                logger.info("Checkbox Checked")
                                break
                            else:
                                self.prod_name_initial_new = self.prod_name_initial_new + 1
            
    def click_on_approve_button(self):
        element = self.driver.find_element_by_xpath(self.Approve_button)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('APPROVALS->Approve')

    def click_on_reject_button(self):
        element = self.driver.find_element_by_xpath(self.Reject_button)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('APPROVALS->Reject')
        
    """Author : Sadiya Kotwal
       Description : This method verify the selected client from dropdown
       Arguments : client_name(EG: client_name="Horizon Pharma")
       Returns : NA""" 
    def verify_client_name(self,client_name):
        self.client_name = client_name
        self.bln_flag=False
        self.txt_client_name = "(//table/child::tr/child::td[2][text()='"+self.client_name+"'])[1]"
        self.bln_flag = locators.element_is_displayed(self,"XPATH", self.txt_client_name)
        if self.bln_flag == True:
            allure.attach("User is see selected client as: "+self.client_name,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the client name"
    
    """Author : Sadiya Kotwal
       Description : This method verify the selected client type dropdown
       Arguments : client_type(EG: client_type="GP Price Type")
       Returns : NA""" 
    def verify_client_type(self,client_type):
        self.client_type = client_type
        self.bln_flag=False
        self.txt_client_type = "(//span[contains(text(),'"+self.client_type+"')])[1]"
        self.bln_flag = locators.element_is_displayed(self,"XPATH", self.txt_client_type)
        if self.bln_flag == True:
            allure.attach("User is see selected client type as: "+self.client_type,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see the client type"

    """Author : Sadiya Kotwal
       Description : This method clicks on approve button from approvals page
                    Screen: Approvals 
       Arguments : 
       Returns : NA"""
    def click_on_approve_button_from_approvals(self):
        #mouse.click_on_element(self, "XPATH", self.btn_approve)
        mouse.click_action_on_element(self, "XPATH", self.btn_approve)
        self.main.screen_load_time('APPROVALS')
        allure.attach("User can see click on approve button: ",attachment_type=allure.attachment_type.TEXT)

    def verify_client_dropdown_from_approvals(self):
        locators.element_is_displayed(self,"XPATH", self.client)
        allure.attach("User can verify client dropdown : ",attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Approval Client")

    def verify_type_dropdown_from_approvals(self):
        locators.element_is_displayed(self,"XPATH", self.type)
        allure.attach("User can verify client type dropdown : ",attachment_type=allure.attachment_type.TEXT)
