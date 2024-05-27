from stack import MyStack


class RPNStack:

    def __init__(self, equation):
        self.equation = equation
        self.number = ""
        self.operators = [["+", "-"], ["*", "/"], ["^", "s"]]
        self.equation_stack = MyStack(len(self.equation) * 2)
        self.operators_stack = MyStack(len(self.equation))
        self.brackets_stack = MyStack(len(self.equation))

    def add_number(self):
        if self.number != "":
            self.equation_stack.my_push(self.number)
            self.number = ""

    def check_if_in_operators(self, char):
        for i in range(len(self.operators)):
            if char in self.operators[i]:
                return i + 1
        return False

    def add_rest_of_operators(self):
        while not self.operators_stack.is_empty():
            self.equation_stack.my_push(self.operators_stack.my_pop())

    def add_operators_from_bracket(self):
        operators_in_bracket = self.operators_stack.len() - int(self.brackets_stack.top())
        self.add_number()
        for i in range(operators_in_bracket):
            self.equation_stack.my_push(self.operators_stack.my_pop())

    def add_operators_according_to_order(self, char):
        if (self.check_if_in_operators(char) <= self.check_if_in_operators(self.operators_stack.top()) and
                not self.operators_stack.is_empty()):
            while (self.check_if_in_operators(char) <= self.check_if_in_operators(self.operators_stack.top()) and
                    not self.operators_stack.is_empty()):
                if self.brackets_stack.is_empty():
                    self.equation_stack.my_push(self.operators_stack.my_pop())
                else:
                    if self.operators_stack.len() - int(self.brackets_stack.top()) == 0:
                        return
                    self.equation_stack.my_push(self.operators_stack.my_pop())

    def create_stack(self):
        number_appeared = 0
        for i in self.equation:
            if self.check_if_in_operators(i):
                if number_appeared:
                    self.add_number()
                    self.add_operators_according_to_order(i)
                    self.operators_stack.my_push(i)
                elif not number_appeared and i == "-":
                    self.equation_stack.my_push("-1")
                    self.operators_stack.my_push("*")
            elif i == "(":
                number_appeared = 0
                self.brackets_stack.my_push(self.operators_stack.len())
            elif i == ")":
                self.add_operators_from_bracket()
                self.brackets_stack.my_pop()
            elif "0" <= i <= "9" or i == ".":
                number_appeared = 1
                self.number += i
        self.add_number()
        self.add_rest_of_operators()


class EquationToCalculate:

    def __init__(self, equation):
        self.rnp_stack = RPNStack(equation)
        self.rnp_stack.create_stack()
        self.reversed_stack = MyStack(self.rnp_stack.equation_stack.len())
        self.result_stack = MyStack(self.rnp_stack.equation_stack.len())
        self.operators = ["+", "-", "/", "*", "^", "s"]

    def reverse_stack(self):
        while not self.rnp_stack.equation_stack.is_empty():
            self.reversed_stack.my_push(self.rnp_stack.equation_stack.my_pop())

    def choose_operation(self, last_digit, second_last_digit):
        if self.reversed_stack.top() == "+":
            return second_last_digit + last_digit
        elif self.reversed_stack.top() == "-":
            return second_last_digit - last_digit
        elif self.reversed_stack.top() == "*":
            return second_last_digit * last_digit
        elif self.reversed_stack.top() == "/":
            return second_last_digit / last_digit
        elif self.reversed_stack.top() == "^":
            return second_last_digit ** last_digit
        elif self.reversed_stack.top() == "s":
            return last_digit ** (1/second_last_digit)

    def calculate(self):
        self.reverse_stack()
        while not self.reversed_stack.is_empty():
            if self.reversed_stack.top() not in self.operators:
                self.result_stack.my_push(self.reversed_stack.my_pop())
            else:
                last_digit = float(self.result_stack.my_pop())
                second_last_digit = float(self.result_stack.my_pop())
                self.result_stack.my_push(self.choose_operation(last_digit, second_last_digit))
                self.reversed_stack.my_pop()
        return self.result_stack.top()


if __name__ == "__main__":
    Equation = input("Enter equation to calculate\n"
                     "Giving negative numbers always put them in brackets like that (-1)\n")
    result = EquationToCalculate(Equation)
    try:
        print(f"{Equation} is equal to {result.calculate()}")
    except TypeError:
        print("error in equation")

# (3*6+2)+(14/3+4) 17*(2+3)+4+(8*5) (-2)*4+6/7.5-2.5 2*2+2-2+(2*2+2-2*2)*2-2+2
