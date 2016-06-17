# PyTrie
A python implementation of a dictionary using a Trie

Example usage:
```python
    t = Trie()
    print "size", len(t)
    t["test 1"] = "a word"
    print "size", len(t)
    t["test 1"] = "aaa word"
    print "size", len(t)
    t["test 2"] = 9
    t["now this is a very long string"*30] = set()
    print len(t)
    print t.items()
    print t.keys()
    print t.values()
    print t["test 2"]
    print "test 1" in t
    print t["now this is a very long string"*30]
    del t["test 1"]
    print len(t)
    print "test 1" in t
    print t.get("test 1", "it's not in here")
    print t
  ```
