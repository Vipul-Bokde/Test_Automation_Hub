from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.client_joins_page import NewJoinPage
from GP.pages.data_overview_page import DataOverviewPage
from GP.pages.rebate_transfer_page import RebateTransferPage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login
import GP.utilities.Repo as Repo
class NewJoin(EnvironmentSetup):


    @given('I select joins option under client from the burger menu')
    def step_impl(self):
        self.NewJoin = NewJoinPage(self.driver)
        self.login = Login(self.driver)
        logger.info("Create instance for new join class in client join steps")
        self.NewJoin.select_global_from_burger_menu()
        logger.info("Click on joins under the global menu")
    
    @then('I click on import join and upload join file')
    def step_impl(self):
        self.NewJoin.click_on_button("Import Joins")
        self.file_to_upload = self.td_set['File to upload']
        self.file_to_upload_path = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_to_upload))
        self.NewJoin.upload_file(self.file_to_upload_path)
        self.NewJoin.click_on_upload_button()
        self.overview = DataOverviewPage(self.driver)
        self.overview.check_uploaded_file(self.file_to_upload)
        
    @then('I click on Export join and get exported file')
    def step_impl(self):
        self.NewJoin.click_on_button("Export Joins")
        self.rebatetransfer = RebateTransferPage(self.driver)
        self.download_file_loc = self.rebatetransfer.copy_remote_file()
        self.rebatetransfer.navigate_back_to_screen()

    @then('I crosscheck exported file and grid data')
    def step_impl(self):
        logger.info(self.download_file_loc)
        self.NewJoin.validate_grid_and_exported_join_data(self.download_file_loc)
        
    @then('I click on inspect join')
    def step_impl(self):
        self.NewJoin.click_on_button("Inspect Joins")
    
    @then('I select source and check query')
    def step_impl(self):
        self.source = self.td_set['Source']
        self.NewJoin.select_source(self.source)
        self.NewJoin.check_query_visible()
        self.NewJoin.close_inspect_pop_up()

    @given('Click on add join')
    def step_impl(self):
        self.NewJoin.click_on_new_join()
        logger.info("Click on new join button")
    
    @when('Select details for new join')
    def step_impl(self):
        self.source = self.td_set['Source']
        self.Validation = self.td_set['Validation']
        self.Table = self.td_set['Table']
        self.Alias = self.td_set['Alias']
        self.Val_Start = self.td_set['Val_Start']
        self.Val_End = self.td_set['Val_End']
        self.Condition = self.td_set['Condition']
        self.NewJoin.create_new_join(self.source, self.Validation, self.Table, self.Alias, self.Val_Start,self.Val_End, self.Condition)

    @then('click on submit for adding new join')
    def step_impl(self):
        self.NewJoin.click_on_submit()

# Edit Join
    @given('I Select the created join')
    def step_impl(self):
        self.NewJoin.select_join_to_edit()

    @when('Edit the details of selected join')
    def step_impl(self):
        self.Source_Edited = self.td_set['Source']
        self.Alias_Edited = self.td_set['Alias']
        self.Condition_Edited = self.td_set['Condition']
        self.NewJoin.edit_selected_join(self.Source_Edited,self.Alias_Edited,self.Condition_Edited)
        
    @then('I check edited join values')
    def step_impl(self):
        self.NewJoin.check_edited_join()
    
    @then('perform click on submit button')
    def step_impl(self):
        self.NewJoin.click_on_submit()
    
    @then('I Select the join and click on action')
    def step_impl(self):
        self.join_list = self.NewJoin.select_join()
        self.NewJoin.check_checkbox()
        self.NewJoin.click_action_button()
        
    @then('I disable join and verify')
    def step_impl(self):
        self.NewJoin.select_from_actions_menu("Disable")
        self.join_list_2 = self.NewJoin.select_join()
        self.NewJoin.check_join_exist_after_action(self.join_list,self.join_list_2)
        self.NewJoin.verify_join_is_disabled("#dddddd")
    
    @then('I enable join and verify')
    def step_impl(self):
        self.NewJoin.select_from_actions_menu("Enable")
        self.join_list_2 = self.NewJoin.select_join()
        self.NewJoin.check_join_exist_after_action(self.join_list,self.join_list_2)
        self.NewJoin.verify_join_is_enabled("#fcfdfe")
    
    @then('I delete join and verify')
    def step_impl(self):    
        self.NewJoin.select_from_actions_menu("Delete")
        self.join_list_2 = self.NewJoin.select_join()
        self.NewJoin.check_join_exist_after_action(self.join_list,self.join_list_2)

        
