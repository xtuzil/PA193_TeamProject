from JsonItems.IJsonItem import IJsonItem


class Title(IJsonItem):
    def __init__(self, title: str):
        self._title = title

    def get_structure_for_json(self):
        return self._title
