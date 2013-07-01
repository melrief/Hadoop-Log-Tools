# Hadoop Log Tools

The goal of this project is to provide easy and extensible tools to work with
*Hadoop* logs.

The project has two directories: *Hadoop* that is a *Python* module containing
all the libraries and *bin* that contains *Python* scripts. Each tool has its
own script in the *bin* directory.

The tools provided are divided in three: conversion tools, transformations tools
and visualization tools.

Note that each script support the `-h` option to get an helper. This is
useful to understand what a script does and what options accepts.

The available tools are:

**Conversion tools**: they are used to convert *Hadoop* logs to a format easy
to manipulate, like json.

- `jobevents2json`: convert *Hadoop* output files of each job containing the
    job events into a json format
- `jobsevents2json`: convert all the job events files in the *Hadoop* log
    directory to json format

**Transformations tools**: they are used to do transform the output of the
conversion tools or of another transformation tool in something else.
For example if you want to extract the
average map time you can use the script `jobtimes` to first extract the map
time for every map and then calculate the average using `stats` by pipelining
the two commands.

- `clusterload`: takes in input json files, one per job, and
   output, for each line, the time and the number of tasks space separated
- `esterror`: takes in input json files, one per job, and
   output the error done for each job when estimating the job size 
   using k samples. One value for each line
- `jobtimes`: take in input json files, one per job, and output one of the
   job times (map, shuffle, sort, reduce or full_reduce)
- `numtasks`: take in input json files, one per job, and output the number
    of tasks for each job, one per line
- `stats`: take in input one number per line and output mean, median, std, var,
    min and/or max

**Visualization tools**: set of tools used to visualize the data in output from
transformations tools with python matplotlib.

- `plotcdf`: takes in input values separated by a newline and output the
    plot with cdf of that lines
- `plotdots`: takes in input points separated by a newlines where each point
    is composed by two values, the x and the y, space separated
- `plotjobevents`: takes in input json files, one per job, and output the
    plot containing the job events. Job events are divided in start/finish of
    the job, map events and reduce events. Each job has its own line.

## Tools tutorials

### Convert job events to json

This is the first step: make a conversion from *Hadoop* logs to json
Let's say that `logs` is the *Hadoop* log directory. You can find the event
file of the jobs completed inside the directory
`logs/history/done/<version>/<job_tracker>/<year>/<month>/<day>/<run>/`.
You can select a file from there and convert it to json using `jobevents2json`.
For example:

```bash
./bin/jobevents2json -i logs/history/done/version-1/10-10-15-40.openstacklocal_1370025702265_/2013/05/31/000000/job_201305311841_0001_1370025764537_ubuntu_PigMix+L17
```

Without the `-o` option `jobevents2json` writes the json conversion to stdout.

If you want to convert *all* the jobs files into json and put them into a
directory you can use the utility `jobsevents2json`. For example:

```bash
./bin/jobsevents2json logs/ job_jsons/
```

Note that `jobsevents2json` takes in input the *root directory* of the logs, so
it is very convenient.

The output json has the following format: it is a dictionary with one key
and one value. The key is the jobid. The value is another dictionary with
all the informations of the jobs (job_name,launch_time,...). The value
contains also a `maps` and a `reduces` key which are two dictionaries with
all the tasks of that time. An example of output is:

```json
{
  "job_201305311841_0099": {
    "finish_time": "1370029490179",
    "jobname": "PigMix L16",
    "launch_time": "1370029440957",
    "maps": {
      "task_201305311841_0099_m_000000": {
        "finish_time": "1370029463019",
        "other_attempts": {},
        "start_time": "1370029453999",
        "successful_attempt": {
          "attempt_201305311841_0099_m_000000_0": {
            "hostname": "/default-rack/10-10-15-22.openstacklocal"
          }
        }
      },
      "task_201305311841_0099_m_000001": {
        "finish_time": "1370029460923",
        "other_attempts": {},
        "start_time": "1370029454878",
        "successful_attempt": {
          "attempt_201305311841_0099_m_000001_0": {
            "hostname": "/default-rack/10-10-15-39.openstacklocal"
          }
        }
      }
    },
    "reduces": {
      "task_201305311841_0099_r_000000": {
        "finish_time": "1370029484047",
        "other_attempts": {},
        "start_time": "1370029466011",
        "successful_attempt": {
          "attempt_201305311841_0099_r_000000_0": {
            "hostname": "/default-rack/10-10-15-25.openstacklocal",
            "shuffle_finished": "1370029477746",
            "sort_finished": "1370029478152"
          }
        }
      }
    },
    "submit_time": "1370029437262"
  }
}
```

