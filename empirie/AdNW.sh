#!/bin/ksh

# Installation: Ausführbar machen (chmod 755 AdNW.sh), gegebenenfalls
# Pfad zur Shell anpassen (bash tut es wahrscheinlich auch).

# $Id: AdNW.sh,v 1.21 2011/06/26 16:11:32 andreas Exp $

hilfe () {
    cat <<EOF
Aufruf: AdNW.sh [-a name] [-b ziffern] [-bd] [-c name] [-cax] [-cua] ] [-h]
                [+kpd] [-m1] [+m4] [-n] [-p] [-qca] [-s] [+std] [-szd]
                [-t name] [-xcv] [±xf86] [-z name] [-zj]

Schreibt die Tastaturbelegung «Aus der Neo-Welt» (und optional ein
modifiziertes schweizerdeutsches, deutsches und amerikanisches Layout) auf die
Standardausgabe.  Die Tastaturbelegung ergibt sich aus der aktuellen Belegung,
die selektiv geändert und ergänzt wird.  Die aktuelle Belegung wird vom
X-Server erfragt.  Dieser ist durch den Wert der Variablen DISPLAY gegeben,
oder :0 falls diese Variable keinen Wert enthält.

Typischerweise erzeugt man einmal ein .xkb-File:

  ./AdNW.sh > belegung.xkb

und legt damit (z.B. in .xinitrc) die Belegung fest:

  xkbcomp belegung.xkb :0

Optionen:

-a     Lies Ausgangsbelegung vom angegebenen .xkb-File statt sie vom Server zu
       holen.

-b     Jede der maximal vier Ziffern steht für ein Layout: 1 = Aus der
       Neo-Welt, 2 = kyrillisch, 3 = griechisch, 4 = US, 5 = CH, 6 = DE.  Die
       Reihenfolge der Ziffern bestimmt als welche Gruppe ein Layout auftritt.
       Voreinstellung: 1, also nur Aus der Neo-Welt.

-bd    Implementiere die Buchstaben per Redirect.

-c     Lies zusätzliche xkb_compatibility-Definitionen vom angegebenen File.

+cax   Verwende für Ctrl/Alt spezielle Ebenen.

-cua   Unterdrücke Cut/Copy/Paste auf Mod4+ linke Ctrl/Win/Alt.

-h     Gib diese Hilfe aus und beende das Programm.

+kpd   Implementiere Ebene4-Zahlenblock direkt statt per Redirect.

+m1    Tastaturmaus auf Ebene 1 des Zifferblocks.

+m4    Tastaturmaus auf Ebene 4 des Zifferblocks.

-n     Erzeuge eine Notbelegung für den Fall, dass die normale Belegung nicht
       funktioniert.  Ebene 4 ist mit Overlays und die Ebenen 3/5 mit
       Gruppenumschaltung implementiert.  Das Ebene-4-Lock ist nur über
       Shift-Mod3-Tab einzuschalten, es ist nur ein Layout erlaubt, für viele
       Tasten muss zum Erreichen von Ebene 6 Mod3 vor Mod4 gedrückt werden.

-p     Vertausche Punkt und Komma auf den Ziffernblöcken.

+qca   Behalte Ctrl/Alt-Ebene der QWERTZ-Positionen von A-Z, Ä, Ö, Ü, Punkt,
       Komma und Bindestrich wie QWERTZ bei.

-s     Schreibe ein Script.  Normalerweise wird ein xkb-File geschrieben.

+std   Implementiere die wichtigsten Steuerzeichen auf Ebene 4 direkt (nicht
       per Redirect).

-szd   Implementiere die wichtigsten ASCII-Zeichen auf Ebene 3, Punkt, Komma
       und die Ziffern per Redirect.

-t     Lies zusätzliche xkb_types-Definitionen vom angegebenen File.

+xcv   Lass Ctrl/Alt+XYCV an ihren QWERTZ-Plätzen

-xf86  Ersetze XFree86/Xorg-spezifische keysyms durch 'NoSymbol'
+xf86  Gebe XFree86/Xorg-spezifische keysyms unverändert aus.  Die
       Voreinstellung ist systemabhängig.

-z     Lies zusätzliche Belegungsinformation vom angegebenen File.  Diese
       ergänzen oder ersetzen die in diesem Skript eingebauten Belegungen.
       Diese Option kann mehrfach angegeben werden; spätere Definitionen
       überschreiben frühere.

-zj    Vertausche bei «Aus der Neo-Welt» die Position von z und j.


Änderungen bei «Aus der Neo-Welt» gegenüber Neo 2 (ausser Buchstabentasten auf
Ebene 1, 2, 5, 6):

- Ebene 3 von Mod3 löst alle Locks.

- Mit Shift+ScrollLock schaltet man auf das zweite Layout, mit Mod3+ScrollLock
  auf das dritte, mit Mod4+ScrollLock auf das vierte.  Zurück zum ersten geht
  es immer mit ScrollLock.

- Mit Mod3+Mod4+ScrollLock setzt und löst man ein spezielles Lock, unter dem
  zwei neue Ebenen zur Verfügung stehen (zu erreichen ohne Modifikator
  beziehungsweise mit Shift).  Zu Ebene 1 und 2 kommt man mit Mod3 und
  Shift+Mod3.  Zu Ebene 3 und 6 kommt man mit Mod3+Mod4 und Mod4+Mod3 (die
  Reihefolge spielt eine Rolle).  Die Navigationsebene bekommt man mit Mod4
  (mit oder ohne Shift).  Die beiden Ebenen (Level7 und Level8) enthalten
  nichts Nützliches, sie stehen dem Benutzer zur Verfügung.

- Falls die Optionen -szd und -bd verwendet werden, kann man mit ScrollLock ein
  beinahe-US-Layout einstellen.  Gegenüber einem normalen US-Layout behalten
  die linke Mod3-Taste und beide Mod4-Tasten und der Zahlenblock ihre Belegung,
  und NumLock wird eine Mod3-Taste.

- Die Tastaturmaus (auf Ebene 1 oder 4) belegt die Tasten KP_5, KP/, KP*, KP-
  und KP+ mit Einfachklicks der Maustasten 1-5.  Diese Aktionen funktionieren
  auch in Verbindung mit Shift. KP0 und KP-Komma halten und lösen Maustaste 1
  bzw 3.

- Cut, Copy und Paste kann man bei CUA-konformen Programmen wie folgt eingeben:
  Cut   als Mod4+Linke Control-Taste
  Copy  als Mod4+Linke Windows-Taste
  Paste als Mod4+Linke Alt-Taste

- Auf Ebene 4 von 4 liegt die keysym Begin, auf Ebene 3 der Strichtaste das
  echte Minus, auf Ebene 4 vor f liegt e, auf der Pseudoebene von T3 liegt die
  keysym Codeinput.

EOF
    exit 0
}

verbinde_types () {
    typeset f1 f2

    while read f1 f2; do
	[[ $f1 = xkb_types ]] && break
    done
    echo "$f1 $f2"

    while read f1 f2; do
	if [[ $f1 = type ]]; then
	    if [[ $f2 = \"NEO* ]]; then
		# Unsere eigenen types ausfiltern, sonst stehen sie vielleicht
		# doppelt in der Ausgabe
		while read f1; do
		    [[ $f1 = }\; ]] && break
		done
	    else
		# Normale types unverändert passieren lassen
		echo "$f1 $f2"
		while read f1; do
		    echo "$f1"
		    [[ $f1 = }\; ]] && break
		done
	    fi
	elif [[ $f1 = }\; ]]; then
	    break
	else
	    echo "$f1 $f2"
	fi
    done

    if [ -z "$NOTBELEGUNG" ]; then
	cat <<EOF
type "NEO_34" {
    modifiers= Lock+Mod3+Mod5;
    map[Lock          ]= Level1;
    map[     Mod3     ]= Level1;
    map[Lock+Mod3     ]= Level2;
    map[          Mod5]= Level1;
    map[Lock+     Mod5]= Level3;
    map[     Mod3+Mod5]= Level3;
    map[Lock+Mod3+Mod5]= Level4;
    level_name[Level1]= "E1";
    level_name[Level2]= "E3";
    level_name[Level3]= "E4";
    level_name[Level4]= "E6";
};
type "NEO_6" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level2;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level2;
    map[           Mod3     ]= Level1;
    map[Shift+     Mod3     ]= Level2;
    map[      Lock+Mod3     ]= Level3;
    map[Shift+Lock+Mod3     ]= Level5;
    map[                Mod5]= Level1;
    map[Shift+          Mod5]= Level2;
    map[      Lock+     Mod5]= Level4;
    map[Shift+Lock+     Mod5]= Level7;
    map[           Mod3+Mod5]= Level4;
    map[Shift+     Mod3+Mod5]= Level7;
    map[      Lock+Mod3+Mod5]= Level6;
    map[Shift+Lock+Mod3+Mod5]= Level6;
    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E4";
    level_name[Level5]= "E5";
    level_name[Level6]= "E6";
    level_name[Level7]= "Shift+E4";
};
type "NEO_TAB" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level2;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level2;
    map[           Mod3     ]= Level1;
    map[Shift+     Mod3     ]= Level2;
    map[      Lock+Mod3     ]= Level3;
    map[Shift+Lock+Mod3     ]= Level4;
    map[                Mod5]= Level1;
    map[Shift+          Mod5]= Level2;
    map[      Lock+     Mod5]= Level1;
    map[Shift+Lock+     Mod5]= Level2;
    map[           Mod3+Mod5]= Level1;
    map[Shift+     Mod3+Mod5]= Level2;
    map[      Lock+Mod3+Mod5]= Level3;
    map[Shift+Lock+Mod3+Mod5]= Level3;
    preserve[      Lock]= Lock;
    preserve[Shift+Lock]= Lock;
    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E5";
};
type "NEO_SHIFT" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level2;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level2;
    map[           Mod3     ]= Level1;
    map[Shift+     Mod3     ]= Level3;
    map[      Lock+Mod3     ]= Level1;
    map[Shift+Lock+Mod3     ]= Level3;
    map[                Mod5]= Level1;
    map[Shift+          Mod5]= Level4;
    map[      Lock+     Mod5]= Level1;
    map[Shift+Lock+     Mod5]= Level1;
    map[           Mod3+Mod5]= Level1;
    map[Shift+     Mod3+Mod5]= Level1;
    map[      Lock+Mod3+Mod5]= Level1;
    map[Shift+Lock+Mod3+Mod5]= Level1;
    level_name[Level1]= "Shift";
    level_name[Level2]= "Lock Lock";
    level_name[Level3]= "Lock Mod3+Lock";
    level_name[Level4]= "Lock Mod5+Lock";
};
type "NEO_MOD3" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level1;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level1;
    map[           Mod3     ]= Level1;
    map[Shift+     Mod3     ]= Level1;
    map[      Lock+Mod3     ]= Level2;
    map[Shift+Lock+Mod3     ]= Level1;
    map[                Mod5]= Level3;
    map[Shift+          Mod5]= Level3;
    map[      Lock+     Mod5]= Level1;
    map[Shift+Lock+     Mod5]= Level1;
    map[           Mod3+Mod5]= Level4;
    map[Shift+     Mod3+Mod5]= Level3;
    map[      Lock+Mod3+Mod5]= Level2;
    map[Shift+Lock+Mod3+Mod5]= Level1;
    level_name[Level1]= "Mod3+Lock";
    level_name[Level2]= "Unlock";
    level_name[Level3]= "Mod3";
    level_name[Level4]= "Unlock Mod5+Lock";
};
type "NEO_MOD4" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level1;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level1;
    map[           Mod3     ]= Level2;
    map[Shift+     Mod3     ]= Level2;
    map[      Lock+Mod3     ]= Level1;
    map[Shift+Lock+Mod3     ]= Level1;
    map[                Mod5]= Level1;
    map[Shift+          Mod5]= Level1;
    map[      Lock+     Mod5]= Level3;
    map[Shift+Lock+     Mod5]= Level1;
    map[           Mod3+Mod5]= Level4;
    map[Shift+     Mod3+Mod5]= Level1;
    map[      Lock+Mod3+Mod5]= Level4;
    map[Shift+Lock+Mod3+Mod5]= Level1;
    level_name[Level1]= "Mod5+Lock";
    level_name[Level2]= "Mod5";
    level_name[Level3]= "Lock Mod3";
    level_name[Level4]= "Unlock Mod3+Shift";
};
EOF
	if [ -z "$CTRLALTEXTRA" ]; then
	    cat <<EOF
type "NEO_N" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level2;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level2;
    map[           Mod3     ]= Level4;
    map[Shift+     Mod3     ]=      9;
    map[      Lock+Mod3     ]= Level3;
    map[Shift+Lock+Mod3     ]= Level5;
    map[                Mod5]= Level7;
    map[Shift+          Mod5]= Level8;
    map[      Lock+     Mod5]= Level4;
    map[Shift+Lock+     Mod5]=      9;
    map[           Mod3+Mod5]= Level1;
    map[Shift+     Mod3+Mod5]= Level2;
    map[      Lock+Mod3+Mod5]= Level6;
    map[Shift+Lock+Mod3+Mod5]= Level3;
    preserve[Shift+     Mod3     ]= Shift;
    preserve[Shift+Lock+     Mod5]= Shift;
    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E4";
    level_name[Level5]= "E5";
    level_name[Level6]= "E6";
    level_name[Level7]= "E7";
    level_name[Level8]= "E8";
    level_name[     9]= "Shift+E4";
};
type "NEO_SPACE" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level2;
    map[      Lock          ]= Level1;
    map[Shift+Lock          ]= Level2;
    map[           Mod3     ]= Level4;
    map[Shift+     Mod3     ]=      9;
    map[      Lock+Mod3     ]= Level3;
    map[Shift+Lock+Mod3     ]= Level5;
    map[                Mod5]= Level7;
    map[Shift+          Mod5]= Level8;
    map[      Lock+     Mod5]= Level4;
    map[Shift+Lock+     Mod5]=      9;
    map[           Mod3+Mod5]= Level1;
    map[Shift+     Mod3+Mod5]= Level2;
    map[      Lock+Mod3+Mod5]= Level6;
    map[Shift+Lock+Mod3+Mod5]= Level3;
    preserve[Shift               ]= Shift;
    preserve[Shift+Lock          ]= Shift;
    preserve[Shift+     Mod3     ]= Shift;
    preserve[Shift+Lock+     Mod5]= Shift;
    preserve[Shift+     Mod3+Mod5]= Shift;
    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E4";
    level_name[Level5]= "E5";
    level_name[Level6]= "E6";
    level_name[Level7]= "E7";
    level_name[Level8]= "E8";
    level_name[     9]= "Shift+E4";
};
EOF
	else
	    cat <<EOF
