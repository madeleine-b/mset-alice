import string
from fuzzingbook import fuzzingbook_utils
from fuzzingbook.Grammars import simple_grammar_fuzzer
import random
import glob
import os
import itertools

random.seed(None)

def add_valid_files_to_grammar(grammar):
	path_of_cwd = os.path.abspath(os.getcwd())
	files = glob.glob(path_of_cwd + '/**/*', recursive=True)
	# Remove leading slash and absolute path
	relative_files = [f.replace(path_of_cwd, '')[1:] for f in files]
	grammar["<file>"] += files + relative_files

def documentation_to_commands(doc_str):
	lines = doc_str.split("\n")
	commands = []
	for line in lines:
		commands_from_this_line = ['']
		i = 0
		while i < len(line):
			temp = ''
			while i < len(line) and line[i] != "[" and line[i] != "(":
				temp += line[i]
				i += 1
			commands_from_this_line = [c + " " + temp.strip() for c in commands_from_this_line]
			if i == len(line):
				break
			if line[i] == "[":
				# we choose one among mutually exclusive options so as not to explode command list
				start_brace_index = None
				try:
					start_brace_index = line[i+1:].index("[")
				except:
					pass
				if start_brace_index is not None:
					# ignore nested options bc that's hard
					end_brace_index = line[i+1:].index("]")
					num_nested_start_braces = line.count("[", i + 1, i + 1 + end_brace_index)
					for j in range(num_nested_start_braces):
						start_brace_index = line[i+1:].index("[")
						line = line[0 : 1+ i + start_brace_index] + \
							   line[i + start_brace_index + 2: i + 1 + end_brace_index] + \
							   line[end_brace_index + i + 2:]
						end_brace_index = line[i+1:].index("]")
				this_option = line[i+1:].split("]")[0]
				this_option = random.choice(this_option.split("|")).strip()
				commands_from_this_line = list(itertools.chain(*zip(commands_from_this_line,
																	[c + " " + this_option for c in commands_from_this_line])))
				i += line[i+1:].index("]") + 2
			elif line[i] == "(":
				# we choose one among mutually exclusive options so as not to explode command list
				this_option = line[i:].split(")")[0]
				this_option = random.choice(this_option.split("|")).strip()
				commands_from_this_line = [c + " " + this_option for c in commands_from_this_line]
				i += line[i+1:].index(")") + 2
		commands += commands_from_this_line
	return commands


# should more formally go from documentation --> grammar automatically?
GIT_GRAMMAR = {
	"<start>": ["<program>"],
	"<program>": ["<command-meta>", "<command-meta>; <program>"],
	"<command-meta>": ["<no-arg>", "<one-arg>", "<two-arg>", "<command>"],
	"<command>": [],
	"<no-arg>": ["git status", "git init", "git pull", "git log", "git branch"],
	"<one-arg>": ["git add <file>", "git commit -m <name>", "git rm <file>", "git cat-file <file>",
				  "git reset <commit>", "git checkout -b <name>", "git checkout <name>"],
	"<two-arg>": ["git diff <name> <name>", "git reset <commit> <name>"],
	"<name>": ["<letter>", "<letter><name>"],
	"<file>": ["<name>"],  # include random stuff too in case bugs cause issues
	"<letter>": [c for c in string.ascii_letters + string.digits + string.punctuation if c not in ["'", '"']],
	"<commit>": ["HEAD", "<digit><digit><digit><digit><digit><digit><digit>", "HEAD^<09number>", "HEAD~<09number>"],
	"<09number>": [str(i) for i in range(10)],
	"<number>": ["<digit>", "<digit><number>"],
	"<digit>": string.hexdigits,
	"<format>": ["sha1", "sha256"]
}

init_str = ("git init [-q | --quiet] [--bare] "
			"[--separate-git-dir name] [--object-format=<format>] "
	  		"[-b <name> | --initial-branch=<name>] "
		  	"[--shared[=<permissions>]] [directory]")

permissions_str = "[false|true|umask|group|all|world|everybody]"

reset_str = ("git reset [-q] [<commit>] [--] <name>\n"
			 "git reset [-q] [--pathspec-from-file=<name> [--pathspec-file-nul]] [<commit>]\n"
			 "git reset (--patch | -p) [<name>] [--] [<name>]\n"
			 "git reset [--soft | --mixed [-N] | --hard | --merge | --keep] [-q] [<commit>]\n")


GIT_GRAMMAR["<command>"] += documentation_to_commands(reset_str)
GIT_GRAMMAR["<permissions>"] = documentation_to_commands(permissions_str)
GIT_GRAMMAR["<command>"] += documentation_to_commands(init_str)

add_valid_files_to_grammar(GIT_GRAMMAR)

print(simple_grammar_fuzzer(grammar=GIT_GRAMMAR, max_nonterminals=50, log=False))
