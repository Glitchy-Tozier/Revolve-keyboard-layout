#!/usr/bin/env python3

"""Optimize keyboard layouts evolutionally (with mutations).

"""
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

from layout_cost import *

# TODO: Split the different ways of evolution into evolve.py. Requirement: Don’t give any output.

### Evolution

def switch_keys(keypairs, layout=NEO_LAYOUT):
    """Switch keys in the layout, so we don't have to fiddle with actual layout files.

    >>> lay = switch_keys([], layout = NEO_LAYOUT)
    >>> lay == NEO_LAYOUT
    True
    >>> lay = switch_keys(["lx", "wq"], layout = NEO_LAYOUT)
    >>> get_key((1, 1, 0), layout=lay)
    'l'
    >>> get_key((1, 3, 0), layout=lay)
    'x'
    >>> get_key((1, 5, 0), layout=lay)
    'q'
    >>> get_key((1, 10, 0), layout=lay)
    'w'
    >>> find_key("l", layout=lay) == (1, 1, 0)
    True
    >>> NEO_LAYOUT_lxwq == lay[:5]
    True
    >>> lay = switch_keys(["lx"], layout = NEO_LAYOUT)
    >>> NEO_LAYOUT_lx == lay[:5]
    True
    >>> a = find_key("a", layout=lay)
    >>> lay = switch_keys(["ab"], layout=lay)
    >>> a == find_key("b", layout=lay)
    True
    """
    lay = deepcopy(layout)
    for pair in keypairs:
        pos0 = find_key(pair[0], layout=lay)
        pos1 = find_key(pair[1], layout=lay)
        tmp0 = pair[1] + lay[pos0[0]][pos0[1]][1:]
        tmp1 = pair[0] + lay[pos1[0]][pos1[1]][1:]
        lay[pos0[0]][pos0[1]] = tmp0
        lay[pos1[0]][pos1[1]] = tmp1
        update_letter_to_key_cache_multiple(pair, layout=lay)
    
    return lay

def randomize_keyboard(abc, num_switches, layout=NEO_LAYOUT): 
        """Do num_switches random keyswitches on the layout and
        @return: the randomized layout."""
        from random import choice
        keypairs = []
        for i in range(num_switches):
            key1 = choice(abc)
            key2 = choice(abc)
            # get unique keypairs, the not nice but very easy to understand way.
            while key2 == key1 or key1+key2 in keypairs or key2+key1 in keypairs:
                key1 = choice(abc)
                key2 = choice(abc)
            keypairs.append(key1+key2)
        lay = switch_keys(keypairs, layout=deepcopy(layout))
        return lay, keypairs

def find_the_best_random_keyboard(letters, repeats, trigrams, num_tries, num_switches=1000, layout=NEO_LAYOUT, abc=abc, quiet=False): 
        """Create num_tries random keyboards (starting from the layout and doing num_switches random keyswitches), compare them and only keep the best (by total_cost)."""
        lay, keypairs = randomize_keyboard(abc, num_switches, layout)
        cost = total_cost(letters=letters, repeats=repeats, layout=lay, trigrams=trigrams)[0]
        if not quiet: 
            info("cost of the first random layout:", cost)
        for i in range(max(0, num_tries-1)): 
            if not quiet: 
                info("-", i, "/", num_tries)
            lay_tmp, keypairs = randomize_keyboard(abc, num_switches, layout)
            cost_tmp = total_cost(letters=letters, repeats=repeats, layout=lay_tmp, trigrams=trigrams)[0]
            if cost_tmp < cost: 
                lay = lay_tmp
                cost = cost_tmp
                if not quiet: 
                    info("better:", cost)
        return lay, cost	    

