import json
import ntpath
from typing import Optional

from Enum.JsonStructureKeys import JsonStructureKey
from IJsonItem import IJsonItem


# Class representation of certificate
# it contains content, filename, content per page
# content per page is guessed based on footers
class Certificate:
    def __init__(self, filename: str, content: str):
        self._filename = ntpath.basename(filename)
        # backup file name
        if not self._filename:
            self._filename = filename
        self._content = content
        self._pages = self._get_per_pages()
        self._json = {}

    def _get_per_pages(self) -> dict[int, str]:
        pages = {}
        page_number = 1
        for page_content in self._content.split('\f'):
            pages[page_number] = page_content
            page_number += 1
        return pages

    def get_page_numbers(self) -> list[int]:
        return list(self._pages.keys())

    def get_page_content(self, page: int) -> str:
        if page not in self._pages:
            raise Exception("not valid page")

        return self._pages[page]

    def get_whole_content(self) -> str:
        return self._content

    def get_filename(self):
        return self._filename

    def set_json_key_item(self, key: JsonStructureKey, item: IJsonItem):
        self._json[key] = item

    def to_json(self, pretty_print: Optional[list[JsonStructureKey]]) -> str:
        tmp = {}
        for key, item in self._json:
            tmp[key.value] = item.get_structure_for_json()

        if pretty_print is not None:
            pretty_printed = {}
            for key in pretty_print:
                if key.value in tmp:
                    pretty_printed[key.value] = tmp[key.value]
            return json.dumps(pretty_printed, indent=4, sort_keys=True)

        return json.dumps(tmp)

    def get_json_filename(self):
        tmp_name = self._filename
        if tmp_name.endswith(".txt"):
            tmp_name = tmp_name[:-len(".txt")]
        return tmp_name + ".json"
