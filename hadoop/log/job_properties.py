#!/usr/bin/python

from argparse import ArgumentParser
import json
import os
import sys


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

def job_props(job_file,names):
  try:
    with open(job_file, 'r') as f:
      jobid, job = json.load(f).items()[0]

    values = []

    if names:
      props = names
    else:
      props = [k for k in job.keys() if k not in ['counters','maps','reduces']]

    for name in props:
      values.append('{}:{}'.format(name, job[name] if name.islower()
                                                   else get_counter_val(name)))
    print(' '.join(values))
  except Exception as e:
    sys.stderr.write('cannot process file {} because {}{}'
        .format(job_file, e, os.linesep))

def jobs_props(job_files, names, num_proc):
  for job_file in job_files:
    job_props(job_file, names)

def parse_args(args):
  p = ArgumentParser()
  p.add_argument('-i','--input-files',required=True,nargs='+')
  p.add_argument('-n','--num-cpus',required=False,default=1,type=int)
  p.add_argument('-p','--properties', required=False,nargs='+')
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])

  jobs_props(args.input_files, args.properties, args.num_cpus)

if __name__=='__main__':
  main()
