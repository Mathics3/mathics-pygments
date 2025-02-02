GIT2CL ?= admin-tools/git2cl
PYTHON ?= python3
PIP ?= pip3
RM  ?= rm
SHELL ?= bash
SASS ?= sass

.PHONY: \
   all \
   build \
   check \
   clean \
   develop \
   dist \
   install \
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

#: Build distribution
dist: admin-tools/make-dist.sh
	$(SHELL) admin-tools/make-dist.sh

distclean: clean
	@rm mma.css || true

#: Install this beauty
install:
	$(PYTHON) ./setup.py install

#: Run py.test tests. Use environment variable "o" for pytest options
pytest:
	$(PYTHON) -m pytest tests $o


#: Remove ChangeLog
rmChangeLog:
	$(RM) ChangeLog || true

#: Create a ChangeLog from git via git log and git2cl
ChangeLog: rmChangeLog
	git log --pretty --numstat --summary | $(GIT2CL) >$@
	patch ChangeLog < ChangeLog-spell-corrected.diff
