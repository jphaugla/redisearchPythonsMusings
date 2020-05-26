import csv
import sys
import datetime

from redisearch import Client

client = Client('product', 'localhost', 6379)
catClient = Client('category', 'localhost', 6379)

maxInt = sys.maxsize

def ifnull(passedParm):
    if passedParm and not passedParm.isspace():
        returnValue=int(passedParm)
    else:
        returnValue=0
    return returnValue


def main():
    # global redis_pool
    # print("PID %d: initializing redis pool..." % os.getpid())
    # redis_pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    print("Starting productimport.py at " + str(datetime.datetime.now()))
    #  open the file to read as csv
    with open('../data/files.index.csv') as csv_file:
        # file is tab delimited
        csv_reader = csv.reader(csv_file, delimiter='\t', quoting=csv.QUOTE_NONE)
        prod_idx = 0
        fields = next(csv_reader, None)
        #  go through all rows in the file
        for row in csv_reader:
            #  increment prod_idx and use as incremental part of the key
            prod_idx += 1
            #hash_key = "prod:" + str(prod_idx)
            # print("hash_key is " + hash_key)
            # hash key
            # print("prodid " + prodid )
            # 0)path 1)product_id 2)updated 3)quality 4)supplier_id 5)prod_id 6)catid 7)m_prod_id 8)ean_upc 9)on_market
            # 10)country_market 11)model_name 12)product_view 13)high_pic 14)high_pic_size
            # 15)high_pic_width 16)high_pic_height 17)m_supplier_id 18)m_supplier_name 19)ean_upc_is_approved
            # 20)Limited Date_Added
            # index will be model name and hold value of prod_idx
            # index_value = str(row[11]) + ":" + str(prod_idx)
            # print("index value is " + index_value)
            # print("category name is " + str(categ_name))
            m_supplier_id=str(row[17])
            supplier_id=str(row[4])
            categ_id = str(row[6])
            product_id = str(row[1])
            m_product_id = str(row[7])
            m_product_string = "mprodid:" + m_product_id
            p_product_string = "prodid:" + product_id
            # supply
            if m_supplier_id and not m_supplier_id.isspace():
                supplier_string = ":msupplyid:" + m_supplier_id
            else:
                supplier_string = ":supplyid:" + supplier_id
            # product
            if m_product_id and not m_product_id.isspace():
                product_string = m_product_string + ":" + p_product_string
            else:
                product_string = "prodid:" + product_id
            keyName = product_string + supplier_string
            categoryDoc = catClient.load_document("category:" + categ_id)
            # print("keyName=" + keyName + " categ_id=" + categ_id + " product_id=" + product_id + " m_product_id=" + m_product_id)
            categoryName = categoryDoc.__dict__.get("name", categ_id)
            client.add_document(keyName, product_id=product_id, updated=str(row[2]), quality=str(row[3]),
                                supplier_id=str(row[4]), prod_id=str(row[5]), catid=categ_id,
                                m_prod_Id=m_product_id, ean_upc=str(row[8]), on_market=str(row[9]),
                                country_market=str(row[10]), model_name=str(row[11]),
                                product_view=str(row[12]),
                                high_pic=str(row[13]),
                                high_pic_size=ifnull(str(row[14])),
                                high_pic_width=ifnull(str(row[15])),
                                high_pic_height=ifnull(str(row[16])),
                                m_supplier_id=m_supplier_id,
                                m_supplier_name=str(row[18]), ean_upc_is_approved=str(row[19]),
                                limited=str(row[20]),
                                date_added=str(row[21]),
                                category_name=categoryName
                                )
            # print("column value " + col)
            # alternative product keys[16
            #  hash key is prod string with prod_id and finally supplier_id
            # hash_key = "prod:" + row[5] + ":" + row[4]
            #  hash key is prod string with m_supplier_name and finally prod_id
            # hash_key = "prod:" + row[18] + ":" + row[5]
            #  hash key is prod string with sequential id
            if prod_idx % 10000 == 0:
                print(str(prod_idx) + " rows loaded")
        csv_file.close()
        print(str(prod_idx) + " rows loaded")
    print("Finished productimport.py at " + str(datetime.datetime.now()))


if '__main__' == __name__:
    main()
