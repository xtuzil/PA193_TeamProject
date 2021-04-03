from typing import Type, List

from ParsingModules.IParsingModule import IParsingModule
from ParsingModules.TitleParsingModule import TitleParsingModule
from ParsingModules.VersionsParsingModule import VersionsParsingModule


class ParsingModulesContainer:
    @staticmethod
    def get_parsing_modules() -> List[Type[IParsingModule]]:
        return [
            VersionsParsingModule,
            TitleParsingModule
        ]
