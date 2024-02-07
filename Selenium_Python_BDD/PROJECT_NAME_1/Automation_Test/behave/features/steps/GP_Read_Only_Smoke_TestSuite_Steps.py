from datetime import date
from behave import *
from libraries.environment_setup import EnvironmentSetup
import allure
from allure_commons.types import AttachmentType
from GP.utilities.logs_util import logger
from GP.pages.data_overview_page import DataOverviewPage
from GP.pages.gp_run_creation_page import RunCreationPage
from GP.pages.analysis_page import AnalysisPage
import GP.utilities.excelUtility as ExclUtlty
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from GP.tests.test_login import TestLogin
from GP.pages.data_dictionary_page import DataDictionaryPage
from GP.pages.view_data_page import ViewDataPage
from GP.pages.rebate_transfer_page import RebateTransferPage
from GP.pages.price_type_editor_page import PriceTypePage
from GP.pages.approvals_page import ApprovalsPage
from GP.pages.client_joins_page import NewJoinPage
from GP.pages.product_page import ProductPage
from GP.pages.global_new_mapping_page import NewMappingPage
from GP.pages.client_pricing_page import ClientPricingPage
from GP.pages.screen_load_time_page import Load_Time_Page
from GP.pages.GP_Read_Only_Smoke_TestSuite_page import ReadOnlySmokeTestSuitePage


