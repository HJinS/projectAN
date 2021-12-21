from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.expected_conditions import presence_of_all_elements_located, presence_of_element_located
from crawler import Crawler

"""
상품 id 가져올 것
상품 이미지 url 가져올 것
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
            uiFlag = False
            try:
                total_pagination_num = int(list(self.driver.find_element(By.CLASS_NAME,'a-pagination').text.split('\n'))[-2])
            except:
                total_pagination_num = int(self.driver.find_elements(By.CLASS_NAME, 's-pagination-item')[-2].text)
                uiFlag = True

            for page in range(total_pagination_num):
                if uiFlag:
                    next_btn = self.driver.find_elements(By.CLASS_NAME, 's-pagination-item')[-1]
                else:
                    next_btn = self.driver.find_element(By.CLASS_NAME,'a-pagination').find_element(By.CLASS_NAME, 'a-last')
                    
                print(next_btn.text, uiFlag)
                data = self.driver.find_element(By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]')
                
                data_list = data.find_elements(By.XPATH, '//div[@data-component-type="s-search-result"]')
                
                for item in data_list:
                    data_asin = item.get_attribute('data-asin')
                    class_name = item.get_attribute('class')
                    
                    if "AdHolder" in class_name:
                        continue
                    if uiFlag:
                        img = item.find_element(By.XPATH, './descendant::div/descendant::span[@data-component-type="s-product-image"]/a/div/img').get_attribute('src')
                        product_name = item.find_element(By.XPATH, './descendant::div/descendant::span/div/div/div[2]/div[2]/div/div/div[1]/h2/a/span').text
                        try:
                            price = item.find_element(By.XPATH, './descendant::div/descendant::span/div/div/div[2]/div[2]/div/div/div[3]/div[1]/div/div/div/a/span/span[2]')
                        except:
                            continue
                    else:    
                        img = item.find_element(By.XPATH, './descendant::div/descendant::span[@data-component-type="s-product-image"]/a/div/img').get_attribute('src')
                        product_name = item.find_element(By.XPATH, './descendant::div/descendant::div/div/div/div[2]/div/div/div[1]/h2/a/span').text
                        try:
                            price = item.find_element(By.XPATH, './descendant::div/descendant::div/div/div/div[2]/div/div/div[3]/div[1]/div/div[1]/div/a/span/span[2]')
                        except:
                            continue
                    
                    print("-----------------------")
                    print(item.text)
                    print(img)
                    print(product_name)
                    print("price = ", str(price.text))
                    print("-----------------------")
                    
                
                print("next_page")        
                next_btn.click()
                self.driverWait.until(presence_of_all_elements_located((By.XPATH, '//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]')))

crawler = AmazonCrawler("E:\Study\chromedriver.exe", ["RTX3080"])
crawler.save()