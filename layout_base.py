#!/usr/bin/env python3
# encoding: utf-8

"""Basic functions and constants for working with keyboard layouts."""

def read_file(path):
    """Get the data from a file.

    >>> read_file("testfile")[:2]
    'ui'
    """

    f = open(path, encoding="utf-8")
    data = f.read()
    f.close()
    return data

### get the config

# check if we got one via the commandline (and remove the argument if yes). Otherwise use the default.
from sys import argv
if "--config" in argv: 
    idx = argv.index("--config")
    # the config module is the file without the extension.
    cfg = argv[idx+1][:-3]
    # replace all / and \ with .
    cfg = cfg.replace("/", ".")
    cfg = cfg.replace("\\", ".")
    argv = argv[:idx] + argv[idx+2:]
    exec("from " + cfg + " import *")
else: 
    from config import *

### Constants

#: Die Layout-Datei für Neo = Tastenbelegung - Großbuchstaben integriert. 
NEO_LAYOUT = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("x", "X", "…", "⇞", "ξ", "Ξ"),("v", "V", "_", "⌫", "", "√"),("l", "L", "[", "⇡", "λ", "Λ"),
     ("c", "C", "]", "Entf", "χ", "ℂ"),("w", "W", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("h", "H", "<", "7", "ψ", "Ψ"),
     ("g", "G", ">", "8", "γ", "Γ"),("f", "F", "=", "9", "φ", "Φ"),("q", "Q", "&", "+", "ϕ", "ℚ"),("ß", "ẞ", "ſ", "−", "ς", "∘"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("u", "U", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("a", "A", "{",  "⇣", "α", "∀"),
     ("e", "E", "}", "⇢", "ε", "∃"),("o", "O", "*", "⇲", "ο", "∈"),("s", "S", "?", "¿", "σ", "Σ"),("n", "N", "(", "4", "ν", "ℕ"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("t", "T", "-", "6", "τ", "∂"),("d", "D", ":", ",", "δ", "Δ"),("y", "Y", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("ü", "Ü", "#", "", "", "∪"),("ö", "Ö", "$", "", "ϵ", "∩"),("ä", "Ä", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("z", "Z", "`", "↶", "ζ", "ℤ"),("b", "B", "+", ":", "β", "⇐"),("m", "M", "%", "1", "μ", "⇔"),
     (",", "–", '"', "2", "ϱ", "⇒"),(".", "•", "'", "3", "ϑ", "↦"),("j", "J", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lx = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("l", "L", "…", "⇞", "ξ", "Ξ"),("v", "V", "_", "⌫", "", "√"),("x", "X", "[", "⇡", "λ", "Λ"),
     ("c", "C", "]", "Entf", "χ", "ℂ"),("w", "W", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("h", "H", "<", "7", "ψ", "Ψ"),
     ("g", "G", ">", "8", "γ", "Γ"),("f", "F", "=", "9", "φ", "Φ"),("q", "Q", "&", "+", "ϕ", "ℚ"),("ß", "ẞ", "ſ", "−", "ς", "∘"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("u", "U", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("a", "A", "{",  "⇣", "α", "∀"),
     ("e", "E", "}", "⇢", "ε", "∃"),("o", "O", "*", "⇲", "ο", "∈"),("s", "S", "?", "¿", "σ", "Σ"),("n", "N", "(", "4", "ν", "ℕ"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("t", "T", "-", "6", "τ", "∂"),("d", "D", ":", ",", "δ", "Δ"),("y", "Y", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("ü", "Ü", "#", "", "", "∪"),("ö", "Ö", "$", "", "ϵ", "∩"),("ä", "Ä", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("z", "Z", "`", "↶", "ζ", "ℤ"),("b", "B", "+", ":", "β", "⇐"),("m", "M", "%", "1", "μ", "⇔"),
     (",", "–", '"', "2", "ϱ", "⇒"),(".", "•", "'", "3", "ϑ", "↦"),("j", "J", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]
NEO_LAYOUT_lxwq = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("l", "L", "…", "⇞", "ξ", "Ξ"),("v", "V", "_", "⌫", "", "√"),("x", "X", "[", "⇡", "λ", "Λ"),
     ("c", "C", "]", "Entf", "χ", "ℂ"),("q", "Q", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("h", "H", "<", "7", "ψ", "Ψ"),
     ("g", "G", ">", "8", "γ", "Γ"),("f", "F", "=", "9", "φ", "Φ"),("w", "W", "&", "+", "ϕ", "ℚ"),("ß", "ẞ", "ſ", "−", "ς", "∘"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("u", "U", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("a", "A", "{",  "⇣", "α", "∀"),
     ("e", "E", "}", "⇢", "ε", "∃"),("o", "O", "*", "⇲", "ο", "∈"),("s", "S", "?", "¿", "σ", "Σ"),("n", "N", "(", "4", "ν", "ℕ"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("t", "T", "-", "6", "τ", "∂"),("d", "D", ":", ",", "δ", "Δ"),("y", "Y", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("ü", "Ü", "#", "", "", "∪"),("ö", "Ö", "$", "", "ϵ", "∩"),("ä", "Ä", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("z", "Z", "`", "↶", "ζ", "ℤ"),("b", "B", "+", ":", "β", "⇐"),("m", "M", "%", "1", "μ", "⇔"),
     (",", "–", '"', "2", "ϱ", "⇒"),(".", "•", "'", "3", "ϑ", "↦"),("j", "J", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]

# TODO: Add higher layers (shift for the numbers, …)
QWERTZ_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("q"),("w"),("e"),("r"),("t"),("z"),("u"),("i"),("o"),("p"),("ü"),("+"),()], # Reihe 1
    [("⇩"),("a"),("s"),("d"),("f"),("g"),("h"),("j"),("k"),("l"),("ö"),("ä"),("#"),("\n")], # Reihe 2
    [("⇧"),("<"),("y"),("x"),("c"),("v"),("b"),("n"),("m"),(",", ";"),(".", ":"),("-"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

#NORDTAST_LAYOUT = [
#    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
#    [("⇥"),("ä"),("u"),("o"),("b"),("p"),("k"),("g"),("l"),("m"),("f"),("x"),("+"),()], # Reihe 1
#    [("⇩"),("a"),("i"),("e"),("t"),("c"),("h"),("d"),("n"),("r"),("s"),("ß"),(),("\n")], # Reihe 2
#    [("⇧"),(),("."),(","),("ü"),("ö"),("q"),("y"),("z"),("w"),("v"),("j"),("⇗")],        # Reihe 3
#    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
#]

#: from Ulf Bro, http://nordtast.org – with added Neo-layers to be fair in the comparisions.
NORDTAST_LAYOUT = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("´", "`", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("ä", "Ä", "…", "⇞", "ξ", "Ξ"),("u", "U", "_", "⌫", "", "√"),("o", "O", "[", "⇡", "λ", "Λ"),
     ("b", "B", "]", "Entf", "χ", "ℂ"),("p", "P", "^", "⇟", "ω", "Ω"),("k", "K", "!", "¡", "κ", "×"),("g", "G", "<", "7", "ψ", "Ψ"),
     ("l", "L", ">", "8", "γ", "Γ"),("m", "M", "=", "9", "φ", "Φ"),("f", "F", "&", "+", "ϕ", "ℚ"),("x", "X", "ſ", "−", "ς", "∘"),
     ("+", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("a", "A", "\\", "⇱", "", "⊂"),("i", "I", "/", "⇠", "ι", "∫"),("e", "E", "{",  "⇣", "α", "∀"),
     ("t", "T", "}", "⇢", "ε", "∃"),("c", "C", "*", "⇲", "ο", "∈"),("h", "H", "?", "¿", "σ", "Σ"),("d", "D", "(", "4", "ν", "ℕ"),
     ("n", "N", ")", "5", "ρ", "ℝ"),("r", "R", "-", "6", "τ", "∂"),("s", "S", ":", ",", "δ", "Δ"),("ß", "ẞ", "@", ".", "υ", "∇"),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),(".", "•", "#", "", "", "∪"),(",", "–", "$", "", "ϵ", "∩"),("ü", "Ü", "|", "⎀", "η", "ℵ"),
     ("p", "P", "~", "\n", "π", "Π"),("ö", "Ö", "`", "↶", "ζ", "ℤ"),("q", "Q", "+", ":", "β", "⇐"),("y", "Y", "%", "1", "μ", "⇔"),
     ("z", "Z", '"', "2", "ϱ", "⇒"),("w", "W", "'", "3", "ϑ", "↦"),("v", "V", ";", ";", "θ", "Θ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]


# TODO: Add higher layers (shift for the numbers, …)
DVORAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("’"),(","),("."),("p"),("y"),("f"),("g"),("c"),("r"),("l"),("/"),("="),()], # Reihe 1
    [("⇩"),("a"),("o"),("e"),("u"),("i"),("d"),("h"),("t"),("n"),("s"),("-"),(),("\n")], # Reihe 2
    [("⇧"),(),(";"),("q"),("j"),("k"),("x"),("b"),("m"),("w"),("v"),("z"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]

# TODO: Add higher layers (shift for the numbers, …)
COLEMAK_LAYOUT = [
    [("^"),("1"),("2"),("3"),("4"),("5"),("6"),("7"),("8"),("9"),("0"),("ß"),("´"),("←")], # Zahlenreihe (0)
    [("⇥"),("q"),("w"),("f"),("p"),("g"),("j"),("l"),("u"),("y"),(";"),("["),("]"),("\\")], # Reihe 1
    [("⇩"),("a"),("r"),("s"),("t"),("d"),("h"),("n"),("e"),("i"),("o"),("`"),(),("\n")], # Reihe 2
    [("⇧"),(),("z"),("x"),("c"),("v"),("b"),("k"),("m"),(","),("."),("/"),("⇗")],        # Reihe 3
    [(), (), (), (" "), (), (), (), ()] # Reihe 4 mit Leertaste
]


AdNW_LAYOUT = [
    [("^", "ˇ", "↻", "˙", "˞", "̣"),("1", "°", "¹", "ª", "₁", "¬"),("2", "§", "²", "º", "₂", "∨"),("3", "ℓ", "³", "№", "₃", "∧"),
     ("4", "»", "›", "", "♀", "⊥"),("5", "«", "‹", "·", "♂", "∡"),("6", "$", "¢", "£", "⚥", "∥"),("7", "€", "¥", "¤", "ϰ", "→"),
     ("8", "„", "‚", "⇥", "⟨", "∞"),("9", "“", "‘", " /", "⟩", "∝"),("0", "”", "’", "*", "₀", "∅"),("-", "—", "-", "‑", "­"),
     ("`", "¸", "°", "¨", "", "¯"),("←")], # Zahlenreihe (0)

    [("⇥"),("k", "K", "…", "⇞", "κ", ""),("u", "U", "_", "⌫", "", "⊂"),("ü", "Ü", "[", "⇡", "", "∪"),
     (".", "•", "]", "Entf", "ϑ", "↦"),("ä", "Ä", "^", "⇟", "η", "ℵ"),("v", "V", "!", "¡", "", "√"),("g", "G", "<", "7", "γ", "Γ"),
     ("c", "C", ">", "8", "χ", "ℂ"),("l", "L", "=", "9", "λ", "Λ"),("j", "J", "&", "+", "θ", "Θ"),("f", "F", "ſ", "−", "φ", "Φ"),
     ("´", "~", "/", "˝", "", "˘"),()], # Reihe 1

    [("⇩"),("h", "H", "\\", "⇱", "ψ", "Ψ"),("i", "I", "/", "⇠", "ι", "∫"),("e", "E", "}", "⇢", "ε", "∃"),
     ("a", "A", "{",  "⇣", "α", "∀"),("o", "O", "*", "⇲", "ο", ""),("d", "D", "?", "¿", "δ", "Δ"),("t", "T", "(", "4", "τ", "∂"),
     ("r", "R", ")", "5", "ρ", "ℝ"),("n", "N", "-", "6", "ν", "ℕ"),("s", "S", ":", ",", "σ", ""),("ß", "ẞ", "@", ".", "ς", ""),
     ("⇘"),("\n")], # Reihe 2

    [("⇧"),("⇚"),("x", "X", "#", "", "ξ", "Ξ"),("y", "Y", "$", "", "υ", ""),("ö", "Ö", "|", "⎀", "", "∩"),
     (",", "–", "~", "\n", "ϱ", "⇒"),("q", "Q", "`", "↶", "ϕ", "ℚ"),("b", "B", "+", ":", "β", "⇐"),("p", "P", "%", "1", "π", "Π"),
     ("w", "W", '"', "2", "ω", ""),("m", "M", "'", "3", "μ", "⇔"),("z", "Z", ";", ";", "ζ", "ℤ"),("⇗")],        # Reihe 3

    [(), (), (), (" ", " ", " ", "0", " ", " "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
]

HAEIU_LAYOUT = [
    [('^', 'ˇ', '↻', '˙', '˞', '̣'), ('1', '°', '¹', 'ª', '₁', '¬'), ('2', '§', '²', 'º', '₂', '∨'), ('3', 'ℓ', '³', '№', '₃', '∧'),
     ('4', '»', '›', '', '♀', '⊥'), ('5', '«', '‹', '·', '♂', '∡'), ('6', '$', '¢', '£', '⚥', '∥'), ('7', '€', '¥', '¤', 'ϰ', '→'),
     ('8', '„', '‚', '⇥', '⟨', '∞'), ('9', '“', '‘', ' /', '⟩', '∝'), ('0', '”', '’', '*', '₀', '∅'), ('-', '—', '-', '‑', '←'),
     ('`', '¸', '°', '¨', '', '¯'), '←'],

    [('⇥'), ('x', 'X', '…', '⇞', 'ξ', 'Ξ'), ('z', 'Z', '_', '⌫', 'ζ', 'ℤ'), ('o', 'O', '[', '⇡', 'ο', '∈'),
     ('.', '•', ']', 'Entf', 'ϑ', '↦'), (',', '–', '^', '⇟', 'ϱ', '⇒'), ('p', 'P', '!', '¡', 'π', 'Π'), ('c', 'C', '<', '7', 'χ', 'ℂ'),
     ('l', 'L', '>', '8', 'λ', 'Λ'), ('m', 'M', '=', '9', 'μ', '⇔'), ('v', 'V', '&', '+', '', '√'), ('ß', 'ẞ', 'ſ', '−', 'ς', '∘'),
     ('´', '~', '/', '˝', '', '˘'), ()],

    [('⇩'), ('h', 'H', '\\', '⇱', 'ψ', 'Ψ'), ('a', 'A', '/', '⇠', 'α', '∀'), ('e', 'E', '{', '⇣', 'ε', '∃'),
     ('i', 'I', '}', '⇢', 'ι', '∫'), ('u', 'U', '*', '⇲', '', '⊂'), ('d', 'D', '?', '¿', 'δ', 'Δ'), ('t', 'T', '(', '4', 'τ', '∂'),
     ('n', 'N', ')', '5', 'ν', 'ℕ'), ('r', 'R', '-', '6', 'ρ', 'ℝ'), ('s', 'S', ':', ',', 'σ', ''), ('w', 'W', '@', '.', 'ω', ''),
     ('⇘'), ('\n')],

    [('⇧'), ('⇚'), ('k', 'K', '#', '', 'κ', '×'), ('ö', 'Ö', '$', '', '', '∩'), ('ä', 'Ä', '|', '⎀', 'η', 'ℵ'),
     ('ü', 'Ü', '~', '\n', '', '∪'), ('y', 'Y', '`', '↶', 'υ', ''), ('b', 'B', '+', ':', 'β', '⇐'), ('g', 'G', '%', '1', 'γ', 'Γ'),
     ('j', 'J', '"', '2', 'θ', 'Θ'), ('q', 'Q', "'", '3', 'ϕ', 'ℚ'), ('f', 'F', ';', ';', 'φ', 'Φ'), ('⇗')],

    [(), (), (), (' ', ' ', ' ', '0', ' ', ' '), '⇙', (), (), ()],

]



# Ulfs All fingers equal but the small one
COST_PER_KEY_OLD  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Reihe 1
        [0,2,1,1,1,3,3,1,1,1,2,6,0,9], # Reihe 2
        [0,4,5,5,5,5,7,7,5,5,5,5,0],     # Reihe 3
        [0,0,0,     9     ,0,0,0,0] # Reihe 4 mit Leertaste
]

# First reweighting
COST_PER_KEY_OLD2  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0,6,3,3,3,4,4,3,3,3,6,7,8,0], # Reihe 1
        [0,3,2,2,1,3,3,1,2,2,3,6,0,9], # Reihe 2
        [0,5,5,5,5,5,7,7,5,5,5,5,0],     # Reihe 3
        [0,0,0,     9     ,0,0,0,0] # Reihe 4 mit Leertaste
]

#: The names of the fingers from left to right
FINGER_NAMES = ["Klein_L", "Ring_L", "Mittel_L", "Zeige_L", "Daumen_L",
                "Daumen_R", "Zeige_R", "Mittel_R", "Ring_R", "Klein_R"]

# Optimized structure for accessing by position. key_to_finger gets 3 times faster than with a cache and doublechecking.
KEY_TO_FINGER = {}
for finger in FINGER_POSITIONS:
    for pos in FINGER_POSITIONS[finger]:
        KEY_TO_FINGER[pos] = finger

### Constants for testing

TEST_LAYOUT = [
    [("^", "ˇ", "↻")], # Zahlenreihe (0)

    [("⇥"),], # Reihe 1

    [("u", "U", "\\", "⇱", "", "⊂"),("\n")], # Reihe 2

    [],        # Reihe 3

    [(), (), (), (" "), ("⇙"), (), (), ()] # Reihe 4 mit Leertaste
    ]
    

# Weighting for the tests — DON’T CHANGE THIS, it’s necessary for correct testing
TEST_COST_PER_KEY  = [ # 0 heißt nicht beachtet
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0], # Zahlenreihe (0)
        [0, 12,9,6,4,10,10,4,6,9,12,15,18,0], # Reihe 1
        [0,  5,3,3,2,5,5,2,3,3,5,12,0,15], # Reihe 2 
        [15,0,10,11,11,7,12,10,7,11,11,10,15],     # Reihe 3
        [0,0,0,     5     ,0,0,0,0] # Reihe 4 mit Leertaste
]

# Gewichtung der unterschiedlichen Kosten
TEST_WEIGHT_FINGER_REPEATS = 8 #: higher than a switch from center to side, but lower than a switch from center to upper left.
TEST_WEIGHT_FINGER_REPEATS_TOP_BOTTOM = 16 #: 2 times a normal repeat, since it's really slow. Better two outside low or up than an up-down repeat. 
TEST_WEIGHT_POSITION = 1 #: reference
TEST_WEIGHT_FINGER_DISBALANCE = 5 #: multiplied with the standard deviation of the finger usage - value guessed and only valid for the 1gramme.txt corpus.
TEST_WEIGHT_TOO_LITTLE_HANDSWITCHING = 1 #: how high should it be counted, if the hands aren’t switched in a triple?
TEST_WEIGHT_INTENDED_FINGER_LOAD_LEFT_PINKY_TO_RIGHT_PINKY = [
    0.5,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    1,
    0.5] #: The intended load per finger. Inversed and then used as multiplier for the finger load before calculating the finger disbalance penalty. Any load distribution which strays from this optimum gives a penalty.

TEST_FINGER_SWITCH_COST = { # iu td < ui dt dr ua rd au < ai rt < nd eu
    "Klein_L": {
        "Ring_L": 3, 
        "Mittel_L": 3
        }, 
    "Ring_L": {
        "Klein_L": 4,
        "Mittel_L": 3
        }, 
    "Mittel_L": {
        "Klein_L": 1,
        "Ring_L": 2
        }, 
    "Zeige_L": {
        "Klein_L": 1
        }, 
    "Daumen_L": {
        },
    "Daumen_R": {
        },
    "Zeige_R": {
        "Klein_R": 1
        },
    "Mittel_R": {
        "Ring_R": 2, 
        "Klein_R": 1
        },
    "Ring_R": {
        "Mittel_R": 3,
        "Klein_R": 4
        }, 
    "Klein_R": {
        "Mittel_R": 3,
        "Ring_R": 3
        }
} # iutd, drua, uidt, rdau, airt, ndeu :)

TEST_WEIGHT_SECONDARY_BIGRAM_IN_TRIGRAM = 0.5 #: multiplier for the cost of secondary bigrams in trigrams. 


### Caches

# together with the more efficient datastructure for key_to_finger, these caches provide a performance boost by about factor 6.6

#_LETTER_TO_KEY_CACHE = {}

# TODO: Refresh directly when mutating. Then we don’t have to check anymore for the letter if it really is at the given position. 

### Imports

from copy import deepcopy


### Helper Functions

def format_layer_1_string(layout):
    """Format a string looking like this:

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj
    """
    l = ""
    l += "".join((i[0] for i in layout[1][1:6])) + " " + "".join((i[0] for i in layout[1][6:-1])) + "\n"
    l += "".join((i[0] for i in layout[2][1:6])) + " " + "".join((i[0] for i in layout[2][6:-2])) + "\n"
    if layout[3][1] and layout[3][1][0] != "⇚": 
        l += "".join((i[0] for i in layout[3][1:7])) + " " + "".join((i[0] for i in layout[3][7:-1]))
    else:
        l += "".join((i[0] for i in layout[3][2:7])) + " " + "".join((i[0] for i in layout[3][7:-1]))
    return l


def get_key(pos, layout=NEO_LAYOUT):
    """Get the key at the given position.

    >>> get_key((2, 3, 0))
    'a'
    """
    try: 
        return layout[pos[0]][pos[1]][pos[2]]
    except: return None


def single_key_position_cost(pos, layout, cost_per_key=COST_PER_KEY):
    """Get the position_cost of a single key.

    @param pos: The position of the key.
    @type pos: tuple (row, col, layer).
    @return: the cost of that one position."""
    if pos is None: # not found
        return COST_PER_KEY_NOT_FOUND
    # shift, M3 and M4
    if COST_LAYER_ADDITION[pos[2]:]:
        return cost_per_key[pos[0]][pos[1]] + COST_LAYER_ADDITION[pos[2]]
    # layer has no addition cost ⇒ undefined layer (higher than layer 6!). Just take the base key…
    return cost_per_key[pos[0]][pos[1]]


def is_position_cost_lower(pos, new_pos, layout, doubled_layer=True):
    """
    >>> is_position_cost_lower((2, 10, 2), (3, 7, 3), NEO_LAYOUT)
    False
    """
    # use tripled layer cost, because it ignores the additional bigrams.
    new_cost = single_key_position_cost(new_pos, layout) + COST_LAYER_ADDITION[new_pos[2]]
    cost = single_key_position_cost(pos, layout) + 2*COST_LAYER_ADDITION[pos[2]]
    return new_cost < cost
        

def update_letter_to_key_cache(key, layout):
    """Update the cache entry for the given key."""
    try: LETTER_TO_KEY_CACHE = layout[5]
    except IndexError:
        layout.append({})
        LETTER_TO_KEY_CACHE = layout[5]
    pos = None
    # search the whole layout for instances of the key.
    for row in range(len(layout[:5])):
        for col in range(len(layout[row])):
            # if the key is found, use the key with the lowest cost.
            if key in layout[row][col]:
                #: the number of keys in the row
                key_num = len(layout[row][col])
                for idx in range(key_num):
                    # if the key exists in multiple places, use the position with the lowest cost.
                    idx_rev = key_num - idx -1
                    if layout[row][col][idx_rev] == key:
                        new_pos = (row, col, idx_rev)
                        if pos is None:
                            pos = new_pos
                        elif is_position_cost_lower(pos, new_pos, layout):
                            pos = new_pos
    LETTER_TO_KEY_CACHE[key] = pos
    return pos


def get_all_positions_in_layout(layout):
    """Get all positions for which there are keys in the layout. 

    >>> get_all_positions_in_layout(TEST_LAYOUT)
    [(0, 0, 0), (0, 0, 1), (0, 0, 2), (1, 0, 0), (2, 0, 0), (2, 0, 1), (2, 0, 2), (2, 0, 3), (2, 0, 5), (2, 1, 0), (4, 3, 0), (4, 4, 0)]
    """
    positions = []
    for line in range(len(layout[:5])): # :5 to avoid finding a cache.
        for key in range(len(layout[line])):
            for letter in range(len(layout[line][key])):
                if layout[line][key][letter]: 
                    positions.append((line, key, letter))
    return positions


def get_all_keys_in_layout(layout):
    """Get all keys which are in the layout. Sorted the same way as the positions from get_all_positions_in_layout(). 

    >>> get_all_keys_in_layout(TEST_LAYOUT)
    ['^', 'ˇ', '↻', '⇥', 'u', 'U', '\\\\', '⇱', '⊂', '\\n', ' ', '⇙']
    """
    keys = []
    for line in layout[:5]:
        for key in line:
            for letter in key:
                if letter: 
                    keys.append(letter)
    return keys


def update_letter_to_key_cache_multiple(keys, layout):
    """Update the cache entries for many keys.

    @param keys: the keys to update. If it’s None, update ALL.
    """
    if keys is None:
        keys = get_all_keys_in_layout(layout)
    for key in keys:
        update_letter_to_key_cache(key, layout=layout)
    

def find_key(key, layout): 
    """Find the position of the key in the layout.
    
    >>> find_key("a", NEO_LAYOUT)
    (2, 3, 0)
    >>> find_key("A", NEO_LAYOUT)
    (2, 3, 1)
    >>> find_key("e", NEO_LAYOUT)
    (2, 4, 0)
    >>> find_key(",", NEO_LAYOUT)
    (3, 9, 0)
    >>> find_key(".", NEO_LAYOUT)
    (3, 10, 0)
    >>> find_key(":", NEO_LAYOUT)
    (2, 10, 2)
    >>> find_key('#', NEO_LAYOUT)
    (3, 2, 2)
    >>> find_key("⇧", layout=NEO_LAYOUT)
    (3, 0, 0)
    >>> find_key("A", layout=QWERTZ_LAYOUT)
    (2, 1, 1)
    >>> find_key("a", layout=QWERTZ_LAYOUT)
    (2, 1, 0)
    >>> find_key("£", layout=NEO_LAYOUT)
    (0, 6, 3)
    >>> find_key("»", layout=NEO_LAYOUT)
    (0, 4, 1)
    >>> find_key("«", layout=NEO_LAYOUT)
    (0, 5, 1)
    >>> find_key("¤", layout=NEO_LAYOUT)
    (0, 7, 3)
    """
    # check, if the layout already has a cache. If not, create it.
    # this approach reduces the time to find a key by about 50%.
    # TODO: find out why this change affects the costs of layouts!
    # the cost is raised by a value between 1.2480213606 (NordTast)
    # and 1.2964878374 (Colemak).
    # a part of the change might be, that now uppercase keys
    # are properly taken into account. 
    #if key != key.lower():
    #    raise ValueError("You shall not ask me for upperkey letters (yet)!")

    try: LETTER_TO_KEY_CACHE = layout[5]
    except IndexError:
        layout.append({})
        LETTER_TO_KEY_CACHE = layout[5]
        update_letter_to_key_cache_multiple(None, layout=layout)
    # first check the caches
    try: pos = LETTER_TO_KEY_CACHE[key]
    except KeyError:
        # maybe we didn’t add the uppercase key, should only happen for incomplete layouts.
        try: 
            pos = LETTER_TO_KEY_CACHE[key.lower()]
            if not pos[2]: # == 0
                pos = pos[:2] + (1,) # this is an uppercase key.
        except KeyError: 
            pos = None # all keys are in there. None means, we don’t need to check by hand.
    return pos


def finger_keys(finger_name, layout=NEO_LAYOUT):
    """Get the keys corresponding to the given finger name.

    >>> for name in FINGER_NAMES:
    ...    name, finger_keys(name)
    ('Klein_L', ['x', '⇩', 'u', '⇧', '⇚', 'ü'])
    ('Ring_L', ['v', 'i', 'ö'])
    ('Mittel_L', ['l', 'a', 'ä'])
    ('Zeige_L', ['c', 'e', 'p', 'w', 'o', 'z'])
    ('Daumen_L', [' '])
    ('Daumen_R', [' ', '⇙'])
    ('Zeige_R', ['k', 's', 'b', 'h', 'n', 'm'])
    ('Mittel_R', ['g', 'r', ','])
    ('Ring_R', ['f', 't', '.'])
    ('Klein_R', ['q', 'd', 'j', 'ß', 'y', '´', '⇘', '\\n', '⇗'])
    """
    keys = [str(get_key(pos, layout=layout)) for pos in FINGER_POSITIONS[finger_name]]
    return keys


def key_to_finger(key, layout=NEO_LAYOUT):
    """Get the finger name used to hit the given key.

    >>> key_to_finger("a")
    'Mittel_L'
    >>> key_to_finger("A")
    'Mittel_L'
    >>> key_to_finger("«")
    ''
    >>> key_to_finger("⇩")
    'Klein_L'
    >>> key_to_finger("⇧")
    'Klein_L'
    """
    pos = find_key(key, layout=layout)
    try: pos = pos[:2] + (0, )
    except TypeError: return "" # pos is None
    # check the cache
    try: return KEY_TO_FINGER[pos]
    except KeyError: return ""


def pos_is_left(pos):
    """check if the given position is on the left hand.

    >>> clear_left_positions = [(0, 0, 0), (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0)]
    >>> False in [pos_is_left(pos) for pos in clear_left_positions]
    False
    
    """
    return RIGHT_HAND_LOWEST_INDEXES[pos[0]] > pos[1]


def switch_positions(pos0, pos1, layout=NEO_LAYOUT):
    """Switch two positions in the layout.

    >>> lay = switch_positions((1, 1, 0), (1, 3, 0), layout=NEO_LAYOUT)
    >>> lay = switch_positions((1, 1, 1), (1, 3, 1), layout=lay)
    >>> lay[:5] == NEO_LAYOUT_lx[:5]
    True
    >>> print(lay[1][1])
    ('l', 'L', '…', '⇞', 'ξ', 'Ξ')
    >>> print(lay[1][3])
    ('x', 'X', '[', '⇡', 'λ', 'Λ')
    >>> lay = switch_positions((1, 1, 0), (1, 1, 1), layout=lay)
    >>> print(lay[1][1])
    ('L', 'l', '…', '⇞', 'ξ', 'Ξ')
    >>> find_key("l", lay)
    (1, 1, 1)
    """
    lay = deepcopy(layout)
    pos0_keys = lay[pos0[0]][pos0[1]]
    pos1_keys = lay[pos1[0]][pos1[1]]

    # if they are on the same physical key, just exchange both positions on the single key
    if pos0[:2] == pos1[:2]:
        tmp = list(pos0_keys)
        tmp[pos0[2]] = pos1_keys[pos1[2]]
        tmp[pos1[2]] = pos0_keys[pos0[2]]
        tmp = tuple(tmp)

        cache_update = "".join(tmp)
        lay[pos0[0]][pos0[1]] = tmp
        update_letter_to_key_cache_multiple(cache_update, layout=lay)
        return lay

    # generate new tuples for all layers, with tmp0 containing pos1 and tmp1 containing pos0
    tmp0 = list(pos0_keys)
    tmp0[pos0[2]] = pos1_keys[pos1[2]]
    tmp0 = tuple(tmp0)
    
    tmp1 = list(pos1_keys)
    tmp1[pos1[2]] = pos0_keys[pos0[2]]
    tmp1 = tuple(tmp1)
    
    cache_update = ""
    for letter in tmp0 + tmp1:
        cache_update += letter

    lay[pos0[0]][pos0[1]] = tmp0
    lay[pos1[0]][pos1[1]] = tmp1
    update_letter_to_key_cache_multiple(cache_update, layout=lay)
    return lay
    

def switch_keys(keypairs, layout=NEO_LAYOUT, switch_layers = [0, 1, 4, 5]):
    """Switch keys in the layout, so we don't have to fiddle with actual layout files.

    @param keypairs: A list of keypairs to switch. The keys in these pairs MUST be the base layer keys.

    >>> lay = switch_keys([], layout = NEO_LAYOUT)
    >>> lay == NEO_LAYOUT
    True
    >>> lay = switch_keys(["lx", "wq"], layout = NEO_LAYOUT, switch_layers=[0,1])
    >>> get_key((1, 1, 0), layout=lay)
    'l'
    >>> get_key((1, 3, 0), layout=lay)
    'x'
    >>> get_key((1, 5, 0), layout=lay)
    'q'
    >>> get_key((1, 10, 0), layout=lay)
    'w'
    >>> get_key((1, 1, 1), layout=lay)
    'L'
    >>> get_key((1, 3, 1), layout=lay)
    'X'
    >>> get_key((1, 5, 1), layout=lay)
    'Q'
    >>> get_key((1, 10, 1), layout=lay)
    'W'
    >>> find_key("l", layout=lay) == (1, 1, 0)
    True
    >>> find_key("L", layout=lay) == (1, 1, 1)
    True
    >>> NEO_LAYOUT_lxwq == lay
    True
    >>> lay = switch_keys(["lx"], layout = NEO_LAYOUT, switch_layers=[0,1])
    >>> NEO_LAYOUT_lx == lay
    True
    >>> a = find_key("a", layout=lay)
    >>> A = find_key("A", layout=lay)
    >>> curly = find_key("{", layout=lay)
    >>> lay = switch_keys(["ae"], layout=lay, switch_layers = [0,1,2])
    >>> a == find_key("e", layout=lay)
    True
    >>> A == find_key("E", layout=lay)
    True
    >>> curly == find_key("}", layout=lay)
    True
    >>> "}" == get_key(find_key("}", layout=lay), layout=lay)
    True
    >>> dot = find_key(".", layout=NEO_LAYOUT)
    >>> d = find_key("d", layout=NEO_LAYOUT)
    >>> comma = find_key(",", layout=NEO_LAYOUT)
    >>> p = find_key("p", layout=NEO_LAYOUT)
    >>> lay = switch_keys([".d", ",p"], layout=NEO_LAYOUT)
    >>> d == find_key(".", layout=lay)
    True
    >>> dot == find_key("d", layout=lay)
    True
    >>> p == find_key(",", layout=lay)
    True
    >>> comma == find_key("p", layout=lay)
    True
    """
    lay = deepcopy(layout)
    from pprint import pprint
    #pprint(lay)
    for pair in keypairs:
            pos0 = find_key(pair[0], layout=lay)
            pos1 = find_key(pair[1], layout=lay)

            # both positions MUST be on the base layer. 
            if pos0[2] or pos1[2]:
                #info("one of the keys isn’t on the base layer. Ignoring the switch", pair)
                continue

            pos0_keys = lay[pos0[0]][pos0[1]]
            pos1_keys = lay[pos1[0]][pos1[1]]

            # add the supported layers.
            tmp0 = []
            for i in range(max(len(pos1_keys), len(pos0_keys))):
                if i in switch_layers:
                    try: 
                        tmp0.append(pos1_keys[i])
                    except IndexError: # not there: Fill the layer.
                        tmp0.append("")
                else:
                    try: 
                        tmp0.append(pos0_keys[i])
                    except IndexError: # not there: Fill the layer.
                        tmp0.append("")
            tmp0 = tuple(tmp0)

            tmp1 = []
            for i in range(max(len(pos1_keys), len(pos0_keys))):
                if i in switch_layers:
                    try: 
                        tmp1.append(pos0_keys[i])
                    except IndexError: # not there: Fill the layer.
                        tmp1.append("")
                else:
                    try: 
                        tmp1.append(pos1_keys[i])
                    except IndexError: # not there: Fill the layer.
                        tmp1.append("")
            tmp1 = tuple(tmp1)

            cache_update = ""
            for letter in tmp0 + tmp1:
                cache_update += letter

            lay[pos0[0]][pos0[1]] = tmp0
            lay[pos1[0]][pos1[1]] = tmp1
            update_letter_to_key_cache_multiple(cache_update, layout=lay)
        #except:
        #    pprint(lay)
        #    print(prev, pair, pos0, pos1, tmp0, tmp1)
        #    exit()
    
    return lay


def string_to_layout(layout_string, base_layout=NEO_LAYOUT):
    """Turn a layout_string into a layout.

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj

    """
    layer_0_keys = [get_key(pos, layout=base_layout) for pos in get_all_positions_in_layout(base_layout) if pos[2] == 0]
    to_replace_list = []
    def set_key(current_key, new_letter, pos_01, layout, base_layout=base_layout, changing_layers = [0,1,4,5]):
        """Set the new_letter into the pos_01 in the layout. Take the key from the position in the base_layout and from the position in the letter and merge them, using layer 3,4 from the position and the rest from the letter.

        @param pos_01: the key which is currently in the given position. Not needed anymore, except for debugging.
        @param current_key: The key which is currently in the position. Not needed anymore, except for debugging.
        @param new_letter: The letter which should be in the position.
        @param pos_01: The position where the key should be placed.
        @param changing_layers: The layers in the base layout which change when the keys get changed."""
        # first get the keys for all layers from position in the base_layout
        base_keys = base_layout[pos_01[0]][pos_01[1]]
        # then get the keys corresponding to the position of the new letter.
        letter_pos = find_key(new_letter, layout=layout)
        if letter_pos is None or letter_pos[2]:
            # the new letter is not in the base_layout or not in the base layer, just set it on layer 0.
            layout[pos_01[0]][pos_01[1]] = (new_letter, ) + tuple(base_keys[1:])
            return layout
            
        letter_keys = base_layout[letter_pos[0]][letter_pos[1]]
        # replace all changing_layers in the base_keys with the new_keys.
        tmp = []
        for i in range(6):
            try: 
                if i in changing_layers:
                    tmp.append(letter_keys[i])
                else:
                    tmp.append(base_keys[i])
            except IndexError: # key not found
                tmp.append("")
        layout[pos_01[0]][pos_01[1]] = tuple(tmp)
        return layout
        
    layout = deepcopy(base_layout)
    lines = layout_string.splitlines()
    # first and second letter row
    for i in range(1, 6):
        layout = set_key(layout[1][i][0], lines[0][i-1], (1, i), layout)
        layout = set_key(layout[1][i+5][0], lines[0][i+5], (1, i+5), layout)
        layout = set_key(layout[2][i][0], lines[1][i-1], (2, i), layout)
        layout = set_key(layout[2][i+5][0], lines[1][i+5], (2, i+5), layout)

    layout = set_key(layout[1][-3][0], lines[0][11], (1, -3), layout)
    layout = set_key(layout[2][-3][0], lines[1][11], (2, -3), layout)

    # third row
    if lines[0][12:]:
        layout = set_key(layout[1][-2][0], lines[0][12], (1, -2), layout)
    
    left, right = lines[2].split()[:2]
    for i in range(len(left)):
        layout = set_key(layout[3][6-i][0], left[-i-1], (3, 6-i), layout)
    for i in range(len(right)):
        layout = set_key(layout[3][7+i][0], right[i], (3, 7+i), layout)

    # finally update the cache
    update_letter_to_key_cache_multiple(None, layout)

    return deepcopy(layout)
    

def changed_keys(layout0, layout1):
    """Find the keys which are in different positions in the two layouts.

    >>> changed_keys(NEO_LAYOUT, NEO_LAYOUT_lx)
    ['X', 'l', 'x', 'L']
    >>> from check_neo import switch_keys
    >>> t = switch_keys(["u\\n"], layout=TEST_LAYOUT, switch_layers=[0,1])
    >>> changed_keys(TEST_LAYOUT, t)
    ['\\n', 'u', 'U']
    """
    # first make sure, we have the caches.
    try: cache0 = layout0[5]
    except IndexError:
        layout0.append({})
        cache0 = layout0[5]
        update_letter_to_key_cache_multiple(None, layout=layout0)

    try: cache1 = layout1[5]
    except IndexError:
        layout1.append({})
        cache1 = layout1[5]
        update_letter_to_key_cache_multiple(None, layout=layout1)

    return [l for l in cache0 if not l in cache1 or cache0[l] != cache1[l]] + [l for l in cache1 if not l in cache0]


def diff_dict(d1, d2):
    """find the difference between two dictionaries.

    >>> a = {1: 2, 3: 4}
    >>> b = {1:2, 7:8}
    >>> c = {}
    >>> diff_dict(a, b)
    {3: 4, 7: 8}
    >>> a == diff_dict(a, c)
    True
    """
    diff = {}
    for key in d1:
        if not key in d2: 
            diff[key] = d1[key]
    for key in d2:
        if not key in d1:
            diff[key] = d2[key]
    return diff


def layout_difference_weighted(layout0, layout1, letters=None, letter_dict=None, sum_keystrokes=None):
    """Find the difference between two layouts, weighted with the number of times the differing letters are used in the corpus.

    This only gives 1.0, if one layout contains all letters from the corpus and the other layout has none of them (or all of them in different positions). 

    >>> from ngrams import get_all_data
    >>> letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data()
    >>> layout_difference_weighted(NEO_LAYOUT, NEO_LAYOUT, letters=letters)
    0.0
    >>> layout_difference_weighted(NEO_LAYOUT, NEO_LAYOUT_lx, letters=letters)
    0.036617925978240665
    >>> layout_difference_weighted(NEO_LAYOUT, NEO_LAYOUT_lxwq, letters=letters)
    0.050589766759669606
    >>> layout_difference_weighted(NEO_LAYOUT, QWERTZ_LAYOUT, letters=letters)
    0.9486182821801175
    >>> layout_difference_weighted(NEO_LAYOUT, NORDTAST_LAYOUT, letters=letters)
    0.8830111461330287
    >>> layout_difference_weighted(NORDTAST_LAYOUT, QWERTZ_LAYOUT, letters=letters)
    0.8983918828764104
    >>> layout_difference_weighted(NEO_LAYOUT, TEST_LAYOUT, letters=letters)
    0.9999201678764246
    >>> empty = [[], [], [], [], []]
    >>> layout_difference_weighted(NEO_LAYOUT, empty, letters=letters)
    0.9999202512375004
    """
    if letter_dict is None and letters is None:
        raise Exception("Need letters or a letter dict")
    elif letter_dict is None:
        letter_dict = {letter: num for num, letter in letters}
    if sum_keystrokes is None: 
        sum_keystrokes = sum(letter_dict.values())
    return sum([letter_dict.get(c, 0) for c in changed_keys(layout0, layout1)])/sum_keystrokes


def find_layout_families(layouts, letters, max_diff=0.2):
    """Find layout families in a list of layouts using the difference in key-positions, weighted by the occurrance probability of each key.

    >>> from ngrams import get_all_data
    >>> letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data()
    >>> len(find_layout_families([NEO_LAYOUT, NEO_LAYOUT_lx, NEO_LAYOUT_lxwq, QWERTZ_LAYOUT, NORDTAST_LAYOUT], letters=letters, max_diff=0.1))
    3
    >>> len(find_layout_families([NEO_LAYOUT, NEO_LAYOUT_lx, NEO_LAYOUT_lxwq, QWERTZ_LAYOUT, NORDTAST_LAYOUT], letters=letters, max_diff=0.9))
    2
    """
    families = []
    letter_dict = {letter: num for num, letter in letters}
    sum_keystrokes = sum(letter_dict.values())
    for l in layouts:
        fits = False
        for f in families:
            if layout_difference_weighted(l, f[0], letter_dict=letter_dict, sum_keystrokes=sum_keystrokes) <= max_diff:
                fits = True
        if not fits:
            families.append([])
            families[-1].append(l)
       
    return families


def combine_genetically(layout1, layout2):
    """Combine two layouts genetically (randomly)."""
    from random import randint
    switchlist = []
    for letter in abc:
        if randint(0, 1) == 1:
            pos = find_key(letter, layout=layout1)
            replacement = get_key(pos, layout=layout2)
            switchlist.append(letter+replacement)
    res = deepcopy(switch_keys(switchlist, layout=layout1))
    return res


if __name__ == "__main__":
    from doctest import testmod
    testmod()
