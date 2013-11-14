#!/usr/bin/env python
from __future__ import print_function,division

import argparse
import json
import os
import sys

import os.path

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
  fields = set()

  def decode(i):
    try:
      return json.load(i).items()[0]
    except ValueError as e:
      errl('{} raised {}'.format(i,e))
      return None
  
  inputs = []
  for input_file in args.input_files:
    res = decode(input_file)
    if res:
      inputs.append(res)
  
  for jobid,job in inputs:
    for key in job:
      if key not in ['counters','maps','reduces']:
        fields.add(key)

  # TODO: sort fields

  acc = []
  for jobid,job in inputs:
    curr = []
    curr.append('id: {}'.format(jobid))
    for field in fields:
      curr.append('{}: {}'.format(field, job[field] if field in job else 'n/a'))
    acc.append(curr)

  for line in to_tab(acc):
    print(' | '.join(line))
        

if __name__=='__main__':
  main()
