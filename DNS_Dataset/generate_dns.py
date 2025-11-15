import random
import os
import time

domains = [
    "google.com", "facebook.com", "youtube.com", "openai.com", "wikipedia.org",
    "amazon.com", "github.com", "reddit.com", "linkedin.com", "cnn.com",
    "netflix.com", "stackoverflow.com", "apple.com", "microsoft.com",
    "cloudflare.com", "mozilla.org", "ibm.com", "dropbox.com", "zoom.us",
    "spotify.com", "oracle.com", "bbc.co.uk", "aliexpress.com", "bing.com",
    "protonmail.com", "python.org", "docker.com", "kubernetes.io"
]

record_types = ["A", "AAAA", "TXT", "MX", "NS", "CNAME"]

# number of queries you want (≈3000)
COUNT = 3000

for i in range(COUNT):
    d = random.choice(domains)
    r = random.choice(record_types)

    os.system(f"dig {d} {r} +short > /dev/null")

    if i % 100 == 0:
        print(f"Sent {i} queries...")

    time.sleep(0.01)  # avoid overloading DNS resolver
