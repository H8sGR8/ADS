class Node:
	def __init__(self, data):
		self.data = data
		self.next = None


class LinkedList:
	def __init__(self):
		self.head = None

	def insert_at_begin(self, data):
		new_node = Node(data)
		if self.head is None:
			self.head = new_node
			return
		else:
			new_node.next = self.head
			self.head = new_node

	def insert_at_index(self, data, index):
		new_node = Node(data)
		current_node = self.head
		position = 0
		if position == index:
			self.insert_at_begin(data)
		else:
			while current_node is not None and position + 1 != index:
				position = position+1
				current_node = current_node.next
			if current_node is not None:
				new_node.next = current_node.next
				current_node.next = new_node
			else:
				print("Index not present")

	def insert_at_end(self, data):
		new_node = Node(data)
		if self.head is None:
			self.head = new_node
			return
		current_node = self.head
		while current_node.next:
			current_node = current_node.next
		current_node.next = new_node

	def update_node(self, val, index):
		current_node = self.head
		position = 0
		if position == index:
			current_node.data = val
		else:
			while current_node is not None and position != index:
				position = position + 1
				current_node = current_node.next
			if current_node is not None:
				current_node.data = val
			else:
				print("Index not present")

	def remove_first_node(self):
		if self.head is None:
			return
		self.head = self.head.next

	def remove_last_node(self):
		if self.head is None:
			return
		current_node = self.head
		while current_node.next.next:
			current_node = current_node.next
		current_node.next = None

	def remove_at_index(self, index):
		if self.head is None:
			return
		current_node = self.head
		position = 0
		if position == index:
			self.remove_first_node()
		else:
			while current_node is not None and position + 1 != index:
				position = position + 1
				current_node = current_node.next
			if current_node is not None:
				current_node.next = current_node.next.next
			else:
				print("Index not present")

	def remove_node(self, data):
		current_node = self.head
		if current_node.data == data:
			self.remove_first_node()
			return
		while current_node is not None and current_node.next.data != data:
			current_node = current_node.next
		if current_node is None:
			return
		else:
			current_node.next = current_node.next.next

	def size_of_ll(self):
		size = 0
		if self.head:
			current_node = self.head
			while current_node:
				size = size + 1
				current_node = current_node.next
			return size
		else:
			return 0

	def print_ll(self):
		current_node = self.head
		while current_node:
			print(current_node.data, end="\t")
			current_node = current_node.next
