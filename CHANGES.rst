CHANGES
=======

1.0.4
-----

This is a Transitional release.

Although there is a dependency on mathics-scanner, we don't use it since tables have changed. There is some code for reading the YAML takes from the project though. With a newer and better mathics-scanner, we should be able to revise this code, use the tokenizer from mathics-scanner, and simplify things greatly.

1.0.3
-----

Modernize:

* update Python style (black),
* import order (isort),
* convert test to pytest,
* fix spelling errors, and
* add code of conduct.

1.0.2
-----

Reorder list of REs tried so that Symbols re comes before Identifier
regular expression.

This corrects symbol detection and "<<" or ``Get[]`` detection.

(There are still two classes lexer tests that need to be addressed to
be on par with pygments-mathematica).


1.0.1
-----

* Fix RE's that I had messed up in initial port for Slots, Patterns and Named Characters
* Make ujson optional. This makes this runnable from pyston 2.2

Note: There are still a few tests from pygments-mathematica that fail.

1.0.0
-----

First public release. Is largely the same thing as
pygments-mathematica, but we are geared for CLI use in mathicsscript and
we get operator information from Mathics Scanner.

For uses outside of terminal use, pygments-mathematica is probably better.
But over time I expect this will change since we will draw more power from
Mathics Scanner.
