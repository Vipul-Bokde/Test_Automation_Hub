from libraries.environment_setup import EnvironmentSetup
from GP.pages.login_page import Login
from GP.pages.sparc_serivce_page import SparcServices
from libraries import gp_mapping
from GP.pages.main_page import MainPage

class TestLogin(EnvironmentSetup):

    def open_sparc(self, env):
        url = gp_mapping.map_environment(env)
        self.driver.get(url)

    def test_login(self, user, password):
        login = Login(self.driver)
        login.enter_username(user)
        login.enter_password(password)
        login.click_login_button()

    def test_config_environment(self, client, service):
        environment = SparcServices(self.driver)
        environment.select_client(client)
        environment.select_service(service)
        environment.click_on_submit_button()
        self.main = MainPage(self.driver)
        # self.main.screen_load_time('Login->Data Overview')


    def close_browser(self):
        self.tearDown()
