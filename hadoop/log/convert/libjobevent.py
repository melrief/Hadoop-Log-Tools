def parse_event(raw_event,preserve_backslash=False,preserve_dot=False):
  in_string = False
  words = []
  d = {}
  key = None
  curr = []
  for c in raw_event:
    if c == '\\' and not preserve_backslash:
      continue
    elif c == '"':
      in_string = not in_string
    elif c == ' ':
      if in_string:
        curr.append(c)
      else:
        if key:
          val = ''.join(curr)
          d[key] = decodeCounters(val) if key == 'COUNTERS' else val
          key = None
        else:
          word = ''.join(curr)
          if preserve_dot or word != '.':
            words.append( ''.join(curr) )
        curr = []
    elif c == '=':
      key = ''.join(curr)
      curr = []
    else:
      curr.append(c)
  if in_string:
    curr.append(c)
  else:
    if key:
      d[key] = ''.join(curr)
      key = None
    else:
      word = ''.join(curr)
      if preserve_dot or word != '.':
        words.append( ''.join(curr) )
  curr = []
  return words,d
    
def decodeCounters(counters):
  raw_counter_families = counters[1:-1].split('}{')
  counter_families = {}
  for raw_family in raw_counter_families:
    splitted = raw_family.split('[')
    name,desc = decodeCounterKey( splitted[0] )
    raw_counters = [s[:-1] if s[-1] == ']' else s for s in splitted[1:]]
    counters = {}
    for raw_counter in raw_counters:
      cname,fdesc,val = decodeCounterKey(raw_counter)
      #counters[cname] = Counter(cname,fdesc,val)
      counters[cname] = (fdesc,val)
    #counter_families[name] = CounterFamily(name,desc,counters)
    counter_families[name] = (name,desc,counters)
  return counter_families

def decodeCounterKey(s):
  return s[1:-1].split(')(')
