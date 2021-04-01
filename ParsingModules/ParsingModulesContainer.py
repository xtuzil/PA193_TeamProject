from typing import Type

from ParsingModules.IParsingModule import IParsingModule
from ParsingModules.VersionsParsingModule import VersionsParsingModule


class ParsingModulesContainer:
    @staticmethod
    def get_parsing_modules() -> list[Type[IParsingModule]]:
        return [
            VersionsParsingModule,
        ]
