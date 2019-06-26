import unittest
from rdflib import Namespace

from rdflib import Literal, RDF

from CFGraph import CFGraph

EX = Namespace("http://example.org/")


class Issue1TestCase(unittest.TestCase):
    def test_subjects(self):
        g = CFGraph()
        g.add((EX.foo, RDF.type, Literal("samsonite")))
        g.add((EX.foo, EX.carries, EX.dogs))
        self.assertEqual(2, len(list(g.subjects())))


if __name__ == '__main__':
    unittest.main()
