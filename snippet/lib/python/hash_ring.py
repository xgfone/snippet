# -*- coding: utf-8 -*-
"""
    hash_ring
    ~~~~~~~~~~~~~~
    Implements consistent hashing that can be used when
    the number of server nodes can increase or decrease (like in memcached).

    Consistent hashing is a scheme that provides a hash table functionality
    in a way that the adding or removing of one slot
    does not significantly change the mapping of keys to slots.

    More information about consistent hashing can be read in these articles:

        "Web Caching with Consistent Hashing":
            http://www8.org/w8-papers/2a-webserver/caching/paper2.html

        "Consistent hashing and random trees:
        Distributed caching protocols for relieving hot spots on the World Wide Web (1997)":
            http://citeseerx.ist.psu.edu/legacymapper?did=38148


    Example of usage::

        memcache_servers = ['192.168.0.246:11212',
                            '192.168.0.247:11212',
                            '192.168.0.249:11212']

        ring = HashRing(memcache_servers)
        server = ring.get_node('my_key')

    :copyright: 2008 by Amir Salihefendic.
    :license: BSD
"""
import sys
from bisect import bisect

if sys.version_info >= (2, 5):
    import hashlib
    md5_constructor = hashlib.md5
else:
    import md5
    md5_constructor = md5.new

if sys.version_info[0] >= 3:
    def get_bytes(obj):
        if isinstance(obj, bytes):
            return obj
        elif isinstance(obj, str):
            return bytes(obj, "utf-8")
        else:
            return bytes(str(obj), "utf-8")
    PY3 = True
else:
    def get_bytes(obj):
        if isinstance(obj, str):
            return obj
        else:
            return str(obj)
    PY3 = False


class HashRing(object):
    def __init__(self, nodes=None, weights=None, default_weight=3, hash=None):
        """Initilize a hash ring object.

        @nodes(list): objects that have a proper __str__ representation.
        @weights(dict): the weights of the @nodes. The default weight is that all nodes are equal.
        @default_weight(int): the default weight if the weight of the node isn't set.
        @hash(func): the user-defined hash function.
        """
        weights = weights if weights else {}
        nodes = nodes if nodes else []
        self.default_weight = default_weight
        self.hash = hash if hash else self.gen_key
        self.ring = dict()
        self._sorted_keys = []
        self.nodes = []
        self.weights = {}
        self.add_nodes(nodes, weights)

    def add_node(self, node, weight=None, sort=True):
        """Add a node into this hash ring.

        @node(object, str): if it's an object, it must have a proper __str__ representation.
        @weight(int): the weight of @node.
        @sort(bool): sort the keys again if it's True. You shouldn't set it.
        """
        weight = weight if weight else self.default_weight
        for j in range(0, weight):
            key = self.hash('%s-%s' % (node, j))
            self.ring[key] = node
            self._sorted_keys.append(key)

        self.nodes.append(node)
        self.weights[node] = weight
        if sort:
            self._sorted_keys.sort()

    def add_nodes(self, nodes, weights=None):
        """Add some nodes into this hash ring.

        @nodes(tuple, list): objects that have a proper __str__ representation.
        @weights(dict): the weights of the @nodes. The default weight is that all nodes are equal.
        """
        weights = weights if weights else {}
        for node in nodes:
            weight = weights.get(node, self.default_weight)
            self.add_node(node, weight, False)
        self._sorted_keys.sort()

    def get_node(self, key):
        """Given a string key a corresponding node in the hash ring is returned.
        If key isn't a string, it must have a proper __str__ representation.

        If the hash ring is empty, `None` is returned.
        """
        pos = self.get_node_pos(key)
        if pos is None:
            return None
        return self.ring[self._sorted_keys[pos]]

    def get_node_pos(self, key):
        """Given a string key a corresponding node in the hash ring is returned
        along with it's position in the ring. If @key isn't a string, it must
        have a proper __str__ representation.

        If the hash ring is empty, `None` is returned.
        """
        if not self.ring:
            return None

        string_key = key if isinstance(key, str) else str(key)
        key = self.hash(string_key)
        pos = bisect(self._sorted_keys, key)

        if pos == len(self._sorted_keys):
            return 0
        else:
            return pos

    def iterate_nodes(self, string_key, distinct=True):
        """Given a string key it returns the nodes as a generator that can hold the key.

        The generator iterates one time through the ring
        starting at the correct position.

        if `distinct` is set, then the nodes returned will be unique,
        i.e. no virtual copies will be returned.
        """
        if not self.ring:
            yield None, None

        returned_values = set()

        def distinct_filter(value):
            if not distinct:
                return value
            if str(value) not in returned_values:
                returned_values.add(str(value))
                return value

        pos = self.get_node_pos(string_key)
        for key in self._sorted_keys[pos:]:
            val = distinct_filter(self.ring[key])
            if val:
                yield val

        for i, key in enumerate(self._sorted_keys):
            if i < pos:
                val = distinct_filter(self.ring[key])
                if val:
                    yield val

    def gen_key(self, key):
        """Given a string key it returns a int value, this int value represents
        a place on the hash ring. If @key isn't a string, it must have a proper
        __str__ representation.

        md5 is currently used because it mixes well.
        """
        key = get_bytes(key)
        b_key = self._hash_digest(key)
        return self._hash_val(b_key, lambda x: x*4)

    @staticmethod
    def _hash_val(b_key, entry_fn):
        return ((b_key[entry_fn(3)] << 24)
                | (b_key[entry_fn(2)] << 16)
                | (b_key[entry_fn(1)] << 8)
                | b_key[entry_fn(0)])

    @staticmethod
    def _hash_digest(key):
        m = md5_constructor()
        m.update(key)
        if PY3:
            return [x for x in m.digest()]
        else:
            return map(ord, m.digest())
