from cmath import log
import imp
import re
# from curses.ascii import TAB
from selenium.webdriver.support.select import Select
from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.main_page import MainPage
from libraries import mapping, mouse, forms, locators,waits_config,dates
from selenium.webdriver.common.keys import Keys
from GP.utilities.logs_util import logger
import allure
from allure_commons.types import AttachmentType
import time
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from GP.utilities.logs_util import logger
from datetime import date
from selenium.webdriver.common.by import By
from libraries import generics


class PriceTypePage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)

        #locators
        self.upload_screen_wait = "//h3[@class='display-4 text-center']"
        self.NewPriceType = "//*[@id='price-type-new-btn']"
        self.NameTextBox = "//div/form/div/div/div/input[@id='price-type-name']"
        self.PriceTypeCategoryDropdown = "//div/select[@id='price-type-category']"
        self.SubmitButton = "//div/button[@id='price-type-submit-btn']"
        self.ExistingPriceTypeText = "//div[@class='invalid-feedback'][contains(text(),'Name is already in use.')]"
        self.rowxpath = "//*[@ref= 'eCenterColsClipper']/div/div/div"
        self.hamburger_Menu =  "//div[@class='float-right mr-2']/div[@class='btn-group']"
        self.import_button = "//div/ul[@class='dropdown-menu dropdown-menu-right show']/li[2]/a/i"
        self.import_file = "//*[@id='price-type-file']"
        self.upload = "//div[@class='sparq-modal-footer']/button[@class='btn submit-btn btn-primary'][contains(text(),'Upload')]"
        self.editor_popup = "//div/h3[@class='hopscotch-title'][contains(text(),'Logic Editor Tab')]"
        self.addingbkt_popup = "//div/h3[@class='hopscotch-title'][contains(text(),'Adding Buckets and Formulas')]"
        self.names_popup = "//div/h3[@class='hopscotch-title'][contains(text(),'Names & Reportable Names')]"
        self.calculation_popup = "//div/h3[@class='hopscotch-title'][contains(text(),'Test Calculations')]"
        self.output_popup = "//div/h3[@class='hopscotch-title'][contains(text(),'Output Tab')]"
        self.undo_popup = "//div/h3[@class='hopscotch-title'][contains(text(),'Undo & Redo)]"
        self.nextButton = "//div/button[@class='hopscotch-nav-button next hopscotch-next']"
        self.restorecolumns = "//div[@id='logic-container']/span[@id='restore-link']"
        # bucket filter column locators
        self.terminalSbmtBtn = "//*[@class='p-3']/div/button[contains(text(),'Submit')]"
        self.execute_Btn = "//*[@id='execute-btn']"
        self.sbmtfrApprovlBtn = "//*[@id='btn-save-record']"
        self.Upload = "//div[@class='sparq-modal-footer']/button[contains(text(),'Upload')]"
        self.approval_note = "//*[@id='approval-note']"
        self.submitBttn_final = "//*[@id='price-type-submit-approval']/div[2]/div[3]/button[1][contains(text(),'Submit')]"
        # Output Tab
        self.Output_Tab = "//a[@class='nav-link']/strong[contains(text(),'Output')]" 
        self.OutputTab_Upload_button = "//div[@class='btn-toolbar']//div/button[@class='btn btn-outline-secondary menu-btn-group']"
        self.Download_Report_Template = "(//li[@class= 'menu-item']/a[@role= 'button'])[2]"
        self.Export = "//div[@class= 'btn-group mr-2']/button[@title='Export']"
        self.template_scan = "//div[@id='alert'][contains(text(),'Your file scanning completed.')]"
        # Changes Tab
        self.Changes_Tab = "//*[@class='nav-link']/strong[contains(text(),'Changes')]"
        self.Modified_by_xpath = "(//*[@class='ag-center-cols-container']/div/div[@col-id='0'])[1]"
        self.Modified_on_xpath = "(//*[@class='ag-center-cols-container']/div/div[@col-id='modified_on'])[1]"
        self.Approved_by_xpath = "(//*[@class='ag-center-cols-container']/div/div[@col-id='1'])[1]"
        self.approved_on_xpath = "//div[@row-index='0']/div[@col-id='approved_on']"
        self.txt_lastest_version_count = "(//div[@col-id='version'])[2]"
        self.tab_revision_history = "//a[@class='nav-link']/child::strong[contains(.,'Revision History')]"
        self.txt_lastest_version_count = "(//div[@col-id='version'])[2]"
        self.tab_revision_history = "//a[@class='nav-link']/child::strong[contains(.,'Revision History')]"
        self.icon_effective_end_date = "(//button[@aria-label='Clear Date']/child::span)[2]"
        self.Modified_by_xpath_for_previous_version_1 = "(//*[@class='ag-center-cols-container']/div/div[@col-id='modified_by'])[2]"
        self.Modified_on_xpath_for_previous_version_1 = "(//*[@class='ag-center-cols-container']/div/div[@col-id='modified_on'])[2]"

        # Create New Price Type
        self.input_effective_start_date = "//my-date-picker[@formcontrolname='effective_start_date']/descendant::div[@class='selectiongroup']/child::input"
        self.calendar_container_effective_start_date = "//my-date-picker[@formcontrolname='effective_start_date']/descendant::div[@class='selectiongroup']/following::div[@class='selector selectorarrow selectorarrowleft']"
        self.txt_today_calendar_effective_start_date ="//div[@class='selector selectorarrow selectorarrowleft']/child::table/child::tr/child::td[2]/descendant::span[contains(text(),'Today')]"
        self.search_box = "//div[@class='ag-input-text-wrapper']/input[@id='filterText']"
        self.btn_export = "//a[contains(.,'Export')]"
        self.btn_upload_report_template = "//li[@class='menu-item']/child::a/input[@type='file']"
        self.btn_run_report = "//button[@title='Run Report'][contains(.,'Run Report')]"
        self.btn_add_logic = "//button[@id='add-logic-btn']"
        self.drp_type_from_add_logic_popup = "//label[text()='Type']/parent::div/child::select2/child::select[@id='logic-type-select']"
        self.txt_add_logic_popup_page = "(//div[contains(.,'Add Logic')])[5]"
        self.drp_name_from_add_logic_popup = "//label[text()='Name']/parent::div/child::select2/child::select[@id='logic-name']"
        self.input_name_from_add_logic_popup = "//input[@role='textbox']"
        self.drp_source_from_add_logic_popup = "//label[text()='Source']/parent::div/child::select2/child::select[@id='bucket-source-select']"
        self.btn_submit_from_add_logic_popup_page = "//div[contains(.,'Add Logic')]/parent::form/child::div/button[@type='submit']"
        self.first_row_first_cell_logic_tab = "(//div[@ref='eCenterContainer']/child::div[@row-index='0']/div)[1]"
        self.btn_actions_from_logic_tab= "//button[contains(.,'Actions')]"
        self.btn_undo_from_logic_tab= "//button[@id='undo-btn']"
        self.btn_redo_from_logic_tab= "//button[@title='Redo']"
        self.btn_changes_from_price_type= "//strong[normalize-space()='Changes']"
        self.get_txt_effective_start_date_from_changes_tab= "(//div[@col-id='Effective_Start']/child::template-renderer/child::span)[1]"
        self.get_txt_effective_end_date_from_changes_tab= "(//div[@col-id='effective_end_date'])[2]"
        self.get_comment_from_changes_tab ="(//div[@col-id='note'])[2]/descendant::span/child::span[2]"
        self.get_version ="(//div[@col-id='version'])[2]"
        self.input_effective_end_date = "//my-date-picker[@formcontrolname='effective_end_date']/descendant::div[@class='selectiongroup']/child::input"
        #case 2
        self.btn_edit_record = "//button[@id='btn-save-record'][contains(.,'Edit Record')]"
        self.icon_pencil_in_changes_tab = "//i[@class='fa fa-pencil text-primary']"
        self.btn_save_for_changes_tab = "(//button[contains(.,'Save')])[1]"
        self.Logic_Tab = "//*[@class='nav-link']/strong[contains(text(),'Logic')]"
        self.icon_note = "(//div[@col-id='notes'])[3]/child::span/child::span[1]"
        self.btn_ok_from_submitter_notes_popup = "(//button[contains(.,'OK')])[4]"
        self.msg_an_error_occuredon_output_tab = "//div[contains(.,'An error occured while generating report')]"
        self.note_msg = "(//div[@row-index='{}']/div[@col-id='notes']//span)[3]"
        self.version_sort = "//div[@col-id='version']//span[@class='ag-icon ag-icon-desc']"

    def select_price_type_editor_from_burger_menu(self):
        self.main.select_gp_option('PRICE TYPE EDITOR')
        self.main.screen_load_time('PRICE TYPE EDITOR')
        allure.attach("User see select price type editor from hamburger menumenu : ",attachment_type=allure.attachment_type.TEXT)

    def click_on_new_price_button(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.NewPriceType,"New Price TYpe element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.NewPriceType)
        self.driver.execute_script("$(arguments[0]).click();", element)
        allure.attach("User can click on new price type button : ",attachment_type=allure.attachment_type.TEXT)

    def add_price_type_name(self, Name):
        self.Name = Name
        forms.enter_text_on_element(self, "XPATH", self.NameTextBox, self.Name)
        allure.attach("Price Type Name : "+self.Name,attachment_type=allure.attachment_type.TEXT)


    def select_price_type_category_from_dropdown(self, Price_type_category):
        self.Price_type_category = Price_type_category
        forms.select_option_by_text(self, "XPATH", self.PriceTypeCategoryDropdown, self.Price_type_category)
        allure.attach("Price Type  Category : "+self.Price_type_category,attachment_type=allure.attachment_type.TEXT)

    def click_on_submit(self):
        mouse.click_on_element(self,"XPATH", self.SubmitButton)
        allure.attach("User can click on submit button from new price type popup page : ",attachment_type=allure.attachment_type.TEXT)
        text_visible = locators.element_exists(self, "XPATH", self.ExistingPriceTypeText)
        if text_visible == True:
          text = forms.get_text_on_element(self,"XPATH", self.ExistingPriceTypeText)
          status_var = "Price Type Name is already in use"
        else:
             status_var = "New Price Type Created"   
        return status_var

# Open Created Price Type

    def select_added_price_type(self,Table_Name):
        self.Table_Name = Table_Name
        self.list_of_elem = []
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.NewPriceType,"New Price Type element not found on Webpage in given wait time.")
        self.list_of_elem = self.driver.find_elements_by_xpath(self.rowxpath)
        logger.info("Element list is:")
        # logger.info(self.list_of_elem)
        logger.info(self.list_of_elem[1])
        logger.info(len(self.list_of_elem))
        self.listLength = len(self.list_of_elem)
        for i in range(self.listLength, 1, -1):
            self.TableList = "//*[@ref= 'eCenterColsClipper']/div/div/div["+str(i)+"]/div[3]"
            self.column_text = forms.get_text_on_element(self, "XPATH", self.TableList)
            logger.info("return value:")
            logger.info(self.column_text)
            if self.column_text == self.Table_Name:
                mouse.double_click_on_element(self, "XPATH", self.TableList)
                logger.info("Selected given price type")
                # mouse.click_on_element(self, "XPATH", self.restorecolumns)
                # logger.info("Column restored to default")
                break
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.editor_popup,"Editor pop up element not found on Webpage in given wait time.")
        self.text = forms.get_text_on_element(self,"XPATH", self.editor_popup)
        logger.info(self.text)
        if self.text == "Logic Editor Tab":
            mouse.click_on_element(self, "XPATH", self.nextButton)
            mouse.click_on_element(self, "XPATH", self.nextButton)
            mouse.click_on_element(self, "XPATH", self.nextButton)
            mouse.click_on_element(self, "XPATH", self.nextButton)
            mouse.click_on_element(self, "XPATH", self.nextButton)
            mouse.click_on_element(self, "XPATH", self.nextButton)
        logger.info("Clicked on Next of Editor pop up")

