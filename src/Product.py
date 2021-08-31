class Product(object):
    def __init__(self, **kwargs):
        self.path = None
        self.product_id = None
        self.updated = None
        self.quality = None
        self.supplier_id = None
        self.prod_id = None
        self.catid = None
        self.m_prod_id = None
        self.ean_upc = None
        self.on_market = None
        self.country_market = None
        self.model_name = None
        self.product_view = None
        self.high_pic = None
        self.high_pic_size = None
        self.high_pic_width = None
        self.high_pic_height = None
        self.m_supplier_id = None
        self.m_supplier_name = None
        self.ean_upc_is_approved = None
        self.Limited = None
        self.Date_Added = None
        self.key_name = None
        self.category_name = None
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return str(self.__dict__)

    def get_key(self):
        if self.key_name is not None:
            return str(self.key_name)
        else:
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
            return self.key_name

    def set_category_name(self, category_name):
        self.category_name = category_name