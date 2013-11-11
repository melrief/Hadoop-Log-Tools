#!/usr/bin/env python
from __future__ import print_function,division

import argparse
import json
import os
import sys

import os.path
sys.path.append(os.path.abspath('.'))
from hadoop.util.padding import to_tab


def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-i','--input-files',required=True, nargs='+'
                     ,type=argparse.FileType('rt'))
  return p.parse_args(args)

def errl(m):
  sys.stderr.write('{}{}'.format(m,os.linesep))

def main():
  args = parse_args(sys.argv[1:])
  acc = []
  for input_file in args.input_files:
    try:
      jobWithId = json.load(input_file)
      jobid = jobWithId.keys()[0]
      job = jobWithId.values()[0]
      curr = ['id: {}'.format(jobid)]
      for key in filter(lambda(a): not a in ['counters','maps','reduces'],job):
        curr.append('{}: {}'.format(key,job[key]))
      acc.append(sorted(curr))
    except KeyError as e:
      errl('error for file {}: {} {}'.format(input_file.name,e.errno,e.strerror))
  for l in to_tab(acc):
    print(' | '.join(l))

if __name__=='__main__':
  main()

