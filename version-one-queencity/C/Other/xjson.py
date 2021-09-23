import json


# consumes a sequence of well-formed JSON values from STDIN and delivers JSON to STDOUT.
def main():
    #defining variables
    global more
    first = {"count": 0, "seq": []}
    more = True
    second = []

    #takes in the input and adds them to the counters
    while more != False:
        try:
            inp = eval(raw_input())
        except:
            more = False
            break
        first['seq'].append(inp)
        first['count'] += len(inp)
    second.append(first["count"])
    reversedlist = reversed(first["seq"])
    
    #adds the elements to the second counter
    for element in reversedlist:
        second.append(element)

    #outputs the counters
    print(str(first))
    print(str(second))


main()
