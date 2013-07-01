from itertools import cycle
from matplotlib.colors import colorConverter as CC

linestyles = cycle(['-',':k','-.','--'])

grays = cycle(map(CC.to_rgb,['0.1','0.3','0.2','0.4','0.5','0.6']))
