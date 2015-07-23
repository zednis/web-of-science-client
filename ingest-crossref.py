__author__ = 'szednik'

import csv
from CrossRefClient import CrossRefClient, Publication
from rdflib import Graph, URIRef, Literal, RDF, RDFS, Namespace
from rdflib.resource import Resource
import pprint


def load_csv(file, delimiter=',', quotechar='"'):
    data = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for (uri, title, doi) in reader:
            data.append((uri, title, doi))
    return data


DCO = Namespace("http://info.deepcarbon.net/schema#")
VIVO = Namespace("http://vivoweb.org/ontology/core#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
BIBO = Namespace("http://purl.org/ontology/bibo/")


def main():
    data = load_csv("dco-dois.csv")
    data.pop(0)

    #g = Graph()

    crossref = CrossRefClient()

    for (uri, title, doi) in data:
        publication = crossref.get_publication(doi)
        print((publication.title, publication.doi, publication.issn, publication.subject, publication.reference_count))

if __name__ == "__main__":
    main()
