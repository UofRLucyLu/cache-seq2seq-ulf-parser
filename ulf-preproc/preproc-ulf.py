"""
Gene Kim 
12-14-2018

Cleans a tsv file of

sid\tsentence\tulf

cleans the data and then puts the sentences and ulfs into separate files.
"""

import os 
import json
import sys

# Removes unnecessary newlines and tabs.
# We leave in extra spaces since lisp can do a better job of filtering those.
# TODO: remember to do the names preprocessing before inputting into Lisp.
def format_ulf(rawulf):
  # Turns it into one line.
  return rawulf.replace("\n", "").replace("\r\\n", "").replace("\\t", "")
  # Preserves the original newlines.
  #return rawulf.replace("\r\\n", "\n").replace("\\t", "")

def format_sent(sent):
  return sent.replace("\\n", "")


if len(sys.argv) < 2:
  sys.exit("Usage: preproc-ulf.py [config file]")

config = json.loads(file(sys.argv[1], 'r').read())

infile = file(config["sid-sent-ulf-file"], 'r').read()
if not os.path.exists(config["out-dir"]):
  os.makedirs(config["out-dir"])
sout = file(os.path.join(config["out-dir"], "raw"), "w")
uout = file(os.path.join(config["out-dir"], "ulf"), "w")

lines = infile.split(os.linesep)[1:]

for l in lines:
  if l.strip() == "":
    continue
  sid, rawsent, rawulf = l.split("\t")
  sent = format_sent(rawsent)
  ulf = format_ulf(rawulf)
  
  sout.write(sent)
  sout.write("\n")
  uout.write("; sid: {}\n".format(sid))
  uout.write("; sentence: {}\n".format(sent))
  uout.write(ulf)
  uout.write("\n\n")

sout.close()
uout.close()

