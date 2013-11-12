#!/usr/bin/env python
def transpose(ls):
  return zip(*ls)

def to_tab(ls):
  if not ls:
    return ls

  strls = [[str(r) for r in c] for c in ls]
  idxs = range(len(ls[0]))
  lens = [0 for _ in idxs]
  for l in strls:
    for idx in idxs:
      curr = len(l[idx])
      if curr > lens[idx]:
        lens[idx] = curr

  acc = []
  for l in strls:
    curr = []
    for idx in idxs[:-1]:
      curr.append(('{:<' + str(lens[idx]) + '}').format(l[idx]))
    curr.append(('{:<}').format(l[-1]))
    acc.append(curr)
  return acc


#  acc = []
#  for strl in strls:
#    curr = []
#    for (s,l) in zip(strl,lenrows):
#      curr.append(('{:<' + (str(l) if l else '') + '}').format(s))
#    acc.append(curr)
#  return acc
