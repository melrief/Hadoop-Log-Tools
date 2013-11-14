import argparse
import datetime
import os
import re
import sys

def to_unix_timestamp(input):
  """ convert datetime to unix timestamp in milliseconds """
  start = datetime.datetime(year=1970,month=1,day=1)
  diff = input - start
  return int(diff.total_seconds() * 1000)

def to_op(raw_op):
  if raw_op == '<':
    return lambda x,y:float(x)<float(y)
  if raw_op == '>':
    return lambda x,y:float(x)>float(y)
  if raw_op == '<=':
    return lambda x,y:float(x)<=float(y)
  if raw_op == '>=':
    return lambda x,y:float(x)>=float(y)
  if raw_op == '==':
    return lambda x,y:float(x)==float(y)

def decode_val(v):
  if v:
    v = v.strip()
    # just a number
    if v.isdigit():
      return int(v)
    
    # date
    if v.startswith('date(') and v[-1] == ')':
      date_comps = map(int, v[5:-1].split(','))
      date = datetime.datetime(*date_comps)
      unix_timestamp = to_unix_timestamp(date)
      #sys.stderr.write('{} -> {} -> {}{}'.format(date_comps
      #                                          ,date
      #                                          ,unix_timestamp
      #                                          ,os.linesep))
      return unix_timestamp

    # something related to bytes
    last = v[-1].lower()
    mult = 1
    if last == 'k':
      mult = 1024
    elif last == 'm':
      mult = 1024 * 1024
    elif last == 'g':
      mult = 1000 * 1024 * 1024
    elif last == 't':
      mult = 1000 * 1000 * 1024 * 1024
    return int(v[:-1]) * mult
    raise ValueError(v)
  else:
    return v

def get_counter_val(key):
  def inner(d):
    counters = d['counters']
    for ns_key in counters:
      ns_val = d['counters'][ns_key][2]
      for counter_key in ns_val.keys():
        if counter_key == key:
          #print ns_val[counter_key][1]
          return ns_val[counter_key][1]
  return inner

class Pred:
  """ A predicated that when called can return either True or an error string """

  def __init__(self, field, op, val):
    self.field = field
    if field.islower():
      self.get_val = lambda d: d[field]
    else:
      self.get_val = get_counter_val(field)
    self.op_repr = op
    self.op = to_op(self.op_repr)
    self.val = decode_val(val)

  def __repr__(self):
    return '{} {} {}'.format(self.field, self.op_repr, self.val)

  def __call__(self, d):
    try:
      #sys.stderr.write('{}{}'.format(self.get_val(d),os.linesep))
      if self.op(self.get_val(d), self.val) == True:
        return True
      else:
        return 'predicate {} failed'.format(repr(self))
    except KeyError as e:
      return 'predicate {} throwed exception: {}'.format(repr(self),repr(e))
    except ValueError as e:
      return 'predicate {} throwed exception: {}'.format(repr(self),repr(e))

def parse_predicate(pred):
  """ 'name [<|<=|==|=>|>] val' """
  m = re.search('(<=|<|==|>=|>)', pred)
  if not m:
    return None

  raw_name = pred[:m.start()].strip()
  op = pred[m.start():m.end()].strip()
  val = pred[m.end():].strip()
  
  return Pred(raw_name, op, val)

def combine_predicates(*preds):
  def predicate(x):
    for pred in preds:
      res = pred(x)
      if res != True:
        return res
    return True

  return predicate

def many_strs_to_predicate(raw_preds):
  preds = []
  for raw_pred in raw_preds:
    pred = parse_predicate(raw_pred)
    if pred:
      preds.append(pred)
    else:
      sys.exit('ERROR: predicate {} wrong!'.format(raw_pred))

  return combine_predicates(*preds)

class PredAction(argparse.Action):
  def __call__(self, parser, ns, values, option_string=None):
    prev_pred = getattr(ns, self.dest)
    values_pred = many_strs_to_predicate(values)
    if prev_pred and values_pred:
      final_pred = combine_predicates(prev_pred, values_pred)
    elif prev_pred:
      final_pred = prev_pred
    elif values_pred:
      final_pred = values_pred
    setattr(ns, self.dest, final_pred)

def add_predicates(p):
  p.add_argument('-P','--predicate',metavar=('name op val')
                ,nargs='+'
                ,required=False
                ,action=PredAction
                ,help='considers jobs that satisfy the given predicate.' +\
                      ' Name is a name of a field (lowercase) or of a counter' +\
                      ' (uppercase) and op in one of < <= == => >')

if __name__=='__main__':

  p = argparse.ArgumentParser()
  add_predicates(p)
  args = p.parse_args(sys.argv[1:])

  if args.predicate:
    print args.predicate({ 'num_maps' : 1})
  else:
    print 'None'
