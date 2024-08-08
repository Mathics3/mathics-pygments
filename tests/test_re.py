import re

from mathics_pygments.lexer import Regex


def verify_match_all(string: str, pattern, pattern_type):
    matches = re.match(pattern, string)
    print(f"{string} matches {pattern_type}")
    assert matches
    assert matches.group(0) == string


def test_regex():
    for string in [
        "_Head",
        "__Head",
        "___Head",
        "x_Head",
        "x__Head",
        "x___Head",
        "Foo`Bar_Head",
        "Foo`Bar__Integer",
        "Foo`Bar___Baz",
        "Foo`Bar_Ctx`Baz",
        "Foo`Bar__Ctx`Baz",
        "Foo`Bar___Ctx`Baz`Qux",
    ]:
        verify_match_all(string, Regex.PATTERNS, "Pattern regular expression")

    integers = ["123", "0", "12345678901234567890"]
    for string in integers:
        verify_match_all(string, Regex.INTEGER, "Integer regular expression")

    floats = ["1.23", "10.1", ".123", "987654321123456789.987654321123456789"]
    for string in floats + []:
        verify_match_all(string, Regex.FLOAT, "Float regular expression")

    # FIXME: expand this.
    for string in floats:
        verify_match_all(string, Regex.REAL, "Real regular expression")

    base_numbers = ["2^^101", "8 ^^ 17", "10^^ 3.4"]
    for string in base_numbers:
        verify_match_all(string, Regex.BASE_NUMBER, "Base number regular expression")

    slots = ["#", "#1", "#234"]
    for string in slots:
        verify_match_all(string, Regex.SLOTS, "Slot regular expression")


# For isolated individual testing...
if __name__ == "__main__":
    test_regex()
