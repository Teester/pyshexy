import unittest

from rdflib import Graph, Namespace, XSD, Literal

from pyshex import ShExEvaluator


FHIR = Namespace("http://hl7.org/fhir/")
EX = Namespace("http://example.org/")

shex = """PREFIX : <%s> 
PREFIX xsd: <%s>

start = @<A>

<A> {
  :predd xsd:string ;
  ( :test @<A>* | :test @<E>* );
  :test2 @<C> ;
}
<E> { :prede xsd:string ; }
<A> { :subject @<C> ; :preda xsd:string }
<C> { :subject @<A> ; :predc xsd:string }
""" % (FHIR, XSD)

data = """PREFIX : <%s>
PREFIX xsd: <%s>

:d :predd "final" ; :test <a> ; :test2 <c> .
<a> :subject   <c> ; :prede    "final" .
<c> :subject   <a> ; :predc    "final" .
""" % (FHIR, XSD)


class ShexjsIssue14TestCase(unittest.TestCase):
    # Test of https://github.com/shexSpec/shex.js/issues/16

    def test_infinite_loop(self):
        e = ShExEvaluator(rdf=data, schema=shex, focus=FHIR.d, debug=False)
        rslt = e.evaluate()
        # self.assertEqual("http://a.example/S: Inconsistent recursive shape reference", rslt[0].reason)
        self.assertFalse(rslt[0].result)
        print(rslt[0].reason)


if __name__ == '__main__':
    unittest.main()