# Import the price type file
    def click_on_hamburger_Menu(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.hamburger_Menu,"Hamburger menu element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.hamburger_Menu)
        allure.attach("Click on hamburger menu from price type editor : ",attachment_type=allure.attachment_type.TEXT)

    def click_on_import_button(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.import_button,"Import Button element not found on Webpage in given wait time.")
        # mouse.click_on_element(self, "XPATH", self.import_button)
        element = self.driver.find_element_by_xpath(self.import_button)
        self.driver.execute_script("$(arguments[0]).click();", element)
        allure.attach("User can click on import button from hamburger menu price type editor page: ",attachment_type=allure.attachment_type.TEXT)

    def choose_file(self,file_name):
        self.file_name = file_name
        file_up = self.driver.find_element_by_xpath(self.import_file)
        self.filepath = os.getcwd() + "/GP/automation_test/uploadfiles/"+self.file_name+""
        file_up.send_keys(os.getcwd() + "/GP/automation_test/uploadfiles/"+self.file_name+"")
        allure.attach("User can choose file from file popup to import file: "+self.file_name,attachment_type=allure.attachment_type.TEXT)
        allure.attach("file path is : "+self.filepath,attachment_type=allure.attachment_type.TEXT)

    def click_on_upload_button(self):
        element = self.driver.find_element_by_xpath(self.Upload)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Price Type->Upload')
        allure.attach("User can click on upload button from hamburger menu popup: ",attachment_type=allure.attachment_type.TEXT)

# Update the price type

    def click_reportable_flag(self):
        for item in range(1, 4):
            logger.info(item)
            self.reportable_flag = "(//*[@class='ag-center-cols-container']/div/div[@col-id='0']/template-renderer)["+str(item)+"]"
            mouse.click_on_element(self, "XPATH", self.reportable_flag)
            self.main.screen_load_time('Repotable Flag')
            logger.info("Clicked on element")
            allure.attach("User can click reportable flag: "+str(item),attachment_type=allure.attachment_type.TEXT)
            mouse.click_on_element(self,"XPATH",self.restorecolumns)

    def update_bucket_filter(self,Filter_Col_Value_DS,Filter_Col_Value_CBK):
        self.Filter_Col_Value_DS = Filter_Col_Value_DS
        self.Filter_Col_Value_CBK = Filter_Col_Value_CBK
        self.count = 0
        self.slider = "//*[@id='top-container']/split/split-gutter"
        self.element = self.driver.find_element_by_xpath(self.slider)
        logger.info("Slider element is:")
        logger.info(self.element)
        actions = ActionChains(self.driver)
        actions.drag_and_drop_by_offset(self.element, 500, 0).perform()
        for item in range(1, 20):
            # At first validate the value of type column, if it is Bucket type then edit the filter column value
            try:
                self.type = "(//*[@class='ag-center-cols-container']/div/div[@col-id='type'])["+str(item)+"]"   
                self.text = forms.get_text_on_element(self,"XPATH", self.type)
                logger.info("text of type is when bucket filter is running:-")
                logger.info(self.text)
                if self.text == "Bucket (DS)" or self.text == "Bucket (CBK)":
                    logger.info("Starting editing of bucket filter")
                    self.bucket_filter = "(//*[@class='ag-center-cols-container']/div/div[@col-id='filter'])["+str(item)+"]"
                    element = self.driver.find_element_by_xpath(self.bucket_filter)
                    self.driver.execute_script("$(arguments[0]).click();", element)
                    # Editing of terminal value
                    self.terminal = "//*[@class='CodeMirror-code']"
                    self.terminal1="//*[@class=' CodeMirror-line ']"
                    # Fetch no of code lines and perform click on last line
                    self.element_2 = self.driver.find_elements_by_xpath(self.terminal1)
                    self.linelen = len(self.element_2)
                    self.lastlinexpath = "(//*[@class=' CodeMirror-line '])["+str(self.linelen)+"]"
                    mouse.click_on_element(self, "XPATH", self.lastlinexpath)
                    # Fetch length of available characters on terminal and perform backspace
                    self.valuelen = len(forms.get_text_on_element(self,"XPATH", self.terminal))
                    if self.text == "Bucket (DS)":
                        actions = ActionChains(self.driver)
                        actions.send_keys(self.valuelen*Keys.BACKSPACE)
                        actions.send_keys(self.valuelen*Keys.DELETE)
                        actions.send_keys(self.Filter_Col_Value_DS)
                        allure.attach("User can update bucket filter for DS: "+self.Filter_Col_Value_DS,attachment_type=allure.attachment_type.TEXT)
                        actions.perform()
                    elif self.text == "Bucket (CBK)":
                        actions = ActionChains(self.driver)
                        actions.send_keys(self.valuelen*Keys.BACKSPACE)
                        actions.send_keys(self.valuelen*Keys.DELETE)
                        actions.send_keys(self.Filter_Col_Value_CBK)
                        allure.attach("User can update bucket filter for CBK: "+self.Filter_Col_Value_CBK,attachment_type=allure.attachment_type.TEXT)
                        actions.perform()
                    mouse.click_on_element(self, "XPATH", self.terminalSbmtBtn)
                    self.count = self.count +1
                if self.count == 3:
                    break
            except AttributeError as ae:
                break
        

    def update_dollar_unit_logic(self,dollarLogic,unitLogic):
        self.dollarLogic = str(dollarLogic)
        self.unitLogic = str(unitLogic)
        logger.info("Value of Column var is:")
        self.count = 0
        for item in range(1, 20):
            try:
                self.type = "(//*[@class='ag-center-cols-container']/div/div[@col-id='type'])["+str(item)+"]"
                self.main.screen_load_time('Price Tppe Editor->Type Column')
                self.text = forms.get_text_on_element(self,"XPATH", self.type)
                if self.text == "Formula":
                    logger.info("Selected Formula record")
                    self.dollar_logic = "(//*[@class='ag-center-cols-container']/div/div[@col-id='dollars_value'])["+str(item)+"]"
                    forms.enter_text_press_enter_and_tab(self,"XPATH",self.dollar_logic,dollarLogic)
                    time.sleep(3)
                    allure.attach("User can update dollar logic as: "+self.dollarLogic,attachment_type=allure.attachment_type.TEXT)
                    self.unit_logic = "(//*[@class='ag-center-cols-container']/div/div[@col-id='units_value'])["+str(item)+"]"
                    forms.enter_text_press_enter_and_tab(self,"XPATH",self.unit_logic,unitLogic)
                    time.sleep(5)
                    allure.attach("User can update unit logic as: "+self.unitLogic,attachment_type=allure.attachment_type.TEXT)
                    self.count = self.count +1
                if self.count == 2:
                    break
            except AttributeError as ae:
                break

    def click_onexecute_submit(self,comment):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.execute_Btn,"Execute Button element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.execute_Btn)
        allure.attach("User can click on execute button fom price type editor: ",attachment_type=allure.attachment_type.TEXT)
        element = self.driver.find_element_by_xpath(self.sbmtfrApprovlBtn)
        self.driver.execute_script("$(arguments[0]).click();", element)
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.approval_note,"Approval note element not found on Webpage in given wait time.")
        forms.enter_text_on_element(self, "XPATH", self.approval_note, comment)
        element = self.driver.find_element_by_xpath(self.submitBttn_final)
        self.driver.execute_script("$(arguments[0]).click();", element)

