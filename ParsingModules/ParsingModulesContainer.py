from typing import Type, List, Optional

from ParsingModules.IParsingModule import IParsingModule
from ParsingModules.RevisionsParsingModule import RevisionsParsingModule
from ParsingModules.TableOfContentParsingModule import TableOfContentParsingModule
from ParsingModules.TitleParsingModule import TitleParsingModule
from ParsingModules.VersionsParsingModule import VersionsParsingModule
from ParsingModules.BibliographyParsingModule import BibliographyParsingModule
from ParsingModules.EmptyOtherModule import EmptyModule

from Enum.JsonStructureKeys import JsonStructureKey


class ParsingModulesContainer:
    MODULES = {
        JsonStructureKey.TITLE.value: TitleParsingModule,
        JsonStructureKey.VERSION.value: VersionsParsingModule,
        JsonStructureKey.CONTENTS.value: TableOfContentParsingModule,
        JsonStructureKey.REVISIONS.value: RevisionsParsingModule,
        JsonStructureKey.BIBLIOGRAPHY.value: BibliographyParsingModule,
        JsonStructureKey.OTHER.value: EmptyModule,
    }

    @staticmethod
    def _get_parsing_module(module_key: JsonStructureKey) -> Optional[Type[IParsingModule]]:
        if module_key in ParsingModulesContainer.MODULES:
            return ParsingModulesContainer.MODULES[module_key]
        return None

    @staticmethod
    def get_parsing_modules(pretty_print: Optional[List[JsonStructureKey]] = None) -> List[Type[IParsingModule]]:
        if pretty_print is None:
            return [
                TitleParsingModule,
                BibliographyParsingModule,
                RevisionsParsingModule,
                VersionsParsingModule,
                TableOfContentParsingModule,
                EmptyModule,
            ]
        modules = []
        for i in pretty_print:
            module = ParsingModulesContainer._get_parsing_module(i)
            if module:
                modules.append(module)
        return modules
