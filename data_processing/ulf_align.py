"""
Aligns an AMR formatted ULF with an annotated sentence (tokens, lemmas, pos,
NER).
"""

from __future__ import division

from collections import namedtuple
from difflib import SequenceMatcher
# Representation based on smatch code.
from el_amr import AMR
# Representation used by Xiaochang's code.
from amr_graph import *

import os
from queue import PriorityQueue
import sys

AnnToken = namedtuple('AnnToken', ['token', 'lemma', 'pos', 'ner'])
AnnSent = namedtuple('AnnSent', ['anntokens'])

# Loads in a dataset of sentence annotations.
class AnnSents:
  def __init__(self, datadir):
    self.__tokens = AnnSents.loadTokens(os.path.join(datadir, "token"))
    self.__lemmas = AnnSents.loadTokens(os.path.join(datadir, "lemma"))
    self.__poses = AnnSents.loadTokens(os.path.join(datadir, "pos"))
    self.__ners = AnnSents.loadNER(os.path.join(datadir, "ner"))

    assert(len(self.__tokens) == len(self.__lemmas))
    assert(len(self.__tokens) == len(self.__poses))
    assert(len(self.__tokens) == len(self.__ners))

    self.annsents = []
    for sdata in zip(self.__tokens, self.__lemmas, self.__poses, self.__ners):
      assert len(sdata[0]) == len(sdata[1]), "{}, {}".format(len(sdata[0]), len(sdata[1]))
      assert len(sdata[0]) == len(sdata[2]), "{}, {}".format(len(sdata[0]), len(sdata[2])) 
      assert len(sdata[0]) == len(sdata[3]), "{}, {}".format(len(sdata[0]), len(sdata[3]))
      annsent = AnnSent([AnnToken(t, l, p, n) for t, l, p, n in zip(*sdata)])
      self.annsents.append(annsent)

  # Tokens are stored in files where each sentence is on its own line and tokens
  # separated by tabs.
  @staticmethod
  def loadTokens(filename):
    lines = [l for l in open(filename, 'r').read().splitlines() if l.strip() != ""]
    return [l.split(" ") for l in lines]

  # NER files separate sentences with two newlines, each word is on its own line 
  # in the format [word]\t[NER label].
  @staticmethod
  def loadNER(filename):
    sents = [s for s in open(filename, 'r').read().split("\n\n") if s.strip() != ""]
    ners = [[l.split("\t")[1] for l in s.splitlines()] for s in sents]
    return ners

  def getAnnSents(self):
    return self.annsents

  def size(self):
    return len(self.annsents)

  def get(self, n):
    if n >= self.size() or n < 0:
      raise Exception
    return self.annsents[n]


