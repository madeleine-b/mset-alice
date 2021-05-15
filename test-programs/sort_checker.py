#!/usr/bin/env python

import os
import sys

crashed_state_directory = sys.argv[1]
stdout_file = sys.argv[2]

os.chdir(crashed_state_directory)
original_length = int(open(stdout_file).read())

out = open('A').read()

assert len(out) == original_length

lines = out.split('\n')

assert all(lines[i] <= lines[i + 1] for i in xrange(len(lines) - 1))