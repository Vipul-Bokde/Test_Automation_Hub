from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.view_data_page import ViewDataPage
import allure
from allure_commons.types import AttachmentType
import time
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login

class viewdata(EnvironmentSetup):

    @given(u'I select Viewdata from the burger menu')
    def step_impl(self):
        self.ViewData = ViewDataPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for ViewData class in view step")
        self.ViewData.select_product_from_burger_menu()
        logger.info("Select view data from burger menu")


    @when(u'Click on dropdown button and select data type from dropdown')
    def step_impl(self):
        self.ViewData = ViewDataPage(self.driver)
        self.Pages = self.td_set['Pages']
        logger.info("Pages value is",self.Pages)
        self.Data = self.td_set['Data']
        logger.info("Data name is",self.Data)
        self.ViewData.click_on_view_data_dropdown(self.Pages,self.Data)
        
        
    @then(u'I see the data record in Viewdata page and click on download button')
    def step_impl(self):
        self.ViewData = ViewDataPage(self.driver)
        self.ViewData.click_on_product_download_button()
        self.login.close_browser()

        