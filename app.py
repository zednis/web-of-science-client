__author__ = 'szednik'

import csv
import json
from WebOfScienceClient import WebOfScienceClient

def load_csv(file, delimiter=',', quotechar='"'):
    data = []
    with open(file) as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter, quotechar=quotechar)
        for (uri, title, doi) in reader:
            data.append((uri, title, doi))
    return data

def main():
    data = load_csv("dco-dois.csv")
    data.pop(0)

    with WebOfScienceClient() as client:
        query = "DO="+data[0][2]
        records = client.user_query(query)
        print(json.dumps(records))

if __name__ == "__main__":
    main()