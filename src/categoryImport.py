import xml.etree.ElementTree as ET
from redisearch import Client

client = Client('category', 'localhost', 6379)


def main():
    with open('../data/CategoriesList.xml') as xml_file:
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
            cat_score = cat.attrib['Score']
            # print("ID is ", str(cat_id))
            for cat_child in cat:
                # print("cat_child is " + str(cat_child))
                if cat_child.tag == 'Name' and cat_child.attrib['langid'] == '1':
                    cat_name = cat_child.attrib['Value']
                    print("cat_name=" + cat_name)
                elif cat_child.tag == 'ParentCategory' and cat_id != "1":
                    parent_cat_id = cat_child.attrib['ID']
                    print("parent_cat_id is " + parent_cat_id)
                    for parent_child in cat_child:
                        # print("parent_child is " + str(parent_child))
                        for name in parent_child:
                            # print("name under parent child is " + str(name))
                            if name.tag == 'Name' and name.attrib['langid']  == '1':
                                 parent_cat_name = name.attrib['Value']
                    client.add_document("category:" + str(cat_id), ID=str(cat_id), lowpic=str(cat.attrib['LowPic']),
                                        thumbpic=str(cat.attrib['ThumbPic']),name=cat_name,
                                        parentcatid=parent_cat_id, parentcatname=parent_cat_name)
            if cat_cntr % 1000 == 0:
                print(str(cat_cntr) + " categories loaded")

    xml_file.close()
    print(str(cat_cntr) + " categories loaded")


if '__main__' == __name__:
    main()
