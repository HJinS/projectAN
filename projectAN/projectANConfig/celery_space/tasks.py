from __future__ import absolute_import

from .Celery import app
from priceInfo.models import PriceInfo
from .neweggCrawler import NeweggCrawler
from .amazonCrawler import AmazonCrawler
from .resultFilter import ResultFilter
from AN.models import Product
import os

try:
    from .loadEnvKey import get_env_key
except:
    pass

@app.task(bind=True)
def CrawlAndSaveAmazon():
    keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
    try:
        driver_path = get_env_key("driver_path")
    except:
        driver_path = os.environ.get("driver_path")
    crawler = AmazonCrawler(driver_path, keywords)
    test_q = crawler.save()
    filter = ResultFilter(test_q)
    res = filter.filtering()
    
    for item in res:
        __save_to_db(item, 0)
    
@app.task(bind=True)
def CrawlAndSaveNewegg():
    keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
    try:
        driver_path = get_env_key("driver_path")
    except:
        driver_path = os.environ.get("driver_path")
    crawler = NeweggCrawler(driver_path, keywords)
    test_q = crawler.save()
    filter = ResultFilter(test_q)
    res = filter.filtering()
    
    for item in res:
        __save_to_db(item, 1)
        
        
def __save_to_db(item: list, crawl_site: int):
    id, image, name, price, keyword = item
    product = Product()
    product.product_id = id
    product.img_src = image
    product.name = name
    product.category = keyword
    product.site = crawl_site
    
    priceInfo = PriceInfo()
    priceInfo.price = price
    priceInfo.product_id = product
    
    product.save()
    priceInfo.save()