def random_evolution_step(letters, repeats, trigrams, num_switches, layout, abc, cost, quiet): 
        """Do one random switch. Keep it, if it is beneficial."""
        lay, keypairs = randomize_keyboard(abc, num_switches, layout)
        new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, trigrams=trigrams)[:3]
        if new_cost < cost:
            if not quiet: 
                info(cost / 1000000, keypairs, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
                info(format_layer_1_string(lay))
            return lay, new_cost, cost - new_cost
        else:
            if not quiet: 
                info("worse", keypairs, end = " ")
            return layout, cost, 0

def controlled_evolution_step(letters, repeats, trigrams, num_switches, layout, abc, cost, quiet, cost_per_key=COST_PER_KEY): 
    """Do the most beneficial change. Keep it, if the new layout is better than the old.

    TODO: reenable the doctests, after the parameters have settled, or pass ALL parameters through the functions. 
    
    >>> data = read_file("testfile")
    >>> repeats = repeats_in_file(data)
    >>> letters = letters_in_file(data)
    >>> trigrams = trigrams_in_file(data)
    >>> #controlled_evolution_step(letters, repeats, trigrams, 1, NEO_LAYOUT, "reo", 190, quiet=False, cost_per_key=TEST_COST_PER_KEY)
    
    # checked switch ('rr',) 201.4
    # checked switch ('re',) 181.4
    # checked switch ('ro',) 184.4
    # checked switch ('ee',) 201.4
    # checked switch ('eo',) 204.4
    # checked switch ('oo',) 201.4
    0.00019 finger repetition: 1e-06 position cost: 0.00015
    [['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]]
    ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'r', 'o', 's', 'n', 'e', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 181.4, 8.599999999999994)
    >>> #controlled_evolution_step(letters, repeats, trigrams, 1, NEO_LAYOUT, "reo", 25, False, cost_per_key=TEST_COST_PER_KEY)
    
    # checked switch ('rr',) 201.4
    # checked switch ('re',) 181.4
    # checked switch ('ro',) 184.4
    # checked switch ('ee',) 201.4
    # checked switch ('eo',) 204.4
    # checked switch ('oo',) 201.4
    worse ('oo',) ([['^', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '`', ()], [(), 'x', 'v', 'l', 'c', 'w', 'k', 'h', 'g', 'f', 'q', 'ß', '´', ()], ['⇩', 'u', 'i', 'a', 'e', 'o', 's', 'n', 'r', 't', 'd', 'y', '⇘', '\\n'], ['⇧', (), 'ü', 'ö', 'ä', 'p', 'z', 'b', 'm', ',', '.', 'j', '⇗'], [(), (), (), ' ', (), (), (), ()]], 25, 0)
    """
    from random import choice
    # First create one long list of possible switches
    keypairs = []
    for key1 in abc: 
        for key2 in abc[abc.index(key1)+1:]: 
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
    for keypairs in switches: 
        lay = switch_keys(keypairs, layout=deepcopy(layout))
        new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, cost_per_key=cost_per_key, trigrams=trigrams)[:3]
        step_results.append((new_cost, frep, pos_cost, lay))
        if not quiet: 
            info("# checked switch", keypairs, new_cost)
    if min(step_results)[0] < cost:
        lay, new_cost = min(step_results)[-1], min(step_results)[0]
        if not quiet: 
            new_cost, frep, pos_cost = total_cost(letters=letters, repeats=repeats, layout=lay, cost_per_key=cost_per_key, trigrams=trigrams)[:3]
            info(cost / 1000000, "finger repetition:", frep / 1000000, "position cost:", pos_cost / 1000000)
            info(format_layer_1_string(lay))
        return lay, new_cost, cost - new_cost
    else: 
        if not quiet: 
            info("worse", keypairs, end = " ")
        return layout, cost, 0

