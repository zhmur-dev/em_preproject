class ObjList:
    def __init__(self, data=None):
        self.__prev = None
        self.__data = data
        self.__next = None

    def set_prev(self, obj):
        self.__prev = obj

    def set_data(self, data):
        self.__data = data

    def set_next(self, obj):
        self.__next = obj

    @property
    def get_prev(self):
        return self.__prev

    @property
    def get_data(self):
        return self.__data

    @property
    def get_next(self):
        return self.__next


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_obj(self, obj):
        if self.head is not None:
            obj.set_prev(self.tail)
            self.tail.set_next(obj)
        else:
            self.head = obj
        self.tail = obj

    def remove_obj(self):
        if self.head is not None:
            self.tail = self.tail.get_prev()
            if self.tail is not None:
                self.tail.set_next(None)
            else:
                self.head = None

    def get_data(self):
        result = []
        obj = self.head
        while obj is not None:
            result.append(obj.get_data())
            obj = obj.get_next()
        return result
