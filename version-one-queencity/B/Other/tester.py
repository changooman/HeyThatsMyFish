import unittest
import time

testingrn = True

'''
Spit has been defined here as well due to importing issues in Python with attempting to import a file without the
python extension
This function takes user input and will print it infinitely or at a limit of twenty depending on what the user inputs
@param userinput This is the variable that stores the user input and the function uses
'''
def spit(userinput):
    # If user put nothing as an input, print hello world
    if userinput == []:
        return 'hello world'

    # Initalizes and declares limit variable which helps determine how many times to print the userinput
    limit = False
    global count
    count = 0
    if type(userinput) is str:
        userinput = userinput.split(' ')

    # Checks and changes the limit variable to True if user wrote '-limit' as the first command line in their input
    if userinput[0] == '-limit':
        userinput.pop(0)
        limit = True

    # Initializes and declares the final string that is to be printed, concatenating them with the user input
    finalstring = ''
    for x in userinput:
        finalstring = finalstring + x + ' '

    # Print either infinitely or limited based on user command line input
    if limit == True:
        while count < 20:
            if testingrn == False:
                print(finalstring)
            count = count + 1
        return count
    else:
        while limit == False:
            if testingrn == False:
                print(finalstring)
                count = count + 1


# This class serves as the executor for the test cases below
class Testing(unittest.TestCase):
    def test_spit(self):
        self.assertEqual(spit([]), "hello world")

    def test_spit2(self):
        self.assertEqual(spit("-limit pass"), 20)

    def test_spit3(self):
        self.assertEqual(spit("-limit"), 20)

    def test_spit4(self):
        self.assertEqual(spit("-limit "), 20)

    def test_spit5(self):
        self.assertEqual(spit("-limit asda  asdad   "), 20)

    def test_spit6(self):
        self.assertEqual(spit("-limit -limit  asdad"), 20)


# This runs the test executor above
if __name__ == "__main__":
    unittest.main()
