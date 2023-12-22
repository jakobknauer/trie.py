from dataclasses import dataclass
from typing import Hashable, Self, Iterable, Iterator

from collections import deque


@dataclass
class _Node:
    children: dict[Hashable, Self]
    value: object


class Trie:
    """A *Prefix Tree* or *Trie*.

    The tree holds key-value pairs where the keys are represented by iterables of hashables
    (generalizing strings, which are iterables of one-element strings),
    and values are general objects.

    The time complexity of all single-key operations (inserting, updating,
    checking existence, accessing value) is linear wrt. the length of the key,
    and generally independent of the number of keys in the tree.

    The class provides operations to quickly access all keys with a given prefix.

    Example usage:
        >>> from trie import Trie
        >>> import string

        >>> # initialize tree that allows sequences of lower-case letters as keys
        >>> dictionary = Trie(string.ascii_lowercase)

        >>> # insert english words and their definitions
        >>> dictionary.insert("apple", "A red or green fruit")
        >>> dictionary.insert("banana", "A yellow fruit")
        >>> dictionary.insert("appletree", "A tree on which apples grow")
        >>> # ...

        >>> # print all words in lexicographical order
        >>> for word in dictionary:
        >>>     print("".join(word))

        >>> prefix = "apple"
        >>> # print all words starting with "apple" and their definitions
        >>> for suffix, definition in dictionary.items(prefix):
        >>>     print(f"'{prefix + ''.join(suffix)}' is defined as '{definition}'.")
    """

    def __init__(self, alphabet: Iterable[Hashable]) -> None:
        """Initializes the instance.

        Args:
            alphabet:
                The items the keys used in the tree may consist of.
                Determines the order of iteration of __iter__, keys, values, and items.
        """
        self._alphabet: list[Hashable] = list(alphabet)
        self._sentinel: object = object()  # used as 'value' of nodes to mark them as not occupied
        self._root: _Node = _Node({}, self._sentinel)
        self._count: int = 0

    def __len__(self) -> int:
        """Returns the number of items in the tree."""
        return self._count

    def count(self) -> int:
        """Counts and returns the number of items in the tree.

        As opposed to __len__, this method computes the number when called,
        instead of returning the stored size.
        Only used for testing purposes.
        """
        return self._count_subtree(self._root)

    def size(self) -> int:
        """Counts and returns the number of nodes in the tree.

        As opposed to count, this method also counts unoccupied nodes,
        so the return value of this function will never be smaller than that of count.
        Only used for testing purposes.
        """
        count = 0
        to_visit: deque[_Node] = deque()
        to_visit.append(self._root)

        while to_visit:
            node = to_visit.pop()
            count += 1
            for child in node.children.values():
                to_visit.append(child)

        return count

    def depth(self) -> int:
        """Computes the maximal depth of the tree.

        Only used for testing purposes.
        """
        max_depth = 0
        to_visit: deque[tuple[_Node, int]] = deque()
        to_visit.append((self._root, 0))

        while to_visit:
            node, depth = to_visit.pop()
            max_depth = max(depth, max_depth)
            for child in node.children.values():
                to_visit.append((child, depth + 1))

        return max_depth

    def __contains__(self, key: Iterable[Hashable]) -> bool:
        """Determines if key is contained in the tree."""
        node = self._get_node(key)
        return node is not None and node.value is not self._sentinel

    def __getitem__(self, key: Iterable[Hashable]) -> object:
        """Returns the value for key if key is in the tree, else raises KeyError."""
        node = self._get_node(key)
        if not node or node.value is self._sentinel:
            raise KeyError("Tree does not contain a value for the given key.")
        return node.value

    def get(self, key: Iterable[Hashable], default: object = None) -> object:
        """Returns the value for key if key is in the tree, else returns default."""
        node = self._get_node(key)
        if not node or node.value is self._sentinel:
            return default
        return node.value

    def __iter__(self) -> Iterator[list[Hashable]]:
        """Returns an iterator over the keys in the tree in lexicographical order.

        The lexicographical order of characters of keys is given by the alphabet
        provided upon construction of the Trie instance.
        """
        return iter(self._iterate_keys(self._root))

    def keys(
        self, prefix: Iterable[Hashable] | None = None
    ) -> Iterable[list[Hashable]]:
        """Returns an iterable over the keys in the tree in lexicographical order.

        The lexicographical order of characters of keys is given by the alphabet
        provided upon construction of the Trie instance.

        Args:
            prefix:
                If given, only keys starting with the given prefix are considered.
                If not given or None, all keys are returned.

        Returns:
            An iterator over the keys.
            If prefix is given, only the suffixes of the keys without the prefix are returned.
        """
        prefix = prefix or tuple()
        prefix_node = self._get_node(prefix)
        return self._iterate_keys(prefix_node)

    def values(self, prefix: Iterable[Hashable] | None = None) -> Iterable[object]:
        """Returns an iterable over the values in the tree in lexicographical order of the keys.

        The lexicographical order of characters of keys is given by the alphabet
        provided upon construction of the Trie instance.

        Args:
            prefix:
                If given, only keys starting with the given prefix are considered.
                If not given or None, all keys are returned.
        """
        prefix = prefix or tuple()
        prefix_node = self._get_node(prefix)
        return self._iterate_values(prefix_node)

    def items(
        self, prefix: Iterable[Hashable] | None = None
    ) -> Iterable[tuple[list[Hashable], object]]:
        """Returns an iterable over the key-value pairs in the tree in lexicographical order of the keys.

        The lexicographical order of characters of keys is given by the alphabet
        provided upon construction of the Trie instance.

        Args:
            prefix:
                If given, only keys starting with the given prefix are considered.
                If not given or None, all keys are returned.

        Returns:
            An iterator over the key-value tuples.
            If prefix is given, only the suffixes of the keys without the prefix are returned.
        """
        prefix = prefix or tuple()
        prefix_node = self._get_node(prefix)
        return self._iterate_items(prefix_node)

    def insert(self, key: list[Hashable], value: object) -> None:
        """Inserts key with value."""
        node = self._root
        for character in key:
            if character not in node.children:
                node.children[character] = _Node({}, self._sentinel)
            node = node.children[character]

        if node.value is self._sentinel:
            self._count += 1
        node.value = value

    def __setitem__(self, key: list[Hashable], value: object) -> None:
        """Inserts key with value."""
        self.insert(key, value)

    def remove(self, key: list[Hashable]) -> None:
        """Removes key from the tree if key is in the tree, else raises KeyError."""
        node = self._root
        # the last node in the path to the word to delete that must remain in the tree
        cutoff_node = None
        # the next character to go from cutoff_node to the word to delete
        cutoff_character = None

        for character in key:
            if not character in node.children:
                raise KeyError("Word to delete is not contained in tree.")
            if (
                not cutoff_node
                or node.value is not self._sentinel
                or len(node.children) >= 2
            ):
                cutoff_node = node
                cutoff_character = character
            node = node.children[character]

        if node.value is self._sentinel:
            raise KeyError("Word to delete is not contained in tree.")
        node.value = self._sentinel

        if cutoff_node and not node.children:
            del cutoff_node.children[cutoff_character]
        self._count -= 1

    def __delitem__(self, key: list[Hashable]) -> None:
        """Removes key from the tree if key is in the tree, else raises KeyError."""
        self.remove(key)

    def update(self, other: Self) -> None:
        """Updates the tree, adding key-value pairs from other.

        Is equivalent to:  for k in other: self[k] = other[k].

        This method can be considered an in-place version of the set-theoretic
        union of the keys of both trees,
        where values from the second tree are preferred if a key is present in both.
        """
        to_visit: deque[tuple[_Node, _Node]] = deque()
        to_visit.append((self._root, other._root))

        while to_visit:
            own_node, other_node = to_visit.pop()

            if other_node.value is not other._sentinel:
                if own_node.value is self._sentinel:
                    self._count += 1
                own_node.value = other_node.value

            for character, other_child in other_node.children.items():
                if character not in own_node.children:
                    own_node.children[character] = _Node({}, self._sentinel)
                to_visit.append((own_node.children[character], other_child))

    def __ior__(self, other: Self) -> Self:
        """Updates the tree, adding key-value pairs from other.

        Is equivalent to:  for k in other: self[k] = other[k].

        This operation can be considered an in-place version of the set-theoretic
        union of the keys of both trees,
        where values from the second tree are preferred if a key is present in both.
        """
        self.update(other)
        return self

    def union(self, other: Self) -> Self:
        """Returns the set-theoretic union of the tree and other.

        The set of keys of the returned tree is the union of the keys of both trees,
        where values of the second tree are preferred if both are given.
        """
        third = Trie(self._alphabet)
        third.update(self)
        third.update(other)
        return third  # type: ignore

    def __or__(self: Self, other: Self) -> Self:
        """Returns the set-theoretic union of the tree and other.

        The set of keys of the returned tree is the union of the keys of both trees,
        where values of the second tree are preferred if both are given.
        """
        return self.union(other)

    def difference_update(self, other: Self) -> None:
        """Updates the tree, removing keys found in other, and keeping other keys untouched."""
        for key in other:
            if key in self:
                del self[key]

    def __isub__(self, other: Self) -> Self:
        """Updates the tree, removing keys found in other, and keeping other keys untouched."""
        self.difference_update(other)
        return self

    def difference(self, other: Self) -> Self:
        """Returns the set-theoretic difference of the tree and other.

        The set of keys of the returned tree is the (non-symmetric!) difference
        of the keys of both trees,
        where the values for the remaining keys are taken from self.
        """
        third = Trie(self._alphabet)
        third.update(self)
        third.difference_update(other)
        return third  # type: ignore

    def __sub__(self, other: Self) -> Self:
        """Returns the set-theoretic difference of the tree and other.

        The set of keys of the returned tree is the (non-symmetric!) difference
        of the keys of both trees,
        where the values for the remaining keys are taken from self.
        """
        return self.difference(other)

    def intersection_update(self, other: Self) -> None:
        """Updates the tree, keeping only keys found in it and other, taking values from other."""
        for key in self:
            if key in other:
                self[key] = other[key]
            else:
                del self[key]

    def __iand__(self, other: Self) -> Self:
        """Updates the tree, keeping only keys found in it and other, taking values from other."""
        self.intersection_update(other)
        return self

    def intersection(self, other: Self) -> Self:
        """Returns the set-theoretic intersection of the tree and other.

        The set keys of the returned tree is the intersection of the keys of
        both trees, with values taken from other.
        """
        third = Trie(self._alphabet)
        third.update(self)
        third.intersection_update(other)
        return third  # type: ignore

    def __and__(self, other: Self) -> Self:
        """Returns the set-theoretic intersection of the tree and other.

        The set keys of the returned tree is the intersection of the keys of
        both trees, with values taken from other.
        """
        return self.intersection(other)

    def _get_node(self, key: Iterable[Hashable]) -> _Node | None:
        """Returns the node corresponding to key if key is in the tree, else None."""
        node = self._root
        for character in key:
            if character not in node.children:
                return None
            node = node.children[character]
        return node

    def _iterate_nodes(
        self, node: _Node | None
    ) -> Iterable[tuple[_Node, list[Hashable]]]:
        if not node:
            return

        to_visit: deque[tuple[_Node, list[Hashable]]] = deque()
        to_visit.append((node, []))

        while to_visit:
            node, prefix = to_visit.pop()

            if node.value is not self._sentinel:
                yield node, prefix

            for character in reversed(self._alphabet):
                if character in node.children:
                    to_visit.append((node.children[character], prefix + [character]))

    def _iterate_keys(self, node: _Node | None) -> Iterable[list[Hashable]]:
        return (word for _, word in self._iterate_nodes(node))

    def _iterate_values(self, node: _Node | None) -> Iterable[object]:
        return (node.value for node, _ in self._iterate_nodes(node))

    def _iterate_items(
        self, node: _Node | None
    ) -> Iterable[tuple[list[Hashable], object]]:
        return ((word, node.value) for node, word in self._iterate_nodes(node))

    def _count_subtree(self, node: _Node) -> int:
        count = 0
        to_visit: deque[_Node] = deque()
        to_visit.append(node)

        while to_visit:
            node = to_visit.pop()
            if node.value is not self._sentinel:
                count += 1
            for child in node.children.values():
                to_visit.append(child)

        return count
