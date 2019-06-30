import unittest
from typing import List, Tuple

from rdflib import URIRef, XSD
# <http://a.example/s1>  <http://a.example/p1> "a","b","c","d","e","f" .
from rdflib.term import Literal

from CFGraph import CFGraph

from pprint import pprint
ppl = lambda t: pprint([(str(s), str(p), o.value if isinstance(o, Literal) else str(o))
                        for s, p, o in sorted(list(t))], width=160)
ppt = lambda t: pprint([(str(e[0]), str(e[1])) for e in t], width=160)
pps = lambda objs: pprint(set([str(o) for o in objs]), width=160)

s1 = URIRef("http://a.example/s1")
s2 = URIRef("http://a.example/s2")
s3 = URIRef("http://a.example/s3")
s4 = URIRef("http://a.example/s4")
s5 = URIRef("http://a.example/s5")
s6 = URIRef("http://a.example/s6")

p1 = URIRef("http://a.example/p1")
p2 = URIRef("http://a.example/p2")
p3 = URIRef("http://a.example/p3")
p4 = URIRef("http://a.example/p4")
p5 = URIRef("http://a.example/p5")
p6 = URIRef("http://a.example/p6")
p7 = URIRef("http://a.example/p7")

o1 = URIRef("http://a.example/o1")
o2 = URIRef("http://a.example/o2")
o3 = URIRef("http://a.example/o3")
o4 = URIRef("http://a.example/o4")
o5 = URIRef("http://a.example/o5")
o6 = URIRef("http://a.example/o6")
o7 = URIRef("http://a.example/o7")

rdf = """
<{}> <{}> ("a" "b" "c" "d" "e" <{}> "b").
<{}> <{}> "a", "b", "c", "d", "e", <{}>, "b".
<{}> <{}> ().
<{}> <{}> (17.0).
<{}> <{}> (1 2), <{}>.
<{}> <{}> (1 2 <{}>), <{}>; <{}> <{}>, (<{}>).
""".format(s1, p1, o1, s2, p2, o2, s3, p3, s4, p4, s5, p5, o5, s6, p6, o6, o6, p7, o6, o7)



class ListTestCase(unittest.TestCase):
    @staticmethod
    def gen_list(s: URIRef, p: URIRef, objs: List[str]) -> List[Tuple[URIRef, URIRef, Literal]]:
        return [(s, p,  e if isinstance(e, URIRef) else Literal(e)) for e in objs]

    @staticmethod
    def gen_lit_list(objs: List[str]) -> List[Literal]:
        return [o if isinstance(o, URIRef) else Literal(o) for o in objs]

    @staticmethod
    def build_graph() -> CFGraph:
        g = CFGraph()
        g.parse(data=rdf, format='turtle')
        return g

    """ Flatten an RDF collection """
    def test_flatten(self):
        g = self.build_graph()
        self.assertEqual(self.gen_list(s1, p1, ["a", "b", "c", "d", "e", URIRef(o1), "b"]), list(g.triples((s1, p1, None))))
        self.assertEqual(self.gen_lit_list(["a", "b", "c", "d", "e", URIRef(o1), "b"]), list(g.objects(s1, p1)))
        self.assertEqual(set(self.gen_lit_list(["a", "b", "c", "d", "e", URIRef(o2), "b"])), set(g.objects(s2, p2)))
        self.assertEqual([], list(g.objects(s3, p3)))
        self.assertEqual([], (list(g.triples((s1, p2, None)))))
        self.assertEqual(set(self.gen_list(s5, p5, [1, 2, o5])), set(g.triples((s5, p5, None))))
        # Note RDFLIB bug below - without the datatype, Literal returns double
        self.assertEqual([Literal(17.0, datatype=XSD.decimal)], list(g.objects(s4, p4)))

    def test_permutations(self):
        g = self.build_graph()
        self.assertEqual([(s6, p6, o6), (s6, p6, o6),
                          (s6, p6, Literal(1)), (s6, p6, Literal(2)),
                          (s6, p7, o6), (s6, p7, o7)],
                         sorted(list(g.triples((s6, None, None )))))
        self.assertEqual([(s6, p6, o6), (s6, p6, o6), (s6, p6, Literal(1)), (s6, p6, Literal(2))],
                         sorted(g.triples((None, p6, None))))
        self.assertEqual([(s6, p7, o6), (s6, p7, o7)], sorted(g.triples((None, p7, None))))
        self.assertEqual([(s6, p6, o6), (s6, p6, o6), (s6, p7, o6)], sorted(g.triples(None, None, o6)))
        self.assertEqual([(s6, p7, o7)], sorted(g.triples(None, None, o7)))
        self.assertEqual([(s6, p6, o6), (s6, p6, o6), (s6, p6, Literal(1)), (s6, p6, Literal(2))],
                         sorted(g.triples(s6, p6, None)))
        self.assertEqual([(s6, p6, o6)], sorted(g.triples(None, p6, o6)))
        self.assertEqual([(s6, p6, o6), (s6, p7, o6)], sorted(g.triples((s6, None, o6))))
        self.assertEqual([(s6, p6, o6)], sorted(g.triples((s6, p6, o6))))
        self.assertEqual([(s1, p1, o1), (s1, p1, Literal('a')), (s1, p1, Literal('b')),
                          (s1, p1, Literal('b')), (s1, p1, Literal('c')), (s1, p1, Literal('d')),
                          (s1, p1, Literal('e')), (s2, p2, o2), (s2, p2, Literal('a')), (s2, p2, Literal('b')),
                          (s2, p2, Literal('c')), (s2, p2, Literal('d')), (s2, p2, Literal('e')),
                          (s4, p4, Literal(17.0, datatype=XSD.decimal)),
                          (s5, p5, o5), (s5, p5,Literal(1)), (s5, p5,Literal(2)), (s6, p6, o6), (s6, p6, o6),
                          (s6, p6,Literal(1)), (s6, p6,Literal(2)), (s6, p7, o6), (s6, p7, o7)],
                         sorted(g.triples(None, None, None)))

    def test_notebook(self):
        rdf = '<{}> <{}> ("a" "b" "c" "d" "e" <{}> "b").'.format(s1, p1, o1)
        g = CFGraph()
        g.parse(data=rdf, format="turtle")
        self.assertEqual([(s1, p1)], sorted(g.subject_predicates(o1)))
        self.assertEqual([s1], sorted(g.subjects(p1, o1)))


if __name__ == '__main__':
    unittest.main()
