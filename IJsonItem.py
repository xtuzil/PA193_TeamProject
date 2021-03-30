from abc import ABCMeta, abstractmethod


# Should me something like interface to be able to get python structure
# that will be converted to json later
class IJsonItem:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_structure_for_json(self): raise NotImplementedError