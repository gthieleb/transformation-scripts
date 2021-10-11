#!/usr/bin/env python3
import os
import json
import sys
import subprocess
import hcl2

"""
This script loads a json file that
is created via python-hcl2 and
extracts the variable names and defaults
and writes them to a tfvars.json file.

The file can be prefixed with dev|prod|etc

Setup:

Install python-hcl2 with using pip

Usage:

1. Convert hcl file using hcl2tojson

2. Extract the vars and defaults with this script

./tf-extract.py source.json <PREFIX> 

The destination file is created in the current directory, attached with the prefix. 
"""

errmsg = "Need to install hcl2tojson package!"

# path to tf variables file
path   = sys.argv[1]
prefix = sys.argv[2]

def load_hcl2(path):
  d = {}
  with open(path) as f:
    d = hcl2.load(f)
  return d

def extract_defaults(data):
  # hcl2tojson puts all variables in 
  # a json key named 'variable' so we extract that
  vars = data['variable']

  # this holds the tfvars json content
  tfvars = {}

  # now we can iterate the variables list and lookup 
  # for the optional default value
  for var in vars:
    for key, value in var.items():
      if not 'default' in value:
          tfvars[key] = None
      else:
          tfvars[key] = value['default']
  return tfvars

def write_tfvars_json(tfvars):
  dest = f"{prefix}.tfvars.json"
  with open(dest, "w") as f:
    json.dump(tfvars, f, indent=4)

d = load_hcl2(path)

tfvars = extract_defaults(d)
write_tfvars_json(tfvars)

print(json.dumps(tfvars, indent=4))
