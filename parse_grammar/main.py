from parsimonious.grammar import Grammar

grammar = Grammar(
"""
expression = number operation expression / number
operation = "+" / "-"
number = ~"[0-9]+"
""")
