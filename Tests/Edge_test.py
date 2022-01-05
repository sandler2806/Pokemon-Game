import unittest
from graph.Edge import Edge


class EdgeTest(unittest.TestCase):
    def test_get_src(self):
        e = Edge(0, 5, 1)
        self.assertEqual(e.get_src(), 0)

        d = Edge(1, 2.5, 0)
        self.assertEqual(d.get_src(), 1)

        g = Edge(1, 30, 2)
        self.assertEqual(g.get_src(), 1)

        a = Edge(3, 2, 2)
        self.assertEqual(a.get_src(), 3)

    def test_get_dest(self):
        e = Edge(0, 5, 1)
        self.assertEqual(e.get_dest(), 1)

        d = Edge(1, 2.5, 0)
        self.assertEqual(d.get_dest(), 0)

        g = Edge(1, 30, 2)
        self.assertEqual(g.get_dest(), 2)

        a = Edge(3, 2, 2)
        self.assertEqual(a.get_dest(), 2)

    def test_get_w(self):
        e = Edge(0, 5, 1)
        self.assertEqual(e.get_w(), 5)

        d = Edge(1, 2.5, 0)
        self.assertEqual(d.get_w(), 2.5)

        g = Edge(1, 30, 2)
        self.assertEqual(g.get_w(), 30)

        a = Edge(3, 2, 2)
        self.assertEqual(a.get_w(), 2)

    def test_str(self):
        e = Edge(0, 5, 1)
        self.assertEqual(e.__str__(), "Edge(0,5,1)")

    def test_repr(self):
        e = Edge(0, 5, 1)
        self.assertEqual(e.__repr__(), "Edge(0,5,1)")


if __name__ == '__main__':
    unittest.main()
