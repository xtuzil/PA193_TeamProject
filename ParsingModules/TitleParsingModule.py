from typing import List

from Certificate import Certificate
from Enum.JsonStructureKeys import JsonStructureKey
from JsonItems.Title import Title
from ParsingModules.IParsingModule import IParsingModule


class TitleParsingModule(IParsingModule):
    _blacklist = {"author", "version", "sponsor", "project", "date", "number", "iban", "vat", "common", "criteria",
                  "facility:", "evaluation", "developer:", "report"}
    _whitelist = {"security", "secure", "crypto", "cryptographic", "module", "trusted", "java", "access", "libraries"
                  "smart", "dedicated", "jcop"}


    @staticmethod
    def parse(certificate: Certificate):
        title_page = certificate.get_page_content(1)
        # expecting double new lines before and after title
        candidate_lines = title_page.split("\n\n")
        while '' in candidate_lines:
            candidate_lines.remove('')
        if len(candidate_lines) == 0:
            candidate_lines = title_page.split("\n")
        title = TitleParsingModule.analyze(candidate_lines)
        certificate.set_json_key_item(JsonStructureKey.TITLE, Title(title))

    @staticmethod
    def analyze(candidate_lines: List[str]) -> str:
        candidates = []
        for candidate in candidate_lines:
            candidate = candidate.strip()
            words = candidate.split()
            score = 0
            # expecting title to have at least 6 words
            if len(words) < 6:
                score -= 10 * (6 - len(words))

            for word in words:
                lower_word = word.lower()
                # expecting most words in title to be capital
                if word[0].isupper() or word[0].isnumeric():
                    score += 50 / len(words)

                if lower_word in TitleParsingModule._blacklist:
                    score -= 10

                if lower_word in TitleParsingModule._whitelist:
                    score += 10

            candidates.append((candidate, score))

        candidates.sort(key=lambda item: item[1], reverse=True)
        return " ".join(candidates[0][0].split())
