#!/bin/bash
crashed_state_directory="$1"

cd $crashed_state_directory

# Use older git
export PATH=/home/ubuntu/git-1.9.2-llvm:$PATH

# If a crash happens in the middle of a Git command, a '.lock' file might be
# left in the repository. In this case, Git displays a message similar to "Make
# sure no other git process is running and remove the file manually to
# continue".  We follow Git's instructions, and remove the file if it exists.
rm -f .git/index.lock


errors=$(script -q -c 'git fsck --full' | grep 'unreachable\|missing\|dangling\|hash mismatch')
if [ ${#errors} -ge 2 ]; then 
  exit 1
fi

# The following "set" command tells bash to exit with a non-zero status, if any
# of the future commands exits with a non-zero status
set -e

# Doing a few operations on the directory (i.e., git repository) supplied by
# ALICE
git status
echo hello > x
git add x
git commit -m "tmp"
