import unittest

from rdflib import Namespace, XSD
from pyshex import ShExEvaluator

EX = Namespace("http://example.org/")

shex = """PREFIX : <%s> 
PREFIX xsd: <%s>

start = @<A>

<A> {:p1 xsd:string }
""" % (EX, XSD)

data = """PREFIX : <%s>

:d :p1 "final" .
""" % EX


class ShexjsIssue17TestCase(unittest.TestCase):
    # Test of https://github.com/shexSpec/shex.js/issues/17

    def test_infinite_loop(self):
        e = ShExEvaluator(rdf=data, schema=shex, focus=EX.d)
        rslt = e.evaluate(debug=False)
        self.assertTrue(rslt[0].result)


if __name__ == '__main__':
    unittest.main()
