# -*- coding: utf-8 -*-
# Copyright (c) 2021, 2024 Rocky Bernstein
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

import pytest
from pygments.token import Token

import mathics_pygments.builtins as mma
from mathics_pygments.lexer import MathematicaLexer, MToken

lexer = MathematicaLexer()


def verify(code, expected):
    expected.append((Token.Text.Whitespace, "\n"))
    returned = list(lexer.get_tokens(code))
    assert expected == returned


def verify_all(code_list, expected_list):
    for code, expected in zip(code_list, expected_list):
        verify(code, expected)


def test_comments():
    code = "(* a comment *)"
    expected = [
        (MToken.COMMENT, "(*"),
        (MToken.COMMENT, " a comment "),
        (MToken.COMMENT, "*)"),
    ]
    verify(code, expected)


def test_comments_with_code():
    code = "(* Plot[Sin[x], {x, 0, 2 Pi}] *)"
    expected = [
        (MToken.COMMENT, "(*"),
        (MToken.COMMENT, " Plot[Sin[x], {x, 0, 2 Pi}] "),
        (MToken.COMMENT, "*)"),
    ]
    verify(code, expected)


def test_nested_comments():
    code = "(* foo (* bar *) baz *)"
    expected = [
        (MToken.COMMENT, "(*"),
        (MToken.COMMENT, " foo "),
        (MToken.COMMENT, "(*"),
        (MToken.COMMENT, " bar "),
        (MToken.COMMENT, "*)"),
        (MToken.COMMENT, " baz "),
        (MToken.COMMENT, "*)"),
    ]
    verify(code, expected)


def test_multiline_comment():
    code = "(* a comment\non two lines *)"
    expected = [
        (MToken.COMMENT, "(*"),
        (MToken.COMMENT, " a comment\non two lines "),
        (MToken.COMMENT, "*)"),
    ]
    verify(code, expected)


def test_strings():
    code = [
        '"a string"',
        '"a string \\" with a quote"',
        '"a string with a newline\\n"',
        '"a string with \\ two backslashes"',
    ]
    expected = [
        [
            (MToken.STRING, '"'),
            (MToken.STRING, "a string"),
            (MToken.STRING, '"'),
        ],
        [
            (MToken.STRING, '"'),
            (MToken.STRING, "a string "),
            (MToken.STRING, '\\"'),
            (MToken.STRING, " with a quote"),
            (MToken.STRING, '"'),
        ],
        [
            (MToken.STRING, '"'),
            (MToken.STRING, "a string with a newline"),
            (MToken.STRING, "\\n"),
            (MToken.STRING, '"'),
        ],
        [
            (MToken.STRING, '"'),
            (MToken.STRING, "a string with "),
            (MToken.STRING, "\\"),
            (MToken.STRING, " two backslashes"),
            (MToken.STRING, '"'),
        ],
    ]
    verify_all(code, expected)


def test_integers():
    code = "123"
    expected = [(MToken.NUMBER, "123")]
    verify(code, expected)


def test_floats():
    code = ["1.23", "10.1", ".123"]
    expected = [[(MToken.NUMBER, num)] for num in code]
    verify_all(code, expected)


def test_precision_numbers():
    code = ["1`", "1.2`", "1.23`30", "20`20"]
    expected = [[(MToken.NUMBER, num)] for num in code]
    verify_all(code, expected)


def test_base_numbers():
    code = ["2^^101", "8 ^^ 17", "10^^ 3.4"]
    expected = [[(MToken.NUMBER, num)] for num in code]
    verify_all(code, expected)


def test_scientific_number():
    code = ["1*^3", "2 *^23", "1.23*^4"]
    expected = [[(MToken.NUMBER, num)] for num in code]
    verify_all(code, expected)


def test_patterns():
    code = [
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
    ]
    expected = [[(MToken.PATTERN, pat)] for pat in code]
    verify_all(code, expected)


def test_slots():
    code = ["#", "#1", "#234"]
    expected = [[(MToken.SLOT, st)] for st in code]
    verify_all(code, expected)


def test_slot_sequences():
    code = ["##", "##2", "##23"]
    expected = [[(MToken.SLOT, st)] for st in code]
    verify_all(code, expected)


def test_association_slots():
    code = ["#foo", '#"foo"', "#foo`bar", "#Foo$1`Bar2$"]
    expected = [[(MToken.SLOT, st)] for st in code]
    verify_all(code, expected)


def test_operators():
    code = mma.OPERATORS
    expected = [[(MToken.OPERATOR, op)] for op in code]
    verify_all(code, expected)