class Alignment:
  def __init__(self, span2nodes, sent, ulfamr, amrtype=None):
    self.__span2nodes = span2nodes
    self.__sent = sent
    self.__ulfamr = ulfamr
    if not amrtype:
      raise Exception
    self.__amrtype = amrtype
    # Alignment node labels (NB: different from the graph node labels!!!)
    self.__node_labels = None
    if amrtype == "smatch":
      self.__node_labels = Alignment.smatch_amr_alignment_labels(ulfamr)
    elif amrtype == "xiaochang":
      self.__node_labels = Alignment.xiaochang_amr_alignment_labels(ulfamr)
    else:
      raise Exception
    self.__alignment_string = None

  # Returns a list of alignment labels for the amr graph which corresponds
  # to the given amr.  Root: 0, First child of root: 0.0, second child of root: 0.1
  @staticmethod
  def smatch_amr_alignment_labels(ulfamr):
    alabels = [-1]*len(ulfamr.nodes)
    def recursive_labels(curidx, curlabel):
      assert alabels[curidx] == curlabel
      # For each child of the current index, add the label and recurse.
      finalidx = 0
      for chd, val in ulfamr.relations[curidx].items():
        chdidx = ulfamr.nodes.index(chd) 
        newlabel = "{}.{}".format(curlabel, finalidx)

        alabels[chdidx] = newlabel
        recursive_labels(chdidx, newlabel)
        finalidx += 1 
    # Assume the root is the first node.
    startlabel = "0"
    alabels[0] = startlabel
    recursive_labels(0, startlabel)
    for x in alabels:
      assert x != -1
    return alabels
  
  # Returns a list of alignment labels for the amr graph which corresponds
  # to the given amr.  Root: 0, First child of root: 0.0, second child of root: 0.1
  @staticmethod
  def xiaochang_amr_alignment_labels(ulfamr):
    # AMR node labels (i.e. variable ) -> Alignment label (i.e. path)
    #alabels = {}
    alabels = [-1]*len(ulfamr.nodes)
    def recursive_labels(curnode, curnid, curlabel):
      assert alabels[curnid] == curlabel
      # For each child of the current index, add the label and recurse.
      for i in range(len(curnode.v_edges)):
        newnid, newnode = curnode.get_child(i) 
        newlabel = "{}.{}".format(curlabel, i)
        #alabels[newnode.node_label()] = newlabel
        alabels[newnid] = newlabel
        #print chdidx
        #print val
        #print ulfamr.relations[curidx]
        #print ulfamr.relations
        #print ulfamr.nodes
        #print ulfamr.node_values
        #print ulfamr.attributes
        recursive_labels(newnode, newnid, newlabel)
    # Assume the root is the first node.
    startlabel = "0"
    rootnode = ulfamr.nodes[ulfamr.root]
    #alabels[rootnode.node_label()] = startlabel
    alabels[ulfamr.root] = startlabel
    recursive_labels(rootnode, ulfamr.root, startlabel)
    #assert len(alabels) == len(ulfamr.nodes)
    for x in alabels:
      assert x != -1
    return alabels

  # Returns an alignment string in AMR format.
  # [span1]|[node]+[node]+[node] [span2]|[node]+[node]+[node]...
  def alignment_string(self):
    if self.__alignment_string:
      return self.__alignment_string
    strpieces = []
    for s, nidxs in self.__span2nodes.items():
      spanstr = "{}-{}".format(s[0],s[1])
      nlabels = [self.__node_labels[n] for n in nidxs]
      nlabels.sort()
      strpieces.append("{}|{}".format(spanstr, "+".join(nlabels)))
    self.__alignment_string = " ".join(strpieces)
    return self.__alignment_string


# TODO: put this in some utility file...
# Splits a ULF atom to the string and the suffix.
# If it's a name (|blah blah|) the extesion is "name"
def split_ulf_atom(atom):
  if atom[len(atom) - 1] == "|":
    return (atom[1:len(atom)-1], "name")
  if len(atom) > 3 and atom[len(atom) - 2] == "|" and atom[len(atom) - 1] == "\"":
    return (atom[2:len(atom)-2], "name")
  dotsplit = atom.split(".")
  if len(dotsplit) == 1:
    return (atom, None)
  else:
    return (".".join(dotsplit[:len(dotsplit)-1]), dotsplit[len(dotsplit)-1])


