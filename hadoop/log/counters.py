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
  p.add_argument('-p','--preserve-namespace',required=False,action='store_true')
  return p.parse_args(args)

def errl(m):
  sys.stderr.write('{}{}'.format(m,os.linesep))

def main():
  args = parse_args(sys.argv[1:])
  for input_file in args.input_files:
    try:
      jobWithId = json.load(input_file)
      jobid = jobWithId.keys()[0]
      job = jobWithId.values()[0]
      acc = []
      for ns_key in job['counters'].keys():
        ns_val = job['counters'][ns_key][2]
        ns_key_short = ns_key if args.preserve_namespace else ns_key.split('.')[-1]
        for counter_key in ns_val.keys():
          key = ns_key_short + "." + counter_key
          counter = ns_val[counter_key]
          acc.append([jobid,key,counter[0],counter[1]])
      to_print = to_tab(acc)
      for line in to_print:
        print(' | '.join(line))
    except Exception as e:
      errl('error for file {}: {}'.format(input_file.name,e))

if __name__=='__main__':
  main()

