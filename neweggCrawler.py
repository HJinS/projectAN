from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
from crawler import Crawler

"""
정규식 등등 사용해서 결과 거를 수 있는 방법 적용
--> DRF setting
"""
class NeweggCrawler(Crawler):
    def __init__(self, driver_path: str, keywords: list):
        super().__init__("https://www.newegg.com/", driver_path)
        self.keywords = keywords

    def __get_data(self, keyword):
        self.driver.get(self.site_loc)
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//input[@type="search"]').send_keys(keyword + Keys.RETURN)
        self.driver.implicitly_wait(5)
        total_pagination_num = int(list(self.driver.find_element(By.XPATH,'./descendant::div[@class="list-tool-pagination"]/span/strong').text.split('/'))[-1])
        
        for page in range(total_pagination_num):    
            self.__get_page_data()
            try:
                self.driverWait.until(presence_of_all_elements_located((By.XPATH, './descendant::div[@class="list-tools-bar"]/descendant::button[@type="button"]')))
                next_btn = self.driver.find_element(By.XPATH, './descendant::div[@class="list-tools-bar"]/descendant::button[@type="button"]')
                next_btn.click()
            except:
                return
        
    def __get_item_data(self, item):
        product_id = item.get_attribute('id')
        try:
            img = item.find_element(By.XPATH, './descendant::div[@class="item-container"]/a/img').get_attribute('src')
            product_name = item.find_element(By.XPATH, './descendant::div[@class="item-container"]/descendant::div[@class="item-info"]/a').text
            price = item.find_element(By.XPATH, './descendant::div[@class="item-container"]/descendant::div[@class="item-action"]/descendant::ul[@class="price"]/li[@class="price-current "]')
            
            print(price.text)
            price_str = list(price.text.split(' '))[0]
            print("-----------------------")
            print("id = ", product_id)
            print(item.text)
            print(img)
            print(product_name)
            print("price = ", price_str)
            print("-----------------------")
        except:
            return
            
        
    def __get_page_data(self):
        data_list = self.driver.find_elements(By.XPATH, './descendant::div[@class="list-wrap"]/descendant::div[@class="item-cell"]')
        for item in data_list:
            self.__get_item_data(item)

    def save(self):
        for keyword in self.keywords:
            self.__get_data(keyword=keyword)
            

crawler = NeweggCrawler("E:\Study\chromedriver.exe", ["12900k"])
crawler.save()