from enum import auto, StrEnum
import re
import warnings

MAX_QUOTE_LENGTH = 50


# The two classes below are available for you to use
# You do not need to implement them
class VariantMode(StrEnum):
    NORMAL = auto()
    UWU = auto()
    PIGLATIN = auto()


class DuplicateError(Exception):
    """Error raised when there is an attempt to add a duplicate entry to a database"""


def pig_latin_format(word: str) -> str:
    vowels = ["A", "a", "E", "e", "I", "i", "O", "o", "U", "u"]
    word = word.lower()
    if word[0] in vowels:
        return word + "way"

    # Find first consonant index
    consonant_index = 0
    for i, char in enumerate(word):
        if char in vowels:
            consonant_index = i
            break
    first_consonant_cluster = word[:consonant_index]
    word_tail = word[consonant_index:]
    pig_latin_word = word_tail + first_consonant_cluster + "ay"
    return pig_latin_word


# Implement the class and function below
class Quote:
    def __init__(self, quote: str, mode: "VariantMode") -> None:
        if len(quote) > 50:
            raise ValueError("Quote is too long")

        self.quote = quote
        self.mode = mode

    def __str__(self) -> str:
        return self._create_variant()

    def _create_variant(self) -> str:
        """
        Transforms the quote to the appropriate variant indicated by `self.mode` and returns the result
        """
        match self.mode:
            case "normal":
                return self.quote

            case "uwu":
                base_str = self.quote
                quote_list = base_str.split()
                modified_quote_list = []
                for word in quote_list:
                    word = word.replace("L", "W").replace("l", "w")
                    word = word.replace("R", "W").replace("r", "w")
                    if word.startswith("u"):
                        modified_quote_list.append(f"u-u{word[1:]}")
                    elif word.startswith("U"):
                        modified_quote_list.append(f"U-U{word[1:]}")
                    else:
                        modified_quote_list.append(word)

                uwu_quote = " ".join(modified_quote_list)

                if len(uwu_quote) > 50:
                    quote_list = base_str.split()
                    modified_quote_list = []
                    for word in quote_list:
                        word = word.replace("L", "W").replace("l", "w")
                        word = word.replace("R", "W").replace("r", "w")
                        modified_quote_list.append(word)

                    warnings.warn("Quote too long, only partially transformed")
                    uwu_quote = " ".join(modified_quote_list)

                    if len(uwu_quote) > 50:
                        raise ValueError("Quote is too long")

                if self.quote == uwu_quote:
                    raise ValueError("Quote was not modified")

                return uwu_quote

            case "piglatin":
                base_str = self.quote
                quote_list = base_str.split()
                modified_quote_list = [pig_latin_format(word) for word in quote_list]
                pig_latin_quote = " ".join(modified_quote_list).capitalize()

                if self.quote == pig_latin_quote or len(pig_latin_quote) > 50:
                    raise ValueError("Quote was not modified")

                return pig_latin_quote


def run_command(command: str) -> None:
    """
    Will be given a command from a user. The command will be parsed and executed appropriately.

    Current supported commands:
        - `quote` - creates and adds a new quote
        - `quote uwu` - uwu-ifys the new quote and then adds it
        - `quote piglatin` - piglatin-ifys the new quote and then adds it
        - `quote list` - print a formatted string that lists the current
           quotes to be displayed in discord flavored markdown
    """

    # Parse command
    if command[:7] == 'quote "' or command[:7] == 'quote “':
        quote_mode = "normie"
    elif command[6:9] == "uwu":
        quote_mode = "uwu"
    elif command[6:14] == "piglatin":
        quote_mode = "piglatin"
    elif command[6:10] == "list":
        quote_mode = "list"
    else:
        raise ValueError("Invalid command")

    # Parse quote
    quote_mode_pattern = r'\b(quote(?: uwu| list| piglatin)?)\b'
    quoted_quote = re.split(quote_mode_pattern, command)[-1].strip()
    quote = quoted_quote.replace('"', "").replace('“', "").replace('”', "")

    match quote_mode:
        case "normie":
            quote = Quote(quote=quote, mode=VariantMode.NORMAL)

            try:
                Database.add_quote(quote)
            except DuplicateError:
                print("Quote has already been added previously")

        case "uwu":
            quote = Quote(quote=quote, mode=VariantMode.UWU)

            try:
                Database.add_quote(quote)
            except DuplicateError:
                print("Quote has already been added previously")

        case "piglatin":
            quote = Quote(quote=quote, mode=VariantMode.PIGLATIN)

            try:
                Database.add_quote(quote)
            except DuplicateError:
                print("Quote has already been added previously")

        case "list":
            quote_list = [f"- {quote}" for quote in Database.get_quotes()]
            quote_str = "\n".join(quote_list)
            print(quote_str)


# The code below is available for you to use
# You do not need to implement it, you can assume it will work as specified
class Database:
    quotes: list["Quote"] = []

    @classmethod
    def get_quotes(cls) -> list[str]:
        "Returns current quotes in a list"
        return [str(quote) for quote in cls.quotes]

    @classmethod
    def add_quote(cls, quote: "Quote") -> None:
        "Adds a quote. Will raise a `DuplicateError` if an error occurs."
        if str(quote) in [str(quote) for quote in cls.quotes]:
            raise DuplicateError
        cls.quotes.append(quote)
