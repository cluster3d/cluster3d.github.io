#!/bin/bash
for i in {20..199}
do
	sbatch ../job_request/job$i.sh
done
