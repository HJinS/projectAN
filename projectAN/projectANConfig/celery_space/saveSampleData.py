import json, os, uuid, pymysql
from datetime import datetime
from pathlib import Path
from amazonCrawler import AmazonCrawler
from neweggCrawler import NeweggCrawler
from resultFilter import ResultFilter

try:
    from .loadEnvKey import get_env_key
except:
    pass

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
            try:
                sql = f'''INSERT INTO `product` (id, name, img_src, category, site, updated_dt) VALUES ("{product_id}", "{name}", "{image}", "{keyword}", "0", "{today}");'''
                cursor.execute(sql)
                sql = f'''INSERT INTO `prices` (id, product_id_id, price, updated_dt) VALUES ("{id}", "{product_id}", "{price}", "{today}");'''
                cursor.execute(sql)
            except:
                try:
                    sql = f'''INSERT INTO `product` (id, name, img_src, category, site, updated_dt) VALUES ("{product_id}", '{name}', "{image}", "{keyword}", "0", "{today}");'''
                    cursor.execute(sql)
                    sql = f'''INSERT INTO `prices` (id, product_id_id, price, updated_dt) VALUES ("{id}", "{product_id}", "{price}", "{today}");'''
                    cursor.execute(sql)
                except Exception as e:
                    with open('crawlLog.txt', 'a') as f:
                        f.write(str(e)+'\n')
                    continue
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
            try:
                sql = f'''INSERT INTO `product` (id, name, img_src, category, site, updated_dt) VALUES ("{product_id}", '{name}', "{image}", "{keyword}", "1", "{today}");'''
                cursor.execute(sql)
                sql = f'''INSERT INTO `prices` (id, product_id_id, price, updated_dt) VALUES ("{id}", "{product_id}", "{price}", "{today}");'''
                cursor.execute(sql)
            except:
                try:
                    sql = f'''INSERT INTO `product` (id, name, img_src, category, site, updated_dt) VALUES ("{product_id}", "{name}", "{image}", "{keyword}", "1", "{today}");'''
                    cursor.execute(sql)
                    sql = f'''INSERT INTO `prices` (id, product_id_id, price, updated_dt) VALUES ("{id}", "{product_id}", "{price}", "{today}");'''
                    cursor.execute(sql)
                except Exception as e:
                    with open('crawlLog.txt', 'a') as f:
                        f.write(str(e)+'\n')
                    continue
            db.commit()

CrawlAndSaveNewegg()
db.close()