import json

_end = '_end_'

def make_trie(*words):
    root = dict()
    for word in words:
        current_dict = root
        for letter in word:
            current_dict = current_dict.setdefault(letter, {})
        current_dict[_end] = _end
    return root

with open('google-10000-english-usa-no-swears-medium.txt', 'r') as f:
    wordList = [line.strip() for line in f]

with open('google-10000-english-usa-no-swears-short.txt', 'r') as f:
    shortWordList = [line.strip() for line in f]
    
# * means yes, % means no
trie = make_trie(*shortWordList, *wordList, '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '*', '%')
with open('trie.json', 'w') as f:
    json.dump(trie, f)

print(trie)