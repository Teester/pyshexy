from typing import Callable, Optional, List, Union, Tuple

from pyjsg.jsglib import JSGObject
from pyjsg.jsglib import isinstance_
from rdflib import BNode, URIRef, Graph

from pyshex.shapemap_structure_and_language.p1_notation_and_terminology import RDFGraph, Node
from pyshex.utils.collection_utils import format_collection
from pyshex.utils.n3_mapper import N3Mapper


class ParseNode:
    def __init__(self,
                 function: Callable[["Context", Union[RDFGraph, Node], JSGObject], bool],
                 expr: JSGObject,
                 obj: Union[RDFGraph, Node],
                 cntxt: "Context"):
        self.function = function
        self.expr = expr
        self.graph = obj if isinstance(obj, RDFGraph) else None
        self.node = obj if isinstance_(obj, Node) else None
        self.result = None
        self._fail_reason = None
        self.reason_stack = []
        self.nodes = []
        self.n3m = cntxt.n3_mapper

    def dump_bnodes(self, g: Graph, node: BNode, indent: str, top: bool = True) -> List[str]:
        indent = indent + "  "
        collection = format_collection(g, node, 6)
        if collection is not None:
            return [indent + c for c in collection]
        rval = []
        if top:
            for s, p in g.subject_predicates(node):
                rval.append("{}  {} {} {} .".format(indent, self.n3m.n3(s), self.n3m.n3(p), self.n3m.n3(node)))
        for p, o in sorted(g.predicate_objects(node)):
            rval += ["{}    {} {} {} .".format(indent, self.n3m.n3(node), self.n3m.n3(p), self.n3m.n3(o))]
            if isinstance(o, BNode):
                rval += self.dump_bnodes(g, o, indent, top=False)
        return rval

    def fail_reasons(self, g: Graph, depth: int = 0) -> List[str]:
        def follow_reasons(d: int) -> List[str]:
            fr = []
            if self._fail_reason:
                fr.append(d * "  " + "  {}".format(self._fail_reason))
                d += 1
            for n in self.nodes:
                fr += n.fail_reasons(g, d)
            return fr

        rval = []
        for i in range(0, len(self.reason_stack)):
            node, shape_name = self.reason_stack[i]
            if not shape_name:
                shape_name = '(unnamed shape)'
            indent = (i+depth)*"  "
            rval.append("{}  Testing {} against shape {}".format(indent, self.n3m.n3(node), shape_name))
            if isinstance(node, BNode):
                rval += ["{}  {} context:".format(indent, self.n3m.n3(node))]
                rval += self.dump_bnodes(g, node, indent)
                rval[-1] = rval[-1] + '\n'
        rval += follow_reasons(depth + len(self.reason_stack))
        return rval

    def set_result(self, rval: bool) -> None:
        """ Set the result of the evaluation. If the result is true, prune all of the children that didn't cut it

        :param rval: Result of evaluation
        """
        self.result = rval
        if self.result:
            self.nodes = [pn for pn in self.nodes if pn.result]
