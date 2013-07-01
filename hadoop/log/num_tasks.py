#!/usr/bin/env python
from __future__ import print_function,division

import argparse
import json
import sys

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-t','--task-type',required=True,choices=['maps','reduces','both'])
  p.add_argument('-i','--input-files',required=True, nargs='+'
                     ,type=argparse.FileType('rt'))
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  for input_file in args.input_files:
    job = json.load(input_file).values()[0]
    if args.task_type == 'both':
      print( len(job['maps']),len(job['reduces']) )
    else:
      print(len( job[args.task_type] ))

if __name__=='__main__':
  main()
