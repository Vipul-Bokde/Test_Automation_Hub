from pydoc import locate
import time
from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.uploads_screen_page import UploadPage
from GP.utilities.logs_util import logger
import GP.utilities.Repo as Repo
from GP.pages.login_page import Login
from GP.pages.rebate_transfer_page import RebateTransferPage
 

class Upload(EnvironmentSetup):
    @when(u'I select Upload File from burger menu')
    def step_impl(self):  
        self.Upload = UploadPage(self.driver)
        self.login = Login(self.driver)
        self.Upload.select_upload_from_burguer_menu()
    
    @when(u'I upload file')
    def step_impl(self):
        self.Upload.click_on_upload_button()
        self.Upload.select_file_type()
        self.Upload.click_on_checkbox()
        self.Upload.select_file_template_source()
        self.Upload.select_file_template()
        self.file_name = self.td_set['File_to_Upload']
        self.file_to_upload = Repo.uploadfiles_path_1+r'\{}'.format(str(self.file_name))
        self.Upload.upload_file(self.file_to_upload)
        self.Upload.click_on_submit_button()
        time.sleep(5)
        self.driver.refresh()
    
    @then(u'I Verify File status')
    def step_impl(self):
        self.status = self.td_set['Status']
        self.UserID = self.td_set['UserID_2']
        if self.status=='FAIL':
            self.Upload.verify_failed_file_status(self.UserID)

        elif self.status=='PASS':
            self.Upload.verify_passed_file_status(self.UserID)
            self.rebatetransfer = RebateTransferPage(self.driver)
            self.download_file_loc = self.rebatetransfer.copy_remote_file()
            self.login.close_browser()        
