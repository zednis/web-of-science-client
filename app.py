__author__ = 'szednik'

import csv, uuid
from WebOfScienceClient import WebOfScienceClient
from CrossRefClient import CrossRefClient
from VIVOClient import VIVOClient
import rdflib.resource
from rdflib import RDF, RDFS

DCO = rdflib.Namespace("http://info.deepcarbon.net/schema#")
VIVO = rdflib.Namespace("http://vivoweb.org/ontology/core#")
SKOS = rdflib.Namespace("http://www.w3.org/2004/02/skos/core#")

concepts = {}
publication2concept = []


def load_csv(file, delimiter=',', quotechar='"'):
    data = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for (uri, title, doi) in reader:
            data.append((uri, title, doi))
    return data


def get_concept(label):
    if label not in concepts:
        uri = "http://info.deepcarbon.net/individual/" + str(uuid.uuid3(uuid.NAMESPACE_URL, label))
        concepts[label] = uri
        return uri
    else:
        return concepts[label]


def create_concept(graph, uri, label):
    concept = rdflib.URIRef(uri)
    graph.add((concept, RDF.type, SKOS.Concept))
    graph.add((concept, RDFS.label, rdflib.Literal(label)))
    return concept


def pub2concept(graph, pub, concept):
    graph.add((rdflib.URIRef(pub), VIVO.hasSubjectArea, rdflib.URIRef(concept)))
    graph.add((rdflib.URIRef(concept), VIVO.subjectAreaFor, rdflib.URIRef(pub)))


def process_keyword(uri, keyword):

    vivo = VIVOClient()
    existing_concepts = vivo.query_keyword(keyword)

    if not existing_concepts:
        concept = get_concept(keyword)
        publication2concept.append((uri, concept))
        return

    vivo_concepts = [c for c in existing_concepts if "http://info.deepcarbon.net" in c]
    if vivo_concepts:
        for vivo_concept in vivo_concepts:
            publication2concept.append((uri, vivo_concept))
    else:
        concept = get_concept(keyword)
        publication2concept.append((uri, concept))


def build_rdf():
    g = rdflib.Graph()
    g.bind("dco", DCO)
    g.bind("vivo", VIVO)
    g.bind("skos", SKOS)

    for label, uri in concepts.items():
        create_concept(g, uri=uri, label=label)

    for pub, concept in publication2concept:
        pub2concept(g, pub=pub, concept=concept)

    return g


def main():
    data = load_csv("dco-dois.csv")
    data.pop(0)

    crossref = CrossRefClient()

    with WebOfScienceClient() as web_of_science:
        for (uri, title, doi) in data:
            keywords = set()
            keywords |= set(web_of_science.get_keywords_by_doi(doi))
            keywords |= set(crossref.get_publication(doi).keywords)
            keywords = set([keyword.lower() for keyword in keywords])
            for keyword in keywords:
                process_keyword(uri=uri, keyword=keyword)

    graph = build_rdf()
    with open("pub.ttl", "w") as out:
        out.write(graph.serialize(format='n3', encoding="UTF-8").decode(encoding="UTF-8"))


if __name__ == "__main__":
    main()
