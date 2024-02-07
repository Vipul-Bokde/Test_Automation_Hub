from behave import fixture
from selenium.webdriver.remote.command import Command
from libraries import selenium_env, cnp_logs

LOGGER = cnp_logs.get_logger("fixtures")


def isSessionAlive(driver):
    response = driver.execute(Command.STATUS)
    for node in response["value"]["nodes"]:
        slots = node["slots"]
        for slot in slots:
            if "session" in slot.keys():
                if slot["session"]["sessionId"] == driver.session_id:
                    return True
    return False


@fixture
def setUp(context):
    context.driver = selenium_env.createEnvironment()
    context.driver.maximize_window()
    context.driver.delete_all_cookies()
    yield context.driver
    if isSessionAlive(context.driver):
        context.driver.quit()
    else:
        LOGGER.info("There is no need to close a session that is already closed")
