import pytest

from lru_cache import LRUCache


def test_insert_and_get():
    cache = LRUCache(2)

    cache.put("A", 10)
    cache.put("B", 20)

    assert cache.get("A") == 10
    assert len(cache) == 2


def test_get_marks_key_as_most_recently_used():
    cache = LRUCache(3)

    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("C", 3)

    assert cache.keys_mru_to_lru() == ["C", "B", "A"]

    assert cache.get("A") == 1

    assert cache.keys_mru_to_lru() == ["A", "C", "B"]


def test_put_evicts_least_recently_used_entry():
    cache = LRUCache(2)

    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("C", 3)

    assert "A" not in cache
    assert cache.get("B") == 2
    assert cache.get("C") == 3


def test_access_changes_which_key_is_evicted():
    cache = LRUCache(2)

    cache.put("A", 1)
    cache.put("B", 2)
    cache.get("A")
    cache.put("C", 3)

    assert "B" not in cache
    assert cache.get("A") == 1


def test_updating_existing_key_does_not_increase_size():
    cache = LRUCache(2)

    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("A", 99)

    assert len(cache) == 2
    assert cache.get("A") == 99


def test_updating_existing_key_marks_it_mru():
    cache = LRUCache(2)

    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("A", 10)

    assert cache.keys_mru_to_lru() == ["A", "B"]


def test_capacity_one():
    cache = LRUCache(1)

    cache.put("A", 1)
    cache.put("B", 2)

    assert len(cache) == 1
    assert "A" not in cache
    assert cache.get("B") == 2


def test_missing_key_raises_key_error():
    cache = LRUCache(2)

    with pytest.raises(KeyError):
        cache.get("missing")


def test_peek_does_not_change_recency():
    cache = LRUCache(2)

    cache.put("A", 1)
    cache.put("B", 2)

    assert cache.peek("A") == 1
    assert cache.keys_mru_to_lru() == ["B", "A"]


@pytest.mark.parametrize("capacity", [0, -1, -100])
def test_non_positive_capacity_raises_value_error(capacity):
    with pytest.raises(ValueError):
        LRUCache(capacity)


@pytest.mark.parametrize("capacity", [1.5, "2", None, True])
def test_non_integer_capacity_raises_type_error(capacity):
    with pytest.raises(TypeError):
        LRUCache(capacity)


def test_none_can_be_a_stored_value():
    cache = LRUCache(1)

    cache.put("A", None)

    assert cache.get("A") is None


def test_falsey_values_are_stored_correctly():
    cache = LRUCache(3)

    cache.put("zero", 0)
    cache.put("false", False)
    cache.put("empty", "")

    assert cache.get("zero") == 0
    assert cache.get("false") is False
    assert cache.get("empty") == ""


def test_peek_missing_key_raises_key_error():
    cache = LRUCache(1)

    with pytest.raises(KeyError):
        cache.peek("missing")


def test_cache_never_exceeds_capacity_after_many_puts():
    cache = LRUCache(4)

    for number in range(100):
        cache.put(number, number * 10)

    assert len(cache) == 4
    assert cache.keys_mru_to_lru() == [99, 98, 97, 96]


def test_unhashable_key_raises_type_error():
    cache = LRUCache(2)

    with pytest.raises(TypeError):
        cache.put(["unhashable"], "value")