@pytest.mark.skip(
    "We detect Messages but are not able separate these from an ::Exception"
)
def test_messages():
    code = ["General::foo", "Foo::bar", "Foo`Bar::baz"]
    expected = [
        [
            (MToken.BUILTIN, "General"),
            (MToken.OPERATOR, "::"),
            (MToken.MESSAGE, "foo"),
        ],
        [(MToken.SYMBOL, "Foo"), (MToken.OPERATOR, "::"), (MToken.MESSAGE, "bar")],
        [
            (MToken.SYMBOL, "Foo`Bar"),
            (MToken.OPERATOR, "::"),
            (MToken.MESSAGE, "baz"),
        ],
    ]
    verify_all(code, expected)


def test_symbols():
    code = [
        "foo",
        "Foo",
        "camelCase",
        "Context`symbol",
        "`symbol",
        "$foo`bar",
        "$Bar`Baz`Qux",
    ]
    expected = [[(MToken.SYMBOL, sym)] for sym in code]
    verify_all(code, expected)


def test_get():
    code = ["<<Foo`", "<<Foo`Bar`"]
    expected = [
        [
            (MToken.OPERATOR, "<<"),
            (MToken.SYMBOL, "Foo`"),
        ],
        [
            (MToken.OPERATOR, "<<"),
            (MToken.SYMBOL, "Foo`Bar`"),
        ],
    ]
    verify_all(code, expected)


def test_builtins():
    code = list(mma.SYSTEM_SYMBOLS)
    expected = [[(MToken.BUILTIN, sym)] for sym in code]
    verify_all(code, expected)


def test_unicode_builtins():
    code = list(mma.UNICODE_SYSTEM_SYMBOLS)
    expected = [[(MToken.BUILTIN, sym)] for sym in code]
    verify_all(code, expected)


def test_unicode_groupings():
    code = list(mma.UNICODE_GROUPINGS)
    expected = [[(MToken.GROUP, grp)] for grp in code]
    verify_all(code, expected)


def test_unicode_operators():
    code = list(mma.UNICODE_OPERATORS)
    expected = [[(MToken.OPERATOR, op)] for op in code]
    verify_all(code, expected)


def test_unicode_undefined():
    code = list(mma.UNICODE_SYSTEM_UNDEFINED_SYMBOLS)
    expected = [[(MToken.SYMBOL, sym)] for sym in code]
    verify_all(code, expected)


def test_lexical_scope_simple():
    code = [
        "Block[{x = 1}, Sin[x]]",
        "Module[{y := Cos[x]}, x + y]",
        "With[{$foo = 1}, f[$foo]]",
    ]
    expected = [
        [
            (MToken.BUILTIN, "Block"),
            (MToken.GROUP, "["),
            (MToken.GROUP, "{"),
            (MToken.LOCAL_SCOPE, "x"),
            (MToken.WHITESPACE, " "),
            (MToken.OPERATOR, "="),
            (MToken.WHITESPACE, " "),
            (MToken.NUMBER, "1"),
            (MToken.GROUP, "}"),
            (MToken.GROUP, ","),
            (MToken.WHITESPACE, " "),
            (MToken.BUILTIN, "Sin"),
            (MToken.GROUP, "["),
            (MToken.LOCAL_SCOPE, "x"),
            (MToken.GROUP, "]"),
            (MToken.GROUP, "]"),
        ],
        [
            (MToken.BUILTIN, "Module"),
            (MToken.GROUP, "["),
            (MToken.GROUP, "{"),
            (MToken.LOCAL_SCOPE, "y"),
            (MToken.WHITESPACE, " "),
            (MToken.OPERATOR, ":="),
            (MToken.WHITESPACE, " "),
            (MToken.BUILTIN, "Cos"),
            (MToken.GROUP, "["),
            (MToken.SYMBOL, "x"),
            (MToken.GROUP, "]"),
            (MToken.GROUP, "}"),
            (MToken.GROUP, ","),
            (MToken.WHITESPACE, " "),
            (MToken.SYMBOL, "x"),
            (MToken.WHITESPACE, " "),
            (MToken.OPERATOR, "+"),
            (MToken.WHITESPACE, " "),
            (MToken.LOCAL_SCOPE, "y"),
            (MToken.GROUP, "]"),
        ],
        [
            (MToken.BUILTIN, "With"),
            (MToken.GROUP, "["),
            (MToken.GROUP, "{"),
            (MToken.LOCAL_SCOPE, "$foo"),
            (MToken.WHITESPACE, " "),
            (MToken.OPERATOR, "="),
            (MToken.WHITESPACE, " "),
            (MToken.NUMBER, "1"),
            (MToken.GROUP, "}"),
            (MToken.GROUP, ","),
            (MToken.WHITESPACE, " "),
            (MToken.SYMBOL, "f"),
            (MToken.GROUP, "["),
            (MToken.LOCAL_SCOPE, "$foo"),
            (MToken.GROUP, "]"),
            (MToken.GROUP, "]"),
        ],
    ]
    verify_all(code, expected)


