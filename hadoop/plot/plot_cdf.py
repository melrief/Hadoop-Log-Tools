#!/usr/bin/env python

import argparse
import matplotlib.pyplot as PLT
import numpy as N
import os
from os.path import basename
import scipy.stats as SS
import sys

from libplot import config_for_paper,linestyles

distr = { 'lognorm' : SS.lognorm }

def makeCDF(ls):
    if not ls:
        return None
    xs = sorted(ls)
    ys = N.linspace( 1/len(xs), 1, len(xs) )
    #print zip(xs,ys)
    return xs,ys

def mk_parser():
    p = argparse.ArgumentParser()
    p.add_argument('--xlim', default=None, required=False, nargs=2,
                   help='passed to pyplot.xlim')
    p.add_argument('-X', '--x-ticks', default=None, required=False,
                   metavar='x:string',nargs='+'
                  ,help='x ticks composed by a number and the string that ' +\
                        'should appear in that place')
    p.add_argument('-x', '--x-scale',required=False,default='semilogx'
                       , choices=['normal','semilogx']
                       , help='scale of the x axis')
    p.add_argument('-xl', '--x-label', default=None, required=False,
                   metavar='string',help='string used as x label')
    p.add_argument('-i', '--input-files', default=None, nargs="+",
                   help='input file or empty (stdin)',metavar='INPUT_FILE')
    p.add_argument('-l', '--legend', default=[], required=False, nargs="+",
                   help='strings to use as legend, one for each line')
    p.add_argument('-L','--legend-loc',required=False,default=1,type=int,
                  choices=range(1,10)
                 ,help='location of the legend according to pyplot')
    p.add_argument('-o', '--output', required=False, help='output file')
    p.add_argument('-s', '--line-style', required=False, default=None
                       , help='line style')
    p.add_argument('-d', '--plot-distr',required=False,nargs='+'
                       , metavar='distr:p1:p2:...'
                       , help='used to plot one or more distributions lines'
                            + ' with the given name and the given parameters')
    p.add_argument('-w', '--line-width',required=False,default=1,type=float
                       , help='width of the line to plot')
    p.add_argument('-a', '--axes-size', required=False, nargs=2, type=float
                       , default=None, help='resize the axes of the plot to ' +
                                            'the given sizes')
    p.add_argument('-p', '--for-paper', required=False, action='store_true'
                       , default=False, help="Use fonts for paper")
    return p

def main():
    p = mk_parser()
    args = p.parse_args(sys.argv[1:])
    
    # fonts
    if args.for_paper:
      config_for_paper()

    lss = []
    legend_labels = []
    if args.input_files is None:
        lss.append([float(l) for l in sys.stdin.read().split(os.linesep)
                             if not l == ''])
    else:
        for input_file in args.input_files:
            legend_labels.append(basename(input_file))
            with open(input_file, 'rt') as f:
                lss.append([float(l) 
                            for l in f.read().split(os.linesep) 
                            if not l == ''])
    if args.axes_size:
      PLT.figure(figsize=args.axes_size)
    PLT.grid()
    PLT.gcf().subplots_adjust(bottom=0.15)

    if args.x_label:
        PLT.xlabel(args.x_label)
    PLT.ylabel('ECDF')

    plotter = PLT.plot
    if args.x_scale == 'semilogx':
      sys.stderr.write('plot: using semilogx' + os.linesep)
      plotter = PLT.semilogx

    lines = []
    for ls in lss:
        xsysOrNone = makeCDF(ls)
        if not xsysOrNone:
          sys.stderr.write('error: cannot plot empty CDF')
          continue
        xs,ys = xsysOrNone
        style = args.line_style if args.line_style else linestyles.next()
        p, = plotter(xs, ys, style, linewidth=args.line_width, aa=True)
        if args.x_scale == 'semilogx':
          PLT.gca().xaxis.set_major_formatter(PLT.ScalarFormatter())
        lines.append(p)

    # fix 0 points overlap by padding
    PLT.gca().xaxis.set_tick_params(pad=10)
    PLT.gca().yaxis.set_tick_params(pad=10)

    if args.plot_distr:
      for raw_distr in args.plot_distr:
        splitted = raw_distr.split(':')
        distr_name = splitted[0]
        distr_args = map(N.float,splitted[1:])
        d = distr[distr_name](*distr_args)
        #d = distr[distr_name](distr_args[0],mean=distr_args[1])
        xs = N.linspace(0,10)
        style = args.line_style if args.line_style else linestyles.next()
        p, = plotter(xs,d.cdf(xs),style, linewidth=args.line_width, aa=True)
        lines.append(p)

   # fontP = MPL.font_manager.FontProperties()
   # fontP.set_size('x-small')
    if args.legend:
      if len(args.legend) != len(legend_labels):
        sys.exit('Input labels {} length {}'.format(args.legend
                                                   ,len(args.legend)) +
                 'isn\'t equal to the ' +
                 'number of lines {}'.format(len(legend_labels)))
      legends = args.legend
      if args.plot_distr:
        for raw_distr in args.plot_distr:
          legends.append(raw_distr.split(':')[0])
      PLT.legend(lines, legends, loc=args.legend_loc)

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

    if args.xlim:
      PLT.xlim(map(float,args.xlim))

    if args.output:
        PLT.savefig(args.output,bbox_inches='tight',dpi=100)
    else:
        PLT.show()


if __name__=='__main__':
    main()
