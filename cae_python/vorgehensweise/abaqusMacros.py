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
    session.viewports['Viewport: 1'].setValues(displayedObject=None)
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', 
        sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.rectangle(point1=(0.0, 0.0), point2=(35.0, 25.0))
    s.CircleByCenterPerimeter(center=(10.0, 10.0), point1=(15.0, 10.0))
    mdb.models['Model-1'].sketches.changeKey(fromName='__profile__', 
        toName='Sketch-1')
    s.unsetPrimaryObject()
    mdb.saveAs(
        pathName='C:/Users/p1340760/Desktop/abaqus_scripting/cae_python/test_record')


def Macro2():
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
    pass


def Macro3():
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
    p = mdb.models['Model-1'].parts['Part-1']
    e = p.edges
    edges = e.getSequenceFromMask(mask=('[#1 ]', ), )
    p.Set(edges=edges, name='Set-2')
    cliCommand("""session.journalOptions.setValues(replayGeometry=COORDINATE)""")
    p = mdb.models['Model-1'].parts['Part-1']
    e = p.edges
    edges = e.findAt(((20.0, 10.0, 5.0), ))
    p.Set(edges=edges, name='Set-3')
    mdb.save()
    p = mdb.models['Model-1'].parts['Part-1']
    e = p.edges
    edges = e.findAt(((20.0, 3.4375, 20.0), ), ((20.0, -16.25, 5.0), ), ((20.0, 
        -9.6875, 0.0), ), ((20.0, 10.0, 5.0), ))
    p.Set(edges=edges, name='Set-4')
    cliCommand("""part= mdb.models['Model-1'].parts['Part-1']""")
    cliCommand("""part.edges.getClosest((0,1,0),)""")
    cliCommand("""part.edges.getClosest(((0,1,0),),)""")
    cliCommand("""part.edges[:]""")
    cliCommand("""type(part.edges[:])""")
    cliCommand("""type(part.edges[0])""")
    cliCommand("""part.edges.getClosest(((0,1,0),),)[0]""")
    cliCommand("""part.edges.getClosest(((0,1,0),),)[0][0]""")
    cliCommand("""type(part.edges.getClosest(((0,1,0),),)[0][0])""")
    cliCommand("""type(part.edges.getClosest(((0,1,0),),))""")
    cliCommand("""type(part.edges.findAt(((20.0, 10.0, 5.0), )))""")
    cliCommand("""part.edges.findAt((20.0, 10.0, 5.0), )""")
    cliCommand("""part.edges[0:2]""")
    cliCommand("""session.journalOptions.setValues(replayGeometry=COORDINATE,
    recoverGeometry=COORDINATE)""")
    cliCommand("""part.edges[0:2]""")
    cliCommand("""part.edges[0:1]""")
    cliCommand("""list_edge_pos = [[20.0, 3.4375, 20.0],[20.0, -16.25, 5.0],
    [20.0, -9.6875, 0.0], [20.0, 10.0, 5.0]]""")
    cliCommand("""part.edges.findAt(coordinates=list_edge_pos)""")
    cliCommand("""type(part.edges.findAt(coordinates=list_edge_pos))""")
    cliCommand("""type(part.edges.findAt(list_edge_pos))""")
    cliCommand(
        """part.Set(name='tt', edges=type(part.edges.findAt(coordinates=list_edge_pos)))""")
    cliCommand(
        """part.Set(name='tt', edges=part.edges.findAt(coordinates=list_edge_pos))""")
    p1 = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    cliCommand("""part.edges[0].pointOn()""")
    cliCommand("""part.edges[0].pointOn""")
    cliCommand("""[[i,j.pointOn] for i,j in part.edges]""")
    cliCommand("""[[i,j.pointOn] for i,j in enumerate(part.edges)]""")
    cliCommand(
        """edge_positions = [[j.getSize(),j.pointOn] for i,j in enumerate(part.edges)]""")
    cliCommand("""[i.pointOn for i in part.edges if i.getSize() > 25]""")
    cliCommand(
        """part.Set(name='big_edges', edges=part.edges.findAt(coordinates=big_edges))""")
    cliCommand(
        """# or more direct: Obtain points on edges where edges have a certain size""")
    cliCommand(
        """big_edges = [i.pointOn for i in part.edges if i.getSize() > 25]""")
    cliCommand(
        """part.Set(name='big_edges', edges=part.edges.findAt(coordinates=big_edges))""")
    cliCommand("""big_edges""")
    cliCommand(
        """big_edges = [i.pointOn[0] for i in part.edges if i.getSize() > 25]""")
    cliCommand(
        """part.Set(name='big_edges', edges=part.edges.findAt(coordinates=big_edges))""")
    p1 = mdb.models['Model-1'].parts['Part-1']
    session.viewports['Viewport: 1'].setValues(displayedObject=p1)
    cliCommand("""dir(part.edges[0])""")
