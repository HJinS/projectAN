import json, os, uuid, pymysql
from datetime import datetime
from pathlib import Path
from loadEnvKey import get_env_key
from amazonCrawler import AmazonCrawler
from neweggCrawler import NeweggCrawler
from resultFilter import ResultFilter

BASE_DIR = Path(__file__).resolve().parent

def __get_secret(key):
    secret_path = os.path.join(BASE_DIR, 'projectAN\\secrets.json')
    with open(secret_path) as file:
        secrets = json.loads(file.read())
    try:
        return secrets[key]
    except KeyError:
        error_message = "Set the {} environment variable".format(key)
        raise ValueError(error_message)


user = 'anuser@localhost'
password = __get_secret('DB_PASSWORD')

db = pymysql.connect(
    user = user,
    passwd = password,
    host = '127.0.0.1',
    db = 'projectAN',
    charset='utf8'
)
cursor = db.cursor()

def CrawlAndSaveAmazon():
    keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
    driver_path = get_env_key("driver_path")
    for keyword in keywords:
        crawler = AmazonCrawler(driver_path, [keyword])    
        test_q = crawler.save()
        filter = ResultFilter(test_q)
        res = filter.filtering()
        for item in res:
            product_id, image, name, price, keyword = item
            id = str(uuid.uuid4().hex)
            today = datetime.today().strftime("%Y-%m-%d")
            sql = f'''INSERT INTO `an_product` (id, product_id, name, price, img_src, category, site, updated_dt) VALUES ("{id}", "{product_id}", "{name}", "{price}", "{image}", "{keyword}", "0", "{today}");'''
            cursor.execute(sql)
            db.commit()
             

def CrawlAndSaveNewegg():
    keywords = ["intel cpu", "amd cpu", "radeon gpu", "nvidia gpu", "ddr4 ram", "ddr5 ram", "nvme ssd", "sata ssd", "liquid cpu cooler", "air cpu cooler"]
    driver_path = get_env_key("driver_path")
    for keyword in keywords:
        crawler = NeweggCrawler(driver_path, [keyword])    
        test_q = crawler.save()
        filter = ResultFilter(test_q)
        res = filter.filtering()
        for item in res:
            product_id, image, name, price, keyword = item
            id = str(uuid.uuid4().hex)
            today = datetime.today().strftime("%Y-%m-%d")
            sql = f'''INSERT INTO `an_product` (id, product_id, name, price, img_src, category, site, updated_dt) VALUES ("{id}", "{product_id}", '{name}', "{price}", "{image}", "{keyword}", "0", "{today}");'''
            cursor.execute(sql)
            db.commit()
