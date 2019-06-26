import unittest

from rdflib import Graph, Namespace

from pyshex import ShExEvaluator


EX = Namespace("http://a.example/")


class IllFoundedTestCase(unittest.TestCase):

    def test_false_positive_minimum(self):
        shex = """<http://a.example/S> {<http://a.example/p> @<http://a.example/S>}"""
        g = Graph()
        g.add((EX.x, EX.p, EX.x))
        e = ShExEvaluator(rdf=g, schema=shex, focus=EX.x, start=EX.S, debug=False)
        self.assertTrue(e.evaluate()[0].result)

    def test_inconsistent(self):
        shex = """<http://a.example/S> {<http://a.example/p> not @<http://a.example/S>}"""
        g = Graph()
        g.add((EX.x, EX.p, EX.x))
        e = ShExEvaluator(rdf=g, schema=shex, focus=EX.x, start=EX.S, debug=False)
        rslt = e.evaluate()
        self.assertFalse(rslt[0].result)
        self.assertEqual("""Testing <http://a.example/x> against shape http://a.example/S
    Testing <http://a.example/x> against shape http://a.example/S
      http://a.example/S: Inconsistent recursive shape reference""", rslt[0].reason.strip())


if __name__ == '__main__':
    unittest.main()
