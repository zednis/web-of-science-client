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

    records = []
    with WebOfScienceClient() as client:

        for (uri, title, doi) in data:
            query = "DO="+doi
            record = client.user_query(query)
            if record is not None:
                records.append(record)

        print(json.dumps(records))

if __name__ == "__main__":
    main()