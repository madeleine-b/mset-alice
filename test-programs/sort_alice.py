import os
import sys
import shutil
import subprocess

start_str = "Creating file "
end_str = " of"

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
    shutil.rmtree("sort_vulns")
except:
    pass
os.mkdir("sort_vulns")

counter = 0
for file_path in file_paths:
    try:
        shutil.rmtree("sort_traces_dir")
    except:
        pass
    os.mkdir("sort_traces_dir")

    try:
        shutil.rmtree("sort_workload_dir")
    except: 
        pass 
    os.mkdir("sort_workload_dir")
    
    shutil.copy(file_path, './sort_workload_dir/A')
    
    os.system("chmod +rw ./sort_workload_dir/A")
    
    subprocess.check_output("""
              alice-record --workload_dir ./sort_workload_dir \
              --traces_dir ./sort_traces_dir \
              ./twosort.sh
              """, shell=True)
    
    alice_output = subprocess.check_output("alice-check --traces_dir=./sort_traces_dir --checker=./sort_checker.py", shell=True)
    
    vulns = open('sort_vulns/run_' + str(counter), "w")
    counter += 1
    vulns.write(alice_output)
    vulns.close()
