#!/bin/bash

for job in ../job_request/*
do
	sbatch "$job"
done
