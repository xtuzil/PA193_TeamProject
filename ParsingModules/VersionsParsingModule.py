import re

from typing import List

from Certificate import Certificate
from Enum.JsonStructureKeys import JsonStructureKey
from Enum.Versions import Versions
from JsonItems.VersionsJson import VersionsJson
from ParsingModules.IParsingModule import IParsingModule


class VersionsParsingModule(IParsingModule):
    # regex strings for each version
    _eal_regex_string = r"EAL ?[1-6]\+?"
    _des_regex_string = r"(?:(?:SINGLE|TRIPLE|DOUBLE)[ -]?|[3T])?DES3?"
    _ecc_regex_string = r"ECC \d+"
    _rsa_regex_string = r"RSA(?:(?:[ -_]\d+(?:/\d+)?)|-CRT|SSA-PSS|SignaturePKCS1)"
    _sha_regex_string = r"SHA[ -_]?\d{1,3}(?:/\d{1,3})?"
    _java_platform_regex_string = r"Java Card \d(?:.\d)*"
    _global_platform_regex_string = r"Global ?Platform \d(?:.\d)*"

    @staticmethod
    def parse(certificate: Certificate):
        versions_map = {
            Versions.EAL: VersionsParsingModule._find_versions(Versions.EAL, certificate.get_whole_content()),
            Versions.DES: VersionsParsingModule._find_versions(Versions.DES, certificate.get_whole_content()),
            Versions.ECC: VersionsParsingModule._find_versions(Versions.ECC, certificate.get_whole_content()),
            Versions.RSA: VersionsParsingModule._find_versions(Versions.RSA, certificate.get_whole_content()),
            Versions.SHA: VersionsParsingModule._find_versions(Versions.SHA, certificate.get_whole_content()),
            Versions.JAVA_PLATFORM: VersionsParsingModule._find_versions(Versions.JAVA_PLATFORM,
                                                                         certificate.get_whole_content()),
            Versions.GLOBAL_PLATFORM: VersionsParsingModule._find_versions(Versions.GLOBAL_PLATFORM,
                                                                           certificate.get_whole_content()),
        }
        certificate.set_json_key_item(JsonStructureKey.VERSION, VersionsJson(versions_map))

    @staticmethod
    def _find_versions(version: Versions, document_content: str) -> List[str]:
        regex_string = VersionsParsingModule._choose_regex(version)

        version_duplicates = re.findall(regex_string, document_content, flags=re.IGNORECASE)
        version_set = set(version_duplicates)
        versions = list(version_set)
        return [a for a in versions if a.lower() != version]  # filter no version

    @staticmethod
    def _choose_regex(version: Versions) -> str:
        regex_string = {
            Versions.EAL: VersionsParsingModule._eal_regex_string,
            Versions.DES: VersionsParsingModule._des_regex_string,
            Versions.ECC: VersionsParsingModule._ecc_regex_string,
            Versions.RSA: VersionsParsingModule._rsa_regex_string,
            Versions.SHA: VersionsParsingModule._sha_regex_string,
            Versions.JAVA_PLATFORM: VersionsParsingModule._java_platform_regex_string,
            Versions.GLOBAL_PLATFORM: VersionsParsingModule._global_platform_regex_string,
        }.get(version, None)

        if regex_string is None:
            raise Exception("Invalid regex string")

        return regex_string
