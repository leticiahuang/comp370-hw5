#!/usr/bin/env python3
import csv, sys
from dateutil.parser import parser

inp = sys.argv[1]
outp = sys.argv[2]

with open(inp, newline='', encoding='utf-8', errors='ignore') as fin, \
     open(outp, 'w', newline='', encoding='utf-8') as fout:
    r = csv.DictReader(fin)
    w = csv.DictWriter(fout, fieldnames=r.fieldnames)
    w.writeheader()
    for row in r:
        cd = row.get("Created Date", "")
        z  = (row.get("Incident Zip") or "").strip()
        if not cd or not z:
            continue
        try:
            y = parser.parse(cd, dayfirst=False, yearfirst=False).year
        except Exception:
            continue
        if y == 2024:
            w.writerow(row)
