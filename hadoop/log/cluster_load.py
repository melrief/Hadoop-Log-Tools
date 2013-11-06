#!/usr/bin/env python
from __future__ import print_function,division

import argparse
import json
from itertools import groupby
import sys

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-t','--task-type',required=False,choices=['map','reduce'])
  p.add_argument('-i','--input-files',required=True, nargs='+'
                     ,type=argparse.FileType('rt'),metavar='INPUT_FILE')
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  events = []
  for input_file in args.input_files:
    job = json.load(input_file).values()[0]
    try:
      launch_time = int(job['launch_time'])
      if args.task_type:
        job_tasks = job[args.task_type + 's'].values()
        for task in job_tasks:
          try:
            finish_time = int(task['finish_time'])
            events.append( (launch_time,True) )
            events.append( (finish_time,False) )
          except KeyError:
            sys.stderr.write('finish time not found, ignoring\n')
          except ValueError:
            sys.stderr.write('the finish time is not a int, ignoring\n')
      else:
        try:
          finish_time = int(job['finish_time'])
          events.append( (launch_time,True) )
          events.append( (finish_time,False) )
        except KeyError:
          sys.stderr.write('finish time not found, ignoring\n')
        except ValueError:
          sys.stderr.write('the finish time is not a int, ignoring\n')
    except KeyError:
      sys.stderr.write('job is not a valid or successful job, ignoring\n'+str(job))
      continue

  loads = []
  c = 0
  for (t,es) in groupby(sorted(events),lambda(k):k[0]):
    for e in es:
      c = c + 1 if e[1] else c - 1
    loads.append( (t,c) )
    print(t,c)

if __name__=='__main__':
  main()
