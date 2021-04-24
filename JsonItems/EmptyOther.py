from typing import Union, List

from JsonItems.IJsonItem import IJsonItem


class EmptyOther(IJsonItem):
    def get_structure_for_json(self):
        return []