def evolve(letters, repeats, trigrams, layout=NEO_LAYOUT, iterations=400, abc=abc, quiet=False, controlled=False):
    """Repeatedly switch a layout randomly and do the same with the new layout,
    if it provides a better total score. Can't be tested easily => Check the source.

    To only mutate a subset of keys, just pass them as
    @param abc: the keys to permutate over.
    @param controlled: Do a slow controlled run, where all possible steps are checked and only the best is chosen? 
    """
    from math import log10
    cost = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[0]
    consecutive_fails = 0
    for i in range(iterations): 
        if not controlled: 
            # increase the size of the changes when the system seems to become stable (1000 consecutive fails: ~ 2*24*23 = every combination tried) to avoid deterministic purely local minima.
            step = int(log10(consecutive_fails + 1) / 3 + 1)
            lay, cost, better = random_evolution_step(letters, repeats, trigrams, step, layout, abc, cost, quiet)
        else: 
            step = int(consecutive_fails / 2 + 1)
            # only do the best possible step instead => damn expensive. For a single switch about 10 min per run. 
            lay, cost, better = controlled_evolution_step(letters, repeats, trigrams, step, layout, abc, cost, quiet)
        if better:
            consecutive_fails = 0
            # save the good mutation
            layout = lay
        else:
            consecutive_fails += 1
        if not quiet: 
            info("- " + str(i) + " / " + str(iterations))
    
    return layout, cost


def evolve_with_controlled_tail(letters, repeats, trigrams, layout=NEO_LAYOUT, iterations=400, abc=abc, quiet=False):
    """Repeatedly switch a layout randomly and do the same with the new layout,
    if it provides a better total score. Can't be tested easily => Check the source.

    After the iterations, do a controlled evolution, until nothing can be improved anymore.

    Different from the normal evolvution, this never increases the step size (which has proven not to be very effective for the normal evolution and is incompatible with the thought of doing controlled optimization up to the end.

    To only mutate a subset of keys, just pass them as
    @param abc: the keys to permutate over.
    @param controlled: Do a slow controlled run, where all possible steps are checked and only the best is chosen? 
    """
    from math import log10
    cost = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[0]

    # first round: do (numper of iterations) mutation tries.
    consecutive_fails = 0
    if not quiet: 
        info("doing", iterations, "random mutations")
    for i in range(iterations): 
        # increase the size of the changes when the system seems to become stable (1000 consecutive fails: ~ 2*24*23 = every combination tried) to avoid deterministic purely local minima.
        step = int(log10(consecutive_fails + 1) / 3 + 1)
        lay, cost, better = random_evolution_step(letters, repeats, trigrams, step, layout, abc, cost, quiet)
        if better:
            # save the good mutation
            layout = lay
            consecutive_fails = 0
        else:
            consecutive_fails += 1
        if not quiet: 
            info("-", i, "/", iterations)

    # second round: do controlled evolution steps, as long as they result in better layouts (do a full controlled optimization of the result).
    if not quiet: 
        info("controlled evolution, until there’s no more to improve")
    better = True
    steps = 0
    while better: 
        # only do the best possible step instead => damn expensive. For a single switch about 10 min per run. 
        lay, cost, better = controlled_evolution_step(letters, repeats, trigrams, 1, layout=layout, abc=abc, cost=cost, quiet=quiet)
        if better:
            # save the good mutation - yes, this could go at the start of the loop, but that wouldn’t be as clear.
            layout = lay
        if not quiet: 
            info("-", steps, "/ ?", )
    
    return layout, cost


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


### UI ###

