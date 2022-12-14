from src.kimchi_object import HashableObject, Object, kimchi_hash
from src.kimchi_object.hash_key import HashKey


class String(HashableObject):
    def __init__(self, value):
        self.value = value

    def type(self):
        return Object.STRING_OBJ

    def inspect(self):
        return self.value

    def __str__(self):
        return self.inspect()

    def hash_key(self):
        return HashKey(Object.STRING_OBJ, kimchi_hash(str(self.value)))
