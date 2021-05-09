#!/bin/bash
bs=${BASH_SOURCE[0]}
mydir=$(dirname $bs)

mathics-generate-json-table --field=ascii-operators --field=unicode-operators -o $mydir/../mathics_pygments/data/mma-tables.json
