import json
import glob
import lib
from lib.Traceroute import RIPETraceroute

output_data = []

for tr_filename in glob.glob("data/US/16509/*.json"):
    print(f"Processing {tr_filename}...")

    for tr_line in lib.generate_lines(tr_filename):
        tr = RIPETraceroute(json.loads(tr_line))  # Create RIPETraceroute object

        # Extract hops and RTTs
        hop_data = [{"hop": hop.addr, "RTT": hop.rtt} for hop in tr.hops]

        output_data.append(hop_data)  # Append to list

# Convert to JSON format and save to file
output_json = json.dumps(output_data, indent=4)

with open("US_1003387_output.json", "w") as f:
    f.write(output_json)

print("JSON output saved to output.json")


# import json
# import glob
# import lib
# from lib.Traceroute import RIPETraceroute


# for tr_filename in glob.glob("data/NG/36940/*.json"):
#     print(f"Processing {tr_filename}...")
#     for tr_line in lib.generate_lines(tr_filename):
#         print(tr_line)
#         tr = RIPETraceroute(json.loads(tr_line))

#         print(tr)
#         print("." * 100)
