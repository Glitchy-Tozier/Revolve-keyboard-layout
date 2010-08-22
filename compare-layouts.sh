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

arg0='-t'
arg1="$1"
arg2="$2"
arg3="$3"
verbose=""
oldvalues=""

while test -n "$arg0"; do
	if test "$arg0" = "-h"; then
		echo "Usage:"
		echo " -h   display Help and exit"
		echo " -m   test layouts for missing characters"
		echo " -t   sorting-key is total penalty (default)"
		echo " -k   sorting-key is keyposition"
		echo " -f   sorting-key is fingerrepeats"
		echo " -o   use old values instead of computing new ones"
		echo " -v   verbose"
		sort=''
		arg1=''
	elif test "$arg0" = "-m"; then
		sort=''
		arg1=''
		c="a b c d e f g h i j k l m n o p q r s t u v w x y z ä ö ü ß , \."
		for a in layouts/* ; do
			missing=''
			for b in $c ; do
				if test -z "$(head -3 "$a" | grep "$b")"; then
					missing="$missing ${b#\\}"
				fi
			done
			if test -n "$missing"; then
				echo "$a:$missing missing"
			fi
		done
	elif test "$arg0" = "-t"; then
		sort='yes'
		kriterium="total penalty"
		suchzeile="billion total penalty compared to notime-noeffort"
	elif test "$arg0" = "-k"; then
		sort='yes'
		kriterium="keyposition"
		suchzeile="mean key position cost in file 1gramme.txt ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-f"; then
		sort='yes'
		kriterium="fingerrepeats"
		suchzeile="finger repeats in file 2gramme.txt ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-v"; then
		verbose="yes"
	# zu faul, um weitere einzufügen, ich bin
	elif test "$arg0" = "-o"; then
		oldvalues="yes"
	else
		echo "unknown option: ‘$arg0’"
		arg1="-h"
	fi
	arg0="$arg1"
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

	sed "$suchzeile" "$tmp" | sort -g

	echo "¹äöüß not counted
²ß not counted
³ä not counted because of M4L
⁴. not counted because of M4L"

	rm "$tmp"
fi
