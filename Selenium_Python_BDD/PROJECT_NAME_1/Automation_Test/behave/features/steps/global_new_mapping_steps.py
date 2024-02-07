from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.global_new_mapping_page import NewMappingPage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login
from GP.pages.approvals_page import ApprovalsPage

class Newmapping(EnvironmentSetup):


    @given(u'I select file templates option under global from the burger menu')
    def step_impl(self):
        self.New_Mapping = NewMappingPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for new mapping class in global new mapping step")
        self.New_Mapping.select_global_from_burger_menu()
        logger.info("Click on file templates under the global menu")
                    
    @given(u'I click on new template')
    def step_impl(self):
        self.New_Mapping.click_on_new_template()
        logger.info("Click on new template")
        
    @given(u'I enter new template details')
    def step_impl(self):
        self.Name = self.td_set['FileTemplate']
        self.Description = self.td_set['TempDesc']
        self.New_Mapping.enter_new_template_details(self.Name, self.Description)
        logger.info("Add new template details")
    
    @then(u'I click on template submit')
    def step_impl(self):
        self.template_name = self.td_set['FileTemplate']
        temp_status_var = self.New_Mapping.click_temp_submit_button(self.template_name)
        if temp_status_var == "File template already exists":
            logger.info("Template already exists pls try with different template name")
        else:
            logger.info("New Template Created")
            
    @then(u'I select file templates name to activate and send for approve')
    def step_impl(self):
        self.Template_Name = self.td_set['FileTemplate']
        self.Approval_Note = self.td_set['ApprovalNotes']
        self.New_Mapping.select_template_name(self.Template_Name, self.Approval_Note)
    
    @then(u'I select file templates to delete and send for approve')
    def step_impl(self):
        self.template_name = self.td_set['FileTemplate']
        self.delete_note = self.td_set['Delete_Note']
        logger.info(self.template_name)
        logger.info(self.delete_note)
        self.New_Mapping.select_template_name_to_delete(self.template_name,self.delete_note)

    @then(u'I crossverify the deleted template')
    def step_impl(self):
        self.template_name = self.td_set['FileTemplate']
        self.New_Mapping.crossverify_deleted_template(self.template_name)
        self.login.close_browser()

    @then(u'Select template and approve')
    def step_impl(self):
        logger.info("Select given value and approve")
        self.New_Mapping = NewMappingPage(self.driver)
        self.template_name = self.td_set['FileTemplate']
        self.New_Mapping.Approve_Template(self.template_name)
        self.Approvals = ApprovalsPage(self.driver)
        self.Approvals.click_on_approve_button()

    @then(u'Select delete template and approve')
    def step_impl(self):
        logger.info("Select delete template and approve")
        self.New_Mapping = NewMappingPage(self.driver)
        self.template_name = self.td_set['FileTemplate']
        self.New_Mapping.Approve_Template(self.template_name)
        self.Approvals = ApprovalsPage(self.driver)
        self.Approvals.click_on_approve_button()
          
    @when(u'I Click on GP mappings')
    def step_impl(self):
        self.New_Mapping.click_on_gp_mappings()
        logger.info("Click on GP Mappings option")
        
    @when('I create new mapping')
    def step_impl(self):
        self.New_Mapping.click_on_new_mapping()
        logger.info("Click on New Mappings button")
        
    @when(u'Select details for new mapping')
    def step_impl(self):
        self.Client = self.td_set['Client_Mapping']
        self.DataType = self.td_set['DataType']
        self.Source = self.td_set['Source']
        self.FileTemplate = self.td_set['MappingFileTemplate']
        self.FilterName = self.td_set['FilterName']
        self.New_Mapping.select_new_mapping_details(self.Client, self.DataType, self.Source, self.FileTemplate, self.FilterName)
        logger.info("Add new Mapping details")

    @then(u'I click on mapping submit button')
    def step_impl(self):
        status_var = self.New_Mapping.click_on_submit_button()
        if status_var == "Mapping Already exist":
            logger.info("Mapping already exists pls try with different mapping set")
        else:
            logger.info("New Mapping Created")
    
    @when('I select mapping and delete')
    def step_impl(self):
        self.Client = self.td_set['Client_Mapping']
        self.DataType = self.td_set['DataType']
        self.Source = self.td_set['Source']
        self.FileTemplate = self.td_set['MappingFileTemplate']
        self.FilterName = self.td_set['FilterName']
        self.value_list=[self.Client,self.DataType,self.Source,self.FileTemplate,self.FilterName]
        self.column_list = ['client_name','data_type','source','name','additional_filter']
        self.New_Mapping.filter_mapping(self.value_list,self.column_list)
        self.New_Mapping.select_mapping(self.value_list,self.column_list)
        self.New_Mapping.delete_mapping()
    
    @then('I verify deleted mapping')
    def step_impl(self):
        self.New_Mapping.filter_mapping(self.value_list,self.column_list)
        self.New_Mapping.verify_mapping(self.value_list,self.column_list)
            