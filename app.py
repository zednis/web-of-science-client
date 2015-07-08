__author__ = 'szednik'

import csv
import xml.etree.ElementTree as ET
from WebOfScienceClient import WebOfScienceClient

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

    client = WebOfScienceClient()
    client.authenticate()
    print("authenticated:", client.is_authenticated())

    query = "DO="+data[5][2]
    record = client.user_query(query)
    ET.dump(record)

    client.close_session()
    print("authenticated:", client.is_authenticated())

if __name__ == "__main__":
    main()