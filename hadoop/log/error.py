#!/usr/bin/env python
from __future__ import print_function,division

import argparse
import json
import sys

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-t','--task-type',required=True,choices=['maps','reduces'])
  p.add_argument('-i','--input-files',required=True, nargs='+'
                     ,type=argparse.FileType('rt'))
  p.add_argument('-k','--num-samples',required=True,type=int)
  p.add_argument('-I','--include-le-k',default=False
                     ,action='store_true')
  p.add_argument('-s','--samples',default='starttime'
                     ,choices=['starttime','finishtime'])
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  k = args.num_samples
  for input_file in args.input_files:
    job = json.load(input_file).values()[0]
    raw_tasks = job[args.task_type]
    if not args.include_le_k and len(raw_tasks) <= k:
      continue
    tasks = []
    for task in raw_tasks.values():
      start_time = float(task['start_time'])/1000.
      finish_time = float(task['finish_time'])/1000.
      tasks.append( (finish_time if args.samples == 'finishtime' else start_time
                    ,finish_time - start_time) )
    tasks = map(lambda a:a[1]
               ,sorted(tasks,cmp=lambda a,b:cmp(a[0],b[0])))
    avg_tasks = sum(tasks)/len(tasks)
    samples = tasks[0:k]
    avg_samples = sum(samples)/len(samples)
    print( avg_samples/avg_tasks )

if __name__=='__main__':
  main()
