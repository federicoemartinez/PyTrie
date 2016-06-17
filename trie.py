from collections import defaultdict
from collections import MutableMapping


class Trie(MutableMapping):

    class TrieNode(object):
        __slots__ = ("_children", "value", "has_value")

        def __init__(self):
            self._children = defaultdict(lambda: Trie.TrieNode())
            self.value = None
            self.has_value = False

        def _traverse(self, base_case, recursion_shortcut, post_process, key, index, has_to_shortcut=True):
            if len(key) == index:
                return base_case(self, key, index)
            else:
                next_key_part = key[index]
                if (not has_to_shortcut) or next_key_part in self._children:
                    child = self._children[next_key_part]
                    recursion_result = child._traverse(base_case, recursion_shortcut, post_process, key, index + 1,
                                                       has_to_shortcut)
                else:
                    return recursion_shortcut(self, key, index)
                return post_process(self, key, index, recursion_result)

        def _set_node(self, value):
            res = 0 if self.has_value else 1
            self.has_value = True
            self.value = value
            return res

        def define(self, key, value):
            base_case = lambda s, k, i: s._set_node(value)
            shortcut = lambda s, k, i: None
            post_process = lambda s, k, i, prev: prev
            return self._traverse(base_case, shortcut, post_process, key, 0, has_to_shortcut=False)

        def _get_value(self):
            if self.has_value:
                return self.value
            raise KeyError

        def get(self, key):
            base_case = lambda s, k, i: s._get_value()

            def shortcut(s, k, i): raise KeyError

            post_process = lambda s, k, i, prev: prev
            return self._traverse(base_case, shortcut, post_process, key, 0)

        def has_key(self, key):
            base_case = lambda s, k, i: s.has_value
            rec_shortcut = lambda s, k, i: False
            post_process = lambda s, k, i, prev: prev
            return self._traverse(base_case, rec_shortcut, post_process, key, 0)

        def delete_key(self, key):
            base_case = lambda s, key, index: s._empty_node()
            rec_shortcut = lambda s, k, i: 0
            post_process = lambda s, k, i, prev_res: s._prune_tree(k, i, prev_res)
            return self._traverse(base_case, rec_shortcut, post_process, key, 0)

        def _empty_node(self):
            self.has_value = False
            self.value = None
            return 1

        def _prune_tree(self, key, index, prev_res):
            if (not self._children[key[index]].has_value) and \
                            len(self._children[key[index]]._children) == 0:
                del self._children[key[index]]
            return prev_res

        def keys(self):
            pseudo_items = self._keys()
            items = []
            for word in pseudo_items:
                items.append("".join(reversed(word)))
            return items

        def _keys(self):
            words = []
            if self.has_value or len(self._children) == 0:
                words = [[]]
            for letter, child in self._children.iteritems():
                child_words = child._keys()
                for acum_letters in child_words:
                    acum_letters.append(letter)
                    words.append(acum_letters)
            return words

    def __init__(self):
        self._trie_node = Trie.TrieNode()
        self._size = 0

    def __contains__(self, key):
        return self._trie_node.has_key(key)

    def __iter__(self):
        return self._trie_node.keys().__iter__()

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        return self._trie_node.get(key)

    def __setitem__(self, key, value):
        self._size += self._trie_node.define(key, value)

    def __delitem__(self, key):
        self._size -= self._trie_node.delete_key(key)

    def __eq__(self, other):
        for each in self:
            if each in other and self[each] == other[each]:
                continue
            return False
        return True

    def __ne__(self, other):
        return not (self.__eq__(other))

    def __unicode__(self):
        return u"{" + u",".join(u"%s:%s"%(key,value) for key,value in self.iteritems()) + u"}"

    def __repr__(self):
        return unicode(self)

if __name__ == "__main__":
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