import pandas as pd
import math
import re
from collections import Counter
import ast

#############################
# CONFIGURATION
#############################

FILES = {
    "normal": "normal_dns_full.csv",
    "txt": "txt_dataset_full.csv",
    "null": "null_dataset_full.csv",
    "dnscat2": "dnscat2_full.csv"
}

OUTPUT_FILE = "dns_preprocessed_dataset.csv"

#############################
# ENTROPY FUNCTION
#############################

def shannon_entropy(s):
    if not isinstance(s, str) or len(s) == 0:
        return 0.0

    counts = Counter(s)
    length = len(s)

    entropy = 0.0
    for char in counts:
        p = counts[char] / length
        entropy -= p * math.log2(p)
    return entropy


#############################
# DOMAIN CLEANING
#############################

def clean_qname(qname):
    if not isinstance(qname, str):
        return ""
    qname_lower = qname.lower()
    if "tunnel.devgossips.me" in qname_lower:
        return qname.split(".tunnel.devgossips.me")[0]
    else:
        return qname
        


#############################
# PARSING dns.Queries FIELD
#############################

def extract_dns_fields(query_string):
    """
    Safely parse dns.Queries JSON-like text and extract key fields.
    """

    result = {
        "qname": "",
        "qname_len": 0,
        "label_count": 0,
        "qtype": 0
    }

    if not isinstance(query_string, str):
        return result

    try:
        parsed = ast.literal_eval(query_string)
        if isinstance(parsed, dict):
            for _, entry in parsed.items():
                if isinstance(entry, dict):
                    result["qname"] = entry.get("dns.qry.name", "")
                    result["qname_len"] = int(entry.get("dns.qry.name.len", 0))
                    result["label_count"] = int(entry.get("dns.count.labels", 0))
                    result["qtype"] = int(entry.get("dns.qry.type", 0))
    except Exception:
        pass

    return result


#############################
# LOAD + PROCESS FUNCTION
#############################

def process_file(filepath, label):
    print(f"Processing: {filepath}")

    df = pd.read_csv(filepath, low_memory=False)

    # Extract DNS query fields
    dns_data = df["dns.Queries"].apply(extract_dns_fields)
    dns_df = pd.DataFrame(dns_data.tolist())

    # Domain leak mitigation
    dns_df["qname_clean"] = dns_df["qname"].apply(clean_qname)

    # Compute entropy
    dns_df["entropy"] = dns_df["qname_clean"].apply(shannon_entropy)

    # Add supporting features if present
    dns_df["udp_length"] = df.get("udp.length", 0)
    dns_df["ip_length"] = df.get("ip.ip.len", 0)
    dns_df["ttl"] = df.get("ip.ip.ttl", 0)
    dns_df["response_flag"] = df.get("dns.flags.response", 0)
    dns_df["dns_time"] = df.get("dns.dns.time", 0)

    dns_df["label"] = label

    return dns_df


#############################
# MAIN PIPELINE
#############################

all_datasets = []

for name, file in FILES.items():
    label = 0 if name == "normal" else 1
    processed = process_file(file, label)
    all_datasets.append(processed)

final_df = pd.concat(all_datasets, ignore_index=True)

# Clean NaNs
final_df.fillna(0, inplace=True)

# Save
final_df.to_csv(OUTPUT_FILE, index=False)

print("\nPreprocessing complete.")
print(f"Saved to: {OUTPUT_FILE}")
print(final_df.head())
