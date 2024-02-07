from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.approvals_page import ApprovalsPage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login
class Approvals(EnvironmentSetup):

    @when(u'I select Approvals from burger menu')
    def step_impl(self):
        self.Approvals = ApprovalsPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for ApprovalsPage class in Approvals steps")
        self.Approvals.select_approval_from_burger_menu()
        logger.info("Select Approvals from burger menu")

    @when(u'I select client and type from dropdown')
    def step_impl(self): 
        self.Approval_Client = self.td_set['Approval_Client']
        self.Type = self.td_set['Type']
        self.Approvals.select_client_from_approvals(self.Approval_Client)
        logger.info("Select Client from dropdown")
        self.Approvals.select_type_from_approvals(self.Type)
        logger.info("Select Type from dropdown")

    @then(u'Select given value and approve')
    def step_impl(self):
        logger.info("Select given value and approve")
        self.Price_type_name = self.td_set['price_type_name']
        self.ndc_11_xl = self.td_set['NDC11']
        self.unit_price_xl  = self.td_set['Unit Price NDC11']
        self.Approvals.select_price_type_name(self.Price_type_name,self.Type,self.ndc_11_xl,self.unit_price_xl)
        self.Approvals.click_on_approve_button()
        self.login.close_browser()

    @then(u'Select price type and reject')
    def step_impl(self):
        logger.info("Select price type and reject")
        self.Price_type_name_reject = self.td_set['price_type_name']
        self.ndc_11_xl = self.td_set['NDC11']
        self.unit_price_xl  = self.td_set['Unit Price NDC11']
        self.Approvals.select_price_type_name(self.Price_type_name_reject,self.Type,self.ndc_11_xl,self.unit_price_xl)
        self.Approvals.click_on_reject_button()
        self.login.close_browser()
