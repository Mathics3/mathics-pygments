GIT2CL ?= admin-tools/git2cl
PYTHON ?= python3
PIP ?= pip3
RM  ?= rm
SASS ?= sass

.PHONY: all build \
   check clean \
   develop dist \
   rmChangeLog \
   test

#: Default target - same as "develop"
all: develop

#: Set up to run from the source tree
develop:
	$(PIP) install -e .

mma.css: mma.scss
	$(SASS) $< $@

test check: pytest

#: Remove derived files
clean:
	@find . -name *.pyc -type f -delete

#: Install this beauty
install:
	$(PYTHON) ./setup.py install

distclean: clean
	@rm mma.css || true

#: Run py.test tests. Use environment variable "o" for pytest options
pytest:
	py.test tests $o
