from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

class Crawler:
    def __init__(self, site_location: str, driver_path: str):
        self.site_loc = site_location
        self.driver_path = driver_path
        self.__init_crawler()
        
    def __init_crawler(self):
        service = Service(self.driver_path)
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        self.driver = webdriver.Chrome(service=service, options=options)
        self.driverWait = WebDriverWait(self.driver, 5)
        
    def __del__(self):
        self.driver.quit()