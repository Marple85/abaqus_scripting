# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__

def Macro1():
    import section
    import regionToolset
    import displayGroupMdbToolset as dgm
    import part
    import material
    import assembly
    import optimization
    import step
    import interaction
    import load
    import mesh
    import job
    import sketch
    import visualization
    import xyPlot
    import displayGroupOdbToolset as dgo
    import connectorBehavior
    s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
    s1.setPrimaryObject(option=STANDALONE)
    s1.ArcByCenterEnds(center=(0.0, 0.0), point1=(5.0, 0.0), point2=(0.0, 5.0), 
        direction=COUNTERCLOCKWISE)
    s1.Line(point1=(5.0, 0.0), point2=(20.0, 0.0))
    s1.HorizontalConstraint(entity=g.findAt((12.5, 0.0)), addUndoState=False)
    s1.PerpendicularConstraint(entity1=g.findAt((3.535534, 3.535534)), 
        entity2=g.findAt((12.5, 0.0)), addUndoState=False)
    s1.Line(point1=(20.0, 0.0), point2=(20.0, 20.0))
    s1.VerticalConstraint(entity=g.findAt((20.0, 10.0)), addUndoState=False)
    s1.PerpendicularConstraint(entity1=g.findAt((12.5, 0.0)), entity2=g.findAt((
        20.0, 10.0)), addUndoState=False)
    s1.Line(point1=(20.0, 20.0), point2=(0.0, 20.0))
    s1.HorizontalConstraint(entity=g.findAt((10.0, 20.0)), addUndoState=False)
    s1.PerpendicularConstraint(entity1=g.findAt((20.0, 10.0)), entity2=g.findAt((
        10.0, 20.0)), addUndoState=False)
    s1.Line(point1=(0.0, 20.0), point2=(0.0, 5.0))
    s1.VerticalConstraint(entity=g.findAt((0.0, 12.5)), addUndoState=False)
    s1.PerpendicularConstraint(entity1=g.findAt((10.0, 20.0)), entity2=g.findAt((
        0.0, 12.5)), addUndoState=False)
    mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', 
        toName='plate')
    s1.unsetPrimaryObject()


