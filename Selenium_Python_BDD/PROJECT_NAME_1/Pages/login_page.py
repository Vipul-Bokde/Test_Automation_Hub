from libraries import forms, mouse


class Login:

    #locators
    username_input = "username"
    password_input = "password"
    signin_button = "//button[@class='btn btn-lg btn-primary btn-block']"

    def __init__(self, driver):
        self.driver = driver

    def enter_username(self, username):
        forms.enter_text_on_element(self, "NAME", self.username_input, username)

    def enter_password(self, password):
        forms.enter_text_on_element(self, "NAME", self.password_input, password)

    def click_login_button(self):
        mouse.click_on_element(self, "XPATH", self.signin_button)
        
    def close_browser(self):
        self.driver.quit()
    
    