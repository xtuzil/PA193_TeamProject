import re

# regex strings for each version
eal_regex_string = r"EAL ?[1-6]\+?"
des_regex_string = r"(?:(?:SINGLE|TRIPLE|DOUBLE)[ -]?|[3T])?DES3?"
ecc_regex_string = r"ECC \d+"
rsa_regex_string = r"RSA(?:(?:[ -_]\d+(?:/\d+)?)|-CRT|SSA-PSS|SignaturePKCS1)"
sha_regex_string = r"SHA[ -_]?\d{1,3}(?:/\d{1,3})?"
java_platform_regex_string = r"Java Card \d(?:.\d)*"
global_platform_regex_string = r"Global ?Platform \d(?:.\d)*"

def findVersions(version):

    regex_string = ""
    if version == "eal":
        regex_string = eal_regex_string
    if version == "des":
        regex_string = des_regex_string
    if version == "ecc":
        regex_string = ecc_regex_string
    if version == "rsa":
        regex_string = rsa_regex_string
    if version == "sha":
        regex_string = sha_regex_string
    if version == "java_platform":
        regex_string = java_platform_regex_string
    if version == "global_platform":
        regex_string = global_platform_regex_string

    version_duplicates = re.findall(regex_string, document, flags = re.IGNORECASE)
    version_set = set(version_duplicates)
    versions = list (version_set)
    return [a for a in versions if a.lower() != version] # filter no version
    




f = open("test.txt", "r")

document = f.read()


eal = findVersions("eal")
des = findVersions("des")
ecc = findVersions("ecc")
rsa = findVersions("rsa")
sha = findVersions("sha")
java_platform = findVersions("java_platform")
global_platform = findVersions("global_platform")

print(global_platform)


