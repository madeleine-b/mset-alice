#!/usr/bin/env python

import os
import sys

crashed_state_directory = sys.argv[1]
stdout_file = sys.argv[2]

os.chdir(crashed_state_directory)
stdout = open(stdout_file).read()

try:
    last_pos = int(stdout.split('\n')[-2])
except:
    exit(0)

assert open('out').read()[:last_pos] == open('A').read()[:last_pos]