After the conversion we can use the transformation tools to extract data from
the result.


### Jobs times

Let's say we want to know the map time of every task of the job_0001. We already
have a file called job_0001.json that contains the result of `jobevents2json`.
We can obtain them with the script `jobtimes`:

```bash
./bin/jobtimes -p map -i job_jsons/job_0001.json
```

This will output one map time per line, for example:

```
12.099
15.117
9.085
12.087
```

Now we want to know the mean of those map times. We can use `stats`:

```bash
./bin/jobtimes -p map -i job_jsons/job_0001.json | ./bin/stats -a
```

We obtain the mean `12.097` as single value in a single line.


### Plot CDF

We want to plot the CDF of the sojourn times of jobs. We can first get the
jobs sojourn times with the command:

```bash
./bin/jobtimes -s -i job_jsons/*
```

and then pipeline it to `plotcdf`:

```bash
./bin/jobtimes -s -i job_jsons/* | ./bin/plotcdf
```

if we like the plot we can save it somewhere:

```bash
./bin/jobtimes -s -i job_jsons/* | ./bin/plotcdf -o sojourn_times.pdf
```

### More advanced examples

To plot the task times CDF of two different workloads, let's say
*huge_hfsp* and *small_hfsp*, you can use:

```bash
./plotcdf.py -i \
  <( ./jobtimes.py -p map -i huge_hfsp/job_infos/* small_hfsp/job_infos/* ) \
  <( ./jobtimes.py -p full_reduce -i huge_hfsp/job_infos/* small_hfsp/job_infos/* ) \
  -l "\\textsc{Map}" "\\textsc{Reduce}" -L 4 -xl "Task Time" \
  -w 5 -a 12.0 6.0 \
  -o task_times.eps
```

Let's analyze it step-by-step:

```bash
./plotcdf.py -i \
  <( ./jobtimes.py -p map -i huge_hfsp/job_infos/* small_hfsp/job_infos/* ) \
  <( ./jobtimes.py -p full_reduce -i huge_hfsp/job_infos/* small_hfsp/job_infos/* ) \
```

means plot two CDF, one for the map times and one for the reduce time

```bash
  -l "\\textsc{Map}" "\\textsc{Reduce}" -L 4 -xl "Task Time" \
```

the options `-l ...` put two entries in the legend: 
Map for the first line and Reduce for the
second. The option `-L 4` says where to put the legend following matplotlib
specification. The option `-xl "Task Time"` say to use "Task Time" as label
of the x-axis.

```bash
  -w 5 -a 12.0 6.0 \
  -o task_times.eps
```

The option `-w 5` says that the lines width must be 5. The option `-a 12.0 6.0`
says that the output figure must have size of x=12 and y=6. Finally the
`-o task_times.eps` says where to save the figure.

## Create your own tool

The output format of the conversion tool is json, so it can be easily imported
using any language. To understand how is written a script that uses the output
of the conversion tool, let's see how `numtasks` is written. Note that the
script calls the main function of `hadoop.log.num_tasks.py`. The source code is:

```python
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
```

The `main` function is the where we load the json of a job and transform it.
The line:

```python
job = json.load(input_file).values()[0]
```

load the job value and put it in a variable called `job`. To understand why
we need `values()[0]` you have to recall the json structure produced by the
converter: the key of the json file is the jobid whereas the value contains
all the informations that we need to get the number of tasks. Now jobs is a
dictionary and contains all the informations that we need.

To print the number of tasks, we need to lookup tasks by task type and then
print the length in output. This is done by:

```python
if args.task_type == 'both':
  print( len(job['maps']),len(job['reduces']) )
else:
  print(len( job[args.task_type] ))
```
