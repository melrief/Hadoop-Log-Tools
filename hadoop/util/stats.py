#!/usr/bin/env python
from __future__ import print_function

import argparse
import numpy as N
import os
import sys

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-i', '--input-files', default=[sys.stdin], nargs="+",
                 type=argparse.FileType('rt'),
                 help='input file or empty (stdin)')
  p.add_argument('-d', '--decorate',default=False,action='store_true'
                ,help='put the stat name before the value (e.g mean:1)')

  g = p.add_mutually_exclusive_group()
  g.add_argument('-A','--all-stats',action='store_true',default=False)

  h = p.add_argument_group('stat')
  h.add_argument('-a', '--mean', action='store_true', default=False)
  h.add_argument('-D', '--median', action='store_true', default=False)
  h.add_argument('-s', '--standard_deviation',action='store_true',default=False)
  h.add_argument('-v', '--variance', action='store_true', default=False)
  h.add_argument('-m', '--min', action='store_true', default=False)
  h.add_argument('-M', '--max', action='store_true', default=False)
  if not args:
    p.print_help()
    sys.exit(0)
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  for input_file in args.input_files:
    vals = [float(x) for x in input_file.read().split(os.linesep) if x]
    a = N.array(vals)

    s = []
    for (name,value,f) in [('mean', args.mean, N.mean)
                         , ('median', args.median, N.median)
                         , ('standard_deviation', args.standard_deviation
                                                , N.std)
                         , ('variance', args.variance, N.var)
                         , ('min', args.min, N.amin)
                         , ('max', args.max, N.amax)]:
      if not args.all_stats and not value:
        continue
      r = f(a)
      if args.decorate:
        s.append('{}:{}'.format(name,r))
      else:
        s.append('{}'.format(r))
    print(' '.join(s))


if __name__=='__main__':
  main()