# Aligns a ULF formula in AMR format to the sentence it represents.
class ULFAMRAligner:
  def __init__(self, annsent, amr, score_weights={"sym":1,"pos":0.5,"loc":0.5}, min_score=1.0, amrtype=None, merge_nodes=True):
    self.__annsent = annsent
    self.__amr = amr
    self.__alignment = None
    # Weighting of each type of comparision between words and nodes.
    self.__score_weights = score_weights
    self.__min_alignment_score = min_score
    if not amrtype:
      raise Exception
    self.__amrtype = amrtype
    self.__merge_nodes = merge_nodes

  # Compute the word-node alignment score.
  # Symbol score: max(overlap(token, symbol), overlap(lemma, symbol))
  # POS score: overlap(pos, extension) TODO: use mapping between the two
  # Loc score: 1 - dist(word location, node location)
  # Combine these together using specified hyperparams.
  @staticmethod
  def wordnode_score(annword, node_value, wloc, nloc, score_weights):
    ulfword, ulfext = split_ulf_atom(node_value)
    tokensm = SequenceMatcher(None, annword.token, ulfword)
    lemmasm = SequenceMatcher(None, annword.lemma, ulfword.lower())
    symscore = max(tokensm.ratio(), lemmasm.ratio())
    posscore = 0
    if ulfext:
      posscore = SequenceMatcher(None, annword.pos.lower(), ulfext.lower()).ratio()
    locscore = 1 - abs(wloc - nloc)
    return symscore * score_weights["sym"] + \
        posscore * score_weights["pos"] + \
        locscore * score_weights["loc"]
      

  def align(self):
    if self.__amrtype == "smatch":
      self.smatch_align()
    elif self.__amrtype == "xiaochang":
      self.xiaochang_align()
    else:
      raise Exception

  # Alignment is performed by computing a word-node alignment score which takes
  # into consideration the overlap of the word and lemma against the node label, 
  # correspondence of the POS tag and the type extension, and the relative 
  # positions in the respective representations.
  # Given these scores, we place them in a priority queue and pull out the alignments
  # in order of scores, discarding any that are inconsistent with existing alignments.
  def smatch_align(self):
    if self.__alignment:
      return self.__alignment
    #print self.__annsent
    #print self.__amr
    # Add the location factor to the sentence.
    # Word width = (1/len(sent))
    # Location factor = index * (1/len(sent))
    wordwidth = 1 / len(self.__annsent.anntokens)
    # Add the location factor to each amr node
    # Node width = (1/len(nodes))
    nodewidth = 1 / len(self.__amr.nodes)
    # For every pair of word and node compute alignment score and
    # add to priority queue.
    pq = PriorityQueue()
    for i in range(len(self.__annsent.anntokens)):
      for j in range(len(self.__amr.nodes)):
        # ignore if the node is a "COMPLEX" node which is a meta-logical symbol.
        if self.__amr.node_values[j].lower() != "complex":
          word = self.__annsent.anntokens[i]
          wloc = wordwidth * i
          node = self.__amr.nodes[j]
          node_value = self.__amr.node_values[j]
          nloc = nodewidth * j
          #print "i: {}\tj: {}".format(i,j)
          #print "Word: {}".format(word)
          #print "Node: {}, {}".format(node, node_value)
          ascore = ULFAMRAligner.wordnode_score(
              word, node_value, wloc, nloc, self.__score_weights)
          if ascore > self.__min_alignment_score:
            # PriorityQueue is small value first so negate weights.
            pq.put((-1 * ascore, i, j))
    # Pull out the alignments one by one and add to the span mapping.
    # Discard any, where adding it would lead to a discontinuous span or node.
    w2n = {}
    n2w = {}
    while not pq.empty():
      ascore, widx, nidx = pq.get()
      curnode = self.__amr.nodes[nidx]
      #print ascore, widx, nidx
      # If a word already has a mapping, make sure that this new node connects
      # to already existing mapped nodes.
      if widx in w2n:
        mapped_nidxs = w2n[widx]
        mrel_nodes = [rn for mnidx in mapped_nidxs for rn in self.__amr.relations[mnidx].keys()]
        #print nodesrels
        #print self.__amr.nodes
        #print self.__amr.nodes[nidx]
        #print self.__amr.relations
        #print self.__amr.relations[nidx][self.__amr.nodes[nidx]]
        curnode_rels = self.__amr.relations[nidx].keys()
        # Current node not in the relations from existings nodes and
        # existing nodes aren't in the relations from the current node (nidx) -- discard.
        if curnode not in mrel_nodes and \
            len([n for n in mapped_nidxs if self.__amr.nodes[n] in curnode_rels]) == 0:
          continue 
      # If a node maps to a word already, make sure this new word is adjacent to at
      # least one of the existing words.
      if nidx in n2w:
        widxs = n2w[nidx]
        if 1 not in [abs(widx - w) for w in widxs]:
          continue
      # We've already checked for discontinuity, so just add it now.
      if widx not in w2n:
        w2n[widx] = []
      if nidx not in n2w:
        n2w[nidx] = []
      w2n[widx].append(nidx)
      n2w[nidx].append(widx)
      # TODO: expand node mappings to certain elements (e.g. ds, type-shifters)
   
    #print "w2n: {}".format(w2n)
    #print "n2w: {}".format(n2w)

    # For each node, construct a span of words it aligns with.
    n2s = { n : (min(ws), max(ws)+1) for n, ws in n2w.items() }
    mergespans = []
    if self.__merge_nodes:
      # Merge overlapping spans and get a union of nodes.
      spans = n2s.values()
      spans.sort()
      remainspans = spans
      while len(remainspans) > 0:
        mergespan = remainspans.pop(0)
        newremainspans = []
        for span2 in remainspans:
          # If both maxes are greater than the other's min, it must overlap.
          if mergespan[1] > span2[0] and span2[1] > mergespan[0]:
            mergespan = (min(mergespan[0], span2[0]), max(mergespan[1], span2[1]))
          else:
            newremainspans.append(span2)
        mergespans.append(mergespan)
        # Update remaining spans to those that weren't merged.
        remainspans = newremainspans
    else:
      mergespans = [v for k, v in n2s.items()]

    # Get union of nodes from this span.
    s2n = {}
    for span in mergespans:
      nodes = []
      for widx in range(span[0], span[1]):
        if widx in w2n:
          nodes.extend(w2n[widx])
      s2n[span] = sorted(list(set(nodes)))

    #print "s2n: {}".format(s2n)
    #print "n2s: {}".format(n2s)

    self.__alignment = Alignment(s2n, self.__annsent, self.__amr, amrtype="smatch")
    return self.__alignment

  # Alignment is performed by computing a word-node alignment score which takes
  # into consideration the overlap of the word and lemma against the node label, 
  # correspondence of the POS tag and the type extension, and the relative 
  # positions in the respective representations.
  # Given these scores, we place them in a priority queue and pull out the alignments
  # in order of scores, discarding any that are inconsistent with existing alignments.
  def xiaochang_align(self):
    if self.__alignment:
      return self.__alignment
    #print self.__annsent
    #print self.__amr
    # Add the location factor to the sentence.
    # Word width = (1/len(sent))
    # Location factor = index * (1/len(sent))
    wordwidth = 1 / len(self.__annsent.anntokens)
    # TODO: ignore complex nodes when computing node location -- not just here,
    #       also in the summing stage.  Probably just make a function that takes a
    #       node and a graph and just does it all in one go.
    # Add the location factor to each amr node
    # Node width = (1/len(nodes))
    nodewidth = 1 / len(self.__amr.nodes)
    # For every pair of word and node compute alignment score and
    # add to priority queue.
    pq = PriorityQueue()
    for i in range(len(self.__annsent.anntokens)):
      for j in range(len(self.__amr.nodes)):
        node = self.__amr.nodes[j]
        node_value = node.node_str()
        # ignore if the node is a "COMPLEX" node which is a meta-logical symbol.
        if node.node_str() != "complex":
          word = self.__annsent.anntokens[i]
          wloc = wordwidth * i
          nloc = nodewidth * j
          #print "i: {}\tj: {}".format(i,j)
          #print "Word: {}".format(word)
          #print "Node: {}, {}".format(node, node_value)
          ascore = ULFAMRAligner.wordnode_score(
              word, node_value, wloc, nloc, self.__score_weights)
          if ascore > self.__min_alignment_score:
            # PriorityQueue is small value first so negate weights.
            pq.put((-1 * ascore, i, j))
    # Pull out the alignments one by one and add to the span mapping.
    # Discard any, where adding it would lead to a discontinuous span or node.
    w2n = {}
    n2w = {}
    while not pq.empty():
      ascore, widx, nidx = pq.get()
      curnode = self.__amr.nodes[nidx]
      curnode_label = self.__amr.nodes[nidx].node_label()
      #print ascore, widx, nidx
      # If a word already has a mapping, make sure that this new node connects
      # to already existing mapped nodes.
      if widx in w2n:
        mapped_nidxs = w2n[widx]

        # Get the node labels (e.g. v1 for (v1 / run ...)) for all nodes neighboring 
        # nodes that are mapped to the current word.
        #print list(enumerate([t.token for t in self.__annsent.anntokens]))
        #print list(enumerate([n.node_label() for n in self.__amr.nodes]))
        #print type(self.__amr)
        #print self.__amr
        #print self.__amr.nodes[nidx]
        #print self.__amr.nodes[nidx].v_edges
        mrel_nodes = [rn for mnidx in mapped_nidxs for rn in \
            [node.node_label() for nid, node in self.__amr.nodes[mnidx].get_children()]]
        #print nodesrels
        #print self.__amr.nodes
        #print self.__amr.nodes[nidx]
        #print self.__amr.relations
        #print self.__amr.relations[nidx][self.__amr.nodes[nidx]]
        # Get the node labels for nodes that neighbor the current node. 
        curnode_rels = [node.node_label() for nid, node in self.__amr.nodes[nidx].get_children()]
        
        # Current node not in the relations from existings nodes and
        # existing nodes aren't in the relations from the current node (nidx) -- discard.
        if curnode_label not in mrel_nodes and \
            len([n for n in mapped_nidxs if self.__amr.nodes[n].node_label() in curnode_rels]) == 0:
          continue 
      # If a node maps to a word already, make sure this new word is adjacent to at
      # least one of the existing words.
      if nidx in n2w:
        widxs = n2w[nidx]
        if 1 not in [abs(widx - w) for w in widxs]:
          continue
      # We've already checked for discontinuity, so just add it now.
      if widx not in w2n:
        w2n[widx] = []
      if nidx not in n2w:
        n2w[nidx] = []
      w2n[widx].append(nidx)
      n2w[nidx].append(widx)
      # TODO: expand node mappings to certain elements (e.g. ds, type-shifters)
   
    #print "w2n: {}".format(w2n)
    #print "n2w: {}".format(n2w)

    # TODO: generalize the merging to ignore COMPLEX nodes, i.e. two nodes with
    #       a path consisting only of COMPLEX nodes is considered adjacent.
    # For each node, construct a span of words it aligns with.
    n2s = { n : (min(ws), max(ws)+1) for n, ws in n2w.items() }
    mergespans = []
    if self.__merge_nodes:
      # Merge overlapping spans and get a union of nodes.
      spans = n2s.values()
      list(spans).sort()
      remainspans = spans
      while len(remainspans) > 0:
        mergespan = list(remainspans).pop(0)
        newremainspans = []
        for span2 in remainspans:
          # If both maxes are greater than the other's min, it must overlap.
          if mergespan[1] > span2[0] and span2[1] > mergespan[0]:
            mergespan = (min(mergespan[0], span2[0]), max(mergespan[1], span2[1]))
          else:
            newremainspans.append(span2)
        mergespans.append(mergespan)
        # Update remaining spans to those that weren't merged.
        remainspans = newremainspans
    else:
      mergespans = [v for k, v in n2s.items()]

    # Get union of nodes from this span.
    s2n = {}
    for span in mergespans:
      nodes = []
      for widx in range(span[0], span[1]):
        if widx in w2n:
          nodes.extend(w2n[widx])
      s2n[span] = sorted(list(set(nodes)))

    #print "s2n: {}".format(s2n)
    #print "n2s: {}".format(n2s)

    self.__alignment = Alignment(s2n, self.__annsent, self.__amr, amrtype="xiaochang")
    return self.__alignment

  def amr_align_format(self):
    if not self.__alignment:
      if self.__amrtype == "smatch":
        self.smatch_align()
      elif self.__amrtype == "xiaochang":
        self.xiaochang_align()
      else:
        raise Exception
    return self.__alignment.alignment_string()


