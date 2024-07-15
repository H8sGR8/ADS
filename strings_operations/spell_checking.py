import math
import time


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word: str) -> bool:
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

    def suggestions(self, prefix: str) -> list[str]:
        results = []
        node = self.root
        for char in prefix:
            if char in node.children:
                node = node.children[char]
            else:
                return results

        self.dfs(node, prefix, results)
        return results

    def dfs(self, node: TrieNode, prefix: str, results: list[str]) -> None:
        if node.is_end_of_word:
            results.append(prefix)
        for char, next_node in node.children.items():
            self.dfs(next_node, prefix + char, results)


class Autocorrection:

    def __init__(self, file_path):
        self.common_typos = {
            ('o', 'p'): 0.5, ('p', 'o'): 0.5,
            ('i', 'o'): 0.5, ('o', 'i'): 0.5,
            ('r', 'e'): 0.5, ('e', 'r'): 0.5,
            ('a', 's'): 0.5, ('s', 'a'): 0.5,
            ('d', 's'): 0.5, ('s', 'd'): 0.5,
            ('z', 'x'): 0.5, ('x', 'z'): 0.5,

        }
        with open(file_path, 'r') as file:
            self.words = set(word.strip() for word in file.readlines())
        self.trie = Trie()
        for word in self.words:
            self.trie.insert(word)

    def levenshtein_distance(self, s1: str, s2: str) -> int:
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitution_cost = self.common_typos.get((c1, c2), 1) if c1 != c2 else 0
                substitutions = previous_row[j] + substitution_cost
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row

        return previous_row[-1]

    def hamming_distance(self, s1: str, s2: str) -> int:
        if len(s1) != len(s2):
            raise ValueError("Hamming distance is only defined for sequences of equal length")
        return sum(self.common_typos.get((el1, el2), 1) if el1 != el2 else 0 for el1, el2 in zip(s1, s2))

    @staticmethod
    def indel_distance(s1: str, s2: str) -> int:
        previous_row = range(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                same_letter = math.inf
                if c1 == c2:
                    same_letter = previous_row[j]
                current_row.append(min(insertions, deletions, same_letter))
            previous_row = current_row
        return previous_row[-1]

    def suggest_word(self, word: str) -> str:
        candidates = self.trie.suggestions(word[:1])
        min_distance = math.inf
        suggestion = word
        for candidate in candidates:
            distance = self.levenshtein_distance(word, candidate)
            if distance == 0:
                suggestion = candidate
                break
            if distance < min_distance:
                min_distance = distance
                suggestion = candidate
        return suggestion

    def correct_text_file(self, input_file: str, output_file: str) -> None:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                corrected_line = ' '.join(self.suggest_word(word) for word in line.strip().split())
                outfile.write(corrected_line + '\n')


if __name__ == "__main__":
    path = "words_alpha.txt"
    input_text = "input_text.txt"
    output_text = "output_text.txt"
    autocorrection = Autocorrection(path)
    t1 = time.time()
    autocorrection.correct_text_file(input_text, output_text)
    print(time.time() - t1)
