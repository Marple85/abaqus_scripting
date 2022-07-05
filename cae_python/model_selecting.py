# Exercise for selecting: Plate with hole

from abaqus import *
from abaqusConstants import *
from caeModules import *
session.journalOptions.setValues(replayGeometry=COORDINATE,
		                         recoverGeometry=COORDINATE)

TOL = 1e-6

# geometry parameters
# --------------------------------
b = 20.
h = 20.
radius = 5. 

# Build up the part (N-mm-s)
# ------------------------------------------------------

Mdb()
m = mdb.models['Model-1']

# draw the sketch
s = m.ConstrainedSketch(name='plate', sheetSize=200.0)
s.ArcByCenterEnds(center=(0,0), point1=(0,radius), point2=(radius,0),
                direction=CLOCKWISE)
s.Line(point1=(radius,0), point2=(b/2.,0))
s.Line(point1=(b/2.,0), point2=(b/2.,h/2.))
s.Line(point1=(b/2.,h/2.), point2=(0,h/2.))
s.Line(point1=(0,radius), point2=(0,h/2.))

# create the part
p = m.Part(name='plate', dimensionality=TWO_D_PLANAR, type=DEFORMABLE_BODY)
p.BaseShell(sketch=s) 

# create sets for the part
# ...