# Download the report template from Output tab and export
    def click_on_output_tab(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Output_Tab,"Output Tab element not found on Webpage in given wait time.")
        element = self.driver.find_element_by_xpath(self.Output_Tab)
        logger.info(element)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Price Type Editor->Output tab')
        logger.info("Clicked on Output tab")

    def click_on_output_tab_hamburger_button(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.OutputTab_Upload_button,"Output Tab upload element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.OutputTab_Upload_button)
        logger.info("Clicked on Hamburger menu button on Output tab")

    def click_on_download_report_template(self):
        mouse.click_on_element(self, "XPATH", self.OutputTab_Upload_button)
        mouse.click_on_element(self, "XPATH", self.Download_Report_Template)
        self.main.screen_load_time('Price Type Editor->Output tab->Download Report Template')
        logger.info("Clicked on Download report template tab")
        allure.attach("User can click on download report template button from output tab : ",attachment_type=allure.attachment_type.TEXT)

    def click_on_export_button(self):
        element = self.driver.find_element_by_xpath(self.Export)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time('Price Type Editor->Output tab->Export')
        logger.info("Clicked on Export button")
        allure.attach("User can click on export button from output tab : ",attachment_type=allure.attachment_type.TEXT)

# Confirm revision history post approval of price type
    def click_on_changes_tab(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.Changes_Tab,"Changes Tab element not found on Webpage in given wait time.")
        # element = self.driver.find_element_by_xpath(self.Changes_Tab)
        # self.driver.execute_script("$(arguments[0]).click();", element)
        mouse.click_js_on_element(self, By.XPATH, self.Changes_Tab)
        logger.info("Clicked on Changes tab")
        self.main.screen_load_time('Price Type Editor->Changes Tab')
        allure.attach("User can click on changes tab : ",attachment_type=allure.attachment_type.TEXT)

    def confirm_history(self,Modified_by_xl,Approved_by_xl,comment,effective_start_date,effective_end_date,version):
        self.modified_by_xl = Modified_by_xl
        self.approved_by_xl = Approved_by_xl
        self.comment = comment
        self.version = version
        self.effective_start_date = effective_start_date
        self.effective_end_date = effective_end_date
        logger.info("XL modified by "+self.modified_by_xl)
        logger.info("XL Approved by "+self.approved_by_xl)
        self.modified_on_xl = MainPage.get_system_current_date(self,"%Y-%m-%d")
        logger.info(self.modified_on_xl)
        logger.info(type(self.modified_on_xl))
        # self.modified_on_xl = date.today()
        self.approved_on_xl = MainPage.get_system_current_date(self,"%Y-%m-%d")
        logger.info(self.approved_on_xl)
        logger.info(type(self.approved_on_xl))
        self.modified_by = forms.get_text_on_element(self,"XPATH",self.Modified_by_xpath)
        logger.info("UI modified by "+self.modified_by)
        self.modified_on = forms.get_text_on_element(self,"XPATH",self.Modified_on_xpath)
        self.approved_by = forms.get_text_on_element(self,"XPATH",self.Approved_by_xpath)
        logger.info("UI approved by "+self.approved_by)
        self.approved_on = forms.get_text_on_element(self,"XPATH",self.approved_on_xpath)
        self.get_text_effective_start_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_start_date_from_changes_tab)
        self.get_text_effective_end_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_end_date_from_changes_tab)
        self.get_comment = forms.get_text_on_element(self, "XPATH", self.get_comment_from_changes_tab)
        self.get_version = forms.get_text_on_element(self, "XPATH",  self.get_version)
        allure.attach("Price Type Modified By On UI: "+self.modified_by,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type Approved By  on UI: "+self.approved_by,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type Modified On for UI: "+self.modified_on,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type Approved On  for UI: "+self.approved_on,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type effective start date On UI: "+self.get_text_effective_start_date,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type effective end date On UI: "+self.get_text_effective_end_date,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type comments On UI: "+self.get_comment,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type version On UI: "+self.get_version,attachment_type=allure.attachment_type.TEXT)
        assert str(self.modified_by) == str(self.modified_by_xl) , "Modified_by does not match"
        assert str(self.modified_on) == str(self.modified_on_xl) , "modified_on does not match"
        assert str(self.approved_by) == str(self.approved_by_xl) , "approved_by does not match"
        assert str(self.approved_on) == str(self.approved_on_xl) , "approved_on does not match"
        assert str(self.get_text_effective_start_date) == str(self.effective_start_date) , "Effective start date does not match"
        assert str(self.get_text_effective_end_date) == str(self.effective_end_date) , "Effective end date does not match"
        assert str(self.get_comment) == str(self.comment) , "comment does not match"
        assert str(self.get_version) == str(self.version) , "version does not match"
        
    """Author : Sadiya Kotwal
       Description : This method clicks on input box for effective start date
                     Screen: Price Type editor > New Price Type Popup Screen > Calender Field : Effective Start Date
       Arguments :
       Returns : NA"""
    def click_on_effective_start_date_input(self):
        mouse.click_on_element(self,"XPATH", self.input_effective_start_date)
        allure.attach("User can click on effective start date calendar: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method select today button from calender
                     Screen: Price Type editor > New Price Type Popup Screen > Calender Field : Effective Start Date
       Arguments :
       Returns : NA"""
    def select_today_from_calendar(self):
        self.bln_flag_calendar_container_exists=False
        self.bln_flag_calendar_container_exists = locators.element_is_displayed(self, "XPATH", self.calendar_container_effective_start_date)
        if self.bln_flag_calendar_container_exists == True:
            mouse.click_on_element(self,"XPATH", self.txt_today_calendar_effective_start_date)
        else:
            assert self.bln_flag_calendar_container_exists , "Calendar Popup Not Visible"
            allure.attach("User cannot see calendar popup: ",attachment_type=allure.attachment_type.TEXT)   
    
    """Author : Sadiya Kotwal
       Description : This method waits for screen to load depends on hamburger menu
                     Screen: Price Type editor > 
       Arguments : hamburger_menu(hamburger_menu='Price Type editor')
       Returns : NA"""
    def wait_for_screen_to_load(self,hamburger_menu):
        self.hamburger_menu =hamburger_menu
        self.main.screen_load_time(self.hamburger_menu+" "+"Screen")

    """Author : Sadiya Kotwal
       Description : This method click on any filter icon
       Arguments : Column Name (Eg: File Name)
       Returns : NA"""
    def click_on_any_filter_icon(self,column_name):
        self.column_name = column_name
        MainPage.click_on_any_filter_icon(self,self.column_name)

    """Author : Sadiya Kotwal
       Description : This method enter data into the filter search box
       Arguments : Filter Text (Eg: journey_med_amp.csv)
       Returns : NA"""
    def enter_text_on_any_filter_icon_searchbox(self,filter_text):
        self.filter_text = filter_text
        MainPage.enter_text_on_any_filter_icon_search_box(self,self.filter_text)

    """Author : Sadiya Kotwal
       Description : This method clicks on upload page
       Arguments : Filter Text (Eg: journey_med_amp.csv)
       Returns : NA"""
    def click_on_uploads_page(self,page_name):
        self.txt_page_name= page_name
        MainPage.click_on_any_screen_text(self,self.txt_page_name)
    
    """Author : Sadiya Kotwal
       Description : This method 
       Arguments : file_name (Eg: journey_med_amp.csv)
       Returns : NA"""
    def verify_file_is_uploaded(self,file_name):
        self.file_name = file_name
        self.bln_flag_element= False
        self.txt_file_name_and_user_name = "(//div[@col-id='filename'][text()='"+self.file_name+"'])[1]"
        self.bln_flag_element= locators.element_is_displayed(self,"XPATH",self.txt_file_name_and_user_name)
        logger.info(self.bln_flag_element)
        logger.info(self.txt_file_name_and_user_name)
        if self.bln_flag_element==True:
            allure.attach("User can see file is uploaded in uploads screen : "+self.file_name,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag_element, "User is not able to see uploaded file"

    """Author : Sadiya Kotwal
       Description : This method verify if price type is created or not
                     Screen: Price Type editor 
       Arguments : price_type(price_type='Test_AMP')
       Returns : NA"""
    def verify_price_type_created(self,price_type):
        self.price_type = price_type
        self.bln_flag_price_type = False
        self.txt_verify_price_type = "//div[@col-id='name'][text()='"+self.price_type+"']"
        self.bln_flag_price_type = locators.element_is_displayed(self, "XPATH", self.txt_verify_price_type)
        if self.bln_flag_price_type==True:
            allure.attach("Price type created is : "+self.price_type,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag_price_type ,"Price type created is not displayed"
            allure.attach("User cannot Price type created : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method verify if user can click on export button
                     Screen: Price Type editor > hamburger menu 
       Arguments : 
       Returns : NA"""
    def click_on_export_button_from_burger_menu(self):
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.btn_export,"Import Button element not found on Webpage in given wait time.")
        mouse.click_on_element(self, "XPATH", self.btn_export)
        allure.attach("User can click on export button from hamburger menu: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method verify if user can click on column name
                     Screen: Price Type editor > output tab 
       Arguments : 
       Returns : NA"""
    def click_on_column_name(self,column_name):
        self.column_name= column_name
        MainPage.click_on_any_screen_text(self,self.column_name)
    
    """Author : Sadiya Kotwal
       Description : This method verify if user can click on column name
                     Screen: Price Type editor >Price Type > output tab 
       Arguments : 
       Returns : NA"""
    def verify_bucket_is_displayed(self,bucket_name):
        self.bucket_name = bucket_name
        self.bln_flag_element= False
        self.verify_bucket_name = "(//div[@col-id='name'][text()='"+self.bucket_name+"'])[1]"
        self.bln_flag_element= locators.element_is_displayed(self,"XPATH",self.verify_bucket_name)
        logger.info(self.bln_flag_element)
        logger.info(self.bucket_name)
        if self.bln_flag_element==True:
            allure.attach("User can see bucket on screen : "+self.bucket_name,attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag_element, "User cannot see bucket on screen"
    
    """Author : Sadiya Kotwal
       Description : This method verify if user can click on hamburger menu from output tab
                     Screen: Price Type editor >Price Type > output tab 
       Arguments : 
       Returns : NA"""
    def click_on_hamburger_menu_from_output_tab(self):
        mouse.click_on_element(self, "XPATH", self.OutputTab_Upload_button)
        allure.attach("User can see click on hamburger menu from output tab screen : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method can click on add logic button from logic tab
                     Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : 
       Returns : NA"""
    def click_on_add_logic_button_from_logic_tab(self):
        mouse.click_on_element(self, "XPATH", self.btn_add_logic)
        allure.attach("User can see click on add logic button : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method selects type option from add logic button popup page
                     Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page > Field Type(Dropdown)
       Arguments : type_name(Eg: type_name="Bucket" or "Formula")
       Returns : NA"""
    def select_type_from_add_logic_popup_page(self,type_name):
        self.type_name = type_name
        forms.select_option_by_text(self, "XPATH", self.drp_type_from_add_logic_popup, self.type_name)
        allure.attach("User can select type from add logic popup page : "+self.type_name,attachment_type=allure.attachment_type.TEXT)
    
    """Author : Sadiya Kotwal
       Description : This method clicks on text add logic from add logic button popup page
                     Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page 
       Arguments : 
       Returns : NA"""
    def click_on_add_logic_text_from_add_logic_popup_page(self):
        mouse.click_on_element(self, "XPATH", self.txt_add_logic_popup_page)
        allure.attach("User can click on add logic text from popup page : ",attachment_type=allure.attachment_type.TEXT)
    
    """Author : Sadiya Kotwal
       Description : This method clicks on name dropdown from add logic button popup page
                     Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page 
       Arguments : 
       Returns : NA"""
    def click_on_name_dropdown_from_add_logic_popup_page(self):
        mouse.click_action_on_element(self, "XPATH", self.drp_name_from_add_logic_popup)
        allure.attach("User can click on name field dropdown from popup: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method enters name for bucket and formula and selects name from dropdown 
                    from add logic button popup page
                    Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page 
       Arguments : name(name = "Test_Bucket" or "Test_formula")
       Returns : NA"""
    def add_name_for_bucket_and_formula_logic(self, name):
        self.name = name
        forms.enter_text_on_element(self, "XPATH", self.input_name_from_add_logic_popup, self.name)
        self.input_name_field= "//ul[contains(@id,'logic-name-results')]//li[text()='"+self.name+"']"
        mouse.click_on_element(self, "XPATH", self.input_name_field)
        allure.attach("Name added is : "+self.name,attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on source dropdown from add logic button popup page
                    Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page 
       Arguments : source_name(source_name = "Direct Sales")
       Returns : NA"""
    def click_source_dropdown_from_add_logic_popup_page(self,source_name):
        self.source_name = source_name
        forms.select_option_by_text(self, "XPATH",  self.drp_source_from_add_logic_popup, self.source_name)
        allure.attach("User can click on source dropdown from add logic popup page : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method enter source for bucket dropdown from add logic button popup page
                    Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page 
       Arguments : source_name(source_name = "Direct Sales")
       Returns : NA"""
    def add_source_for_bucket_logic(self, bucket_source_name):
        self.bucket_source_name = bucket_source_name
        forms.enter_text_on_element(self, "XPATH", self.input_name_from_add_logic_popup, self.bucket_source_name)
        self.bucket_source = "//ul[contains(@id,'bucket-source-select-results')]//li[text()='"+self.bucket_source_name+"']"
        mouse.click_on_element(self, "XPATH", self.bucket_source)
        allure.attach("Bucket Source added is : "+self.bucket_source_name,attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on submit button from add logic button popup page
                    Screen: Price Type editor >Price Type > Logic Tab > Add logic popup page 
       Arguments : 
       Returns : NA"""
    def click_submit_button_from_add_logic_popup_page(self):
        mouse.click_on_element(self, "XPATH", self.btn_submit_from_add_logic_popup_page)
        self.main.screen_load_time('PRICE TYPE EDITOR')
        allure.attach("User can click on submit button from add logic popup page : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on checkbox from logic tab
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : checkbox_name(checkbox_name="Test_Bucket")
       Returns : NA"""
    def click_on_checkbox_from_logic_tab(self,checkbox_name):
        self.checkbox_name = checkbox_name
        self.chkbox_logic_tab= "//div[text()='"+self.checkbox_name+"']/parent::div/child::div/child::span/child::span[@class='ag-selection-checkbox']"
        mouse.click_on_element(self, "XPATH", self.chkbox_logic_tab)
        allure.attach("User can click on checkbox from logic tab : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on action button from logic tab
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : 
       Returns : NA"""
    def click_on_action_button_from_logic_tab(self):
        mouse.click_on_element(self, "XPATH", self.btn_actions_from_logic_tab)
        allure.attach("User can click actions button from logic tab : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on any button from actions menu
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : button_name(button_name="Enable or Disable or Delete")
       Returns : NA"""
    def click_on_any_button_from_action_buttons_menu(self,button_name):
        self.button_name = button_name
        self.btn_action = "//div[@class='btn-group show']/child::ul/child::li[@class='menu-item']/a[contains(.,'"+self.button_name+"')]"
        mouse.click_on_element(self, "XPATH", self.btn_action )
        allure.attach("User can click  on "+self.button_name+" button from actions button menu : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method verify the color and background is disabled
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : name(name="Test_Bucket")
       Returns : NA"""
    def verify_background_color_of_disabled_field_and_verify_field_disabled(self,name,hex_code):
        self.name = name
        self.hex_code  = hex_code
        self.row_diable_check= "(//div[@row-id='"+self.name+"'])[2]"
        self.hex_value= locators.get_css_property_value(self, "XPATH", self.row_diable_check,"background-color")
        if self.hex_value == self.hex_code:
                allure.attach("User can see the row "+self.name+" is disabled and color is light grey: "+str(self.hex_value),attachment_type=allure.attachment_type.TEXT)
        else:
            assert False, " The row is not disabled"

    """Author : Sadiya Kotwal
       Description : This method verify the color and background is enabled
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : name(name="Test_Bucket")
       Returns : NA"""
    def verify_background_color_of_enabled_field_and_verify_field_enabled(self,name,hex_code):
        self.name = name
        self.hex_code  = hex_code
        self.row_diable_check= "(//div[@row-id='"+self.name+"'])[2]"
        self.hex_value= locators.get_css_property_value(self, "XPATH", self.row_diable_check,"background-color")
        if self.hex_value == self.hex_code:
                allure.attach("User can see the row "+self.name+" is enabled and color is white: "+self.hex_value,attachment_type=allure.attachment_type.TEXT)
        else:
            assert False, " The row is not enabled"

    """Author : Sadiya Kotwal
       Description : This method click on undo button
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : 
       Returns : NA"""
    def click_on_undo_button(self):
        mouse.click_on_element(self, "XPATH", self.btn_undo_from_logic_tab)
        allure.attach("User can click undo button from logic tab : ",attachment_type=allure.attachment_type.TEXT)        
    
    """Author : Sadiya Kotwal
       Description : This method click on redo button
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments :
       Returns : NA"""
    def click_on_redo_button(self):
        mouse.click_on_element(self, "XPATH", self.btn_redo_from_logic_tab)
        allure.attach("User can click redo button from logic tab : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method verify the bucket and formula
                    Screen: Price Type editor >Price Type > Logic Tab 
       Arguments : name(name="Test_Bucket")
       Returns : NA"""
    def verify_bucket_and_formula_is_displayed(self,name):
        self.name = name
        self.bln_flag_element= False
        self.verify_bucket_and_formula_name = "(//div[@row-id='"+self.name+"'])[2]"
        self.bln_flag_element= locators.element_is_displayed(self,"XPATH",self.verify_bucket_and_formula_name)
        if self.bln_flag_element==True:
            allure.attach("User can see "+self.name+"  on screen: ",attachment_type=allure.attachment_type.TEXT)
        else:
            assert self.bln_flag_element, "User cannot see "+self.name+" on screen"

    """Author : Sadiya Kotwal
       Description : This method get_effective_start date
                    Screen: Price Type editor >Price Type > Changes Tab Tab 
       Arguments : 
       Returns : NA"""
    def get_effective_start_date(self):
        self.get_text_effective_start_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_start_date_from_changes_tab)
        allure.attach("User can get effective start date as : "+self.get_text_effective_start_date,attachment_type=allure.attachment_type.TEXT)
        return self.get_text_effective_start_date

    """Author : Sadiya Kotwal
       Description : This method get_effective_end_date
                    Screen: Price Type editor >Price Type > Changes Tab Tab 
       Arguments : 
       Returns : NA"""
    def get_effective_end_date(self):
        self.get_text_effective_end_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_end_date_from_changes_tab)
        allure.attach("User can get effective end date as: "+self.get_text_effective_end_date,attachment_type=allure.attachment_type.TEXT)
        return self.get_text_effective_end_date
    
    """Author : Sadiya Kotwal
       Description : This method used to upload the template file 
                     Screen: Price Type editor >Price Type > output tab 
       Arguments : file_name(file_name="Democlient AMP Report_template.xlsm")
       Returns : NA"""
    def choose_file_in_output_tab_for_template_upload(self,file_name):
        self.file_name = file_name
        file_up = self.driver.find_element_by_xpath(self.btn_upload_report_template)
        self.filepath = os.getcwd() + "/GP/TestData/DownloadFiles/"+self.file_name+""
        file_up.send_keys(os.getcwd() + "/GP/TestData/DownloadFiles/"+self.file_name+"")
        self.main.screen_load_time('PRICE TYPE EDITOR->Report Template Upload')
        locators.wait_until_visibility_of_element(self,'XPATH',self.template_scan)
        mouse.click_on_element(self, "XPATH", self.OutputTab_Upload_button)
        allure.attach("User can click on upload file template button : "+self.file_name,attachment_type=allure.attachment_type.TEXT)
        allure.attach("file path is : "+self.filepath,attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method used click on run report button
                     Screen: Price Type editor >Price Type > output tab 
       Arguments : 
       Returns : NA"""
    def click_on_run_report_button(self):
        mouse.click_on_element(self, "XPATH", self.btn_run_report)
        allure.attach("User can click on run report button from output tab : ",attachment_type=allure.attachment_type.TEXT)
        self.bln_flag_msg= locators.element_is_displayed(self,"XPATH",self.msg_an_error_occuredon_output_tab)
        if self.bln_flag_msg==True:
            assert False, "An error occured while generating report msg popup appears"
        else:
            pass
        
    """Author : Sadiya Kotwal
       Description : This method is used to wait for 4 sec
       Arguments : 
       Returns : NA"""
    def wait_for_min_time(self):
        locators.wait_implicite(self,waits_config.MAX_IMPLICIT_TIMEOUT)

    """Author : Sadiya Kotwal
       Description : This method clicks input box of effective end date field
                     Screen: Price Type editor > New Price Type Popup Screen > Calender Field : Effective End Date
       Arguments :
       Returns : NA"""
    def click_on_effective_end_date_input(self):
        mouse.click_on_element(self,"XPATH", self.input_effective_end_date)
        allure.attach("User can click on effective end date calendar: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method select date as mont year and date from calender popup
                     Screen: Price Type editor > New Price Type Popup Screen > Calender Field : Effective End Date,Effective Start Date
       Arguments :
       Returns : NA"""
    def select_date_from_calender(self,date_format):
        self.date_format = date_format
        dates.select_date_from_calender(self,self.date_format)

    """Author : Sadiya Kotwal
       Description : This method clicks on edit button
                     Screen: Price Type editor > Logic tab  > edit button
       Returns : NA"""
    def click_on_edit_button_from_logic_tab(self):
        mouse.click_on_element(self,"XPATH", self.btn_edit_record)
        allure.attach("User can click on edit button: ",attachment_type=allure.attachment_type.TEXT)

       
    """Author : Sadiya Kotwal
       Description : This method verify price type is in edit mode
       Arguments : 
       Returns : NA"""
    def verify_price_type_is_in_edit_mode_with_pencil_icon(self):
        self.bln_flag_element= locators.element_is_displayed(self,"XPATH",self.icon_pencil_in_changes_tab)
        if self.bln_flag_element==True:
            allure.attach("User can see pencil icon which means price type is in edit mode: ",attachment_type=allure.attachment_type.TEXT)

        else:
            assert self.bln_flag_element, "User is not able to see pencil icon which means price type is not in edit mode"
    

    """Author : Sadiya Kotwal
       Description : This method clicks on edit pencil button
                     Screen: Price Type editor > Changes tab  > edit button
       Returns : NA"""
    def click_on_pencil_icon(self):
        mouse.click_on_element(self,"XPATH", self.icon_pencil_in_changes_tab)
        allure.attach("User can click on edit button: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method get_effective_start date of any version
                    Screen: Price Type editor >Price Type > Changes Tab Tab 
       Arguments : version_no(Eg: version_no='1' or '2')
       Returns : Effective Start Date(self.get_text_effective_start_date='1900-01-01')"""
    def get_effective_start_date_of_any_version(self,version_no):
        self.version_no = version_no
        self.get_txt_effective_start_date_from_changes_tab_for_version= "(//div[text()='"+self.version_no+"']//following-sibling::div[@col-id='Effective_Start'])[1]"
        self.get_text_effective_start_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_start_date_from_changes_tab_for_version)
        allure.attach("User can get effective start date as : "+self.get_text_effective_start_date,attachment_type=allure.attachment_type.TEXT)
        return self.get_text_effective_start_date
    
    """Author : Sadiya Kotwal
       Description : This method get_effective_end_date_of_any_version of any version
                    Screen: Price Type editor >Price Type > Changes Tab Tab 
       Arguments :  version_no(Eg: version_no='1' or '2')
       Returns : Effective End Date(self.get_text_effective_end_date='2099-12-31')"""
    def get_effective_end_date_of_any_version(self,version_no):
        self.version_no = version_no
        self.get_txt_effective_end_date_from_changes_tab_for_version= "(//div[text()='"+self.version_no+"']//following-sibling::div[@col-id='effective_end_date'])[1]"
        self.get_text_effective_end_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_end_date_from_changes_tab_for_version)
        allure.attach("User can get effective end date as : "+self.get_text_effective_end_date,attachment_type=allure.attachment_type.TEXT)
        return self.get_text_effective_end_date
    
    """Author : Sadiya Kotwal
       Description : This method clicks on save button
                     Screen: Price Type editor > Changes tab  > Save button
       Returns : NA"""
    def click_on_save_button(self):
        mouse.click_on_element(self,"XPATH", self.btn_save_for_changes_tab)
        self.main.screen_load_time("Save Effective Dates")
        allure.attach("User can click on save button: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on edit button
                     Screen: Price Type editor > Changes tab  > edit button
       Returns : NA"""
    def click_on_logic_tab(self):
        mouse.click_on_element(self,"XPATH", self.Logic_Tab)
        self.main.screen_load_time("Logic Tab")
        allure.attach("User can click on logic tab: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method clicks on submitt button for approval 
                     Screen: Price Type editor > Logic tab  > Submitt button
       Returns : NA"""
    def click_on_submit_for_approval_button(self,comment):
        element = self.driver.find_element_by_xpath(self.sbmtfrApprovlBtn)
        self.driver.execute_script("$(arguments[0]).click();", element)
        MainPage.wait_until_element_is_present(self, 60, By.XPATH, self.approval_note,"Approval note element not found on Webpage in given wait time.")
        forms.enter_text_on_element(self, "XPATH", self.approval_note, comment)
        element = self.driver.find_element_by_xpath(self.submitBttn_final)
        self.driver.execute_script("$(arguments[0]).click();", element)
        self.main.screen_load_time("Clicked on Submit for Sent For Approval")
        allure.attach("User can submit for approval: "+comment,attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method get_effective_start date
                    Screen: Price Type editor >Price Type > Changes Tab Tab 
       Arguments : version_no(Eg: version_no='1' or '2')
       Returns : Effective Start Date(self.get_text_effective_start_date='1900-01-01')"""
    def get_effective_start_date_of_any_version_for_edit_mode(self,version_no):
        self.version_no = version_no
        self.get_txt_effective_start_date_from_changes_tab_for_edit= "(//div[text()='"+self.version_no+"']//following-sibling::div[@col-id='Effective_Start']/descendant::span)[1]"
        self.get_text_effective_start_date= forms.get_text_on_element(self, "XPATH", self.get_txt_effective_start_date_from_changes_tab_for_edit)
        allure.attach("User can get effective start date as for edit mode: "+self.get_text_effective_start_date,attachment_type=allure.attachment_type.TEXT)
        return self.get_text_effective_start_date
    

    """Author : Sadiya Kotwal
       Description : This method verify price type previous version note
       Arguments : calulatd_effective_end_date_of_previous_version(calulatd_effective_end_date_of_previous_version='Updated as')
                    version_no(version_no=1)
       Returns : NA"""
    def verify_previous_version_note(self,calulatd_effective_end_date_of_previous_version,version_no):
        self.next_version_effective_start_date = calulatd_effective_end_date_of_previous_version
        self.version_no = version_no
        logger.info(self.next_version_effective_start_date)
        logger.info(self.version_no)
        mouse.click_on_element(self,"XPATH",self.version_sort)
        self.get_note = forms.get_text_on_element(self, "XPATH", self.note_msg.format(int(self.version_no)-1))
        logger.info(self.get_note)
        logger.info("Updated Effective End Date to "+self.next_version_effective_start_date+" upon version "+str(self.version_no)+"'s approval.")
        assert self.get_note == "Updated Effective End Date to "+self.next_version_effective_start_date+" upon version "+str(self.version_no)+"'s approval.","Note is not correct for version  "+self.version_no
        allure.attach("User can see note as: "+self.get_note,attachment_type=allure.attachment_type.TEXT)
        mouse.click_on_element(self,"XPATH", self.btn_ok_from_submitter_notes_popup)
    
    """Author : Sadiya Kotwal
       Description : This method calculate the previous version eff end date
       Arguments : next_version_effective_start_date(next_version_effective_start_date='2023-05-31')
                    version_no(version_no=2)
       Returns : updated_effective_end_date_for_previous_version(updated_effective_end_date_for_previous_version='2023-05-30')"""
    def calculate_effective_end_date(self,next_version_effective_start_date,version_no):
        self.next_version_effective_start_date = next_version_effective_start_date
        self.version_no = version_no
        self.split_effective_start_date = self.next_version_effective_start_date.split("-")
        self.year = self.split_effective_start_date[0]
        self.month = self.split_effective_start_date[1]
        self.date = self.split_effective_start_date[2]
        self.int_year = int(self.year)
        self.int_month = int(self.month)
        self.int_date = int(self.date)
        allure.attach("User can next version eff start year as : "+self.year,attachment_type=allure.attachment_type.TEXT)
        allure.attach("User can next version eff start month as : "+self.month,attachment_type=allure.attachment_type.TEXT)
        allure.attach("User can next version eff start date as : : "+self.date,attachment_type=allure.attachment_type.TEXT)
        if '01' in self.date:
            if '01' in self.month:
                self.int_new_year = self.int_year -1
                self.str_new_year = str(self.int_new_year)
                self.updated_eff_end_date = "{}-{}-{}".format(self.str_new_year,"12","31")
                self.updated_effective_end_date_for_previous_version = self.updated_eff_end_date
                allure.attach("User can see previous version effective end date calculated as : "+self.updated_effective_end_date_for_previous_version,attachment_type=allure.attachment_type.TEXT)
                return self.updated_effective_end_date_for_previous_version
            elif '03' in self.month:
                self.str_leap_year_or_not = self.calculate_leap_year(self.int_year)
                self.int_new_month = self.int_month -1
                if 'Not' in self.str_leap_year_or_not:
                    self.updated_eff_end_date = "{}-{}-{}".format(self.year,"0"+self.str_new_month,"28")
                else:
                    self.updated_eff_end_date = "{}-{}-{}".format(self.year,"0"+self.str_new_month,"29")
                self.updated_effective_end_date_for_previous_version = self.updated_eff_end_date
                allure.attach("User can see previous version effective end date calculated as : "+self.updated_effective_end_date_for_previous_version,attachment_type=allure.attachment_type.TEXT)
                return self.updated_effective_end_date_for_previous_version
            elif '02' or '04' or '06' or '08'  or '09' or '11' or '12' in self.month:
                self.int_new_month = self.int_month -1
                self.str_new_month = str(self.int_new_month)
                if '12' in self.month:
                    self.updated_eff_end_date = "{}-{}-{}".format(self.year,self.str_new_month,"30")
                elif '02' or '04' or '06' or '08'  or '09' or '11' in self.month:
                    if '11' in self.month:
                        self.updated_eff_end_date = "{}-{}-{}".format(self.year,self.str_new_month,"31")
                    else:
                        self.updated_eff_end_date = "{}-{}-{}".format(self.year,"0"+self.str_new_month,"31")
                self.updated_effective_end_date_for_previous_version = self.updated_eff_end_date
                allure.attach("User can see previous version effective end date calculated as : "+self.updated_effective_end_date_for_previous_version,attachment_type=allure.attachment_type.TEXT)
                return self.updated_effective_end_date_for_previous_version
            elif '05' or '07' or '10' in self.month:
                self.int_new_month = self.int_month -1
                self.str_new_month = str(self.int_new_month)
                self.updated_eff_end_date = "{}-{}-{}".format(self.year,self.str_new_month,"30")
            self.updated_effective_end_date_for_previous_version = self.updated_eff_end_date
            allure.attach("User can see previous version effective end date calculated as : "+self.updated_effective_end_date_for_previous_version,attachment_type=allure.attachment_type.TEXT)
            return self.updated_effective_end_date_for_previous_version
        elif self.int_date >= 2 and self.int_date <=10 :
            self.int_new_date = self.int_date -1
            self.str_new_date = str(self.int_new_date)
            self.updated_eff_end_date = "{}-{}-{}".format(self.year,self.month,"0"+self.str_new_date)
            self.updated_effective_end_date_for_previous_version = self.updated_eff_end_date
            allure.attach("User can see previous version effective end date calculated as : "+self.updated_effective_end_date_for_previous_version,attachment_type=allure.attachment_type.TEXT)
            return self.updated_effective_end_date_for_previous_version
        elif self.int_date >=11:
            self.int_new_date = self.int_date -1
            self.str_new_date = str(self.int_new_date)
            self.updated_eff_end_date = "{}-{}-{}".format(self.year,self.month,self.str_new_date)
            self.updated_effective_end_date_for_previous_version = self.updated_eff_end_date
            allure.attach("User can see previous version effective end date calculated as : "+self.updated_effective_end_date_for_previous_version,attachment_type=allure.attachment_type.TEXT)
            return self.updated_effective_end_date_for_previous_version
        else:
            allure.attach("Wrong date calculated : ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method calculate leap year
       Arguments : year(year='2023')
       Returns : str_leap_year or str_not_leap_year (str_not_leap_year='2020'+"Not leap Year")"""
    def calculate_leap_year(self,year):
        self.int_year = year
        if (self.int_year  % 400 == 0) or  (self.int_year % 100 != 0) and  (self.int_year % 4 == 0):
            self.str_leap_year = str(self.int_year)+ "Leap Year"
            return self.str_leap_year
        else:
            self.str_not_leap_year = str(self.int_year)+ "Not Leap Year"
            return self.str_not_leap_year
        
    """Author : Sadiya Kotwal
       Description : This method verify previous eff end date is updated to 1 minus eff start date of next version
       Arguments : calculated_eff_end_date(calculated_eff_end_date='2023-05-30')
                    version_no(version_no=1)
       Returns :"""
    def verify_previous_version_effective_end_date_isupdated_to_oneday_minusof_nextversion_eff_startdate(self,calculated_eff_end_date,version_no):
        self.calculated_eff_end_date = calculated_eff_end_date
        self.version_no = version_no
        self.pervious_version_eff_end_date = self.get_effective_end_date_of_any_version(self.version_no)
        allure.attach("User can see previous version effective end date updated as : "+self.pervious_version_eff_end_date,attachment_type=allure.attachment_type.TEXT)
        if self.pervious_version_eff_end_date == self.calculated_eff_end_date:
            allure.attach("User can see previous version effective end date  and calculated date is same: "+self.calculated_eff_end_date,attachment_type=allure.attachment_type.TEXT)
        else:
            assert False, "User cannot see previous version effective end date updated"

    def get_latest_version_count(self):
        self.get_text_version_count = forms.get_text_on_element(self, "XPATH", )
        allure.attach("User can get latest version count : "+self.get_text_effective_end_date,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Versions')
        return self.get_text_version_count
    
    def click_on_revision_history_tab(self):
        mouse.click_js_on_element(self, By.XPATH, self.tab_revision_history)
        self.main.screen_load_time('Price Type Editor->Revision Tab')
        allure.attach("User can click on revision tab : ",attachment_type=allure.attachment_type.TEXT)

    def get_latest_version_count(self):
        self.get_text_version_count = forms.get_text_on_element(self, "XPATH", )
        allure.attach("User can get latest version count : "+self.get_text_effective_end_date,attachment_type=allure.attachment_type.TEXT)
        generics.capture_screenshot_allure(self.main, 'Versions')
        return self.get_text_version_count
    
    def click_on_revision_history_tab(self):
        mouse.click_js_on_element(self, By.XPATH, self.tab_revision_history)
        self.main.screen_load_time('Price Type Editor->Revision Tab')
        allure.attach("User can click on revision tab : ",attachment_type=allure.attachment_type.TEXT)

    def confirm_history_for_version_1(self,Modified_by_xl):
        self.modified_by_xl = Modified_by_xl
        self.modified_on_xl = MainPage.get_system_current_date(self,"%Y-%m-%d")
        self.modified_by = forms.get_text_on_element(self,"XPATH",self.Modified_by_xpath_for_previous_version_1)
        self.modified_on = forms.get_text_on_element(self,"XPATH",self.Modified_on_xpath_for_previous_version_1)
        allure.attach("Price Type Modified By On UI for version 1: "+self.modified_by,attachment_type=allure.attachment_type.TEXT)
        allure.attach("Price Type Modified On for UI for version 1: "+self.modified_on,attachment_type=allure.attachment_type.TEXT)
        assert str(self.modified_by) == str(self.modified_by_xl) , "Modified_by does not match"
        assert str(self.modified_on) == str(self.modified_on_xl) , "modified_on does not match"
    
    def click_on_effective_end_date_input_cross_mark(self):
        mouse.click_on_element(self,"XPATH", self.icon_effective_end_date)
        allure.attach("User can click on effective end date calendar cross mark to keep effective end date blank: ",attachment_type=allure.attachment_type.TEXT)

    """Author : Sadiya Kotwal
       Description : This method sconverts date format          
       Arguments : date_str(Eg:date_str="06/14/2023"  MM/DD/YYYY)
       Returns : NA"""
    def convert_date_fromat(self,date_format):
        allure.attach("User entered date as : " + date_format, attachment_type=allure.attachment_type.TEXT)
        split_date = date_format.split('/')
        month = split_date[0]
        date = split_date[1]
        year = split_date[2]
        self.new_year = year+"-"+month+"-"+date
        allure.attach("User get converted date as : " + self.new_year, attachment_type=allure.attachment_type.TEXT)
        return self.new_year