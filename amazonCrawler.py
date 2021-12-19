from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
from crawler import Crawler

"""
상품 id 가져올 것
상품 이미지 url 가져올 것
클래스 만들 것
뉴에그 크롤러 만들 것
정규식 등등 사용해서 결과 거를 수 있는 방법 적용
--> DRF setting
"""
class AmazonCrawler(Crawler):
    def __init__(self, driver_path: str, keywords: list):
        super().__init__("https://www.amazon.com/", driver_path)
        self.keywords = keywords

    def save(self):
        for keyword in self.keywords:
            self.driver.get(self.site_loc)
            self.driver.implicitly_wait(5)
            self.driver.find_element(By.XPATH, '//*[@id="twotabsearchtextbox"]').send_keys(keyword + Keys.RETURN)
            self.driver.implicitly_wait(5)
            total_pagination_num = int(list(self.driver.find_element(By.CLASS_NAME, 'a-pagination').text.split('\n'))[-2])
            for page in range(total_pagination_num):
                next_btn = self.driver.find_element(By.CLASS_NAME, 'a-last')
                data = self.driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div').text
                next_btn.click()
                self.driverWait.until(presence_of_all_elements_located((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div')))

crawler = AmazonCrawler("E:\Study\chromedriver.exe", ["RTX3080"])
crawler.save()