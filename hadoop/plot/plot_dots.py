#!/usr/bin/env python
from __future__ import division

import argparse
import matplotlib.pyplot as PLT
import os
import sys

from libplot import config_for_paper,dotstyles,linestyles

def parse_args(args):
  p = argparse.ArgumentParser()
  p.add_argument('-x', '--x-label', default=None, required=False,
                 metavar='string',  help='x label')
  p.add_argument('-y', '--y-label', default=None, required=False,
                 metavar='string',  help='y label')
  p.add_argument('-xt', '--x-type', default=None, required=False,
                 choices=[None,'time'])
  p.add_argument('-T', '--x-ticks', default=None, required=False,
                 metavar='x:string',nargs='+'
                ,help='x ticks composed by a number and the string that ' +\
                      'should appear in that place')
  p.add_argument('-n','--normalize',required=False,action='store_true')
  p.add_argument('-z','--zero',required=False,action='store_true')
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
  p.add_argument('-s', '--line-style', required=False, default=None
                     , help='line style')
  p.add_argument('-S', '--style',required=False,default="line"
                     ,choices=['line','dots','both'])
  p.add_argument('-X', '--x-scale',required=False,default='normal'
                     , choices=['normal','semilog']
                     , help='scale of the x axis')
  p.add_argument('-Y', '--y-scale',required=False,default='normal'
                     , choices=['normal','semilog']
                     , help='scale of the y axis')
  p.add_argument('-p', '--for-paper', required=False, action='store_true'
                     , default=False, help="Use fonts for paper")
  return p.parse_args(args)

def main():
  args = parse_args(sys.argv[1:])

  # fonts
  if args.for_paper:
    config_for_paper()

  if not args.normalize and args.zero:
    sys.exit('-z/--zero works only with -n/--normalize')

  if args.x_label:
      PLT.xlabel(args.x_label)

  lines = []
  for input_file in args.input_files:
    xs,ys=[],[]
    for line in input_file.read().split(os.linesep):
      ws = [float(w) for w in line.split()]
      if len(ws) >= 2:
        xs.append(ws[0])
        ys.append(ws[1])
    lines.append( (xs,ys) )

  if args.normalize:
    first_x = min(lines[0][0])
    new_lines = []
    if args.zero:
      for line in lines:
        diff = min(line[0])
        norm_xs = [x - diff for x in line[0]]
        new_lines.append( (norm_xs,line[1]) )
    else:
      new_lines.append(lines[0])
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

  if args.x_ticks:
    txs,tstrs = [],[]
    for e in args.x_ticks:
      splitted = e.split(':')
      if len(splitted) == 1:
        txs.append(float(e))
        tstrs.append(e)
      else:
        txs.append(float(splitted[0]))
        tstrs.append(splitted[1])
    PLT.xticks(txs,tstrs)

  if args.axes_size:
    PLT.figure(figsize=args.axes_size)
  PLT.grid()
  PLT.gcf().subplots_adjust(bottom=0.15)

  plotter = PLT.plot
  if args.x_scale == 'semilog' and args.y_scale == 'semilog':
    sys.stderr.write('using loglog' + os.linesep)
    plotter = PLT.loglog
  elif args.x_scale == 'semilog':
    sys.stderr.write('using semilogx' + os.linesep)
    plotter = PLT.semilogx
  elif args.y_scale == 'semilog':
    sys.stderr.write('using semilogy' + os.linesep)
    plotter = PLT.semilogy

  for line in lines:
    linestyle = args.line_style if args.line_style else linestyles.next()
    marker = dotstyles.next()
    if args.style == 'line':
      plotter(line[0],line[1],linestyle,linewidth=args.line_width)
    elif args.style == 'dots':
      plotter(line[0],line[1],' ',marker=marker)
    else:
      plotter(line[0] # if args.x_type == None else range(len(line[0]))
             ,line[1]
             ,linestyle
             ,marker=marker
             ,linewidth=args.line_width
             )
    #    if args.x_type:
    #      len_line = len(line[0])
    #      n_ticks = 10
    #      steps = int(len_line/n_ticks)
    #      print(zip(range(0,n_ticks),line[0][::steps]))
    #      PLT.xticks(range(0,n_ticks,steps),line[0][::steps])

  PLT.gca().xaxis.set_major_formatter(PLT.ScalarFormatter())
  PLT.gca().yaxis.set_major_formatter(PLT.ScalarFormatter())

  # fix 0 points overlap by padding
  PLT.gca().xaxis.set_tick_params(pad=10)
  PLT.gca().yaxis.set_tick_params(pad=10)

  if args.x_label:
    PLT.xlabel(args.x_label)
  if args.y_label:
    PLT.ylabel(args.y_label)
  if args.legend and len(args.legend) == len(args.input_files):
    PLT.legend(args.legend,loc=args.legend_loc)
  if args.output_file:
    PLT.savefig(args.output_file,format='pdf',bbox_inches='tight',dpi=100)
  else:
    PLT.show()

if __name__=='__main__':
  main()
