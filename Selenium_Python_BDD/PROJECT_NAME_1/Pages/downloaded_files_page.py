from GP.utilities.logs_util import logger
import os,base64
import GP.utilities.Repo as Repo
import logging
from libraries.environment_setup import EnvironmentSetup
from GP.pages.main_page import MainPage


class DownloadedFilesPage(EnvironmentSetup):

    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self.main = MainPage(self.driver)


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