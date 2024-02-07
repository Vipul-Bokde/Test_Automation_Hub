from libraries.environment_setup import EnvironmentSetup
from GP.pages.main_page import MainPage
from libraries import mouse, forms
from GP.utilities.logs_util import logger
from libraries import mouse, locators
from selenium.webdriver.common.by import By
import allure
from selenium.common.exceptions import NoSuchElementException
from random import randint
import GP.utilities.csv_utility as CSVUtlty
import json
class NewJoinPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators
        self.AddJoin = "//div[@class='mb-2 float-right']/button[@class='btn btn-outline-secondary']"
        self.source = "//div/select[@formcontrolname='source']"
        self.validation= "//div/input[@id= 'join-validation']"
        self.table = "//div/select[@formcontrolname='target_id']"
        self.alias = "//div/input[@formcontrolname='alias']"
        self.validation_start_date = "//div/input[@formcontrolname='validate_start']"
        self.validation_end_date = "//div/input[@formcontrolname='validate_end']"
        self.condition = "//div/input[@formcontrolname='condition']"
        self.submitbutton = "//div/button[@id='join-submit-btn']"
        self.divrowxpath = "//*[@id='page-container']/join-editor/ag-grid-angular/div/div[1]/div/div[3]/div[2]/div/div/div[2]/div[2]"
        self.cancelbutton = "//*[@id='join-cancel-btn']"
        self.joins_buttons = "//div[@class='mb-2 float-left']//button[contains(.,'{}')]"
        self.file_upload =   "//div/input[@id='upload-file-chooser']"  #"//div[@class='sparq-modal-body']/input[@id='joins-file']"
        self.upload_button = "//div[@class='sparq-modal-footer']/button[@type='submit'][contains(.,'Upload')]"
        self.grid_data = "//div[@class='ag-center-cols-container']/div[@row-id='{}']/div[@col-id='{}']"
        self.inspect_pop_up = "//div[@class='sparq-modal']/div[@class='sparq-modal-header'][contains(.,'Join Inspector')]"
        self.inspect_source = "//div[@class='sparq-modal-body']/select"
        self.inspect_query = "//div[@class='sparq-modal-body']/div[@id='join-inspector-well']"
        self.inspect_pop_up_close = "//div[@class='sparq-modal-footer']/button[@class='btn btn-primary w-75']"
        self.edit_warning_msg = "//div[@class='invalid-feedback']"
        self.action_button = "//div[@class='btn-group']/button[@class='btn btn-outline-secondary']"
        self.actions = "//ul[@class='dropdown-menu dropdown-menu-right show']/li[contains(.,'{}')]"

    def select_global_from_burger_menu(self):
        self.main.select_gp_option('CLIENT', sub_item='JOINS')
        self.main.screen_load_time('CLIENT->JOINS Screen')
        allure.attach("User can select clients menu and joins as sub menu: ",attachment_type=allure.attachment_type.TEXT)
      
    def click_on_button(self,button_name):
        self.main.screen_load_time('Before clicking on '+str(button_name)+' Button')
        self.element = locators.element_is_displayed(self,"XPATH",self.joins_buttons.format(button_name))
        logger.info(self.element)
        allure.attach(str(button_name)+ ' button displayed is '+str(self.element),attachment_type=allure.attachment_type.TEXT)
        if self.element == True:
            mouse.click_on_element(self,"XPATH",self.joins_buttons.format(button_name))
            self.main.screen_load_time('After clicking on '+str(button_name)+' Button')
            allure.attach('Clicked on '+str(button_name)+' button',attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info(+str(button_name)+' button does not exist or not enabled')
            allure.attach(+str(button_name)+' button does not exist or not enabled',attachment_type=allure.attachment_type.TEXT)
        
    def upload_file(self,file_to_upload):
        self.file_to_upload = file_to_upload
        file_up = self.driver.find_element_by_xpath(self.file_upload)
        file_up.send_keys(self.file_to_upload)    
        allure.attach("File to upload is"+self.file_to_upload,attachment_type=allure.attachment_type.TEXT)
    
    def click_on_upload_button(self):
        self.element = locators.element_is_displayed(self,"XPATH",self.upload_button)
        logger.info(self.element)
        allure.attach("Upload button displayed is "+str(self.element),attachment_type=allure.attachment_type.TEXT)
        if self.element == True:
            mouse.click_on_element(self,"XPATH",self.upload_button)
            allure.attach("Clicked on Upload button",attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info("Upload button does not exist or not enabled")    
            allure.attach("Upload button does not exist or not enabled",attachment_type=allure.attachment_type.TEXT)    
    
    def validate_grid_and_exported_join_data(self,dwnld_filpath):
        for item in range (0,5):
            random_no = randint(0,4)
            logger.info("Row no is:"+str(random_no))
            allure.attach("Row no is: "+str(random_no),attachment_type=allure.attachment_type.TEXT)
            # UI Values
            UI_Val_List = []
            source = forms.get_text_on_element(self, "XPATH", self.grid_data.format(random_no,'source'))
            UI_Val_List.append(source)
            table = forms.get_text_on_element(self, "XPATH", self.grid_data.format(random_no,'table'))
            UI_Val_List.append(table)
            enabled = forms.get_text_on_element(self, "XPATH", self.grid_data.format(random_no,'enabled'))
            UI_Val_List.append(enabled)
            validation = forms.get_text_on_element(self, "XPATH", self.grid_data.format(random_no,'validation'))
            UI_Val_List.append(validation)
            condition = forms.get_text_on_element(self, "XPATH", self.grid_data.format(random_no,'condition'))
            UI_Val_List.append(condition)
            logger.info(UI_Val_List)
            UI_Val_List = json.dumps(UI_Val_List)
            allure.attach("UI_Val_List is: "+UI_Val_List,attachment_type=allure.attachment_type.JSON)
            # CSV Values
            csv_column_list = ['Source','Table','Enabled','Validation','Condition']
            CSV_Val_List= CSVUtlty.csvReader(dwnld_filpath,random_no,csv_column_list)
            logger.info(CSV_Val_List)
            CSV_Val_List = json.dumps(CSV_Val_List)
            allure.attach("CSV_Val_List is: "+CSV_Val_List,attachment_type=allure.attachment_type.JSON)
            comparison_result = CSVUtlty.compareLists(UI_Val_List,CSV_Val_List)
            logger.info("Return list comparison is:")
            logger.info(comparison_result)
            assert comparison_result == "Equal", "Downloaded grid file value does not match with UI values"
            
    def select_source(self,source):
        logger.info(source)
        self.element = locators.element_is_displayed(self,"XPATH",self.inspect_pop_up)
        allure.attach("Join Inspector pop-up displayed is "+str(self.element),attachment_type=allure.attachment_type.TEXT)
        if self.element == True:
            forms.select_option_by_text(self,"XPATH",self.inspect_source,source)
            allure.attach("Selected source is "+source,attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info("Join Inspector pop-up does not open")    
            allure.attach("Join Inspector pop-up does not open",attachment_type=allure.attachment_type.TEXT)    
    
    def check_query_visible(self):
        self.query = forms.get_text_on_element(self,"XPATH",self.inspect_query)
        logger.info(self.query)
        if self.query != None:
            allure.attach("Query for selected source is "+self.query,attachment_type=allure.attachment_type.TEXT)
        else:
            allure.attach("Query is not present for selected source source "+self.query,attachment_type=allure.attachment_type.TEXT)

    def close_inspect_pop_up(self):    
        self.element = locators.element_is_displayed(self,"XPATH",self.inspect_pop_up_close)
        logger.info(self.element)
        allure.attach("Inspect Join ->Ok button displayed is "+str(self.element),attachment_type=allure.attachment_type.TEXT)
        if self.element == True:
            mouse.click_on_element(self,"XPATH",self.inspect_pop_up_close)
            allure.attach("Clicked on ok button",attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info("OK button does not exist or not enabled")    
            allure.attach("OK button does not exist or not enabled",attachment_type=allure.attachment_type.TEXT)    
        
    def click_on_new_join(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.AddJoin,"Add join element not found on Webpage in given wait time.")
        mouse.click_action_on_element(self, 'XPATH', self.AddJoin)
        allure.attach("Clicked on Add Join Button",attachment_type=allure.attachment_type.TEXT)  

    def create_new_join(self, Source, Validation, Table, Alias, Val_Start, Val_End, Condition):
        self.Source = Source
        self.Validation = Validation
        self.Table = Table
        self.Alias = Alias
        self.Val_Start  = Val_Start
        self.Val_End = Val_End
        self.Condition = Condition
        forms.select_option_by_text(self, "XPATH", self.source, self.Source)
        forms.check_checkbox(self, "XPATH", self.validation)
        forms.select_option_by_text(self, "XPATH", self.table, self.Table)
        forms.enter_text_on_element(self, "XPATH", self.alias, self.Alias)
        forms.enter_text_on_element(self, "XPATH", self.validation_start_date, self.Val_Start)
        forms.enter_text_on_element(self, "XPATH", self.validation_end_date, self.Val_End)
        forms.enter_text_on_element(self, "XPATH", self.condition, self.Condition)
        allure.attach('Selected values are '+self.Source+','+self.Table+','+self.Alias+','+self.Validation+','+self.Val_Start+','+self.Val_End+','+self.Condition,attachment_type=allure.attachment_type.TEXT)  
       
    def click_on_submit(self):
        mouse.click_action_on_element(self, "XPATH", self.submitbutton)
        allure.attach("Clicked on Submit Button",attachment_type=allure.attachment_type.TEXT)  
        self.main.screen_load_time('CLIENT->JOINS Screen->Submit')
        element = locators.element_is_displayed(self, "XPATH", self.submitbutton)
        warining_msg = locators.element_is_displayed(self,"XPATH",self.edit_warning_msg)
        assert warining_msg == False,"warning message exist"
        allure.attach("warning message exist is "+str(warining_msg),attachment_type=allure.attachment_type.TEXT)
        allure.attach("Submit button still displayed after submission is "+str(element),attachment_type=allure.attachment_type.TEXT)  
        assert element == False,"Not able to submit Added/Edited Join"           
    
# Action Join
    def select_join(self):
        UI_Val_List = []
        row_no = "1"
        source = forms.get_text_on_element(self, "XPATH", self.grid_data.format(row_no,'source'))
        UI_Val_List.append(source)
        table = forms.get_text_on_element(self, "XPATH", self.grid_data.format(row_no,'table'))
        UI_Val_List.append(table)
        alias = forms.get_text_on_element(self, "XPATH", self.grid_data.format(row_no,'alias'))
        UI_Val_List.append(alias)
        condition = forms.get_text_on_element(self, "XPATH", self.grid_data.format(row_no,'condition'))
        UI_Val_List.append(condition)
        logger.info(UI_Val_List)
        UI_Val_List_1 = json.dumps(UI_Val_List)
        allure.attach(" join List is: "+UI_Val_List_1,attachment_type=allure.attachment_type.JSON)
        return UI_Val_List
    
    def check_checkbox(self):
        self.checkbox= "//div[@row-index='1']//span[@class='ag-selection-checkbox']"
        forms.check_checkbox(self, "XPATH", self.checkbox) 
        allure.attach("Checkbox is checked",attachment_type=allure.attachment_type.TEXT)
      
    def check_join_exist_after_action(self,join_list_1,join_list_2):
        if join_list_1 == join_list_2:
            logger.info("Join before and after performing action is same")
            allure.attach("Join before and after performing action is same",attachment_type=allure.attachment_type.TEXT)
        else:
            logger.info("Join before and after performing action is not same or join might be deleted")
            allure.attach("Join before and after performing action is not same or join might be deleted",attachment_type=allure.attachment_type.TEXT)
                 
    def click_action_button(self):
        mouse.click_on_element(self,"XPATH",self.action_button)
        allure.attach("Clicked on Action button",attachment_type=allure.attachment_type.TEXT)

    def select_from_actions_menu(self,action):
        mouse.click_on_element(self,"XPATH",self.actions.format(action))
        allure.attach("Clicked on "+action+" button",attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time("Join-> "+action)
        
    def verify_join_is_disabled(self,hex_code):
        self.hex_code  = hex_code
        self.row_disable_check= "//div[@class='ag-center-cols-container']//div[@row-id='1']"
        self.hex_value= locators.get_css_property_value(self, "XPATH", self.row_disable_check,"background-color")
        logger.info(self.hex_value)
        if self.hex_value == self.hex_code:
                allure.attach("User can see the row is disabled and color is light grey: "+str(self.hex_value),attachment_type=allure.attachment_type.TEXT)
        else:
            assert False, " The row is not disabled"
            
    def verify_join_is_enabled(self,hex_code):
        self.hex_code  = hex_code
        self.row_enabled_check= "//div[@class='ag-center-cols-container']//div[@row-id='1']"
        self.hex_value= locators.get_css_property_value(self, "XPATH", self.row_enabled_check,"background-color")
        logger.info(self.hex_value)
        if self.hex_value == self.hex_code:
                allure.attach("User can see the row is enabled and color is white: "+str(self.hex_value),attachment_type=allure.attachment_type.TEXT)
        else:
            assert False, " The row is not enabled"

    def select_join_to_edit(self):  
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.AddJoin,"Add join element not found on Webpage in given wait time.")
        mouse.click_action_on_element(self, "XPATH", self.divrowxpath)

    def edit_selected_join(self, Source, Alias, Condition):
        self.Source = Source
        self.Alias = Alias
        self.Condition = Condition
        forms.select_option_by_text(self, "XPATH", self.source, self.Source)
        allure.attach("Selected source to edit existing join is "+self.Source,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.alias, self.Alias)
        allure.attach("Selected alias to edit existing join is "+self.Alias,attachment_type=allure.attachment_type.TEXT)
        forms.enter_text_on_element(self, "XPATH", self.condition, self.Condition)
        allure.attach("Selected condition to edit existing join is "+self.Condition,attachment_type=allure.attachment_type.TEXT)
    
    def check_edited_join(self):
        mouse.click_action_on_element(self, "XPATH", self.divrowxpath)
        assert self.source == self.Source,'Source does not match with the edited value'
        assert self.alias == self.Alias,'Alias Does not mach with the edited value'
        assert self.condition == self.Condition,'Condition Does not mach with the edited value'
        
    def click_on_cancel(self):
        mouse.click_action_on_element(self, "XPATH", self.cancelbutton)
        allure.attach("Clicked on cancel button",attachment_type=allure.attachment_type.TEXT)
        self.main.screen_load_time('CLIENT->JOINS Screen->Cancel')
            
