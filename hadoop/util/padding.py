#!/usr/bin/env python
def transpose(ls):
  return zip(*ls)

def to_tab(ls):
  strls = [[str(r) for r in c] for c in ls]
  lenls = transpose([[len(r) for r in c[:-1]] for c in strls])
  lenrows = map(max,lenls)
  lenrows.append(None)
  acc = []
  for strl in strls:
    curr = []
    for (s,l) in zip(strl,lenrows):
      curr.append(('{:<' + (str(l) if l else '') + '}').format(s))
    acc.append(curr)
  return acc
