#!/usr/bin/env python3
import argparse, csv, sys
from dateutil import parser

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("-i", "--input", required=True)
    p.add_argument("-s", "--start", required=True)
    p.add_argument("-e", "--end",   required=True)
    p.add_argument("-o", "--output") # defaults to stdout
    return p.parse_args()

def parse_date(s):
    return parser.parse(s, dayfirst=False, yearfirst=False)

def main():
    args = parse_args()
    try:
        start = parse_date(args.start)
        end   = parse_date(args.end)
    except Exception:
        sys.exit("Error parsing dates")

    dict = {}  #(complaint_type, borough), count


    # Read input and see if date is valid
    with open(args.input, newline='', encoding='utf-8', errors='ignore') as input:
        r = csv.DictReader(input)
        for row in r:
            created_date = row.get("Created Date", "")
            borough  = (row.get("Borough") or "").strip()
            complaint_type = (row.get("Complaint Type") or "").strip()
            if not created_date or not borough or not complaint_type:
                continue
            try:
                created_date = parse_date(created_date)
            except Exception:
                continue
            if start <= created_date <= end:
                key = (complaint_type, borough)
                dict[key] = dict.get(key, 0) + 1

    # Create output
    out = sys.stdout
    if args.output:
        out = open(args.output, "w", newline='', encoding='utf-8')
    w = csv.writer(out)
    w.writerow(["complaint type", "borough", "count"])
    for (complaint_type, borough), n in dict.items():
        w.writerow([complaint_type, borough, n])
    if args.output:
        out.close()

if __name__ == "__main__":
    main()