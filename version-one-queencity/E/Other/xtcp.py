import socket
import sys
import time


# Consumes a list of well-formed JSON values from STDIN and delivers JSON to STDOUT.
def jsonify(input):
    # defining variables
    global more
    first = {"count": 0, "seq": []}
    more = True
    second = []

    # Runs through a list of well formed JSON values
    # Checks if it is well formed and processes them
    for x in input:
        try:
            inp = x
            inp = eval(inp)
            first['seq'].append(inp)
            if type(inp) is not int and type(inp) is not str:
                first['count'] += len(inp)
            else:
                first['count'] += 1
        except Exception as e:
            more = False
            break

    second.append(first["count"])
    reversedlist = reversed(first["seq"])

    # adds the elements to the second counter
    for element in reversedlist:
        second.append(element)

    # outputs the counters
    print(str(first))
    print(str(second))


# This function takes an ip address, a port and connects there, listening in for
# a client which will direct an input
# It will take that input from the client and put it into jsonify
# @hostname - IP Address
# @port - Port number
def netcat(hostname, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setblocking(0)
    s.settimeout(3)
    s.bind((hostname, port))
    s.listen(1)
    conn2, addr = s.accept()
    data = conn2.recv(1024)
    data2 = data.splitlines()
    jsonify(data2)
    conn2.close()
    s.close()


# Take in a port, default to 4567 otherwise
def main():
    userinput = sys.argv
    userinput.pop(0)
    host = '127.0.0.1'
    # port = 24
    try:
        netcat(host, int(userinput[0]))
    except:
        netcat(host, int(4567))


main()

# !/usr/bin/env python
