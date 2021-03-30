import json
import ntpath
import re
import uuid
from typing import Optional

from Enum.JsonStructureKeys import JsonStructureKey
from IJsonItem import IJsonItem


# Class representation of certificate
# it contains content, filename, content per page
# content per page is guessed based on footers
class Certificate:
    def __init__(self, filename: str, content: str):
        self._filename = ntpath.basename(filename)
        # backup
        if not self._filename:
            self._filename = filename
        self._content = content
        self._pages = self._guess_pages()
        self._json = {}

    # trying to guess each page. Prints warning if not finding footer
    # probably can find also wrong footer
    def _guess_pages(self) -> dict[int, str]:
        placeholder, footer = self._find_footer()
        if footer is None:
            print("Warning! Did not found pages for " + self._filename + ". Skipping")
            return {}
        regex_string_split = self._get_footer_regex(footer, placeholder)
        regex = re.compile(regex_string_split)
        page_numbers = regex.findall(self._content)
        tmp_content = self._content
        pages = {}
        for page_number in page_numbers:
            regex_to_grab_footer = footer.replace(" ", " +").replace(placeholder, " " + page_number )
            concrete_footer = re.findall(regex_to_grab_footer, self._content)
            tmp = regex.split(tmp_content, 1)
            tmp_content = tmp[2]
            pages[int(page_number)] = tmp[0] + concrete_footer[0]
        return pages

    def _find_footer(self) -> (str, str):
        tmp_content = re.sub(' +', ' ', self._content)
        tmp_content_split = tmp_content.splitlines(keepends=True)
        for i in range(5, len(tmp_content_split)):
            tested_are = "".join(tmp_content_split[i - 5: i])
            numbers = [int(x) for x in tested_are.split() if x.isdigit()]
            for number in numbers:
                possible = True
                for increment in range(number, number + 4):
                    if tested_are.replace(str(number), str(increment)) not in tmp_content:
                        possible = False
                        break

                    if tested_are.replace(" " + str(number),  " " + str(increment)) not in tmp_content:
                        possible = False
                if possible:
                    placeholder = "{%" + str(uuid.uuid4()) + "%}"
                    return placeholder, tested_are.replace(str(number), placeholder)
        return None

    @staticmethod
    def _get_footer_regex(footer: str, placeholder: str) -> str:
        regex = footer.replace(" ", " +").split(placeholder)
        return regex[0] + "(?P<page>[0-9]+)" + regex[1]

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
