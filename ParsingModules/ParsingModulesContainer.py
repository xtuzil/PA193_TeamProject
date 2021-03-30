from ParsingModules.IParsingModule import IParsingModule


# Container for parsing modules.
# After creating one add it here
class ParsingModulesContainer:
    @staticmethod
    def get_parsing_modules() -> list[IParsingModule]:
        return []

