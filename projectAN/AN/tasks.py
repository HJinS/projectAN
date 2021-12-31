from __future__ import absolute_import
from neweggCrawler import NeweggCrawler

from projectANConfig.Celery import app
from ...neweggCrawler import NeweggCrawler
from ...amazonCrawler import AmazonCrawler
from ...resultFilter import ResultFilter
from ...loadEnvKey import get_env_key

@app.task(bind=True)
def CrawlAndSaveAmazon():
    ##keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
    keywords = ["liquid cpu cooler", "air cpu cooler"]
    driver_path = get_env_key("driver_path")
    crawler = AmazonCrawler(driver_path, keywords)
    test_q = crawler.save()
    filter = ResultFilter(test_q)
    res = filter.filtering()
    
@app.task(bind=True)
def CrawlAndSaveNewegg():
    ##keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
    keywords = ["liquid cpu cooler", "air cpu cooler"]
    driver_path = get_env_key("driver_path")
    crawler = NeweggCrawler(driver_path, keywords)
    test_q = crawler.save()
    filter = ResultFilter(test_q)
    res = filter.filtering()