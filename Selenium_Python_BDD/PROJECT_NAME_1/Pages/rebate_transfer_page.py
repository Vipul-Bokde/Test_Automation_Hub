from sre_constants import IN
# from selenium.webdriver.support.select import Select
# import pyautogui
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators,waits_config,mouse_rfn
from GP.utilities.logs_util import logger
# import allure
# from allure_commons.types import AttachmentType
import os, base64
from random import randint
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.csv_utility as CSVUtlty
import logging
import GP.utilities.Repo as Repo
import time
# from selenium.webdriver import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from GP.utilities.database_connection import SqlConnection
import allure
import json
import re
from libraries import generics

class RebateTransferPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)
        
        #locators
        self.Submit = "//div[@class='sparq-modal']/form/div/button[@class= 'btn btn-primary']"
        self.btn_submit_transfer_options_popup_page = "//div[contains(.,'Transfer Options')]/child::form/child::div/child::button[contains(.,'Submit')]"
        # self.Cancel = "//div/button[@class= 'btn btn-secondary'][contains(text(), 'Cancel')]"
        self.Export = "//div[@class='mb-1']/export/button[@title='Export']"
        self.Invoice_name_filter = "//div[@col-id='invoice_name']/div[contains(@class,'ag-cell-label-container')]/span"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"
        self.invoice_name = "//div[@row-index='0']/div[@col-id='invoice_name']"
        self.invoice_name_count = "(//div[@role='row']/div[@col-id='invoice_name'])[{}]"
        self.period = "(//div[@role='row']/div[@col-id='1'])[{}]"
        self.record_length = "(//div[@role='row']/div[@col-id='1'])"
        self.contracting_entity = "(//div[@role='row']/div[@col-id='0'])[{}]"
        self.Transfer_btn = "(//button[@tooltip= 'Transfer']/i)[1]"
        self.msg = "//div[@class='sparq-modal-body']/small"
        self.radio_btn = "//div[@class='col-12']/input[@id='existing-date']"
        self.Date_txtbx = "//div[@class='sparq-modal-body']/my-date-picker//div/input"
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        self.header_values = "//div[@class='ag-header-row']/div[@class='ag-header-cell ag-header-cell-sortable']"
        #Rebate Transfer validation
        self.txt_rebate_transfer = "//span[text()='Rebate Transfer']"
        self.drp_combobox_menu = "(//select[contains(@class,'form-control mr-2')])[2]"
        self.drp_page_Size = "(//select[contains(@class,'form-control mr-2')])[1]"
        self.txt_view_data_page = "//span[text()='Data']"
        self.txt_column_name = "//span[text()='PeriodMonth']"
        self.row_first_view_data_page = "(//div[@col-id='Item'])[2]"
        self.txt_of_record_count_on_ui = "//span[@ref='eSummaryPanel']/child::span[@ref='lbRecordCount']"


    def select_rebate_transfer_from_burger_menu(self):
        self.main.select_gp_option('REBATE TRANSFER')
        self.main.screen_load_time('Rebate Transfer Screen')

    def click_on_transfer_button(self,Invoice_Name):
        self.Invoice_Name = Invoice_Name 
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.invoice_name,"Invoice Name element not found on Webpage in given wait time.")
        mouse.click_on_element(self,"XPATH",self.Invoice_name_filter)
        forms.enter_text_on_element(self,"XPATH",self.search_box,self.Invoice_Name)
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.invoice_name,"Invoice Name element not found on Webpage in given wait time.")
        self.column_text = forms.get_text_on_element(self, "XPATH", self.invoice_name)
        logger.info("ui value"+self.column_text)
        logger.info("xl value"+self.Invoice_Name)
        if self.column_text == self.Invoice_Name:
                mouse.click_on_element(self, "XPATH", self.Transfer_btn)
        else:
            logger.info("Invoice name not found")
            self.login = Login(self.driver)
            self.login.close_browser()
            exit(0)
        
    def select_period_date(self,Date):
        self.date_txt_box = Date
        self.msg_visible = locators.element_exists(self,"XPATH",self.msg)
        if self.msg_visible == True:
            mouse.click_on_element(self,"XPATH",self.radio_btn)
        else:
            forms.enter_text_on_element(self,'XPATH',self.Date_txtbx,self.date_txt_box)
        
    def click_on_submit(self):
        mouse.click_on_element(self, "XPATH", self.Submit)
        self.main.screen_load_time('Screen load after Rebate Transfer')

    def click_on_export_btn(self):
        Record_count_UI = []
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.invoice_name,"Invoice Name element not found on Webpage in given wait time.")
        self.list_of_elem = self.driver.find_elements_by_xpath(self.record_length)
        Record_count_UI = len(self.list_of_elem)
        logger.info("list length:")
        logger.info(Record_count_UI)
        element = self.driver.find_element_by_xpath(self.Export)
        self.driver.execute_script("$(arguments[0]).click();", element)
        return  Record_count_UI

    def copy_remote_file(self):
        self.files = self.get_downloaded_files()
        logger.info("return file list is:")
        logger.info(self.files)
        self.content = self.get_file_content(self.files[0])
      # save the content in a local file in the working directory
        self.file_basename = os.path.basename(self.files[0])
        self.download_file_loc = os.path.join(Repo.downloadfiles_path, self.file_basename)
        with open(self.download_file_loc, 'wb') as f:
            f.write(self.content)
        return  self.download_file_loc
    
    def get_downloaded_files(self):
        self.files = self.driver.get("chrome://downloads")
        return  self.driver.execute_script( \
                "return  document.querySelector('downloads-manager')  "
                " .shadowRoot.querySelector('#downloadsList')         "
                " .items.filter(e => e.state === 'COMPLETE')          "
                " .map(e => e.filePath || e.file_path || e.fileUrl || e.file_url); ")
                
    def navigate_back_to_screen(self):
        self.driver.back()
        self.driver.refresh()
        self.main.screen_load_time('Downloads->Screen')

    def get_file_content(self, path):
        try:
            elem = self.driver.execute_script( \
                "var input = window.document.createElement('INPUT'); "
                "input.setAttribute('type', 'file'); "
                "input.hidden = true; "
                "input.onchange = function (e) { e.stopPropagation() }; "
                "return window.document.documentElement.appendChild(input); " )
            elem._execute('sendKeysToElement', {'value': [ path ], 'text': path})
            result = self.driver.execute_async_script( \
                "var input = arguments[0], callback = arguments[1]; "
                "var reader = new FileReader(); "
                "reader.onload = function (ev) { callback(reader.result) }; "
                "reader.onerror = function (ex) { callback(ex.message) }; "
                "reader.readAsDataURL(input.files[0]); "
                "input.remove(); "
                , elem)
            if not result.startswith('data:') :
                raise Exception("Failed to get file content: %s" % result)
            return base64.b64decode(result[result.find('base64,') + 7:])
        finally:
            logging.info("get_file_content executed successfully")
    
    def validate_exported_file(self,dwnld_filpath,Record_count_UI):
        # code for validating random values from exported grid file
        for item in range (0,5):
            random_no = randint(1,5)
            logger.info("Random no is:")
            logger.info(random_no)
            # UI Values
            UI_Val_List = []
            contract_entity = forms.get_text_on_element(self, "XPATH", self.contracting_entity.format(random_no))
            UI_Val_List.append(contract_entity)
            invoice_name = forms.get_text_on_element(self, "XPATH", self.invoice_name_count.format(random_no))
            UI_Val_List.append(invoice_name)
            Period = forms.get_text_on_element(self, "XPATH", self.period.format(random_no))
            UI_Val_List.append(Period)
            logger.info("UI List")
            logger.info(UI_Val_List)
            # CSV Values
            csv_column_list = ['Contracting Entity','Invoice Name','Period']
            CSV_Val_List= CSVUtlty.csvReader(dwnld_filpath,random_no-1,csv_column_list)
            logger.info("CSV List")
            logger.info(CSV_Val_List)
            comparison_result = CSVUtlty.compareLists(UI_Val_List,CSV_Val_List)
            logger.info("Return list comparison is:")
            logger.info(comparison_result)
            assert comparison_result == "Equal", "Downloaded grid file value does not match with UI values"
       
        # UI 1st row Values
        UI_Val_List = []
        contract_entity = forms.get_text_on_element(self, "XPATH", self.contracting_entity.format(1))
        UI_Val_List.append(contract_entity)
        invoice_name = forms.get_text_on_element(self, "XPATH", self.invoice_name_count.format(1))
        UI_Val_List.append(invoice_name)
        Period = forms.get_text_on_element(self, "XPATH", self.period.format(1))
        UI_Val_List.append(Period)
        logger.info("UI 1st row List")
        logger.info(UI_Val_List)
        # CSV 1st row Values
        csv_column_list = ['Contracting Entity','Invoice Name','Period']
        CSV_Val_List= CSVUtlty.csvReader(dwnld_filpath,0,csv_column_list)
        logger.info("CSV 1st row List")
        logger.info(CSV_Val_List)
        comparison_result = CSVUtlty.compareLists(UI_Val_List,CSV_Val_List)
        logger.info("Return list comparison is:")
        logger.info(comparison_result)
        assert comparison_result == "Equal", "Downloaded grid file value does not match with UI values"
        
        # # UI last row Values
        # UI_Val_List = []
        # contract_entity = forms.get_text_on_element(self, "XPATH", self.contracting_entity.format(Record_count_UI))
        # UI_Val_List.append(contract_entity)
        # invoice_name = forms.get_text_on_element(self, "XPATH", self.invoice_name_count.format(Record_count_UI))
        # UI_Val_List.append(invoice_name)
        # Period = forms.get_text_on_element(self, "XPATH", self.period.format(Record_count_UI))
        # UI_Val_List.append(Period)
        # logger.info("UI last row List")
        # logger.info(UI_Val_List)
        # # CSV last row Values
        # csv_column_list = ['Contracting Entity','Invoice Name','Period']
        # CSV_Val_List= CSVUtlty.csvReader(dwnld_filpath,Record_count_UI-1,csv_column_list)
        # logger.info("CSV last row List")
        # logger.info(CSV_Val_List)
        # comparison_result = CSVUtlty.compareLists(UI_Val_List,CSV_Val_List)
        # logger.info("Return list comparison is:")
        # logger.info(comparison_result)
        # assert comparison_result == "Equal", "Downloaded grid file value does not match with UI values"

        # code for validating count from exported grid file
        Record_count_csv = CSVUtlty.rowcountfetch(dwnld_filpath)
        logger.info("Record count CSV is:")
        logger.info(Record_count_csv)
        logger.info("Record count UI is:")
        logger.info(Record_count_UI)
        assert Record_count_UI == Record_count_csv, "Record count in UI grid and exported file does not matches"
        
        # code for validating headers of exported grid file and UI columns  
        self.ui_column_length = []
        self.ui_header_list = []
        self.list_of_elem = self.driver.find_elements_by_xpath(self.header_values)
        self.ui_column_length = len(self.list_of_elem)
        logger.info(self.ui_column_length)
        for i in range(1,self.ui_column_length):
            self.header = "(//div[@class='ag-header-row']/div[@class='ag-header-cell ag-header-cell-sortable'])["+str(i)+"]"
            a = forms.get_text_on_element(self, "XPATH", self.header)
            self.ui_header_list.append(a)
        logger.info(self.ui_header_list)
        csv_header_list = CSVUtlty.csvHeaderReader(dwnld_filpath)
        csv_header_list.pop(15)
        logger.info(csv_header_list)
        assert self.ui_header_list == csv_header_list, "Header data in UI grid and exported file does not matches"

    def click_on_any_filter_icon(self,column_name):
        self.column_name = column_name
        MainPage.click_on_any_filter_icon(self,self.column_name)

    def enter_text_on_any_filter_icon_search_box(self,filter_text):
        self.filter_text = filter_text
        MainPage.enter_text_on_any_filter_icon_search_box(self,self.filter_text)       
        
    def click_on_rebate_transfer_page(self):
        mouse.click_on_element(self, "XPATH", self.txt_rebate_transfer)
        logger.info("User can click on rebate transfer page")

    def verify_status_column_for_unsettled_invoice(self,status):
        self.status = status
        self.verify_status_column = "//div[@ref='eCenterContainer']//child::div[contains(@class,'ag-row-first')]/child::div[11][text()='"+self.status+"' or '"+self.status+"']"
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.invoice_name,"Invoice Name element not found on Webpage in given wait time.")
        logger.info("User can see status column with the unsettled invoice")
        logger.info(self.status)
    
    def get_text_of_first_row_for_column(self,column_name,column_index):
        self.column_name = column_name
        self.column_index = column_index
        self.txt_of_first_row = "//span[text()='"+self.column_name+"']//ancestor::div[contains(@class,'ag-header ag-pivot-off')]/following-sibling::div[@ref='eBodyViewport']/descendant::div[contains(@class,'ag-row-first')]/child::div["+self.column_index+"]"
        self.txt_get_data_of_first_row = forms.get_text_on_element(self,"XPATH",self.txt_of_first_row)
        allure.attach("Column used is: "+self.column_name,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Column data is: "+self.txt_get_data_of_first_row,attachment_type=allure.attachment_type.TEXT)
        return self.txt_get_data_of_first_row
    
    def click_on_rebate_transfer_button(self,row_index):
        self.row_index = row_index
        self.btn_Transfer = "(//div[@title='Transfer']/child::page-action/child::button/i)["+self.row_index+"]"
        #self.btn_rebate_transfer = "//div[@ref='eCenterContainer']//child::div[contains(@class,'ag-row-position-absolute')]["+self.row_index+"]/child::div[16]/child::page-action/child::button[@tooltip='Transfer']/i"
        mouse.click_on_element(self, "XPATH", self.btn_Transfer)
        logger.info("User can click on rebate transfer button")
    
    def verify_rebate_transfer_successfully_done_and_internal_id_not_displayed(self,internal_id):
        self.internal_id = internal_id
        self.verify_internal_id = "(//div[@col-id='id'][text()='"+self.internal_id+"'])[1]"
        self.element= locators.check_element_not_displayed(self,"XPATH",self.verify_internal_id)
        logger.info(self.element)
        assert self.element, "User can see internal id"
    
    def select_any_menu_from_burger_menu(self,hamburger_menu):
        self.hamburger_menu =hamburger_menu
        self.main.select_gp_option(self.hamburger_menu)
        self.main.screen_load_time(self.hamburger_menu+" "+"Screen")
        allure.attach("User see select menu as: "+self.hamburger_menu,attachment_type=allure.attachment_type.TEXT)
    
    def select_any_menu_from_combobox_menu(self,combobox_menu):
        self.combobox_menu = combobox_menu
        forms.select_option_by_text(self, "XPATH", self.drp_combobox_menu,self.combobox_menu)
        self.main.screen_load_time(self.combobox_menu+" : "+" is selected from combobox menu")
        allure.attach("User see select combobox menu as: "+self.combobox_menu,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, "Products Combox Menu Selected")

    def select_page_size_from_dropdown(self,page_size):
        self.page_size = page_size
        forms.select_option_by_text(self, "XPATH", self.drp_page_Size,self.page_size)
        logger.info("User can select page size as: ")
        allure.attach("User see select page size as: "+self.page_size,attachment_type=allure.attachment_type.TEXT)

   
    def click_on_view_data_page(self):
        mouse.click_on_element(self, "XPATH", self.txt_view_data_page)
        logger.info("User can click on view data page")

    def get_date_of_period_month(self,period_month_date):
        self.period_month_date = period_month_date
        self.splitted_date_of_period_month = self.period_month_date.split('/')
        logger.info("Splitted date is :")
        logger.info(self.splitted_date_of_period_month)
        self.get_period_month_date = self.splitted_date_of_period_month[2]+self.splitted_date_of_period_month[0]
        logger.info("Period Month is :")
        logger.info(self.get_period_month_date)
        return self.get_period_month_date

    def verify_filtered_data_is_displayed(self,column_col_id,filtered_data):
        self.column_col_id = column_col_id
        self.filtered_data = filtered_data
        self.verify_filtered_data = "(//div[@col-id='"+self.column_col_id+"'][text()='"+self.filtered_data+"'])[1]"
        self.element = locators.element_is_displayed(self, "XPATH",self.verify_filtered_data)
        logger.info(self.element)
        assert self.element , "User cannot see the filtered data"
        allure.attach("User can see filtered data as : "+self.filtered_data,attachment_type=allure.attachment_type.TEXT)

    def scroll_to_view(self,length):
        self.int_length = int(length)
        mouse.click_on_element(self,"XPATH",self.row_first_view_data_page)
        self.bln_flag = mouse.scroll_to_right_using_send_keyboard_keys(self,self.int_length)

    def get_current_system_date(self,date_format):
        self.date_format = date_format
        self.system_current_date = MainPage.get_system_current_date(self,self.date_format)
        allure.attach("User can see current system date as : "+self.system_current_date,attachment_type=allure.attachment_type.TEXT)
        return self.system_current_date
    
    def wait_for_screen_to_load(self,hamburger_menu):
        self.hamburger_menu =hamburger_menu
        self.main.screen_load_time(self.hamburger_menu+" "+"Screen")
    
    def get_record_count_of_UI(self):
        self.txt_get_data_of_record_count_on_ui = forms.get_text_on_element(self,"XPATH",self.txt_of_record_count_on_ui)
        self.txt_get_data_of_record_count_on_ui = self.txt_get_data_of_record_count_on_ui.replace(',','')
        self.split_record = re.findall(r'\d+',self.txt_get_data_of_record_count_on_ui)
        self.get_record_count= self.split_record[0]
        allure.attach("Count from UI Is : "+self.get_record_count,attachment_type=allure.attachment_type.TEXT)
        return self.get_record_count
    
    def data_base_connection_and_get_DB_record_count(self,sql_query,client,settlement_num,period_month):
        self.client = client
        self.settlement_num = settlement_num
        self.period_month = period_month
        self.updated_query = sql_query.replace('${client}', self.client)
        self.updated_query_1 = self.updated_query.replace('${settlement_num}',self.settlement_num)
        self.updated_query_2 = self.updated_query_1.replace('${period_month}',self.period_month)
        allure.attach("SQL Query Updated  : "+self.updated_query_2,attachment_type=allure.attachment_type.TEXT)
        self.query_result = SqlConnection.connection(self.updated_query_2) 
        query_json_result = json.dumps(self.query_result, default=str, sort_keys=True)
        allure.attach("SQL Result Set: " +query_json_result, attachment_type=allure.attachment_type.JSON)
        return self.query_result
    
    def verify_UI_and_DB_records(self,UI_count,DB_count):
        self.UI_count = UI_count
        self.DB_count = DB_count
        if self.UI_count == self.DB_count:
            allure.attach("UI records  count is : "+self.UI_count,attachment_type=allure.attachment_type.TEXT)
            allure.attach("DB records count  is : "+self.DB_count,attachment_type=allure.attachment_type.TEXT)
            logger.info("UI records is equal to DB records")
            assert True , "UI records equal to DB records"
        else:
            allure.attach("UI records  count is : "+self.UI_count,attachment_type=allure.attachment_type.TEXT)
            allure.attach("DB records count  is : "+self.DB_count,attachment_type=allure.attachment_type.TEXT)
            logger.info("UI records not equal to DB records")
            assert False , "UI records not equal to DB records"

    def get_count_from_DB(self,Data):
        self.Data = Data
        self.get_DB_count = self.Data[0]
        self.get_DB_count = self.get_DB_count[0]
        self.str_DB_count = str(self.get_DB_count)
        return self.str_DB_count
    
    def verify_dollar_amount_and_get_data_and_click_on_rebate_transfer_button(self,dollar_amount,column_name_rebate_source,column_index_rebate_source,column_name_internl_id,column_index_internal_id,row_index_1,row_index_2,row_index_1_for_rebate_transfer,filter_column_name):
        self.dollar_amount = dollar_amount
        self.column_name_rebate_source = column_name_rebate_source
        self.column_index_rebate_source = column_index_rebate_source
        self.column_name_internl_id = column_name_internl_id
        self.column_index_internal_id = column_index_internal_id
        self.row_index_1 = row_index_1
        self.row_index_2 = row_index_2
        self.filter_column_name = filter_column_name
        self.row_index_1_for_rebate_transfer = row_index_1_for_rebate_transfer
        if '0.00' in self.dollar_amount:
            self.get_data_of_column_internal_id =self.get_data_of_any_row_for_column(self.column_name_internl_id,self.column_index_internal_id,self.row_index_1_for_rebate_transfer)
            self.get_data_of_column_rebate_source =self.get_data_of_any_row_for_column(self.column_name_rebate_source,self.column_index_rebate_source,self.row_index_1_for_rebate_transfer)
            self.click_on_any_filter_icon(self.filter_column_name)
            self.enter_text_on_any_filter_icon_search_box(self.get_data_of_column_internal_id)
            self.click_on_rebate_transfer_page()
            self.click_on_rebate_transfer_button(self.row_index_2)
            allure.attach("User can click on second row : "+self.row_index_2,attachment_type=allure.attachment_type.TEXT)
            self.internal_id_and_rebate_source = self.get_data_of_column_internal_id+" "+self.get_data_of_column_rebate_source
            return self.internal_id_and_rebate_source
        else:
            self.get_data_of_column_internal_id = self.get_text_of_first_row_for_column(self.column_name_internl_id,self.column_index_internal_id)
            self.get_data_of_column_rebate_source = self.get_text_of_first_row_for_column(self.column_name_rebate_source,self.column_index_rebate_source)
            self.click_on_any_filter_icon(self.filter_column_name)
            self.enter_text_on_any_filter_icon_search_box(self.get_data_of_column_internal_id)
            self.click_on_rebate_transfer_page()
            self.click_on_rebate_transfer_button(self.row_index_1)
            allure.attach("User can click on first Row : "+self.row_index_1,attachment_type=allure.attachment_type.TEXT)
            self.internal_id_and_rebate_source = self.get_data_of_column_internal_id+" "+self.get_data_of_column_rebate_source
            return self.internal_id_and_rebate_source
        
    def split_internal_id_and_get_internal_id(self,internal_id_and_rebate_source):
        self.internal_id_and_rebate_source = internal_id_and_rebate_source
        self.split_internal_id_and_rebate_source = self.internal_id_and_rebate_source.split(' ')
        self.internal_id = self.split_internal_id_and_rebate_source[0]
        allure.attach("Internal Id Is : "+self.internal_id,attachment_type=allure.attachment_type.TEXT)
        return self.internal_id
    
    def split_rebate_source_and_get_rebate_source(self,internal_id_and_rebate_source):
        self.internal_id_and_rebate_source = internal_id_and_rebate_source
        self.split_internal_id_and_rebate_source = self.internal_id_and_rebate_source.split(' ')
        self.rebate_source = self.split_internal_id_and_rebate_source[1]
        allure.attach("Rebate Source Is : "+self.rebate_source,attachment_type=allure.attachment_type.TEXT)
        return self.rebate_source

    def get_data_of_any_row_for_column(self,column_name,column_index,row_index):
        self.column_name = column_name
        self.column_index = column_index
        self.row_index = row_index
        self.txt_of_any_row = "//span[text()='"+self.column_name+"']//ancestor::div[contains(@class,'ag-header ag-pivot-off')]/following-sibling::div[@ref='eBodyViewport']/descendant::div[@row-index='"+self.row_index+"'][2]/child::div["+self.column_index+"]"
        self.txt_get_data_of_any_row = forms.get_text_on_element(self,"XPATH",self.txt_of_any_row)
        allure.attach("Column used is : "+self.column_name,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Column data is : "+self.txt_get_data_of_any_row,attachment_type=allure.attachment_type.TEXT)
        return self.txt_get_data_of_any_row
    
    def wait_for_min_time(self):
        locators.wait_implicite(self,waits_config.MAX_IMPLICIT_TIMEOUT)  

    def verify_data_available_on_view_data_screen(self,column_col_id,filtered_data):
        self.column_col_id = column_col_id
        self.filtered_data = filtered_data
        self.verify_filtered_data = "(//div[@col-id='"+self.column_col_id+"'][text()='"+self.filtered_data+"'])[1]"
        self.element = locators.element_is_displayed(self, "XPATH",self.verify_filtered_data)
        logger.info(self.element)
        return self.element
    
    def verify_data_for_settlement_num(self,length,column_name_settlement_num,get_internal_id,column_col_id,hamburger_menu,txt_page_size):
        self.column_name_settlement_num = column_name_settlement_num
        self.get_internal_id =get_internal_id
        self.column_col_id = column_col_id
        self.hamburger_menu = hamburger_menu
        self.txt_page_size = txt_page_size
        self.length = length
        self.int_counter =0
        self.bln_flag_while_loop = False
        while self.bln_flag_while_loop==False:
            self.select_page_size_from_dropdown(self.txt_page_size)
            self.scroll_to_view(self.length)
            self.click_on_any_filter_icon(self.column_name_settlement_num)
            self.enter_text_on_any_filter_icon_search_box(self.get_internal_id)
            self.click_on_view_data_page()
            self.bln_flag_verify_data= self.verify_data_available_on_view_data_screen(self.column_col_id,self.get_internal_id)
            logger.info(self.bln_flag_verify_data)
            if self.bln_flag_verify_data == True:
                allure.attach("Data Available for settlement Number : "+self.get_internal_id,attachment_type=allure.attachment_type.TEXT)
                self.bln_flag_while_loop = True
            self.int_counter = self.int_counter+1
            logger.info(self.int_counter)
            self.driver.refresh()
            self.wait_for_screen_to_load(self.hamburger_menu)
            if self.int_counter > 30:
                self.bln_flag_while_loop= True

    """Author : Sadiya Kotwal
       Description : This method verify the  transfer button
       Arguments : 
       Returns : NA""" 
    def verify_rebate_transfer_button(self):
        self.bln_flag=False
        self.bln_flag = locators.element_is_displayed(self,"XPATH", self.Transfer_btn)
        if self.bln_flag == True:
            allure.attach("User can see transfer button",attachment_type=allure.attachment_type.TEXT)
            generics.capture_screenshot_allure(self.main, "Transfer Button")
        else:
            assert self.bln_flag , "User cannot see the transfer button"

    """Author : Sadiya Kotwal
       Description : This method clicks on submit button
       Arguments : 
       Returns : NA""" 
    def click_on_submit_from_transfer_options_popup_page(self):
        mouse.click_on_element(self, "XPATH", self.btn_submit_transfer_options_popup_page)
        allure.attach("User can click on submit button",attachment_type=allure.attachment_type.TEXT)
