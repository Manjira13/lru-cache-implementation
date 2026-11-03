LRU Cache Implementation in Python
A from-scratch implementation of a Least Recently Used (LRU) Cache using a Python dictionary and a custom doubly linked list.
The project demonstrates core Data Structures and Algorithms concepts, object-oriented programming, pointer/reference manipulation, time-complexity analysis, and unit testing with `pytest`.
> This implementation does not use `OrderedDict`, `functools.lru_cache`, or third-party cache libraries.
Features
Configurable positive-integer cache capacity.
`get(key)` retrieves a value and marks the entry as most recently used.
`put(key, value)` inserts a new entry or updates an existing entry.
Automatic eviction of the least recently used entry when capacity is exceeded.
Average O(1) lookup, insertion, update, recency changes, and eviction.
Custom doubly linked list with sentinel head and tail nodes.
Explicit handling of invalid capacity and missing keys.
Unit tests for normal behaviour and edge cases.
How an LRU Cache works
An LRU cache has a limited capacity. When it is full and a new item is inserted, the item that has not been used for the longest time is removed.
The cache tracks recency:
MRU (Most Recently Used): the entry accessed or updated most recently.
LRU (Least Recently Used): the entry that has gone the longest without being accessed.
For example, with a capacity of 3:
```text
Insert A       MRU -> A
Insert B       MRU -> B -> A
Insert C       MRU -> C -> B -> A  <- LRU
Access A       MRU -> A -> C -> B  <- LRU
Insert D       MRU -> D -> A -> C  <- LRU
```
When `D` is inserted, `B` is evicted because it is the least recently used entry.
Architecture
The implementation combines two data structures because each solves a different part of the problem efficiently.
```text
                    LRUCache
                       |
             +---------+---------+
             |                   |
         Dictionary          Doubly Linked List
         key -> Node         MRU <-> ... <-> LRU
             |                   |
             +---- references ---+
```
1. Hash map (Python dictionary)
The dictionary maps each key to its corresponding linked-list node:
```python
{
    "A": node_a,
    "B": node_b
}
```
This provides average O(1) access to the node for a given key.
2. Doubly linked list
The custom linked list maintains usage order:
```text
HEAD <-> [MRU] <-> [...] <-> [LRU] <-> TAIL
```
The list uses dummy/sentinel `head` and `tail` nodes. The first real node is the MRU entry; the last real node is the LRU entry.
Because each real node has both `prev` and `next` references, a known node can be detached and re-linked without traversing the list.
3. Node
Each node stores:
`key`: the cache key.
`value`: the cached value.
`prev`: reference to the previous node.
`next`: reference to the next node.
The key is stored in the node so that eviction can also remove the corresponding dictionary entry.
Project structure
```text
lru-cache-python/
├── README.md
├── main.py
├── lru_cache.py
├── linked_list.py
├── requirements.txt
├── .gitignore
├── LICENSE
└── tests/
    ├── __init__.py
    ├── test_linked_list.py
    └── test_lru_cache.py
```
Requirements
Python 3.10 or later
pip
pytest (for running tests)
Setup
Clone the repository:
```bash
git clone https://github.com/YOUR-USERNAME/lru-cache-python.git
cd lru-cache-python
```
Create and activate a virtual environment.
Windows PowerShell:
```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
```
macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```
Install dependencies:
```bash
python -m pip install -r requirements.txt
```
Run the demonstration
```bash
python main.py
```
The demonstration inserts entries, accesses an existing key, and inserts another key to trigger LRU eviction.
Usage
```python
from lru_cache import LRUCache

cache = LRUCache(capacity=2)

cache.put("apple", 100)
cache.put("banana", 200)

print(cache.get("apple"))  # 100; apple becomes MRU

cache.put("cherry", 300)   # banana is evicted

print("banana" in cache)   # False
print(cache.get("cherry")) # 300
print(cache.keys_mru_to_lru())  # ['cherry', 'apple']
```
API behaviour
Method	Behaviour
`LRUCache(capacity)`	Creates a cache with a positive integer capacity
`put(key, value)`	Inserts or updates an entry; makes it MRU
`get(key)`	Returns the value and makes the entry MRU
`peek(key)`	Returns the value without changing recency
`key in cache`	Checks whether a key is present
`len(cache)`	Returns the number of cached entries
`keys_mru_to_lru()`	Returns keys ordered from MRU to LRU
A missing key passed to `get()` or `peek()` raises `KeyError`, matching Python dictionary behaviour.
Invalid capacities raise:
`TypeError` if capacity is not an integer (including `bool`).
`ValueError` if capacity is zero or negative.
Keys must be hashable, as required by Python dictionaries.
Time and space complexity
Operation	Average time complexity	Reason
Dictionary lookup	O(1)	Average-case hash-table lookup
Add node to front	O(1)	A fixed number of reference updates
Remove known node	O(1)	Uses the node's `prev` and `next` references
Move node to front	O(1)	Detach and re-link a known node
Get	O(1)	Dictionary lookup plus list update
Put/update	O(1)	Dictionary operation plus list update
Evict LRU	O(1)	LRU node is immediately before the tail sentinel
Overall cache operations: O(1) average time, assuming average-case dictionary operations.
Space complexity: O(capacity). The dictionary and linked list each store at most `capacity` real entries, plus two sentinel nodes in the linked list.
Run tests
From the project root:
```bash
python -m pytest -v
```
The test suite covers:
Empty-list and sentinel initialisation.
Insertion, removal, and movement of linked-list nodes.
LRU eviction.
Recency updates after `get()` and `put()`.
Updating an existing key.
Capacity-one behaviour.
Missing keys.
Invalid capacities.
Falsey values and `None`.
Unhashable keys.
Capacity limits after repeated insertions.
Design decisions
Dictionary + doubly linked list: the dictionary locates nodes; the list maintains recency.
Sentinel nodes: reduce special-case logic for insertion and deletion at list boundaries.
Key stored in each node: allows dictionary cleanup during eviction.
`KeyError` for missing keys: provides predictable behaviour consistent with Python dictionaries.
Separate linked-list tests: makes it easier to isolate pointer-management bugs from cache-logic bugs.
Limitations
This is an in-memory cache; entries are not persisted.
The implementation is not thread-safe.
It uses a fixed capacity and does not implement expiration/TTL.
Average O(1) dictionary complexity is expected; dictionary operations have O(n) worst-case behaviour under pathological hash collisions.
Learning outcomes
This project is intended to demonstrate practical understanding of:
Hash maps and average-case lookup complexity.
Singly and doubly linked lists.
Nodes and object references.
Head/tail sentinel management.
Insertion, deletion, and node repositioning.
Object-oriented design and encapsulation.
Time and space complexity.
Edge-case handling and unit testing.
Future improvements
Possible extensions:
Add thread-safety with a lock.
Add an optional cache statistics feature (hits, misses, and evictions).
Add a benchmark comparing this implementation with a simpler list-based approach.
Add generic type annotations for keys and values.
License
This project is released under the MIT License. See LICENSE.
