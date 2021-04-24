from enum import unique, Enum, auto
from typing import Optional


@unique
class PARSER_STATE(Enum):
    EMPTY = auto(),
    CHAPTER = auto(),
    NAME = auto(),
    SPACE_PLACEHOLDER = auto(),
    PAGE_NUMBER = auto(),
    END = auto()
    ERROR = auto()


class SingleColumnParser:
    def __init__(self):
        self._STATE = PARSER_STATE.EMPTY
        self._chapter = None
        self._page_number = None
        self._chapter_name = None
        self._space_counter = 0
        self._dot_counter = 0

    def reset(self):
        self._STATE = PARSER_STATE.EMPTY
        self._chapter = None
        self._page_number = None
        self._chapter_name = None
        self._space_counter = 0
        self._dot_counter = 0

    def parse(self, line: str) -> (Optional[str], Optional[str], Optional[int]):
        for letter in line:
            if self._STATE == PARSER_STATE.EMPTY:
                self._action_empty(letter)
            elif self._STATE == PARSER_STATE.CHAPTER:
                self._action_chapter(letter)
            elif self._STATE == PARSER_STATE.NAME:
                self._action_name(letter)
            elif self._STATE == PARSER_STATE.SPACE_PLACEHOLDER:
                self._action_spaces(letter)
            elif self._STATE == PARSER_STATE.PAGE_NUMBER:
                self._action_page_number(letter)
            elif self._STATE == PARSER_STATE.ERROR:
                return None, None, None

        if self._STATE == PARSER_STATE.PAGE_NUMBER:
            return self._chapter, self._clean(self._chapter_name), int(self._page_number)
        return None, None, None

    def _action_empty(self, letter: str) -> None:
        if not self._STATE == PARSER_STATE.EMPTY:
            raise Exception("Wrong state")

        if letter.isalnum():
            self._chapter = letter
            self._STATE = PARSER_STATE.CHAPTER
        elif letter == " ":
            return

    def _action_chapter(self, letter: str) -> None:
        if not self._STATE == PARSER_STATE.CHAPTER:
            raise Exception("Wrong state")

        if letter.isnumeric() and (self._chapter[-1].isnumeric() or self._chapter[-1] == "."):
            self._chapter += letter
        elif letter == "." and (self._chapter[-1].isnumeric() or self._chapter[-1].isalpha()):
            self._chapter += letter
        elif letter == " ":
            self._STATE = PARSER_STATE.NAME
        else:
            self._chapter_name = self._chapter + letter
            self._chapter = ''
            self._STATE = PARSER_STATE.NAME

    def _action_name(self, letter: str) -> None:
        if not PARSER_STATE.NAME == self._STATE:
            raise Exception("Wrong state")

        if letter == " " and self._chapter_name is not None:
            if self._space_counter > 1:
                self._STATE = PARSER_STATE.SPACE_PLACEHOLDER
            self._space_counter += 1
            self._chapter_name += letter
        elif letter == "." and self._chapter_name is not None:
            if self._dot_counter > 1:
                self._STATE = PARSER_STATE.SPACE_PLACEHOLDER
            self._dot_counter += 1
            self._chapter_name += letter
        elif letter == " " and self._chapter_name is None:
            return
        else:
            self._space_counter = 0
            self._dot_counter = 0
            if self._chapter_name is None:
                self._chapter_name = ''
            self._chapter_name += letter

    def _action_spaces(self, letter: str) -> None:
        if not PARSER_STATE.SPACE_PLACEHOLDER == self._STATE:
            raise Exception("Wrong state")

        if letter == " ":
            self._space_counter += 1
        elif letter.isalpha():
            self._STATE = PARSER_STATE.ERROR
        elif letter.isnumeric():
            self._STATE = PARSER_STATE.PAGE_NUMBER
            self._page_number = letter

    def _action_page_number(self, letter: str) -> None:
        if not PARSER_STATE.PAGE_NUMBER == self._STATE:
            raise Exception("Wrong state")

        if letter.isnumeric():
            self._page_number += letter
        else:
            self._STATE = PARSER_STATE.ERROR

    def get_state(self) -> PARSER_STATE:
        return self._STATE

    @staticmethod
    def _clean(string: str) -> str:
        while string[-1] == ".":
            string = string[:-1]
        return string.strip()
