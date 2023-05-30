
class Cache:
    def __init__(self):
        self.cache = {}

    def __getitem__(self, key):
        if key in self.cache:
            return self.cache[key]
        else:
            raise KeyError(f"Key '{key}' not found in the cache.")

    def __setitem__(self, key, value):
        self.cache[key] = value
