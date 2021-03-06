#!/usr/bin/env python3
# encoding: utf-8

"""Optimize keyboard layouts evolutionally (with mutations).

"""

# python 2.6 compatibility via 3to2
from __future__ import print_function
from random import choice, shuffle

__usage__ = """Usage:

- check_neo.py --help (display this text)

- check_neo.py [-q] [-v] [-o <file>]
  compare the Neo layout with others, using the included datafiles(*gramme.txt).
  -q only shows the results for the Neo layout.
  -v shows several additional metrics which are included in the total cost.
  -o writes the output to a file instead of printing it.

- check_neo.py --file <file> [--switch <lx,wq>] [-q] [-v]
  run the script on the file.
  --switch switches letters on the neo keyboard (lx,wq switches l for x and w for q).
  -q removes the qwertz comparision.
  -v adds the list of finger repeats.

- check_neo.py [-v] [--file <file>] --layout-string "khßwv ä.uozj
  dnclr aitesb
  fpgmx ,üöyq"
  check the layout given by a layout string.
  -v gives more statistical info on the layout
  --file <file> uses a file as corpus for checking the layout.


- check_neo.py --evolve <iterations> [--prerandomize <num_switches>] [-q] [-v] [--controlled-evolution] [--controlled-tail]
  randomly permutate keys on the Neo keyboard to see if a better layout emerges.
  --controlled-evolution tells it to use the horribly slow and deterministic code which always chooses the best possible change in each step.
  --controlled-tail makes it first do <iterations> random mutations and then a controlled evolution, until it can’t go any further. controlled_tail and controlled-evolution are exclusive. When both are used, the tail wins.
  --prerandomize tells it to do num_switches random switches before beginning the evolution. Use >100000 to get a mostly random keyboard layout as starting point.

- check_neo.py --best-random-layout <num of random layouts to try> [--prerandomize <num_switches>] [-q]
  --prerandomize selects the number of random switches to do to get a random keyboard.

- ./check_neo.py --check "[[('^'),('1'),('2'),('3'),('4'),('5'),('6'),('7'),('8'),('9'),('0'),('-'),('\\`'),('←')], # Zahlenreihe (0)
[('⇥'),('x'),('v'),('l'),('c'),('w'),('k'),('h'),('g'),('f'),('q'),('ß'),('´'),()], # Reihe 1
[('⇩'),('u'),('i'),('a'),('e'),('o'),('s'),('n'),('r'),('t'),('d'),('y'),('⇘'),('\\n')], # Reihe 2
[('⇧'),(),('ü'),('ö'),('ä'),('p'),('z'),('b'),('m'),(','),('.'),('j'),('⇗')],        # Reihe 3
[(), (), (), (' '), (), (), (), ()] # Reihe 4 mit Leertaste
]" [-q]
  check the layout passed on the commandline (mind the shell escapes!)

- check_neo.py [-v] [-q] --check-string "öckäy zhmlß,
atieo dsnru.
xpfüq bgvwj"
  check a layout string for layer 1.

- check_neo.py --test (run doctests)

Note: If --prerandomize is set to 1000000 or more, it just does a real shuffle instead of prerandomizing.

"""

from design import __design__

__doc__ += __usage__ + __design__

__version__ = "0.1.2"

__copyright__ = """2010 © Arne Babenhauserheide

License: GPLv3 or later
"""

from sys import argv
# forced fileoutput instead of printing
if "-o" in argv:
    idx = argv.index("-o")
    FILE = argv[idx+1]
    argv = argv[:idx] + argv[idx+2:]
else:
    FILE = None

from termctrl import erase, priorline, write

def info(*args, **kwds):
    return print(*args, **kwds)

def result(*args, **kwds):
    if FILE is not None:
        with open(FILE, "a", encoding='utf-8') as f:
            for i in args:
                f.write(str(i) + " ")
            f.write("\n")
    else:
        info(*args, **kwds)

from math import log10, log
from pprint import pprint

from config import ABC, WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, COST_PER_KEY
from layout_base import FINGER_NAMES, Layout, Layouts
from layout_cost import get_all_data, letters_in_file_precalculated, load_per_finger, repeats_in_file_precalculated, total_cost, trigrams_in_file_precalculated
from layout_info import draw_keyboard_layout, short_number
from ngrams import read_file



# TODO: Split the different ways of evolution into evolve.py. Requirement: Don’t give any output.

### Evolution

