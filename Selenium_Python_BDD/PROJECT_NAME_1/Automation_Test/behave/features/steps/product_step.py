from GP.pages.approvals_page import ApprovalsPage
from pydoc import locate
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.product_page import ProductPage
from GP.utilities.logs_util import logger
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
 

class Product(EnvironmentSetup):
    
    @when(u'I select Upload from burger menu')
    def step_impl(self):  
        self.Product = ProductPage(self.driver)
        self.login = Login(self.driver)
        self.Product.select_upload_from_burguer_menu()
    
    @when(u'I upload product file and get ndc11 value')
    def step_impl(self,):  
        self.Product.click_on_upload_button()
        self.Product.select_file_type()
        self.Product.click_on_checkbox()
        self.file_name = self.td_set['File_to_Upload']
        self.file_to_upload = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_name))
        self.Product.upload_file(self.file_to_upload)
        self.Product.click_on_submit_button()
        self.upload_value_list = self.Product.get_ndc11_and_product_name()
        
    @when(u'I log out')
    def step_impl(self):
        self.Product = ProductPage(self.driver)
        self.Product.log_out()
        self.login.close_browser()
        
    @when(u'I Approve Product')
    def step_impl(self):
        self.Approvals = ApprovalsPage(self.driver)
        self.Approvals.select_approval_from_burger_menu()
        self.Approval_Client = self.td_set['Client']
        self.Approvals.select_client_from_approvals(self.Approval_Client)
        self.Approvals.select_type_from_approvals("Product")
        self.Approvals = ApprovalsPage(self.driver)
        logger.info(self.upload_value_list[0])
        logger.info(self.upload_value_list[1])
        self.Approvals.select_price_type_name(self.upload_value_list[1],"Product",self.upload_value_list[0],self.upload_value_list[0])
        self.Approvals.click_on_approve_button()

    @when(u'I goes to changes tab')
    def step_impl(self):
        self.Product = ProductPage(self.driver)
        self.Product.goto_changes_tab(self.upload_value_list[0])   

    @when(u'I validate changes tab')     
    def step_impl(self):
        self.Product = ProductPage(self.driver)
        self.approved_by = self.td_set['UserID_2']
        self.modified_by = self.td_set['UserID']
        self.Product.validate_changes_tab(self.approved_by,self.modified_by)
        self.login.close_browser()
