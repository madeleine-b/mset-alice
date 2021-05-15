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
        f_pos = line.find(":")
        if f_pos == -1:
            continue
        paths = line[:f_pos]
        paths = paths.split(',')
        in_path = paths[0]
        out_path = paths[1]
        line = line[f_pos + 1:]
        data = line.rstrip(',').split(',')

        f = open(in_path)
        in_str = f.read()
        f.close()
        
        f = open(out_path)
        out_str = f.read()
        f.close()

        assert in_str[:int(data[-1])] == out_str
    except AssertionError as e:
        raise e
    except:
        continue
