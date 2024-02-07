from behave import *
from libraries.environment_setup import EnvironmentSetup
from GP.pages.price_type_delete_page import DeletePriceTypePage
from GP.utilities.logs_util import logger
from GP.pages.login_page import Login

class DeletePriceType(EnvironmentSetup):
    
    @when(u'I select Price type and click on checkbox')
    def step_impl(context):
        context.deletepricetype =DeletePriceTypePage(context.driver)
        context.login = Login(context.driver)
        context.price_type = context.td_set['Price_Type']
        context.deletepricetype.delete_price_type(context.price_type)
        logger.info("I select Price type and click on checkbox")
        
    @then(u'I Delete Price Type')
    def step_impl(context):
        context.deletepricetype.click_on_delete_btn()
        logger.info("I Delete Price Type")
        context.login.close_browser()
        
    