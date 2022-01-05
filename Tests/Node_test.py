import unittest
from graph.Node import Node


class NodeTest(unittest.TestCase):
    def test_get_id(self):
        n = Node(0, (30.9, 31.8, 0))
        self.assertEqual(n.get__id(), 0)

        o = Node(1, (33, 44, 0))
        self.assertEqual(o.get__id(), 1)

        d = Node(2, (4, 6.3, 0))
        self.assertEqual(d.get__id(), 2)

        e = Node(3, (12.0, 5, 0))
        self.assertEqual(e.get__id(), 3)

    def test_get_pos(self):
        n = Node(0, (30.9, 31.8, 0))
        self.assertEqual(n.get__pos(), (30.9, 31.8, 0))

        o = Node(1, (33, 44, 0))
        self.assertEqual(o.get__pos(), (33, 44, 0))

        d = Node(2, (4, 6.3, 0))
        self.assertEqual(d.get__pos(), (4, 6.3, 0))

        e = Node(3, (12.0, 5, 0))
        self.assertEqual(e.get__pos(), (12.0, 5, 0))

    def test_get_tag(self):
        n = Node(0, (30.9, 31.8, 0))
        n.set__tag(2)
        self.assertEqual(n.get__tag(), 2)

    def test_set_tag(self):
        e = Node(3, (12.0, 5, 0))
        e.set__tag(1)
        self.assertEqual(e.get__tag(), 1)

    def test_set_id(self):
        n = Node(0, (30.9, 31.8, 0))
        n.set__id(5)
        self.assertEqual(n.get__id(), 5)

        n.set__id(0)
        self.assertEqual(n.get__id(), 0)

    def test_set_pos(self):
        n = Node(0, (30.9, 31.8, 0))
        n.set__pos((12.0, 5, 0))
        self.assertEqual(n.get__pos(), (12.0, 5, 0))

    def test_str(self):
        n = Node(0, (30.9, 31.8, 0))
        self.assertEqual(n.__str__(), "0: |edges out| 0 |edges in| 0")

    def test_repr(self):
        n = Node(0, (30.9, 31.8, 0))
        self.assertEqual(n.__repr__(), "0: |edges out| 0 |edges in| 0")


if __name__ == '__main__':
    unittest.main()
