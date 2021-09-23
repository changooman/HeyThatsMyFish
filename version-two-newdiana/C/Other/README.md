# xjson
A shell-executable command-line program that consumes a sequence of well-formed JSON values from STDIN and delivers JSON to STDOUT.

## Requirements
* python 3.6.8

## Structure
```
.
├── Other           # all auxiliary files
│   ├── README.md   # this README
│   └── tests       # executable unit tests
├── Test
│   ├── 1-in.json   # the test input file
│   └── 1-out.json  # the 1-in.json expected output file
└── xjson           # the xjson executable
```

## Running

* Run the program with `./xjson`
* Provide well-formed JSON values to STDIN

Run the unit tests in the Other directory with `./tests`