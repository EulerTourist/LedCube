# modulate
# horizontal bars that appear to flow, new one at y=0, with the previous y=0 moved to y=1 and so on 
# bars have centre roughly down the vertical midline, and are varying width, 
# each is a small colour variation from it's neighbours, each changes width 0, 1 or 2 px relative to neighbours
# 
# bars can be horz or vert, later on can move neg or pos direction
# 
# libraries #
# default values #
# classes #
# helper functions #
# 
# functions #
# iterate():
# moveBar()
# makeBar()
# renderBars()
# 
# makeBar()
# select random centre, width and colour constrained with y=1 bar. if len(bars)==0, any will do
# create the bar
# 
# moveBar()
# update the y value of all px in each bar, starting at bottom
# if the y is already at px_per_edge-1 then delete that bar
# 
# renderBars()
# same as drips...
# 
# execute #
# 
# runMods()
# same as drips...
# update globals
# iterate()