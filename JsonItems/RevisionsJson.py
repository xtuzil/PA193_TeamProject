from typing import Dict, List

from JsonItems.IJsonItem import IJsonItem


class RevisionsJson(IJsonItem):
    def __init__(self, revisions:  List[Dict[str, str]]):
        self._revisions = revisions

    def get_structure_for_json(self):
        return self._revisions
        """tmp = {}
        for key, item in self._bibliography.items():
            if not item:
                continue
            tmp[key] = item
        return tmp"""
