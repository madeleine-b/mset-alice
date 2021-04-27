import string
from fuzzingbook import fuzzingbook_utils
from fuzzingbook.Grammars import simple_grammar_fuzzer
import random

random.seed(None)


def documentation_to_commands(doc_str):
	lines = doc_str.split("\n")
	commands = []
	for line in lines:
		commands_from_this_line = []
		options = line.split()
		for index in range(len(options)):
			o = options[index]
			o = o.strip()
			if ")" in o or "|" in o:
				continue
			if "(" in o:
				s = "" 
				i = 0
				while i < len(o):
					if o[i] != "(":
						s += o[i]
					else:
						i += 1
						while i < len(o) and o[i] != "|":
							s += o[i]
							i += 1
						while i < len(o) and o[i] != ")":
							i += 1
					i += 1
				o = s
			if len(commands_from_this_line) == 0:
				commands_from_this_line = [o]
			elif "]" not in o:
				# we're not perfect! we don't do nested options like [--a [-N]] so sue us
				commands_from_this_line = [c + " " + o.replace("[", "").replace("]", "") for c in commands_from_this_line]
			else:
				temp = commands_from_this_line.copy()
				for c in temp:
					commands_from_this_line.append(c + " " + o.replace("[", "").replace("]", ""))
		commands += commands_from_this_line
	return commands


# should more formally go from documentation --> grammar automatically?
GIT_GRAMMAR = {
	"<start>": ["<program>"],
	"<program>": ["<command-meta>", "<command-meta>; <program>"],
	"<command-meta>": ["<no-arg>", "<one-arg>", "<two-arg>", "<command>"],
	"<command>": [],
	"<no-arg>": ["git status", "git init", "git pull", "git log", "git branch"],
	"<one-arg>": ["git add <name>", "git commit -m <name>", "git rm <name>", "git cat-file <name>",
				  "git reset <commit>", "git checkout -b <name>", "git checkout <name>"],
	"<two-arg>": ["git diff <name> <name>", "git reset <commit> <name>"],
	"<name>": ["<letter>", "<letter><name>"],
	"<letter>": [c for c in string.ascii_letters + string.digits + string.punctuation if c not in ["'", '"']],
	"<commit>": ["HEAD", "<number><number><number><number><number><number><number>"],
	"<number>": string.hexdigits
}

reset_str = ("git reset [-q] [<commit>] [--] <name>\n"
			 "git reset [-q] [--pathspec-from-file=<name> [--pathspec-file-nul]] [<commit>]\n"
			 "git reset (--patch | -p) [<name>] [--] [<name>]\n"
			 "git reset [--soft | --mixed [-N] | --hard | --merge | --keep] [-q] [<commit>]\n")

GIT_GRAMMAR["<command>"] += documentation_to_commands(reset_str)

for i in range(50):
	print(simple_grammar_fuzzer(grammar=GIT_GRAMMAR, max_nonterminals=50, log=False))
