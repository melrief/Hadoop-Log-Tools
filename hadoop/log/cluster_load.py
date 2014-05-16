#!/usr/bin/env python
from __future__ import print_function,division

import argparse
import json
from itertools import groupby
import sys

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-i','--input-files',required=True, nargs='+'
                     ,type=argparse.FileType('rt'),metavar='INPUT_FILE')
  p.add_argument('-t','--time-format',required=False
                     ,choices=['milliseconds','seconds','minutes','hours']
                     ,default='milliseconds')
  return p.parse_args(args)

converters = {
      "milliseconds" : (lambda t:int(t))
    , "seconds"      : (lambda t:int(t/1000.))
    , "minutes"      : (lambda t:int(t/60000.))
    , "hours"        : (lambda t:int(t/3600000.))
    }

def run(input_files,converter=id):
  events = []
  for input_file in input_files:
    job = json.load(input_file).values()[0]
    try:
      launch_time = int(job['launch_time'])
      try:
        finish_time = int(job['finish_time'])
        events.append( (launch_time,True) )
        events.append( (finish_time,False) )
      except KeyError:
        sys.stderr.write('finish time not found, ignoring\n')
      except ValueError:
        sys.stderr.write('the finish time is not an int, ignoring\n')
    except KeyError:
      sys.stderr.write('job is not a valid or successful job, ignoring\n'+str(job))
      continue

  loads = []
  c = 0
  for (t,es) in groupby(sorted(events),lambda(k):k[0]):
    for e in es:
      c = c + 1 if e[1] else c - 1
    converted_t = converter(t)
    loads.append( (converted_t,c) )
    print(converted_t,c)

def main():
  args = parse_args(sys.argv[1:])
  run(args.input_files,converters[args.time_format])

if __name__=='__main__':
  main()
