import os
import json
import sys
import subprocess
import hcl2


path = sys.argv[1]
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