def test_lexical_scope_nested():
    code = "Block[{Plus = Times}, x + With[{y = 1}, 3 * y]]"
    expected = [
        (MToken.BUILTIN, "Block"),
        (MToken.GROUP, "["),
        (MToken.GROUP, "{"),
        (MToken.LOCAL_SCOPE, "Plus"),
        (MToken.WHITESPACE, " "),
        (MToken.OPERATOR, "="),
        (MToken.WHITESPACE, " "),
        (MToken.BUILTIN, "Times"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, ","),
        (MToken.WHITESPACE, " "),
        (MToken.SYMBOL, "x"),
        (MToken.WHITESPACE, " "),
        (MToken.OPERATOR, "+"),
        (MToken.WHITESPACE, " "),
        (MToken.BUILTIN, "With"),
        (MToken.GROUP, "["),
        (MToken.GROUP, "{"),
        (MToken.LOCAL_SCOPE, "y"),
        (MToken.WHITESPACE, " "),
        (MToken.OPERATOR, "="),
        (MToken.WHITESPACE, " "),
        (MToken.NUMBER, "1"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, ","),
        (MToken.WHITESPACE, " "),
        (MToken.NUMBER, "3"),
        (MToken.WHITESPACE, " "),
        (MToken.OPERATOR, "*"),
        (MToken.WHITESPACE, " "),
        (MToken.LOCAL_SCOPE, "y"),
        (MToken.GROUP, "]"),
        (MToken.GROUP, "]"),
    ]
    verify(code, expected)


def test_lexical_scope_nasty():
    code = "Block[{x=Module[{y=<|a->1,b->2|>},y],z=With[{k={1,2}},k*3]}, x+y*Block[{k=3},f[k]]]"
    expected = [
        (MToken.BUILTIN, "Block"),
        (MToken.GROUP, "["),
        (MToken.GROUP, "{"),
        (MToken.LOCAL_SCOPE, "x"),
        (MToken.OPERATOR, "="),
        (MToken.BUILTIN, "Module"),
        (MToken.GROUP, "["),
        (MToken.GROUP, "{"),
        (MToken.LOCAL_SCOPE, "y"),
        (MToken.OPERATOR, "="),
        (MToken.GROUP, "<|"),
        (MToken.SYMBOL, "a"),
        (MToken.OPERATOR, "->"),
        (MToken.NUMBER, "1"),
        (MToken.GROUP, ","),
        (MToken.SYMBOL, "b"),
        (MToken.OPERATOR, "->"),
        (MToken.NUMBER, "2"),
        (MToken.GROUP, "|>"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, ","),
        (MToken.LOCAL_SCOPE, "y"),
        (MToken.GROUP, "]"),
        (MToken.GROUP, ","),
        (MToken.LOCAL_SCOPE, "z"),
        (MToken.OPERATOR, "="),
        (MToken.BUILTIN, "With"),
        (MToken.GROUP, "["),
        (MToken.GROUP, "{"),
        (MToken.LOCAL_SCOPE, "k"),
        (MToken.OPERATOR, "="),
        (MToken.GROUP, "{"),
        (MToken.NUMBER, "1"),
        (MToken.GROUP, ","),
        (MToken.NUMBER, "2"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, ","),
        (MToken.LOCAL_SCOPE, "k"),
        (MToken.OPERATOR, "*"),
        (MToken.NUMBER, "3"),
        (MToken.GROUP, "]"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, ","),
        (MToken.WHITESPACE, " "),
        (MToken.LOCAL_SCOPE, "x"),
        (MToken.OPERATOR, "+"),
        (MToken.SYMBOL, "y"),
        (MToken.OPERATOR, "*"),
        (MToken.BUILTIN, "Block"),
        (MToken.GROUP, "["),
        (MToken.GROUP, "{"),
        (MToken.LOCAL_SCOPE, "k"),
        (MToken.OPERATOR, "="),
        (MToken.NUMBER, "3"),
        (MToken.GROUP, "}"),
        (MToken.GROUP, ","),
        (MToken.SYMBOL, "f"),
        (MToken.GROUP, "["),
        (MToken.LOCAL_SCOPE, "k"),
        (MToken.GROUP, "]"),
        (MToken.GROUP, "]"),
        (MToken.GROUP, "]"),
    ]
    verify(code, expected)
