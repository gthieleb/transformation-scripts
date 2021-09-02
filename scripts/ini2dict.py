#!/usr/bin/env python3

from configparser import RawConfigParser
import sys
import os
import json
from argparse import ArgumentParser

dest = "terraform.tfvars.json"

config = RawConfigParser()

root, src = sys.argv[1].split('=')

tpl = f"{src}.tpl"

config.read(src)

market = "BT"
app = "VMFrontend"
data = {root: {}}

config_tpl = RawConfigParser()

for s in config.sections():

    for k,v in config[s].items():
        key = "/".join((f"/{market}", app, s, k.replace('.', '/')))
        data[root][key] = v
        tpl_key = '{{{{ key "${{prefix}}{key}" }}}}'.format(key=key)
        if not s in config_tpl:
            config_tpl[s] = {k: tpl_key}
        else: 
            config_tpl[s][k] = tpl_key

for d in sys.argv[2:]:
    k,v = d.split('=')
    data[k] = v

with open(dest, 'w') as f:
    json.dump(data, f, indent=4)

with open(tpl, 'w') as f:
    config_tpl.write(f)
