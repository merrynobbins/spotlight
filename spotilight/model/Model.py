class Model:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs
        
    @staticmethod
    def from_object_list(objects):
        return [Model.from_object(obj) for obj in objects]
    
    @staticmethod
    def from_object(obj):
        return Model(**obj)