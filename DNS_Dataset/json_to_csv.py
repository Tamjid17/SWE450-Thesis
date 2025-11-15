import json
import pandas as pd

with open("dnscat2_session.json") as f:
    data = json.load(f)

rows = []
for packet in data:
    flat = {}

    # Flatten JSON
    for layer in packet["_source"]["layers"]:
        for key, value in packet["_source"]["layers"][layer].items():
            flat[f"{layer}.{key}"] = value

    rows.append(flat)

df = pd.DataFrame(rows)
df.to_csv("dnscat2_full.csv", index=False)