type "NEO_N" {
    modifiers= Shift+Lock+Control+Mod1+Mod3+Mod5;
    map[        Shift                    ]= Level2;
    map[              Lock               ]= Level1;
    map[        Shift+Lock               ]= Level2;
    map[                        Mod3     ]= Level4;
    map[        Shift+          Mod3     ]=     11;
    map[              Lock+     Mod3     ]= Level3;
    map[        Shift+Lock+     Mod3     ]= Level5;
    map[                             Mod5]= Level7;
    map[        Shift+               Mod5]= Level8;
    map[              Lock+          Mod5]= Level4;
    map[        Shift+Lock+          Mod5]=     11;
    map[                        Mod3+Mod5]= Level1;
    map[        Shift+          Mod3+Mod5]= Level2;
    map[              Lock+     Mod3+Mod5]= Level6;
    map[        Shift+Lock+     Mod3+Mod5]= Level3;
    map[Control                          ]=      9;
    map[Control+Shift                    ]=     10;
    map[Control+      Lock               ]=      9;
    map[Control+Shift+Lock               ]=     10;
    map[Control+                Mod3     ]= Level4;
    map[Control+Shift+          Mod3     ]=     11;
    map[Control+      Lock+     Mod3     ]= Level3;
    map[Control+Shift+Lock+     Mod3     ]= Level5;
    map[Control+                     Mod5]= Level7;
    map[Control+Shift+               Mod5]= Level8;
    map[Control+      Lock+          Mod5]= Level4;
    map[Control+Shift+Lock+          Mod5]=     11;
    map[Control+                Mod3+Mod5]=      9;
    map[Control+Shift+          Mod3+Mod5]=     10;
    map[Control+      Lock+     Mod3+Mod5]= Level6;
    map[Control+Shift+Lock+     Mod3+Mod5]= Level3;
    map[                   Mod1          ]=      9;
    map[        Shift+     Mod1          ]=     10;
    map[              Lock+Mod1          ]=      9;
    map[        Shift+Lock+Mod1          ]=     10;
    map[                   Mod1+Mod3     ]= Level4;
    map[        Shift+     Mod1+Mod3     ]=     11;
    map[              Lock+Mod1+Mod3     ]= Level3;
    map[        Shift+Lock+Mod1+Mod3     ]= Level5;
    map[                   Mod1+     Mod5]= Level7;
    map[        Shift+     Mod1+     Mod5]= Level8;
    map[              Lock+Mod1+     Mod5]= Level4;
    map[        Shift+Lock+Mod1+     Mod5]=     11;
    map[                   Mod1+Mod3+Mod5]=      9;
    map[        Shift+     Mod1+Mod3+Mod5]=     10;
    map[              Lock+Mod1+Mod3+Mod5]= Level6;
    map[        Shift+Lock+Mod1+Mod3+Mod5]= Level3;
    map[Control+           Mod1          ]=      9;
    map[Control+Shift+     Mod1          ]=     10;
    map[Control+      Lock+Mod1          ]=      9;
    map[Control+Shift+Lock+Mod1          ]=     10;
    map[Control+           Mod1+Mod3     ]= Level4;
    map[Control+Shift+     Mod1+Mod3     ]=     11;
    map[Control+      Lock+Mod1+Mod3     ]= Level3;
    map[Control+Shift+Lock+Mod1+Mod3     ]= Level5;
    map[Control+           Mod1+     Mod5]= Level7;
    map[Control+Shift+     Mod1+     Mod5]= Level8;
    map[Control+      Lock+Mod1+     Mod5]= Level4;
    map[Control+Shift+Lock+Mod1+     Mod5]=     11;
    map[Control+           Mod1+Mod3+Mod5]=      9;
    map[Control+Shift+     Mod1+Mod3+Mod5]=     10;
    map[Control+      Lock+Mod1+Mod3+Mod5]= Level6;
    map[Control+Shift+Lock+Mod1+Mod3+Mod5]= Level3;

    preserve[              Lock               ]= Lock;
    preserve[        Shift+Lock               ]= Lock;
    preserve[        Shift+          Mod3     ]= Shift;
    preserve[        Shift+Lock+          Mod5]= Shift;
    preserve[Control                          ]= Control;
    preserve[Control+Shift                    ]= Control;
    preserve[Control+      Lock               ]= Control;
    preserve[Control+Shift+Lock               ]= Control;
    preserve[Control+                Mod3     ]= Control;
    preserve[Control+Shift+          Mod3     ]= Control+Shift;
    preserve[Control+      Lock+     Mod3     ]= Control;
    preserve[Control+Shift+Lock+     Mod3     ]= Control;
    preserve[Control+                     Mod5]= Control;
    preserve[Control+Shift+               Mod5]= Control;
    preserve[Control+      Lock+          Mod5]= Control;
    preserve[Control+Shift+Lock+          Mod5]= Control+Shift;
    preserve[Control+                Mod3+Mod5]= Control;
    preserve[Control+Shift+          Mod3+Mod5]= Control;
    preserve[Control+      Lock+     Mod3+Mod5]= Control;
    preserve[Control+Shift+Lock+     Mod3+Mod5]= Control;
    preserve[                   Mod1          ]= Mod1;
    preserve[        Shift+     Mod1          ]= Mod1;
    preserve[              Lock+Mod1          ]= Mod1;
    preserve[        Shift+Lock+Mod1          ]= Mod1;
    preserve[                   Mod1+Mod3     ]= Mod1;
    preserve[        Shift+     Mod1+Mod3     ]= Mod1+Shift;
    preserve[              Lock+Mod1+Mod3     ]= Mod1;
    preserve[        Shift+Lock+Mod1+Mod3     ]= Mod1;
    preserve[                   Mod1+     Mod5]= Mod1;
    preserve[        Shift+     Mod1+     Mod5]= Mod1;
    preserve[              Lock+Mod1+     Mod5]= Mod1;
    preserve[        Shift+Lock+Mod1+     Mod5]= Mod1+Shift;
    preserve[                   Mod1+Mod3+Mod5]= Mod1;
    preserve[        Shift+     Mod1+Mod3+Mod5]= Mod1;
    preserve[              Lock+Mod1+Mod3+Mod5]= Mod1;
    preserve[        Shift+Lock+Mod1+Mod3+Mod5]= Mod1;
    preserve[Control+           Mod1          ]= Control+Mod1;
    preserve[Control+Shift+     Mod1          ]= Control+Mod1;
    preserve[Control+      Lock+Mod1          ]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1          ]= Control+Mod1;
    preserve[Control+           Mod1+Mod3     ]= Control+Mod1;
    preserve[Control+Shift+     Mod1+Mod3     ]= Control+Mod1+Shift;
    preserve[Control+      Lock+Mod1+Mod3     ]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1+Mod3     ]= Control+Mod1;
    preserve[Control+           Mod1+     Mod5]= Control+Mod1;
    preserve[Control+Shift+     Mod1+     Mod5]= Control+Mod1;
    preserve[Control+      Lock+Mod1+     Mod5]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1+     Mod5]= Control+Mod1+Shift;
    preserve[Control+           Mod1+Mod3+Mod5]= Control+Mod1;
    preserve[Control+Shift+     Mod1+Mod3+Mod5]= Control+Mod1;
    preserve[Control+      Lock+Mod1+Mod3+Mod5]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1+Mod3+Mod5]= Control+Mod1;

    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E4";
    level_name[Level5]= "E5";
    level_name[Level6]= "E6";
    level_name[Level7]= "E7";
    level_name[Level8]= "E8";
    level_name[     9]= "Ctrl/Meta";
    level_name[    10]= "Shift+Ctrl/Meta";
    level_name[    11]= "Shift+E4";
};
type "NEO_SPACE" {
    modifiers= Shift+Lock+Control+Mod1+Mod3+Mod5;
    map[        Shift                    ]= Level2;
    map[              Lock               ]= Level1;
    map[        Shift+Lock               ]= Level2;
    map[                        Mod3     ]= Level4;
    map[        Shift+          Mod3     ]=     11;
    map[              Lock+     Mod3     ]= Level3;
    map[        Shift+Lock+     Mod3     ]= Level5;
    map[                             Mod5]= Level7;
    map[        Shift+               Mod5]= Level8;
    map[              Lock+          Mod5]= Level4;
    map[        Shift+Lock+          Mod5]=     11;
    map[                        Mod3+Mod5]= Level1;
    map[        Shift+          Mod3+Mod5]= Level2;
    map[              Lock+     Mod3+Mod5]= Level6;
    map[        Shift+Lock+     Mod3+Mod5]= Level3;
    map[Control                          ]=      9;
    map[Control+Shift                    ]=     10;
    map[Control+      Lock               ]=      9;
    map[Control+Shift+Lock               ]=     10;
    map[Control+                Mod3     ]= Level4;
    map[Control+Shift+          Mod3     ]=     11;
    map[Control+      Lock+     Mod3     ]= Level3;
    map[Control+Shift+Lock+     Mod3     ]= Level5;
    map[Control+                     Mod5]= Level7;
    map[Control+Shift+               Mod5]= Level8;
    map[Control+      Lock+          Mod5]= Level4;
    map[Control+Shift+Lock+          Mod5]=     11;
    map[Control+                Mod3+Mod5]=      9;
    map[Control+Shift+          Mod3+Mod5]=     10;
    map[Control+      Lock+     Mod3+Mod5]= Level6;
    map[Control+Shift+Lock+     Mod3+Mod5]= Level3;
    map[                   Mod1          ]=      9;
    map[        Shift+     Mod1          ]=     10;
    map[              Lock+Mod1          ]=      9;
    map[        Shift+Lock+Mod1          ]=     10;
    map[                   Mod1+Mod3     ]= Level4;
    map[        Shift+     Mod1+Mod3     ]=     11;
    map[              Lock+Mod1+Mod3     ]= Level3;
    map[        Shift+Lock+Mod1+Mod3     ]= Level5;
    map[                   Mod1+     Mod5]= Level7;
    map[        Shift+     Mod1+     Mod5]= Level8;
    map[              Lock+Mod1+     Mod5]= Level4;
    map[        Shift+Lock+Mod1+     Mod5]=     11;
    map[                   Mod1+Mod3+Mod5]=      9;
    map[        Shift+     Mod1+Mod3+Mod5]=     10;
    map[              Lock+Mod1+Mod3+Mod5]= Level6;
    map[        Shift+Lock+Mod1+Mod3+Mod5]= Level3;
    map[Control+           Mod1          ]=      9;
    map[Control+Shift+     Mod1          ]=     10;
    map[Control+      Lock+Mod1          ]=      9;
    map[Control+Shift+Lock+Mod1          ]=     10;
    map[Control+           Mod1+Mod3     ]= Level4;
    map[Control+Shift+     Mod1+Mod3     ]=     11;
    map[Control+      Lock+Mod1+Mod3     ]= Level3;
    map[Control+Shift+Lock+Mod1+Mod3     ]= Level5;
    map[Control+           Mod1+     Mod5]= Level7;
    map[Control+Shift+     Mod1+     Mod5]= Level8;
    map[Control+      Lock+Mod1+     Mod5]= Level4;
    map[Control+Shift+Lock+Mod1+     Mod5]=     11;
    map[Control+           Mod1+Mod3+Mod5]=      9;
    map[Control+Shift+     Mod1+Mod3+Mod5]=     10;
    map[Control+      Lock+Mod1+Mod3+Mod5]= Level6;
    map[Control+Shift+Lock+Mod1+Mod3+Mod5]= Level3;

    preserve[        Shift                    ]= Shift;
    preserve[        Shift+Lock               ]= Shift;
    preserve[        Shift+          Mod3     ]= Shift;
    preserve[        Shift+Lock+          Mod5]= Shift;
    preserve[        Shift+          Mod3+Mod5]= Shift;
    preserve[Control                          ]= Control;
    preserve[Control+Shift                    ]= Control+Shift;
    preserve[Control+      Lock               ]= Control;
    preserve[Control+Shift+Lock               ]= Control+Shift;
    preserve[Control+                Mod3     ]= Control;
    preserve[Control+Shift+          Mod3     ]= Control+Shift;
    preserve[Control+      Lock+     Mod3     ]= Control;
    preserve[Control+Shift+Lock+     Mod3     ]= Control;
    preserve[Control+                     Mod5]= Control;
    preserve[Control+Shift+               Mod5]= Control;
    preserve[Control+      Lock+          Mod5]= Control;
    preserve[Control+Shift+Lock+          Mod5]= Control+Shift;
    preserve[Control+                Mod3+Mod5]= Control;
    preserve[Control+Shift+          Mod3+Mod5]= Control+Shift;
    preserve[Control+      Lock+     Mod3+Mod5]= Control;
    preserve[Control+Shift+Lock+     Mod3+Mod5]= Control;
    preserve[                   Mod1          ]= Mod1;
    preserve[        Shift+     Mod1          ]= Mod1+Shift;
    preserve[              Lock+Mod1          ]= Mod1;
    preserve[        Shift+Lock+Mod1          ]= Mod1+Shift;
    preserve[                   Mod1+Mod3     ]= Mod1;
    preserve[        Shift+     Mod1+Mod3     ]= Mod1+Shift;
    preserve[              Lock+Mod1+Mod3     ]= Mod1;
    preserve[        Shift+Lock+Mod1+Mod3     ]= Mod1;
    preserve[                   Mod1+     Mod5]= Mod1;
    preserve[        Shift+     Mod1+     Mod5]= Mod1;
    preserve[              Lock+Mod1+     Mod5]= Mod1;
    preserve[        Shift+Lock+Mod1+     Mod5]= Mod1+Shift;
    preserve[                   Mod1+Mod3+Mod5]= Mod1;
    preserve[        Shift+     Mod1+Mod3+Mod5]= Mod1+Shift;
    preserve[              Lock+Mod1+Mod3+Mod5]= Mod1;
    preserve[        Shift+Lock+Mod1+Mod3+Mod5]= Mod1;
    preserve[Control+           Mod1          ]= Control+Mod1;
    preserve[Control+Shift+     Mod1          ]= Control+Shift+Mod1;
    preserve[Control+      Lock+Mod1          ]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1          ]= Control+Shift+Mod1;
    preserve[Control+           Mod1+Mod3     ]= Control+Mod1;
    preserve[Control+Shift+     Mod1+Mod3     ]= Control+Mod1+Shift;
    preserve[Control+      Lock+Mod1+Mod3     ]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1+Mod3     ]= Control+Mod1;
    preserve[Control+           Mod1+     Mod5]= Control+Mod1;
    preserve[Control+Shift+     Mod1+     Mod5]= Control+Mod1;
    preserve[Control+      Lock+Mod1+     Mod5]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1+     Mod5]= Control+Mod1+Shift;
    preserve[Control+           Mod1+Mod3+Mod5]= Control+Mod1;
    preserve[Control+Shift+     Mod1+Mod3+Mod5]= Control+Shift+Mod1;
    preserve[Control+      Lock+Mod1+Mod3+Mod5]= Control+Mod1;
    preserve[Control+Shift+Lock+Mod1+Mod3+Mod5]= Control+Mod1;

    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E4";
    level_name[Level5]= "E5";
    level_name[Level6]= "E6";
    level_name[Level7]= "E7";
    level_name[Level8]= "E8";
    level_name[     9]= "Ctrl/Meta";
    level_name[    10]= "Shift+Ctrl/Meta";
    level_name[    11]= "Shift+E4";
};
EOF
	fi

	[ -n "$BUCHSTABENDIREKT" ] && cat<<EOF
type "NEO_A" {
    modifiers= Shift+Lock+Mod3+Mod5;
    map[Shift               ]= Level2;
    map[      Lock          ]= Level2;
    map[Shift+Lock          ]= Level1;
    map[           Mod3     ]= Level4;
    map[Shift+     Mod3     ]=      9;
    map[      Lock+Mod3     ]= Level3;
    map[Shift+Lock+Mod3     ]= Level5;
    map[                Mod5]= Level7;
    map[Shift+          Mod5]= Level8;
    map[      Lock+     Mod5]= Level4;
    map[Shift+Lock+     Mod5]=      9;
    map[           Mod3+Mod5]= Level1;
    map[Shift+     Mod3+Mod5]= Level2;
    map[      Lock+Mod3+Mod5]= Level6;
    map[Shift+Lock+Mod3+Mod5]= Level3;
    preserve[Shift+     Mod3     ]= Shift;
    preserve[Shift+Lock+     Mod5]= Shift;
    level_name[Level1]= "E1";
    level_name[Level2]= "E2";
    level_name[Level3]= "E3";
    level_name[Level4]= "E4";
    level_name[Level5]= "E5";
    level_name[Level6]= "E6";
    level_name[Level7]= "E7";
    level_name[Level8]= "E8";
    level_name[     9]= "Shift+E4";
};
EOF
    else
	# Notbelegung: Unterstützung für Caps-Lock
	cat <<EOF
type "NEO_SHIFT" {
    modifiers= Shift+Lock;
    map[Shift     ]= Level2;
    map[Shift+Lock]= Level2;

    level_name[Level1]= "Basis";
    level_name[Level2]= "Shift";
};
type "NEO_3" {
    modifiers= Shift+Lock+Mod5;
    map[Shift          ]= Level2;
    map[Shift+Lock     ]= Level2;
    map[           Mod5]= Level3;
    map[      Lock+Mod5]= Level3;

    level_name[Level1]= "E3";
    level_name[Level2]= "E5";
    level_name[Level3]= "E6";
};
EOF
    fi

    for fi in $TYPES; do
	cat "$fi"
    done

    echo '};'
}

