import requests
import urllib
from flask import Flask, request, json
from flask_cors import CORS
from sparql_slurper import SlurpyGraph
from pyshex.shex_evaluator import ShExEvaluator
from pyshex.utils.sparql_query import SPARQLQuery

app = Flask(__name__)
CORS(app)


@app.route("/api")
def data():
    entity_schema = request.args.get("entityschema", type=str)
    entity = request.args.get("entity", type=str)
    sparql = request.args.get("sparql", type=str)
    shexc = request.args.get("shexc", type=str)
    endpoint = request.args.get("endpoint", type=str)
    result = check_shex(shexc, entity_schema, entity, sparql, endpoint)
    payload = {'results': result, 'length': len(result)}
    response = app.response_class(response=json.dumps(payload), status=200, mimetype="application/json")
    return response


def check_shex(shexc, entity_schema, entity, query, endpoint):
    result = []
    if endpoint is None:
        endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
        
    if query is None:
        query = "SELECT ?item WHERE { BIND(wd:%s as ?item) } LIMIT 1" % entity

    if entity_schema:
        shex = "https://www.wikidata.org/wiki/Special:EntitySchemaText/%s" % entity_schema
        shex_string = process_shex(shex)
    else:
        shex_string = urllib.parse.unquote(shexc)

    results = ShExEvaluator(SlurpyGraph(endpoint),
                            shex_string,
                            SPARQLQuery(endpoint, query).focus_nodes()).evaluate()
    for r in results:
        this_result = {'result': r.result, 'reason': r.reason if r.reason else "", 'focus': r.focus if r.focus else "",
                       'start': r.start if r.start else ""}
        result.append(this_result)
    return result


def process_shex(shex):
    r = requests.get(shex)
    shex_string = r.text
     
    # Replace import statements with the contents of those schemas since PyShEx doesn't do imports
    for line in shex_string.splitlines():
        if line.startswith("IMPORT"):
            import_string = line[line.find("<")+1:line.find(">")]
            s = requests.get(import_string)
            shex_string = shex_string.replace(line, s.text)

    # Replace some definitions in the shex in order to mitigate a bug in PyShEx
    shex_string = shex_string.replace("http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                                      "http://www.w3.org/2001/XMLSchema#")
    shex_string = shex_string.replace("rdf:langString", "rdf:string")
    return shex_string


if __name__ == '__main__':
    app.run(debug=True)
