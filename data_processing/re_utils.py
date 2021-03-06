import re
def extract_patterns(s_repr, pattern):
    #print s_repr
    #print pattern
    re_pat = re.compile(pattern)
    position = 0
    matched_list = []
    while position < len(s_repr):
        match = re_pat.search(s_repr, position)
        if not match:
            break
        matched_s = match.group(0)
        matched_list.append(matched_s)
        #print matched_s
        position = match.end()
    return matched_list

def delete_pattern(s_repr, pattern):
    re_pat = re.compile(pattern)
    position = 0
    matched_list = []
    while position < len(s_repr):
        match = re_pat.search(s_repr, position)
        if not match:
            break
        matched_s = match.group(0)
        matched_list.append(matched_s)
        position = match.end()

    for matched in matched_list:
        s_repr = s_repr.replace(matched, '')
    return s_repr

def parse_indexes(toks):
    toks = [tok.split('.')[1] for tok in toks]
    spans = []
    for tok in toks:
        spans += [int(p) for p in tok.split(',')]
    return spans

def getContinuousSpans(tok_indexes, unaligned, covered):
    all_spans = []
    if len(tok_indexes) == 0:
        return []
    if len(tok_indexes) == 1:
        return [(tok_indexes[0], tok_indexes[0]+1)]

    start = tok_indexes[0]
    end = tok_indexes[-1] + 1

    tmp_start = None
    for i in xrange(start, end):
        if i in covered:
            if tmp_start is None:
                tmp_start = i
        elif tmp_start is not None and i not in unaligned:
            all_spans.append((tmp_start, i))
            tmp_start = None

    if tmp_start is not None:
        all_spans.append((tmp_start, end))

    if len(all_spans) > 1:
        new_spans = []
        for (start, end) in all_spans:
            while (end-1) in unaligned:
                end -= 1
            assert start < end
            new_spans.append((start, end))
        all_spans = new_spans

    return all_spans

def all_aligned_spans(frag, opt_toks, role_toks, unaligned):
    tok_indexes = []
    covered = set()

    #First find all ops that are aligned to this frag
    for (s_index, e_index) in opt_toks:
        if frag.edges[e_index] == 1:
            if s_index not in covered:
                tok_indexes.append(s_index)
                covered.add(s_index)

    for (s_index, e_index) in role_toks:
        if frag.edges[e_index] == 1:
            if s_index not in covered:
                tok_indexes.append(s_index)
                covered.add(s_index)

    if len(tok_indexes) == 0:
        return (None, None)

    sorted_tok_indexes = sorted(tok_indexes)
    all_spans = getContinuousSpans(sorted_tok_indexes, unaligned, covered)

    return (sorted_tok_indexes, all_spans)

def extract_entity_spans(frag, opt_toks, role_toks, unaligned):
    op_indexs = []
    role_index_set = set()
    #First find all ops that are aligned to this frag
    for (s_index, e_index) in opt_toks:
        if frag.edges[e_index] == 1:
            op_indexs.append(s_index)

    for (s_index, e_index) in role_toks:
        if frag.edges[e_index] == 1:
            role_index_set.add(s_index)

    if len(op_indexs) == 0:
        return (None, None, None)

    op_indexs = sorted(op_indexs)
    op_set = set(op_indexs)
    start = op_indexs[0]
    end = start + 1
    m_end = start + 1
    while True:
        if end in op_set:
            end += 1
            m_end = end
        elif end in role_index_set:
            end += 1
            m_end = end
        elif end in unaligned:
            end += 1
        else:
            break
    return (start, m_end, m_end < op_indexs[-1])

if __name__ == '__main__':
    #print extract_patterns('. :t/tour~e.8 :wiki (. :-) :name (. :n/name :op1 (. :"APOLOGIES"~e.5) :op2 (. :"ON"~e.6) :op3 (. :"BEER"~e.7,10))', '~e\.[0-9]+(,[0-9]+)*')
    print extract_entity_spans('. :t/tour~e.8 :wiki (. :-) :name (. :n/name :op1 (. :"APOLOGIES"~e.5) :op2 (. :"ON"~e.6) :op3 (. :"BEER"~e.7,10))')