class Read_Only_Smoke_Test_Suite(EnvironmentSetup):

    @When(u'user is on landing screen data overview')
    def step_impl(self):
        self.overview = DataOverviewPage(self.driver)
        self.run_creation = RunCreationPage(self.driver)
        self.login = Login(self.driver)
        self.DataDictionary = DataDictionaryPage(self.driver)
        self.ViewData = ViewDataPage(self.driver)
        self.rebatetransfer = RebateTransferPage(self.driver)
        self.PriceType = PriceTypePage(self.driver)
        self.Approvals = ApprovalsPage(self.driver)
        self.NewJoin = NewJoinPage(self.driver)
        self.Product = ProductPage(self.driver)
        self.New_Mapping = NewMappingPage(self.driver)
        self.ClientPricing = ClientPricingPage(self.driver)
        self.load_time = Load_Time_Page(self.driver)
        self.ReadOnlySmokeTestSuite = ReadOnlySmokeTestSuitePage(self.driver)
        self.screen_name_data_overview = self.td_set['Screen_Name_Data_Overview']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_data_overview)
    
    @Then(u'I verify client name and overview screen all available buttons')
    def step_impl(self):
        self.client_name = self.td_set['Client']
        self.overview.verify_client_name(self.client_name)
        for row in self.table:
            self.overview.verify_buttons_on_screen(row["Button_Name"])

    @When(u'I navigate to the run screen')
    def step_impl(self):
        self.run_creation.select_run_option()
        self.screen_name_runs = self.td_set['Screen_Name_Runs']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_runs)

    @Then(u'I verify run screen all available buttons')
    def step_impl(self):
        for runscreen in self.table:
            self.overview.verify_buttons_on_screen(runscreen["Run_Screen_Buttons"])

    @When(u'I navigate to data dictionary screen')
    def step_impl(self):
        self.DataDictionary.select_global_from_burger_menu()
        self.screen_name_data_dictionary = self.td_set['Screen_Name_Data_Dictionary']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_data_dictionary)

    @Then(u'I verify data dictionary screen all available buttons')
    def step_impl(self):
         for datadictionary in self.table:
            self.overview.verify_buttons_on_screen(datadictionary["Data_Dictionary_Buttons"])
    
    @When(u'user navigate to view data screen')
    def step_impl(self):
        self.ViewData.select_product_from_burger_menu()
        self.screen_name_view_data = self.td_set['Screen_Name_View_Data']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_view_data)

    @Then(u'I verify view data screen all available buttons')
    def step_impl(self):
         self.ViewData.verify_calender_icon()
         self.ViewData.verify_export_button()
         self.txt_page_size = self.td_set['Pages']
         self.rebatetransfer.select_page_size_from_dropdown(self.txt_page_size)
         self.combobox_menu= self.td_set['Combobox_Menu_Product']
         self.rebatetransfer.select_any_menu_from_combobox_menu(self.combobox_menu)
         self.screen_name_view_data = self.td_set['Screen_Name_View_Data']
         self.rebatetransfer.wait_for_screen_to_load(self.screen_name_view_data)

    @When(u'I navigate to Price type editor screen')
    def step_impl(self):
        self.PriceType.select_price_type_editor_from_burger_menu()
        self.screen_name_price_type_editor = self.td_set['Screen_Name_Price_Type_Editor']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_price_type_editor)

    @Then(u'I verify Price type editor screen all available buttons')
    def step_impl(self):
          for pricetypeeditor in self.table:
            self.overview.verify_buttons_on_screen(pricetypeeditor["Price_Type_Editor"])

    @When(u'user navigate to Rebate transfer screen')
    def step_impl(self):
        self.hamburger_menu_rebate_transfer = self.td_set['Hamburger_Menu_Rebate_Transfer']
        self.rebatetransfer.select_any_menu_from_burger_menu(self.hamburger_menu_rebate_transfer)
        self.screen_name_rebate_transfer = self.td_set['Screen_Name_Rebate_Transfer']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_rebate_transfer)

    @Then(u'user verify Rebate transfer screen all available buttons')
    def step_impl(self):
        self.ViewData.verify_export_button()
        self.rebatetransfer.verify_rebate_transfer_button()

    @When(u'I navigate to Approvals screen')
    def step_impl(self):
        self.Approvals.select_approval_from_burger_menu()
        self.screen_name_approvals = self.td_set['Screen_Name_Approvals']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_approvals)

    @Then(u'I verify Approvals screen all available buttons and available dropdown')
    def step_impl(self):
        for approvals in self.table:
            self.overview.verify_buttons_on_screen(approvals["Approvals"])
        self.Approvals.verify_client_dropdown_from_approvals()
        self.Approvals.verify_type_dropdown_from_approvals()

    @When(u'I navigate to Uploads screen')
    def step_impl(self):
        self.Product.select_upload_from_burguer_menu()
        self.screen_name_uploads = self.td_set['Screen_Name_Uploads']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_uploads)

    @Then(u'I verify Uploads screen all available buttons')
    def step_impl(self):
        for uploads in self.table:
            self.overview.verify_buttons_on_screen(uploads["Uploads"])
        self.ClientPricing.verify_export_button()

    @When(u'I navigate to client join screen')
    def step_impl(self):
        self.NewJoin.select_global_from_burger_menu()
        self.screen_name_client_joins = self.td_set['Screen_Name_Client_Joins']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_client_joins)

    @Then(u'I verify client joins screen all available buttons')
    def step_impl(self):
        for clientJoins in self.table:
             self.overview.verify_buttons_on_screen(clientJoins["Client ->Joins"])
        self.ViewData.verify_calender_icon()

    @When(u'I navigate to client pricing screen')
    def step_impl(self):
        self.ClientPricing.select_pricing_sub_menu_from_burguer_menu()
        self.screen_name_client_pricing = self.td_set['Screen_Name_Client_Pricing']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_client_pricing)

    @Then(u'I verify client pricing screen all available buttons')
    def step_impl(self):
        for clientPricing in self.table:
             self.overview.verify_buttons_on_screen(clientPricing["Client ->Pricing"])
        self.ClientPricing.verify_export_button()
        self.ClientPricing.verify_upload_button()
       
    @When(u'I navigate to client product screen')
    def step_impl(self):
        self.Product.select_products_submenu_from_burguer_menu()
        self.screen_name_client_product = self.td_set['Screen_Name_Client_Product']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_client_product)

    @Then(u'I verify client product screen all available buttons')
    def step_impl(self):
        for clientProduct in self.table:
             self.overview.verify_buttons_on_screen(clientProduct["Client ->Product"])
        self.Product.verify_export_button()
        self.Product.verify_upload_button()
            
    @When(u'I navigate to Global price type screen')
    def step_impl(self):
        self.New_Mapping.select_pricetypes_submenu_from_burguer_menu()
        self.screen_name_global_pricetypes = self.td_set['Screen_Name_Global_PriceTypes']
        self.ReadOnlySmokeTestSuite.verify_selected_screen(self.screen_name_global_pricetypes)

    @Then(u'I verify Global price type screen all available buttons')
    def step_impl(self):
        for globalPriceType in self.table:
             self.overview.verify_buttons_on_screen(globalPriceType["Global ->PriceTypes"])
        self.ViewData.verify_export_button()
        
    @When(u'I navigate to Global file template screen')
    def step_impl(self):
        self.New_Mapping.select_filetemplates_submenu_from_burguer_menu()
        self.screen_name_fileTemplate = self.td_set['Screen_Name_Global_FileTemplate']
        self.ReadOnlySmokeTestSuite.verify_screen_name(self.screen_name_fileTemplate)

    @Then(u'I verify file template screen all available buttons')
    def step_impl(self):
        for fileTemplate in self.table:
             self.overview.verify_buttons_on_screen(fileTemplate["Global ->File Template -> Templates"])
        
    @When(u'I navigate to Global file template GP mapping screen')
    def step_impl(self):
        self.New_Mapping.click_on_gp_mappings()
        self.screen_name_fileTemplate_gpmappings = self.td_set['Screen_Name_Global_GPMapping']
        self.ReadOnlySmokeTestSuite.verify_screen_name(self.screen_name_fileTemplate_gpmappings)

    @Then(u'I verify Global file template GP mapping screen all available buttons')
    def step_impl(self):
        for fileTemplateGPMapping in self.table:
             self.overview.verify_buttons_on_screen(fileTemplateGPMapping["Global ->File Template -> GPMappings"])
        
