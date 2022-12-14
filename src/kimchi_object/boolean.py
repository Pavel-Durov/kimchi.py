from src.kimchi_object.hash_key import HashKey
from src.kimchi_object.object import HashableObject, Object


class Boolean(HashableObject):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.BOOLEAN_OBJ

    def inspect(self):
        return str(self.value)

    def __str__(self):
        return self.inspect()

    def hash_key(self):
        if self.value:
            return HashKey(self.type(), 1)
        else:
            return HashKey(self.type(), 0)