def randomize_keyboard(layout, num_switches):
        """Do num_switches random keyswitches on the layout and
        @return: the randomized layout."""
        keypairs = []
        num_letters = len(ABC)
        if num_switches >= 1000:
            # for very high number of switches just do use shuffle.
            abc_list = list(ABC)
            abc_shuffled = list(ABC)
            shuffle(abc_shuffled)
            for i in range(num_letters):
                orig = abc_list[i]
                new = abc_shuffled[i]
                if orig != new and not orig+new in keypairs and not new+orig in keypairs:
                    new_in_list = abc_list.index(new)
                    abc_list[new_in_list] = orig
                    keypairs.append(orig+new)
        else:
            # incomplete shuffling (only find the given number of switches), slower because we need to avoid dupliates the hard way.
            max_unique_tries = 1000
            for i in range(num_switches):
                key1 = choice(ABC)
                key2 = choice(ABC)
                # get unique keypairs, the not nice but very easy to understand way.
                tries = 0
                while (key2 == key1 or key1+key2 in keypairs or key2+key1 in keypairs) and (num_switches <= num_letters or tries < max_unique_tries):
                    key1 = choice(ABC)
                    key2 = choice(ABC)
                    if num_switches > num_letters:
                        tries += log(len(keypairs)+1, 2) + 1
                keypairs.append(key1+key2)
                
        new_layout, switched_letters = layout.switch_keys(keypairs)
        return new_layout, keypairs, switched_letters

def find_the_best_random_keyboard(layout, letters, repeats, trigrams, num_tries, num_switches=1000, quiet=False):
        """Create num_tries random keyboards (starting from the layout and doing num_switches random keyswitches), compare them and only keep the best (by total_cost)."""
        lay, keypairs, switched_letters = randomize_keyboard(layout, num_switches)
        cost = total_cost(layout, letters=letters, repeats=repeats, trigrams=trigrams)[0]
        if not quiet:
            info("cost of the first random layout:", cost)
        for i in range(max(0, num_tries-1)):
            if not quiet:
                info("-", i, "/", num_tries)
            lay_tmp, keypairs, switched_letters = randomize_keyboard(layout, num_switches)
            cost_tmp = total_cost(lay_tmp, letters=letters, repeats=repeats, trigrams=trigrams)[0]
            if cost_tmp < cost:
                lay = lay_tmp
                cost = cost_tmp
                if not quiet:
                    info("better:", cost)
        return lay, cost

def random_evolution_step(letters, repeats, trigrams, num_switches, layout, cost, trigram_cost_dic, quiet):
        """Do one random switch. Keep it, if it is beneficial."""
        lay, keypairs, switched_letters = randomize_keyboard(layout, num_switches)
        new_cost, frep, pos_cost, new_trigram_cost_dic = total_cost(lay, letters=letters, switched_letters=switched_letters, repeats=repeats, trigrams=trigrams, trigram_cost_dic=trigram_cost_dic, max_cost=cost)[:4]
        if new_cost < cost:
            return lay, new_cost, cost - new_cost, keypairs, frep, pos_cost, new_trigram_cost_dic
        else:
            return layout, cost, 0, keypairs, frep, pos_cost, trigram_cost_dic

