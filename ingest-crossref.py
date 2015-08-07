__author__ = 'szednik'

from CrossRefClient import CrossRefClient, Publication
from rdflib import Graph, URIRef, Literal, RDF, RDFS, XSD, Namespace
from rdflib.resource import Resource
import pprint
from SPARQLWrapper import SPARQLWrapper, JSON


def select_publications():
    sparql = SPARQLWrapper("http://deepcarbon.tw.rpi.edu:3030/VIVO/query")
    with open("selectPublications.rq") as rq:
        query = rq.read().replace('\n', " ")

    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    return [{"uri": result["publication"]["value"], "doi": result["doi"]["value"]}
            for result in results["results"]["bindings"]]


def generate_rdf(data):
    DCO = Namespace("http://info.deepcarbon.net/schema#")
    VIVO = Namespace("http://vivoweb.org/ontology/core#")
    SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
    BIBO = Namespace("http://purl.org/ontology/bibo/")

    g = Graph()
    g.bind("dco", DCO)
    g.bind("bibo", BIBO)
    g.bind("vivo", VIVO)

    for (uri, record) in data:
        try:
            publication = Publication(record)
            pub = Resource(g, URIRef(uri))

            if publication.issue is not None:
                pub.add(BIBO.issue, Literal(publication.issue))

            if publication.issued is not None and publication.issued["year"] is not None:
                pub.add(DCO.yearOfPublicationYear, Literal(publication.issued["year"], datatype=XSD.gYear))

            if publication.volume is not None:
                pub.add(BIBO.volume, Literal(publication.volume))

            if publication.issn is not None:
                pub.add(BIBO.issn, Literal(publication.issn))

            if publication.pages is not None:
                if "-" in publication.pages:
                    pageStart = publication.pages[:publication.pages.find("-")]
                    pageEnd = publication.pages[publication.pages.find("-") + 1:]
                    if pageStart != "n/a":
                        pub.add(BIBO.pageStart, Literal(pageStart))
                    if pageEnd != "n/a":
                        pub.add(BIBO.pageEnd, Literal(pageEnd))
                else:
                    #pub.add(BIBO.pages, Literal(publication.pages))
                    pass

        except ValueError as err:
            #print((uri,str(err)))
            pass

    with open("pub-info.ttl", "w") as out:
        out.write(g.serialize(format="turtle", encoding="UTF-8").decode(encoding="UTF-8"))


def main():
    crossref = CrossRefClient()
    publications = select_publications()
    out = [(pub["uri"], crossref.resolve_doi(pub["doi"])) for pub in publications]
    generate_rdf(out)


if __name__ == "__main__":
    main()
