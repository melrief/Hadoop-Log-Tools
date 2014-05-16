#!/usr/bin/python

from argparse import ArgumentParser
import json
import os
import sys


def get_counter_val(d,key):
  counters = d['counters']
  for ns_key in counters:
    ns_val = d['counters'][ns_key][2]
    for counter_key in ns_val.keys():
      if counter_key == key:
        #print ns_val[counter_key][1]
        return ns_val[counter_key][1]

def job_props(job_file, names, with_job_name=False):
  try:
    with open(job_file, 'r') as f:
      jobid, job = json.load(f).items()[0]
    return job_props_from_json(jobid, job, names, with_job_name)
  except Exception as e:
    sys.stderr.write('cannot process file {} because {}{}'
        .format(job_file, e, os.linesep))


def job_props_from_json(jobid, job, names, with_job_name=False):
  try:
    values = {}

    if names:
      props = names
    else:
      props = [k for k in job.keys() if k not in ['counters','maps','reduces']]

    if with_job_name:
      values['jobid'] = jobid

    for name in props:
      values[name] = job[name] if name.islower() else get_counter_val(job, name)
    return values
  except Exception as e:
    sys.stderr.write('cannot process jobid {} because {}{}'
        .format(jobid, e, os.linesep))

def jobs_props(job_files, names, num_proc, with_job_name, show_props_names):
  for job_file in job_files:
    values = job_props(job_file, names, with_job_name)
    acc = []
    for name in names:
      buff = []
      if show_props_names:
        buff.append('{}:'.format(name))
      buff.append(values[name])
      acc.append(''.join(buff))
    print('\t'.join(acc))

def parse_args(args):
  p = ArgumentParser()
  p.add_argument('-j','--with-job-name',action='store_true',required=False)
  p.add_argument('-i','--input-files',required=True,nargs='+')
  p.add_argument('-n','--num-cpus',required=False,default=1,type=int)
  p.add_argument('-p','--properties', required=False,nargs='+')
  p.add_argument('-P','--show-props-names', action='store_true',required=False)
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])

  jobs_props(args.input_files
            ,args.properties
            ,args.num_cpus
            ,args.with_job_name
            ,args.show_props_names)

if __name__=='__main__':
  main()
