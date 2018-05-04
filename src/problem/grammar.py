#! /usr/bin/env python

# Taken from PonyGE
# Copyright (c) 2009-2012 Erik Hemberg and James McDermott
# Hereby licensed under the GNU GPL v3.
# http://ponyge.googlecode.com

import sys, copy, re, random, math, operator, pprint, functools

class Grammar(object):
    """Context Free Grammar"""
    NT = "NT" # Non Terminal
    T = "T" # Terminal

    def __init__(self, file_name=None, input_s=None, **kwargs):
        """Pass either a filename or an input string"""
        self.rules = {}
        self.non_terminals, self.terminals = set(), set()
        self.start_rule = None
        if input_s is None and file_name is not None:
            input_s = open(file_name, 'r').read()
        self.parse_bnf(input_s, **kwargs)
        self.production_lcm = lcm(len(self.rules[k]) for k in self.non_terminals)

    def parse_bnf(self, input_s, **kwargs):
        """Parse a grammar in BNF format, passed in as a string."""
        rule_separator = "::="
        # Don't allow space in NTs, and use lookbehind to match "<"
        # and ">" only if not preceded by backslash. Group the whole
        # thing with capturing parentheses so that split() will return
        # all NTs and Ts. TODO does this handle quoted NT symbols?
        non_terminal_pattern = r"((?<!\\)<\S+?(?<!\\)>)"
        # Use lookbehind again to match "|" only if not preceded by
        # backslash. Don't group, so split() will return only the
        # productions, not the separators.
        production_separator = r"(?<!\\)\|"

        # Parse the grammar
        for line in input_s.split("\n"):
            if not line.startswith("#") and line.strip() != "":
                # Split rules. Everything must be on one line
                if line.find(rule_separator):
                    lhs, productions = line.split(rule_separator, 1) # 1 split
                    lhs = lhs.strip()
                    if not re.search(non_terminal_pattern, lhs):
                        raise ValueError("lhs is not a NT:", lhs)
                    self.non_terminals.add(lhs)
                    if self.start_rule == None:
                        self.start_rule = (lhs, self.NT)
                    # Find terminals and non-terminals
                    tmp_productions = []

                    if productions.strip().startswith("GE_RANGE:"):
                        # Special case: for GE_RANGE:nvars, substitute
                        # 0 | 1 | ... | 9 (assuming nvars=10)
                        varname = productions.strip().split(":")[1]
                        assert varname in kwargs
                        n = kwargs[varname]
                        tmp_productions = []
                        for i in range(n):
                            tmp_production = []
                            symbol = str(i)
                            tmp_production.append((symbol, self.T))
                            tmp_productions.append(tmp_production)
                            self.terminals.add(symbol)
                    else:
                        # Usual case: iterate through productions on RHS
                        for production in re.split(production_separator, productions):
                            production = production.strip().replace(r"\|", "|")
                            tmp_production = []
                            for symbol in re.split(non_terminal_pattern, production):
                                symbol = symbol.replace(r"\<", "<").replace(r"\>", ">")
                                if len(symbol) == 0:
                                    continue
                                elif re.match(non_terminal_pattern, symbol):
                                    tmp_production.append((symbol, self.NT))
                                else:
                                    self.terminals.add(symbol)
                                    tmp_production.append((symbol, self.T))

                            tmp_productions.append(tmp_production)
                    # Create a rule
                    if not lhs in self.rules:
                        self.rules[lhs] = tmp_productions
                    else:
                        raise ValueError("lhs should be unique", lhs)
                else:
                    raise ValueError("Each rule must be on one line")

    def __str__(self):
        return "%s %s %s %s" % (self.terminals, self.non_terminals,
                                self.rules, self.start_rule)
    
def derive_string(grammar, genome, s=None):
    """Recursively derive a string given a grammar, genome, and start
    symbol. Don't create the derivation tree."""
    if s is None:
        s = grammar.start_rule[0]
    elif s in grammar.terminals:
        return s
    rule = grammar.rules[s]
    if len(rule) > 1:
        codon = genome.next()
        idx = codon % len(rule)
        prod = rule[idx]
        # print "rule", rule, "codon", codon, "prod", prod
    else:
        prod = rule[0]
        # print "rule", rule, "no codon", "prod", prod
    return "".join([derive_string(grammar, genome, s[0]) for s in prod])


# -----

# GCD and LCM from https://gist.github.com/endolith/114336

# Greatest common divisor of more than 2 numbers. Am I terrible for
# doing it this way?
 
def gcd(numbers):
    """Return the greatest common divisor of the given integers"""
    from fractions import gcd
    return functools.reduce(gcd, numbers)
 
# Least common multiple is not in standard libraries? It's in gmpy,
# but this is simple enough:
 
def lcm(numbers):
    """Return lowest common multiple."""    
    def lcm_(a, b):
        return (a * b) // gcd([a, b])
    return functools.reduce(lcm_, numbers, 1)
 
# Assuming numbers are positive integers...

