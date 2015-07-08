__author__ = 'szednik'

import xml.etree.ElementTree as ET
import requests

ET.register_namespace("soapenv", "http://schemas.xmlsoap.org/soap/envelope/")
ET.register_namespace("woksearchlite", "http://woksearchlite.v3.wokmws.thomsonreuters.com")
ET.register_namespace("auth", "http://auth.cxf.wokmws.thomsonreuters.com")


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
        auth_response = ET.fromstring(r.content)
        _return = auth_response.find(".//return")
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
        return ET.fromstring(r.content)

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
            return None

    def _get_session_header(self):
        return {"Cookie": "SID=\"" + str(self.session_id) + "\""}
