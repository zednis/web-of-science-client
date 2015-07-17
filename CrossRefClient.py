__author__ = 'szednik'

import requests

class CrossRefClient(object):

    crossref_api_url = "http://api.crossref.org/works/"

    def __init__(self):
        super().__init__()

    def resolve_doi(self, doi):
        r = requests.get(self.crossref_api_url+doi)
        return r.json()

    def get_keywords(self, doi):
        data = self.resolve_doi(doi)
        keywords = data["message"]["keywords"]
        return keywords

