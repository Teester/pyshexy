from flask import Flask
from flask_restful import Api, Resource, reqparse
import urllib.request
from sparql_slurper import SlurpyGraph
from pyshex.shex_evaluator import ShExEvaluator
from pyshex.utils.sparql_query import SPARQLQuery
import json
 
app = Flask(__name__)
api = Api(app)
 
class Query(Resource):
    def get(self, entitySchema, entity):
        result = checkShex(self, entitySchema, entity)
        data = {}
        data['result'] = result
        return data, 200
 
def checkShex(self, shex, entity):
    result = ""
    endpoint = " https://query.wikidata.org/bigdata/namespace/wdq/sparql"
 
    sparql = "SELECT ?item WHERE { BIND(wd:" + entity + " as ?item) } LIMIT 1"
 
    shex = "https://www.wikidata.org/wiki/Special:EntitySchemaText/" + shex
     
    shexString = processShex(self, shex)
     
    results = ShExEvaluator(SlurpyGraph(endpoint),
                        shexString,
                        SPARQLQuery(endpoint, sparql).focus_nodes()).evaluate()
    for r in results:
        print(r)
        if r.result:
            result += "PASS"
        else:
            result += "FAIL"
    return result
 
def processShex(self, shex):
    fp = urllib.request.urlopen(shex)
    mybytes = fp.read()
    shexString = mybytes.decode("utf8")
    fp.close()
     
    # Replace import statements with the contents of those schemas since PyShEx doesn't do imports
    for line in shexString.splitlines():
        if line.startswith("IMPORT"):
            importString = line[line.find("<")+1:line.find(">")]
            pq = urllib.request.urlopen(importString)
            mybytes2 = pq.read()
            importString2 = mybytes2.decode("UTF-8")
            pq.close()
            shexString = shexString.replace(line, importString2)
 
    # Replace some definitions in the shex in order to mitigate a bug in PyShEx
    shexString = shexString.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#", "http://www.w3.org/2001/XMLSchema#")
    shexString = shexString.replace("rdf:langString", "rdf:string")
     
    return shexString
 
api.add_resource(Query, "/api/entityschema=<string:entitySchema>&entity=<string:entity>")
app.run()
