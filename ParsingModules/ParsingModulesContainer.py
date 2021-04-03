from typing import Type, List

from ParsingModules.IParsingModule import IParsingModule
from ParsingModules.VersionsParsingModule import VersionsParsingModule
from ParsingModules.BibliographyParsingModule import BibliographyParsingModule


class ParsingModulesContainer:
    @staticmethod
    def get_parsing_modules() -> List[Type[IParsingModule]]:
        return [
            VersionsParsingModule,
            BibliographyParsingModule,
        ]
