import unittest

from rdflib import Namespace, RDF

from pyshex import ShExEvaluator

BASE = Namespace("https://w3id.org/biolink/vocab/")

rdf = """
@prefix : <{}> .
@prefix rdf: <{}> .
:s rdf:type :X .
""".format(BASE, RDF)

shex = """
BASE <{}>
<BiologicalProcess> ( 
    {{
        ( $<BiologicalProcess_tes> a [ <BiologicalProcessOrActivity> ] ?;
          a [ <BiologicalProcess> ]
        )
    }} OR @<X>
)
<X> {{&<BiologicalProcess_tes>; a [<X>]}}
""".format(BASE)

shex2 = """
BASE <{}>
<BiologicalProcess> ( 
    {{
        ( $<BiologicalProcess_tes> a [ <BiologicalProcessOrActivity> ] ?;
          a [ <BiologicalProcess> ]
        )
    }} OR @<X>
)
<X> {{&<missing>}}
""".format(BASE)


class Issue51TestCase(unittest.TestCase):
    def test_inner_te(self):
        """ Test recognition of an inner triple expression """

        e = ShExEvaluator(rdf=rdf, schema=shex, focus=BASE.s, start=BASE.X).evaluate()
        self.assertTrue(e[0].result)

    def test_te_message(self):
        """ Test the error message (and eventually the startup test) """
        e = ShExEvaluator(rdf=rdf, schema=shex2, focus=BASE.s, start=BASE.X).evaluate()
        self.assertFalse(e[0].result)
        self.assertEqual('  Testing :s against shape https://w3id.org/biolink/vocab/X\n'
                         '    https://w3id.org/biolink/vocab/missing: Reference not found', e[0].reason)


if __name__ == '__main__':
    unittest.main()
