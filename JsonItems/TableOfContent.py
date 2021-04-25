from typing import Union, List

from JsonItems.IJsonItem import IJsonItem


class TableOfContent(IJsonItem):
    def __init__(self, array: List[List[Union[str, int]]]):
        self._structure = array

    def _get_clean(self):
        tmp = []
        for item in self._structure:
            chapter, chapter_name, page_number = item
            chapter_name = " ".join(chapter_name.replace("\n", " ").strip().split())
            if len(chapter_name) > 0 and chapter_name[-1] == ".":
                chapter_name = chapter_name[:-1]
            tmp.append([chapter, chapter_name, page_number])
        return tmp

    def get_structure_for_json(self):
        return self._get_clean()
