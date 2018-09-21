#!/usr/bin/env bash

function bla() {
    return 1
}

# 二者等价
path=$(pwd)
echo $path 

# directly output can't work
echo pwd

path1=`pwd`
echo $path1

#() runs commands in the subshell 
# (list) list is executed in a subshell environment.
bla ||  ( echo '1' ; exit 1 ;)
echo '2'

# the pipeline still exits only from the subshell. 
bla ||  echo '1' | exit 1
echo "3"

# { list; } list is simply executed in the current shell environment
bla ||  { echo '1' ; exit 1; }

echo '4'