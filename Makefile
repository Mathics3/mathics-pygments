GIT2CL ?= admin-tools/git2cl
PYTHON ?= python3
PIP ?= pip3
RM  ?= rm

.PHONY: all build \
   check clean \
   develop dist \
   rmChangeLog \
   test

#: Default target - same as "develop"
all: develop


test check: pytest

#: Remove derived files
clean:
	@find . -name *.pyc -type f -delete

#: Run py.test tests. Use environment variable "o" for pytest options
pytest:
	py.test tests $o
