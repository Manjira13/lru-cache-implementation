"""A manually implemented doubly linked list for LRU cache entries."""

from __future__ import annotations

from typing import Iterator, Optional


class Node:
    """A node stores a cache key/value pair and links to adjacent nodes."""

    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key: object = None, value: object = None) -> None:
        self.key = key
        self.value = value
        self.prev: Optional[Node] = None
        self.next: Optional[Node] = None

    def __repr__(self) -> str:
        return f"Node(key={self.key!r}, value={self.value!r})"


class DoublyLinkedList:
    """
    Doubly linked list with sentinel head and tail nodes.

    The most-recently-used real node is immediately after head.
    The least-recently-used real node is immediately before tail.
    """

    def __init__(self) -> None:
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def is_empty(self) -> bool:
        return self._size == 0

    def add_to_front(self, node: Node) -> None:
        """Insert an existing, detached node immediately after head. O(1)."""
        if node is self.head or node is self.tail:
            raise ValueError("Sentinel nodes cannot be inserted.")

        if node.prev is not None or node.next is not None:
            raise ValueError("Node must be detached before insertion.")

        first = self.head.next

        node.prev = self.head
        node.next = first
        self.head.next = node
        first.prev = node
        self._size += 1

    def remove(self, node: Node) -> None:
        """Remove a node already belonging to this list. O(1)."""
        if node is self.head or node is self.tail:
            raise ValueError("Cannot remove a sentinel node.")

        if node.prev is None or node.next is None:
            raise ValueError("Node is not currently linked.")

        previous_node = node.prev
        next_node = node.next

        previous_node.next = next_node
        next_node.prev = previous_node

        node.prev = None
        node.next = None
        self._size -= 1

    def move_to_front(self, node: Node) -> None:
        """Move a linked node to the MRU position. O(1)."""
        if node is self.head or node is self.tail:
            raise ValueError("Cannot move a sentinel node.")

        if node.prev is None or node.next is None:
            raise ValueError("Node is not currently linked.")

        if node.prev is self.head:
            return

        self.remove(node)
        self.add_to_front(node)

    def pop_lru(self) -> Node:
        """Remove and return the least-recently-used node. O(1)."""
        if self.is_empty():
            raise IndexError("Cannot evict from an empty linked list.")

        lru_node = self.tail.prev
        self.remove(lru_node)
        return lru_node

    def iter_nodes(self) -> Iterator[Node]:
        """Iterate from MRU to LRU."""
        current = self.head.next

        while current is not None and current is not self.tail:
            yield current
            current = current.next

    def keys_mru_to_lru(self) -> list:
        """Return keys in recency order."""
        return [node.key for node in self.iter_nodes()]
