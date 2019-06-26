import os
import unittest
from typing import Optional, List, NamedTuple, Union

import jsonasobj
import requests
from SPARQLWrapper import SPARQLWrapper, JSON
from jsonasobj import loads
from rdflib import URIRef, Literal
from rdflib.namespace import SKOS
from sparql_slurper import SlurpyGraph

from pyshex import PrefixLibrary, ShExEvaluator
from pyshex.shex_evaluator import EvaluationResult


class DataFrame(NamedTuple):
    item: str


class Triple(NamedTuple):
    s: Optional[URIRef]
    p: Optional[URIRef]
    o: Optional[Union[Literal, URIRef]]


class WikiDataTestCase(unittest.TestCase):
    save_test_data = False

    @staticmethod
    def get_sparql_dataframe(service, query):
        """
        Helper function to convert SPARQL results into a Pandas data frame.
        """
        sparql = SPARQLWrapper(service)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        result = sparql.query()

        processed_results = jsonasobj.load(result.response)
        return [row.item.value for row in processed_results.results.bindings]

    def fetch_uri(self, uri: str) -> str:
        req = requests.get(uri)
        self.assertTrue(req.ok, f"Unable to read {uri}")
        return req.text

    def run_test(self, manifest_uri: str, num_entries: Optional[int]=None, verbose: bool=True, debug: bool=False,
                 stop_on_fail: bool=False, debug_slurps: bool=False, save_graph_dir: Optional[str]=None) \
            -> List[EvaluationResult]:
        """ Run the test identified by manifest_uri

        :param manifest_uri: uri of manifest
        :param num_entries: number of manifest elements to test
        :param verbose: True means talk about it
        :param debug: debug setting for shex evaluator
        :param stop_on_fail: True means run until failure
        :param debug_slurps: True means emit SPARQL_slurper statistics
        :param save_graph_dir: If present, save the final graph in this directory
        :return:
        """
        manifest = loads(self.fetch_uri(manifest_uri))
        rval: List[EvaluationResult] = []
        for case in manifest:
            if verbose:
                print(case._as_json_dumps())
            sparql_endpoint = case.data.replace("Endpoint: ", "")
            shex = self.fetch_uri(case.schemaURL)
            evaluator = ShExEvaluator(schema=shex, debug=debug)
            prefixes = PrefixLibrary(shex, SKOS=SKOS)
            sparql_query = case.queryMap.replace("SPARQL '''", "").replace("'''@START", "")
            dfs: List[str] = self.get_sparql_dataframe(sparql_endpoint, sparql_query)
            dfs_slice = dfs[:num_entries] if num_entries is not None else dfs
            for df in dfs_slice:
                slurper = SlurpyGraph(sparql_endpoint)
                # slurper.debug_slurps = debug_slurps
                prefixes.add_bindings(slurper)
                print(f"Evaluating: {df}")
                results = evaluator.evaluate(rdf=slurper, focus=df, debug=debug, debug_slurps=debug_slurps, over_slurp=False)
                rval += results
                if save_graph_dir:
                    element_name = df.rsplit('/', 1)[1]
                    file_name = os.path.join(save_graph_dir, element_name + '.ttl')
                    print(f"Writing: {file_name}")
                    slurper.serialize(file_name, format="turtle")
                if stop_on_fail and not all(r.result for r in results):
                    break
        return rval
