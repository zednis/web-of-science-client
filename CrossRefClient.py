__author__ = 'szednik'

import requests


class CrossRefClient(object):
    crossref_api_url = "http://api.crossref.org/works/"

    def __init__(self):
        super().__init__()

    def get_publication(self, doi):
        data = self._resolve_doi(doi)
        return Publication(data) if data is not None else None

    def _resolve_doi(self, doi):
        r = requests.get(self.crossref_api_url + doi)
        return r.json()["message"] \
            if r is not None \
               and r.status_code == 200 \
               and "message" in r.json() \
            else None


class Publication(object):
    def __init__(self, data):
        self._data = data

        if data is not None:
            self._keywords = data["keywords"] if "keywords" in data else []
            self._pages = data["pages"] if "pages" in data else None
            self._publisher = data["publisher"] if "publisher" in data else None
            self._volume = data["volume"] if "volume" in data else None
            self._type = data["type"] if "type" in data else None
            self._doi = data["DOI"] if "DOI" in data else None
            self._issn = data["ISSN"][0] if "ISSN" in data and data["ISSN"] else None
            self._subject = data["subject"] if "subject" in data else []
            self._title = data["title"][0] if "title" in data and data["title"] else None
            self._issued = Publication.get_date(data["issued"]["date-parts"][0]) if "issued" in data else None
            self._publication_venue = data["container-title"] if "container-title" in data else None
            self._authors = data["author"] if "author" in data and data["author"] else []
            self._reference_count = data["reference-count"] if "reference-count" in data else None
            self._issue = data["issue"] if "issue" in data else None

    @staticmethod
    def get_date(d):
        size = len(d)
        return {
            "year": d[0] if size > 0 else None,
            "month": d[1] if size > 1 else None,
            "day": d[2] if size > 2 else None
        } if d else None

    @property
    def keywords(self):
        return self._keywords

    @property
    def pages(self):
        return self._pages

    @property
    def publisher(self):
        return self._publisher

    @property
    def volume(self):
        return self._volume

    @property
    def type(self):
        return self._type

    @property
    def doi(self):
        return self._doi

    @property
    def issn(self):
        return self._issn

    @property
    def subject(self):
        return self._subject

    @property
    def title(self):
        return self._title

    @property
    def issued(self):
        return self._issued

    @property
    def authors(self):
        return self._authors

    @property
    def reference_count(self):
        return self._reference_count

    @property
    def publication_venue(self):
        return self._publication_venue

    @property
    def issue(self):
        return self._issue
