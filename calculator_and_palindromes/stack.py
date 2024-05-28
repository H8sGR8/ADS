class MyStack:
    def __init__(self, max_space):
        self.max_space = max_space
        self.top_index = -1
        self.stack = [""] * self.max_space

    def len(self) -> int:
        return self.top_index + 1

    def is_empty(self) -> bool:
        return self.len() == 0

    def top(self):
        if not self.is_empty():
            return self.stack[self.top_index]

    def my_push(self, element: str) -> None:
        if self.top_index != self.max_space:
            self.top_index += 1
            self.stack[self.top_index] = str(element)
        else:
            print("Stack is full")

    def my_pop(self) -> str:
        if not self.is_empty():
            popped = self.top()
            self.stack[self.top_index] = ""
            self.top_index -= 1
            return popped
        else:
            print("Stack is empty")
