#!/bin/sh

# Dieses kleine Scriptlein prüft für alle Dateien unter ./layouts/ die
# Gesamtstrafpunktzahl des beinhalteten Layouts und listet deren Namen
# sortiert auf.
# Es ist nicht Fehlertolerant, läuft nur unter unixartigen Systemen und
# produziert eine nur begrenzt aussagefähige Rangfolge.

# Da die Bewertungsfunktion für die Optimierung von Neo 3 geschrieben
# wurde, kann sie nur in Grenzen zum Vergleich anderer Layouts
# verwendet werden. Eine entsprechende Erweiterung nützt der
# Entwicklung von Neo 3 nicht und wird deshalb wahrscheinlich nie
# erfolgen.

arg1="$1"
arg2="$2"
arg3="$3"
sort="yes"
verbose=""
oldvalues=""
kriterium="total penalty"
suchzeile="billion total penalty compared to notime-noeffort"

while test -n "$arg1"; do
	if test "$arg1" = "-h"; then
		sort=''
		arg2=''
		echo "Usage:"
		echo " -h   display Help and exit"
		echo " -t   test layouts for missing characters"
		echo " -v   verbose"
		echo " -o   use old values instead of computing new ones"
		echo " -k   sorting-key is keyposition"
		echo " -f   sorting-key is fingerrepeats"
	elif test "$arg1" = "-t"; then
		sort=''
		arg2=''
		c="a b c d e f g h i j k l m n o p q r s t u v w x y z ä ö ü ß , \."
		for a in layouts/* ; do
			for b in $c ; do
				if test -z "$(grep "$b" "$a")"; then
					echo "$a: ‚$b‘ fehlt"
				fi
			done
		done
	elif test "$arg1" = "-v"; then
		verbose="yes"
	elif test "$arg1" = "-k"; then
		kriterium="keyposition"
		suchzeile="mean key position cost in file 1gramme.txt ( [0-9]*.[0-9]* )"
	elif test "$arg1" = "-f"; then
		kriterium="fingerrepeats"
		suchzeile="finger repeats in file 2gramme.txt ( [0-9]*.[0-9]* )"
	# zu faul, um weitere einzufügen, ich bin
	elif test "$arg1" = "-o"; then
		oldvalues="yes"
	else
		echo "Unknown Option: ‘$arg1’"
		arg2="-h"
	fi
	arg1="$arg2"
	arg2="$arg3"
	arg3=""
done

if test -n "$sort"; then
	tmp=$(tempfile)
	for a in layouts/* ; do
		if test -n "$oldvalues"; then
			ergebnis="$(cat "$a")"
		else
			ergebnis="$(./check_neo.py -v --check-string "`cat "$a"`")"
			if ! test "$ergebnis" = "$(cat "$a")"; then
				echo "$ergebnis" > "$a"
			fi
		fi
		echo "${a##*/}:" >> "$tmp"
		echo "$ergebnis" >> "$tmp"
		if test -n "$verbose"; then
			echo "${a##*/}:"
			echo "$ergebnis"
		fi
	done

	echo "Ranking of $kriterium:\n"
	
	suchzeile="s/:$// ; t a ; s/^# // ; t b; d ; :b s/$suchzeile// ; t c; d; :c G; s/\\n//; p; d; :a h; d"

	sed "$suchzeile" "$tmp" | sort

	echo "¹äöüß not counted
²ß not counted
³ä not counted because of M4L
⁴. not counted because of M4L"

	rm "$tmp"
fi
