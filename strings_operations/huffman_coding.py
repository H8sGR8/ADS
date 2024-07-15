from collections import Counter


class BinaryHeap:
    def __init__(self):
        self.heap = []

    def push(self, item: tuple[int, str]) -> None:
        self.heap.append(item)
        self.heapify_up(len(self.heap) - 1)

    def pop(self) -> tuple[int, str]:
        if len(self.heap) > 1:
            self.swap(0, len(self.heap) - 1)
            item = self.heap.pop()
            self.heapify_down(0)
        elif self.heap:
            item = self.heap.pop()
        else:
            item = None
        return item

    def heapify_up(self, index: int) -> None:
        parent = (index - 1) // 2
        if parent >= 0 and self.heap[index] < self.heap[parent]:
            self.swap(index, parent)
            self.heapify_up(parent)

    def heapify_down(self, index: int) -> None:
        left = 2 * index + 1
        right = 2 * index + 2
        smallest = index
        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right
        if smallest != index:
            self.swap(index, smallest)
            self.heapify_down(smallest)

    def swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]


class HuffmanNode:
    def __init__(self, symbol=None, frequency=0):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other) -> bool:
        return self.frequency < other.frequency


class PriorityQueue:
    def __init__(self):
        self.heap = BinaryHeap()

    def enqueue(self, item: str or HuffmanNode, priority: int) -> None:
        self.heap.push((priority, item))

    def dequeue(self) -> str or HuffmanNode:
        return self.heap.pop()[1]


class HuffmanCode:

    def __init__(self, data: str):
        self.data = data
        self.huffman_codes = {}
        self.encoded_data = ''

    def generate_codes(self, node: HuffmanNode, code='') -> None:
        if node.symbol is not None:
            self.huffman_codes[node.symbol] = code
        if node.left:
            self.generate_codes(node.left, code + "0")
        if node.right:
            self.generate_codes(node.right, code + "1")

    def huffman_coding(self) -> None:
        frequency = Counter(self.data)
        pq = PriorityQueue()
        for symbol, freq in frequency.items():
            pq.enqueue(HuffmanNode(symbol, freq), freq)
        while len(pq.heap.heap) > 1:
            left = pq.dequeue()
            right = pq.dequeue()
            merged = HuffmanNode(frequency=left.frequency + right.frequency)
            merged.left = left
            merged.right = right
            pq.enqueue(merged, merged.frequency)
        root = pq.dequeue()
        self.generate_codes(root)
        self.encoded_data = ''.join(self.huffman_codes[symbol] for symbol in self.data)


if __name__ == "__main__":
    sentence = "I love data structures"
    coding = HuffmanCode(sentence)
    coding.huffman_coding()
    print(f"Huffman Codes: {coding.huffman_codes}")
    print(f"Encoded Data: {coding.encoded_data}")
    original_bits = len(sentence) * 8
    compressed_bits = len(coding.encoded_data)
    compression_ratio = original_bits / compressed_bits
    print(f"Compression Ratio: {compression_ratio}")
