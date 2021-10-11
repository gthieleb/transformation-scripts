from netaddr import IPNetwork
import sys
import json
import glob

azs = 3
subnet_names = ["public", "private", "db", "custom1", "custom2", "custom3"]

# vpc cidr
cidr   = sys.argv[1]
# supernet prefix
prefix = int(sys.argv[2])

ip = IPNetwork(cidr)
supernet = ip.supernet(prefix)[0]

subnet_list = list(str(i) for i in supernet.subnet(ip.prefixlen))

count = len(subnet_list) // azs

subnets = {}
for idx in range(count):
    name = subnet_names[idx]
    if not name in subnets:
        subnets[name] = []
    subnets[name] = subnet_list[:3]
    del(subnet_list[:3])

print(json.dumps(subnets, indent=4))

files = glob.glob("*.json")

for fn in files:
    data = {}
    changed = False
    with open(fn) as f:
        data = json.load(f)
    if "vpc_cidr" in data and data["vpc_cidr"] != str(supernet):
        if input("Replace old supernet address {old} with {new}? [Y|y]: " \
                .format(old=data["vpc_cidr"],
                new=str(supernet))).lower() == "y":
            data["vpc_cidr"] = str(supernet)
            changed = True

    for lookup in subnet_names:
        keys = list(k for k in data.keys() if f"{lookup}_subnets" == k)
        if not keys:
            continue
        for key in keys:
            if input("Key {key} found!. Replace {old} with {new}? [Y|y]: ".format(
                                                key=key,
                                                old=json.dumps(data[key], indent=4),
                                                new=json.dumps(subnets[lookup], indent=4))).lower() == "y":
                data[key] = subnets[lookup]
                changed = True
    if not changed:
        continue
    print(f"Write new subnets to file {fn} ...")
    with open(fn, "w") as f:
        json.dump(data, f, indent=4)
