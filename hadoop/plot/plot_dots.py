#!/usr/bin/env python
from __future__ import division

import argparse
import matplotlib.pyplot as PLT
import os
import sys

from libplot import linestyles

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-x', '--x-label', default=None, required=False,
                 metavar='string',  help='x label')
  p.add_argument('-y', '--y-label', default=None, required=False,
                 metavar='string',  help='y label')
  p.add_argument('-xt', '--x-type', default=None, required=False,
                 choices=[None,'time'])
  p.add_argument('-n','--normalize',required=False,action='store_true')
  p.add_argument('-i','--input-files',required=False, nargs='+'
                     ,default=[sys.stdin]
                     ,metavar='INPUT_FILE',type=argparse.FileType('rt')
                     ,help='file where each line is a pair x y separated' + 
                           ' by space')
  p.add_argument('-l','--legend',required=False,nargs='+')
  p.add_argument('-L','--legend-loc',required=False,default=1,type=int,
                choices=range(1,10))
  p.add_argument('-o','--output-file',required=False)
  p.add_argument('-w', '--line-width',required=False,default=1,type=float)
  p.add_argument('-a', '--axes-size', required=False, nargs=2, type=float
                     , default=None)
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])
  lines = []
  for input_file in args.input_files:
    xs,ys=[],[]
    for line in input_file.read().split(os.linesep):
      ws = [int(w) for w in line.split()]
      if len(ws) >= 2:
        xs.append(ws[0])
        ys.append(ws[1])
    lines.append( (xs,ys) )

  if args.normalize:
    first_x = min(lines[0][0])
    new_lines = [lines[0]]
    for line in lines[1:]:
      diff = min(line[0]) - first_x
      norm_xs = [x - diff for x in line[0]]
      new_lines.append( (norm_xs,line[1]) )
    lines = new_lines

  if args.x_type:
    if args.x_type == 'time':
      first_x = min(lines[0][0])/1000.
      new_lines = []
      for (xs,ys) in lines:
        new_xs = []
        for x in xs:
          curr_x = x/1000
          seconds = (curr_x - first_x)/3600
          new_xs.append( seconds )
        new_lines.append( (new_xs,ys) )
      lines = new_lines

  if args.axes_size:
    PLT.figure(figsize=args.axes_size)
  PLT.grid()
  PLT.gcf().subplots_adjust(bottom=0.15)

  for line in lines:
    linestyle = linestyles.next()
    PLT.plot(line[0] # if args.x_type == None else range(len(line[0]))
            ,line[1]
            ,linestyle
            ,linewidth=args.line_width
            )
    #    if args.x_type:
    #      len_line = len(line[0])
    #      n_ticks = 10
    #      steps = int(len_line/n_ticks)
    #      print(zip(range(0,n_ticks),line[0][::steps]))
    #      PLT.xticks(range(0,n_ticks,steps),line[0][::steps])

  if args.x_label:
    PLT.xlabel(args.x_label)
  if args.y_label:
    PLT.ylabel(args.y_label)
  if args.legend and len(args.legend) == len(args.input_files):
    PLT.legend(args.legend,loc=args.legend_loc)
  if args.output_file:
    PLT.savefig(args.output_file,format='eps',bbox_inches='tight',dpi=100)
  else:
    PLT.show()

if __name__=='__main__':
  main()
