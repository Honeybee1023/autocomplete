"""
6.101 Lab:
Autocomplete
"""

# NO ADDITIONAL IMPORTS!

# import string # optional import
# import pprint # optional import
# import typing # optional import
import doctest
from text_tokenize import tokenize_sentences


class PrefixTree:
    """
    Stores a condensed mapping from word strings to values.
    """

    def __init__(self):
        self.value = None
        self.children = {}

    def __setitem__(self, word, value):
        """
        Mutates the tree so that the word is associated with the given value.
        Raises a TypeError if the given word is not a string.
        """
        # tree[1]=True should raise type error
        if not isinstance(word, str):
            raise TypeError

        # tree[''] = 7 doesn't add any nodes and only sets the value of the top node to 7
        if word == "":
            self.value = value
            return

        # Traverse/create nodes for longer words
        for ch in word:
            if ch not in self.children:
                # create a new PrefixTree node for this child
                child = PrefixTree()
                self.children[ch] = child
            self = self.children[ch]
        # after we find the node for this word
        self.value = value

    def __getitem__(self, word):
        """
        Returns the value for the specified word.
        Raises a KeyError if the given word is not in the tree.
        Raises a TypeError if the given word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError
        
        if word == "":
            if self.value is not None:
                return self.value
            else:
                raise KeyError
        
        for ch in word:
            if ch not in self.children:
                raise KeyError
            self = self.children[ch]

        if self.value is not None:
            return self.value
        else:
            raise KeyError
            

    def __contains__(self, word):
        """
        Returns a boolean indicating whether the given word has a set value in the tree.
        Raises a TypeError if the given key is not a string.
        """
        if not isinstance(word, str):
            raise TypeError

        if word == "":
            return self.value is not None

        for ch in word:
            if ch not in self.children:
                return False
            self = self.children[ch]

        return self.value is not None

    def __iter__(self):
        """
        Generator that yields tuples of all the (word, value) pairs in the tree.
        """
        if self.value is not None:
            yield ("", self.value)

        for ch, child in self.children.items():
            for suffix, val in child:
                yield (ch + suffix, val)

    def __delitem__(self, word):
        """
        Deletes the value of the given word from the tree.
        Raises a KeyError if the given word does not exist.
        Raises a TypeError if the given word is not a string.
        """
        if not isinstance(word, str):
            raise TypeError

        if word == "":
            if self.value is not None:
                self.value = None
                return
            else:
                raise KeyError

        path = []
        for ch in word:
            if ch not in self.children:
                raise KeyError
            path.append((self, ch))
            self = self.children[ch]

        if self.value is None:
            raise KeyError

        self.value = None

        for parent, ch in reversed(path):
            child = parent.children[ch]
            if child.value is None and not child.children:
                del parent.children[ch]
            else:
                break


def word_frequencies(text):
    """
    Given a piece of text as a single string, creates and returns a prefix tree whose
    keys are the words that appear in the text, and whose values are the number of times
    the associated word appears in the text.
    """
    sentences = tokenize_sentences(text)
    tree = PrefixTree()
    word_count = {}
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
    for word, count in word_count.items():
        tree[word] = count
    return tree

def autocomplete(tree, prefix, max_count=None):
    """
    Returns the set of the most-frequently occurring words that start with the given
    prefix string in the given tree. Includes only the top max_count most common words
    if max_count is specified, otherwise returns all auto-completions.
    """
    final_words = []

    #get to current spot first
    node = tree
    for ch in prefix:
        if ch not in node.children:
            return set()
        node = node.children[ch]

    for suffix, value in node:
        final_words.append((prefix + suffix, value))

    #sort highest to lowest frequency
    final_words.sort(key=lambda x: x[1], reverse=True)

    if max_count is not None:
        final_words = final_words[0:max_count]

    return set(word for word, _ in final_words)


def generate_edits(word):
    """
    Generates and yields all the possible ways to edit the given word string consisting
    entirely of lowercase letters in the range from "a" to "z".

    An edit for a word can be any one of the following:
    * A single insertion (add a single letter from "a" to "z" anywhere in the word)
    * A single deletion  (remove any one character from the word)
    * A single replacement (replace any one character in the word with a character in
      the range "a" to "z")
    * A two-character transpose (switch the positions of any two adjacent characters)

    Must be a generator! May output duplicate edits or the original word.
    """
    letters = 'abcdefghijklmnopqrstuvwxyz'
    length = len(word)

    # Insertion
    for i in range(length + 1):
        for ch in letters:
            yield word[:i] + ch + word[i:]

    # Deletion
    for i in range(length):
        yield word[:i] + word[i+1:]

    # Replacement
    for i in range(length):
        for ch in letters:
            yield word[:i] + ch + word[i+1:]

    # Transpose
    for i in range(length - 1):
        yield word[:i] + word[i+1] + word[i] + word[i+2:]


def autocorrect(tree, prefix, max_count=None):
    """
    Returns the set of words that represent valid ways to autocorrect the given prefix
    string. Starts by including auto-completions. If there are fewer than max_count
    auto-completions (or if max_count is not specified), then includes the
    most-frequently occurring words that differ from prefix by a small edit, up to
    max_count total elements (or all elements if max_count is not specified).
    """
    raise NotImplementedError


def word_filter(tree, pattern):
    """
    Returns a set of all the words in the given tree that match the given
    pattern string. Each character in the pattern is one of:
        - '*' - matches any sequence of zero or more characters,
        - '?' - matches any single character,
        - otherwise the character must match the character in the word.
    """
    raise NotImplementedError


if __name__ == "__main__":
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    # doctest.run_docstring_examples( # runs doctests for one function
    #    PrefixTree.__getitem__,
    #    globals(),
    #    optionflags=_doctest_flags,
    #    verbose=True
    # )
