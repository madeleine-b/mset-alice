# mset-alice

## copy/sort + fuzzer
`./copy_workload.sh` will delete the contents of workload_dir and fill it with a few hardcoded files and contents as well as random files with random bytes. Then the fuzzer will create `copy_fuzzed.sh` and run the workload under the ALICE strace framework. Same for `./sort_workload.sh`

If you optionally pass an existing workload of copy/sort commands, the `{copy,sort}_workload.sh` script will take the workload_dir contents as is. **Be careful of this** and make sure you restore from a previous compressed workload_dir.

Right before `{copy,sort}_workload.sh` runs any script commands, it compresses workload_dir into a .tar.gz archive. This allows for reproducibility because the randomly created files may be changed by the actual workload commands after they're run.
