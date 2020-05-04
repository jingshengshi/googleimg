#!/usr/bin/env bash
#robot --pythonpath . -d Reports -i DEBUG robotcase

for((i=0;i<1;i++))
do
robot --pythonpath . -d Reports robotcase 
done

#kill $Pid


