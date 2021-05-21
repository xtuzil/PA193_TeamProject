from enum import unique, Enum, auto
from typing import List, Union

from Certificate import Certificate


@unique
class TWO_COL_PARSER_STATE(Enum):
    EMPTY = auto(),
    CHAPTER = auto(),
    NAME = auto(),
    SPACE_PLACEHOLDER = auto(),
    PAGE_NUMBER = auto(),
    END = auto(),
    ERROR = auto(),
    LEFT = auto(),
    RIGHT = auto(),
    NEXT_LINE = auto(),
    SKIP_LINE = auto()


class TwoColumnParser:
    _CONFIG_SPACE_BAR = 16
    _CONFIG_DOTS = 3

    _CONFIG_ALLOWED_CHARS = ["(", "[", "]", ")"]

    def __init__(self, content: str, certificate: Certificate):
        self._content = content
        self._STATE_LEFT = TWO_COL_PARSER_STATE.EMPTY
        self._STATE_RIGHT = TWO_COL_PARSER_STATE.EMPTY
        self._STATE = TWO_COL_PARSER_STATE.EMPTY
        self._SIDE = TWO_COL_PARSER_STATE.LEFT
        self._left_chapter = None
        self._left_chapter_name = ''
        self._left_page_number = None
        self._right_chapter = None
        self._right_chapter_name = ''
        self._right_page_number = None
        self._dot_counter = 0
        self._space_counter = 0
        self._toc_left = []
        self._toc_right = []

        self.tmp = certificate

    def parse(self) -> List[List[Union[str, int]]]:
        lines = self._content.split("\n")
        line_i = 0
        for position in range(len(self._content)):
            line = lines[line_i]
            if self._STATE_LEFT == TWO_COL_PARSER_STATE.NEXT_LINE and line == "" and not self._have_found_toc():
                self._reset_left()

            if self._STATE_RIGHT == TWO_COL_PARSER_STATE.NEXT_LINE and line == "" and not self._have_found_toc():
                self._reset_right()

            letter = self._content[position]
            if self._STATE == TWO_COL_PARSER_STATE.EMPTY:
                self._action_empty(letter)
            elif self._STATE == TWO_COL_PARSER_STATE.CHAPTER:
                self._action_chapter(letter)
            elif self._STATE == TWO_COL_PARSER_STATE.NAME:
                self._action_chapter_name(letter)
            elif self._STATE == TWO_COL_PARSER_STATE.SPACE_PLACEHOLDER:
                self._action_space_fill(letter, position)
            elif self._STATE == TWO_COL_PARSER_STATE.PAGE_NUMBER:
                self._action_page_number(letter)
            elif self._STATE == TWO_COL_PARSER_STATE.SKIP_LINE and letter != "\n":
                continue
            if letter == "\n":
                self._action_new_line(letter)
                line_i += 1
        tmp = []
        tmp.extend(self._toc_left)
        tmp.extend(self._toc_right)
        return tmp

    def _action_empty(self, letter: str):
        if letter == " ":
            return

        if (letter.isalnum() or letter in self._CONFIG_ALLOWED_CHARS) \
                and self._STATE_LEFT == TWO_COL_PARSER_STATE.NEXT_LINE \
                and self._SIDE == TWO_COL_PARSER_STATE.LEFT:
            self._left_chapter_name += letter
            self._STATE = TWO_COL_PARSER_STATE.NAME
            self._STATE_LEFT = TWO_COL_PARSER_STATE.NAME
        elif (letter.isalnum() or letter in self._CONFIG_ALLOWED_CHARS) \
                and self._STATE_RIGHT == TWO_COL_PARSER_STATE.NEXT_LINE \
                and self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
            self._right_chapter_name += letter
            self._STATE = TWO_COL_PARSER_STATE.NAME
            self._STATE_RIGHT = TWO_COL_PARSER_STATE.NAME
        elif letter.isnumeric():
            if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._STATE_LEFT = TWO_COL_PARSER_STATE.CHAPTER
                self._STATE = TWO_COL_PARSER_STATE.CHAPTER
                self._left_chapter = letter
            if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                self._STATE_RIGHT = TWO_COL_PARSER_STATE.CHAPTER
                self._STATE = TWO_COL_PARSER_STATE.CHAPTER
                self._right_chapter = letter
        elif letter.isalpha():
            self._STATE = TWO_COL_PARSER_STATE.SKIP_LINE

    def _action_chapter(self, letter: str):
        if letter == "." or letter.isnumeric():
            if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                self._right_chapter += letter
            elif self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._left_chapter += letter
        elif letter == " ":
            if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._STATE_LEFT = TWO_COL_PARSER_STATE.NAME
                self._STATE = TWO_COL_PARSER_STATE.NAME
            elif self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                self._STATE_RIGHT = TWO_COL_PARSER_STATE.NAME
                self._STATE = TWO_COL_PARSER_STATE.NAME

    def _action_chapter_name(self, letter: str):
        if letter == ".":
            self._dot_counter += 1
            if self._dot_counter >= self._CONFIG_DOTS:
                if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                    self._STATE_LEFT = TWO_COL_PARSER_STATE.SPACE_PLACEHOLDER
                    self._STATE = TWO_COL_PARSER_STATE.SPACE_PLACEHOLDER
                    self._left_chapter_name = self._left_chapter_name[:-self._CONFIG_DOTS]
                if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                    self._STATE_RIGHT = TWO_COL_PARSER_STATE.SPACE_PLACEHOLDER
                    self._STATE = TWO_COL_PARSER_STATE.SPACE_PLACEHOLDER
                    self._right_chapter_name = self._right_chapter_name[:-self._CONFIG_DOTS]
        elif letter == " ":
            self._space_counter += 1
            if self._space_counter >= self._CONFIG_SPACE_BAR and self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._STATE_LEFT = TWO_COL_PARSER_STATE.NEXT_LINE
                self._STATE = TWO_COL_PARSER_STATE.EMPTY
                self._SIDE = TWO_COL_PARSER_STATE.RIGHT
        else:
            self._dot_counter = 0
            self._space_counter = 0

        if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
            self._left_chapter_name += letter
        if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
            self._right_chapter_name += letter

    def _action_space_fill(self, letter: str, position: int):
        if letter == '.' or letter == " ":
            return

        if letter.isnumeric():
            next_number_position = position + 1
            # 2 or more digit number
            while next_number_position < len(self._content) and \
                    self._content[next_number_position].isnumeric():
                next_number_position += 1

            while next_number_position < len(self._content) and \
                    not self._content[next_number_position].isnumeric():
                next_non_number = self._content[next_number_position]
                if next_non_number == " " or next_non_number == "\n":
                    if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                        self._STATE_LEFT = TWO_COL_PARSER_STATE.PAGE_NUMBER
                        self._STATE = TWO_COL_PARSER_STATE.PAGE_NUMBER
                        self._left_page_number = letter
                    if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                        self._STATE_RIGHT = TWO_COL_PARSER_STATE.PAGE_NUMBER
                        self._STATE = TWO_COL_PARSER_STATE.PAGE_NUMBER
                        self._right_page_number = letter
                    break
                next_number_position += 1

    def _action_page_number(self, letter: str):
        if letter == " ":
            if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._SIDE = TWO_COL_PARSER_STATE.RIGHT
                self._STATE_LEFT = TWO_COL_PARSER_STATE.END
                self._STATE = TWO_COL_PARSER_STATE.EMPTY
        elif letter == "\n":
            if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._STATE_LEFT = TWO_COL_PARSER_STATE.END
            if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                self._STATE_RIGHT = TWO_COL_PARSER_STATE.END
        elif letter.isnumeric():
            if self._SIDE == TWO_COL_PARSER_STATE.LEFT:
                self._left_page_number += letter
            if self._SIDE == TWO_COL_PARSER_STATE.RIGHT:
                self._right_page_number += letter

    def _action_new_line(self, letter: str):
        if not letter == "\n":
            return

        if self._STATE_LEFT == TWO_COL_PARSER_STATE.END:
            self._toc_left.append([self._left_chapter, self._left_chapter_name.strip(), self._left_page_number])
            self._reset_left()

        if self._STATE_RIGHT == TWO_COL_PARSER_STATE.END:
            self._toc_right.append([self._right_chapter, self._right_chapter_name.strip(), self._right_page_number])
            self._reset_right()

        if self._STATE_LEFT != TWO_COL_PARSER_STATE.NAME and self._STATE_LEFT != TWO_COL_PARSER_STATE.NEXT_LINE:
            self._STATE_LEFT = TWO_COL_PARSER_STATE.EMPTY
        else:
            self._STATE_LEFT = TWO_COL_PARSER_STATE.NEXT_LINE

        if self._STATE_RIGHT != TWO_COL_PARSER_STATE.NAME and self._STATE_RIGHT != TWO_COL_PARSER_STATE.NEXT_LINE:
            self._STATE_RIGHT = TWO_COL_PARSER_STATE.EMPTY
        else:
            self._STATE_RIGHT = TWO_COL_PARSER_STATE.NEXT_LINE

        self._STATE = TWO_COL_PARSER_STATE.EMPTY
        self._SIDE = TWO_COL_PARSER_STATE.LEFT

    def _reset_left(self) -> None:
        self._STATE_LEFT = TWO_COL_PARSER_STATE.EMPTY
        self._left_chapter = None
        self._left_chapter_name = ''
        self._left_page_number = None

    def _reset_right(self) -> None:
        self._right_chapter = None
        self._right_chapter_name = ''
        self._right_page_number = None

    def _have_found_toc(self) -> bool:
        return len(self._toc_left) > 0 or len(self._toc_right) > 0