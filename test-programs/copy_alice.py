import os
import sys
import shutil
import subprocess

start_str = "Creating file "
end_str = " of"

workload_dir = "copy_workload_dir"
traces_dir = "copy_traces_dir"

out = open(sys.argv[1]).read()
file_paths = []
start = 0

while True:
    pos = out.find(start_str, start)
    if pos == -1:
        break
    end = out.find(end_str, start)
    file_paths.append(out[pos + len(start_str):end])
    start = end + len(end_str)

try:
    os.mkdir("copy_vulns")
except:
    pass

counter = 0
for file_path in file_paths:
    try:
        shutil.rmtree(traces_dir)
    except:
        pass
    os.mkdir(traces_dir)

    try:
        shutil.rmtree(workload_dir)
    except: 
        pass 
    os.mkdir(workload_dir)
    
    os.system("chmod +rw " + file_path)
    shutil.copy(file_path, './copy_workload_dir/A')
    
    os.system("chmod +rw ./copy_workload_dir/A")
    
    subprocess.check_output("""
              alice-record --workload_dir ./copy_workload_dir \
              --traces_dir ./copy_traces_dir \
              ./bin/copy ./copy_workload_dir/A ./copy_workload_dir/out
              """, shell=True)
    
    alice_output = subprocess.check_output("alice-check --traces_dir=./copy_traces_dir --checker=./copy_checker.py", shell=True)
    
    vulns = open('copy_vulns/run_' + str(counter), "w")
    counter += 1
    vulns.write(alice_output)
    vulns.close()
