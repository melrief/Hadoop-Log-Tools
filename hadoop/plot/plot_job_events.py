import argparse
from itertools import repeat,cycle
import json
import matplotlib.pyplot as PLT
import sys

colors = cycle(['r','b','g','y','b'])

def mkargparse():
  p = argparse.ArgumentParser()
  p.add_argument('-i','--inputs',help='json files with job informations',
                 nargs='+',required=True)
  p.add_argument('-o','--output',help='output file', required=False)
  return p

def plot_lines(jid,job,y,job_start='s', job_finish='d', map_start='+'
              ,map_finish='x', reduce_start='v', reduce_finish='^'):
  jy,my,ry = y+1,y+0.5,y
  def plot_dot(xs,marker,y,color='b',linestyle=''):
    PLT.plot([long(x)/1000. for x in xs]
            ,[_y for _y in repeat(y,len(xs))]
            ,marker=marker,color=color,linestyle=linestyle)

  color = colors.next()

  plot_dot( [job['submit_time'],job['launch_time'],job['finish_time']],job_start,jy,color=color,linestyle='-')

  map_tasks = job['maps'].values()
  plot_dot( [m['start_time'] for m in map_tasks],map_start,my,color=color )
  plot_dot( [m['finish_time'] for m in map_tasks],map_finish,my,color=color )

  reduce_tasks = job['reduces'].values()
  plot_dot( [r['start_time'] for r in reduce_tasks],reduce_start,ry,color=color )
  plot_dot( [r['finish_time'] for r in reduce_tasks],reduce_finish,ry,color=color )

  return jy,my,ry

def main():
  args = mkargparse().parse_args(sys.argv[1:])
  jobs = {}
  for input_file in args.inputs:
    with open(input_file,'rt') as fp:
      d = json.load(fp)
      jobs[d.keys()[0]] = d.values()[0]
  
  yticks = []
  def sort_by_launch_time((jid1,job1),(jid2,job2)):
    return cmp(job1['launch_time'],job2['launch_time'])
  for i,(jid,job) in enumerate(sorted(jobs.items(),cmp=sort_by_launch_time)):
    #print job
    jy,my,ry = plot_lines(jid,job,0.5+i*2)
    yticks.extend([jy,my,ry])
  PLT.ylim(0,yticks[-1]+1)
  PLT.yticks(yticks,
             [k for key in jobs.keys() for k in [key+' job'
                                                ,key+' map'
                                                ,key+' reduce']])
  if args.output:
    PLT.savefig(args.output,format='eps')
  else:
    PLT.show()


if __name__=='__main__':
  main()
