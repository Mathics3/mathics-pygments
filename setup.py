# -*- coding: utf-8 -*-
# Copyright (c) 2021 Rocky Bernstein
# Copyright (c) 2016 rsmenon
# Licensed under the MIT License (https://opensource.org/licenses/MIT)

u"""This is a lexer and highlighter for Mathematica/Wolfram Language source code \
using the pygments engine.

It currently supports:

 - All builtin functions in the ``System`` context including unicode symbols except \
 those that use characters from the private unicode space (e.g. ``\[FormalA]``).
 - User defined symbols, including those in a context.
 - All operators including unicode operators like \u03C0.
 - Comments, including multi line and nested.
 - Strings, including multi line and escaped quotes.
 - Patterns, slots (including named slots ``#name`` introduced in version 10) and slot sequences.
 - Message names (e.g. the ivar in ``General::ivar``)
 - Numbers including base notation (e.g. ``8 ^^ 23 == 19``) and scientific notation \
 (e.g. ``1 *^ 3 == 1000``).
 - Local variables in ``Block``, ``With`` and ``Module``.

A Sass file containing the styles can be obtained from the package repository for use in static \
website generators such as Jekyll, Octopress, Pelican, etc.

Copyright 2021 Rocky Bernstein
(C) 2016 rsmenon
"""

from setuptools import setup
import sys

# Ensure user has the correct Python version
if sys.version_info < (3, 6):
    print("mathicsscript does not support Python %d.%d" % sys.version_info[:2])
    sys.exit(-1)


import os.path as osp


def get_srcdir():
    filename = osp.normcase(osp.dirname(osp.abspath(__file__)))
    return osp.realpath(filename)


def read(*rnames):
    return open(osp.join(get_srcdir(), *rnames)).read()


# stores __version__ in the current namespace
exec(
    compile(read("mathics_pygments/version.py"), "mathics_pygments/version.py", "exec")
)

setup(
    name="mathics_pygments",
    version=__version__,  # noqa
    description="Mathematica/Wolfram Language Lexer for Pygments",
    long_description=__doc__,
    long_description_content_type="text/x-rst",
    author="Rocky Bernstein",
    author_email="rb@dustyfeet.com",
    license="MIT",
    keywords="syntax highlighting mathematica",
    url="http://github.com/Mathics3/mathics-pygments/",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Processing",
        "Topic :: Utilities",
    ],
    packages=["mathics_pygments"],
    package_data={
        "mathics_pygments": [
            "data/mma-tables.json",
        ],
    },
    install_requires=["Pygments >= 2", "Mathics_Scanner>=1.2.0"],
    include_package_data=False,
    platforms=["any"],
    entry_points={
        "pygments.lexers": ["MathematicaLexer = mathics_pygments:MathematicaLexer"],
        "pygments.styles": [
            "mathematica = mathics_pygments:MathematicaStyle",
            "mathematicanotebook = mathics_pygments:MathematicaNotebookStyle",
        ],
    },
    zip_safe=False,
)
