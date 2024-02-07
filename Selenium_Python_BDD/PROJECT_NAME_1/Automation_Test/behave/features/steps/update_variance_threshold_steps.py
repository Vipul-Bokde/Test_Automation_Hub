import time
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.update_variance_threshold_page import UpdateVarianceThresholdPage
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login

class UpdateVarianceThreshold(EnvironmentSetup):
   
    @when(u'I click on Price type and select Rules Tab')
    def step_impl(self):
        self.login = Login(self.driver)
        self.updatevariancethreshold =UpdateVarianceThresholdPage(self.driver)
        self.price_type = self.td_set['Price_Type']
        self.updatevariancethreshold.click_on_price_type(self.price_type)
        self.updatevariancethreshold.click_on_rules_tab()
        logger.info("I click on Price type and select Rules Tab")

    @when(u'I update threshold')
    def step_impl(self):
        self.updatevariancethreshold.update_threshold()
        logger.info("I update threshold")

    @then(u'I click on submit')
    def step_impl(self):
        self.updatevariancethreshold.click_on_submit()
        logger.info("I click on submit")
        self.login.close_browser()
