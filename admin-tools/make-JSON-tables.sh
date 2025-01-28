#!/bin/bash
bs=${BASH_SOURCE[0]}
json_tables_owd=$(pwd)
mydir=$(dirname $bs)
cd $mydir
python ../mathics_pygments/generate/build_pygments_tables.py -o $mydir/../mathics_pygments/data/mma-tables-new.json
cd $json_tables_owd
