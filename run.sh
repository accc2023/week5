#!/bin/bash

for assignment_file in *-assignment.dfy; do
    if [ -e "$assignment_file" ]; then
        submission_file="${assignment_file%-assignment.dfy}-submission.dfy"
        python check_submission.py "$assignment_file" "$submission_file"
    fi
done
