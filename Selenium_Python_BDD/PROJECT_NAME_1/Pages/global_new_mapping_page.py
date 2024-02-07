from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators
from selenium.webdriver.common.keys import Keys
import allure
from allure_commons.types import AttachmentType
import os
import time
from GP.utilities.logs_util import logger
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from selenium.webdriver.common.by import By
from GP.pages.login_page import Login
from libraries import generics


class NewMappingPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators Templates
        self.file_template = "//li[contains(.,'GLOBAL')]/ul/li[contains(.,'FILE TEMPLATES')]"
        self.New_Template = "//div[@id = 'template-controls']/button[1]"
        self.Temp_Name = "//div/input[@formcontrolname='name']"
        self.Temp_Descripation = "//div/textarea[@formcontrolname='description']"
        self.Temp_GP_Service = "//div[@class='col']/div[3]/input"
        self.Temp_Submit = "//div/button[@id='template-submit-btn']"
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        self.page_count = "//div[@class='ag-paging-panel ag-font-style']/span/span[@ref='lbTotal']"
        self.last_page = "//div[@class='ag-paging-panel ag-font-style']/span/button[@ref='btLast']"

        # self.TempExistText = "(//div[@class= 'sparq-modal-body']/div[contains(text(),"File template with name 'Test_Template' already exists.")])"
        
        self.NameFilter = "(//div[@role= 'presentation']/span[@ref= 'eMenu']/span)[3]" 
        self.TempNameTextBox = "//div[@class='ag-input-text-wrapper']/input[@type='text']"
        self.Template_length = "//div[@role='gridcell'][@col-id='name']"
        self.TemplateNameSelect = "//div[@row-index='0']/div[@col-id='name']"
        self.template_checkbox = "//div[@row-index='0']/div//span[@class='ag-icon ag-icon-checkbox-unchecked']"
        self.delete_template = "//div[@class='float-right mt-2']/button[@class='btn btn-danger']"
        self.EditRecordBtn = "//div/button[@id='btn-save-record']"
        self.SubmitForApproval = "//div/span/button[@id='btn-save-record']"
        self.ApprovalNotesTextBox = "//div[@class= 'sparq-modal-body']/textarea[@id='approval-note']"
        self.ApprovalSubmitBtn = "(//div[@class= 'sparq-modal-footer']/button[@type='submit'])[7]"
        self.delete_popup_text= "//modal[@id='filetemplate-submit-approval']/div[@class='sparq-modal']/div[@class='sparq-modal-header']"
        self.note = "//div[@class='sparq-modal-body']/textarea[@id='approval-note']"
        self.submit_btn = "//div[@class='sparq-modal-footer']/button[@class='btn submit-btn btn-primary']"
        self.cancel_btn = "//div[@class='sparq-modal-footer']/button[@class='btn cancel-btn btn-secondary']"
        
         #locators
        self.Approval_Screen_Client = "//*[@id='page-container']/approval/div[2]/div/div/div[1]/select"
        self.type = "//*[@id='page-container']/approval/div[2]/div/div/div[2]/select"
        self.Approval_Name_Row = "//div[@role='row']/diff-renderer/div" 
        #locators GP Mappings
        self.FileTemplete = "//li/a[@id='file-templates-link'][contains(text(),'FILE TEMPLATES')]"
        self.GPMappings = "//uL/li[2]/a[contains(text(),'GP Mappings')]"
        self.NewMapping = "//div[@class='float-right mt-2 mb-2']/button[@class='btn btn-secondary']"
        self.client = "//div/select[@formcontrolname='client_id']"
        self.datatype = "//div/select[@formcontrolname='data_type']"
        self.source = "//div/select[@formcontrolname='source']"
        self.filetemplate = "//div/select[@formcontrolname='template_id']"
        self.filtername = "//div[@class='form-group']/input[@id='filter-name']"   
        self.Submitbutton = "//div/button[@id='mapping-submit-btn']"
        self.MappingExistText = "//div[@class='sparq-modal-body']/div[contains(text(),'Mapping already exists.')]"
        self.filter_icon = "//div[@col-id='{}']/div[contains(@class,'ag-cell-label-container')]/span"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"
        self.row_data = "//div[@row-index='0']/div[@col-id='{}']"
        self.mapping_checkbox = "//div[@row-index='0']/div[@col-id='id']//span[@class='ag-selection-checkbox']"
        self.delete_mapping_button = "//div[@class='float-right mt-2 mb-2']/button[@class='btn btn-danger']"

    def select_global_from_burger_menu(self):
        self.element_exist = locators.element_exists(self,"XPATH",self.file_template)
        if self.element_exist == True:
            self.main.select_gp_option('GLOBAL', sub_item='FILE TEMPLATES')
            self.main.screen_load_time('FILE TEMPLATES Screen')
        else:
            logger.info("FILE TEMPLATES option does not exist")
            self.login = Login(self.driver)
            self.login.close_browser()
            exit(0)
     
    def click_on_new_template(self):
        mouse.click_on_element(self, 'XPATH', self.New_Template)

    def enter_new_template_details(self,Name , Description):
        self.Name = Name
        self.Description = Description       
        forms.enter_text_on_element(self, "XPATH", self.Temp_Name, self.Name)
        allure.attach("Template Name is : "+self.Name,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.Temp_Descripation, self.Description)
        allure.attach("Template Description is : "+self.Description,attachment_type=allure.attachment_type.TEXT)
        forms.check_checkbox(self, 'XPATH', self.Temp_GP_Service)
     
    def click_temp_submit_button(self,template_name):
        self.FileTemplateName = template_name
        mouse.click_action_on_element(self, "XPATH", self.Temp_Submit)        
        self.Temp_text = """(//div[@class= 'sparq-modal-body']/div[contains(text(),"File template with name '"""+str(self.FileTemplateName)+"""' already exists.")])"""         
        Temp_text_visible = locators.element_exists(self, "XPATH", self.Temp_text)
        if Temp_text_visible == True:
          text = forms.get_text_on_element(self,"XPATH", self.Temp_text)
          status_var = "File template already exists"
        else:
             status_var = "New Template Created"   
        return status_var
                
    def select_template_name(self, Template_Name, Approval_Note):
        self.Template_Name = Template_Name
        self.Approval_Note = Approval_Note
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.NameFilter,"Name Filter element not found on Webpage in given wait time.")
        mouse.click_on_element(self, 'XPATH', self.NameFilter)
        forms.enter_text_on_element(self, 'XPATH', self.TempNameTextBox, self.Template_Name)
        allure.attach("Selected Template is : "+self.Template_Name,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, 'XPATH', self.TemplateNameSelect)
        # mouse.click_on_element(self, 'XPATH', self.EditRecordBtn)
        mouse.click_on_element(self,'XPATH', self.SubmitForApproval)
        allure.attach("Clicked on Sent for Approval",attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, 'XPATH', self.ApprovalNotesTextBox, self.Approval_Note)
        allure.attach("Submit For Approval note is: "+self.Approval_Note,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, 'XPATH', self.ApprovalSubmitBtn)
        allure.attach("Template sent For Approval",attachment_type=allure.attachment_type.TEXT)

    def select_template_name_to_delete(self, Template_Name,delete_note):
        self.Template_Name = Template_Name
        self.delete_note = delete_note
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.NameFilter,"Name Filter element not found on Webpage in given wait time.")
        mouse.click_on_element(self, 'XPATH', self.NameFilter)
        forms.enter_text_on_element(self, 'XPATH', self.TempNameTextBox, self.Template_Name)
        allure.attach("Template to delete is: "+self.Template_Name,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self, 'XPATH', self.template_checkbox)
        mouse.click_on_element(self, 'XPATH', self.delete_template)
        allure.attach("Clicked on Delete Button",attachment_type=allure.attachment_type.TEXT) 
        self.pop_up_text = forms.get_text_on_element(self,'XPATH',self.delete_popup_text)
        logger.info(self.pop_up_text)
        try:
            assert self.pop_up_text == "Submit For Deletion"
        except AssertionError:
            logger.info("Template need to be in Active Status")
            self.login = Login(self.driver)
            self.login.close_browser()
            exit(0)
        forms.enter_text_on_element(self,'XPATH',self.note,self.delete_note)
        allure.attach("Template Submit For Delete note is: "+self.delete_note,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,'XPATH',self.submit_btn)

    def crossverify_deleted_template(self, Template_Name):
        self.Template_Name = Template_Name
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.NameFilter,"Name Filter element not found on Webpage in given wait time.")
        mouse.click_on_element(self, 'XPATH', self.NameFilter)
        forms.enter_text_on_element(self, 'XPATH', self.TempNameTextBox, self.Template_Name)
        time.sleep(2)
        self.select_template_length = self.driver.find_elements_by_xpath(self.Template_length)
        self.length = len(self.select_template_length)
        logger.info(self.length)
        if self.length == 0:
            try:
                forms.get_text_on_element(self,'XPATH',self.TemplateNameSelect)
            except AttributeError:
                logger.info("Template Deleted")
                allure.attach("Template Deleted successfully: ",attachment_type=allure.attachment_type.TEXT)
        else:
            self.template_name_delete = forms.get_text_on_element(self,'XPATH',self.TemplateNameSelect)
            if self.template_name_delete != self.Template_Name:
                logger.info("Template Deleted")
                allure.attach("Template Deleted successfully: ",attachment_type=allure.attachment_type.TEXT)

    def Approve_Template(self, Template_Name):
        self.page_count = forms.get_text_on_element(self, "XPATH", self.page_count)
        logger.info(self.page_count)
        if int(self.page_count) > 1:
            mouse.click_action_on_element(self,"XPATH",self.last_page)
        self.template_names_xl = Template_Name
        self.template_name_name_list = []
        self.template_name_name_list = self.driver.find_elements_by_xpath(self.Approval_Name_Row)
        logger.info(len(self.template_name_name_list))
        self.list_length = len(self.template_name_name_list)
        for i in range( 1, self.list_length+1):
            self.template_names = "(//div[@class='metadata p-3 float-left']/table/tr[1]/td[2])["+str(i)+"]"
            mouse.scroll_to_element(self,"XPATH",self.template_names)
            self.template_names_ui = forms.get_text_on_element(self, "XPATH", self.template_names)
            logger.info(self.template_names_ui)
            logger.info(self.template_names_xl)
            if self.template_names_ui == self.template_names_xl:
                self.Checkbox = "(//div[@class= 'mt-3']/span/label/input)["+str(i)+"]"
                logger.info("Template name found")
                allure.attach("Template Approved.",attachment_type=allure.attachment_type.TEXT)
                forms.check_checkbox(self, "XPATH", self.Checkbox)
                logger.info("Checkbox Checked")
      
    def click_on_gp_mappings(self):
        mouse.click_action_on_element(self, 'XPATH', self.GPMappings)
        self.main.screen_load_time('File Template->Mapping Screen')

    def click_on_new_mapping(self):
        mouse.click_action_on_element(self, 'XPATH', self.NewMapping)

    def select_new_mapping_details(self, Client, DataType, Source, FileTemplate, FilterName):
        self.Client = Client
        self.DataType = DataType
        self.Source = Source
        self.FileTemplate = FileTemplate
        self.FilterName = FilterName
        forms.select_option_by_text(self, "XPATH", self.client, self.Client)
        allure.attach("Template Mapping Client is: "+self.Client,attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self, "XPATH", self.datatype, self.DataType)
        allure.attach("Template Mapping Data Type is:"+self.DataType,attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self, "XPATH", self.source, self.Source)
        allure.attach("Template Mapping Source is:"+self.Source,attachment_type=allure.attachment_type.TEXT)
        forms.select_option_by_text(self, "XPATH", self.filetemplate, self.FileTemplate)
        allure.attach("Template Mapping File template is:"+self.FileTemplate,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.filtername, self.FilterName)
        allure.attach("Template Mapping Filter is:"+self.FilterName,attachment_type=allure.attachment_type.TEXT)
        
    def click_on_submit_button(self):
        mouse.click_action_on_element(self, "XPATH", self.Submitbutton)
        text_visible = locators.element_exists(self, "XPATH", self.MappingExistText)
        if text_visible == True:
          text = forms.get_text_on_element(self,"XPATH", self.MappingExistText)
          status_var = "Mapping Already exist"
          logger.info("Mapping Already exist")
          allure.attach("Mapping Already exist",attachment_type=allure.attachment_type.TEXT)
        else:
             status_var = "New Mapping Created" 
             logger.info("New Mapping Created")  
             allure.attach("New Mapping Created",attachment_type=allure.attachment_type.TEXT)
        return status_var
    
    """Author : Pooja Jundhare
       Description : This method filter the mapping as per given parameters
       Arguments : xl value list and ui column list 
       Returns : NA""" 
    def filter_mapping(self,value_list,column_list):
        for i in range(0,5):
            logger.info(column_list[i])
            allure.attach("Filter Column is "+column_list[i],attachment_type=allure.attachment_type.TEXT)
            logger.info(value_list[i])
            allure.attach("Value Entered in search box is "+value_list[i],attachment_type=allure.attachment_type.TEXT)
            mouse.click_on_element(self,"XPATH",self.filter_icon.format(column_list[i]))
            forms.enter_text_on_element(self,"XPATH",self.search_box,value_list[i])
            self.main.screen_load_time('Filtering Data')
        
    """Author : Pooja Jundhare
       Description : This method verifies the first row data with xl data and if correct click on checkbox
       Arguments : xl value list and ui column list 
       Returns : NA""" 
    def select_mapping(self,value_list,column_list):
        try:
            for i in range(0,5):
                row_value = forms.get_text_on_element(self,"XPATH",self.row_data.format(column_list[i]))
                allure.attach("Value from UI is "+row_value,attachment_type=allure.attachment_type.TEXT)
                allure.attach("VAlue from XL is "+value_list[i],attachment_type=allure.attachment_type.TEXT)
                logger.info(row_value)
                logger.info(value_list[i])
                assert row_value.upper() == value_list[i].upper(),'GP Mapping does not match'
            forms.check_checkbox(self,"XPATH",self.mapping_checkbox)
            allure.attach("Checkbox checked",attachment_type=allure.attachment_type.TEXT)
        except AttributeError:
            logger.info("No Mapping found on Screen for filtered data")
            allure.attach("No Mapping found on Screen for filtered data",attachment_type=allure.attachment_type.TEXT)
            self.login = Login(self.driver)
            self.login.close_browser()
            exit(0)
            
    """Author : Pooja Jundhare
       Description : This method clicks on delete button of GP mapping screen
       Arguments : NA
       Returns : NA""" 
    def delete_mapping(self):
        self.element = locators.element_is_displayed(self,"XPATH",self.delete_mapping_button)
        logger.info(self.element)
        allure.attach('Delete Mapping button displayed is '+str(self.element),attachment_type=allure.attachment_type.TEXT)
        if self.element == True:
            mouse.click_on_element(self,"XPATH",self.delete_mapping_button)
            self.main.screen_load_time('After clicking on Delete Mapping Button')
            allure.attach('Clicked on Delete Mapping button',attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info('Delete Mapping button does not exist or not enabled')
            allure.attach('Delete Mapping button does not exist or not enabled',attachment_type=allure.attachment_type.TEXT)
    
    """Author : Pooja Jundhare
       Description : This method verifies the first row data with xl data and check check deleted mapping exist or not
       Arguments : xl value list and ui column list 
       Returns : NA"""    
    def verify_mapping(self,value_list,column_list):
        try:
            for i in range(0,5):
                row_value = forms.get_text_on_element(self,"XPATH",self.row_data.format(column_list[i]))
                allure.attach("Value from UI is "+row_value,attachment_type=allure.attachment_type.TEXT)
                allure.attach("VAlue from XL is "+value_list[i],attachment_type=allure.attachment_type.TEXT)
                logger.info(row_value.upper())
                logger.info(value_list[i].upper())
                assert row_value.upper() != value_list[i].upper(),'GP Mapping Matches'
        except AttributeError:
            logger.info("No Mapping found on Screen for filtered data or Mapping is Deleted")
            allure.attach("No Mapping found on Screen for filtered data or Mapping is Deleted",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method select sub menu Global ->price types
       Arguments : screen_name(screen_name="Price Types")
       Returns : NA""" 
    def select_pricetypes_submenu_from_burguer_menu(self):
        self.main.select_gp_option('GLOBAL', sub_item='PRICE TYPES')
        self.main.screen_load_time('GLOBAL->PRICE TYPES Screen')
        allure.attach("User can select global menu and price types as sub menu: ",attachment_type=allure.attachment_type.TEXT)
    

    """Author : Sadiya Kotwal
       Description : This method select sub menu Global ->File templates
       Arguments : screen_name(screen_name="File Templates")
       Returns : NA""" 
    def select_filetemplates_submenu_from_burguer_menu(self):
        self.main.select_gp_option('GLOBAL', sub_item='FILE TEMPLATES')
        self.main.screen_load_time('GLOBAL->FILE TEMPLATES Screen')
        allure.attach("User can select global menu and file templates as sub menu: ",attachment_type=allure.attachment_type.TEXT)

    