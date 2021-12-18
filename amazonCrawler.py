from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

"""
페이지네이션 제거하고 데이터 전부 가져올 것
클래스 만들 것
뉴에그 크롤러 만들 것
정규식 등등 사용해서 결과 거를 수 있는 방법 적용
--> DRF setting
"""

### Setting selenium
service = Service("D:\study\chromedriver")
options = webdriver.ChromeOptions()
options.add_argument('disable-gpu')
driver = webdriver.Chrome(service=service, options=options)

### Get page source
driver.get('https://www.amazon.com/')
driver.implicitly_wait(time_to_wait=2)

### Get search box and send search key
driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys('RTX3080')
driver.implicitly_wait(time_to_wait=2)

### Click search btn
driver.find_element(By.XPATH, '//*[@id="nav-search-submit-button"]').click()
driver.implicitly_wait(time_to_wait=2)

### Get item data
data = driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]')
driver.implicitly_wait(time_to_wait=2)
driver.quit()