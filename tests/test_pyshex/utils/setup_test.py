import re
from typing import Tuple, Optional

from ShExJSG import ShExJ
from pyjsg.jsglib import loads

from rdflib import Graph, RDF, RDFS, XSD
from rdflib.namespace import FOAF

from pyshex.shape_expressions_language.p5_context import Context
from pyshex.utils.rdf_namespace import RDFNamespace

EX = RDFNamespace("http://schema.example/")
INST = RDFNamespace("http://inst.example/#")

rdf_header = """
prefix ex: <%s>
prefix : <%s>
prefix rdf: <%s>
prefix rdfs: <%s>
prefix xsd: <%s>
prefix inst: <%s>
prefix foaf: <%s>
""" % (EX, EX, RDF, RDFS, XSD, INST, FOAF)


def setup_context(shex_str: str, rdf_str: Optional[str]) -> Context:
    schema, g = setup_test(shex_str, rdf_str)
    if g is None:
        g = Graph()
        g.parse(rdf_header)
    return Context(g, schema)


def setup_test(shex_str: Optional[str], rdf_str: Optional[str]) -> Tuple[Optional[ShExJ.Schema], Optional[Graph]]:
    schema = loads(shex_str, ShExJ, strict=False) if shex_str else None
    if rdf_str:
        g = Graph()
        g.parse(data=rdf_str, format="turtle")
    else:
        g = None
    return schema, g


def gen_rdf(rdf_fragment: str) -> str:
    """ Edit rdf_fragment from the spec to be complete. We
    1) Add the rdf header and
    2) convert relative URI's into URI's based in the default space """
    return """%s""" % (rdf_header) + re.sub(r'<([^.:>]+)>', r':\1', rdf_fragment)
