class Enum(frozenset):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError
