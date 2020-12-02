#!/bin/bash

# create secure, easy to type passwords

cd $(dirname $(realpath $0))

function securepassword () {
	if [ x"$1" == x"" ]; then
		nletters=8
	else
		nletters="$1"
	fi
	python2 <<EOF
from random import choice
letters = "0123456789ABCDEFGHJKLMNPQRSTUVWXabcdefghijkmnopqrstuvwx"
delimiters = ",.+-*/!"
pw = ""
for i in range($nletters):
    if i%4 == 0 and i != 0 and i != $nletters:
        pw += choice(delimiters)
    pw += choice(letters)
print pw
EOF
}

TMPDIR=$(mktemp -d /run/user/1000/securepassword-XXXXX)

if [ x"${TMPDIR}" == x"" ]; then
    echo cannot create TMPDIR >&2
    exit 1
fi

for i in {1..10}; do securepassword "$1" >> ${TMPDIR}/pws.txt; done

for i in $(cat ${TMPDIR}/pws.txt); do
    echo "$i" > ${TMPDIR}/pwtest.txt
    Q=$(./check_neo.py --check=QWERTZ_LAYOUT  -f ${TMPDIR}/pwtest.txt | grep x100 | cut -d " " -f 2)
    N=$(./check_neo.py --check=NEO_LAYOUT  -f ${TMPDIR}/pwtest.txt | grep x100 | cut -d " " -f 2)
    D=$(./check_neo.py --check=DVORAK_LAYOUT  -f ${TMPDIR}/pwtest.txt | grep x100 | cut -d " " -f 2)
    C=$(./check_neo.py --check=CRY_LAYOUT  -f ${TMPDIR}/pwtest.txt | grep x100 | cut -d " " -f 2)
    S=$(guile -c "(import (ice-9 format))(format #t \"~15,2,,,'0f\" (* $Q $N $D $C))")
    echo $S $Q $N $D $C "$i"
done > ${TMPDIR}/pws-checked-qwertz-neo-dvorak-cry.tmp

cat ${TMPDIR}/pws-checked-qwertz-neo-dvorak-cry.tmp | sort -V > ${TMPDIR}/pws-checked-qwertz-neo-dvorak-cry.txt

echo your passwords are in ${TMPDIR}/pws-checked-qwertz-neo-dvorak-cry.txt

echo when you are finished, delete ${TMPDIR} >&2