def format_keyboard_layout(layout):
    """Format a keyboard layout to look like a real keyboard."""
    neo = """
┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐
│ ^ │ 1 │ 2 │ 3 │ 4 │ 5 │ 6 │ 7 │ 8 │ 9 │ 0 │ - │ ` │ Back │
├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬────┤
│Tab  │ x │ v │ l │ c │ w │ k │ h │ g │ f │ q │ ß │ ´ │ Ret│
├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┐   │
│M3    │ u │ i │ a │ e │ o │ s │ n │ r │ t │ d │ y │ M3│   │
├────┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┴───┤
│Ums │ M4│ ü │ ö │ ä │ p │ z │ b │ m │ , │ . │ j │  Umsch  │
├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴─┬─┴──┬┴───┼────┬────┤
│Strg│ Fe │ Al │      Leerzeichen      │ M4 │ Fe │ Me │Strg│
└────┴────┴────┴───────────────────────┴────┴────┴────┴────┘

    """
    lay = "┌───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬───┬──────┐\n"
    lay +="│ "
    lay += " │ ".join([l[0] for l in layout[0]])
    lay += "    │\n" 
    lay += "├───┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬────┤\n"
    lay += "│   " 
    lay += " │ ".join([l[0] for l in layout[1][:-1]])
    lay += " │ Ret│\n"
    lay += "├─────┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┬──┴┐   │\n"
    lay += "│    "
    if layout[2][-2]: 
        lay += " │ ".join([l[0] for l in layout[2][:-1]])
    else:
        lay += " │ ".join([l[0] for l in layout[2][:-2]])
        lay += " │  "
    lay += " │   │\n"
    lay += "├────┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴─┬─┴───┴───┤\n"
    if layout[3][1]:
        lay += "│  "
        lay += " │ ".join([l[0] for l in layout[3]])
    else:
        lay +="│  ⇧ │ M4│ "
        lay += " │ ".join([l[0] for l in layout[3][2:]])
    lay += "       │\n"
    lay += """├────┼───┴┬──┴─┬─┴───┴───┴───┴───┴───┴─┬─┴──┬┴───┼────┬────┤
│Strg│ Fe │ Alt│      Leerzeichen      │ M4 │ Fe │ Me │Strg│
└────┴────┴────┴───────────────────────┴────┴────┴────┴────┘"""
    return lay
    

def short_number(s, letters=8):
    """shorten a number to the given number of letters"""
    if not "e" in str(s): 
        return str(s)[:letters]
    else:
        idx = min(letters-4, str(s).index("e"))
        idx = max(0, idx)
        return str(s)[:idx] + str(s)[-4:]

def print_layout_with_statistics(layout, letters=None, repeats=None, number_of_letters=None, number_of_bigrams=None, print_layout=True, trigrams=None, number_of_trigrams=None, verbose=False, data=None, shorten_numbers=False):
    """Print a layout along with statistics."""
    letters, number_of_letters, repeats, number_of_bigrams, trigrams, number_of_trigrams = get_all_data(
        data=data, 
        letters=letters, number_of_letters=number_of_letters,
        repeats=repeats, number_of_bigrams=number_of_bigrams,
        trigrams=trigrams, number_of_trigrams=number_of_trigrams
        )

    if print_layout:
        result(format_layer_1_string(layout))
        result(format_keyboard_layout(layout))
        #from pprint import pprint
        #pprint(layout[:5])

    # unweighted
    total, frep_num, cost, frep_top_bottom, disbalance, no_handswitches, line_change_same_hand = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams)[:7]
    # weighted
    total, cost_w, frep_num_w, frep_num_top_bottom_w, neighboring_fings_w, fing_disbalance_w, no_handswitches_w, badly_positioned_w, line_change_same_hand_w, no_switch_after_unbalancing_w = total_cost(letters=letters, repeats=repeats, layout=layout, trigrams=trigrams, return_weighted=True)[:10]

    hand_load = load_per_hand(letters, layout=layout)

    if shorten_numbers: 
        sn = short_number
    else:
        sn = str

    result("#", sn(total/max(1, number_of_letters)), "total penalty per letter")
    result("#", sn(total / 1000000000), "billion total penalty compared to notime-noeffort")
    result("#", sn(cost / max(1, number_of_letters)), "mean key position cost in file 1gramme.txt", "(", str(cost_w/1000000000), ")")
    result("#", sn(100 * frep_num / max(1, number_of_bigrams)), "% finger repeats in file 2gramme.txt", "(", str(frep_num_w/1000000000), ")")
    if verbose: 
        result("#", sn(disbalance / 1000000), "million keystrokes disbalance of the fingers", "(", str(fing_disbalance_w/1000000000), ")")
        result("#", sn(100 * frep_top_bottom / max(1, number_of_bigrams)), "% finger repeats top to bottom or vice versa", "(", str(frep_num_top_bottom_w/1000000000), ")")
        result("#", sn(100 * no_handswitches / max(1, number_of_trigrams)), "% of trigrams have no handswitching (after direction change counted x", WEIGHT_NO_HANDSWITCH_AFTER_DIRECTION_CHANGE, ")", "(", str(no_handswitches_w/1000000000), ")")
        result("#", sn(line_change_same_hand / 1000000000), "billion (rows²/dist)² to cross", "(", str(line_change_same_hand_w/1000000000), ")")
        result("#", sn(abs(hand_load[0]/max(1, sum(hand_load)) - 0.5)), "hand disbalance. Left:", hand_load[0]/max(1, sum(hand_load)), "%, Right:", hand_load[1]/max(1, sum(hand_load)), "%")
        result("#", sn(badly_positioned_w/1000000000), "badly positioned shortcut keys (weighted).")
        result("#", sn(no_switch_after_unbalancing_w/1000000000), "no handswitching after unbalancing key (weighted).")
        result("#", sn(neighboring_fings_w/1000000000), "movement pattern cost (weighted).")


