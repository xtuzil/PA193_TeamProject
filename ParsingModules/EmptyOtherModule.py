from Certificate import Certificate
from Enum.JsonStructureKeys import JsonStructureKey
from JsonItems.EmptyOther import EmptyOther
from ParsingModules.IParsingModule import IParsingModule


class EmptyModule(IParsingModule):
    @staticmethod
    def parse(certificate: Certificate):
        certificate.set_json_key_item(JsonStructureKey.OTHER, EmptyOther())
