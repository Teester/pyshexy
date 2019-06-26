import unittest
import json
import jsonasobj
from dict_compare import compare_dicts

from jsonasobj.jsonobj import as_json, as_dict

test_data = {
  "@context": {
    "name": "http://xmlns.com/foaf/0.1/name",
    "knows": "http://xmlns.com/foaf/0.1/knows",
    "menu": {
      "@id": "name:foo",
      "@type": "@id"
    }
  },
  "@id": "http://me.markus-lanthaler.com/",
  "name": "Markus Lanthaler",
  "knows": [
    {
      "name": "Dave Longley",
      "menu": "something",
      "modelDate" : "01/01/2015"
    }
  ]
}
test_json = str(test_data).replace("'", '"')


class ExampleTestCase(unittest.TestCase):
    def test_example(self):
        pyobj = jsonasobj.loads(str(test_json))
        self.assertEqual('Markus Lanthaler', pyobj.name)
        self.assertEqual(pyobj.name, pyobj['name'])
        self.assertEqual('Dave Longley', pyobj.knows[0].name)
        self.assertEqual('http://xmlns.com/foaf/0.1/name', pyobj['@context'].name)
        self.assertEqual(json.loads(test_json), json.loads(pyobj._as_json))
        self.assertEqual(json.loads(pyobj._as_json), json.loads(as_json(pyobj)))
        self.assertTrue(compare_dicts(test_data, pyobj._as_dict))
        self.assertTrue(compare_dicts(test_data, as_dict(pyobj)))


if __name__ == '__main__':
    unittest.main()
