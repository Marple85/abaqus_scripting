# plate with hole in middle, 2D, MP 09-2020

from abaqus import *
from abaqusConstants import *
from caeModules import *
import os

session.journalOptions.setValues(replayGeometry=COORDINATE,
		                 recoverGeometry=COORDINATE)
DIR0 = os.path.abspath('')
TOL = 1e-6

# parameters for geometry, material, load and mesh (N-mm-s)
# ------------------------------------------------------
b = 15.               # width of the plate (mm)
h = 20.               # height of the plate (mm)
radius = 4.5          # radius of the hole (mm)

uy = 0.08             # vertical displacement of the top (mm)

E_steel = 210000.     # Young's modulus of steel (MPa)
nu_steel = 0.3        # Poisson's ratio of steel (1)
sy_steel = 500.       # yield stress of steel (MPa)

mesh_size = 2.        # edge length of the mesh (mm)

if radius >= b/2:
    raise ValueError('width b too small for the hole radius')
if radius >= h/2:
    raise ValueError('height h too small for the hole radius')

# create the model
# -------------------------------------------------------

Mdb()                 # reset the model
model = mdb.models['Model-1']

# create a sketch
s = model.ConstrainedSketch(name='plate', sheetSize=200.0)

# draw the arc for the hole
s.ArcByCenterEnds(center=(0.0, 0.0), point1=(radius, 0.0), point2=(0.0, radius), 
                  direction=COUNTERCLOCKWISE)
# draw lines
s.Line(point1=(radius, 0.0), point2=(b/2, 0.0))
s.Line(point1=(b/2, 0.0), point2=(b/2, h/2))
s.Line(point1=(b/2, h/2), point2=(0.0, h/2))
s.Line(point1=(0.0, h/2), point2=(0.0, radius))
# print sketch to image
s.setPrimaryObject(option=STANDALONE)
session.printToFile(fileName='plate', format=PNG,
                    canvasObjects=(session.viewports['Viewport: 1'], ))
# go back to model from sketch
s.unsetPrimaryObject()