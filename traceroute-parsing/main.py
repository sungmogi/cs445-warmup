import json
import glob
import lib
from lib.Traceroute import RIPETraceroute


for tr_filename in glob.glob("data/NG/36940/*.json"):
    print(f"Processing {tr_filename}...")
    for tr_line in lib.generate_lines(tr_filename):
        print(tr_line)
        tr = RIPETraceroute(json.loads(tr_line))

        print(tr)
        print("." * 100)