ersetze_compat () {
    typeset f1

    while read f1; do
	[[ $f1 = xkb_compatibility* ]] && break
    done
    echo "$f1"

    cat <<EOF
virtual_modifiers Alt,Meta,Super,NumLock;
interpret.useModMapMods= AnyLevel;
interpret.locking= False;
interpret.repeat= False;
interpret Alt_L   { virtualModifier= Alt;   action= SetMods(modifiers=Alt); };
interpret Alt_R   { virtualModifier= Alt;   action= SetMods(modifiers=Alt); };
interpret Meta_L  { virtualModifier= Meta;  action= SetMods(modifiers=Meta); };
interpret Meta_R  { virtualModifier= Meta;  action= SetMods(modifiers=Meta); };
interpret Super_L { virtualModifier= Super; action= SetMods(modifiers=Super); };
interpret Super_R { virtualModifier= Super; action= SetMods(modifiers=Super); };
interpret Hyper_L              { action= SetMods(modifiers=Mod2); };
interpret Hyper_R              { action= SetMods(modifiers=Mod2); };
interpret Control_L            { action= SetMods(modifiers=Control); };
interpret Control_R            { action= SetMods(modifiers=Control); };
interpret Shift_L              { action= SetMods(modifiers=Shift); };
interpret Shift_R              { action= SetMods(modifiers=Shift); };
interpret Caps_Lock            { action= LockMods(modifiers=Lock); };
interpret Pointer_EnableKeys   { action= LockControls(controls=MouseKeys); };
interpret Terminate_Server     { action= Terminate(); };
EOF

    if [ -z "$NOTBELEGUNG" ]; then
	cat <<EOF
interpret Num_Lock+Mod3 { virtualModifier= NumLock; action= LockMods(modifiers=NumLock); };
interpret Num_Lock             { action= LockMods(modifiers=Mod3); };
interpret ISO_Group_Shift      { action= SetMods(modifiers=Lock+Mod3); };
interpret ISO_Last_Group       { action= SetMods(modifiers=Lock+Mod3); };
interpret ISO_Level3_Lock      { action= LockMods(modifiers=Lock+Mod3); };
interpret ISO_Level3_Shift     { action= SetMods(modifiers=Lock+Mod5); };
interpret ISO_First_Group      { action= SetMods(modifiers=Lock+Mod5); };
interpret ISO_Group_Latch      { action= SetMods(modifiers=Lock+Mod5, clearLocks); };
interpret ISO_Group_Lock       { action= LockMods(modifiers=Lock+Mod5); };
interpret ISO_Level3_Latch     { action= SetMods(modifiers=Shift+Lock+Mod3, clearLocks); };
interpret ISO_Level2_Latch     { action= SetMods(modifiers=Shift+Lock+Mod3+Mod5, clearLocks); };
interpret Shift_Lock           { action= LockMods(modifiers=Mod5); };
interpret ISO_Next_Group       { action= SetMods(modifiers=Mod3); };
interpret ISO_Prev_Group       { action= SetMods(modifiers=Mod5); };
interpret ISO_First_Group_Lock { action= LockGroup(group=1); };
interpret ISO_Next_Group_Lock  { action= LockGroup(group=+1); };
interpret ISO_Last_Group_Lock  { action= LockGroup(group=+2); };
interpret ISO_Prev_Group_Lock  { action= LockGroup(group=+3); };
interpret Overlay2_Enable      { action= LockControls(ctrls=Overlay2); };
interpret.repeat= True;
EOF
	if [ -z "$BUCHSTABENDIREKT" ]; then
	    echo 'interpret 0x110AD11 { action= Redirect(key=<REEE>, clearMods= Lock+Mod3+Mod5); };'
	else
	    echo 'interpret 0x110AD11 { action= Redirect(key=<AC03>, clearMods= Lock+Mod3+Mod5); };'
	fi

	[ -z "$STEUERDIREKT" ] && cat <<EOF
interpret 0x110AB01     { action= Redirect(key=<ESC>,  clearMods= Lock+Mod3+Mod5); };
interpret 0x110AB03     { action= Redirect(key=<INS>,  clearMods= Lock+Mod3+Mod5); };
interpret 0x110AB04     { action= Redirect(key=<RTRN>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AB05     { action= Redirect(key=<UNDO>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AC01     { action= Redirect(key=<HOME>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AC02     { action= Redirect(key=<LEFT>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AC03     { action= Redirect(key=<DOWN>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AC04     { action= Redirect(key=<RGHT>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AC05     { action= Redirect(key=<END>,  clearMods= Lock+Mod3+Mod5); };
interpret 0x110AD01     { action= Redirect(key=<PGUP>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AD02     { action= Redirect(key=<BKSP>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AD03     { action= Redirect(key=<NUP>,  clearMods= Lock+Mod3+Mod5); };
interpret 0x110AD04     { action= Redirect(key=<DELE>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AD05     { action= Redirect(key=<PGDN>, clearMods= Lock+Mod3+Mod5); };
interpret 0x110AE04     { action= Redirect(key=<BEGI>, clearMods= Lock+Mod3+Mod5); };
interpret Pointer_Drag1 { action= Redirect(key=<TAB>,  clearMods=Lock+Mod3+Mod5); };
EOF

	[ -n "$CUAHACK" ] && cat <<EOF
interpret 0x110AA01 { action= Redirect(key=<DELE>, clearMods= Lock+Mod3+Mod5, Mods= Shift); };
interpret 0x110AA02 { action= Redirect(key=<INS>,  clearMods= Shift+Lock+Mod3+Mod5, Mods= Control); };
interpret 0x110AA03 { action= Redirect(key=<INS>,  clearMods= Lock+Mod3+Mod5, Mods= Shift); };
EOF

	if [ -z "$USUMSONST" ]; then
	    cat <<EOF
indicator "Num Lock" {
    !allowExplicit;
    whichModState= locked;
    modifiers= Mod3+Mod5;
};
indicator "Caps Lock" {
    !allowExplicit;
    whichModState= locked;
    modifiers= Lock;
};
EOF
	else
	    cat <<EOF
indicator "Num Lock" {
    !allowExplicit;
    ctrls= Overlay2;
};
indicator "Caps Lock" {
    !allowExplicit;
    whichModState= locked;
    modifiers= Mod3+Mod5+Lock;
};
EOF
	fi

	cat <<EOF
indicator "Scroll Lock" {
    !allowExplicit;
    groups= 0xfe;
};
EOF
    else
	# Notbelegung
	cat <<EOF
interpret ISO_Next_Group   { action= SetGroup(group=+1); };
interpret Num_Lock         { action= LockControls(ctrls=Overlay1); };
interpret ISO_Prev_Group   { action= SetControls(ctrls=Overlay1); };
interpret ISO_Level3_Shift { action= SetMods(modifiers=Mod5); };
interpret.repeat= True;
indicator "Caps Lock" {
    !allowExplicit;
    whichModState= locked;
    modifiers= Lock;
};
EOF
    fi

    # Tastaturmaus Ebene 1
    [ -n "$MAUSKP1" ] && cat <<EOF
interpret.repeat= True;
interpret KP_1              { action= MovePtr(x=-1,y=+1); };
interpret diamond           { action= MovePtr(x=-1,y=+1); };
interpret KP_2              { action= MovePtr(x=+0,y=+1); };
interpret heart             { action= MovePtr(x=+0,y=+1); };
interpret KP_3              { action= MovePtr(x=+1,y=+1); };
interpret 0x1002660         { action= MovePtr(x=+1,y=+1); };
interpret KP_4              { action= MovePtr(x=-1,y=+0); };
interpret club              { action= MovePtr(x=-1,y=+0); };
interpret KP_6              { action= MovePtr(x=+1,y=+0); };
interpret 0x1002023         { action= MovePtr(x=+1,y=+0); };
interpret KP_7              { action= MovePtr(x=-1,y=-1); };
interpret 0x1002714         { action= MovePtr(x=-1,y=-1); };
interpret KP_8              { action= MovePtr(x=+0,y=-1); };
interpret 0x1002718         { action= MovePtr(x=+0,y=-1); };
interpret KP_9              { action= MovePtr(x=+1,y=-1); };
interpret dagger            { action= MovePtr(x=+1,y=-1); };
interpret KP_Add            { action= PtrBtn(button=4); };
interpret KP_Subtract       { action= PtrBtn(button=5); };
interpret.repeat= False;
interpret KP_Divide         { action= PtrBtn(button=2); };
interpret KP_Multiply       { action= PtrBtn(button=3); };
interpret KP_5              { action= PtrBtn(button=1); };
interpret 0x20AC+Mod3       { action= PtrBtn(button=1); };
interpret KP_0              { action= LockPtrBtn(button=1); };
interpret 0x1002423         { action= LockPtrBtn(button=1); };
interpret KP_Separator      { action= LockPtrBtn(button=3); };
interpret KP_Decimal        { action= LockPtrBtn(button=3); };
EOF

    # Tastaturmaus Ebene 4
    [ -n "$MAUSKP4" ] && cat <<EOF
interpret.repeat= True;
interpret KP_End       { action= MovePtr(x=-1,y=+1); };
interpret KP_Down      { action= MovePtr(x=+0,y=+1); };
interpret KP_Next      { action= MovePtr(x=+1,y=+1); };
interpret KP_Left      { action= MovePtr(x=-1,y=+0); };
interpret KP_Right     { action= MovePtr(x=+1,y=+0); };
interpret KP_Home      { action= MovePtr(x=-1,y=-1); };
interpret KP_Up        { action= MovePtr(x=+0,y=-1); };
interpret KP_Prior     { action= MovePtr(x=+1,y=-1); };
interpret 0x1002216    { action= PtrBtn(button=4); };
interpret 0x1002213    { action= PtrBtn(button=5); };
interpret.repeat= False;
interpret 0x1002044    { action= PtrBtn(button=2); };
interpret multiply     { action= PtrBtn(button=3); };
interpret KP_Begin     { action= PtrBtn(button=1); };
interpret KP_Insert    { action= LockPtrBtn(button=1); };
interpret KP_Delete    { action= LockPtrBtn(button=3); };
interpret 0x110AE16    { action= Redirect(key=<KPMU>, clearMods= Mod3); };
EOF

    [ -z "$KPDIREKT" ] && cat <<EOF
interpret.repeat= True;
interpret 0x110AA04 { action= Redirect(key=<KP0>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB07 { action= Redirect(key=<KP1>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB08 { action= Redirect(key=<KP2>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB09 { action= Redirect(key=<KP3>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC07 { action= Redirect(key=<KP4>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC08 { action= Redirect(key=<KP5>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC09 { action= Redirect(key=<KP6>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC10 { action= Redirect(key=<KPDL>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD07 { action= Redirect(key=<KP7>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD08 { action= Redirect(key=<KP8>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD09 { action= Redirect(key=<KP9>,  clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD10 { action= Redirect(key=<KPAD>, clearMods=Lock+Mod3+Mod5); };
interpret 0x110AD13 { action= Redirect(key=<KPEN>, clearMods=Lock+Mod3+Mod5); };
interpret 0x110AE09 { action= Redirect(key=<KPDV>, clearMods=Lock+Mod3+Mod5); };
interpret 0x110AE10 { action= Redirect(key=<KPMU>, clearMods=Lock+Mod3+Mod5); };
interpret 0x110AE11 { action= Redirect(key=<KPSU>, clearMods=Lock+Mod3+Mod5); };
EOF

    [ -z "$SZDIREKT" ] && cat <<EOF
interpret 0x110AC28 { action= Redirect(key=<R000>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC48 { action= Redirect(key=<R000>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD26 { action= Redirect(key=<R111>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AD46 { action= Redirect(key=<R111>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC31 { action= Redirect(key=<R222>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC51 { action= Redirect(key=<R222>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB21 { action= Redirect(key=<R333>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AB41 { action= Redirect(key=<R333>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB22 { action= Redirect(key=<R444>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AB42 { action= Redirect(key=<R444>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB27 { action= Redirect(key=<R555>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AB47 { action= Redirect(key=<R555>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD25 { action= Redirect(key=<R666>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AD45 { action= Redirect(key=<R666>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD30 { action= Redirect(key=<R777>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AD50 { action= Redirect(key=<R777>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC25 { action= Redirect(key=<R888>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC45 { action= Redirect(key=<R888>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC27 { action= Redirect(key=<R999>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC47 { action= Redirect(key=<R999>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD22 { action= Redirect(key=<RC09>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC29 { action= Redirect(key=<RC09>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC23 { action= Redirect(key=<RD03>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AD23 { action= Redirect(key=<RD03>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC24 { action= Redirect(key=<RD04>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AD24 { action= Redirect(key=<RD04>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD27 { action= Redirect(key=<RCOM>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x1109000 { action= Redirect(key=<RCOM>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AD28 { action= Redirect(key=<RPKT>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x1108999 { action= Redirect(key=<RPKT>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB26 { action= Redirect(key=<RD09>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AD29 { action= Redirect(key=<RD09>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB23 { action= Redirect(key=<RC01>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC21 { action= Redirect(key=<RC01>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC26 { action= Redirect(key=<RC02>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AC22 { action= Redirect(key=<RC02>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AC30 { action= Redirect(key=<RB10>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AB30 { action= Redirect(key=<RB10>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB24 { action= Redirect(key=<RB05>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AB25 { action= Redirect(key=<RB05>, clearMods=Lock+Mod3+Mod5+Shift); };
interpret 0x110AB28 { action= Redirect(key=<RB09>, clearMods=Lock+Mod3+Mod5, Mods=Shift); };
interpret 0x110AB29 { action= Redirect(key=<RB09>, clearMods=Lock+Mod3+Mod5+Shift); };
EOF

    [ -z "$BUCHSTABENDIREKT" ] && cat <<EOF
interpret 0x1109001 { action= Redirect(key=<RAAA>, clearMods=Mod3+Mod5); };
interpret 0x1109002 { action= Redirect(key=<RBBB>, clearMods=Mod3+Mod5); };
interpret 0x1109003 { action= Redirect(key=<RCCC>, clearMods=Mod3+Mod5); };
interpret 0x1109004 { action= Redirect(key=<RDDD>, clearMods=Mod3+Mod5); };
interpret 0x1109005 { action= Redirect(key=<REEE>, clearMods=Mod3+Mod5); };
interpret 0x1109006 { action= Redirect(key=<RFFF>, clearMods=Mod3+Mod5); };
interpret 0x1109007 { action= Redirect(key=<RGGG>, clearMods=Mod3+Mod5); };
interpret 0x1109008 { action= Redirect(key=<RHHH>, clearMods=Mod3+Mod5); };
interpret 0x1109009 { action= Redirect(key=<RIII>, clearMods=Mod3+Mod5); };
interpret 0x1109010 { action= Redirect(key=<RJJJ>, clearMods=Mod3+Mod5); };
interpret 0x1109011 { action= Redirect(key=<RKKK>, clearMods=Mod3+Mod5); };
interpret 0x1109012 { action= Redirect(key=<RLLL>, clearMods=Mod3+Mod5); };
interpret 0x1109013 { action= Redirect(key=<RMMM>, clearMods=Mod3+Mod5); };
interpret 0x1109014 { action= Redirect(key=<RNNN>, clearMods=Mod3+Mod5); };
interpret 0x1109015 { action= Redirect(key=<ROOO>, clearMods=Mod3+Mod5); };
interpret 0x1109016 { action= Redirect(key=<RPPP>, clearMods=Mod3+Mod5); };
interpret 0x1109017 { action= Redirect(key=<RQQQ>, clearMods=Mod3+Mod5); };
interpret 0x1109018 { action= Redirect(key=<RRRR>, clearMods=Mod3+Mod5); };
interpret 0x1109019 { action= Redirect(key=<RSSS>, clearMods=Mod3+Mod5); };
interpret 0x1109020 { action= Redirect(key=<RTTT>, clearMods=Mod3+Mod5); };
interpret 0x1109021 { action= Redirect(key=<RUUU>, clearMods=Mod3+Mod5); };
interpret 0x1109022 { action= Redirect(key=<RVVV>, clearMods=Mod3+Mod5); };
interpret 0x1109023 { action= Redirect(key=<RWWW>, clearMods=Mod3+Mod5); };
interpret 0x1109024 { action= Redirect(key=<RXXX>, clearMods=Mod3+Mod5); };
interpret 0x1109025 { action= Redirect(key=<RYYY>, clearMods=Mod3+Mod5); };
interpret 0x1109026 { action= Redirect(key=<RZZZ>, clearMods=Mod3+Mod5); };
interpret 0x1109027 { action= Redirect(key=<RUAE>, clearMods=Mod3+Mod5); };
interpret 0x1109028 { action= Redirect(key=<RUOE>, clearMods=Mod3+Mod5); };
interpret 0x1109029 { action= Redirect(key=<RUUE>, clearMods=Mod3+Mod5); };
interpret 0x1109030 { action= Redirect(key=<RUSS>, clearMods=Mod3+Mod5); };
EOF

    [ -n "$XF86" ] && cat <<EOF
interpret.repeat= False;
interpret XF86_Switch_VT_1  { action= SwitchScreen(screen=1,!same); };
interpret XF86_Switch_VT_2  { action= SwitchScreen(screen=2,!same); };
interpret XF86_Switch_VT_3  { action= SwitchScreen(screen=3,!same); };
interpret XF86_Switch_VT_4  { action= SwitchScreen(screen=4,!same); };
interpret XF86_Switch_VT_5  { action= SwitchScreen(screen=5,!same); };
interpret XF86_Switch_VT_6  { action= SwitchScreen(screen=6,!same); };
interpret XF86_Switch_VT_7  { action= SwitchScreen(screen=7,!same); };
interpret XF86_Switch_VT_8  { action= SwitchScreen(screen=8,!same); };
interpret XF86_Switch_VT_9  { action= SwitchScreen(screen=9,!same); };
interpret XF86_Switch_VT_10 { action= SwitchScreen(screen=10,!same); };
interpret XF86_Switch_VT_11 { action= SwitchScreen(screen=11,!same); };
interpret XF86_Switch_VT_12 { action= SwitchScreen(screen=12,!same); };
interpret XF86_Ungrab     { action= Private(type=0x86, data= "Ungrab"); };
interpret XF86_ClearGrab  { action= Private(type=0x86, data= "ClsGrb"); };
interpret XF86_Next_VMode { action = Private(type=0x86, data="+VMode"); };
interpret XF86_Prev_VMode { action = Private(type=0x86, data="-VMode"); };
EOF

    for fi in $COMPAT; do
	cat "$fi"
    done

    echo '};'
}

std_belegung () {
    LAYOUTNAME[0]='Aus der Neo-Welt'
    LAYOUTNAME[1]='Aus der Neo-Welt Kyrillisch'
    LAYOUTNAME[2]='Aus der Neo-Welt Griechisch'
    LAYOUTNAME[3]=US
    LAYOUTNAME[4]=CH
    LAYOUTNAME[5]=DE

    ALTERNATIVE[0]=Pointer_Drag1
    ALTERNATIVE[1]=Pointer_Drag1
    ALTERNATIVE[2]=0x110AD10
    ALTERNATIVE[3]=0x110AD13
    ALTERNATIVE[4]=0x110AE09
    ALTERNATIVE[5]=0x110AE10
    ALTERNATIVE[6]=0x110AE11
    ALTERNATIVE[7]=0x110AA04
    ALTERNATIVE[8]=0x110AB07
    ALTERNATIVE[9]=0x110AB08
    ALTERNATIVE[10]=0x110AB09
    ALTERNATIVE[11]=0x110AC07
    ALTERNATIVE[12]=0x110AC08
    ALTERNATIVE[13]=0x110AC09
    ALTERNATIVE[14]=0x110AD07
    ALTERNATIVE[15]=0x110AD08
    ALTERNATIVE[16]=0x110AD09
    ALTERNATIVE[17]=0x110AC10
    ALTERNATIVE[18]=multiply

    ALTERNATIVE[22]=0x110AD22
    ALTERNATIVE[23]=0x110AD23
    ALTERNATIVE[24]=0x110AD24
    ALTERNATIVE[25]=0x110AD25
    ALTERNATIVE[26]=0x110AD26
    ALTERNATIVE[27]=0x110AD27
    ALTERNATIVE[28]=0x110AD28
    ALTERNATIVE[29]=0x110AD29
    ALTERNATIVE[30]=0x110AD30
    ALTERNATIVE[31]=0x110AC21
    ALTERNATIVE[32]=0x110AC22
    ALTERNATIVE[33]=0x110AC23
    ALTERNATIVE[34]=0x110AC24
    ALTERNATIVE[35]=0x110AC25
    ALTERNATIVE[36]=0x110AC26
    ALTERNATIVE[37]=0x110AC27
    ALTERNATIVE[38]=0x110AC28
    ALTERNATIVE[39]=0x110AC29
    ALTERNATIVE[40]=0x110AC30
    ALTERNATIVE[41]=0x110AC31
    ALTERNATIVE[42]=0x110AB21
    ALTERNATIVE[43]=0x110AB22
    ALTERNATIVE[44]=0x110AB23
    ALTERNATIVE[45]=0x110AB24
    ALTERNATIVE[46]=0x110AB25
    ALTERNATIVE[47]=0x110AB26
    ALTERNATIVE[48]=0x110AB27
    ALTERNATIVE[49]=0x110AB28
    ALTERNATIVE[50]=0x110AB29
    ALTERNATIVE[51]=0x110AB30

    ALTERNATIVE[52]=0x110AB01
    ALTERNATIVE[53]=0x110AB03
    ALTERNATIVE[54]=0x110AB04
    ALTERNATIVE[55]=0x110AB05
    ALTERNATIVE[56]=0x110AC01
    ALTERNATIVE[57]=0x110AC02
    ALTERNATIVE[58]=0x110AC03
    ALTERNATIVE[59]=0x110AC04
    ALTERNATIVE[60]=0x110AC05
    ALTERNATIVE[61]=0x110AD01
    ALTERNATIVE[62]=0x110AD02
    ALTERNATIVE[63]=0x110AD03
    ALTERNATIVE[64]=0x110AD04
    ALTERNATIVE[65]=0x110AD05
    ALTERNATIVE[66]=0x110AE04
    ALTERNATIVE[67]=0x1108999
    ALTERNATIVE[68]=0x1109000

    ALTERNATIVE[70]=0x110AC48
    ALTERNATIVE[71]=0x110AD46
    ALTERNATIVE[72]=0x110AC51
    ALTERNATIVE[73]=0x110AB41
    ALTERNATIVE[74]=0x110AB42
    ALTERNATIVE[75]=0x110AB47
    ALTERNATIVE[76]=0x110AD45
    ALTERNATIVE[77]=0x110AD50
    ALTERNATIVE[78]=0x110AC45
    ALTERNATIVE[79]=0x110AC47

    ALTERNATIVE[80]=0x110AA01
    ALTERNATIVE[81]=0x110AA02
    ALTERNATIVE[82]=0x110AA03

    ALTERNATIVE[101]=0x1109001
    ALTERNATIVE[102]=0x1109002
    ALTERNATIVE[103]=0x1109003
    ALTERNATIVE[104]=0x1109004
    ALTERNATIVE[105]=0x1109005
    ALTERNATIVE[106]=0x1109006
    ALTERNATIVE[107]=0x1109007
    ALTERNATIVE[108]=0x1109008
    ALTERNATIVE[109]=0x1109009
    ALTERNATIVE[110]=0x1109010
    ALTERNATIVE[111]=0x1109011
    ALTERNATIVE[112]=0x1109012
    ALTERNATIVE[113]=0x1109013
    ALTERNATIVE[114]=0x1109014
    ALTERNATIVE[115]=0x1109015
    ALTERNATIVE[116]=0x1109016
    ALTERNATIVE[117]=0x1109017
    ALTERNATIVE[118]=0x1109018
    ALTERNATIVE[119]=0x1109019
    ALTERNATIVE[120]=0x1109020
    ALTERNATIVE[121]=0x1109021
    ALTERNATIVE[122]=0x1109022
    ALTERNATIVE[123]=0x1109023
    ALTERNATIVE[124]=0x1109024
    ALTERNATIVE[125]=0x1109025
    ALTERNATIVE[126]=0x1109026
    ALTERNATIVE[127]=0x1109027
    ALTERNATIVE[128]=0x1109028
    ALTERNATIVE[129]=0x1109029
    ALTERNATIVE[130]=0x1109030

    ALTERNATIVE[131]=0x1109001
    ALTERNATIVE[132]=0x1109002
    ALTERNATIVE[133]=0x1109003
    ALTERNATIVE[134]=0x1109004
    ALTERNATIVE[135]=0x1109005
    ALTERNATIVE[136]=0x1109006
    ALTERNATIVE[137]=0x1109007
    ALTERNATIVE[138]=0x1109008
    ALTERNATIVE[139]=0x1109009
    ALTERNATIVE[140]=0x1109010
    ALTERNATIVE[141]=0x1109011
    ALTERNATIVE[142]=0x1109012
    ALTERNATIVE[143]=0x1109013
    ALTERNATIVE[144]=0x1109014
    ALTERNATIVE[145]=0x1109015
    ALTERNATIVE[146]=0x1109016
    ALTERNATIVE[147]=0x1109017
    ALTERNATIVE[148]=0x1109018
    ALTERNATIVE[149]=0x1109019
    ALTERNATIVE[150]=0x1109020
    ALTERNATIVE[151]=0x1109021
    ALTERNATIVE[152]=0x1109022
    ALTERNATIVE[153]=0x1109023
    ALTERNATIVE[154]=0x1109024
    ALTERNATIVE[155]=0x1109025
    ALTERNATIVE[156]=0x1109026
    ALTERNATIVE[157]=0x1109027
    ALTERNATIVE[158]=0x1109028
    ALTERNATIVE[159]=0x1109029
    ALTERNATIVE[160]=0x1109030

    if [ -n "$KPDIREKT" ]; then
	ALTERNATIVE[0]=Tab
	ALTERNATIVE[1]=ISO_Left_Tab
	ALTERNATIVE[2]=KP_Add
	ALTERNATIVE[3]=KP_Enter
	ALTERNATIVE[4]=KP_Divide
	ALTERNATIVE[5]=KP_Multiply
	ALTERNATIVE[6]=KP_Subtract
	ALTERNATIVE[7]=KP_0
	ALTERNATIVE[8]=KP_1
	ALTERNATIVE[9]=KP_2
	ALTERNATIVE[10]=KP_3
	ALTERNATIVE[11]=KP_4
	ALTERNATIVE[12]=KP_5
	ALTERNATIVE[13]=KP_6
	ALTERNATIVE[14]=KP_7
	ALTERNATIVE[15]=KP_8
	ALTERNATIVE[16]=KP_9
	ALTERNATIVE[17]=KP_Separator
	[ -n "$PUNKT" ] && ALTERNATIVE[17]=KP_Decimal
    else
	[ -n "$MAUSKP4" ] && ALTERNATIVE[18]=0x110AE16
    fi

    if [ -n "$SZDIREKT" ]; then
	ALTERNATIVE[22]=underscore
	ALTERNATIVE[23]=bracketleft
	ALTERNATIVE[24]=bracketright
	ALTERNATIVE[25]=asciicircum
	ALTERNATIVE[26]=exclam
	ALTERNATIVE[27]=less
	ALTERNATIVE[28]=greater
	ALTERNATIVE[29]=equal
	ALTERNATIVE[30]=ampersand
	ALTERNATIVE[31]=backslash
	ALTERNATIVE[32]=slash
	ALTERNATIVE[33]=braceleft
	ALTERNATIVE[34]=braceright
	ALTERNATIVE[35]=asterisk
	ALTERNATIVE[36]=question
	ALTERNATIVE[37]=parenleft
	ALTERNATIVE[38]=parenright
	ALTERNATIVE[39]=minus
	ALTERNATIVE[40]=colon
	ALTERNATIVE[41]=at
	ALTERNATIVE[42]=numbersign
	ALTERNATIVE[43]=dollar
	ALTERNATIVE[44]=bar
	ALTERNATIVE[45]=asciitilde
	ALTERNATIVE[46]=grave
	ALTERNATIVE[47]=plus
	ALTERNATIVE[48]=percent
	ALTERNATIVE[49]=quotedbl
	ALTERNATIVE[50]=apostrophe
	ALTERNATIVE[51]=semicolon
	ALTERNATIVE[67]=period
	ALTERNATIVE[68]=comma

	ALTERNATIVE[70]=0
	ALTERNATIVE[71]=1
	ALTERNATIVE[72]=2
	ALTERNATIVE[73]=3
	ALTERNATIVE[74]=4
	ALTERNATIVE[75]=5
	ALTERNATIVE[76]=6
	ALTERNATIVE[77]=7
	ALTERNATIVE[78]=8
	ALTERNATIVE[79]=9
    fi

    if [ -n "$STEUERDIREKT" ]; then
	ALTERNATIVE[52]=Escape
	ALTERNATIVE[53]=Insert
	ALTERNATIVE[54]=Return
	ALTERNATIVE[55]=Undo
	ALTERNATIVE[56]=Home
	ALTERNATIVE[57]=Left
	ALTERNATIVE[58]=Down
	ALTERNATIVE[59]=Right
	ALTERNATIVE[60]=End
	ALTERNATIVE[61]=Prior
	ALTERNATIVE[62]=BackSpace
	ALTERNATIVE[63]=Up
	ALTERNATIVE[64]=Delete
	ALTERNATIVE[65]=Next
	ALTERNATIVE[66]=Begin
    fi

    if [ -z "$CUAHACK" ]; then
	ALTERNATIVE[80]=Control_L
	ALTERNATIVE[81]=Super_L
	ALTERNATIVE[82]=Alt_L
    fi

    if [ -n "$BUCHSTABENDIREKT" ]; then
	ALTERNATIVE[101]=a
	ALTERNATIVE[102]=b
	ALTERNATIVE[103]=c
	ALTERNATIVE[104]=d
	ALTERNATIVE[105]=e
	ALTERNATIVE[106]=f
	ALTERNATIVE[107]=g
	ALTERNATIVE[108]=h
	ALTERNATIVE[109]=i
	ALTERNATIVE[110]=j
	ALTERNATIVE[111]=k
	ALTERNATIVE[112]=l
	ALTERNATIVE[113]=m
	ALTERNATIVE[114]=n
	ALTERNATIVE[115]=o
	ALTERNATIVE[116]=p
	ALTERNATIVE[117]=q
	ALTERNATIVE[118]=r
	ALTERNATIVE[119]=s
	ALTERNATIVE[120]=t
	ALTERNATIVE[121]=u
	ALTERNATIVE[122]=v
	ALTERNATIVE[123]=w
	ALTERNATIVE[124]=x
	ALTERNATIVE[125]=y
	ALTERNATIVE[126]=z
	ALTERNATIVE[127]=adiaeresis
	ALTERNATIVE[128]=odiaeresis
	ALTERNATIVE[129]=udiaeresis
	ALTERNATIVE[130]=ssharp
	ALTERNATIVE[131]=A
	ALTERNATIVE[132]=B
	ALTERNATIVE[133]=C
	ALTERNATIVE[134]=D
	ALTERNATIVE[135]=E
	ALTERNATIVE[136]=F
	ALTERNATIVE[137]=G
	ALTERNATIVE[138]=H
	ALTERNATIVE[139]=I
	ALTERNATIVE[140]=J
	ALTERNATIVE[141]=K
	ALTERNATIVE[142]=L
	ALTERNATIVE[143]=M
	ALTERNATIVE[144]=N
	ALTERNATIVE[145]=O
	ALTERNATIVE[146]=P
	ALTERNATIVE[147]=Q
	ALTERNATIVE[148]=R
	ALTERNATIVE[149]=S
	ALTERNATIVE[150]=T
	ALTERNATIVE[151]=U
	ALTERNATIVE[152]=V
	ALTERNATIVE[153]=W
	ALTERNATIVE[154]=X
	ALTERNATIVE[155]=Y
	ALTERNATIVE[156]=Z
	ALTERNATIVE[157]=Adiaeresis
	ALTERNATIVE[158]=Odiaeresis
	ALTERNATIVE[159]=Udiaeresis
	ALTERNATIVE[160]=0x1001E9E
    fi

    if [ -n "$PUNKT" ]; then
	ALTERNATIVE[19]=${ALTERNATIVE[68]}
	ALTERNATIVE[20]=KP_Decimal
	ALTERNATIVE[21]=${ALTERNATIVE[67]}
    else
	ALTERNATIVE[19]=${ALTERNATIVE[67]}
	ALTERNATIVE[20]=KP_Separator
	ALTERNATIVE[21]=${ALTERNATIVE[68]}
    fi

    if [ -n "$XCVORIG" ]; then
	ALTERNATIVE[83]=${ALTERNATIVE[122]}
	ALTERNATIVE[84]=${ALTERNATIVE[152]}
	ALTERNATIVE[184]=${ALTERNATIVE[125]}
	ALTERNATIVE[185]=${ALTERNATIVE[124]}
	ALTERNATIVE[188]=${ALTERNATIVE[103]}
	ALTERNATIVE[214]=${ALTERNATIVE[155]}
	ALTERNATIVE[215]=${ALTERNATIVE[154]}
	ALTERNATIVE[218]=${ALTERNATIVE[133]}
    else
	ALTERNATIVE[83]=${ALTERNATIVE[68]}
	ALTERNATIVE[84]=endash
	ALTERNATIVE[184]=${ALTERNATIVE[124]}
	ALTERNATIVE[185]=${ALTERNATIVE[125]}
	ALTERNATIVE[188]=${ALTERNATIVE[128]}
	ALTERNATIVE[214]=${ALTERNATIVE[154]}
	ALTERNATIVE[215]=${ALTERNATIVE[126]}
	ALTERNATIVE[218]=${ALTERNATIVE[158]}
    fi

    if [ -n "$QWERTZCTRLALT" ]; then
	ALTERNATIVE[85]=${ALTERNATIVE[118]}
	ALTERNATIVE[86]=${ALTERNATIVE[148]}
	ALTERNATIVE[161]=${ALTERNATIVE[106]}
	ALTERNATIVE[162]=${ALTERNATIVE[114]}
	ALTERNATIVE[163]=${ALTERNATIVE[109]}
	ALTERNATIVE[164]=${ALTERNATIVE[108]}
	ALTERNATIVE[165]=${ALTERNATIVE[104]}
	ALTERNATIVE[166]=${ALTERNATIVE[129]}
	ALTERNATIVE[167]=${ALTERNATIVE[121]}
	ALTERNATIVE[168]=${ALTERNATIVE[101]}
	ALTERNATIVE[169]=${ALTERNATIVE[119]}
	ALTERNATIVE[170]=${ALTERNATIVE[116]}
	ALTERNATIVE[171]=${ALTERNATIVE[117]}
	ALTERNATIVE[172]=${ALTERNATIVE[115]}
	ALTERNATIVE[173]=${ALTERNATIVE[67]}
	ALTERNATIVE[174]=${ALTERNATIVE[112]}
	ALTERNATIVE[175]=${ALTERNATIVE[107]}
	ALTERNATIVE[176]=${ALTERNATIVE[113]}
	ALTERNATIVE[177]=${ALTERNATIVE[102]}
	ALTERNATIVE[178]=${ALTERNATIVE[111]}
	ALTERNATIVE[179]=${ALTERNATIVE[128]}
	ALTERNATIVE[180]=${ALTERNATIVE[110]}
	ALTERNATIVE[181]=${ALTERNATIVE[123]}
	ALTERNATIVE[182]=${ALTERNATIVE[126]}
	ALTERNATIVE[183]=${ALTERNATIVE[68]}
	ALTERNATIVE[186]=${ALTERNATIVE[39]}
	ALTERNATIVE[187]=${ALTERNATIVE[120]}
	ALTERNATIVE[189]=${ALTERNATIVE[105]}
	ALTERNATIVE[190]=${ALTERNATIVE[127]}
	ALTERNATIVE[191]=${ALTERNATIVE[136]}
	ALTERNATIVE[192]=${ALTERNATIVE[144]}
	ALTERNATIVE[193]=${ALTERNATIVE[139]}
	ALTERNATIVE[194]=${ALTERNATIVE[138]}
	ALTERNATIVE[195]=${ALTERNATIVE[134]}
	ALTERNATIVE[196]=${ALTERNATIVE[159]}
	ALTERNATIVE[197]=${ALTERNATIVE[151]}
	ALTERNATIVE[198]=${ALTERNATIVE[131]}
	ALTERNATIVE[199]=${ALTERNATIVE[149]}
	ALTERNATIVE[200]=${ALTERNATIVE[146]}
	ALTERNATIVE[201]=${ALTERNATIVE[147]}
	ALTERNATIVE[202]=${ALTERNATIVE[145]}
	ALTERNATIVE[203]=${ALTERNATIVE[40]}
	ALTERNATIVE[204]=${ALTERNATIVE[142]}
	ALTERNATIVE[205]=${ALTERNATIVE[107]}
	ALTERNATIVE[206]=${ALTERNATIVE[143]}
	ALTERNATIVE[207]=${ALTERNATIVE[132]}
	ALTERNATIVE[208]=${ALTERNATIVE[141]}
	ALTERNATIVE[209]=${ALTERNATIVE[158]}
	ALTERNATIVE[210]=${ALTERNATIVE[140]}
	ALTERNATIVE[211]=${ALTERNATIVE[153]}
	ALTERNATIVE[212]=${ALTERNATIVE[156]}
	ALTERNATIVE[213]=${ALTERNATIVE[51]}
	ALTERNATIVE[216]=${ALTERNATIVE[22]}
	ALTERNATIVE[217]=${ALTERNATIVE[150]}
	ALTERNATIVE[219]=${ALTERNATIVE[135]}
	ALTERNATIVE[220]=${ALTERNATIVE[157]}
    else
	ALTERNATIVE[85]=${ALTERNATIVE[67]}
	ALTERNATIVE[86]=enfilledcircbullet
	ALTERNATIVE[161]=${ALTERNATIVE[101]}
	ALTERNATIVE[162]=${ALTERNATIVE[102]}
	ALTERNATIVE[163]=${ALTERNATIVE[103]}
	ALTERNATIVE[164]=${ALTERNATIVE[104]}
	ALTERNATIVE[165]=${ALTERNATIVE[105]}
	ALTERNATIVE[166]=${ALTERNATIVE[106]}
	ALTERNATIVE[167]=${ALTERNATIVE[107]}
	ALTERNATIVE[168]=${ALTERNATIVE[108]}
	ALTERNATIVE[169]=${ALTERNATIVE[109]}
	ALTERNATIVE[171]=${ALTERNATIVE[141]}
	ALTERNATIVE[172]=${ALTERNATIVE[112]}
	ALTERNATIVE[173]=${ALTERNATIVE[113]}
	ALTERNATIVE[174]=${ALTERNATIVE[114]}
	ALTERNATIVE[175]=${ALTERNATIVE[115]}
	ALTERNATIVE[176]=${ALTERNATIVE[116]}
	ALTERNATIVE[177]=${ALTERNATIVE[117]}
	ALTERNATIVE[178]=${ALTERNATIVE[118]}
	ALTERNATIVE[179]=${ALTERNATIVE[119]}
	ALTERNATIVE[180]=${ALTERNATIVE[120]}
	ALTERNATIVE[181]=${ALTERNATIVE[121]}
	ALTERNATIVE[182]=${ALTERNATIVE[122]}
	ALTERNATIVE[183]=${ALTERNATIVE[123]}
	ALTERNATIVE[187]=${ALTERNATIVE[127]}
	ALTERNATIVE[189]=${ALTERNATIVE[129]}
	ALTERNATIVE[190]=${ALTERNATIVE[130]}
	ALTERNATIVE[191]=${ALTERNATIVE[131]}
	ALTERNATIVE[192]=${ALTERNATIVE[132]}
	ALTERNATIVE[193]=${ALTERNATIVE[133]}
	ALTERNATIVE[194]=${ALTERNATIVE[134]}
	ALTERNATIVE[195]=${ALTERNATIVE[135]}
	ALTERNATIVE[196]=${ALTERNATIVE[136]}
	ALTERNATIVE[197]=${ALTERNATIVE[137]}
	ALTERNATIVE[198]=${ALTERNATIVE[138]}
	ALTERNATIVE[199]=${ALTERNATIVE[139]}
	ALTERNATIVE[201]=${ALTERNATIVE[171]}
	ALTERNATIVE[202]=${ALTERNATIVE[142]}
	ALTERNATIVE[203]=${ALTERNATIVE[143]}
	ALTERNATIVE[204]=${ALTERNATIVE[144]}
	ALTERNATIVE[205]=${ALTERNATIVE[145]}
	ALTERNATIVE[206]=${ALTERNATIVE[146]}
	ALTERNATIVE[207]=${ALTERNATIVE[147]}
	ALTERNATIVE[208]=${ALTERNATIVE[148]}
	ALTERNATIVE[209]=${ALTERNATIVE[149]}
	ALTERNATIVE[210]=${ALTERNATIVE[150]}
	ALTERNATIVE[211]=${ALTERNATIVE[151]}
	ALTERNATIVE[212]=${ALTERNATIVE[152]}
	ALTERNATIVE[213]=${ALTERNATIVE[153]}
	ALTERNATIVE[217]=${ALTERNATIVE[157]}
	ALTERNATIVE[219]=${ALTERNATIVE[159]}
	ALTERNATIVE[220]=${ALTERNATIVE[160]}
	if [ -n "$ZJVARIANTE" ]; then
	    ALTERNATIVE[170]=${ALTERNATIVE[126]}
	    ALTERNATIVE[186]=${ALTERNATIVE[110]}
	    ALTERNATIVE[200]=${ALTERNATIVE[156]}
	    ALTERNATIVE[216]=${ALTERNATIVE[140]}
	else
	    ALTERNATIVE[170]=${ALTERNATIVE[110]}
	    ALTERNATIVE[186]=${ALTERNATIVE[126]}
	    ALTERNATIVE[200]=${ALTERNATIVE[140]}
	    ALTERNATIVE[216]=${ALTERNATIVE[156]}
	fi
    fi

    export LAYOUTNAME ALTERNATIVE

    parse_belegungen <<EOF
TLDE - RTLD RB05
NEO_N dead_circumflex dead_caron 0x10021BB dead_abovedot 0x10002DE 0xfe60 NoSymbol NoSymbol dead_circumflex dead_caron Pointer_EnableKeys
NEO_N dead_circumflex dead_caron 0x10021BB dead_abovedot 0x10002DE 0xfe60 NoSymbol NoSymbol dead_circumflex dead_caron Pointer_EnableKeys
NEO_N dead_circumflex dead_caron 0x10021BB dead_abovedot 0x10002DE 0xfe60 NoSymbol NoSymbol dead_circumflex dead_caron Pointer_EnableKeys
      ALT46           ALT45
      section         degree
      dead_circumflex degree

AE01 + R001 R111
NEO_N   ALT71 degree onesuperior ordfeminine 0x1002081 notsign ALT71 NoSymbol ALT71 degree
NEO_N   ALT71 degree onesuperior ordfeminine 0x1002081 notsign ALT71 NoSymbol ALT71 degree
NEO_N   ALT71 degree onesuperior ordfeminine 0x1002081 notsign ALT71 NoSymbol ALT71 degree
        ALT71 ALT26
NEO_TAB ALT71 ALT47  ALT44
        ALT71 ALT26

AE02 + R002 R222
NEO_N   ALT72 section twosuperior masculine 0x1002082 logicalor ALT72 NoSymbol ALT72 section
NEO_N   ALT72 section twosuperior masculine 0x1002082 logicalor ALT72 NoSymbol ALT72 section
NEO_N   ALT72 section twosuperior masculine 0x1002082 logicalor ALT72 NoSymbol ALT72 section
        ALT72 ALT41
NEO_TAB ALT72 ALT49   ALT41
NEO_TAB ALT72 ALT49   twosuperior

AE03 + R003 R333
NEO_N   ALT73 0x1002113 threesuperior numerosign 0x1002083 logicaland ALT73 NoSymbol ALT73 0x1002113
NEO_N   ALT73 0x1002113 threesuperior numerosign 0x1002083 logicaland ALT73 NoSymbol ALT73 0x1002113
NEO_N   ALT73 0x1002113 threesuperior numerosign 0x1002083 logicaland ALT73 NoSymbol ALT73 0x1002113
        ALT73 ALT42
NEO_TAB ALT73 ALT35     ALT42
NEO_TAB ALT73 section   threesuperior

AE04 + BEGI R444
NEO_N   ALT74 guillemotright 0x100203A ALT66 femalesymbol 0x10022A5 ALT74 NoSymbol ALT74 guillemotright ALT66
NEO_N   ALT74 guillemotright 0x100203A ALT66 femalesymbol 0x10022A5 ALT74 NoSymbol ALT74 guillemotright ALT66
NEO_N   ALT74 guillemotright 0x100203A ALT66 femalesymbol 0x10022A5 ALT74 NoSymbol ALT74 guillemotright ALT66
NEO_TAB ALT74 ALT43          0x20AC
NEO_TAB ALT74 ccedilla       ALT25
        ALT74 ALT43

AE05 + R005 R555
NEO_N   ALT75 guillemotleft 0x1002039 periodcentered malesymbol 0x1002221 ALT75 NoSymbol ALT75 guillemotleft
NEO_N   ALT75 guillemotleft 0x1002039 periodcentered malesymbol 0x1002221 ALT75 NoSymbol ALT75 guillemotleft
NEO_N   ALT75 guillemotleft 0x1002039 periodcentered malesymbol 0x1002221 ALT75 NoSymbol ALT75 guillemotleft
        ALT75 ALT48
NEO_TAB ALT75 ALT48         ALT45
        ALT75 ALT48

AE06 + R006 R666
NEO_N   ALT76 ALT43 cent    sterling 0x10026A5 0x1002225 ALT76 NoSymbol ALT76 ALT43
NEO_N   ALT76 ALT43 cent    sterling 0x10026A5 0x1002225 ALT76 NoSymbol ALT76 ALT43
NEO_N   ALT76 ALT43 cent    sterling 0x10026A5 0x1002225 ALT76 NoSymbol ALT76 ALT43
        ALT76 ALT25
NEO_TAB ALT76 ALT30 notsign
        ALT76 ALT30

AE07 + R007 R777
NEO_N   ALT77 0x20AC yen       currency 0x10003F0 rightarrow ALT77 NoSymbol ALT77 0x20AC
NEO_N   ALT77 0x20AC yen       currency 0x10003F0 rightarrow ALT77 NoSymbol ALT77 0x20AC
NEO_N   ALT77 0x20AC yen       currency 0x10003F0 rightarrow ALT77 NoSymbol ALT77 0x20AC
        ALT77 ALT30
NEO_TAB ALT77 ALT32  brokenbar
NEO_TAB ALT77 ALT32  ALT33

AE08 + TAB R888
NEO_N   ALT78 doublelowquotemark singlelowquotemark ALT0 0x10027E8 0x100221E ALT78 NoSymbol ALT78 doublelowquotemark ALT1
NEO_N   ALT78 doublelowquotemark singlelowquotemark ALT0 0x10027E8 0x100221E ALT78 NoSymbol ALT78 doublelowquotemark ALT1
NEO_N   ALT78 doublelowquotemark singlelowquotemark ALT0 0x10027E8 0x100221E ALT78 NoSymbol ALT78 doublelowquotemark ALT1
        ALT78 ALT35
NEO_TAB ALT78 ALT37              cent
NEO_TAB ALT78 ALT37              ALT23

AE09 + KPDV R999
NEO_N   ALT79 leftdoublequotemark leftsinglequotemark ALT4 0x10027E9 variation ALT79 NoSymbol ALT79 leftdoublequotemark ALT32
NEO_N   ALT79 leftdoublequotemark leftsinglequotemark ALT4 0x10027E9 variation ALT79 NoSymbol ALT79 leftdoublequotemark ALT32
NEO_N   ALT79 leftdoublequotemark leftsinglequotemark ALT4 0x10027E9 variation ALT79 NoSymbol ALT79 leftdoublequotemark ALT32
        ALT79 ALT37
        ALT79 ALT38
NEO_TAB ALT79 ALT38               ALT24

AE10 + KPMU R000
NEO_N   ALT70 rightdoublequotemark rightsinglequotemark ALT5 0x1002080 0x1002205 ALT70 NoSymbol ALT70 rightdoublequotemark ALT35
NEO_N   ALT70 rightdoublequotemark rightsinglequotemark ALT5 0x1002080 0x1002205 ALT70 NoSymbol ALT70 rightdoublequotemark ALT35
NEO_N   ALT70 rightdoublequotemark rightsinglequotemark ALT5 0x1002080 0x1002205 ALT70 NoSymbol ALT70 rightdoublequotemark ALT35
        ALT70 ALT38
NEO_TAB ALT70 ALT29                ALT46
NEO_TAB ALT70 ALT29                ALT34

AE11 + KPSU RC09
NEO_N   ALT39  emdash 0x1002212  ALT6 0x1002011 hyphen 0x1002212 NoSymbol ALT39 emdash ALT39
NEO_N   ALT39  emdash 0x1002212  ALT6 0x1002011 hyphen 0x1002212 NoSymbol ALT39 emdash ALT39
NEO_N   ALT39  emdash 0x1002212  ALT6 0x1002011 hyphen 0x1002212 NoSymbol ALT39 emdash ALT39
        ALT39  ALT22
NEO_TAB ALT50  ALT36  dead_acute
NEO_TAB ssharp ALT36  ALT31

AE12 - R012 RD09
NEO_N   dead_grave      dead_cedilla dead_abovering dead_diaeresis 0xfe65 dead_macron NoSymbol NoSymbol dead_grave dead_cedilla
NEO_N   dead_grave      dead_cedilla dead_abovering dead_diaeresis 0xfe65 dead_macron NoSymbol NoSymbol dead_grave dead_cedilla
NEO_N   dead_grave      dead_cedilla dead_abovering dead_diaeresis 0xfe65 dead_macron NoSymbol NoSymbol dead_grave dead_cedilla
        ALT29           ALT47
NEO_TAB dead_circumflex dead_grave   dead_tilde
        dead_acute      dead_grave

BKSP
NEO_34 BackSpace BackSpace BackSpace Terminate_Server

TAB
NEO_TAB Tab ISO_Left_Tab Multi_key Num_Lock

AD01 + PGUP RQQQ
NEO_A   ALT111      ALT141      ellipsis ALT61 Greek_kappa ALT18 0x101D458 0x101D43E ALT171 ALT201 ALT61
NEO_A   Cyrillic_ka Cyrillic_KA ellipsis ALT61 Greek_kappa ALT18 0x101D528 0x101D50E ALT171 ALT201 ALT61
NEO_A   Greek_kappa Greek_KAPPA ellipsis ALT61 Greek_kappa ALT18 0x101D705 0x101D6EB ALT171 ALT201 ALT61
        ALT117      ALT147
        ALT117      ALT147
NEO_TAB ALT117      ALT147      ALT41

AD02 + BKSP RWWW
NEO_A ALT121     ALT151     ALT22 ALT62 NoSymbol includedin 0x101D462 0x101D448 ALT181 ALT211 ALT62
NEO_A Cyrillic_u Cyrillic_U ALT22 ALT62 NoSymbol includedin 0x101D532 0x101D518 ALT181 ALT211 ALT62
NEO_A 0x1000374  0x1000375  ALT22 ALT62 NoSymbol includedin NoSymbol  NoSymbol  ALT181 ALT211 ALT62
      ALT123     ALT153

AD03 + NUP REEE
NEO_A   ALT129       ALT159       ALT23  ALT63 NoSymbol union NoSymbol NoSymbol ALT189 ALT219 ALT63
NEO_A   Serbian_tshe Serbian_TSHE ALT23  ALT63 NoSymbol union NoSymbol NoSymbol ALT189 ALT219 ALT63
NEO_A   0x10003E1    0x10003E0    ALT159 ALT63 NoSymbol union NoSymbol NoSymbol ALT189 ALT219 ALT63
        ALT105       ALT135
NEO_TAB ALT105       ALT135       0x20AC

AD04 + DELE RRRR
NEO_N ALT67  enfilledcircbullet ALT24 ALT64 0x10003D1 0x10021A6 ALT67     NoSymbol  ALT85 ALT86 ALT64
NEO_N ALT67  enfilledcircbullet ALT24 ALT64 0x10003D1 0x10021A6 ALT67     NoSymbol  ALT85 ALT86 ALT64
NEO_N ALT67  enfilledcircbullet ALT24 ALT64 0x10003D1 0x10021A6 0x101D717 0x101D719 ALT85 ALT86 ALT64
      ALT118 ALT148

AD05 + PGDN RTTT
NEO_A ALT127     ALT157     ALT25 ALT65 Greek_eta 0x1002135 NoSymbol  NoSymbol  ALT187 ALT217 ALT65
NEO_A Cyrillic_e Cyrillic_E ALT25 ALT65 Greek_eta 0x1002135 NoSymbol  NoSymbol  ALT187 ALT217 ALT65
NEO_A Greek_eta  Greek_ETA  ALT25 ALT65 Greek_eta 0x1002135 0x101D718 0x101D716 ALT187 ALT217 ALT65
      ALT120     ALT150

AD06 + RD06 RYYY
NEO_A ALT122      ALT152      ALT26 exclamdown NoSymbol radical 0x101D463 0x101D449 ALT182 ALT212
NEO_A Cyrillic_ve Cyrillic_VE ALT26 exclamdown NoSymbol radical 0x101D533 0x101D519 ALT182 ALT212
NEO_A 0x10003DD   0x10003DC   ALT26 exclamdown NoSymbol radical NoSymbol  NoSymbol  ALT182 ALT212
      ALT125      ALT155
      ALT126      ALT156

AD07 + KP7 RUUU
NEO_A ALT107       ALT137       ALT27 ALT14 Greek_gamma Greek_GAMMA 0x101D454 0x101D43A ALT167 ALT197 ALT77
NEO_A Cyrillic_ghe Cyrillic_GHE ALT27 ALT14 Greek_gamma Greek_GAMMA 0x101D524 0x101D50A ALT167 ALT197 ALT77
NEO_A Greek_gamma  Greek_GAMMA  ALT27 ALT14 Greek_gamma Greek_GAMMA 0x101D6FE 0x101D6E4 ALT167 ALT197 ALT77
      ALT121       ALT151

AD08 + KP8 RIII
NEO_A ALT103       ALT133       ALT28 ALT15 Greek_chi 0x1002102 0x101D450 0x101D436 ALT163 ALT193 ALT78
NEO_A Cyrillic_tse Cyrillic_TSE ALT28 ALT15 Greek_chi 0x1002102 0x101D520 0x100212D ALT163 ALT193 ALT78
NEO_A Greek_chi    Greek_CHI    ALT28 ALT15 Greek_chi 0x1002102 0x101D712 0x101D6F8 ALT163 ALT193 ALT78
      ALT109       ALT139

AD09 + KP9 ROOO
NEO_A ALT112      ALT142      ALT29 ALT16 Greek_lamda Greek_LAMDA 0x101D459 0x101D43F ALT172 ALT202 ALT79
NEO_A Cyrillic_el Cyrillic_EL ALT29 ALT16 Greek_lamda Greek_LAMDA 0x101D529 0x101D50F ALT172 ALT202 ALT79
NEO_A Greek_lamda Greek_LAMDA ALT29 ALT16 Greek_lamda Greek_LAMDA 0x101D706 0x101D6EC ALT172 ALT202 ALT79
      ALT115      ALT145

AD10 + KPAD RPPP
NEO_A ALT110      ALT140      ALT30 ALT2 Greek_theta Greek_THETA 0x101D457 0x101D43D ALT170 ALT200 ALT47
NEO_A Cyrillic_je Cyrillic_JE ALT30 ALT2 Greek_theta Greek_THETA 0x101D527 0x101D50D ALT170 ALT200 ALT47
NEO_A Greek_theta Greek_THETA ALT30 ALT2 Greek_theta Greek_THETA 0x101D703 0x101D6E9 ALT170 ALT200 ALT47
      ALT116      ALT146

AD11 + AC03 RD03
NEO_A   ALT106      ALT136      0x100017F 0x110AD11 Greek_phi Greek_PHI 0x101D453 0x101D439 ALT166 ALT196 0x110AD11
NEO_A   Cyrillic_ef Cyrillic_EF 0x100017F 0x110AD11 Greek_phi Greek_PHI 0x101D523 0x101D509 ALT166 ALT196 0x110AD11
NEO_A   Greek_phi   Greek_PHI   0x100017F 0x110AD11 Greek_phi Greek_PHI 0x101D711 0x101D6F7 ALT166 ALT196 0x110AD11
        ALT23       ALT33
NEO_TAB ALT129      egrave      ALT23
        ALT129      ALT159

AD12 - RD12 RD04
NEO_N   dead_acute     dead_tilde 0xfe63 dead_doubleacute 0xfe64 dead_breve NoSymbol NoSymbol dead_acute dead_tilde Codeinput
NEO_N   dead_acute     dead_tilde 0xfe63 dead_doubleacute 0xfe64 dead_breve NoSymbol NoSymbol dead_acute dead_tilde Codeinput
NEO_N   dead_acute     dead_tilde 0xfe63 dead_doubleacute 0xfe64 dead_breve NoSymbol NoSymbol dead_acute dead_tilde Codeinput
        ALT24          ALT34
NEO_TAB dead_diaeresis ALT26      ALT24
NEO_TAB ALT47          ALT35      ALT45

RTRN + KPEN
NEO_SPACE Return Return Return ALT3 Return Return Return Return Return Return ALT3
NEO_SPACE Return Return Return ALT3 Return Return Return Return Return Return ALT3
NEO_SPACE Return Return Return ALT3 Return Return Return Return Return Return ALT3
          Return

CAPS -
NEO_MOD3 ISO_Group_Shift ISO_Level2_Latch ISO_Next_Group ISO_Group_Latch
NEO_MOD3 ISO_Group_Shift ISO_Level2_Latch ISO_Next_Group ISO_Group_Latch
NEO_MOD3 ISO_Group_Shift ISO_Level2_Latch ISO_Next_Group ISO_Group_Latch
         Caps_Lock

AC01 + HOME RAAA
NEO_A ALT108      ALT138      ALT31 ALT56 Greek_psi Greek_PSI 0x100210E 0x101D43B ALT168 ALT198 ALT56
NEO_A Cyrillic_ha Cyrillic_HA ALT31 ALT56 Greek_psi Greek_PSI 0x101D525 0x100210C ALT168 ALT198 ALT56
NEO_A Greek_psi   Greek_PSI   ALT31 ALT56 Greek_psi Greek_PSI 0x101D713 0x101D6F9 ALT168 ALT198 ALT56
      ALT101      ALT131

AC02 + LEFT RSSS
NEO_A ALT109     ALT139     ALT32 ALT57 Greek_iota integral 0x101D456 0x101D43C ALT169 ALT199 ALT57
NEO_A Cyrillic_i Cyrillic_I ALT32 ALT57 Greek_iota integral 0x101D526 0x1002111 ALT169 ALT199 ALT57
NEO_A Greek_iota Greek_IOTA ALT32 ALT57 Greek_iota integral 0x101D704 0x101D6EA ALT169 ALT199 ALT57
      ALT119     ALT149

AC03 + DOWN RDDD
NEO_A ALT105        ALT135        ALT33 ALT58 Greek_epsilon 0x1002203 0x101D452 0x101D438 ALT165 ALT195 ALT58
NEO_A Cyrillic_ie   Cyrillic_IE   ALT33 ALT58 Greek_epsilon 0x1002203 0x101D522 0x101D508 ALT165 ALT195 ALT58
NEO_A Greek_epsilon Greek_EPSILON ALT33 ALT58 Greek_epsilon 0x1002203 0x101D6C6 0x101D6E6 ALT165 ALT195 ALT58
      ALT104        ALT134

AC04 + RGHT RFFF
NEO_A ALT101      ALT131      ALT34 ALT59 Greek_alpha 0x1002200 0x101D44E 0x101D434 ALT161 ALT191 ALT59
NEO_A Cyrillic_a  Cyrillic_A  ALT34 ALT59 Greek_alpha 0x1002200 0x101D51E 0x101D504 ALT161 ALT191 ALT59
NEO_A Greek_alpha Greek_ALPHA ALT34 ALT59 Greek_alpha 0x1002200 0x101D6FC 0x101D6E2 ALT161 ALT191 ALT59
      ALT106      ALT136

AC05 + END RGGG
NEO_A ALT115        ALT145        ALT35 ALT60 Greek_omicron 0x1002208 0x101D45C 0x101D442 ALT175 ALT205 ALT60
NEO_A Cyrillic_o    Cyrillic_O    ALT35 ALT60 Greek_omicron 0x1002208 0x101D52C 0x101D512 ALT175 ALT205 ALT60
NEO_A Greek_omicron Greek_OMICRON ALT35 ALT60 Greek_omicron 0x1002208 0x101D70A 0x101D6F0 ALT175 ALT205 ALT60
      ALT107        ALT137

AC06 + RC06 RHHH
NEO_A ALT104      ALT134      ALT36 questiondown Greek_delta Greek_DELTA 0x101D451 0x101D437 ALT164 ALT194
NEO_A Cyrillic_de Cyrillic_DE ALT36 questiondown Greek_delta Greek_DELTA 0x101D521 0x101D507 ALT164 ALT194
NEO_A Greek_delta Greek_DELTA ALT36 questiondown Greek_delta Greek_DELTA 0x101D6FF 0x101D6E5 ALT164 ALT194
      ALT108      ALT138

AC07 + KP4 RJJJ
NEO_A ALT120      ALT150      ALT37 ALT11 Greek_tau partialderivative 0x101D461 0x101D447 ALT180 ALT210 ALT74
NEO_A Cyrillic_te Cyrillic_TE ALT37 ALT11 Greek_tau partialderivative 0x101D531 0x101D517 ALT180 ALT210 ALT74
NEO_A Greek_tau   Greek_TAU   ALT37 ALT11 Greek_tau partialderivative 0x101D70F 0x101D6F5 ALT180 ALT210 ALT74
      ALT110      ALT140

AC08 + KP5 RKKK
NEO_A ALT118      ALT148      ALT38 ALT12 Greek_rho 0x100211D 0x101D45F 0x101D445 ALT178 ALT208 ALT75
NEO_A Cyrillic_er Cyrillic_ER ALT38 ALT12 Greek_rho 0x100211D 0x101D52F 0x100211C ALT178 ALT208 ALT75
NEO_A Greek_rho   Greek_RHO   ALT38 ALT12 Greek_rho 0x100211D 0x101D70C 0x101D6F2 ALT178 ALT208 ALT75
      ALT111      ALT141

AC09 + KP6 RLLL
NEO_A ALT114      ALT144      ALT39 ALT13 Greek_nu 0x1002115 0x101D45B 0x101D441 ALT174 ALT204 ALT76
NEO_A Cyrillic_en Cyrillic_EN ALT39 ALT13 Greek_nu 0x1002115 0x101D52B 0x101D511 ALT174 ALT204 ALT76
NEO_A Greek_nu    Greek_NU    ALT39 ALT13 Greek_nu 0x1002115 0x101D708 0x101D6EE ALT174 ALT204 ALT76
      ALT112      ALT142

AC10 + KPDL RB10
NEO_A   ALT119      ALT149      ALT40 ALT17 Greek_sigma Greek_SIGMA 0x101D460 0x101D446 ALT179 ALT209 ALT21
NEO_A   Cyrillic_es Cyrillic_ES ALT40 ALT17 Greek_sigma Greek_SIGMA 0x101D530 0x101D516 ALT179 ALT209 ALT21
NEO_A   Greek_sigma Greek_SIGMA ALT40 ALT17 Greek_sigma Greek_SIGMA 0x101D70E 0x101D6F4 ALT179 ALT209 ALT21
NEO_N   ALT51       ALT40
NEO_TAB ALT128      eacute
NEO_A   ALT128      ALT158

AC11 + AD04 RB09
NEO_A   ALT130                ALT160        ALT41 ALT19 Greek_finalsmallsigma 0x1002218 NoSymbol  NoSymbol ALT190 ALT220 ALT19
NEO_A   Macedonia_dse         Macedonia_DSE ALT41 ALT19 Greek_finalsmallsigma 0x1002218 NoSymbol  NoSymbol ALT190 ALT220 ALT19
NEO_A   Greek_finalsmallsigma NoSymbol      ALT41 ALT19 Greek_finalsmallsigma 0x1002218 0x101D70D NoSymbol ALT190 ALT220 ALT19
        ALT50                 ALT49
NEO_TAB ALT127                agrave        ALT33
        ALT127                ALT157

BKSL - - RC01
NEO_MOD3 ISO_Last_Group ISO_Level2_Latch ISO_Next_Group ISO_Group_Latch
NEO_MOD3 ISO_Last_Group ISO_Level2_Latch ISO_Next_Group ISO_Group_Latch
NEO_MOD3 ISO_Last_Group ISO_Level2_Latch ISO_Next_Group ISO_Group_Latch
         ALT31          ALT44
NEO_TAB  ALT43          sterling         ALT34
         ALT42 ALT50

LFSH -
NEO_SHIFT Shift_L Caps_Lock ISO_Level3_Lock ISO_Group_Lock
NEO_SHIFT Shift_L Caps_Lock ISO_Level3_Lock ISO_Group_Lock
NEO_SHIFT Shift_L Caps_Lock ISO_Level3_Lock ISO_Group_Lock
          Shift_L

LSGT -
NEO_MOD4 ISO_Level3_Shift ISO_Prev_Group Num_Lock ISO_Level3_Latch
NEO_MOD4 ISO_Level3_Shift ISO_Prev_Group Num_Lock ISO_Level3_Latch
NEO_MOD4 ISO_Level3_Shift ISO_Prev_Group Num_Lock ISO_Level3_Latch
         Shift_L
NEO_TAB  ALT27            ALT28          ALT31
NEO_TAB  ALT27            ALT28          ALT44

AB01 + ESC RZZZ
NEO_A ALT124       ALT154       ALT42 ALT52 Greek_xi Greek_XI 0x101D465 0x101D44B ALT184 ALT214 ALT52
NEO_A Cyrillic_che Cyrillic_CHE ALT42 ALT52 Greek_xi Greek_XI 0x101D535 0x101D51B ALT184 ALT214 ALT52
NEO_A Greek_xi     Greek_XI     ALT42 ALT52 Greek_xi Greek_XI 0x101D709 0x101D6EF ALT184 ALT214 ALT52
      ALT126       ALT156
      ALT125       ALT155

AB02 + TAB RXXX
NEO_A ALT125            ALT155            ALT43 ALT0 Greek_upsilon nabla 0x101D466 0x101D44C ALT185 ALT215 ALT1
NEO_A Cyrillic_softsign Cyrillic_SOFTSIGN ALT43 ALT0 Greek_upsilon nabla 0x101D536 0x101D51C ALT185 ALT215 ALT1
NEO_A Greek_upsilon     Greek_UPSILON     ALT43 ALT0 Greek_upsilon nabla 0x101D710 0x101D6F6 ALT185 ALT215 ALT1
      ALT124            ALT154

AB03 + INS RCCC
NEO_A ALT128      ALT158      ALT44 ALT53 0x10003F5 intersection NoSymbol NoSymbol ALT188 ALT218 ALT53
NEO_A Ukrainian_i Ukrainian_I ALT44 ALT53 0x10003F5 intersection NoSymbol NoSymbol ALT188 ALT218 ALT53
NEO_A 0x10003DF   0x10003DE   ALT44 ALT53 0x10003F5 intersection NoSymbol NoSymbol ALT188 ALT218 ALT53
      ALT103      ALT133

AB04 + RTRN RVVV
NEO_N ALT68  endash ALT45 ALT54 0x10003F1 0x10021D2 ALT68     NoSymbol  ALT83 ALT84 ALT54
NEO_N ALT68  endash ALT45 ALT54 0x10003F1 0x10021D2 ALT68     NoSymbol  ALT83 ALT84 ALT54
NEO_N ALT68  endash ALT45 ALT54 0x10003F1 0x10021D2 0x101D71A 0x101D715 ALT83 ALT84 ALT54
      ALT122 ALT152

AB05 + UNDO RBBB
NEO_A ALT117       ALT147       ALT46 ALT55 0x10003D5 0x100211A 0x101D45E 0x101D444 ALT177 ALT207 ALT55
NEO_A Cyrillic_zhe Cyrillic_ZHE ALT46 ALT55 0x10003D5 0x100211A 0x101D52E 0x101D514 ALT177 ALT207 ALT55
NEO_A 0x10003D9    0x10003D8    ALT46 ALT55 0x10003D5 0x100211A NoSymbol  NoSymbol  ALT177 ALT207 ALT55
      ALT102       ALT132

AB06 + RB06 RNNN
NEO_A ALT102      ALT132      ALT47 ALT40 Greek_beta 0x10021D0 0x101D44F 0x101D435 ALT162 ALT192
NEO_A Cyrillic_be Cyrillic_BE ALT47 ALT40 Greek_beta 0x10021D0 0x101D51F 0x101D505 ALT162 ALT192
NEO_A Greek_beta  Greek_BETA  ALT47 ALT40 Greek_beta 0x10021D0 0x101D6FD 0x101D6E3 ALT162 ALT192
      ALT114      ALT144

AB07 + KP1 RMMM
NEO_A   ALT116      ALT146      ALT48     ALT8 Greek_pi Greek_PI 0x101D45D 0x101D443 ALT176 ALT206 ALT71
NEO_A   Cyrillic_pe Cyrillic_PE ALT48     ALT8 Greek_pi Greek_PI 0x101D52D 0x101D513 ALT176 ALT206 ALT71
NEO_A   Greek_pi    Greek_PI    ALT48     ALT8 Greek_pi Greek_PI 0x101D70B 0x101D6F1 ALT176 ALT206 ALT71
        ALT113      ALT143
        ALT113      ALT143
NEO_TAB ALT113      ALT143      Greek_mu

AB08 + KP2 RCOM
NEO_A ALT123       ALT153       ALT49 ALT9 Greek_omega Greek_OMEGA 0x101D464 0x101D44A ALT183 ALT213 ALT72
NEO_A Cyrillic_sha Cyrillic_SHA ALT49 ALT9 Greek_omega Greek_OMEGA 0x101D534 0x101D51A ALT183 ALT213 ALT72
NEO_A Greek_omega  Greek_OMEGA  ALT49 ALT9 Greek_omega Greek_OMEGA 0x101D714 0x101D6FA ALT183 ALT213 ALT72
      ALT68        ALT27
      ALT68        ALT51

AB09 + KP3 RPKT
NEO_A ALT113      ALT143      ALT50 ALT10 Greek_mu ifonlyif 0x101D45A 0x101D440 ALT173 ALT203 ALT73
NEO_A Cyrillic_em Cyrillic_EM ALT50 ALT10 Greek_mu ifonlyif 0x101D52A 0x101D510 ALT173 ALT203 ALT73
NEO_A Greek_mu    Greek_MU    ALT50 ALT10 Greek_mu ifonlyif 0x101D707 0x101D6ED ALT173 ALT203 ALT73
      ALT67       ALT28
      ALT67       ALT40

AB10 + RB10 RC02
NEO_A ALT126      ALT156      ALT51 ALT51 Greek_zeta 0x1002124 0x101D467 0x101D44D ALT186 ALT216
NEO_A Cyrillic_ze Cyrillic_ZE ALT51 ALT51 Greek_zeta 0x1002124 0x101D537 0x1002128 ALT186 ALT216
NEO_A Greek_zeta  Greek_ZETA  ALT51 ALT51 Greek_zeta 0x1002124 0x101D701 0x101D6E7 ALT186 ALT216
      ALT32       ALT36
      ALT39       ALT22

RTSH -
NEO_SHIFT Shift_R Caps_Lock ISO_Level3_Lock ISO_Group_Lock
NEO_SHIFT Shift_R Caps_Lock ISO_Level3_Lock ISO_Group_Lock
NEO_SHIFT Shift_R Caps_Lock ISO_Level3_Lock ISO_Group_Lock
          Shift_R

LCTL -
NEO_34 Control_L Control_L ALT80 Control_L
NEO_34 Control_L Control_L ALT80 Control_L
NEO_34 Control_L Control_L ALT80 Control_L
       Control_L

LWIN -
NEO_34 Super_L Super_L ALT81 Super_L
NEO_34 Super_L Super_L ALT81 Super_L
NEO_34 Super_L Super_L ALT81 Super_L
       Super_L

LALT -
NEO_34 Alt_L Meta_L ALT82 Meta_L
NEO_34 Alt_L Meta_L ALT82 Meta_L
NEO_34 Alt_L Meta_L ALT82 Meta_L
       Alt_L Meta_L 

SPCE + KP0
NEO_SPACE space space space ALT7 nobreakspace 0x100202F NoSymbol NoSymbol space space ALT70
NEO_SPACE space space space ALT7 nobreakspace 0x100202F NoSymbol NoSymbol space space ALT70
NEO_SPACE space space space ALT7 nobreakspace 0x100202F NoSymbol NoSymbol space space ALT70
          space

RALT -
NEO_MOD4 ISO_First_Group ISO_Prev_Group Num_Lock ISO_Level3_Latch
NEO_MOD4 ISO_First_Group ISO_Prev_Group Num_Lock ISO_Level3_Latch
NEO_MOD4 ISO_First_Group ISO_Prev_Group Num_Lock ISO_Level3_Latch
         Alt_R           Meta_R
         ISO_Last_Group

RWIN -
Super_R

SCLK - - - gruppenweise
NEO_6 Overlay2_Enable      ISO_Next_Group_Lock  ISO_Last_Group_Lock  ISO_Prev_Group_Lock  ISO_Level2_Latch Shift_Lock ISO_Level2_Latch
NEO_6 ISO_First_Group_Lock ISO_First_Group_Lock ISO_First_Group_Lock ISO_First_Group_Lock ISO_Level2_Latch Shift_Lock ISO_Level2_Latch
NEO_6 ISO_First_Group_Lock ISO_First_Group_Lock ISO_First_Group_Lock ISO_First_Group_Lock ISO_Level2_Latch Shift_Lock ISO_Level2_Latch
NEO_6 ISO_First_Group_Lock ISO_First_Group_Lock ISO_First_Group_Lock ISO_First_Group_Lock ISO_Level2_Latch Shift_Lock ISO_Level2_Latch

NMLK + RNML BKSL
NEO_N ALT0     ALT1               ALT29 notequal 0x1002248 identical NoSymbol NoSymbol ALT0 ALT1 Pointer_EnableKeys
NEO_N ALT0     ALT1               ALT29 notequal 0x1002248 identical NoSymbol NoSymbol ALT0 ALT1 Pointer_EnableKeys
NEO_N ALT0     ALT1               ALT29 notequal 0x1002248 identical NoSymbol NoSymbol ALT0 ALT1 Pointer_EnableKeys
      Num_Lock Pointer_EnableKeys

KPDV + RKDV
NEO_SPACE KP_Divide KP_Divide division 0x1002044 0x1002300 0x1002223 NoSymbol NoSymbol KP_Divide KP_Divide 0x1002044
NEO_SPACE KP_Divide KP_Divide division 0x1002044 0x1002300 0x1002223 NoSymbol NoSymbol KP_Divide KP_Divide 0x1002044
NEO_SPACE KP_Divide KP_Divide division 0x1002044 0x1002300 0x1002223 NoSymbol NoSymbol KP_Divide KP_Divide 0x1002044
          KP_Divide

KPMU + RKMU
NEO_SPACE KP_Multiply KP_Multiply 0x1002219 multiply 0x1002299 0x1002297 NoSymbol NoSymbol KP_Multiply KP_Multiply multiply
NEO_SPACE KP_Multiply KP_Multiply 0x1002219 multiply 0x1002299 0x1002297 NoSymbol NoSymbol KP_Multiply KP_Multiply multiply
NEO_SPACE KP_Multiply KP_Multiply 0x1002219 multiply 0x1002299 0x1002297 NoSymbol NoSymbol KP_Multiply KP_Multiply multiply
          KP_Multiply

KPSU + RKSU
NEO_SPACE KP_Subtract KP_Subtract 0x1002212 0x1002216 0x1002296 0x1002238 NoSymbol NoSymbol KP_Subtract KP_Subtract 0x1002216
NEO_SPACE KP_Subtract KP_Subtract 0x1002212 0x1002216 0x1002296 0x1002238 NoSymbol NoSymbol KP_Subtract KP_Subtract 0x1002216
NEO_SPACE KP_Subtract KP_Subtract 0x1002212 0x1002216 0x1002296 0x1002238 NoSymbol NoSymbol KP_Subtract KP_Subtract 0x1002216
          KP_Subtract

KP7 + RKP7
NEO_N  KP_7 0x1002714 0x1002195 KP_Home 0x100226A upstile NoSymbol NoSymbol KP_7 0x1002714 KP_Home
NEO_N  KP_7 0x1002714 0x1002195 KP_Home 0x100226A upstile NoSymbol NoSymbol KP_7 0x1002714 KP_Home
NEO_N  KP_7 0x1002714 0x1002195 KP_Home 0x100226A upstile NoSymbol NoSymbol KP_7 0x1002714 KP_Home
KEYPAD KP_7 KP_Home

KP8 + RKP8
NEO_N  KP_8 0x1002718 uparrow KP_Up intersection 0x10022C2 NoSymbol NoSymbol KP_8 0x1002718 KP_Up
NEO_N  KP_8 0x1002718 uparrow KP_Up intersection 0x10022C2 NoSymbol NoSymbol KP_8 0x1002718 KP_Up
NEO_N  KP_8 0x1002718 uparrow KP_Up intersection 0x10022C2 NoSymbol NoSymbol KP_8 0x1002718 KP_Up
KEYPAD KP_8 KP_Up

KP9 + RKP9
NEO_N  KP_9 dagger   0x10020D7 KP_Prior 0x100226B 0x1002309 NoSymbol NoSymbol KP_9 dagger KP_Prior
NEO_N  KP_9 dagger   0x10020D7 KP_Prior 0x100226B 0x1002309 NoSymbol NoSymbol KP_9 dagger KP_Prior
NEO_N  KP_9 dagger   0x10020D7 KP_Prior 0x100226B 0x1002309 NoSymbol NoSymbol KP_9 dagger KP_Prior
KEYPAD KP_9 KP_Prior

KP4 + RKP4
NEO_N  KP_4 club    leftarrow KP_Left includedin 0x1002286 NoSymbol NoSymbol KP_4 club KP_Left
NEO_N  KP_4 club    leftarrow KP_Left includedin 0x1002286 NoSymbol NoSymbol KP_4 club KP_Left
NEO_N  KP_4 club    leftarrow KP_Left includedin 0x1002286 NoSymbol NoSymbol KP_4 club KP_Left
KEYPAD KP_4 KP_Left

KP5 + RKP5
NEO_N  KP_5 0x20AC   ALT40 KP_Begin 0x10022B6 0x10022B7 NoSymbol NoSymbol KP_5 0x20AC KP_Begin
NEO_N  KP_5 0x20AC   ALT40 KP_Begin 0x10022B6 0x10022B7 NoSymbol NoSymbol KP_5 0x20AC KP_Begin
NEO_N  KP_5 0x20AC   ALT40 KP_Begin 0x10022B6 0x10022B7 NoSymbol NoSymbol KP_5 0x20AC KP_Begin
KEYPAD KP_5 KP_Begin

KP6 + RKP6
NEO_N  KP_6 0x1002023 rightarrow KP_Right includes 0x1002287 NoSymbol NoSymbol KP_6 0x1002023 KP_Right
NEO_N  KP_6 0x1002023 rightarrow KP_Right includes 0x1002287 NoSymbol NoSymbol KP_6 0x1002023 KP_Right
NEO_N  KP_6 0x1002023 rightarrow KP_Right includes 0x1002287 NoSymbol NoSymbol KP_6 0x1002023 KP_Right
KEYPAD KP_6 KP_Right

KPAD + RKAD
NEO_SPACE KP_Add KP_Add plusminus 0x1002213 0x1002295 0x1002214 NoSymbol NoSymbol KP_Add KP_Add 0x1002213
NEO_SPACE KP_Add KP_Add plusminus 0x1002213 0x1002295 0x1002214 NoSymbol NoSymbol KP_Add KP_Add 0x1002213
NEO_SPACE KP_Add KP_Add plusminus 0x1002213 0x1002295 0x1002214 NoSymbol NoSymbol KP_Add KP_Add 0x1002213
          KP_Add

KP1 + RKP1
NEO_N  KP_1 diamond 0x1002194 KP_End lessthanequal downstile NoSymbol NoSymbol KP_1 diamond KP_End
NEO_N  KP_1 diamond 0x1002194 KP_End lessthanequal downstile NoSymbol NoSymbol KP_1 diamond KP_End
NEO_N  KP_1 diamond 0x1002194 KP_End lessthanequal downstile NoSymbol NoSymbol KP_1 diamond KP_End
KEYPAD KP_1 KP_End

KP2 + RKP2
NEO_N  KP_2 heart downarrow KP_Down union 0x10022C3 NoSymbol NoSymbol KP_2 heart KP_Down
NEO_N  KP_2 heart downarrow KP_Down union 0x10022C3 NoSymbol NoSymbol KP_2 heart KP_Down
NEO_N  KP_2 heart downarrow KP_Down union 0x10022C3 NoSymbol NoSymbol KP_2 heart KP_Down
KEYPAD KP_2 KP_Down

KP3 + RKP3
NEO_N  KP_3 0x1002660 0x10021CC KP_Next greaterthanequal 0x100230B NoSymbol NoSymbol KP_3 0x1002660 KP_Next
NEO_N  KP_3 0x1002660 0x10021CC KP_Next greaterthanequal 0x100230B NoSymbol NoSymbol KP_3 0x1002660 KP_Next
NEO_N  KP_3 0x1002660 0x10021CC KP_Next greaterthanequal 0x100230B NoSymbol NoSymbol KP_3 0x1002660 KP_Next
KEYPAD KP_3 KP_Next

KP0 + RKP0
NEO_N  KP_0 0x1002423 ALT48 KP_Insert 0x1002030 0x10025A1 NoSymbol NoSymbol KP_0 0x1002423 KP_Insert
NEO_N  KP_0 0x1002423 ALT48 KP_Insert 0x1002030 0x10025A1 NoSymbol NoSymbol KP_0 0x1002423 KP_Insert
NEO_N  KP_0 0x1002423 ALT48 KP_Insert 0x1002030 0x10025A1 NoSymbol NoSymbol KP_0 0x1002423 KP_Insert
KEYPAD KP_0 KP_Insert

KPDL + RKDL
NEO_N  ALT20        ALT21 ALT19 KP_Delete minutes seconds NoSymbol NoSymbol ALT20 ALT21 KP_Delete
NEO_N  ALT20        ALT21 ALT19 KP_Delete minutes seconds NoSymbol NoSymbol ALT20 ALT21 KP_Delete
NEO_N  ALT20        ALT21 ALT19 KP_Delete minutes seconds NoSymbol NoSymbol ALT20 ALT21 KP_Delete
KEYPAD KP_Decimal   KP_Delete
KEYPAD KP_Decimal   KP_Delete
KEYPAD KP_Separator KP_Delete

KPEN
KP_Enter

EOF

    [ -n "$ZJVARIANTE" ] && parse_belegungen <<EOF
AD10 + KPAD
NEO_A ALT126      ALT156      ALT30 ALT2 Greek_zeta 0x1002124 0x101D467 0x101D44D ALT170 ALT299 ALT2
NEO_A Cyrillic_ze Cyrillic_ZE ALT30 ALT2 Greek_zeta 0x1002124 0x101D537 0x1002128 ALT170 ALT299 ALT2
NEO_A Greek_zeta  Greek_ZETA  ALT30 ALT2 Greek_zeta 0x1002124 0x101D701 0x101D6E7 ALT170 ALT299 ALT2
      ALT116      ALT146

AB10 + RB10
NEO_A ALT110      ALT140      ALT51 ALT51 Greek_theta Greek_THETA 0x101D457 0x101D43D ALT186 ALT216
NEO_A Cyrillic_je Cyrillic_JE ALT51 ALT51 Greek_theta Greek_THETA 0x101D527 0x101D50D ALT186 ALT216
NEO_A Greek_theta Greek_THETA ALT51 ALT51 Greek_theta Greek_THETA 0x101D703 0x101D6E9 ALT186 ALT216
      ALT32       ALT36
      ALT39       ALT22

EOF

    [ -n "$NOTBELEGUNG" ] && parse_belegungen <<EOF
SCLK
NoSymbol

RTLD -
NEO_TAB dead_abovedot Pointer_EnableKeys 0xfe60

R001
NEO_NOT ordfeminine notsign

R002
NEO_NOT masculine logicalor

R003
NEO_NOT numerosign logicaland

R005
NEO_NOT periodcentered 0x1002221

R006
NEO_NOT sterling 0x1002225

R007
NEO_NOT currency rightarrow

R012 -
NEO_NOT dead_diaeresis dead_macron

RD06
NEO_NOT exclamdown radical

RD12 -
NEO_TAB dead_doubleacute Codeinput dead_breve

RC06
NEO_NOT questiondown Greek_DELTA

RB06
NEO_NOT ALT40 0x10021D0

RB10
NEO_NOT ALT51 0x1002124

RNML
NEO_TAB notequal Pointer_EnableKeys identical

RKDV
NEO_NOT 0x1002044 0x1002223

RKMU
NEO_NOT multiply 0x1002297

RKSU
NEO_NOT 0x1002216 0x1002238

RKP7
NEO_NOT KP_Home upstile

RKP8
NEO_NOT KP_Up 0x10022C2

RKP9
NEO_NOT KP_Prior 0x1002309

RKP4
NEO_NOT KP_Left 0x1002286

RKP5
NEO_NOT KP_Begin 0x10022B7

RKP6
NEO_NOT KP_Right 0x1002287

RKAD
NEO_NOT 0x1002213 0x1002214

RKP1
NEO_NOT KP_End downstile

RKP2
NEO_NOT KP_Down 0x10022C3

RKP3
NEO_NOT KP_Next 0x100230B

RKP0
NEO_NOT KP_Insert 0x10025A1

RKDL
NEO_NOT KP_Delete seconds

EOF


    [ -z "$STEUERDIREKT" -o -n "$NOTBELEGUNG" ] && parse_belegungen <<EOF
UNDO
Undo

BEGI
Begin

EOF

    [ -z "$SZDIREKT" ] && parse_belegungen <<EOF
RD03
bracketleft braceleft

RD04
bracketright braceright

RD09
equal plus

RC01
backslash bar

RC02
slash question

RC09
minus underscore

RB05
grave asciitilde

RB09
apostrophe quotedbl

RB10
semicolon colon

RPKT
period greater

RCOM
comma less

R000
0 parenright

R111
1 exclam

R222
2 at

R333
3 numbersign

R444
4 dollar

R555
5 percent

R666
6 asciicircum

R777
7 ampersand

R888
8 asterisk

R999
9 parenleft

EOF

    [ -z "$BUCHSTABENDIREKT" ] && parse_belegungen <<EOF
RAAA
ALPHABETIC a A

RBBB
ALPHABETIC b B

RCCC
ALPHABETIC c C

RDDD
ALPHABETIC d D

REEE
ALPHABETIC e E

RFFF
ALPHABETIC f F

RGGG
ALPHABETIC g G

RHHH
ALPHABETIC h H

RIII
ALPHABETIC i I

RJJJ
ALPHABETIC j J

RKKK
ALPHABETIC k K

RLLL
ALPHABETIC l L

RMMM
ALPHABETIC m M

RNNN
ALPHABETIC n N

ROOO
ALPHABETIC o O

RPPP
ALPHABETIC p P

RQQQ
ALPHABETIC q Q

RRRR
ALPHABETIC r R

RSSS
ALPHABETIC s S

RTTT
ALPHABETIC t T

RUUU
ALPHABETIC u U

RVVV
ALPHABETIC v V

RWWW
ALPHABETIC w W

RXXX
ALPHABETIC x X

RYYY
ALPHABETIC y Y

RZZZ
ALPHABETIC z Z

RUAE
ALPHABETIC adiaeresis Adiaeresis

RUOE
ALPHABETIC odiaeresis Odiaeresis

RUUE
ALPHABETIC udiaeresis Udiaeresis

RUSS
ALPHABETIC ssharp 0x1001E9E

EOF

}

schreibe_modmap () {
    cat <<EOF
modifier_map Control { Control_R, Control_L };
modifier_map Shift   { Shift_R, Shift_L };
modifier_map Mod1    { Meta_R, Meta_L, Alt_R, Alt_L };
modifier_map Mod3    { <KP5>, <NMLK> };
modifier_map Mod4    { Super_R, Super_L };
EOF
}

fehler () {
    echo "Fehler: $@" >&2
    [ -n "$TMPFILE" ] && rm -f $TMPFILE
    exit 1
}

teste_lesbarkeit () {
    [ -r "$1" ] || fehler "File $1 ist nicht lesbar."
}

bereinige_keyname () {
    typeset norm
    case $1 in
	VOL+) norm=VOLp ;;
	VOL-) norm=VOLm ;;
	*) norm=$1 ;;
    esac
    echo $norm
}

taste_ebene () {
    typeset symbole='' typ='ONE_LEVEL' trenn='' zwei=2 actions symbol umschalt filter='xxxxxxxxoox' tmp eins args

    actions=
    if [[ $1 = \! ]]; then
	shift
	actions=' '
	zwei=4
    fi
    if [ $# = $zwei ]; then
	typ=TWO_LEVEL
    elif  [ $# -gt $zwei ]; then
	typ="$1"
	shift
    fi

    args="$@"
    if [ -n "$NOTBELEGUNG" ]; then
	if [[ $NOTBELEGUNG = 12 ]]; then
	    filter='xxooooooooo'
	    case $typ in
		NEO_A)
		    typ=ALPHABETIC
		    ;;
		NEO_N | NEO_TAB)
		    typ=TWO_LEVEL
		    ;;
		NEO_SPACE | NEO_NOT)
		    typ=ONE_LEVEL
		    filter='xoooooooooo'
		    ;;
		NEO_MOD3)
		    typ=ONE_LEVEL
		    args=ISO_Next_Group
		    ;;
		NEO_MOD4)
		    typ=ONE_LEVEL
		    args=ISO_Prev_Group
		    ;;
	    esac
	else
	    case $typ in
		NEO_A | NEO_N | NEO_SPACE)
		    typ=NEO_3
		    filter='ooxoxxooooo'
		    ;;
		NEO_TAB)
		    typ=TWO_LEVEL
		    filter='ooxxooooooo'
		    ;;
		NEO_NOT)
		    typ=ONE_LEVEL
		    filter='oxooooooooo'
		    ;;
		NEO_MOD3)
		    typ=ONE_LEVEL
		    args=NoSymbol
		    ;;
		NEO_MOD4)
		    typ=ONE_LEVEL
		    args=ISO_Level3_Shift
		    ;;
	    esac
	fi
	case $typ in
	    NEO_34)
		typ=ONE_LEVEL
		filter='xoooooooooo'
		;;
	    NEO_SHIFT)
		if [[ $args = *Shift_R* ]]; then
		    args='Shift_R Caps_Lock'
		else
		    args='Shift_L Caps_Lock'
		fi
		;;
	esac
    elif [ -n "$CTRLALTEXTRA" ]; then
	filter='xxxxxxxxxxx'
	case $typ in
	    NEO_A)
		typ=NEO_N
		;;
	esac
    elif [ -z "$BUCHSTABENDIREKT" ]; then
	case $typ in
	    NEO_A)
		typ=NEO_N
		;;
	esac
    fi

    umschalt="$actions"
    for symbol in $args; do
	tmp=${filter#[xo]}
	eins=${filter%${tmp}}
	if [ -n "$umschalt" ]; then
	    if [[ $eins = x ]]; then
		if [[ $symbol = \<*\> ]]; then
		    symbol="${symbol#\<}"
		    symbol=$(bereinige_keyname "${symbol%\>}")
		    eval "symbol=\$KEYCODE_$symbol"
		    actions="$actions${trenn}Message(data[0]=$symbol, data[1]=0, report=all)"
		else
		    actions="$actions$trenn$symbol"
		fi
	    fi
	    umschalt=
	else
	    if [[ $eins = x ]]; then
		[[ -z $XF86 && $symbol = XF86* ]] && symbol=NoSymbol
		[[ $symbol = ALT* ]] && symbol=${ALTERNATIVE[${symbol#ALT}]}
		symbole="$symbole$trenn$symbol"
		trenn=', '
	    fi
	    filter=$tmp
	    umschalt="$actions"
	fi
    done

    [ "$actions" != "$umschalt" ] && fehler "Symbole und Actions müssen paarweise angegben werden."

    [ -n "$symbole" ] || return
    TYP[0]=$typ
    SYMBOLE[0]="$symbole"
    ACTIONS[0]=
    [ -n "$actions" ] && ACTIONS[0]="$actions"
}

kopiere_taste_ebene () {
    BELEGT[$1]=ja
    TYP[4*$1+$2]=${TYP[0]}
    SYMBOLE[4*$1+$2]="${SYMBOLE[0]}"
    ACTIONS[4*$1+$2]="${ACTIONS[0]}"
}

parse_layouts () {
    typeset j=0 f1 f1alt ebene kopie
    while read f1; do
	[ -z "$f1" ] && break
	[[ $f1 = \#* ]] && continue

	f1alt="$f1"
	taste_ebene $f1

	if [ -n "$2" ]; then
	    ebene=$j
	    [ $((j=j+1)) -le ${#BELEGUNG[*]} ] || ebene=
	else
	    ebene=${BELEGUNG[j=j+1]}
	fi
	if [ -n "$ebene" ]; then
	    kopiere_taste_ebene $1 $ebene
	    # Für die Notbelegung benutzen wir die höheren Ebenen des primären
	    # Layouts.
	    if [ -n "$NOTBELEGUNG" -a $ebene -eq 0 ]; then
		NOTBELEGUNG=34
		taste_ebene $f1
		kopiere_taste_ebene $1 1
		NOTBELEGUNG=12
	    fi
	fi
    done

    # Das Ende einer Tastendefinition ist erreicht.  Falls keine
    # Belegung definiert wurde markiere diese Taste als unverändert.
    if [ $j -eq 0 ]; then
	REPEAT[$1]=
    else
 	# Falls diese Taste weniger Layouts spezifiziert als maximal
	# erlaubt wird die letzte Gruppe wiederholt.
	while [ $j -lt ${#LAYOUTNAME[*]} ]; do
	    taste_ebene $f1alt

	    if [ -n "$2" ]; then
		kopie=$j
		[ $((j=j+1)) -le ${#BELEGUNG[*]} ] || return
	    else
		kopie=${BELEGUNG[j=j+1]}
	    fi
	    if [ -n "$kopie" ]; then
		kopiere_taste_ebene $1 $kopie
		if [ -n "$NOTBELEGUNG" -a $kopie -eq 0 ]; then
		    NOTBELEGUNG=34
		    taste_ebene $f1alt
		    kopiere_taste_ebene $1 1
		    NOTBELEGUNG=12
		fi
	    fi
	done
    fi
}

suche_freien_keycode () {
    typeset j="$2"
    while [ $((j=j+1)) -le 255 ]; do
	if [ -z "${KEYNAME[j]}" ]; then
 	    EXTRAKEY[$j]="$1"
	    KEYNAME[$j]="$1"
	    eval "KEYCODE_$1=$j"
	    [ $j -gt $MAXIMUM ] && MAXIMUM=$j
	    return $j
	elif [ -z "${BELEGT[j]}" ]; then
	    EXTRAALIAS[$j]="$1"
	    return $j
	fi
    done
    if [ $MINIMUM -gt 8 ]; then 
	let MINIMUM--
 	EXTRAKEY[$MINIMUM]="$1"
	KEYNAME[$MINIMUM]="$1"
	eval "KEYCODE_$1=$MINIMUM"
	return $MINIMUM
    fi
    fehler "Kann $1 keine Taste zuordnen."
}

parse_belegungen () {
    typeset f1 f2 f3 f4 f5 keycode gruppenweise letzte=$((MINIMUM-1))
    export REPEAT OVERLAY1 OVERLAY2 SYMBOLE ACTIONS TYP EXTRAKEY EXTRAALIAS

    while read f1 f2 f3 f4 f5; do
	[[ -z $f1 || $f1 = \#* ]] && continue
	eval "keycode=\$KEYCODE_$f1"
	if [ -z "$keycode" ]; then
	    suche_freien_keycode "$f1" $letzte
	    keycode=$?
	    letzte=$keycode
	fi

	REPEAT[$keycode]=ja
	[[ $f2 = - ]] && REPEAT[$keycode]=nein

	OVERLAY1[$keycode]='-'
	OVERLAY2[$keycode]='-'
	[ -n "$f3" ] && OVERLAY1[$keycode]="$f3"
	[ -n "$f4" ] && OVERLAY2[$keycode]="$f4"

	gruppenweise=
	[[ $f5 = gruppenweise ]] && gruppenweise=ja

	parse_layouts $keycode $gruppenweise
    done
}

lies_keycodes () {
    typeset aname desemi linkeseite keysym keycode f1 f2 f3 f4
    export MINIMUM=8 MAXIMUM=255 KEYNAME REPEAT

    while read f1 f2; do
	[[ $f1 = xkb_keycodes ]] && break
    done

    while read f1 f2 f3 f4; do
	if [[ $f1 = \<*\> ]]; then
	    f1="${f1#\<}";  keysym=$(bereinige_keyname "${f1%\>}")
	    keycode="${f3%;}"
	    KEYNAME[$keycode]=$keysym
	    eval "export KEYCODE_$keysym=$keycode"
	elif [[ $f1 = alias ]]; then
	    f2="${f2#\<}";   aname=$(bereinige_keyname "${f2%\>}")
	    f4="${f4#\<}";  keysym=$(bereinige_keyname "${f4%\>;}")
	    eval "keycode=\$KEYCODE_$keysym"
	    [ -n "$keycode" ] && eval "export KEYCODE_$aname=$keycode"
	elif [[ $f1 = minimum ]]; then
	    MINIMUM=${f3%;}
	elif [[ $f1 = maximum ]]; then
	    MAXIMUM=${f3%;}
	elif [[ $f1 = }\; ]]; then
            break
	fi
    done
}

lies_symbols () {
    typeset f1 f2 f3 keycode
    export BELEGT

    while read f1 f2; do
	[[ $f1 = xkb_symbols ]] && break
    done

    while read f1 f2 f3; do
	[[ $f1 = key ]] || continue
	f2="${f2#\<}";	f2=$(bereinige_keyname "${f2%\>}");
	eval "keycode=\$KEYCODE_$f2"
	BELEGT[$keycode]=ja
    done
}

lies_orginalbelegung () {
    lies_keycodes
    lies_symbols
}

verbinde_keycodes () {
    typeset f1 aname keycode keysym

    while read f1; do
	[[ $f1 = xkb_keycodes* ]] && break
    done
    echo "$f1"
    while read f1; do
	if [[ $f1 = }\; ]]; then
	    # Neue Tastennamen einfügen
	    keycode=$((MINIMUM-1))
	    while [ $((keycode=keycode+1)) -le $MAXIMUM ]; do
		keysym="${EXTRAKEY[keycode]}"
		[ -n "$keysym" ] && echo "<$keysym> = $keycode;"

		aname="${EXTRAALIAS[keycode]}"
		[ -n "$aname" ] && echo "alias <$aname> = <${KEYNAME[keycode]}>;"
	    done

	    # Umschiffe ein merkwürdiges Problem auf IRIX: <UP> wird in
	    # Redirect nicht als gültiger Tastenname erkannt.
	    [ -n "$KEYCODE_NUP" ] || echo 'alias <NUP> = <UP>;'

	    echo "$f1"
	    break
	elif [[ $f1 = minimum* ]]; then
	    echo "minimum = $MINIMUM;"
	elif [[ $f1 = maximum* ]]; then
	    echo "maximum = $MAXIMUM;"
	else
	    echo "$f1"
	fi
    done
}

schreibe_taste () {
    # $1 ist der (numerische) keycode
    typeset trenn j
    export REPEAT_KEYCODES

    echo "key <${KEYNAME[$1]}> {"

    # Tasten behandeln, für die repeat explizit angeschaltet wurde
    if [ "${REPEAT[$1]}" = nein ]; then
	echo 'repeat=no,'
	REPEAT_KEYCODES="$REPEAT_KEYCODES $1"
    fi

    [ -n "$NOTBELEGUNG" -a "${OVERLAY1[$1]}" != '-' ] && echo "overlay1=<${OVERLAY1[$1]}>,"
    [ -n "$USUMSONST"   -a "${OVERLAY2[$1]}" != '-' ] && echo "overlay2=<${OVERLAY2[$1]}>,"

    # Die eigentliche Tastenbelegung ausgeben
    trenn=
    j=0
    while [ $((j=j+1)) -le 4 ]; do
	if [ -n "${SYMBOLE[4*$1+j-1]}" ]; then
	    echo "$trenn"
	    echo "type[group$j]=\"${TYP[4*$1+j-1]}\","
	    echo "symbols[group$j]=[ ${SYMBOLE[4*$1+j-1]} ]"
	    if [ -n "${ACTIONS[4*$1+j-1]}" ]; then
		echo ","
		echo "actions[group$j]=[ ${ACTIONS[4*$1+j-1]} ]"
	    fi
	    trenn=','
	fi
    done

    echo ' };'
}

verbinde_symbols () {
    typeset i keycode j keysym f1 f2 f3
    REPEAT_KEYCODES=

    while read f1; do
	[[ $f1 = xkb_symbols* ]] && break
    done
    echo "$f1"

    i=0
    while [ $((i=i+1)) -le ${#LAYOUTNAME[*]} ]; do
	j="${BELEGUNG[i]}"
	if [ -n "$j" ]; then
	    echo "name[group$((j+1))]=\"${LAYOUTNAME[$((i-1))]}\";"
	    [ -n "$NOTBELEGUNG" -a $j -eq 0 ] && echo 'name[group2]="Ebene 3 und 5";'
	fi
    done
    echo "key.repeat= True;"

    while read f1 f2 f3; do
	if [[ $f1 = key ]]; then
	    keysym="${f2#\<}"; keysym=$(bereinige_keyname "${keysym%\>}")
	    # Anfang einer Tastendefinition gefunden
	    eval "keycode=\$KEYCODE_$keysym"
	    # Anhand von repeat erkennen wir, ob wir diese Belegung
	    # überschreiben wollen
	    if [ -n "${REPEAT[keycode]}" ]; then
		# Orginalbelegung übergehen
		while [[ $f3 != *\; ]]; do
		     read f3
		done
		# Neue Belegung einfügen
		schreibe_taste $keycode
	    else
		# Die Belegung der Taste bleibt erhalten
		echo "$f1 $f2 $f3"
		while [[ $f3 != *\; ]]; do
		     read f3
		     echo "$f3"
		done
	    fi
	    # Wir markieren dies Taste als behandelt indem wir sie aus dem
	    # Array belegter keycodes entfernen
	    KEYNAME[$keycode]=
	elif [[ $f1 = }\; ]]; then
	    # Gib die verbleibenden Tastenbelegungen aus
	    i=$((MINIMUM-1))
	    while [ $((i=i+1)) -le $MAXIMUM ]; do
		[ -n "${KEYNAME[i]}" ] || continue
		[ -n "${REPEAT[i]}" ] && schreibe_taste $i
	    done

	    # Gib die Modmap aus
	    schreibe_modmap

	    echo '};'
	    break
        # Ursprüngliche Gruppennamen und Modmap werden verworfen
	elif [[ $f1 != name* && $f1 != modifier_map ]]; then
	    echo "$f1 $f2 $f3"
	fi
    done
}

rest_passieren_lassen () {
    typeset f1
    while read f1; do
	echo "$f1"
    done
}

schreibe_xset () {
    typeset kommentar='//   '
    if [ -n "$SKRIPT" ]; then
	kommentar=
    else
	echo '// Vorschlag für .xinitrc:'
	echo '//'
    fi
    echo "${kommentar}for i in${REPEAT_KEYCODES}; do"
    echo "${kommentar}    xset -r \$i"
    echo "${kommentar}done"
}

verbinde () {
    if [ -n "$SKRIPT" ]; then
	echo '#!/bin/ksh'
	echo "xkbcomp -w0 - ${DISPLAY:-:0}<<EOF"
    fi

    echo 'xkb_keymap {'
    verbinde_keycodes
    verbinde_types
    ersetze_compat
    verbinde_symbols
    rest_passieren_lassen  # geometry wird komplett durchgereicht.

    [ -n "$SKRIPT" ] && echo 'EOF'

    [ -n "$GUTESXSET" ] && schreibe_xset
}

gruppe_zu_layout () {
    typeset i=-1 rest="$1" tmp eins
    export BELEGUNG

    while [ -n "$rest" -a $((i=i+1)) -lt 4 ]; do
	tmp=${rest#[1-6]}
	eins=${rest%${tmp}}
	[ -n "$eins" ] || fehler 'Layouts werden durch Ziffern im Bereich 1-6 angegeben.'
	rest=$tmp
	BELEGUNG[$eins]=$i

	[ -n "$NOTBELEGUNG" -a $i -eq 0 ] && let i=i+1
    done
    [ -n "$rest" ] && fehler 'Maximal können vier Layouts angegeben werden.'
}

# Voreinstellungen
export SKRIPT GUTESXSET XF86 ORGINAL TMPFILE PUNKT COMPAT TYPES STEUERDIREKT KPDIREKT
export MAUSKP4 MAUSKP1 NOTBELEGUNG ZJVARIANTE CTRLALTEXTRA QWERTZCTRLALT XCVORIG
export USUMSONST
export SZDIREKT=ja BUCHSTABENDIREKT=ja CUAHACK=ja

layouts=1
zusatzbelegungen=

# Platformabhänigige Voreinstellungen
case $(uname) in
    AIX)
	;;
    IRIX*)
	GUTESXSET=ja
	;;
    SunOS)
	GUTESXSET=ja
	[ $(uname -p) = sparc ] || XF86=ja
	;;
    *)
	XF86=ja
	GUTESXSET=ja
	;;
esac

# Optionen abarbeiten
while [ $# -ne 0 ]; do
    case "$1" in
	-a)
	    shift
	    [ $# = 0 ] && fehler 'Nach Option -a muss ein Filename stehen.'
	    teste_lesbarkeit "$1"
	    AUSGANGSBELEGUNG="$1"
	    ;;
	-b)
	    shift
	    [ $# = 0 ] && fehler 'Nach Option -b muss ein Wort aus Ziffern 1-4 stehen.'
	    layouts=$1
	    ;;
	-bd)
	    BUCHSTABENDIREKT=
	    ;;
	-c)
	    shift
	    [ $# = 0 ] && fehler 'Nach Option -c muss ein Filename stehen.'
	    teste_lesbarkeit "$1"
	    COMPAT="$COMPAT $1"
	    ;;
	-cua)
	    CUAHACK=
	    ;;
	+cax)
	    CTRLALTEXTRA=ja
	    ;;
	-h)
	    hilfe
	    ;;
	+kpd)
	    KPDIREKT=ja
	    ;;
	+m1)
	    MAUSKP1=ja
	    ;;
	+m4)
	    MAUSKP4=ja
	    ;;
	-n)
	    NOTBELEGUNG=12
	    KPDIREKT=ja
	    ;;
	-p)
	    PUNKT=ja
	    ;;
	+qca)
	    QWERTZCTRLALT=ja
	    ;;
	-s)
	    SKRIPT=ja
	    ;;
	+std)
	    STEUERDIREKT=ja
	    ;;
	-szd)
	    SZDIREKT=
	    ;;
	-t)
	    shift
	    [ $# = 0 ] && fehler 'Nach Option -t muss ein Filename stehen.'
	    teste_lesbarkeit "$1"
	    TYPES="$TYPES $1"
	    ;;
        +xcv)
	    XCVORIG=ja
	    ;;
	+xf86)
	    XF86=ja
	    ;;
	-xf86)
	    XF86=
	    ;;
	-z)
	    shift
	    [ $# = 0 ] && fehler 'Nach Option -z muss ein Filename stehen.'
	    teste_lesbarkeit "$1"
	    zusatzbelegungen="$zusatzbelegungen $1"
	    ;;
	-zj)
	    ZJVARIANTE=ja
	    ;;
	*)
	    fehler "Unbekannte Option: $1"
    esac
    shift
done

# Ctrl/Alt-XCV wie bei QWERTZ ist Teil von Ctrl/Alt-QWERTZ; beides bedingt
# spezielle Ebenen für Ctrl/Alt, und diese Ebenen funktionieren nur gut, wenn
# man Redirect (für die Buchstaben) benutzt.
[ -n "$QWERTZCTRLALT" ] && XCVORIG=ja
[ -n "$XCVORIG" ] && CTRLALTEXTRA=ja
[ -n "$CTRLALTEXTRA" ] && BUCHSTABENDIREKT=

[ -z "$STEUERDIREKT" -a -z "$BUCHSTABENDIREKT" ] && USUMSONST=ja

if [ -z "$AUSGANGSBELEGUNG" ]; then
    type xkbcomp>/dev/null || fehler 'xkbcomp nicht gefunden'
    AUSGANGSBELEGUNG=.orginalbelegung.xkb
    [ -f $AUSGANGSBELEGUNG ] && fehler "File $AUSGANGSBELEGUNG existiert und wird nicht überschrieben"
    TMPFILE="$AUSGANGSBELEGUNG"
fi

# Zuordnung zwischen Layout und Gruppe berechnen.
gruppe_zu_layout "$layouts"

# Hole alle keycodes, finde heraus welche noch unbelegt oder namenlos
# sind.
[ -n "$TMPFILE" ] && xkbcomp ${DISPLAY:-:0} $TMPFILE
lies_orginalbelegung < $AUSGANGSBELEGUNG

# Lies die Belegungsinformation ein mit der die ursprüngliche
# überschrieben werden soll.
std_belegung
for i in $zusatzbelegungen; do
    parse_belegungen < "$i"
done

# Verbinde die bisherige Belegung mit der Überschreibenden zur neuen
# Belegung.
verbinde < $AUSGANGSBELEGUNG
[ -n "$TMPFILE" ] && rm -f $TMPFILE
