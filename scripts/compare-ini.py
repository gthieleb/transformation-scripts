from configparser import RawConfigParser
import os
import sys
import json

d = {}

for path in sys.argv[1:]:

  c = RawConfigParser()
  # override lowercase method
  c.optionxform = lambda option: option
  c.read(path)

  sections = c.sections()
  
  for s in sections:
    for k in c[s]:
      if not s in d:
        d[s] = {}
      if not k in d[s]:
        d[s][k] = {}
      d[s][k][path] = c[s][k]

print(json.dumps(d, indent=4))
