from linked_list import LinkedList
from stack import MyStack


class PalindromeCheck:

    def __init__(self, word):
        self.word = word
        self.first_half = MyStack(len(self.word) // 2)
        self.reversed_second_half = MyStack(len(self.word) // 2)
        self.my_list = LinkedList()

    def create_linked_list(self):
        for letter in self.word:
            self.my_list.insert_at_end(letter)

    def create_normal_and_reversed_stack(self):
        self.create_linked_list()
        for i in range(self.my_list.size_of_ll()//2):
            current_node = self.my_list.head
            for _ in range(self.my_list.size_of_ll() - i - 1):
                current_node = current_node.next
            self.reversed_second_half.my_push(current_node.data)
        current_node = self.my_list.head
        for _ in range(self.my_list.size_of_ll()//2):
            self.first_half.my_push(current_node.data)
            current_node = current_node.next

    def check_if_palindrome(self):
        self.create_normal_and_reversed_stack()
        if self.first_half.len() != self.reversed_second_half.len():
            return False
        for _ in range(self.my_list.size_of_ll()//2):
            if self.first_half.my_pop() != self.reversed_second_half.my_pop():
                return False
        return True

    def print_result(self):
        if self.check_if_palindrome():
            print(f"{self.word} is a palindrome")
        else:
            print(f"{self.word} is not a palindrome")


if __name__ == "__main__":
    Word = input("enter word for palindrome check\n")
    result = PalindromeCheck(Word)
    result.print_result()

# racecar
