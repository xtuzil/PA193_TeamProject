import re
from datetime import datetime
from typing import List

from Certificate import Certificate

from Enum.JsonStructureKeys import JsonStructureKey
from JsonItems.RevisionsJson import RevisionsJson
from ParsingModules.IParsingModule import IParsingModule


# TODO: potential improve - change places date and version: 0782V5b_pdf.txt, 1105b_pdf.txt, [ST-Lite-EAC]_(
#  v1.1)_2018_2000036361_-_Security_Target_Lite_IDeal_Pass_v2.3-n_(SAC_EAC_Polymorphic).txt

class RevisionsParsingModule(IParsingModule):
    _revisions_title_regex_string = r"[\d\s.]*(?:Revision History|Version Control|DOCUMENT EVOLUTION|" \
                                    r"(?:Rev *Date *Description\n))[^ ..]"

    _version = r"(?: Version)? {0,20}((?:\d\.)+\d)"
    _date = r"(\d{2,4}\s{0,2}[- \.]\s{0,2}(?:(?:\w+)|(?:\d{2}))\s{0,2}[- \.]\s{0,2}\d{2,4})"
    _description = r" {1,100}([A-Za-z].*\n(?: {5,50}[\(“\w].*(?:\n)+)*)"
    _revision_regex_string = fr"{_version}\s+(?:{_date})?:?{_description}"

    @staticmethod
    def _change_date_format(date: str) -> str:
        try:
            d = datetime.strptime(date, '%d-%B-%Y')
            return d.strftime('%Y-%m-%d')
        except ValueError:
            pass
        try:
            d = datetime.strptime(date, '%d %B %Y')
            return d.strftime('%Y-%m-%d')
        except ValueError:
            pass
        try:
            d = datetime.strptime(date, '%d.%m.%Y')
            return d.strftime('%Y-%m-%d')
        except ValueError:
            pass
        return date

    @staticmethod
    def _cut_author_if_exists(desc: str) -> str:
        return re.sub(r"(\w+ +){1,3} {5,}", "", desc)

    @staticmethod
    def _change_newline(string: str) -> str:
        change_newlines_to_space = re.sub(r"\n\s+", " ", string)
        return change_newlines_to_space[:-1]

    @staticmethod
    def _is_revisions_on_page(certificate: Certificate, page_number: int) -> bool:
        page_content = certificate.get_page_content(page_number)
        founded = re.search(RevisionsParsingModule._revisions_title_regex_string, page_content, re.IGNORECASE)
        return founded is not None

    @staticmethod
    def _find_revisions_page_number(certificate: Certificate) -> int:
        for page_number in range(1, certificate.get_pages_count()):
            if RevisionsParsingModule._is_revisions_on_page(certificate, page_number):
                return page_number
        return -1

    @staticmethod
    def parse(certificate: Certificate):
        revisions_list = []

        revisions_page = RevisionsParsingModule._find_revisions_page_number(certificate)
        if revisions_page == -1:
            certificate.set_json_key_item(JsonStructureKey.REVISIONS, RevisionsJson([]))
            return

        page_content = certificate.get_page_content(revisions_page)
        revisions = re.findall(RevisionsParsingModule._revision_regex_string, page_content, re.M)

        for revision in revisions:
            version = revision[0][:-1] if revision[0][-1] == ' ' else revision[0]
            date = RevisionsParsingModule._change_date_format(revision[1])

            desc = RevisionsParsingModule._change_newline(revision[2])
            desc = RevisionsParsingModule._cut_author_if_exists(desc)
            revision_dict = {'version': version, 'date': date, 'description': desc}
            revisions_list.append(revision_dict)

        certificate.set_json_key_item(JsonStructureKey.REVISIONS, RevisionsJson(revisions_list))
