class Calculator(object):

    operators = "+-*/"
    paranthesis = "()"
    valid_chars = "1234567890"

    def read(self) :
        '''read input from stdin'''
        return input('> ')
    

    def eval(self, string) :
        '''evaluates an infix arithmetic expression '''
        #TODO implement me
        string = self.removeAllWhitespace(string)
        string = self.checkValidity(string)
        result = self.calculateExpression(string)
        print(result)
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
        # operators = "*/-+"
        paranthesis_stack = []
        prev_char = ''
        index = 0
        addedCharacters = 0
        newStr = string
        for char in string:
            if char == '(':
                paranthesis_stack.append(char)
                if (prev_char == ")" or prev_char in self.valid_chars) and index != 0:
                    newStr = newStr[:index + addedCharacters] + '*' + newStr[index + addedCharacters:] 
                    addedCharacters += 1

                try:
                    if string[index + 1] in self.operators:
                        raise CalculatorException("Invalid operator position in parahtesis")
                except IndexError:
                    raise CalculatorException("Invalid parathesis")
            elif char == ')':
                if len(paranthesis_stack) == 0:
                    raise CalculatorException("Invalid parathesis")
                elif prev_char == '(':
                    raise CalculatorException("Empty Parthesis")
                elif prev_char in self.operators:
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
        # valid_characters_list = "0123456789"
        # valid_parathesis_list = "()"
        # valid_operators = "*/+-"
        index = 0
        for char in string:
            if char in self.valid_chars or char in self.operators or char in self.paranthesis:
                if ((index == 0 or index == len(string) - 1) and char in self.operators):
                    raise CalculatorException("Expression cannot begin or end with an operator")
            else: 
                raise CalculatorException("Expression contains characters which are not accepted")

            index += 1
        pass


    def calculateExpression(self, string: str):
        #TODO Calculate expression - find parathesis and order of op
        nr_parathesis = self.findNumParathesis(string)

        work_string = string
        # for operator in 
        if nr_parathesis != 0:
            last_open_parath_index = work_string.rfind('(')
            first_closed_paranth_index = work_string.find(')')

            parath_expression = work_string[last_open_parath_index+1: first_closed_paranth_index]
            print(parath_expression)
            work_string = work_string[:last_open_parath_index+1] + str(self.calculateParathExpression(parath_expression)) + work_string[first_closed_paranth_index:] 
        else: 
            work_string = str(self.calculateParathExpression(work_string))

        return work_string


    def findNumParathesis(self, string):
        """
        returns the number of parathesis pairs.
        """
        num_parathesis = 0
        for char in string:
            if char == "(":
                num_parathesis += 1
        
        return num_parathesis


    def calculateParathExpression(self, string: str):
        work_string = string

        while "*" in work_string or "/" in work_string:
            is_first_num = True
            first_num = ""
            second_num = ""
            curr_operator = ""
            op_start_index = 0
            op_end_index = 0
            index = 0

            for char in work_string:
                if char in "*/":
                    if not is_first_num:
                        op_end_index = index
                        work_string = work_string[:op_start_index] + self.calculateSingleOperation(first_num, second_num, curr_operator) + work_string[op_end_index:]
                        op_start_index = op_end_index + 1
                        print("paranth")
                        print(work_string)
                        break

                    is_first_num = False
                    curr_operator = char
                elif is_first_num:
                    first_num += char
                    if char in "+-":
                        first_num = ""
                        op_start_index = index + 1
                else:
                    if char in "+-":
                        op_end_index = index
                        work_string = work_string[:op_start_index] + self.calculateSingleOperation(first_num, second_num, curr_operator) + work_string[op_end_index:]
                        break
                    else:
                        second_num += char
                index += 1

                if index == len(work_string):
                    op_end_index = index
                    if "*" in work_string or "/" in work_string:
                        work_string = work_string[:op_start_index] + self.calculateSingleOperation(first_num, second_num, curr_operator) + work_string[op_end_index:]
                    
        work_string = self.calculateAdditionOrSubtraction(work_string)
        
        return work_string

    def calculateAdditionOrSubtraction(self, string: str):
        work_string = string
        is_result_negative = False
        while "+" in work_string or "-" in work_string:
            is_first_num = True
            first_num = ""
            second_num = ""
            curr_operator = ""
            index = 0
             
            if is_result_negative: break

            for char in work_string:
                if is_first_num:
                    if char in "-+":
                        is_first_num = False
                        curr_operator = char
                    else:
                        first_num += char
                else:
                    if char in "-+":
                        work_string = self.calculateSingleOperation(first_num, second_num, curr_operator) + work_string[index:]
                        break
                    if index == len(work_string) - 1:
                        second_num += char
                        work_string = self.calculateSingleOperation(first_num, second_num, curr_operator)
                        first_char = work_string[0]
                        if first_char == "-":
                            is_result_negative = True
                        break

                    second_num += char
                index += 1

        return work_string



    def calculateSingleOperation(self, first_num, second_num, operator):
        first_num = float(first_num)
        second_num = float(second_num)
        result = 0
        print(operator)

        if operator == '*':
            result = first_num * second_num
            print(f"{first_num} * {second_num} = {result}")
        elif operator == '/':
            result = first_num / second_num
            print(f"{first_num} / {second_num} = {result}")
        elif operator == '+':
            result = first_num + second_num
            print(f"{first_num} + {second_num} = {result}")
        elif operator == '-':
            result = first_num - second_num
            print(f"{first_num} - {second_num} = {result}")
        
        return str(result)



class CalculatorException(Exception):
    default_message = 'The passed string could not be evaluated'

    def __init__(self, message):
        super().__init__(self.default_message + ": " + message)



if __name__ == '__main__':
    calc = Calculator()
    calc.loop()