def find_a_qwertzy_layout(steps, prerandomize, quiet, verbose):
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
   
    if prerandomize:
        if not quiet:
            info("doing", prerandomize, "randomization switches.")
        lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT)
    else: lay = NEO_LAYOUT

    qvals = total_cost(letters=letters, repeats=repeats, layout=QWERTZ_LAYOUT, trigrams=trigrams, return_weighted=True)

    qhand_load = load_per_hand(letters, layout=QWERTZ_LAYOUT)

    def compare_with_qwertz(lay, base=QWERTZ_LAYOUT):
        """compare the layout with qwertz."""
        vals = total_cost(letters=letters, repeats=repeats, layout=lay, trigrams=trigrams, return_weighted=True)
        hand_load = load_per_hand(letters, layout=lay)
        diff = 0
        to_compare = zip(vals, qvals)
        for l,q in to_compare: 
            diff += (l - q)**2
        return diff

    diff = compare_with_qwertz(lay)

    for i in range(steps):
        lay = deepcopy(lay)
        l, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=lay)
        d = compare_with_qwertz(l)
        if d < diff:
            info("# qwertzer")
            info(format_layer_1_string(l))
            lay = deepcopy(l)
            diff = d

    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)
    

def evolve_a_layout(steps, prerandomize, controlled, quiet, verbose, controlled_tail, starting_layout=NEO_LAYOUT, data=None):
    """Evolve a layout by selecting the fittest of random mutations step by step."""
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(data=data)

    if prerandomize:
        if not quiet:
            info("doing", prerandomize, "prerandomization switches.")
        lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=starting_layout)
    else: lay = starting_layout

    if controlled_tail:
        lay, cost = evolve_with_controlled_tail(letters, repeats, trigrams, layout=lay, iterations=steps, quiet=quiet)
    else: 
        lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=steps, quiet=quiet, controlled=controlled)
    
    result("\n# Evolved Layout")
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose)


