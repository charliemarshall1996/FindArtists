class Cache:

    def __init__(self):
        self.cache = {}

    def get(self):
        return self.cache
    
    def set(self, key, val):
        self.cache[key] = val

    def delete(self, key):
        del self.cache[key]

