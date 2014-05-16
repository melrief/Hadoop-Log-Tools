from itertools import cycle
import matplotlib
from matplotlib.colors import colorConverter as CC

linestyles = cycle(['-',':k','-.','--'])
dotstyles  = cycle(['x','+','o','v','x','.','^','<','>'])

grays = cycle(map(CC.to_rgb,['0.1','0.3','0.2','0.4','0.5','0.6']))

def config_for_paper():
  matplotlib.rc('font', **{'family': 'serif', 'serif': ['Palatino']})
  matplotlib.rc('text', usetex=True)
  matplotlib.rcParams.update({'font.size':22})
