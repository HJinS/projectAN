from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
from crawler import Crawler
from collections import deque
from resultFilter import ResultFilter
from loadEnvKey import get_env_key

class NeweggCrawler(Crawler):
    def __init__(self, driver_path: str, keywords: list):
        super().__init__("https://www.newegg.com/", driver_path)
        self.keywords = keywords
        self.resultQueue = deque()

    def __get_data(self, keyword):
        self.driver.get(self.site_loc)
        self.driver.implicitly_wait(5)
        self.driver.find_element(By.XPATH, '//input[@type="search"]').send_keys(keyword + Keys.RETURN)
        self.driver.implicitly_wait(5)
        total_pagination_num = int(list(self.driver.find_element(By.XPATH,'./descendant::div[@class="list-tool-pagination"]/span/strong').text.split('/'))[-1])
        print("newegg total crawl page = {page} keyword = {keyword}".format(page=total_pagination_num, keyword=keyword))
        for page in range(min(4, total_pagination_num)):
            print("page{page:3} ".format(page=page), "--------------------", end='')
            self.__get_page_data(keyword)
            try:
                self.driverWait.until(presence_of_all_elements_located((By.XPATH, './descendant::div[@class="list-tools-bar"]/descendant::button[@type="button"]')))
                next_btn = self.driver.find_element(By.XPATH, './descendant::div[@class="list-tools-bar"]/descendant::button[@type="button"]')
                next_btn.click()
            except:
                return
            print("complete")
        
    def __get_item_data(self, item, keyword):
        product_id = item.get_attribute('id')
        try:
            img = item.find_element(By.XPATH, './descendant::div[@class="item-container"]/a/img').get_attribute('src')
            product_name = item.find_element(By.XPATH, './descendant::div[@class="item-container"]/descendant::div[@class="item-info"]/a').text
            price = item.find_element(By.XPATH, './descendant::div[@class="item-container"]/descendant::div[@class="item-action"]/descendant::ul[@class="price"]/li[@class="price-current "]')
            price_str = list(price.text.split(' '))[0]
            self.resultQueue.append([product_id, img, product_name, price_str, keyword])
        except:
            return
            
    def __get_page_data(self, keyword):
        data_list = self.driver.find_elements(By.XPATH, './descendant::div[@class="list-wrap"]/descendant::div[@class="item-cell"]')
        for item in data_list:
            self.__get_item_data(item, keyword)

    def save(self):
        for keyword in self.keywords:
            self.__get_data(keyword=keyword)
        return self.resultQueue
            
##keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
keywords = ["liquid cpu cooler", "air cpu cooler"]
driver_path = get_env_key("driver_path")
crawler = NeweggCrawler(driver_path, keywords)
test_q = crawler.save()
filter = ResultFilter(test_q)
filter.filtering()