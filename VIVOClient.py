__author__ = 'szednik'

from SPARQLWrapper import SPARQLWrapper, JSON


class VIVOClient(object):

    uri_base = "http://info.deepcarbon.net/individual/"
    vivo_endpoint = "http://deepcarbon.tw.rpi.edu:3030/VIVO/query"

    def __init__(self):
        super().__init__()
        self.sparql = SPARQLWrapper(self.vivo_endpoint)
        with open("concept-query.rq") as _file:
            self.template = _file.read().replace('\n', " ")

    def query_keyword(self, keyword):
        _query = self.template.replace("{keyword}", keyword.lower())
        self.sparql.setQuery(_query)
        self.sparql.setReturnFormat(JSON)
        results = self.sparql.query().convert()

        r = []
        for result in results["results"]["bindings"]:
            r.append(result["concept"]["value"])
        return r
