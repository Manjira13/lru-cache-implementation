"""Run a small demonstration of the LRU cache."""

from lru_cache import LRUCache


def main() -> None:
    cache = LRUCache(capacity=3)

    print("Insert A, B and C")

    cache.put("A", 100)
    cache.put("B", 200)
    cache.put("C", 300)

    print("MRU -> LRU:", cache.keys_mru_to_lru())

    print("\nAccess A")

    print("cache.get('A') =", cache.get("A"))
    print("MRU -> LRU:", cache.keys_mru_to_lru())

    print("\nInsert D (the least-recently-used key is evicted)")

    cache.put("D", 400)

    print("MRU -> LRU:", cache.keys_mru_to_lru())
    print("Cache:", cache)

    print("\nIs B still present?", "B" in cache)
    print("Is A still present?", "A" in cache)


if __name__ == "__main__":
    main()
