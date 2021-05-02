from enum import unique, Enum


# keys for the output json
@unique
class JsonStructureKey(Enum):
    TITLE = 'title'
    VERSION = 'versions'
    CONTENTS = 'table_of_contents'
    REVISIONS = 'revisions'
    BIBLIOGRAPHY = 'bibliography'
    OTHER = 'other'

    @staticmethod
    def get_values() -> list:
        return [key.value for key in JsonStructureKey]
