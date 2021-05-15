#!/usr/bin/env python

import os
import sys

crashed_state_directory = sys.argv[1]
stdout_file = sys.argv[2]

os.chdir(crashed_state_directory)

stdout = open(stdout_file)
stdout_lines = stdout.read()
stdout.close()

stdout_lines = stdout_lines.rstrip().split('\n')

i = 0
n = len(stdout_lines)
for i in xrange(n):
    try:
        line = stdout_lines[i]
        data = line.split(',')
        
        f = open(data[1])
        out = f.read()
        f.close()
        
        lines = out.rstrip().split('\n')
        assert all(lines[i] <= lines[i + 1] for i in xrange(len(lines) - 1))
        
        if data[0] == data[1]:
            # same file for input and output, require no data loss
            assert len(out) == int(data[2])
    except:
        continue
