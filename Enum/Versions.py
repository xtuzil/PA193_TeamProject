from enum import unique, Enum

# keys for the output json
@unique
class Versions(Enum):
    EAL = 'eal'
    DES = 'des'
    ECC = 'ecc'
    RSA = 'rsa'
    SHA = 'sha'
    JAVA_PLATFORM = 'java_platform'
    GLOBAL_PLATFORM = 'global_platform'
