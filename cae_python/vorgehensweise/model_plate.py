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

s.rectangle(point1=(0.0, 0.0), point2=(35.0, 25.0))
s.CircleByCenterPerimeter(center=(10.0, 10.0), point1=(15.0, 10.0))

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

####################################################################################
# SELECTING IN ABAQUS
####################################################################################

# default recording in Abaqus: set from edge
part.Set(edges=part.edges.getSequenceFromMask(('[#400 ]',),), name='Set-1')

# rather strange way of selecting: not scriptable!
part.edges.getSequenceFromMask(('[#400 ]',),)

# after setting journalOptions (COORDINATES)
session.journalOptions.setValues(replayGeometry=COORDINATE,
        		                 recoverGeometry=COORDINATE)

part.edges.findAt(((20.0, 10.0, 5.0), ))

# Why all thoses brackets?!? objects in Abaqus:
>>> type(part.edges[:])
<type 'Sequence'>
>>> type(part.edges[0])
<type 'Edge'>

# --> in sets and surfaces we need a sequence, not a single edge, face, ...
# also not a list of edges!!

# documentation of set: http://130.149.89.49:2080/v2016/books/ker/pt01ch45pyo04.html#ker-set-set-pyc

# for creating sets (boolean): http://130.149.89.49:2080/v2016/books/ker/pt01ch45pyo04.html#ker-set-set2-pyc

part.edges[0]   # single edge
part.edges[0:2] # first two edges

i_edge = 2
part.edges[i_edge:i_edge+1]     # edge array but just with a single edge in it


# single edge:
part.edges.findAt((20.0, 10.0, 5.0), )

# great, just replace coordinates by variables.
# But attention: if 2 or more entities are possible, you just get one of them (random)

# however, for more edges it gets unpractical
part.edges.findAt(((20.0, 3.4375, 20.0), ), ((20.0, -16.25, 5.0), ),
                  ((20.0, -9.6875, 0.0), ), ((20.0, 10.0, 5.0), ))

# with list or numpy array:
list_edge_pos = [[20.0, 3.4375, 20.0],[20.0, -16.25, 5.0],
                  [20.0, -9.6875, 0.0], [20.0, 10.0, 5.0]]

part.edges.findAt(coordinates=list_edge_pos)

# manually choosing edges with certain positions:

part.edges[0].pointOn

# in a loop, we could thus choose all edges with certain coordinates
edge_positions = [[i,j.pointOn] for i,j in enumerate(part.edges)]

# or more direct: Obtain points on edges where edges have a certain size
big_edges = [i.pointOn[0] for i in part.edges if i.getSize() > 25]

part.Set(name='big_edges', edges=part.edges.findAt(coordinates=big_edges))

# other options for selecting edges:
>>> dir(part.edges[0])
['__class__', '__cmp__', '__delattr__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'featureName', 'getAdjacentEdges', 'getCurvature', 'getEdgesByEdgeAngle', 'getElements', 'getFaces', 'getNodes', 'getRadius', 'getSize', 'getVertices', 'index', 'instanceName', 'isReferenceRep', 'isTangentFlipped', 'pointOn']

# getByBoundingBox

# boolean options

# Regions: just use the syntax of the recorded code!

# if we want to have all of them, that's easy
part.edges[:]

# DODO
# getByBoundingBox
# all entities there are...
