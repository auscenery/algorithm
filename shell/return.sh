#! /usr/bin/env bash

function f {
    echo "lcj"
    echo "hello world"
}

results=$(f)
echo ${results}
echo $?