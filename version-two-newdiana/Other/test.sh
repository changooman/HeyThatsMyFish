#!/bin/bash

for ((i = 1; i <= $(find Tests/ -name "*-in.json" | wc -l); i++)); do
    if [[ $1 == "-ow" ]]; then
        ./x* < Tests/$i-in.json > Tests/$i-out.json
        echo Output:
        cat Tests/$i-out.json
    else
        echo Output:
        ./x* < Tests/$i-in.json
        echo Expected:
        cat Tests/$i-out.json
    fi
    echo
done
