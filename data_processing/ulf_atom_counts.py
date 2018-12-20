"""
Given alignments of ULFs to token spans, generate correlation counts.
"""

from __future__ import division

from ulf_align import split_ulf_atom, AnnSents, AnnToken, AnnSent
import argparse
import json

# I'm pretty sure there's already a function that does this, but I couldn't 
# find it.
def load_alignment_file(filename):
  aligns = file(filename, 'r').read().split("\n\n")
  adata = []
  for a in aligns:
    if a.strip() != "":
      alines = a.splitlines()
      # First line is sentenc enumber so ignore.
      split = [[e.strip() for e in l.split("|||")] for l in alines[1:]]
      # Assume alignments are just token level (so ignore the span).
      adatum = [ [int(spl[0].split("-")[0])] + spl[1:] for spl in split ]
      adata.append(adatum)
  return adata



def correlation_counts(annsents, align_data):

  # token -> atom -> count
  token2atom = {}
  # lemma -> atom -> count
  lemma2atom = {}
  # pos -> ext -> count
  pos2ext = {}

  for i in range(len(annsents.annsents)):
    annsent = annsents.get(i)
    align = align_data[i]
    # Align format: index -> [span, token, TOKEN/NONE, atom, (amr) category, ?, atom]
    assert len(align) == len(annsent.anntokens)
    for anntok, aligntok in zip(annsent.anntokens, align):
      atom = aligntok[3]
      pos = anntok.pos
      lemma = anntok.lemma
      token = anntok.token
      # TODO: use defaultdict and Counter so that this code isn't so fucking messy.
      if atom != "NONE": 
        base, ext = split_ulf_atom(atom)
        if pos not in pos2ext:
          pos2ext[pos] = {}
        if ext not in pos2ext[pos]:
          pos2ext[pos][ext] = 0
        pos2ext[pos][ext] += 1

      if token not in token2atom:
        token2atom[token] = {}
      if atom not in token2atom[token]:
        token2atom[token][atom] = 0
      token2atom[token][atom] += 1
      if lemma not in lemma2atom:
        lemma2atom[lemma] = {}
      if atom not in lemma2atom[lemma]:
        lemma2atom[lemma][atom] = 0
      lemma2atom[lemma][atom] += 1

  # Convert the key1 -> key2 -> count to key1 -> (key2, count)
  token2atom = { token : [(a, c) for a, c in acounts.iteritems()]\
      for token, acounts in token2atom.iteritems() }
  lemma2atom = { lemma : [(a, c) for a, c in acounts.iteritems()] \
      for lemma, acounts in lemma2atom.iteritems() }
  pos2ext = { pos : [(e, c) for e, c in ecounts.iteritems()] \
      for pos, ecounts in pos2ext.iteritems() }
  
  return { "token2atom" : token2atom, "lemma2atom" : lemma2atom, "pos2ext" : pos2ext }


if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--annsent_dir", type=str, required=True, help="Path to the annotated data")
  parser.add_argument("--alignment_file", type=str, required=True, help="CoNLL style alignment file.")
  parser.add_argument("--outfile", type=str, required=True, help="Path for output JSON file of correlation counts.")

  args, unparsed_args = parser.parse_known_args()
  
  annsents = AnnSents(args.annsent_dir)
  align_data = load_alignment_file(args.alignment_file)
  
  counts = correlation_counts(annsents, align_data)
  out = file(args.outfile, 'w')
  out.write(json.dumps(counts, indent=4))

