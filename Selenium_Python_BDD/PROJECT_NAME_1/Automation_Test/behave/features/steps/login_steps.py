from behave import *
from GP.tests.test_login import TestLogin
import GP.utilities.excelUtility as ExclUtlty

@given(u'As a user login into the application')
def step_impl(context):
    context.login = TestLogin()
    context.environment = context.td_set['Environment']
    context.login.setUp()
    context.login.open_sparc(context.environment)
    context.driver = context.login.driver
  
@when(u'I login into the application')
def step_impl(context):
    context.username = context.td_set['UserID']
    context.password = context.td_set['Password']
    context.login.test_login(context.username, context.password)

@when(u'I select a config to the environment')
def step_impl(context):
    context.client = context.td_set['Client']
    context.service = context.td_set['Service']
    context.login.test_config_environment(context.client, context.service)

@when(u'I login into the application as a Manager')
def step_impl(context):
    context.username = context.td_set['UserID_2']
    context.password = context.td_set['Password_2']
    context.login.test_login(context.username, context.password)

@then(u'I enter the application')
def step_impl(context):
    pass

@given(u'Initialize testdata for "{sheet}" "{scenario_id}" and "{tc_id}"')
def step_impl(self,sheet,scenario_id,tc_id):
    self.scenario_id = scenario_id
    self.td_set = ExclUtlty.dataReader_Initialize(sheet, scenario_id, tc_id)

    for i in self.td_set.keys():
        value = self.td_set[i]
        print(i, ":", value)

    self.TCID=tc_id