# Author: Dairo Cortes
# Date: Jun 9 2021
# Don't forget add the environment variables:
#	LOAD_BALANCER_NAME
#	BROWSER_NAME=[chrome, safari, edge, opera, firefox, opera_local] 
# Example:
#	export LOAD_BALANCER_NAME=http://localhost:4545
#	export BROWSER_NAME=chrome
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common import desired_capabilities
from selenium.webdriver.opera import options
import os

CHROME = "CHROME"
FIREFOX= "FIREFOX"
EDGE   = "EDGE"
OPERA  = "OPERA"
SAFARI = "SAFARI"
OPERA_LOCAL="OPERA_LOCAL"

def chromeEnvironment():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    urlSelenium =  os.environ.get('LOAD_BALANCER_NAME')+"/wd/hub"
    #urlSelenium = "https://uat-selenium-grid.integrichain.net/grid/console"
    #urlSelenium = "https://test-selenium-grid.integrichain.net/grid/console"
    return webdriver.Remote(desired_capabilities=DesiredCapabilities.CHROME,command_executor=urlSelenium,options=options)

def firefoxEnvironment():
    urlSelenium =  os.environ.get('LOAD_BALANCER_NAME')+"/wd/hub"
    return webdriver.Remote(desired_capabilities=DesiredCapabilities.FIREFOX,command_executor=urlSelenium)

def edgeEnvironment():
    urlSelenium =  os.environ.get('LOAD_BALANCER_NAME')+"/wd/hub"
    return webdriver.Remote(desired_capabilities=DesiredCapabilities.EDGE,command_executor=urlSelenium)

def operaEnvironment():
    _operaDriverLoc = os.path.abspath('/etc/operadriver')  # Replace this path with the actual path on your machine.
    _operaExeLoc = os.path.abspath('/Applications/Opera.app/Contents/MacOS/Opera')   # Replace this path with the actual path on your machine.
    _operaCaps = desired_capabilities.DesiredCapabilities.OPERA.copy()
    _operaOpts = options.ChromeOptions()  
    _operaOpts._binary_location = _operaExeLoc
    _operaOpts.add_argument('--start-maximized')  
    return  webdriver.Chrome(executable_path = _operaDriverLoc, chrome_options = _operaOpts, desired_capabilities = _operaCaps)

def operaRemotoEnvironment():
    #operablink
    desired_caps = {}
    desired_caps['platform'] = 'linux'
    desired_caps['browserName'] = 'operablink'
    urlSelenium =  os.environ.get('LOAD_BALANCER_NAME')+"/wd/hub"
    return webdriver.Remote(desired_capabilities=desired_caps,command_executor=urlSelenium)


def createEnvironment():
    if (os.environ.get("BROWSER_NAME")==None) or (os.environ.get("LOAD_BALANCER_NAME")==None):
        print("Error, can't found the environment variables:[BROWSER_NAME or LOAD_BALANCER_NAME]")
        return None
    browser = os.environ.get("BROWSER_NAME").upper()
    print (browser)
    if browser==SAFARI:
        return webdriver.Safari()
    elif browser==OPERA:
        return operaRemotoEnvironment()
    elif browser==OPERA_LOCAL:
        return operaEnvironment()
    elif browser==CHROME:
        return chromeEnvironment()
    elif browser==FIREFOX:
        return firefoxEnvironment()
    elif browser==EDGE:
        return edgeEnvironment()
    else:
        return chromeEnvironment()
