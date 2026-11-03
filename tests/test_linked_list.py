import pytest

from linked_list import DoublyLinkedList, Node


def test_new_list_is_empty():
    linked_list = DoublyLinkedList()

    assert linked_list.is_empty()
    assert len(linked_list) == 0


def test_add_nodes_to_front():
    linked_list = DoublyLinkedList()

    first = Node("A", 1)
    second = Node("B", 2)

    linked_list.add_to_front(first)
    linked_list.add_to_front(second)

    assert linked_list.keys_mru_to_lru() == ["B", "A"]
    assert len(linked_list) == 2


def test_remove_middle_node():
    linked_list = DoublyLinkedList()

    nodes = [Node(key, key.lower()) for key in "ABC"]

    for node in nodes:
        linked_list.add_to_front(node)

    linked_list.remove(nodes[1])

    assert linked_list.keys_mru_to_lru() == ["C", "A"]
    assert len(linked_list) == 2


def test_move_node_to_front():
    linked_list = DoublyLinkedList()

    nodes = [Node(key, key.lower()) for key in "ABC"]

    for node in nodes:
        linked_list.add_to_front(node)

    linked_list.move_to_front(nodes[0])

    assert linked_list.keys_mru_to_lru() == ["A", "C", "B"]


def test_move_front_node_is_noop():
    linked_list = DoublyLinkedList()

    node = Node("A", 1)
    linked_list.add_to_front(node)

    linked_list.move_to_front(node)

    assert linked_list.keys_mru_to_lru() == ["A"]


def test_pop_lru():
    linked_list = DoublyLinkedList()

    a = Node("A", 1)
    b = Node("B", 2)
    c = Node("C", 3)

    linked_list.add_to_front(a)
    linked_list.add_to_front(b)
    linked_list.add_to_front(c)

    removed = linked_list.pop_lru()

    assert removed is a
    assert linked_list.keys_mru_to_lru() == ["C", "B"]


def test_pop_lru_from_empty_list_raises():
    with pytest.raises(IndexError):
        DoublyLinkedList().pop_lru()


def test_cannot_insert_already_linked_node():
    linked_list = DoublyLinkedList()
    node = Node("A", 1)

    linked_list.add_to_front(node)

    with pytest.raises(ValueError):
        linked_list.add_to_front(node)


def test_cannot_remove_detached_node():
    linked_list = DoublyLinkedList()

    with pytest.raises(ValueError):
        linked_list.remove(Node("A", 1))