def evolution_challenge(layout=NEO_LAYOUT, challengers=100, rounds=10, iterations=400, abc=abc, prerandomize=10000, quiet=False, controlled=False, data=None):
     """Run a challenge between many randomized layouts, then combine the best pseudo-genetically (random) and add them to the challenge."""
     # Data for evaluating layouts.
     letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(data=data)

     from pprint import pprint

     layouts = [] # [(cost, lay), …]
     if not quiet:
         info("# create the", challengers, "starting layouts")
     for i in range(challengers):
         info("#", i, "of", challengers)
         lay, keypairs = randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT)
         lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=iterations, quiet=True)
         layouts.append((cost, lay))
     # run the challenge
     for round in range(rounds): 
         # sort and throw out the worst
         layouts.sort()
         if not quiet:
             info("# round", round)
             info("# top five")
             for cost, lay in layouts[:5]:
                 print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
         layouts = deepcopy(layouts[:int(challengers / 4)+1])
         # combine the best and worst to get new ones.
         info("breeding new layouts")
         for i in range(int(challengers/8)):
            info(i, "of", int(challengers/4), "from weak and strong")
            new = deepcopy(combine_genetically(layouts[i][1], layouts[-i - 1][1]))
            # evolve, then append
            new, cost = deepcopy(evolve(letters, repeats, trigrams, layout=new, iterations=iterations, quiet=True))
            layouts.append((cost, new))
            # also combine the best one with the upper half
         for i in range(max(0, int(challengers/8))):
            info(i+int(challengers/8), "of", int(challengers/4), "from the strongest with the top half")
            new = deepcopy(combine_genetically(layouts[0][1], layouts[i+1][1]))
            new, cost = evolve(letters, repeats, trigrams, layout=new, iterations=iterations, quiet=True)
            layouts.append((cost, new))
         # and new random ones
         info("and fill up the ranks with random layouts")
         for i in range(challengers - len(layouts)):
             info(i, "of", challengers - len(layouts))
             lay, keypairs = deepcopy(randomize_keyboard(abc, num_switches=prerandomize, layout=NEO_LAYOUT))
             lay, cost = evolve(letters, repeats, trigrams, layout=lay, iterations=iterations, quiet=True)
             layouts.append((cost, lay))

     info("# Top 3")
     layouts.sort()

     for num, name in [(0, "gold"), (1, "silver"), (2, "bronze")][:len(layouts)]: 
         cost, lay = layouts[num]
         info(name)
         print_layout_with_statistics(lay, letters, repeats, datalen1, datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)

def best_random_layout(number, prerandomize, quiet=False, data=None, layout=NEO_LAYOUT):
    """Select the best of a number of randomly created layouts."""
    info("Selecting the best from", number, "random layouts.")
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(data=data)
     
    if prerandomize: 
        lay, cost = find_the_best_random_keyboard(letters, repeats, trigrams, num_tries=number, num_switches=prerandomize, layout=layout, abc=abc, quiet=quiet)
    else: 
        lay, cost = find_the_best_random_keyboard(letters, repeats, trigrams, num_tries=number, layout=layout, abc=abc, quiet=quiet)
        
    info("\nBest of the random layouts")
    print_layout_with_statistics(lay, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams)
    

