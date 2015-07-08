__author__ = 'szednik'

import xml.etree.ElementTree as ET
import requests

ns = {
    "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
    "woksearchlite": "http://woksearchlite.v3.wokmws.thomsonreuters.com",
    "auth": "http://auth.cxf.wokmws.thomsonreuters.com"
}

class WebOfScienceClient(object):

    def __init__(self):
        self.session_id = None

    def is_authenticated(self):
        if self.session_id is not None:
            return True
        else:
            return False

    def authenticate(self):
        tree = ET.parse("resources/authenticate.xml")
        payload = ET.tostring(tree.getroot())
        r = requests.post("http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate", data=payload)
        response = ET.fromstring(r.content)
        _return = response.find(".//return")
        if _return is not None:
            self.session_id = _return.text
            return True
        else:
            return False

    def user_query(self, query):
        if not self.is_authenticated():
            return

        tree = ET.parse("resources/userQuery.xml")
        user_query_node = tree.find(".//userQuery")
        user_query_node.text = query
        headers = self._get_session_header()
        payload = ET.tostring(tree.getroot())
        r = requests.post("http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite", headers=headers,
                          data=payload)
        return self._process_response(r.content)

    def close_session(self):
        if not self.is_authenticated():
            return

        tree = ET.parse("resources/closeSession.xml")
        payload = ET.tostring(tree.getroot())
        headers = self._get_session_header()
        r = requests.post("http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate", headers=headers,
                          data=payload)
        response = ET.fromstring(r.content)
        fault = response.find(".//faultstring")
        if fault is not None:
            return fault.text
        else:
            self.session_id = None
            return None

    def _get_session_header(self):
        if self.is_authenticated():
            return {"Cookie": "SID=\"" + str(self.session_id) + "\""}
        else:
            return None

    def __enter__(self):
        self.authenticate()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_session()

    @staticmethod
    def _process_response(content):
        response = ET.fromstring(content)
        _return = response.find(".//return")

        if _return is None:
            return None

        d = {"records": []}
        for record in _return.findall(".//records/"):
            r = {}
            r.update({"uid": record.find("uid").text})
            r.update({"title": record.find("title/value").text})

            authors = []
            for author in record.findall("authors/value"):
                authors.append(author.text)
            if authors:
                r.update({"authors": authors})

            for other in record.findall("other"):
                if other.find("label").text == "Identifier.Doi":
                    r.update({"doi": other.find("value").text})
                if other.find("label").text == "Identifier.Issn":
                    r.update({"issn": other.find("value").text})

            d.get("records").append(r)
        return d
