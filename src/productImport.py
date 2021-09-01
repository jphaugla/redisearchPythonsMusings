import csv
import sys
import datetime
import redis
from Product import Product

maxInt = sys.maxsize


REDIS_HOST = '34.138.134.33'


def main():
    # global redis_pool
    # print("PID %d: initializing redis pool..." % os.getpid())
    # redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    print("Starting productimport.py at " + str(datetime.datetime.now()))
    conn = redis.StrictRedis(host=REDIS_HOST, port=15999, db=0, charset="utf-8", decode_responses=True)
    pipe = conn.pipeline()
    #  open the file to read as csv
    with open('data/files.index.csv') as csv_file:
        # file is tab delimited
        csv_reader = csv.DictReader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
        prod_idx = 0
        # fields = next(csv_reader, None)
        #  go through all rows in the file
        for row in csv_reader:
            #  increment prod_idx
            prod_idx += 1
            # hash_key = "prod:" + str(prod_idx)
            nextProduct = Product(**row)

            category_id = 'categ:' + nextProduct.catid
            categ_name = conn.hget(category_id, "Name")
            nextProduct.set_category_name(categ_name)
            conn.hset(nextProduct.get_key(), mapping=nextProduct.__dict__)
            # print("prodid " + prodid )
            # 0)path 1)product_id 2)updated 3)quality 4)supplier_id 5)prod_id 6)catid 7)m_prod_id 8)ean_upc 9)on_market
            # 10)country_market 11)model_name 12)product_view 13)high_pic 14)high_pic_size
            # 15)high_pic_width 16)high_pic_height 17)m_supplier_id 18)m_supplier_name 19)ean_upc_is_approved
            # 20)Limited Date_Added
            conn.sadd("CategIDX:" + categ_name, nextProduct.get_key())
            model_key: str = "ProductModel:" + nextProduct.model_name
            # print("model key is " + model_key)
            conn.sadd(model_key, nextProduct.get_key())
            if prod_idx % 10000 == 0:
                print(str(prod_idx) + " rows loaded")
        csv_file.close()
        print(str(prod_idx) + " rows loaded")
        conn.set("prod_highest_idx", prod_idx)
    print("Finished productimport.py at " + str(datetime.datetime.now()))

if '__main__' == __name__:
    main()

