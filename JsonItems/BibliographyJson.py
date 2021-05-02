from typing import Dict, List

from JsonItems.IJsonItem import IJsonItem


class BibliographyJson(IJsonItem):
    def __init__(self, bibliography: Dict[str, str]):
        self._bibliography = bibliography

    def get_structure_for_json(self):
        tmp = {}
        for key, item in self._bibliography.items():
            if not item:
                continue
            tmp[key] = item
        return tmp
