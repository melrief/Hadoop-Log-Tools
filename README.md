# Hadoop Log Tools

The goal of this project is to provide easy and extensible tools to work with
*Hadoop* logs.

The project has two directories: *Hadoop* that is a *Python* module containing
all the libraries and *bin* that contains *Python* scripts. Each tool has its
own script in the *bin* directory.

The tools provided are divided in three: conversion tools, transformations tools
and visualization tools. The list of those tools is:

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

## Convert job events to json

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
./bin/jobsevents2json logs/ output_dir/
```
