from abc import abstractmethod, ABCMeta
from Certificate import Certificate


# Just an interface for parsing modules
# in main will be called parse
class IParsingModule:
    __metaclass__ = ABCMeta

    @staticmethod
    @abstractmethod
    def parse(certificate: Certificate): raise NotImplementedError
