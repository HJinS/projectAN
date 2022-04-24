from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class Crawler:
    def __init__(self, site_location: str, driver_path: str):
        self.site_loc = site_location
        self.driver_path = driver_path
        self.__init_crawler()
        
    def __init_crawler(self):
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('incognito')
        self.driver = webdriver.Remote(
            command_executor='http://chrome:4444/wd/hub',
            desired_capabilities=DesiredCapabilities.CHROME,
            options=options
        )
        self.driverWait = WebDriverWait(self.driver, 10)
        
    def __del__(self):
        self.driver.close()