"""Tests the following methods of the Trie class returning iterators/iterables:
    __iter__
    keys
    items
    values
"""


import pytest


ITERATOR_TEST_CASES = [
    ([], []),
    ([("a", 5)], [("a", 5)]),
    ([("a", 5), ("b", 6)], [("a", 5), ("b", 6)]),
    ([("b", 6), ("a", 5)], [("a", 5), ("b", 6)]),
    ([("aa", 6), ("a", 5)], [("a", 5), ("aa", 6)]),
    ([("ab", 6), ("aa", 7), ("a", 5)], [("a", 5), ("aa", 7), ("ab", 6)]),
    ([("ab", 6), ("a", 5), ("b", 7)], [("a", 5), ("ab", 6), ("b", 7)]),
]

ITERATOR_TEST_CASES_WITH_PREFIX = [
    ("",) + test_case for test_case in ITERATOR_TEST_CASES
] + [
    ("a", [], []),
    ("a", [("b", 6)], []),
    ("b", [("b", 6)], [("", 6)]),
    ("b", [("a", 5), ("b", 6)], [("", 6)]),
    ("b", [("a", 5), ("b", 6), ("bb", 7), ("ba", 8)], [("", 6), ("a", 8), ("b", 7)]),
]


@pytest.mark.parametrize(
    ["items_in_insertion_order", "items_in_expected_order"],
    ITERATOR_TEST_CASES,
)
def test_iter(initialized_tree, items_in_expected_order):
    assert list(map("".join, initialized_tree)) == [
        key for key, _ in items_in_expected_order
    ]


@pytest.mark.parametrize(
    ["prefix", "items_in_insertion_order", "items_in_expected_order"],
    ITERATOR_TEST_CASES_WITH_PREFIX,
)
def test_keys(initialized_tree, prefix, items_in_expected_order):
    assert list(map("".join, initialized_tree.keys(prefix))) == [
        key for key, _ in items_in_expected_order
    ]


@pytest.mark.parametrize(
    ["prefix", "items_in_insertion_order", "items_in_expected_order"],
    ITERATOR_TEST_CASES_WITH_PREFIX,
)
def test_items(initialized_tree, prefix, items_in_expected_order):
    assert [
        ("".join(key), value) for key, value in initialized_tree.items(prefix)
    ] == items_in_expected_order


@pytest.mark.parametrize(
    ["prefix", "items_in_insertion_order", "items_in_expected_order"],
    ITERATOR_TEST_CASES_WITH_PREFIX,
)
def test_values(initialized_tree, prefix, items_in_expected_order):
    assert list(initialized_tree.values(prefix)) == [
        value for _, value in items_in_expected_order
    ]