def controlled_evolution_step(letters, repeats, trigrams, num_switches, layout, cost, quiet, meter, cost_per_key=COST_PER_KEY):
    """Do the most beneficial change. Keep it, if the new layout is better than the old.

    TODO: reenable the doctests, after the parameters have settled, or pass ALL parameters through the functions.

    >>> data = read_file("testfile")
    >>> repeats = repeats_in_file(data)
    >>> letters = letters_in_file(data)
    >>> trigrams = trigrams_in_file(data)
    >>> #controlled_evolution_step(letters, repeats, trigrams, 1, Layouts.NEO2, "reo", 190, quiet=False, cost_per_key=TEST_COST_PER_KEY)

        # checked switch ('rr',) 201.4
        # checked switch ('re',) 181.4
        # checked switch ('ro',) 184.4
        # checked switch ('ee',) 201.4
        # checked switch ('eo',) 204.4
        # checked switch ('oo',) 201.4
        0.00019 finger repetition: 1e-06 position cost: 0.00015
        [['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]]
        ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 181.4, 8.599999999999994)
    >>> #controlled_evolution_step(letters, repeats, trigrams, 1, Layouts.NEO2, "reo", 25, False, cost_per_key=TEST_COST_PER_KEY)

        # checked switch ('rr',) 201.4
        # checked switch ('re',) 181.4
        # checked switch ('ro',) 184.4
        # checked switch ('ee',) 201.4
        # checked switch ('eo',) 204.4
        # checked switch ('oo',) 201.4
        worse ('oo',) ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'e', 'o', 's', 'n', 'r', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 25, 0)
    """

    # First create one long list of possible switches
    keypairs = []
    best_pairs = []
    for key1 in ABC:
        for key2 in ABC[ABC.index(key1)+1:]:
            keypairs.append(key1+key2)

    # then combine it into possible switch tuples (O(N²))
    switches = []
    for i in range(num_switches):
        switches.append([]) # layers
    for pair1 in keypairs:
        # pair 1 list
        for i in range(len(keypairs) ** min(1, num_switches - 1)): # ** (num_switches - 1)):
            switches[0].append(pair1) # [[1, 1, 1]]
        for i in range(min(1, num_switches - 1)): # num_switches - 1): # TODO: Make it work for num > 2.
            #for j in range(len(keypairs) ** max(0, (num_switches - 2))):
                for pair_x in keypairs: #[keypairs.index(pair1)+1:]:
                    # add additional possible pairs.
                    switches[i+1].append(pair_x) # [[1, 1, 1], [1, 2, 3]]
    switches = list(zip(*switches[:2]))

    # results for 1 step: [(cost, frep, pos_cost, layout), ...]
    step_results = []
    length = len(switches)
    for keypairs in switches:
        i += 1
        lay, switched_letters = layout.switch_keys(keypairs)
        new_cost, frep, pos_cost = total_cost(lay, letters=letters, repeats=repeats, cost_per_key=cost_per_key, trigrams=trigrams, max_cost=cost)[:3]
        step_results.append((new_cost, frep, pos_cost, keypairs, lay))
        if not quiet:
            tppl = (new_cost - cost)/sum((num for num, l in letters))
            freedom = new_cost - cost < cost/100
            if freedom: freedom = "less than 1% tppl"
            else: freedom = ""
            tppl = "{:+07,.2f}".format(tppl)
            info("#", tppl, ", ".join(keypairs), freedom)
        if meter:
            write('switch:  %4d/%4d'%(i,length))
    if meter:
        erase(); priorline()
    if min(step_results)[0] < cost:
        best = min(step_results)
        lay, new_cost, best_pairs = best[-1], best[0], best[-2]
        new_cost, frep, pos_cost = total_cost(lay, letters=letters, repeats=repeats, cost_per_key=cost_per_key, trigrams=trigrams, max_cost=cost)[:3]
        return lay, new_cost, cost - new_cost, best_pairs, frep, pos_cost
    else:
        return layout, cost, 0, keypairs, frep, pos_cost

