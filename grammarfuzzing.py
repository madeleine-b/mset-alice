import string
from fuzzingbook import fuzzingbook_utils
from fuzzingbook.Grammars import simple_grammar_fuzzer
import random

random.seed(None)

# should more formally go from documentation --> grammar automatically?
GIT_GRAMMAR = {
	"<start>": ["<program>"],
	"<program>": ["<command>", "<command>; <program>"],
	"<command>": ["<no-arg>", "<one-arg>", "<two-arg>"],
	"<no-arg>": ["git status", "git init", "git pull", "git log", "git branch"],
	"<one-arg>": ["git add <name>", "git commit -m <name>", "git rm <name>", "git cat-file <name>",
				  "git reset <commit>", "git checkout -b <name>", "git checkout <name>"],
	"<two-arg>": ["git diff <name> <name>", "git reset <commit> <name>"],
	"<name>": ["<letter>", "<letter><name>"],
	"<letter>": [c for c in string.printable],
	"<commit>": ["HEAD", "<number><number><number><number><number><number><number>"],
	"<number>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
}

print(simple_grammar_fuzzer(grammar=GIT_GRAMMAR, max_nonterminals=50, log=False))
