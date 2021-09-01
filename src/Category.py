class Category(object):
    def __init__(self, **kwargs):
        self.ID = None
        self.LowPic = None
        self.ThumbPic = None
        self.Name = None
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self):
        return str(self.__dict__)

    def get_key(self):
        if self.ID is not None:
            return str(self.ID)