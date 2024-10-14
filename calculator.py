class Calculator(object):
    def read(self) :
        '''read input from stdin'''
        return input('> ')
    

    def eval(self, string) :
        '''evaluates an infix arithmetic expression '''
        #TODO implement me
        string = self.removeAllWhitespace(string)
        string = self.checkValidity(string)
        self.calculateExpression(string)
        pass


    def loop(self) :
        """read a line of input, evaluate and print it
        repeat the above until the user types 'quit'. """
        line = self.read()
        #TODO implement me
        isProgramRunning = True
        while isProgramRunning:
            if line.strip().lower() == 'quit':
                isProgramRunning = False
            else:
                self.eval(line)
                line = self.read()
            pass


    def removeAllWhitespace(self, string):
        return string.translate(str.maketrans('', '', ' \n\t\r'))


    def checkValidity(self, string):
        """
        checks the content of the string. If valid, returns a string ready to be evaluated for calculation
        """
        self.checkCharacterContentValidity(string)
        return self.checkParathesisValidity(string)


    def checkParathesisValidity(self, string):
        """
        Checks if the parathesis are placed correctly and if the contents can form operations
        returns a new string with added multiplication operator for cases
                                    (a*b)(a*b) -> (a*b)*(a*b) 
                                    someInt(a*b) -> someInt*(a*b) 
        """
        operators = "*/-+"
        paranthesis_stack = []
        prev_char = ''
        index = 0
        addedCharacters = 0
        newStr = string
        for char in string:
            if char == '(':
                paranthesis_stack.append(char)
                if prev_char == ")" or prev_char in '1234567890':
                    newStr = newStr[:index + addedCharacters] + '*' + newStr[index + addedCharacters:] 
                    addedCharacters += 1

                try:
                    if string[index + 1] in operators:
                        raise CalculatorException("Invalid operator position in parahtesis")
                except IndexError:
                    raise CalculatorException("Invalid parathesis")
            elif char == ')':
                if len(paranthesis_stack) == 0:
                    raise CalculatorException("Invalid parathesis")
                elif prev_char == '(':
                    raise CalculatorException("Empty Parthesis")
                elif prev_char in operators:
                    raise CalculatorException("Invalid operator position in parahtesis")

                paranthesis_stack.pop()

            prev_char = char
            index += 1

            

        if len(paranthesis_stack) == 0: 

            print('valid paranthesis')
        else:
            raise CalculatorException("Invalid parathesis")

        print(newStr)
        return newStr


    def checkCharacterContentValidity(self, string):
        valid_characters_list = "0123456789"
        valid_parathesis_list = "()"
        valid_operators = "*/+-"
        index = 0
        for char in string:
            if char in valid_characters_list or char in valid_operators or char in valid_parathesis_list:
                if ((index == 0 or index == len(string) - 1) and char in valid_operators):
                    raise CalculatorException("Expression cannot begin or end with an operator")
            else: 
                raise CalculatorException("Expression contains characters which are not accepted")

            index += 1
        pass


    def calculateExpression(self, string):

        pass


    def calculateSingleOperation(self, first_num, second_num, operator):
        if operator == '*':
            return first_num * second_num
        elif operator == '/':
            return first_num / second_num
        elif operator == '+':
            return first_num + second_num
        elif operator == '-':
            return first_num - second_num
        pass



class CalculatorException(Exception):
    default_message = 'The passed string could not be evaluated'

    def __init__(self, message):
        super().__init__(self.default_message + ": " + message)



if __name__ == '__main__':
    calc = Calculator()
    calc.loop()