class Product(object):
    def __init__(self, **kwargs):
        self.path = ""
        self.product_id = ""
        self.updated = ""
        self.quality = ""
        self.supplier_id = ""
        self.prod_id = ""
        self.catid = ""
        self.m_prod_id = ""
        self.ean_upc = ""
        self.on_market = ""
        self.country_market = ""
        self.model_name = ""
        self.product_view = ""
        self.high_pic = ""
        self.high_pic_size = ""
        self.high_pic_width = ""
        self.high_pic_height = ""
        self.m_supplier_id = ""
        self.m_supplier_name = ""
        self.ean_upc_is_approved = ""
        self.Limited = ""
        self.Date_Added = ""
        self.key_name = ""
        self.category_name = ""
        self.parent_category_name = ""
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return str(self.__dict__)

    def set_key(self):
        m_product_string = "mprodid:" + self.m_prod_id
        p_product_string = "prodid:" + self.product_id
        # supply
        if self.m_supplier_id and not self.m_supplier_id.isspace():
            supplier_string = ":msupplyid:" + self.m_supplier_id
        else:
            supplier_string = ":supplyid:" + self.supplier_id
        # product
        if self.prod_id and not self.prod_id.isspace():
            product_string = m_product_string + ":" + p_product_string
        else:
            product_string = "prodid:" + self.product_id
        self.key_name = product_string + supplier_string

    def set_category_name(self, category_name):
        self.category_name = str(category_name)

    def set_parent_category_name(self, parent_category_name):
        self.parent_category_name = str(parent_category_name)
