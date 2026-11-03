"""LRU Cache using a dictionary and custom doubly linked list."""

from __future__ import annotations

from typing import Any

from linked_list import DoublyLinkedList, Node


class LRUCache:
    """
    Fixed-capacity LRU cache.

    get(key) returns the value and marks the entry as MRU.
    A missing key raises KeyError.
    put(key, value) inserts or updates an entry.
    """

    def __init__(self, capacity: int) -> None:
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an integer.")

        if capacity <= 0:
            raise ValueError("capacity must be greater than zero.")

        self.capacity = capacity
        self.cache: dict[Any, Node] = {}
        self._order = DoublyLinkedList()

    def __len__(self) -> int:
        return len(self.cache)

    def __contains__(self, key: object) -> bool:
        return key in self.cache

    def get(self, key: Any) -> Any:
        """Return a value and mark its entry as MRU. O(1) average."""
        if key not in self.cache:
            raise KeyError(key)

        node = self.cache[key]
        self._order.move_to_front(node)

        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Insert or update an entry. O(1) average."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._order.move_to_front(node)
            return

        node = Node(key, value)

        self.cache[key] = node
        self._order.add_to_front(node)

        if len(self.cache) > self.capacity:
            lru_node = self._order.pop_lru()
            del self.cache[lru_node.key]

    def peek(self, key: Any) -> Any:
        """Return a value without changing recency."""
        if key not in self.cache:
            raise KeyError(key)

        return self.cache[key].value

    def keys_mru_to_lru(self) -> list:
        """Return keys from most to least recently used."""
        return self._order.keys_mru_to_lru()

    def __repr__(self) -> str:
        entries = [
            f"{node.key!r}: {node.value!r}"
            for node in self._order.iter_nodes()
        ]

        return (
            f"LRUCache(capacity={self.capacity}, "
            f"entries=[{', '.join(entries)}])"
        )
