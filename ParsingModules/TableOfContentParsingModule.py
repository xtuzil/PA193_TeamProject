from typing import Union, List

from Certificate import Certificate
from JsonItems.TableOfContent import TableOfContent
from ParsingModules.IParsingModule import IParsingModule
from ParsingModules.ToCHelper.SingleColumnParser import SingleColumnParser
from Enum.JsonStructureKeys import JsonStructureKey
from ParsingModules.ToCHelper.TwoColumnParser import TwoColumnParser


class TableOfContentParsingModule(IParsingModule):
    @staticmethod
    def __get_table_headlines():
        return [
            "table of contents",
            "table of content",
            "content",
            "contents",
        ]

    @staticmethod
    def __wrong_headline():
        return [
            "table",
            "tables",
            "list of tables",
            "figures",
            "figure",
            "list of figures"
        ]

    @staticmethod
    def parse(certificate: Certificate):
        toc_pages = TableOfContentParsingModule.__get_first_toc_page_number(certificate)
        if not toc_pages:
            return
        single_col = True
        if TableOfContentParsingModule._toc_is_two_columns(certificate, toc_pages[0]):
            single_col = False
        toc = []
        for toc_page in toc_pages:
            if not single_col:
                # ToC has two columns
                toc.extend(TableOfContentParsingModule._parse_two_column(certificate, toc_page))
            else:
                # ToC single column
                toc.extend(TableOfContentParsingModule._parse_single_column(certificate, toc_page))
        certificate.set_json_key_item(JsonStructureKey.CONTENTS, TableOfContent(toc))

    @staticmethod
    def __get_first_toc_page_number(certificate: Certificate) -> List[int]:
        probable_first_page = []
        tmp = []
        probably_wrong_page = []
        for page_number in range(1, certificate.get_pages_count() + 1):
            current_trimmed_page = certificate.get_page_content_trim(page_number).lower()

            if "..." not in current_trimmed_page and ". . ." not in \
                    current_trimmed_page and " "*5 not in current_trimmed_page:
                continue

            matches = 0
            for i in range(1, certificate.get_pages_count() + 1):
                if " "*3 + str(i) + "\n" in current_trimmed_page \
                        or "."*3 + str(i) + "\n" in current_trimmed_page \
                        or "."*3 + " " + str(i) + "\n" in current_trimmed_page:
                    matches += 1
            if matches < 5:
                continue

            has_wrong = False
            for wrong in TableOfContentParsingModule.__wrong_headline():
                if wrong + "\n" in current_trimmed_page:
                    has_wrong = True
                    break

            if has_wrong:
                continue

            if page_number - 1 not in tmp:
                probable_first_page.append(page_number)
            if page_number - 1 not in tmp and len(tmp) > 0:
                probably_wrong_page.extend(tmp)

            tmp.append(page_number)

        # if len(probably_wrong_page) > 1:
        #     print("Warning: " + certificate.get_filename() + " " + str(probably_wrong_page))

        return tmp

    @staticmethod
    def _toc_is_two_columns(certificate: Certificate, page_number: int) -> bool:
        page = certificate.get_page_content_trim(page_number).split("\n")
        for line in page:
            line = line.replace(" ", "")
            dot_counter = 0
            dot_ended = False
            for letter in line:
                if letter == ".":
                    dot_counter += 1
                    continue
                if dot_counter > 4:
                    if dot_ended:
                        return True
                    dot_ended = True
                dot_counter = 0
        return False

    @staticmethod
    def _parse_single_column(certificate: Certificate, toc_page_number: int) -> List[List[Union[str, int]]]:
        page = certificate.get_page_content(toc_page_number).split("\n")
        parser = SingleColumnParser()
        table_of_content = []
        for line in page:
            chapter, chapter_name, page_number = parser.parse(line)
            parser.reset()
            if chapter is None:
                continue
            table_of_content.append([chapter, chapter_name, page_number])

        return table_of_content

    @staticmethod
    def _parse_two_column(certificate: Certificate, page_number: int) -> List[List[Union[str, int]]]:
        page = certificate.get_page_content(page_number)
        parser = TwoColumnParser(page, certificate)
        # return [["", "", -1]]

        return parser.parse()