def evolve(layout, letters, repeats, trigrams, iterations=3000, quiet=False, meter=False, controlled=False, controlled_tail=False, anneal=0, anneal_step=100, show_each_step=False):
    """Repeatedly switch a layout randomly and do the same with the new layout,
    if it provides a better total score. Can't be tested easily => Check the source.

    @param controlled: Do a slow controlled run, where all possible steps are checked and only the best is chosen?
    @param anneal: start by switching 1 + int(anneal) keypairs, reduce by 1 after anneal_step iterations.
    """
    cost, _, _, trigram_cost_dic = total_cost(layout, letters=letters, repeats=repeats, trigrams=trigrams)[:4]
    consecutive_fails = 0
    # take anneal_step steps for the first anneal level, too
    if anneal:
        anneal += 1
        anneal -= 1/anneal_step

    for i in range(iterations):
        if not controlled:
            # increase the size of the changes when the system seems to become stable (1000 consecutive fails: ~ 2*24*23 = every combination tried) to avoid deterministic purely local minima.
            if anneal > 0:
                step = int(anneal + 1)
                anneal -= 1/anneal_step
            else:
                step = int(log10(consecutive_fails + 1) / 3 + 1)
            lay, cost, better, keypairs, frep, pos_cost, trigram_cost_dic = random_evolution_step(letters, repeats, trigrams, step, layout, cost, trigram_cost_dic, quiet)
        else:
            step = int(consecutive_fails + 1)
            # only do the best possible step instead => damn expensive. For a single switch about 10 min per run.
            lay, cost, better, keypairs, frep, pos_cost = controlled_evolution_step(letters, repeats, trigrams, step, layout, cost, quiet, meter)
        if show_each_step:
            info(" # ", step, cost)
        if better:
            consecutive_fails = 0
            # save the good mutation
            layout = lay
            if not quiet:
                info(cost / 1000000, keypairs, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
                info(layout.to_layer_1_string())
        else:
            consecutive_fails += 1
            if not quiet:
                info("worse", keypairs, end = " ")
        if not quiet:
            info("- " + str(i) + " / " + str(iterations))
        if meter:
            write('steps:   %4d/%4d'%(i+1,iterations))
    if meter:
        print

    if controlled_tail:
        # second round: do controlled evolution steps, as long as they result in better layouts (do a full controlled optimization of the result).
        if not quiet:
            info("controlled evolution, until there’s no more to improve")
        better = True
        steps = 0
        while better:
            steps += 1
            if meter:
                erase(); write('tail:    %4d\n'%steps)
            # only do the best possible step instead => damn expensive. For a single switch about 10 min per run.
            lay, cost, better, keypairs, frep, pos_cost = controlled_evolution_step(letters, repeats, trigrams, 1, layout=layout, cost=cost, quiet=quiet, meter=meter)
            if better:
                # save the good mutation - yes, this could go at the start of the loop, but that wouldn’t be as clear.
                layout = lay
            if not quiet:
                info("-", steps, "/ ?", keypairs)
                info(lay.to_layer_1_string())
    if meter:
        erase()
        priorline()
        erase()
    return layout, cost




### UI ###




def print_layout_with_statistics(layout, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, trigrams=None, number_of_trigrams=None, print_layout=True, verbose=False, data=None, shorten_numbers=False, datapath=None, fingerstats=False, show_manual_penalty=True, show_neighboring_unbalance=True, show_asymmetric_bigrams=True, show_asymmetric_similar=True):
    """Print a layout along with statistics."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(
            data=data,
            letters=letters, number_of_letters=number_of_letters,
            repeats=repeats, number_of_bigrams=number_of_bigrams,
            trigrams=trigrams, number_of_trigrams=number_of_trigrams,
            datapath=datapath,
            layout=layout
        )

    res = "\n# Evolved Layout\n"
    
    def c(*args):
        """concatenate the args to a string similar to how print() does it, just simpler."""
        return " ".join((str(i) for i in args)) + "\n"

    if print_layout:
        res += c(layout.to_layer_1_string())
        res += c(draw_keyboard_layout(layout))

    # unweighted
    total, frep_num, cost, _, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand, hand_load = total_cost(layout, letters=letters, repeats=repeats, trigrams=trigrams)[:9]
    # weighted
    total, frep_num_w, cost_w, _, frep_num_top_bottom_w, neighboring_fings_w, fing_disbalance_w, no_handswitches_w, badly_positioned_w, line_change_same_hand_w, no_switch_after_unbalancing_w, hand_disbalance_w, manual_penalty_w, neighboring_unbalance_w, asymmetric_bigrams_w, asymmetric_similar_w, irregularity_w = total_cost(layout, letters=letters, repeats=repeats, trigrams=trigrams, return_weighted=True)[:17]

    if shorten_numbers:
        sn = short_number
    else:
        sn = str

    res += c("#", sn(total/max(1, number_of_letters)/100), "x100 total penalty per letter")
    res += c("#", sn(total / 10000000000), "x10 billion total penalty compared to notime-noeffort")
    res += c("#", sn(cost / max(1, number_of_letters)), "mean key position cost in file 1gramme.txt", "(", str(cost_w/1000000000), ")")
    res += c("#", sn(100 * frep_num / max(1, number_of_bigrams)), "% finger repeats in file 2gramme.txt", "(", str(frep_num_w/1000000000), ")")
    if verbose:
        res += c("#", sn(disbalance / 1000000), "million keystrokes disbalance of the fingers", "(", str(fing_disbalance_w/1000000000), ")")
        res += c("#", sn(100 * frep_top_bottom / max(1, number_of_bigrams)), "% finger repeats top to bottom or vice versa", "(", str(frep_num_top_bottom_w/1000000000), ")")
        res += c("#", sn(100 * no_handswitches / max(1, number_of_trigrams)), "% of trigrams have no handswitching (after direction change counted x", WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, ")", "(", str(no_handswitches_w/1000000000), ")")
        res += c("#", sn(line_change_same_hand / 1000000000), "billion (rows²/dist)² to cross", "(", str(line_change_same_hand_w/1000000000), ")")
        res += c("#", sn(abs(hand_load[0]/max(1, sum(hand_load)) - 0.5)), "hand disbalance (4% shift is too much). Left:", hand_load[0]/max(1, sum(hand_load)), "%, Right:", hand_load[1]/max(1, sum(hand_load)), "% (", str(hand_disbalance_w/1000000000), ")")
        res += c("#", sn(badly_positioned_w/1000000000), "badly positioned shortcut keys (weighted).")
        res += c("#", sn(no_switch_after_unbalancing_w/1000000000), "no handswitching after unbalancing key (weighted).")
        res += c("#", sn(neighboring_fings_w/1000000000), "movement pattern cost (weighted).")
        res += c("#", sn(asymmetric_bigrams_w/1000000000), "asymmetric bigram cost (weighted).")
        res += c("#", sn(irregularity_w/1000000000), "irregularity cost (weighted).")
    if show_manual_penalty and verbose: # TODO: remove ‘and verbose’ once there’s a CLI parameter for this.
        res += c("#", sn(manual_penalty_w/1000000000), "manually assigned bigram penalty (weighted)")
    if show_neighboring_unbalance and verbose: # TODO: remove ‘and verbose’ once there’s a CLI parameter for this.
        res += c("#", sn(neighboring_unbalance_w/1000000000), "unbalancing key after neighboring finger (weighted)")
    if show_asymmetric_bigrams and verbose: # TODO: remove ‘and verbose’ once there’s a CLI parameter for this.
        res += c("#", sn(asymmetric_bigrams_w/1000000000), "asymmetrc bigrams (weighted)")
    if show_asymmetric_similar and verbose: # TODO: remove ‘and verbose’ once there’s a CLI parameter for this.
        res += c("#", sn(asymmetric_similar_w/1000000000), "inconsistent symmetries of similar keys (weighted)")
    if fingerstats:
        # also print statistics
        # Finger-load:
        finger_load = load_per_finger(letters, layout=layout)
        finger_sum = sum(finger_load.values())
        no_thumbs = [int(1000*finger_load.get(name, 0)/finger_sum)/10 for name in FINGER_NAMES[:4]] + ["-"] + [int(1000*finger_load.get(name, 0)/finger_sum)/10 for name in FINGER_NAMES[6:]]
        res += c("# Finger load %:", *no_thumbs)
    result(res)
    return total/max(1, number_of_letters)/100

def find_a_qwertzy_layout(steps=100, prerandomize=100000, quiet=False, verbose=True, anneal=5, anneal_step=10):
    """Find a layout with values similar to qwertz."""
    info("# Qwertzing Layout")
    #data = read_file("/tmp/sskreszta")
    data1 = read_file("1gramme.txt")
    letters = letters_in_file_precalculated(data1)
    #letters = letters_in_file(data)
    datalen1 = sum([i for i, s in letters])

    data2 = read_file("2gramme.txt")
    repeats = repeats_in_file_precalculated(data2)
    #repeats = repeats_in_file(data)
    datalen2 = sum([i for i, s in repeats])

    data3 = read_file("3gramme.txt")
    trigrams = trigrams_in_file_precalculated(data3)
    number_of_trigrams = sum([i for i, s in trigrams])

    qwertz_layout = Layouts.QWERTZ

    if prerandomize:
        if not quiet:
            info("doing", prerandomize, "randomization switches.")
        lay, keypairs, switched_letters = randomize_keyboard(Layouts.NEO2, prerandomize)
    else: lay = Layouts.NEO2

    qvals = total_cost(qwertz_layout, letters=letters, repeats=repeats, trigrams=trigrams, return_weighted=True)

    #qhand_load = load_per_hand(letters, layout=Layouts.QWERTZ)

    def compare_with_qwertz(lay):
        """compare the layout with qwertz."""
        vals = total_cost(lay, letters=letters, repeats=repeats, trigrams=trigrams, return_weighted=True)
        #hand_load = load_per_hand(letters, layout=lay)
        diff = 0
        to_compare = zip(vals, qvals)
        for l,q in to_compare:
            diff += (l - q)**2
        return diff

    diff = compare_with_qwertz(lay)

    if anneal:
        anneal += 1.
        anneal -= 1./anneal_step

    for i in range(steps):
        if anneal > 0:
                step = int(anneal + 1)
                anneal -= 1/anneal_step
        else:
                step = 1
        l, keypairs, switched_letters = randomize_keyboard(lay, step)
        d = compare_with_qwertz(l)
        if d < diff:
            info("# qwertzer")
            info(l.to_layer_1_string())
            lay = l
            diff = d


    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)


def evolve_a_layout(starting_layout, steps, prerandomize, controlled, quiet, meter=False, verbose=False, controlled_tail=False, datafile=None, anneal=0, anneal_step=100, ngram_config=None, fingerstats=True, limit_ngrams=False, preselect_random=100, show_each_step=False):
    """Evolve a layout by selecting the fittest of random mutations step by step."""
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(datapath=datafile, ngram_config_path=ngram_config, layout=starting_layout)
    if limit_ngrams:
        letters = letters[:limit_ngrams]
        repeats = repeats[:limit_ngrams]
        trigrams = trigrams[:limit_ngrams]
        datalen1, datalen2, number_of_trigrams = [limit_ngrams]*3

    if preselect_random and prerandomize:
        if not quiet:
            info("creating", preselect_random, "randomized layouts and choosing the best.")
        lay, cost = find_the_best_random_keyboard(starting_layout, letters, repeats, trigrams, num_tries=preselect_random, num_switches=prerandomize, quiet=quiet and not show_each_step)
    elif prerandomize:
        if not quiet:
            info("doing", prerandomize, "prerandomization switches.")
        lay, keypairs, switched_letters = randomize_keyboard(starting_layout, prerandomize)
    else: lay = starting_layout

        
    lay, cost = evolve(lay, letters, repeats, trigrams, iterations=steps, quiet=quiet, meter=meter, controlled=controlled, controlled_tail = controlled_tail, anneal=anneal, anneal_step=anneal_step, show_each_step=show_each_step)

    return print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, fingerstats=fingerstats)


def evolution_challenge(layout, challengers=100, rounds=10, iterations=20, prerandomize=10000, quiet=False, controlled=False, datafile=None):
     """Run a challenge between many randomized layouts, then combine the best pseudo-genetically (random) and add them to the challenge."""
     # Data for evaluating layouts.
     letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(datapath=datafile, layout=layout)

     #: the maximum number of genetic combination tries to get a unique layout (no clone)
     max_unique_tries = 200

     layouts = [] # [(cost, lay), …]
     if not quiet:
         info("# create the", challengers, "starting layouts")
     for i in range(challengers):

         info("#", i, "of", challengers)
         lay, keypairs, switched_letters = randomize_keyboard(layout, prerandomize)
         lay, cost = evolve(lay, letters, repeats, trigrams, iterations=iterations, quiet=True)
         layouts.append((cost, lay))

     # run the challenge
     for round in range(rounds):
         # sort and throw out the worst
         layouts.sort()
         if not quiet:
             info("\n# round", round)
             info("# top five")
             for cost, lay in layouts:
                 print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
         info("\n# killing the worst", int(challengers * 3/4)-1, "layouts")
         layouts = layouts[:int(challengers / 4)+1]

         # combine the best and worst to get new ones.
         info("\n# breeding new layouts")
         for i in range(int(challengers/8)):
            info(i, "of", int(challengers/4-1), "from weak and strong")
            new = layouts[i][1].combine_genetically(layouts[-i - 1][1])
            # evolve, then append
            new, cost = evolve(new, letters, repeats, trigrams, iterations=iterations, quiet=True)
            # make sure we have no clones :)
            tries = 0
            while (cost, new) in layouts and tries < max_unique_tries:
                new = layouts[i][1].combine_genetically(layouts[-i - 1][1])
                new, cost = evolve(layout, letters, repeats, trigrams, iterations=iterations, quiet=True)
                tries += 1
            layouts.append((cost, new))

        # also combine the best one with the upper half
         for i in range(max(0, int(challengers/8))):
            info(i+int(challengers/8), "of", int(challengers/4-1), "from the strongest with the top half")
            new = layouts[0][1].combine_genetically(layouts[i+1][1])
            new, cost = evolve(new, letters, repeats, trigrams, iterations=iterations, quiet=True)
            # make sure we have no clones :)
            tries = 0
            while (cost, new) in layouts and tries < max_unique_tries:
                new = layouts[0][1].combine_genetically(layouts[i+1][1])
                new, cost = evolve(new, letters, repeats, trigrams, iterations=iterations, quiet=True)
                tries += 1
            layouts.append((cost, new))

         # and new random ones
         info("\n# and fill up the ranks with random layouts")
         for i in range(challengers - len(layouts)):
             info(i, "of", int(challengers/2))
             lay, keypairs, switched_letters = randomize_keyboard(layout, prerandomize)
             lay, cost = evolve(lay, letters, repeats, trigrams, iterations=iterations, quiet=True)
             # make sure we have no clones :)
             tries = 0
             while (cost, lay) in layouts and tries < max_unique_tries:
                 lay, keypairs, switched_letters = randomize_keyboard(layout, prerandomize)
                 lay, cost = evolve(lay, letters, repeats, trigrams, iterations=iterations, quiet=True)
                 tries += 1
             layouts.append((cost, lay))

     info("# Top 3")
     layouts.sort()

     for num, name in [(0, "\n# gold"), (1, "\n# silver"), (2, "\n# bronze")][:len(layouts)]:
         cost, lay = layouts[num]
         info(name)
         print_layout_with_statistics(lay, letters, repeats, datalen1, datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)

def best_random_layout(number, prerandomize, quiet=False, datafile=None, layout=Layouts.NEO2):
    """Select the best of a number of randomly created layouts."""
    info("Selecting the best from", number, "random layouts.")
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(datapath=datafile, layout=layout)

    if prerandomize:
        lay, cost = find_the_best_random_keyboard(layout, letters, repeats, trigrams, num_tries=number, num_switches=prerandomize, quiet=quiet)
    else:
        lay, cost = find_the_best_random_keyboard(layout, letters, repeats, trigrams, num_tries=number, quiet=quiet)

    info("\nBest of the random layouts")
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)


def compare_a_layout(quiet, verbose, datafile=None, layout=None, fingerstats=False):
    """Check the performance of a layout, optionally scoring it against Qwertz and other layouts."""
    neo_layout = Layouts.NEO2
    if layout is None:
        layout = neo_layout
    if layout.blueprint is neo_layout.blueprint:
        info("Neo")
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(datapath=datafile, layout=layout)

    print_layout_with_statistics(layout, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)

    if not quiet:
        info("\nQwertz for comparision")
        print_layout_with_statistics(Layouts.QWERTZ, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd AdNW")
        print_layout_with_statistics(Layouts.AdNW, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd KOY")
        print_layout_with_statistics(Layouts.KOY, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd CRY")
        print_layout_with_statistics(Layouts.CRY, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd Bone")
        print_layout_with_statistics(Layouts.BONE, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd Dvorak")
        print_layout_with_statistics(Layouts.DVORAK, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd Colemak")
        print_layout_with_statistics(Layouts.COLEMAK, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd Workman")
        print_layout_with_statistics(Layouts.WORKMAN, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd Capewell")
        print_layout_with_statistics(Layouts.CAPEWELL, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)
        info("\nAnd Carpalx QGMLWY")
        print_layout_with_statistics(Layouts.QGMLWY, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True, fingerstats=fingerstats)

# for compatibility
check_the_neo_layout = compare_a_layout

def check_a_layout_from_shell(layout, quiet, verbose, datafile=None, fingerstats=False):
    """Check a layout we get passed as shell argument."""
    print_layout_with_statistics(layout, verbose=verbose, datapath=datafile, shorten_numbers=True, fingerstats=fingerstats)


def check_a_layout_string_from_shell(layout_string, quiet, verbose, base_layout=Layouts.NEO2, datafile=None, fingerstats=False):
    """Check a string passed via shell and formatted as

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj

    or

    qwert zuiopü+
    asdfg hjklöä
    <yxcvb nm,.-
    """
    layout = Layout.from_string(layout_string, base_layout)
    print_layout_with_statistics(layout, verbose=verbose, datapath=datafile, shorten_numbers=True, fingerstats=fingerstats)

### Self-Test

if __name__ == "__main__":
    if "--test" in argv:
        from doctest import testmod
        testmod()
        exit()

    from optparse import OptionParser

    parser = OptionParser(description="Check and evolve keyboard layouts. Actions can’t be combined, the other options and arguments can. Without action, it checks layouts.")
    # actions
    parser.add_option("--best-random-layout", dest="best_random_layout", type="int", default=0,
                      help="(action) create the given number of random layouts and show the best one", metavar="number")
    parser.add_option("--challenge", dest="challenge_rounds", type="int", default=0,
                      help="(action) do an evolution challenge for the given number of rounds. Slow", metavar="rounds")
    parser.add_option("--check", dest="check",
                      help="(action)check a layout from shell. ignores --base-blueprint*", metavar="layout")
    parser.add_option("--check-string", dest="check_string",
                      help="(action) check a layout_string from shell", metavar="layout_string")
    parser.add_option("--evolve", dest="evolve", type="int", default=0,
                      help="(action) do the given number of random mutation steps", metavar="number")

    # options
    parser.add_option("--base-blueprint", dest="base_blueprint", default=None,
                      help="take the given layout as base-blueprint", metavar="layout")
    parser.add_option("--base-name", dest="base_name", default=None,
                      help="take the named layout as base. I.e.: Layouts.NEO2 or Layouts.QWERTZ", metavar="layout_name")
    parser.add_option("--base-string", dest="base_string", default=None,
                      help="take the given layout as base for layer 1. Compatible with --base-blueprint and --base-name", metavar="layout")
    parser.add_option("--challenge-evolution-steps", dest="challenge_evolution_steps", type="int", default=3,
                      help="the number of individual evolution steps to take between evolution challenge rounds", metavar="number")
    parser.add_option("--challengers", dest="challengers", type="int", default=16,
                      help="the number of challengers for an evolution challenge", metavar="number")
    parser.add_option("-f", "--file", dest="file",
                      help="get the ngram data from the given textfile", metavar="textfile")
#    parser.add_option("--ngrams", dest="ngram_config",
#                      help="take the ngram sources from the config file", metavar="ngram.config")
    parser.add_option("--prerandomize", dest="prerandomize", type="int", default=1000,
                      help="do the given number of randomization steps", metavar="number")
    parser.add_option("--anneal", dest="anneal", type="int", default=0,
                      help="start with number additional keyswitches per iteration and slowly reduce them (simulated annealing)", metavar="number")
    parser.add_option("--anneal-step", dest="anneal_step", type="int", default=100,
                      help="the number of steps after which to reduce the annealing switches by 1", metavar="number")


    # arguments
    parser.add_option("--controlled",
                      action="store_true", dest="controlled_evolution", default=False,
                      help="check all possible mutations at each step and only take the best")
    parser.add_option("--controlled-tail",
                      action="store_true", dest="controlled_tail", default=False,
                      help="do a controlled evolution after the random evolution steps")
    parser.add_option("--fingerstats",
                      action="store_true", dest="fingerstats", default=False,
                      help="Show statistics on the finger load distribution")
    parser.add_option("--progress",
                      action="store_true", dest="progress", default=False,
                      help="Show a progress meter. Does not work on Windows.")
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet", default=False,
                      help="don’t print progress messages to stdout")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print more detailed layout statistics")
    parser.add_option("--print-raw-layout",
                      action="store_true", default=False,
                      help="print the raw internal layout representation")

    (options, args) = parser.parse_args()

    # post process options
    if options.base_blueprint:
        options.base_blueprint = eval(options.base_blueprint)
        layout = Layout(options.base_blueprint)
    elif options.base_name:
        options.base_blueprint = eval(options.base_name)
        layout = Layout(options.base_blueprint)
    if not options.base_blueprint:
        layout = Layouts.NEO2

    if options.base_string:
        # base + base-string: base for the surroundings,
        # base-string for the base layer.
        layout = Layout.from_string(options.base_string, Layouts.NEO2)

    if options.progress:
        options.quiet = True

    if options.check:
        options.check = eval(options.check)

    # act

    if options.check:
        check_a_layout_from_shell(options.check, quiet=options.quiet, verbose=options.verbose, datafile=options.file, fingerstats=options.fingerstats)

    elif options.print_raw_layout:
        if not options.check_string:
            print("please give the layout to print with --check-string")
        pprint(Layout.from_string(options.check_string, layout))
        
    elif options.check_string:
        check_a_layout_string_from_shell(options.check_string, quiet=options.quiet, verbose=options.verbose, datafile=options.file, base_layout=layout, fingerstats=options.fingerstats)

    elif options.evolve:
        evolve_a_layout(layout, steps=options.evolve, prerandomize=options.prerandomize, quiet=options.quiet, controlled=options.controlled_evolution, verbose=options.verbose, controlled_tail=options.controlled_tail, datafile=options.file, anneal=options.anneal, anneal_step=options.anneal_step, meter=options.progress)

    elif options.best_random_layout:
        best_random_layout(number=options.best_random_layout, prerandomize=options.prerandomize, quiet=options.quiet, datafile=options.file, layout=layout)

    elif options.challenge_rounds:
            evolution_challenge(layout,
                                rounds=options.challenge_rounds,
                                iterations=options.challenge_evolution_steps,
                                challengers=options.challengers,
                                prerandomize=options.prerandomize,
                                datafile=options.file,
                                controlled=options.controlled_evolution)
    
    else:
        check_the_neo_layout(quiet=options.quiet, verbose=options.verbose, datafile=options.file, layout=layout, fingerstats=options.fingerstats)

