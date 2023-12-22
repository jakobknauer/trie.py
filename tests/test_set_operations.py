"""Tests the following set-theoretic methods of the Trie class:
    update
    __ior__
    union
    __or__
    difference_update
    __isub__
    difference
    __sub__
    intersection_update
    __iand__
    intersection
    __and__
"""


import pytest


@pytest.fixture
def operand1(initialized_tree1):
    """An alias for initialized_tree1 that better fits the domain of binary operations."""
    yield initialized_tree1


@pytest.fixture
def operand2(initialized_tree2):
    """An alias for initialized_tree2 that better fits the domain of binary operations."""
    yield initialized_tree2


UNION_TEST_CASES = [
    ([], [], []),
    ([("a", 5)], [], [("a", 5)]),
    ([], [("b", 6)], [("b", 6)]),
    ([("a", 5)], [("a", 5)], [("a", 5)]),
    ([("a", 5)], [("a", 6)], [("a", 6)]),
    ([("a", 5)], [("b", 6)], [("a", 5), ("b", 6)]),
    ([("a", 5), ("b", 6)], [("b", 6), ("c", 7)], [("a", 5), ("b", 6), ("c", 7)]),
]


@pytest.mark.parametrize(["items1", "items2", "union_items"], UNION_TEST_CASES)
def test_update(operand1, operand2, union_items, items2):
    operand1.update(operand2)
    assert len(operand1) == len(union_items)
    assert [("".join(key), value) for key, value in operand1.items()] == union_items
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(["items1", "items2", "union_items"], UNION_TEST_CASES)
def test_ior(operand1, operand2, union_items, items2):
    operand1 |= operand2
    assert len(operand1) == len(union_items)
    assert [("".join(key), value) for key, value in operand1.items()] == union_items
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(["items1", "items2", "union_items"], UNION_TEST_CASES)
def test_union(operand1, operand2, union_items, items1, items2):
    union = operand1.union(operand2)
    assert len(union) == len(union_items)
    assert [("".join(key), value) for key, value in union.items()] == union_items
    assert [("".join(key), value) for key, value in operand1.items()] == items1
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(["items1", "items2", "union_items"], UNION_TEST_CASES)
def test_or(operand1, operand2, union_items, items1, items2):
    union = operand1 | operand2
    assert len(union) == len(union_items)
    assert [("".join(key), value) for key, value in union.items()] == union_items
    assert [("".join(key), value) for key, value in operand1.items()] == items1
    assert [("".join(key), value) for key, value in operand2.items()] == items2


DIFFERENCE_TEST_CASES = [
    ([], [], []),
    ([("a", 5)], [], [("a", 5)]),
    ([], [("b", 6)], []),
    ([("a", 5)], [("a", 5)], []),
    ([("a", 5)], [("a", 6)], []),
    ([("a", 5)], [("b", 6)], [("a", 5)]),
    ([("a", 5), ("b", 6)], [("b", 6), ("c", 7)], [("a", 5)]),
]


@pytest.mark.parametrize(
    ["items1", "items2", "difference_items"], DIFFERENCE_TEST_CASES
)
def test_difference_update(operand1, operand2, difference_items, items2):
    operand1.difference_update(operand2)
    assert len(operand1) == len(difference_items)
    assert [
        ("".join(key), value) for key, value in operand1.items()
    ] == difference_items
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(
    ["items1", "items2", "difference_items"], DIFFERENCE_TEST_CASES
)
def test_isub(operand1, operand2, difference_items, items2):
    operand1 -= operand2
    assert len(operand1) == len(difference_items)
    assert [
        ("".join(key), value) for key, value in operand1.items()
    ] == difference_items
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(
    ["items1", "items2", "difference_items"], DIFFERENCE_TEST_CASES
)
def test_difference(operand1, operand2, difference_items, items1, items2):
    difference = operand1.difference(operand2)
    assert len(difference) == len(difference_items)
    assert [
        ("".join(key), value) for key, value in difference.items()
    ] == difference_items
    assert [("".join(key), value) for key, value in operand1.items()] == items1
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(
    ["items1", "items2", "difference_items"], DIFFERENCE_TEST_CASES
)
def test_sub(operand1, operand2, difference_items, items1, items2):
    difference = operand1 - operand2
    assert len(difference) == len(difference_items)
    assert [
        ("".join(key), value) for key, value in difference.items()
    ] == difference_items
    assert [("".join(key), value) for key, value in operand1.items()] == items1
    assert [("".join(key), value) for key, value in operand2.items()] == items2


INTERSECTION_TEST_CASES = [
    ([], [], []),
    ([("a", 5)], [], []),
    ([], [("b", 6)], []),
    ([("a", 5)], [("a", 5)], [("a", 5)]),
    ([("a", 5)], [("a", 6)], [("a", 6)]),
    ([("a", 5)], [("b", 6)], []),
    ([("a", 5), ("b", 6)], [("b", 6), ("c", 7)], [("b", 6)]),
]


@pytest.mark.parametrize(
    ["items1", "items2", "intersection_items"], INTERSECTION_TEST_CASES
)
def test_intersection_update(operand1, operand2, intersection_items, items2):
    operand1.intersection_update(operand2)
    assert len(operand1) == len(intersection_items)
    assert [
        ("".join(key), value) for key, value in operand1.items()
    ] == intersection_items
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(
    ["items1", "items2", "intersection_items"], INTERSECTION_TEST_CASES
)
def test_iand(operand1, operand2, intersection_items, items2):
    operand1 &= operand2
    assert len(operand1) == len(intersection_items)
    assert [
        ("".join(key), value) for key, value in operand1.items()
    ] == intersection_items
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(
    ["items1", "items2", "intersection_items"], INTERSECTION_TEST_CASES
)
def test_intersection(operand1, operand2, intersection_items, items1, items2):
    intersection = operand1.intersection(operand2)
    assert len(intersection) == len(intersection_items)
    assert [
        ("".join(key), value) for key, value in intersection.items()
    ] == intersection_items
    assert [("".join(key), value) for key, value in operand1.items()] == items1
    assert [("".join(key), value) for key, value in operand2.items()] == items2


@pytest.mark.parametrize(
    ["items1", "items2", "intersection_items"], INTERSECTION_TEST_CASES
)
def test_and(operand1, operand2, intersection_items, items1, items2):
    intersection = operand1 & operand2
    assert len(intersection) == len(intersection_items)
    assert [
        ("".join(key), value) for key, value in intersection.items()
    ] == intersection_items
    assert [("".join(key), value) for key, value in operand1.items()] == items1
    assert [("".join(key), value) for key, value in operand2.items()] == items2
