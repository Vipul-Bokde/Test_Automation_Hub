from libraries.environment_setup import EnvironmentSetup
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from GP.utilities.logs_util import logger
from selenium.webdriver.common.by import By
from libraries import generics
import allure
import time
from GP.utilities.database_connection import SqlConnection
import json
from GP.pages.rebate_transfer_page import RebateTransferPage
from selenium.common.exceptions import NoSuchElementException
class DataOverviewPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        self.data_overview = "//span[@id='container']/span[@class='stage active-stage']"
        self.Upload = "//div[@class='mb-2 float-right']/button[2]"
        self.File_Type = "//div[@class='sparq-modal']/form/div[2]/div[2]/select"
        self.source = "//div[@class='form-group ng-untouched ng-pristine ng-invalid']/select[@id='file-source']"
        self.file_template = "//select[@id='filetemplate']"
        self.UseTempleteCheckbox = "//div[@formgroupname='gp']/input[@id='use_template']"
        self.FileUpload = "//div[@class='form-group']/input[@id='upload-file-chooser']"
        self.Submit = "//div[@class='sparq-modal-footer']/button[@id='upload-submit-btn']"
        self.upload_checkbox = "//div[@formgroupname='gp']/input[@id="'{}'"]"
        self.table = "//div[@class='ag-center-cols-container']"
        self.row = "div[role='row']"
        self.id = "div[col-id='id']"
        self.file = "div[col-id='filename']"
        self.upload_wait_screen = "(//div[@class='ag-header-cell'])[1]"
        self.load_bar = "//div[@class='load-bar']/div[@class='bar'][1]"
            # Validation
        self.validate_button = "//div[@id='page-container']/overview/div[1]/button" 
        self.data_source = "//div[@class='form-check form-check-inline']/label[@for="'{}'"]"
        self.validation_period = "//div[@class='form-check form-check-inline']/input[@value="'{}'"]"
        self.custom_date = "//div[@class='selectiongroup']/input[@placeholder="'{}'"]"
        self.validate_pop_up_button = "//div[@class='sparq-modal-footer upper-margin ']/button[@id="'{}'"]"
        self.validation_render = "//div[@class='jumbotron jumbotron-fluid mt-4 ng-star-inserted']/p/i[@class='fa fa-circle-notch fa-spin']"
        self.validation_result = "//div[@id='no-validations']/p[contains(text(),'No Validation Errors.')]"
        self.validation_results_text = "//overview-detail/h3[contains(text(),'Validation Results')]"
        self.missing_join_header = "//div[@id='validations']//div[@class='card-header'][contains(text(),'{}')]"
        self.missing_join_button = "//div[@id='validations']//div[@class='card-body']/button[contains(text(),'{}')]"
            # upload screen
        self.red_traingle = "//div[@row-index='0']/div[@col-id='status']/span/span/i[@class='text-danger fa fa-exclamation-triangle']"
        self.green_stack  = "//div[@row-index='0']/div[@col-id='status']/span/span/i[@class='text-success fa fa-database']"
        self.FileName = "//div[@class='ag-center-cols-container']/div[@row-index='0']/div[@col-id='filename']"
        self.file_name_filter = "(//div/span[@class='ag-header-icon ag-header-cell-menu-button']/span[@class='ag-icon ag-icon-menu'])[4]"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"
        self.file_type_dropdown ="(//div/select[@class='form-control mr-2 ng-untouched ng-pristine ng-valid'])[2]"
            # getting upload and view data values and column filter
        self.view_data_filter_column = "//div[@col-id='{}']/div[contains(@class,'ag-cell-label-container')]/span"
        self.row_value = "//div[@row-index='0']/div[@col-id='{}']"
            #Data Overview Screen
        self.txt_data_overview_screen = "//span[text()='Overview']"
        self.data_overview_button = "//span[@id='container']/span[1]"
        self.view_data_source = "//div[@class='ag-pinned-left-cols-container']/div[@row-index='{}']"
        self.grid_value = "//div[@class='ag-center-cols-container']/div[@row-id='{}']/div[@col-id='{}']"
        self.total_grid_values = "//div[@class='ag-center-cols-container']/div[@row-index='{}']/div"
        self.view_data_period = "//div[@class='ag-header-row']/div[@col-id='{}']"
        self.view_data_count = "//div[@class='ag-paging-panel ag-font-style']//span[@ref='lbRecordCount']"
    
    def navigate_to_overview_screen(self):
        element = self.driver.find_element_by_xpath(self.data_overview_button)
        self.driver.execute_script("$(arguments[0]).click();", element) 
        # mouse.click_on_element(self,"XPATH",self.data_overview_button)
        self.main.screen_load_time('Navigate to Overview Screen')
    
    def click_on_upload_button(self):
        self.main.screen_load_time('Data Overview Screen')
        element = self.driver.find_element_by_xpath(self.Upload)
        self.driver.execute_script("$(arguments[0]).click();", element) 
        self.main.screen_load_time('Data Overview->upload')

    def select_file_type(self,FileType):
        self.FileType = FileType
        forms.select_option_by_text(self, "XPATH", self.File_Type , self.FileType)
        self.main.screen_load_time('Data Overview->File Type')
        logger.info("Select Filetype from dropdown : " + FileType)
    
      
    """Author : Pooja Jundhare
       Description : This method is to select source and template for file to upload
       Arguments :  source_data,file_template,use_template
       Returns : NA"""        
    def select_source_template(self,source_data,file_template,use_template):
        self.source_value = source_data
        self.file_template_value = file_template
        self.use_template = use_template
        logger.info(self.source_value)
        logger.info(self.file_template_value)
        logger.info(self.FileType)
        if self.FileType != "File Template":
            self.element = self.driver.find_element_by_xpath(self.upload_checkbox.format("'use_template'"))
            if self.element.is_displayed() == True and self.use_template == 'YES':
                if self.FileType == "Direct Sales" or self.FileType == "Chargebacks" or self.FileType == "Rebates" or self.FileType == "Tricare" or self.FileType == "PHS Results":
                    forms.select_option_by_text(self, "XPATH", self.source , self.source_value)
                    allure.attach("Source name selected as  : "+self.source_value,attachment_type=allure.attachment_type.TEXT)
                    forms.select_option_by_text(self, "XPATH", self.file_template , self.file_template_value)
                    allure.attach("Template name selected as  : "+self.file_template_value,attachment_type=allure.attachment_type.TEXT)
                else:
                    forms.select_option_by_text(self, "XPATH", self.file_template , self.file_template_value)
                    allure.attach("Template name selected as  : "+self.file_template_value,attachment_type=allure.attachment_type.TEXT)
            else:
                forms.uncheck_checkbox(self, "XPATH" , self.upload_checkbox.format("'use_template'"))
    
    """Author : Pooja Jundhare
       Description : This method is to click on refresh option while uploading files
       Arguments :  full_refresh, file_template_refresh as boolean
       Returns : NA"""        
    def select_refresh_option(self,full_refresh,file_template_refresh):
        self.full_refresh = full_refresh
        self.file_template_refresh = file_template_refresh
        logger.info("Full Refresh selected as : " + str(self.full_refresh) + " For "+ str(self.FileType))
        allure.attach("Full Refresh selected as  : "+str(self.full_refresh),attachment_type=allure.attachment_type.TEXT)
        logger.info("File Template Refresh selected as : " + str(file_template_refresh) + " For "+ str(self.FileType))
        allure.attach("File Template Refresh selected as : "+str(file_template_refresh),attachment_type=allure.attachment_type.TEXT)
        if self.FileType == "Direct Sales" or self.FileType == "Chargebacks" or self.FileType == "Rebates" or self.FileType == "Tricare":
            if full_refresh == "YES" and file_template_refresh == "NO":
                forms.check_checkbox(self, "XPATH" , self.upload_checkbox.format("'full_refresh'"))
                    
            elif file_template_refresh == "YES" and full_refresh == "NO":
                    forms.check_checkbox(self, "XPATH" , self.upload_checkbox.format("'file_template_refresh'"))
            
            elif file_template_refresh == "YES" and full_refresh == "YES":
                logger.info("full_refresh and file_template_refresh both can not be YES at a time.")

    def upload_file(self,file_to_upload):
        self.file_to_upload = file_to_upload
        file_up = self.driver.find_element_by_xpath(self.FileUpload)
        file_up.send_keys(self.file_to_upload)

    def click_on_submit_button(self):
        mouse.click_on_element(self,"XPATH", self.Submit)
        self.main.screen_load_time('Data Overview->Submit->Uploads Screen')

    def check_uploaded_file(self,file_name):       
        self.file_name = file_name
        MainPage.wait_until_element_is_present(self, 400, By.XPATH, self.green_stack,"Green stack element not found on Webpage in given wait time.")
        self.uploaded_file_name = forms.get_text_on_element(self,"XPATH",self.FileName)
        logger.info(self.uploaded_file_name)
        logger.info(self.file_name)
        try:
            if self.uploaded_file_name == self.file_name:
                element = self.driver.find_element_by_xpath(self.FileName)
                self.driver.execute_script("$(arguments[0]).click();", element) 
                logger.info("File Successfully uploaded")   
                allure.attach("Uploaded File name is : "+self.uploaded_file_name,attachment_type=allure.attachment_type.TEXT)
        except:
            logger.info('File Name does not match')            
            
    def get_upload_screen_data(self):
        self.main.screen_load_time('Master Data->Uploads->File')
        if  self.FileType == "PHS Results":
            phs_results_list =[]
            self.upload_number = forms.get_text_on_element(self,"XPATH",self.row_value.format('number'))
            phs_results_list.append(self.upload_number)
            self.upload_mtype = forms.get_text_on_element(self,"XPATH",self.row_value.format('mtype'))
            phs_results_list.append(self.upload_mtype)
            return phs_results_list
        elif self.FileType == "Trans Types":
            trans_types_list = []
            self.upload_key = forms.get_text_on_element(self,"XPATH",self.row_value.format('key'))
            trans_types_list.append(self.upload_key)
            self.upload_description = forms.get_text_on_element(self,"XPATH",self.row_value.format('description'))
            trans_types_list.append(self.upload_description)
            self.upload_trans_code = forms.get_text_on_element(self,"XPATH",self.row_value.format('trans_code'))
            trans_types_list.append(self.upload_trans_code)
            return trans_types_list
        elif self.FileType == "Contracts":
            contracts_list= []
            self.upload_name = forms.get_text_on_element(self,"XPATH",self.row_value.format('name'))
            contracts_list.append(self.upload_name)
            self.upload_type = forms.get_text_on_element(self,"XPATH",self.row_value.format('type'))
            contracts_list.append(self.upload_type)
            self.upload_number = forms.get_text_on_element(self,"XPATH",self.row_value.format('number'))
            contracts_list.append(self.upload_number)
            return contracts_list
        elif self.FileType == "Direct Sales" or self.FileType == "Chargebacks" or self.FileType== "Rebates":
            trx_list = []
            self.item = forms.get_text_on_element(self,"XPATH",self.row_value.format('item'))
            trx_list.append(self.item)
            self.st_num = forms.get_text_on_element(self,"XPATH",self.row_value.format('st_num'))
            trx_list.append(self.st_num)
            self.bt_num = forms.get_text_on_element(self,"XPATH",self.row_value.format('bt_num'))
            trx_list.append(self.bt_num)
            mouse.click_on_element(self,"XPATH",self.row_value.format('item'))
            self.bln_flag = mouse.scroll_to_right_using_send_keyboard_keys(self,20)
            self.period_month = forms.get_text_on_element(self,"XPATH",self.row_value.format('period_month'))
            trx_list.append(self.period_month)
            return trx_list
        elif self.FileType == "Tricare":
            trx_list = []
            self.item = forms.get_text_on_element(self,"XPATH",self.row_value.format('item'))
            trx_list.append(self.item)
            self.quantity = forms.get_text_on_element(self,"XPATH",self.row_value.format('quantity'))
            trx_list.append(self.quantity)
            self.net_amount = forms.get_text_on_element(self,"XPATH",self.row_value.format('net_amount')) 
            trx_list.append(self.net_amount) 
            self.period_month = forms.get_text_on_element(self,"XPATH",self.row_value.format('period_month'))
            trx_list.append(self.period_month)
            return trx_list
        elif self.FileType  == "Contract Terms" or self.FileType == "Contract Term Products/Contract Products":
            values_list = []
            contract_term_column_list =["contract_id","term_name","term_type","source"]
            contract_term_product_list = ["contract_number","term_name","term_type","source","ndc11"]
            contract_term_list_len =len(contract_term_column_list)
            contract_term_product_list_len =len(contract_term_product_list)
            logger.info(contract_term_list_len)
            logger.info(contract_term_product_list_len)
            if self.FileType == "Contract Terms":
                for i in range(contract_term_list_len):
                    self.column_name = forms.get_text_on_element(self,"XPATH",self.row_value.format(contract_term_column_list[i]))
                    values_list.append(self.column_name)
            else:
               for i in range(contract_term_product_list_len):
                    self.column_name = forms.get_text_on_element(self,"XPATH",self.row_value.format(contract_term_product_list[i]))
                    values_list.append(self.column_name)
            logger.info(values_list)        
            return values_list

            
    """Author : Pooja Jundhare
       Description : This method is to click on upload source and period value on overview screen and navigate to view data screen
       Arguments :  file type
       Returns : period"""    
    def click_on_upload_period_and_source(self,file_type):
        self.file_type = file_type
        logger.info("Uploaded source: "+self.file_type)
        logger.info("Uploaded Period: "+self.period_month)
        self.value_count_len = []
        for source in range(0,4):
            self.source_name = forms.get_text_on_element(self,"XPATH",self.view_data_source.format(source))  
            logger.info(source)  
            logger.info(self.source_name)
            if self.source_name == self.file_type:
                self.value_count = self.driver.find_elements_by_xpath(self.total_grid_values.format(source))
                self.value_count_len = len(self.value_count)
                logger.info(self.value_count_len)
                for period in range(1,self.value_count_len):
                    self.period_name = forms.get_text_on_element(self,"XPATH",self.view_data_period.format(period))  
                    logger.info(self.period_name)
                    if self.period_name == self.period_month:
                        mouse.click_on_element(self,"XPATH",self.grid_value.format(source, period))
                        self.main.screen_load_time(str(self.source_name)+' '+str(self.period_name)+' Overview->View Data')  
                        break
                    else:
                        period = period + 1   
                break                                     
            else:
                source =source + 1 
        return self.period_name
     
    """Author : Pooja Jundhare
       Description : This method returns the record count from view data screen
       Arguments :  NA
       Returns : record count"""                
    def get_view_data_count(self):
        self.main.screen_load_time('Overview->View Data')  
        self.count = forms.get_text_on_element(self,"XPATH",self.view_data_count)   
        self.count = self.count.replace('[','')    
        self.count = self.count.replace(']','') 
        self.count = self.count.replace(',','')   
        logger.info("View Data Count is: "+self.count) 
        allure.attach("View Data count is : "+self.count,attachment_type=allure.attachment_type.TEXT)
        return self.count
     
    """Author : Pooja Jundhare
       Description : This method returns the active record count from gp.source_table based on given client id and period month
       Arguments :  sql query from testdata sheet,client id)
       Returns : record count""" 
    def get_view_data_db_count(self,client_id,sql_query,period_month):
        self.updated_query = sql_query.replace('${period_month}', period_month)
        self.updated_query_1 = self.updated_query.replace('${client_id}',client_id)
        logger.info("SQL Query Updated  : "+self.updated_query_1)
        allure.attach("SQL Query Updated  : "+self.updated_query_1,attachment_type=allure.attachment_type.TEXT)
        self.query_result = SqlConnection.connection(self.updated_query_1) 
        query_json_result = json.dumps(self.query_result, default=str, sort_keys=True)
        allure.attach("SQL Result Set: " +query_json_result, attachment_type=allure.attachment_type.JSON)
        return self.query_result
    
    def select_viewdata_from_burger_menu(self,View_data_dropdown_value):
        self.View_data_dropdown_value = View_data_dropdown_value
        self.main.select_gp_option('VIEW DATA')
        self.main.screen_load_time('VIEW DATA Screen')
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.file_type_dropdown,"File Type dropdown element not found on Webpage in given wait time.")
        forms.select_option_by_text(self, "XPATH", self.file_type_dropdown, self.View_data_dropdown_value)  
        logger.info(self.View_data_dropdown_value)
        self.main.screen_load_time("VIEW DATA->"+str(self.View_data_dropdown_value)+" Screen")  

    def crosscheck_data(self,FileType,upload_column_value_list):
        self.FileType = FileType
        logger.info(upload_column_value_list)
        if self.FileType == "PHS Results":
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('ID'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[0])
            locators.wait_until_presence_of_element(self,By.XPATH, self.row_value.format('ID'))
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('MType'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[1])
            locators.wait_until_presence_of_element(self,By.XPATH, self.row_value.format('MType'))
            self.main.screen_load_time('View Data->PHS Results')
            self.view_data_number= forms.get_text_on_element(self,"XPATH",self.row_value.format('ID'))
            locators.wait_until_presence_of_element(self,By.XPATH, self.row_value.format('MType'))
            self.view_data_mtype = forms.get_text_on_element(self,"XPATH",self.row_value.format('MType'))
            if self.view_data_number == upload_column_value_list[0] and self.view_data_mtype == upload_column_value_list[1]:
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)

            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)

        elif self.FileType == "Trans Types":
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Key'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[0])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Key'))
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Description'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[1])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Description'))
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Code'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[2])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Code'))
            self.main.screen_load_time('View Data->Trans Types')
            self.view_data_key= forms.get_text_on_element(self,"XPATH",self.row_value.format('Key'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Description'))
            self.view_data_description = forms.get_text_on_element(self,"XPATH",self.row_value.format('Description'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Code'))
            self.view_data_code = forms.get_text_on_element(self,"XPATH",self.row_value.format('Code')) 
            if self.view_data_key == upload_column_value_list[0] and self.view_data_description == upload_column_value_list[1] and self.view_data_code == upload_column_value_list[2]:
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)
            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)

        elif self.FileType == "Contracts":
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('ID'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[2])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('ID'))
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Name'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[0])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Name'))
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Type'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[1])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Type'))
            self.main.screen_load_time('View Data->Contracts')
            self.view_data_id= forms.get_text_on_element(self,"XPATH",self.row_value.format('ID'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Name'))
            self.view_data_name = forms.get_text_on_element(self,"XPATH",self.row_value.format('Name'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Type'))
            self.view_data_type = forms.get_text_on_element(self,"XPATH",self.row_value.format('Type')) 
            if self.view_data_name == upload_column_value_list[0] and self.view_data_type == upload_column_value_list[1]  and self.view_data_id == upload_column_value_list[2]:
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)
            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)

        elif self.FileType == "Direct Sales" or self.FileType == "Chargebacks" or self.FileType== "Rebates":
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Item'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[0])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Item'))
            self.main.screen_load_time('View Data->Loading time after entering value into Filter')
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('ShiptoNum'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[1])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('ShiptoNum'))
            self.main.screen_load_time('View Data->Loading time after entering value into Filter')
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('BilltoNum'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[2])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('BilltoNum'))
            self.main.screen_load_time('View Data->Transaction data')
            self.item_data_value = forms.get_text_on_element(self,"XPATH",self.row_value.format('Item'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('ShiptoNum'))
            self.st_num_data_value = forms.get_text_on_element(self,"XPATH",self.row_value.format('ShiptoNum'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('BilltoNum'))
            self.bt_num_data_value = forms.get_text_on_element(self,"XPATH",self.row_value.format('BilltoNum')) 
            if self.item_data_value == upload_column_value_list[0] and self.st_num_data_value == upload_column_value_list[1] and self.bt_num_data_value == upload_column_value_list[2]:
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)
            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)
                
        elif self.FileType == "Tricare":
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Item'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[0])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Item'))
            self.main.screen_load_time('View Data->Loading time after entering value into Filter')
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('Quantity'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[1])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Quantity'))
            self.main.screen_load_time('View Data->Loading time after entering value into Filter')
            mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format('NetAmount'))
            forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[2])
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('NetAmount'))
            self.main.screen_load_time('View Data->Transaction data')
            self.item_data_value = forms.get_text_on_element(self,"XPATH",self.row_value.format('Item'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('Quantity'))
            self.quantity_value = forms.get_text_on_element(self,"XPATH",self.row_value.format('Quantity'))
            locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format('NetAmount'))
            self.net_amount_value = forms.get_text_on_element(self,"XPATH",self.row_value.format('NetAmount')) 
            self.quantity = int(float(self.quantity_value))
            self.net_amount = float(self.net_amount_value)
            if self.item_data_value == upload_column_value_list[0] and self.quantity == int(upload_column_value_list[1]) and self.net_amount == float(upload_column_value_list[2]):
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)
            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)
                
        elif self.FileType  == "Contract Terms":
            upload_column_value_list_len = len(upload_column_value_list)
            logger.info(upload_column_value_list)
            logger.info(upload_column_value_list_len)
            contract_term_column_list =["ContractID","Name","Type","Source"]
            for i in range(upload_column_value_list_len):
                mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format(contract_term_column_list[i]))
                forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[i])
                locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format(contract_term_column_list[i]))
                self.main.screen_load_time('View Data->Loading time after entering value into Filter')
            self.main.screen_load_time('View Data->Transaction data')
            contract_term_row_list=[]
            for i in range(upload_column_value_list_len):
                self.data_value = forms.get_text_on_element(self,"XPATH",self.row_value.format(contract_term_column_list[i]))
                contract_term_row_list.append(self.data_value)
            logger.info(upload_column_value_list)
            logger.info(contract_term_row_list)
            if upload_column_value_list == contract_term_row_list:
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)
            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)
        
        elif self.FileType == "Contract Term Products/Contract Products":
            upload_column_value_list_len = len(upload_column_value_list)
            logger.info(upload_column_value_list)
            logger.info(upload_column_value_list_len)
            contract_term_product_list = ["ContractNumber","TermName","TermType","Source","NDC11"]
            for i in range(upload_column_value_list_len):
                mouse.click_on_element(self,"XPATH",self.view_data_filter_column.format(contract_term_product_list[i]))
                forms.enter_text_on_element(self,"XPATH",self.search_box,upload_column_value_list[i])
                locators.wait_until_presence_of_element(self, By.XPATH, self.row_value.format(contract_term_product_list[i]))
                self.main.screen_load_time('View Data->Loading time after entering value into Filter')
            contract_term_product_row_list =[]
            for i in range(upload_column_value_list_len):
                self.data_value = forms.get_text_on_element(self,"XPATH",self.row_value.format(contract_term_product_list[i]))
                contract_term_product_row_list.append(self.data_value)
            self.product = forms.get_text_on_element(self,"XPATH",self.row_value.format('Product'))
            logger.info(len(self.product))
            assert len(self.product) > 0 ,"Added contract term products's NDC11 does not present into Client"
            logger.info(upload_column_value_list)
            logger.info(contract_term_product_row_list)
            if upload_column_value_list == contract_term_product_row_list:
                logger.info("data is correct")
                allure.attach("data is correct ",attachment_type=allure.attachment_type.TEXT)
            else:
                logger.info("data is not correct")
                allure.attach("data is not correct ",attachment_type=allure.attachment_type.TEXT)

    def validate(self):
        self.main.screen_load_time('Data Overview Screen')
        element = self.driver.find_element_by_xpath(self.validate_button)
        self.driver.execute_script("$(arguments[0]).click();", element)  
    
    def select_validation_source(self,source_all,source_ds,source_cbk,source_reb,source_tri):
        self.source_all = source_all
        self.source_ds = source_ds
        self.source_cbk = source_cbk
        self.source_reb = source_reb
        self.source_tri = source_tri
        # if SOURCE_ALL is selected as yes then other filed should be marked as false into test data sheet
        if self.source_all == 'YES':
            forms.check_checkbox(self,"XPATH",self.data_source.format("'all'"))
        
        # if source is selected individually then SELECT_ALL should be NO into test data sheet
        if self.source_all == 'NO':
            if self.source_ds == 'YES':
                forms.check_checkbox(self,"XPATH",self.data_source.format("'ds'"))
            if self.source_cbk == 'YES':
                forms.check_checkbox(self,"XPATH",self.data_source.format("'cbk'"))
            if self.source_reb == 'YES':
                forms.check_checkbox(self,"XPATH",self.data_source.format("'reb'"))
            if self.source_tri == 'YES':
                forms.check_checkbox(self,"XPATH",self.data_source.format("'tri'"))
    
    def select_validation_type(self, validation_type, custom_start_date, custom_end_date):
        self.validation_type = validation_type
        self.custom_start_date = custom_start_date
        self.custom_end_date = custom_end_date
        if (self.validation_type == "custom"):
            logger.info("Custom range option selected")
            mouse.click_on_element(self,"XPATH",self.validation_period.format("'select-periods'"))
            forms.enter_text_on_element(self,"XPATH",self.custom_date.format("'Start Date'"),str(self.custom_start_date))
            forms.enter_text_on_element(self,"XPATH",self.custom_date.format("'End Date'"),str(self.custom_end_date))
        else:
           logger.info("All Period selected by default") 
    
    def click_on_validate(self):
        mouse.click_on_element(self,"XPATH",self.validate_pop_up_button.format("'validate-submit-btn'")) 
        generics.capture_screenshot_allure(self.main, 'Click on Validate Button')
        self.error_msg = self.main.validation_time_capture('Validation time:')
    
    def validation_results(self):
        if self.error_msg == False:
            self.main.screen_load_time('Overview screen')
            try:
                self.element =  self.driver.find_element_by_xpath(self.validation_result)
                if self.element.is_displayed() == True:
                    self.no_validation_error = forms.get_text_on_element(self,"XPATH",self.validation_result)
                    logger.info("No Validation Errors") 
                    allure.attach("No Validation Errors",attachment_type=allure.attachment_type.TEXT)
                    
            except:
                logger.info("Validation Results Exists")
                allure.attach("Validation Results Exists",attachment_type=allure.attachment_type.TEXT)
        else:
            pass
            
    def click_on_cancel(self):
        mouse.click_on_element(self,"XPATH",self.validate_pop_up_button.format("'validate-cancel-btn'"))
        logger.info("Clicked on Cancel Button")
        
    """Author : Sadiya Kotwal
       Description : This method verify the client name on landing page
       Arguments : client_name (client_name= "Akorn Inc")
       Returns : NA""" 
    def verify_client_name(self,client_name):
        self.client_name = client_name
        self.main.screen_load_time('Data Overview Screen')
        self.bln_flag=False
        self.txt_client_name = "//h4[text()='"+self.client_name+"']"
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.txt_data_overview_screen)
        if self.bln_flag == True:
            allure.attach("User can see client as: "+client_name,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see client "
    
    """Author : Sadiya Kotwal
       Description : This method verify the buttons avialable on screen
       Arguments : button_name (Eg: button_name= "Upload")
       Returns : NA""" 
    def verify_buttons_on_screen(self,button_name):
        self.button_name = button_name
        self.bln_flag=False
        self.btn_name = "(//button[contains(.,'"+self.button_name+"')])[1]"
        self.bln_flag = locators.element_is_displayed(self,"XPATH",self.btn_name)
        if self.bln_flag == True:
            allure.attach("User can see button: "+self.button_name,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag , "User cannot see button "
     
    """Author : Pooja Jundhare
       Description : This method verify the Validation Results is present on screen or not
       Arguments : NA
       Returns : NA"""        
    def check_validation_results(self):
            self.main.screen_load_time('Screen load after validation completes.')
            self.element =  self.driver.find_element_by_xpath(self.validation_results_text)
            assert self.element.is_displayed() == True,"Validation Results Does not Exists"
            self.results = forms.get_text_on_element(self,"XPATH",self.validation_results_text)
            logger.info("Validation Results Text Exists") 
            allure.attach("Validation Results Text Exists",attachment_type=allure.attachment_type.TEXT)
            try:
                self.element =  self.driver.find_element_by_xpath(self.validation_result)
                if self.element.is_displayed() == True:
                    self.no_validation_error = forms.get_text_on_element(self,"XPATH",self.validation_result)
                    logger.info("No Validation Errors") 
                    allure.attach("No Validation Errors",attachment_type=allure.attachment_type.TEXT)
            except:
                    logger.info("Validation Errors Exist") 
                    allure.attach("Validation Errors Exist",attachment_type=allure.attachment_type.TEXT)


    """Author : Pooja Jundhare
       Description : This method verify that given missing join is present on screen or not
       Arguments : missing join name (Eg: Missing ContractTerm) 
       Returns : NA"""  
    def check_missing_join(self,missing_validation_header):
        try:
            self.element = self.driver.find_element_by_xpath(self.missing_join_header.format(missing_validation_header))
            if self.element.is_displayed() == True:
                logger.info(missing_validation_header+" Does Exists")
                allure.attach(missing_validation_header+" Does Exists",attachment_type=allure.attachment_type.TEXT)
        except NoSuchElementException: 
            logger.info(missing_validation_header+" Does not Exists") 
            allure.attach(missing_validation_header+" Does not Exists",attachment_type=allure.attachment_type.TEXT)

    """Author : Pooja Jundhare
       Description : This method verify that missing join's create record for... button is present on screen or not
       Arguments : missing validation join button (Eg: Create Records for ContractTerm) 
       Returns : NA"""  
    def download_missing_join_file(self,missing_validation_join_button):
        try:
            if self.element.is_displayed() == True:
                self.element = self.driver.find_element_by_xpath(self.missing_join_button.format(missing_validation_join_button))
                if self.element.is_displayed() == True:
                    logger.info(missing_validation_join_button+" Button Does Exists")
                    allure.attach(missing_validation_join_button+" Button Does Exists",attachment_type=allure.attachment_type.TEXT)
                    mouse.click_on_element(self,"XPATH",self.missing_join_button.format(missing_validation_join_button))
                    self.main.screen_load_time(' Clicked on'+missing_validation_join_button+' Button')
                    self.rebate_transfer = RebateTransferPage(self.driver)
                    self.download_file_loc = self.rebate_transfer.copy_remote_file()
                    self.rebate_transfer.navigate_back_to_screen()      
                    allure.attach(missing_validation_join_button+" File Downloaded Successfully at "+self.download_file_loc, attachment_type=allure.attachment_type.TEXT)
        except NoSuchElementException:
            logger.info(missing_validation_join_button+" Button Does not Exists") 
            allure.attach(missing_validation_join_button+" Button Does not Exists",attachment_type=allure.attachment_type.TEXT)

    
    
    
    