import string

import pytest

from trie import Trie


@pytest.fixture
def tree():
    """An empty tree."""
    return Trie(string.ascii_lowercase)


# Copies of the tree fixture, for when a test requires multiple empty trees
tree1 = tree
tree2 = tree


@pytest.fixture
def initialized_tree(tree, items_in_insertion_order):
    """A tree where given key-value pairs where inserted in a given order."""
    for key, value in items_in_insertion_order:
        tree.insert(key, value)
    return tree


@pytest.fixture
def initialized_tree1(tree1, items1):
    """
    Similar to initialized_tree but with renamed parameters,
    such that indirect parametrization can be done independently.
    """
    for key, value in items1:
        tree1.insert(key, value)
    return tree1


@pytest.fixture
def initialized_tree2(tree2, items2):
    """
    Similar to initialized_tree but with renamed parameters,
    such that indirect parametrization can be done independently.
    """
    for key, value in items2:
        tree2.insert(key, value)
    return tree2
