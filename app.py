import requests
from flask import Flask, request, json
from flask_cors import CORS, cross_origin
from sparql_slurper import SlurpyGraph
from pyshex.shex_evaluator import ShExEvaluator
from pyshex.utils.sparql_query import SPARQLQuery

app = Flask(__name__)
CORS(app)

@app.route("/api")
def data():
    entitySchema = request.args.get("entityschema", type=str)
    entity = request.args.get("entity", type=str)
    sparql = request.args.get("sparql", type=str)
    shexc = request.args.get("shexc", type=str)
    endpoint = request.args.get("endpoint", type=str)
    result = checkShex(shexc, entitySchema, entity, sparql, endpoint)
    payload = {}
    payload['results'] = result
    payload['length'] = len(result)
    response = app.response_class(response=json.dumps(payload), status=200, mimetype="application/json")
    return response

def checkShex(shexc, entitySchema, entity, query, endpoint):
    result = []
    if endpoint is= None:
        endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
        
    if query is None:
        query = "SELECT ?item WHERE { BIND(wd:%s as ?item) } LIMIT 1" % (entity)

    if entitySchema:
        shex = "https://www.wikidata.org/wiki/Special:EntitySchemaText/%s" % (entitySchema)
        shexString = processShex(shex)
    else:
        shexString = shexc

    results = ShExEvaluator(SlurpyGraph(endpoint),
                        shexString,
                        SPARQLQuery(endpoint, query).focus_nodes()).evaluate()
    for r in results:
        thisResult = {}
        thisResult['result'] = r.result
        thisResult['reason'] = r.reason if r.reason else ""
        thisResult['focus'] = r.focus if r.focus else ""
        thisResult['start'] = r.start if r.start else ""
        result.append(thisResult)
    return result
 
def processShex(shex):
    r = requests.get(shex)
    shexString = r.text
    
    # Replace import statements with the contents of those schemas since PyShEx doesn't do imports
    for line in shexString.splitlines():
        if line.startswith("IMPORT"):
            importString = line[line.find("<")+1:line.find(">")]
            s = requests.get(importString)
            shexString = shexString.replace(line, s.text)
    return shexString

if __name__ == '__main__':
    app.run()
   
