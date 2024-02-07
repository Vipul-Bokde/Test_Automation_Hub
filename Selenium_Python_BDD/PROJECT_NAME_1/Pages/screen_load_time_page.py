from libraries.environment_setup import EnvironmentSetup
from selenium.webdriver.support import expected_conditions as EC
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from GP.utilities.logs_util import logger
import allure
from allure_commons.types import AttachmentType
import time
import os
import datetime
from selenium.webdriver.common.by import By


class Load_Time_Page(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        
        self.template_name = "//div[@row-index='0']/div[@col-id='name']"
        self.client_price_type = "//div[@row-index='0']/div[@col-id='price_type']"
        self.client_product = "//div[@row-index='0']/div[@col-id='product_name']"
        self.medicaid = "//ul[@class='nav nav-tabs']/li/a[@href='#medicaid']"
        self.ubr = "//ul[@class='nav nav-tabs']/li/a[@href='#managedcare']"
        self.gp = "//ul[@class='nav nav-tabs']/li/a[@href='#gp']"  
        self.change = "//ul[@class='nav nav-tabs']/li/a[@href='#change']"   
        self.username = "//div[@row-index='0']/div[@col-id='username']"   
        self.Resources = "(//ul[@class='nav nav-tabs']/li/a)[2]"
        self.services = "(//ul[@class='nav nav-tabs']/li/a)[2]"
        self.identifiers = "(//ul[@class='nav nav-tabs']/li/a)[3]"
        self.rule = "(//ul[@class='nav nav-tabs mt-3 ml-2']/li/a)[2]"
        self.output = "(//ul[@class='nav nav-tabs mt-3 ml-2']/li/a)[3]"
        self.changes = "(//ul[@class='nav nav-tabs mt-3 ml-2']/li/a)[4]"
        self.file_name = "//div[@row-index='0']/div[@col-id='filename']"
        self.tracker = "//div[@id='header-right']/button[@id='gp-tracker-btn']"
        self.Page = "//div[@id= 'output-controls']/div[1]/select"
        self.DataType = "//div[@id= 'output-controls']/div[3]/select"

    def select_template_name(self):
        mouse.click_on_element(self, 'XPATH',self.template_name)
        self.main.screen_load_time('Global->File Template->Template Screen')
    
    def select_global_price_type(self):
        self.main.select_gp_option('GLOBAL', sub_item='PRICE TYPES')
        self.main.screen_load_time('Global->Price Type')
    
    def select_screens_under_client(self):
        self.main.select_gp_option('CLIENT', sub_item='JOINS')
        self.main.screen_load_time('CLIENT->JOINS')
        self.main.select_gp_option('CLIENT', sub_item='LABELERS')
        self.main.screen_load_time('CLIENT->LABELERS')
        self.main.select_gp_option('CLIENT', sub_item='PRICING')
        self.main.screen_load_time('CLIENT->PRICING')
        mouse.click_on_element(self, 'XPATH',self.client_price_type)
        self.main.screen_load_time('CLIENT->PRICING->General')
        self.main.select_gp_option('CLIENT', sub_item='PRODUCTS')
        self.main.screen_load_time('CLIENT->PRODUCTS')
        mouse.click_on_element(self, 'XPATH',self.client_product)
        self.main.screen_load_time('CLIENT->PRODUCT->General')
        mouse.click_on_element(self, 'XPATH',self.medicaid)
        self.main.screen_load_time('CLIENT->PRODUCT->Medicaid')
        mouse.click_on_element(self, 'XPATH',self.ubr)
        self.main.screen_load_time('CLIENT->PRODUCT->UBR')
        mouse.click_on_element(self, 'XPATH',self.gp)
        self.main.screen_load_time('CLIENT->PRODUCT->GP')
        mouse.click_on_element(self, 'XPATH',self.change)
        self.main.screen_load_time('CLIENT->PRODUCT->Change')

    def select_screens_under_users(self):
        self.main.select_gp_option('USERS', sub_item='ACCESS CONTROL')
        self.main.screen_load_time('USRES->ACCESS CONTROL')
        mouse.click_on_element(self, 'XPATH',self.username)
        self.main.screen_load_time('USRES->ACCESS CONTROL->Role')
        mouse.click_on_element(self, 'XPATH',self.Resources)
        self.main.screen_load_time('USRES->ACCESS CONTROL->Resources')
        self.main.select_gp_option('USERS', sub_item='ROLE TEMPLATES')
        self.main.screen_load_time('USRES->ROLE TEMPLATES')
        mouse.click_on_element(self, 'XPATH',self.template_name)
        self.main.screen_load_time('USRES->ACCESS CONTROL->Role->Name')
    
    def select_clients_screen(self):
        self.main.select_gp_option('CLIENTS')
        self.main.screen_load_time('CLIENTS')        
        mouse.click_on_element(self, 'XPATH',self.template_name)
        self.main.screen_load_time('CLIENTS->Header')
        mouse.click_on_element(self, 'XPATH',self.services)
        self.main.screen_load_time('CLIENTS->Services')
        mouse.click_on_element(self, 'XPATH',self.identifiers)
        self.main.screen_load_time('CLIENTS->Identifiers')

    def select_data_dictionary_table_screen(self):
        mouse.click_on_element(self, 'XPATH',self.template_name)
        self.main.screen_load_time('Data Dictionary->Column')
    
    def select_price_type(self):
        mouse.click_on_element(self, 'XPATH',self.template_name)
        self.main.screen_load_time('Prict Type->Logic Tab')
        mouse.click_on_element(self, 'XPATH',self.rule)
        self.main.screen_load_time('Prict Type->Rule Tab')
        mouse.click_on_element(self, 'XPATH',self.output)
        self.main.screen_load_time('Prict Type->Output Tab')
        mouse.click_on_element(self, 'XPATH',self.changes)
        self.main.screen_load_time('Prict Type->Change Tab')

    def uploads_screen(self):
        self.main.select_gp_option('UPLOADS')
        self.main.screen_load_time('UPLOADS')   
        mouse.click_on_element(self, 'XPATH',self.file_name)
        self.main.screen_load_time('UPLOADS->File')
    
    def run_tracker(self):
        mouse.click_on_element(self, 'XPATH',self.tracker)
        self.main.screen_load_time('Run Tracker')
    
    def click_on_view_data_sources(self):
        self.Pages = '1000'
        self.Data = ['AnnualCPIU','BPEstimate','Chargeback','Contract','COT','CPIU','CPPD','Customer','CustomerID','CustomerIDRef','CustomerIDType','CustomerProductCPPD','CustomerRef','DirectSale','HistoricPricing','LineExtension','OTC','PHSResult','Pricing','Product','ProductBlend','ProductCPPD','ProductXRef','Rebate','State','TransType','Tricare']
        forms.select_option_by_text(self, "XPATH", self.Page , self.Pages)
        for item in self.Data:
            logger.info(item)
            forms.select_option_by_text(self, "XPATH", self.DataType,item )
            self.main.screen_load_time('View Data->'+item)

    
