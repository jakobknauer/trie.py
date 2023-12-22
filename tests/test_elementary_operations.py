"""Tests the interaction of the following elementary operations of the Trie class:
    __init__
    __len__
    __in__
    insert
    __setitem__
    get
    __getitem__
    remove
    __del__
"""


import pytest


def test_len_on_empty_tree(tree):
    assert len(tree) == 0


def test_insert_and_len(tree):
    tree.insert("a", 5)
    assert len(tree) == 1


def test_setitem_and_len(tree):
    tree["a"] = 5
    assert len(tree) == 1


def test_in_on_empty_tree(tree):
    assert "a" not in tree


def test_insert_and_in(tree):
    tree.insert("a", 5)
    assert "a" in tree


def test_setitem_and_in(tree):
    tree["a"] = 5
    assert "a" in tree


def test_get_on_empty_tree(tree):
    assert tree.get("b") is None
    assert tree.get("b", 6) == 6


def test_insert_and_get(tree):
    tree.insert("a", 5)
    assert tree.get("a") == 5


def test_get_with_invalid_key(tree):
    tree.insert("a", 5)
    assert tree.get("b") is None
    assert tree.get("b", 6) == 6


def test_getitem_on_empty_tree(tree):
    with pytest.raises(KeyError):
        _ = tree["b"]


def test_setitem_and_getitem(tree):
    tree["a"] = 5
    assert tree["a"] == 5


def test_getitem_with_invalid_key(tree):
    tree.insert("a", 5)
    with pytest.raises(KeyError):
        _ = tree["b"]


def test_insert_same_key_twice_and_get(tree):
    tree.insert("a", 5)
    tree.insert("a", 6)
    assert tree.get("a") == 6


def test_setitem_same_key_twice_and_get(tree):
    tree["a"] = 5
    tree["a"] = 6
    assert tree.get("a") == 6


def test_remove_on_empty_tree(tree):
    with pytest.raises(KeyError):
        tree.remove("a")


def test_insert_and_remove(tree):
    tree.insert("a", 5)
    tree.remove("a")
    assert len(tree) == 0
    assert "a" not in tree
    assert tree.get("a") is None


def test_remove_invalid_key(tree):
    tree.insert("b", 6)
    with pytest.raises(KeyError):
        tree.remove("a")
    assert len(tree) == 1
    assert "b" in tree
    assert tree["b"] == 6


def test_del_on_empty_tree(tree):
    with pytest.raises(KeyError):
        del tree["a"]


def test_insert_and_del(tree):
    tree.insert("a", 5)
    del tree["a"]
    assert len(tree) == 0
    assert "a" not in tree
    assert tree.get("a") is None


def test_insert_and_del_inner_node(tree):
    tree.insert("a", 5)
    tree.insert("aa", 6)
    del tree["a"]
    assert len(tree) == 1
    assert "a" not in tree
    assert tree.get("a") is None
    assert "aa" in tree
    assert tree.get("aa") == 6


def test_del_invalid_key(tree):
    tree.insert("b", 6)
    with pytest.raises(KeyError):
        del tree["a"]
    assert len(tree) == 1
    assert "b" in tree
    assert tree["b"] == 6


def test_del_invalid_key_on_inner_node(tree):
    tree.insert("aa", 6)
    with pytest.raises(KeyError):
        del tree["a"]
    assert len(tree) == 1
    assert "aa" in tree
    assert tree["aa"] == 6
