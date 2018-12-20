"""
Given preprocessed sentences and word-atom alignment frequencies generates a sequence of ULF atoms.
"""

from __future__ import division

from ulf_align import split_ulf_atom, AnnSents, AnnToken, AnnSent
import argparse
import json

# Generates ULF atoms from words, lemmas, and POS tags and alignment counts.
# Uses pos2ext counts either separately or integrated with token2atomcounts
# TODO: handle multiword -> ULF segment mappings.
def words2atoms(annsent, token2atom, lemma2atom, pos2ext):
  # If this is an ner get contiguous ner and form a |...| TODO: figure out
  # how to recover original text span from the tokens... I think stanford
  # parser preserves the character spans form the original sentence.  ACTUALLY, apparent the NER files have the capitalization preserved tokens!  The original span would still be better, but this can be simple start
 
  in_ner = False
  cur_ners = []
  atoms = []
  for anntoken in annsent.anntokens:
    token = anntoken.token.decode("utf-8").encode("ascii", "ignore")
    lemma = anntoken.lemma.decode("utf-8").encode("ascii", "ignore")
    pos = anntoken.pos.decode("utf-8").encode("ascii", "ignore")
    ner = anntoken.ner.decode("utf-8").encode("ascii", "ignore")
    if in_ner and ner == "O":
      # Just finished building a named entity.
      atoms.append("|{}|".format(" ".join(cur_ners)))
      cur_ners = []
      in_ner = False
    elif in_ner:
      # Middle of building named enitty.
      cur_ners.append(token)
    elif ner != "O":
      # STarted building a named enitty.
      cur_ners.append(token)
      in_ner = True
    else:
      # Building normal atoms.
      extc = pos2ext[pos] if pos in pos2ext else []
      latc = [(x,y) for x, y in lemma2atom[lemma]] if lemma in lemma2atom else []
      tatc = [(x,y) for x,y in token2atom[token]] if token in token2atom else []
      
      # TODO preprocess these counts.
      extsum = sum([e[1] for e in extc])
      extmle = { ext : c / extsum for ext, c in extc }
      latsum = sum([e[1] for e in latc])
      latmle = { lat : c / latsum for lat, c in latc }
      tatsum = sum([e[1] for e in tatc])
      tatmle = { tat : c / tatsum for tat, c in tatc }


      # Considered concepts.
      ats = list(set([e[0] for e in latc + tatc]))
      
      if len(ats) == 0:
        # If there are no available atoms, generate one.
        bestext = "PRO"
        bestscore = -1
        for ext, score in extmle.iteritems():
          if score > bestscore and ext:
            bestscore = score
            bestext = ext
        atoms.append(lemma.upper() + "." + bestext)
      else:
        # Sum the scores of all three with the token having twice the weight of
        # the other two.
        bestat = ats[0]
        bestscore = -1
        for at in ats:
          base, ext = split_ulf_atom(at)
          extscore = 1 / extsum if extsum > 0 else 0
          if ext in extmle:
            extscore = extmle[ext]
          latscore = 1 / latsum if latsum > 0 else 0
          if at in latmle:
            latscore = latmle[at]
          tatscore = 1 / tatsum if tatsum > 0 else 0
          if at in tatmle:
            tatscore = tatmle[at]
          score = tatscore + 0.5 * (latscore + extscore)
          if score > bestscore:
            bestscore = score
            bestat = at
        atoms.append(bestat)
  return atoms
    
    
if __name__ == "__main__":
  parser = argparse.ArgumentParser()

  parser.add_argument("--annsent_dir", type=str, required=True, help="Path to the annotated data")
  #parser.add_argument("--token_file", type=str, required=True, help="Path to token file.")
  #parser.add_argument("--lemma_file", type=str, required=True, help="Path to the lemmatized data file.")
  #parser.add_argument("--pos_file", type=str, required=True, help="Path to the POS tag file.")
  #parser.add_argument("--ner_file", type=str, required=True, help="Path to the NER tag file.")
  parser.add_argument("--atom_counts", type=str, required=True, help="Path to the JSON file with ULF atom and extension counts.")
  parser.add_argument("--outfile", type=str, required=True, help="Output file path.")

  args, unparsed_args = parser.parse_known_args()

  annsents = AnnSents(args.annsent_dir)
  atcounts = json.loads(file(args.atom_counts, 'r').read())
  
  sent_atoms = []
  for annsent in annsents.annsents:
    atoms = words2atoms(annsent, atcounts["token2atom"], atcounts["lemma2atom"], atcounts["pos2ext"])
    sent_atoms.append(atoms)

  out = file(args.outfile, "w")
  out.write("\n".join(["\t".join(atoms) for atoms in sent_atoms]))
  out.close()

