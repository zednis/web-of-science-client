__author__ = 'szednik'

import csv
import json
import rdflib
import uuid
import rdflib.resource
from rdflib import RDF, RDFS
# from SPARQLWrapper import SPARQLWrapper, JSON

DCO = rdflib.Namespace("http://info.deepcarbon.net/schema#")
VIVO = rdflib.Namespace("http://vivoweb.org/ontology/core#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")

# uri_base = "http://info.deepcarbon.net/individual/"
# vivo_endpoint = "http://deepcarbon.tw.rpi.edu:3030/VIVO/query"

concepts = {}
# sparql = SPARQLWrapper(vivo_endpoint)
#
# with open("concept-query.rq") as query_file:
#     query_template = query_file.read().replace('\n', " ")
#
# def query_keyword(keyword):
#     _query = query_template.replace("{keyword}", keyword.lower())
#     sparql.setQuery(_query)
#     sparql.setReturnFormat(JSON)
#     results = sparql.query().convert()
#
#     r = []
#     for result in results["results"]["bindings"]:
#         r.append(result["concept"]["value"])
#     return r

def load_csv(file, delimiter=',', quotechar='"'):
    data = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for (uri, title, doi) in reader:
            data.append((uri, title, doi))
    return data

def get_concept(graph, label):
    if label not in concepts:
        uri = uri_base + str(uuid.uuid4())
        concept = rdflib.URIRef(uri)
        graph.add((concept, RDF.type, SKOS.Concept))
        graph.add((concept, RDFS.label, rdflib.Literal(label)))
        concepts[label] = concept
        return concept
    else:
        return concepts[label]

def main():

    g = rdflib.Graph()
    g.bind("dco", DCO)
    g.bind("vivo", VIVO)
    g.bind("skos", SKOS)

    data = load_csv("dco-dois.csv")
    data.pop(0)

    with open("publications.json") as f:
        publications = json.load(f)

    for pub in publications:

        if "Identifier.Doi" in pub:
            doi = pub["Identifier.Doi"]
            f = [(uri, title, d) for uri, title, d in data if d.lower() == doi.lower()]
        else:
            title = pub["title"]
            f = [(uri, t, doi) for uri, t, doi in data if t.lower() == title.lower()]

        if f:
            n = rdflib.URIRef(f[0][0])

            if "keywords" in pub:
                for keyword in pub["keywords"]:

                    k = query_keyword(keyword)

                    if k:
                        k2 = [c for c in k if "http://info.deepcarbon.net" in c]
                        if k2:
                            for c in k2:
                                g.add((n, VIVO.hasSubjectArea, rdflib.URIRef(c)))
                                g.add((rdflib.URIRef(c), VIVO.subjectAreaFor, n))
                        else:
                            concept = get_concept(g, keyword)
                            g.add((n, VIVO.hasSubjectArea, concept))
                            g.add((concept, VIVO.subjectAreaFor, n))
                    else:
                        concept = get_concept(g, keyword)
                        g.add((n, VIVO.hasSubjectArea, concept))
                        g.add((concept, VIVO.subjectAreaFor, n))

    print(g.serialize(format='n3', encoding="UTF-8").decode(encoding="UTF-8"))

if __name__ == "__main__":
    main()

