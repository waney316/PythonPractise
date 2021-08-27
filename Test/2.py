import json
import pandas as pd


def format_data(data):
    if isinstance(data, dict):
        pd_keys = data.get("rows")[0].keys()
        pd_data = []
        for item in data.get("rows"):
            pd_data.append(item.values())
        return pd_keys, pd_data

if __name__ == '__main__':
    with open("1.json", "r", encoding="utf-8") as f:
        read_data = json.load(f)

    data = read_data.get("data")
    columns, data = format_data(data)
    df = pd.DataFrame(data, columns=columns)
    print(df)




