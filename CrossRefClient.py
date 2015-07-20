__author__ = 'szednik'

import requests


class CrossRefClient(object):
    crossref_api_url = "http://api.crossref.org/works/"

    def __init__(self):
        super().__init__()

    def resolve_doi(self, doi):
        r = requests.get(self.crossref_api_url + doi)
        return r.json() \
            if r is not None \
               and r.status_code == 200 \
            else None

    def get_keywords(self, doi):
        data = self.resolve_doi(doi)
        return data["message"]["keywords"] \
            if data is not None \
               and "message" in data \
               and "keywords" in data["message"] \
            else []