def compare_a_layout(quiet, verbose, data=None, layout=NEO_LAYOUT):
    """Check the performance of the neo layout, optionally scoring it against Qwertz."""
    if layout == NEO_LAYOUT: 
        info("Neo")
    letters, datalen1, repeats, datalen2, trigrams, number_of_trigrams = get_all_data(data=data)
     
    print_layout_with_statistics(layout, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, print_layout=not quiet, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
    
    if not quiet:
        info("\nQwertz for comparision")
        print_layout_with_statistics(QWERTZ_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
        info("\nAnd the Nordtast Layout")
        print_layout_with_statistics(NORDTAST_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
        info("\nAnd Dvorak")
        print_layout_with_statistics(DVORAK_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)
        info("\nAnd Colemak")
        print_layout_with_statistics(COLEMAK_LAYOUT, letters=letters, repeats=repeats, number_of_letters=datalen1, number_of_bigrams=datalen2, trigrams=trigrams, number_of_trigrams=number_of_trigrams, verbose=verbose, shorten_numbers=True)

# for compatibility
check_the_neo_layout = compare_a_layout

def check_a_layout_from_shell(layout, quiet, verbose, data=None):
    """Check a layout we get passed as shell argument."""
    print_layout_with_statistics(layout, print_layout=not quiet, verbose=verbose, data=data, shorten_numbers=True)
    

def check_a_layout_string_from_shell(layout_string, quiet, verbose, base_layout=NEO_LAYOUT, data=None):
    """Check a string passed via shell and formatted as

    öckäy zhmlß,´
    atieo dsnru.
    xpfüq bgvwj

    or

    qwert zuiopü+
    asdfg hjklöä
    <yxcvb nm,.-
    """
    layout = string_to_layout(layout_string, base_layout)
    print_layout_with_statistics(layout, print_layout=not quiet, verbose=verbose, data=data, shorten_numbers=True)

### Self-Test 

if __name__ == "__main__": 
    from sys import argv

    if "--test" in argv:
        from doctest import testmod
        testmod()
        exit()

    from optparse import OptionParser

    parser = OptionParser(description="Check and evolve keyboard layouts")
    # actions
    parser.add_option("--evolve", dest="evolve", type="int", default=0,
                      help="do the given number of random mutation steps", metavar="number")
    parser.add_option("--best-random-layout", dest="best_random_layout", type="int", default=0,
                      help="create the given number of random layouts and show the best one", metavar="number")
    parser.add_option("--challenge", dest="challenge_rounds", type="int", default=0,
                      help="do an evolution challenge for the given number of rounds", metavar="rounds")
    parser.add_option("--check", dest="check", 
                      help="check a layout from shell", metavar="layout")
    parser.add_option("--check-string", dest="check_string", 
                      help="check a layout_string from shell", metavar="layout_string")
    
    # options
    parser.add_option("-f", "--file", dest="file",
                      help="get the ngram data from the given textfile", metavar="textfile")
    parser.add_option("--prerandomize", dest="prerandomize", type="int", default=1000000,
                      help="do the given number of randomization steps", metavar="number")
    parser.add_option("--challengers", dest="challengers", type="int", default=10,
                      help="the number of challengers for an evolution challenge", metavar="number")
    parser.add_option("--base", dest="base", default=None, 
                      help="take the given layout as base", metavar="layout")
    parser.add_option("--base-string", dest="base_string", default=None, 
                      help="take the given layout as base for layer 1. Compatible with --base and --base-name", metavar="layout")
    parser.add_option("--base-name", dest="base_name", default=None, 
                      help="take the named layout as base. I.e.: NEO_LAYOUT or QWERTZ_LAYOUT", metavar="layout_name")

    # arguments
    parser.add_option("-q", "--quiet",
                      action="store_true", dest="quiet", default=False,
                      help="don’t print progress messages to stdout")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose", default=False,
                      help="print more detailed layout statistics")
    parser.add_option("--controlled-tail",
                      action="store_true", dest="controlled_tail", default=False,
                      help="do a controlled evolution after the random evolution steps")
    parser.add_option("--controlled",
                      action="store_true", dest="controlled_evolution", default=False,
                      help="check all possible mutations at each step and only take the best")

    (options, args) = parser.parse_args()

    # post process options
    if options.base: 
        options.base = eval(options.base)
    elif options.base_name:
        options.base = eval(options.base_name)
    if not options.base:
        options.base = NEO_LAYOUT
    if options.base_string:
        # base + base-string: base for the surroundings,
        # base-string for the base layer.
        options.base = string_to_layout(options.base_string, NEO_LAYOUT)

    if options.file: 
        options.data = read_file(options.file)
    else:
        options.data = None
    if options.check: 
        options.check = eval(options.check)

    # act
    
    if options.check:
        check_a_layout_from_shell(options.check, quiet=options.quiet, verbose=options.verbose, data=options.data)

    elif options.check_string:
        check_a_layout_string_from_shell(options.check_string, quiet=options.quiet, verbose=options.verbose, data=options.data)
            
    elif options.evolve:
        evolve_a_layout(steps=options.evolve, prerandomize=options.prerandomize, quiet=options.quiet, controlled=options.controlled_evolution, verbose=options.verbose, controlled_tail=options.controlled_tail, data=options.data, layout=options.base)
        
    elif options.best_random_layout:
        best_random_layout(number=options.best_random_layout, prerandomize=options.prerandomize, quiet=options.quiet, data=options.data, layout=options.base)

    elif options.challenge_rounds:
            evolution_challenge(rounds=options.challenge_rounds, challengers=options.challengers, data=options.data, layout=options.base)

    else:
        check_the_neo_layout(quiet=options.quiet, verbose=options.verbose, data=options.data, layout=options.base)
        
