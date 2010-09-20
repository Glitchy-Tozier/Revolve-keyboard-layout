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

arg0='-p'
arg1="$1"
arg2="$2"
arg3="$3"
verbose=""
oldvalues=""

while test -n "$arg0"; do
	if test "$arg0" = "-h"; then
		echo "Usage:"
		echo " -h   display Help and exit"
		echo " -m   test layouts for missing characters" # don't rely on this
		echo " -p   sort by tot. penalty per letter (default)"
		echo " -t   sort by total penalty"
		echo " -k   sort by key position cost"
		echo " -f   sort by fingerrepeats in 2-gramme"
		echo " -d   sort by disbalance of fingers"
		echo " -r   sort by finger repeats between top and bottom"
		echo " -3   sort by trigrams without handswitching"
		echo " -j   sort by row jumps (rows²/dist)²"
		echo " -i   sort by hand disbalance"
		echo " -s   sort by badly positioned shortcut keys"
		echo " -u   sort by no handswitching after unbalancing"
		echo " -a   sort by movement pattern"
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
	elif test "$arg0" = "-p"; then
		sort='yes'
		kriterium="tot. penalty per letter"
		suchzeile="x100 total penalty per letter"
	elif test "$arg0" = "-t"; then
		sort='yes'
		kriterium="total penalty"
		suchzeile="x10 billion total penalty compared to notime-noeffort"
	elif test "$arg0" = "-k"; then
		sort='yes'
		kriterium="keyposition"
		suchzeile="mean key position cost in file 1gramme.txt ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-f"; then
		sort='yes'
		kriterium="fingerrepeats"
		suchzeile="% finger repeats in file 2gramme.txt ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-d"; then
		sort='yes'
		kriterium="disbalance of fingers"
		suchzeile="million keystrokes disbalance of the fingers ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-r"; then
		sort='yes'
		kriterium="finger repeats between top and bottom"
		suchzeile="% finger repeats top to bottom or vice versa ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-3"; then
		sort='yes'
		kriterium="trigrams without handswitching"
		suchzeile="% of trigrams have no handswitching (after direction change counted x 1 ) ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-j"; then
		sort='yes'
		kriterium="row jumps (rows²/dist)²"
		suchzeile="billion (rows²\/dist)² to cross ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-i"; then
		sort='yes'
		kriterium="hand disbalance"
		suchzeile="hand disbalance. Left: [0-9]*.[0-9]* %, Right: [0-9]*.[0-9]* % ( [0-9]*.[0-9]* )"
	elif test "$arg0" = "-s"; then
		sort='yes'
		kriterium="badly positioned shortcut keys"
		suchzeile="badly positioned shortcut keys (weighted)."
	elif test "$arg0" = "-u"; then
		sort='yes'
		kriterium="no handswitching after unbalancing"
		suchzeile="no handswitching after unbalancing key (weighted)."
	elif test "$arg0" = "-a"; then
		sort='yes'
		kriterium="movement pattern"
		suchzeile="movement pattern cost (weighted)."
	elif test "$arg0" = "-v"; then
		verbose="yes"
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
	
	echo "¹äöüß missing
²ß missing
³ä missing because of M4L
⁴. missing because of M4L
missing letters are getting overall penalty" # dont blame me for my english ;-)

	rm "$tmp"
fi
