import xml.etree.ElementTree as ET
import redis

REDIS_HOST = '34.138.134.33'


def main():
    conn = redis.StrictRedis(REDIS_HOST, port=15999, charset="utf-8", decode_responses=True)
    with open('data/CategoriesList.xml') as xml_file:
        # create element tree object
        tree = ET.parse(xml_file)

        # get root element
        root = tree.getroot()
        print("root.tag is ", root.tag)
        cat_cntr = 0
        for child in root:
            print("child tag is " + child.tag)
            print("child attribute is " + str(child.attrib))
        for cat in root.findall('Response/CategoriesList/Category'):
            # print("starting in xml file")
            # print("cat.tag is " + str(cat.tag))
            # print("cat.attribute is " + str(cat.attrib))
            cat_cntr += 1
            cat_id = cat.attrib['ID']
            # print("ID is ", str(cat_id))

            category_id = 'categ:' + cat_id
            conn.hset(category_id, "ID", cat_id)
            if cat.attrib['LowPic']:
                conn.hset(category_id, "lowpic", cat.attrib['LowPic'])
            if cat.attrib['ThumbPic']:
                conn.hset(category_id, "thumbpic", cat.attrib['ThumbPic'])
            for cat_child in cat:
                # category_id is
                # print("cat_child.tag is " + str(cat_child.tag))
                # print("cat_child.attribute is " + str(cat_child.attrib))
                if cat_child.tag == 'Name' and cat_child.attrib['langid'] == '1':
                    cat_name = cat_child.attrib['Value']
                    # print("category name is " + cat_name)
                    conn.hset(category_id, "Name", cat_name)
            if cat_cntr % 1000 == 0:
                print(str(cat_cntr) + " categories loaded")

    xml_file.close()
    print(str(cat_cntr) + " categories loaded")


if '__main__' == __name__:
    main()
