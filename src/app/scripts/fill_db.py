import pandas as pd
import requests


# Write dialect to db
def write_dialect_to_db(region_name: str, title: str, description: str):
    url = "http://localhost:8002/dialects/named/" + region_name + "/"
    print(region_name)
    payload = '{"title": "' + title + '", "description": "' + description + '"}'
    print(payload)
    payload = payload.encode(encoding='utf-8')
    response = requests.post(url, data=payload)
    print(response.text, "\n\n")


# Executing part
if __name__ == '__main__':
    df = pd.read_excel("dialects.xlsx", header=None, names=["region_name", "title", "description"])

    for i in range(0, len(df)):
        record = df.iloc[i]
        write_dialect_to_db(record["region_name"], record["title"], record["description"])
