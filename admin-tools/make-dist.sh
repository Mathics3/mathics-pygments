#!/bin/bash
PACKAGE=mathics-pygments
package=mathics_pygments

# FIXME put some of the below in a common routine
function finish {
  cd $mathics_pygments_owd
}

cd $(dirname ${BASH_SOURCE[0]})
mathics_pygments_owd=$(pwd)
trap finish EXIT

if ! source ./pyenv-versions ; then
    exit $?
fi


cd ..
source mathics_pygments/version.py
echo $__version__

for pyversion in $PYVERSIONS; do
    if ! pyenv local $pyversion ; then
	exit $?
    fi
    rm -fr build
    python setup.py bdist_egg
done
python setup.py bdist_wheel --universal
mv -v dist/${package}-${__version__}-{py2.,}py3-none-any.whl
python ./setup.py sdist
finish
