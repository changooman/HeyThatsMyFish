from json import JSONDecoder

decoder = JSONDecoder()

# consumes a sequence of well-formed JSON values from STDIN and delivers JSON to STDOUT.
def main():
    #defining variables
    global more
    first = {"count": 0, "seq": []}
    more = True
    second = []

    #takes in the input and adds them to the counters
    while more is True:
        try:
            inp = raw_input()
            inp = eval(inp)
            first['seq'].append(inp)
            if type(inp) is not int and type(inp) is not str:
                print(type(inp))
                first['count'] += len(inp)
            else:
                first['count'] += 1
        except Exception as e:
            print e
            more = False
            break
    second.append(first["count"])
    reversedlist = reversed(first["seq"])
    
    #adds the elements to the second counter
    for element in reversedlist:
        second.append(element)

    #outputs the counters
    print(str(first))
    print(str(second))


main()
