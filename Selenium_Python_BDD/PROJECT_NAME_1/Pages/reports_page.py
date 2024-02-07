from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators,dates
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import os
from GP.utilities.logs_util import logger
from libraries import mouse
from selenium.webdriver.common.by import By
from GP.utilities.database_connection import SqlConnection
import json
import pandas as pd



class reportpage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        
    #locators
        self.client = "//div[@class='col'] /select"
        self.submit = "//div/button[@class='btn btn-primary']"
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        #control and resonability report
        self.input_current_date = "//div[contains(.,'Reasonability Report Date')]/parent::div/child::div[2]/child::div/child::div[2]/child::my-date-picker/descendant::div[@class='selectiongroup']"
        self.input_prior_date = "//div[contains(.,'Reasonability Report Date')]/parent::div/child::div[2]/child::div/child::div[4]/child::my-date-picker/descendant::input"
        self.btn_submit ="//div[contains(.,'Reasonability Report Date')]/parent::div/child::div[@class='sparq-modal-footer']/child::button[contains(.,'Submit')]"
        self.hdr_popup_for_control_and_reasonability_report = "//div[contains(.,'Reasonability Report Date')][@class='sparq-modal-header']"
        #Calc Audit LOg
        self.input_start_date = "//div[contains(.,'Calc Audit Log')]/parent::div/child::div[2]/child::div/child::div[1]/child::my-date-picker/descendant::div[@class='selectiongroup']/child::input"
        self.input_end_date ="//div[contains(.,'Calc Audit Log')]/parent::div/child::div[2]/child::div/child::div[2]/child::my-date-picker/descendant::div[@class='selectiongroup']/child::input"
        self.btn_submit_cal_audit_log ="//div[contains(.,'Calc Audit Log')]/parent::div/child::div[@class='sparq-modal-footer']/child::button[contains(.,'Submit')]"


    def select_global_from_burger_menu(self):
        self.main.screen_load_time('Data Overview Screen')
        self.main.select_gp_option('REPORTS', sub_item='CREDIT BALANCE REPORT')
        self.main.screen_load_time('Reports->CREDIT BALANCE REPORT')
        allure.attach("Clicked on CREDIT BALANCE REPORT",attachment_type=allure.attachment_type.TEXT)

    def select_control_and_reasonability_report_menu_from_burger_menu(self):
        self.main.screen_load_time('Data Overview Screen')
        self.main.select_gp_option('REPORTS', sub_item='CONTROL AND REASONABILITY REPORT')
        self.main.screen_load_time('Reports->CONTROL AND REASONABILITY REPORT')
        allure.attach("User see select menu as:  CONTROL AND REASONABILITY REPORT" ,attachment_type=allure.attachment_type.TEXT)
    
    def verify_header_popup_for_control_and_reasonability_report(self):
        locators.element_is_displayed(self,"XPATH", self.hdr_popup_for_control_and_reasonability_report)
        allure.attach("User can see the popup for control and reasonability report: ",attachment_type=allure.attachment_type.TEXT)

    def click_on_current_date_input(self):
        mouse.click_on_element(self,"XPATH", self.input_current_date)
        allure.attach("User can click on current date calendar: ",attachment_type=allure.attachment_type.TEXT)

    def click_on_prior_date_input(self):
        mouse.click_on_element(self,"XPATH", self.input_prior_date)
        allure.attach("User can click on prior date calendar: ",attachment_type=allure.attachment_type.TEXT)

    def select_date_from_calender(self,date_format):
        self.date_format = date_format
        dates.select_date_from_calender(self,self.date_format)

    def verify_prior_date_is_less_than_current_date(self,prior_date,current_date):
        self.prior_entire_date =prior_date
        self.current_entire_date = current_date
        self.split_prior_date = self.prior_entire_date.split("/")
        self.prior_year = self.split_prior_date[2]
        self.prior_month = self.split_prior_date[0]
        self.prior_date = self.split_prior_date[1]
        self.split_current_date = self.current_entire_date.split("/")
        self.current_year = self.split_current_date[2]
        self.current_month = self.split_current_date[0]
        self.current_date = self.split_current_date[1]
        if int(self.prior_month) < int(self.current_month):
            allure.attach("Prior date is less than current date : "+self.prior_entire_date+"  "+self.current_entire_date+"",attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Prior date is not less than current date : "+self.prior_entire_date+"  "+self.current_entire_date+"",attachment_type=allure.attachment_type.TEXT)


    def click_on_submit_from_reports_popup(self):
        mouse.click_on_element(self, "XPATH", self.btn_submit)
        allure.attach("User can click on submit button",attachment_type=allure.attachment_type.TEXT)

    def data_base_connection_and_get_DB_record_for_control_and_reasonability_report(self,sql_query,client_id,period_month):
        self.client_id = client_id
        self.period_month = period_month
        self.updated_query = sql_query.replace('${client_id}', self.client_id)
        self.updated_query_1 = self.updated_query.replace('${period_month}',self.period_month)
        allure.attach("SQL Query Updated  : "+self.updated_query_1,attachment_type=allure.attachment_type.TEXT)
        self.query_result = SqlConnection.connection(self.updated_query_1) 
        query_json_result = json.dumps(self.query_result, default=str, sort_keys=True)
        allure.attach("SQL Returned Result: " +query_json_result, attachment_type=allure.attachment_type.JSON)
        return query_json_result
    
    def select_calc_audit_report_menu_from_burger_menu(self):
        self.main.screen_load_time('Data Overview Screen')
        self.main.select_gp_option('REPORTS', sub_item='CALC AUDIT LOG')
        self.main.screen_load_time('Reports->CALC AUDIT LOG')
        allure.attach("User see select menu as:  CALC AUDIT LOG" ,attachment_type=allure.attachment_type.TEXT)

    def click_on_start_date_input(self,start_date):
        self.start_date = start_date
        mouse.click_on_element(self,"XPATH", self.input_start_date)
        allure.attach("User can click on start date calendar: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH", self.input_start_date,self.start_date)
        allure.attach("User can enter start date  in calendar as: "+self.start_date,attachment_type=allure.attachment_type.TEXT)

    def click_on_end_date_input(self,end_date):
        self.end_date = end_date
        mouse.click_on_element(self,"XPATH", self.input_end_date)
        allure.attach("User can click on end date calendar: ",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self,"XPATH", self.input_end_date,self.end_date)
        allure.attach("User can enter end date in calendar as: "+self.end_date,attachment_type=allure.attachment_type.TEXT)

    def click_on_submit_from_calc_audit_reports_popup(self):
        mouse.click_on_element(self, "XPATH", self.btn_submit_cal_audit_log)
        self.main.screen_load_time('Data Overview Screen')
        allure.attach("User can click on submit button from calc audit log: ",attachment_type=allure.attachment_type.TEXT)

    def data_base_connection_and_get_DB_record_for_calc_audit_log_report(self,sql_query,client_id,start_date,end_date):
        self.client_id = client_id
        self.start_date = start_date
        self.end_date = end_date
        self.updated_query = sql_query.replace('${client_id}', self.client_id)
        self.updated_query_1 = self.updated_query.replace('${start_date}',self.start_date)
        self.updated_query_2 = self.updated_query_1.replace('${end_date}',self.end_date)
        allure.attach("SQL Query Updated  : "+self.updated_query_2,attachment_type=allure.attachment_type.TEXT)
        self.query_result = SqlConnection.connection(self.updated_query_2) 
        query_json_result = json.dumps(self.query_result, default=str, sort_keys=True)
        allure.attach("SQL Calc Audit Log Entire Result set : " +query_json_result, attachment_type=allure.attachment_type.JSON)
        return query_json_result