from typing import Dict, List

from Enum.Versions import Versions
from JsonItems.IJsonItem import IJsonItem


class VersionsJson(IJsonItem):
    def __init__(self, versions: Dict[Versions, List[str]]):
        self._versions = versions

    def get_structure_for_json(self):
        tmp = {}
        for key, item in self._versions.items():
            if not item:
                continue
            tmp[key.value] = item
        return tmp
