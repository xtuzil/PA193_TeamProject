import re
from Certificate import Certificate

from Enum.JsonStructureKeys import JsonStructureKey
from JsonItems.BibliographyJson import BibliographyJson
from ParsingModules.IParsingModule import IParsingModule


class BibliographyParsingModule(IParsingModule):
    _bibliography_title_regex_string = r"[\d\s.]*(?:References|Referenced Literature|Bibliography|" \
                                       r"REFERENCE DOCUMENTS|Literature)"
    _bibliography_regex_string = r'\[.{1,20}\]\n* {1,50}[“\w].*\n(?: {1,50}[\(“\w].*(?:\n)+)*'

    @staticmethod
    def _change_newline(string: str) -> str:
        change_newlines_to_space = re.sub(r"\n\s+", " ", string)
        return re.sub("\n", "", change_newlines_to_space)

    @staticmethod
    def _is_bib_on_page(certificate: Certificate, page_number: int) -> bool:
        page_content = certificate.get_page_content(page_number)
        founded = re.search(BibliographyParsingModule._bibliography_title_regex_string, page_content)

        if founded is not None:
            if re.search(BibliographyParsingModule._bibliography_regex_string,
                         certificate.get_page_content(page_number)) is None:
                return False
            else:
                return True
        return False

    @staticmethod
    def _guess_bibliography_length(certificate: Certificate, start: int) -> int:
        min_b = 2
        max_b = 5
        actual_guess = 0
        for page_number in range(start, certificate.get_pages_count() + 1):
            founded_bibliography = re.search(BibliographyParsingModule._bibliography_regex_string,
                                             certificate.get_page_content(page_number))
            if founded_bibliography is None:
                actual_guess = actual_guess if actual_guess > min_b else min_b
                return actual_guess
            actual_guess += 1
            if actual_guess == max_b:
                break
        return actual_guess

    @staticmethod
    def _find_bibliography_start_page_number(certificate: Certificate) -> int:
        bibliography_start = 0
        for page_number in range(certificate.get_pages_count(), 0, -1):
            if (BibliographyParsingModule._is_bib_on_page(certificate, page_number)) and not \
                    (BibliographyParsingModule._is_bib_on_page(certificate, page_number - 1)):
                bibliography_start = page_number
                break

        return bibliography_start

    @staticmethod
    def parse(certificate: Certificate):
        bibliography_dict = {}

        bibliography_start = BibliographyParsingModule._find_bibliography_start_page_number(certificate)
        if bibliography_start == 0:
            print("Bibliography not found! filename: " + certificate.get_filename())
            return

        bibliography_length = BibliographyParsingModule._guess_bibliography_length(certificate, bibliography_start)

        # found each bibliography
        bibliography_content = ""
        for page_number in range(bibliography_start, bibliography_start + bibliography_length):
            bibliography_content += certificate.get_page_content(page_number)

        bibliography = re.findall(BibliographyParsingModule._bibliography_regex_string, bibliography_content, re.M)

        # parse each bibliography - append to dictionary key:value
        for work in bibliography:
            key_end = (re.search(r"\[.*\]", work)).end()
            desc_start = (re.search(r"\[.*\]\s+", work)).end()
            key = work[:key_end]
            desc = BibliographyParsingModule._change_newline(work[desc_start:])
            bibliography_dict[key] = desc

        certificate.set_json_key_item(JsonStructureKey.BIBLIOGRAPHY, BibliographyJson(bibliography_dict))
