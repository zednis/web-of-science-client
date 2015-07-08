__author__ = 'szednik'

import xml.etree.ElementTree as ET
import csv
import requests

# send requests from one of 128.213.3.13, 128.213.3.14, 128.113.106.126

ET.register_namespace("soapenv", "http://schemas.xmlsoap.org/soap/envelope/")
ET.register_namespace("woksearchlite", "http://woksearchlite.v3.wokmws.thomsonreuters.com")
ET.register_namespace("auth", "http://auth.cxf.wokmws.thomsonreuters.com")

def user_query(session_id, query):
    tree = ET.parse("resources/userQuery.xml")
    user_query_node = tree.find(".//userQuery")
    user_query_node.text = query
    headers = {"Cookie": "SID=\""+session_id+"\""}
    payload = ET.tostring(tree.getroot())
    r = requests.post("http://search.webofknowledge.com/esti/wokmws/ws/WokSearchLite", headers=headers, data=payload)
    return ET.fromstring(r.content)

def authenticate():
    tree = ET.parse("resources/authenticate.xml")
    payload = ET.tostring(tree.getroot())
    r = requests.post("http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate", data=payload)
    auth_response = ET.fromstring(r.content)
    return auth_response.find(".//return").text

def close_session(session_id):
    tree = ET.parse("resources/closeSession.xml")
    payload = ET.tostring(tree.getroot())
    headers = {"Cookie": "SID=\""+session_id+"\""}
    r = requests.post("http://search.webofknowledge.com/esti/wokmws/ws/WOKMWSAuthenticate", headers=headers, data=payload)
    response = ET.fromstring(r.content)
    fault = response.find(".//faultstring")
    if fault is not None:
        return fault.text
    else:
        return None

def load_csv(file, delimiter=',', quotechar='"'):
    data = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for (uri, title, doi) in reader:
            data.append((uri, title, doi))
    return data

def main():
    data = load_csv("resources/dco-dois.csv")
    data.pop(0)
    session_id = authenticate()
    query = "DO="+data[5][2]
    record = user_query(session_id, query)
    ET.dump(record)
    close_session(session_id)

if __name__ == "__main__":
    main()
