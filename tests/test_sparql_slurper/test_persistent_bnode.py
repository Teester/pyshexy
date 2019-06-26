import unittest

from rdflib import Namespace, BNode

from sparql_slurper import SlurpyGraph, URIRef, Literal

NEXTPROT = Namespace("http://nextprot.org/rdf#")


class PersistentBnodeTestCase(unittest.TestCase):
    def test_persistent_bnode(self):
        """ Test the persistent_bnode argument """
        g = SlurpyGraph("http://sparql-playground.nextprot.org/sparql")
        with self.assertRaises(ValueError):
            _ = list(g.objects(NEXTPROT['NATUR-NX_PEPT00119967-NX_Q9Y5X1-1'], NEXTPROT.evidence))
        g.persistent_bnodes = True
        evidence = g.value(NEXTPROT['NATUR-NX_PEPT00119967-NX_Q9Y5X1-1'], NEXTPROT.evidence)
        self.assertTrue(isinstance(evidence, BNode))
        peptide_name = g.value(evidence, NEXTPROT.peptideName)
        if peptide_name != "NX_PEPT00119967":
            print("Warning: %s does not support persistent BNodes!" % (g.sparql.endpoint))


if __name__ == '__main__':
    unittest.main()
