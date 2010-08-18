#!/bin/sh

# Dieses kleine Scriptlein prüft für alle Dateien unter ./layouts/ die
# Gesamtstrafpunktzahl des beinhalteten Layouts und listet deren Namen
# sortiert auf.
# Es ist nicht Fehlertolerant, läuft nur unter unixartigen Systemen und
# produziert eine nur begrenzt aussagefähige Rangfolge.

# Optionen:
#   -v   für verbose
#   -t   zum testen auf fehlende Buchstaben

# Da die Bewertungsfunktion für die Optimierung von Neo 3 geschrieben
# wurde, kann sie nur in Grenzen zum Vergleich anderer Layouts
# verwendet werden. Eine entsprechende Erweiterung nützt der
# Entwicklung von Neo 3 nicht und wird deshalb wahrscheinlich nie
# erfolgen.

if test "$1" = "-t"; then
	c="a b c d e f g h i j k l m n o p q r s t u v w x y z ä ö ü ß , \."
	for a in layouts/* ; do
		for b in $c ; do
			if test -z "$(grep "$b" "$a")"; then
				echo "$a: ‚$b‘ fehlt"
			fi
		done
	done
else
	tmp=$(tempfile)
	if test "$1" = "-v"; then
		for a in layouts/* ; do
			echo "${a##*/}:" | tee -a "$tmp"
			./check_neo.py -v --check-string "`cat "$a"`" | tee -a "$tmp"
		done
		echo
	else
		for a in layouts/* ; do
			echo "${a##*/}:" >> "$tmp"
			./check_neo.py -v --check-string "`cat "$a"`" >> "$tmp"
		done
	fi

	echo "Rangfolge nach Gesamtpunkten:\n"

	sed 's/:$// ; t a ; s/^# // ; t b; d ; :b s/billion total penalty compared to notime-noeffort// ; t c; d; :c G; s/\n//; p; d; :a h; d' "$tmp" | sort

	echo "¹äöüß nicht bewertet
²ß nicht bewertet?
³ä wegen M4L nicht bewertet
⁴. wegen M4L nicht bewertet"

	rm "$tmp"
fi