if __name__ == "__main__":
  # TODO: use argparser, this is getting out of hand...
  if len(sys.argv) < 6:
    sys.exit("Usage: python align.py [sentence data dir] [ulfamr file] [output alignment file] [amr type] [merge nodes?]")
  
  amrtype = sys.argv[4]
  merge_nodes = sys.argv[5]
  merge_nodes_flag = None
  if merge_nodes.lower()[0] == "t":
    merge_nodes_flag = True
  elif merge_nodes.lower()[0] == "f":
    merge_nodes_flag = False
  else:
    raise Exception

  # Load data.
  print("Reading annotated sentence data...")
  annsents = AnnSents(sys.argv[1])
  print("Loading ULF AMRs...")
  ulfamrs = []
  for line in open(sys.argv[2]):
    cur_line = line.strip()
    if cur_line == "" or cur_line.startswith("#") or cur_line.startswith(";"):
      continue
    current = None
    if amrtype == "smatch":
      current = AMR.parse_AMR_line(cur_line.strip()[1:len(cur_line)-1])
    elif amrtype == "xiaochang":
      current = AMRGraph(cur_line.strip()[1:len(cur_line)-1])
    else:
      raise Exception
    #print "Parsed AMR line: {}".format(cur_line)
    #print current
    ulfamrs.append(current)
  assert annsents.size() == len(ulfamrs)
  
  # Get alignments.
  print("Computing alignments...")
  alignouts = []
  for annsent, ulfamr in zip(annsents.annsents, ulfamrs):
    aligner = ULFAMRAligner(annsent, ulfamr, amrtype=amrtype, merge_nodes=merge_nodes_flag)
    aligner.align()
    alignouts.append(aligner.amr_align_format())
  
  # Output results.
  print("Writing results...")
  out = open(sys.argv[3], 'w')
  out.write("\n".join(alignouts))
  out.close()
  print("Done!")

