#!/bin/bash

wd=$(pwd)
export PATH=$wd/test-programs/bin:$PATH

rm -rf traces_dir
mkdir -p traces_dir

# If we are given a pre-existing fuzzed script, then use it and current workload_dir
# Otherwise we create new random files etc in the workload directory
if [[ $# -eq 1 ]]; then
    workload=$wd/$1
    
    # Move into the workload 
    cd workload_dir
else
    rm -rf workload_dir
    mkdir -p workload_dir

    # Move into the workload 
    cd workload_dir

    # Create some files that we will be adding to the repository during the
    # workload.
    echo -e "hello\ngoodbye\naaaa" > file1
    echo "hello2" > file2
    
    python3 ../grammarfuzzing.py sort 10000 > ../sort_fuzzed.sh
    chmod u+x ../sort_fuzzed.sh
    workload=$wd/sort_fuzzed.sh
fi

# Save the workload_dir with the randomly created fuzzed files before we
# potentially modify them
cd ..
tar -czvf workload_dir_before_workload_runs.tar.gz workload_dir
cd workload_dir

# Perform the actual workload and collect traces. The "workload_dir" argument
# to alice-record specifies the entire directory which will be re-constructed
# by alice and supplied to the checker. Alice also takes an initial snapshot of
# the workload directory before beginning the workload. The "traces_dir"
# argument specifies where all the traces recorded will be stored.
alice-record --workload_dir .  --traces_dir ../traces_dir $workload

