# Lego Model for Abaqus/Python course, MP, 11-2020

from abaqus import *
from abaqusConstants import *
from caeModules import *
import os
import numpy as np

session.journalOptions.setValues(replayGeometry=COORDINATE,
		                         recoverGeometry=COORDINATE)
DIR0 = os.path.abspath('')
TOL = 1e-6

# the functions for the model
# ----------------------------------------------------------------------------------------------

def make_geometry(model,(T,B,H,H0,Hn,Ri,Hup,R),deltaR,mesh_size):
    #
    # draw the sketch
    s = model.ConstrainedSketch(name='brick', sheetSize=200.0)

    s.Line(point1=(0,0), point2=(0,B/2))
    s.Line(point1=(0,B/2), point2=(B/2,B/2))
    s.Line(point1=(B/2,B/2), point2=(0,0))

    # create the part
    p = model.Part(name='Legostein', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    p.BaseSolidExtrude(sketch=s,depth=H+Hn)

    # create sets for cuts
    p.Set(name='top0',faces=p.faces.getByBoundingBox(zMin=H+Hn-TOL))
    p.Set(name='bot0',faces=p.faces.getByBoundingBox(zMax=TOL))
    p.Set(name='top0-yedge', edges=p.edges.findAt(((0,B/4,0),),))

    # cut from top
    cut_top = p.MakeSketchTransform(sketchPlane=p.sets['top0'].faces[0], 
                                    sketchUpEdge=p.edges.findAt((0,B/4,0),), 
                                    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0,0,H+Hn))

    s_top = model.ConstrainedSketch(name='cut-top', sheetSize=200.0, transform=cut_top)
    s_top.CircleByCenterPerimeter(center=(0,0), point1=(R,0))
    s_top.rectangle(point1=(-H,-H), point2=(H,H))

    p.CutExtrude(sketchPlane=p.sets['top0'].faces[0], sketchUpEdge=p.edges.findAt((0,B/4,0),),
                sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s_top, depth=Hn,
                flipExtrudeDirection=OFF)

    # cut from bottom
    cut_bot = p.MakeSketchTransform(sketchPlane=p.sets['bot0'].faces[0], 
                                    sketchUpEdge=p.edges.findAt((0,B/4,0),), 
                                    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0,0,0))

    s_bot = model.ConstrainedSketch(name='cut-bot', sheetSize=200.0, transform=cut_bot)

    s_bot.rectangle(point1=(0,0), point2=(-B/2+T,B/2-T))

    p.CutExtrude(sketchPlane=p.sets['bot0'].faces[0], sketchUpEdge=p.edges.findAt((0,B/4,0),),
                sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s_bot, depth=H-H0,
                flipExtrudeDirection=OFF)

    # cut again from bottom
    cut_bot2 = p.MakeSketchTransform(sketchPlane=p.faces.findAt((10*TOL,20*TOL,H-H0)), 
                                    sketchUpEdge=p.edges.findAt((0,20*TOL,H-H0),), 
                                    sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, origin=(0,0,0))

    s_bot2 = model.ConstrainedSketch(name='cut-bot2', sheetSize=200.0, transform=cut_bot2)

    s_bot2.CircleByCenterPerimeter(center=(0,0), point1=(Ri,0))

    p.CutExtrude(sketchPlane=p.faces.findAt((10*TOL,20*TOL,H-H0)), sketchUpEdge=p.edges.findAt((0,20*TOL,H-H0),),
                sketchPlaneSide=SIDE1, sketchOrientation=RIGHT, sketch=s_bot2, depth=Hup,
                flipExtrudeDirection=OFF)

    # Partitionieren fuer Netz
    dp1 = p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=H-H0)
    dp2 = p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=H)
    dp3 = p.DatumPlaneByPrincipalPlane(principalPlane=XYPLANE, offset=Hn*1.3)

    p.PartitionCellByDatumPlane(datumPlane=p.datums[dp1.id], cells=p.cells)
    p.PartitionCellByDatumPlane(datumPlane=p.datums[dp2.id], cells=p.cells)
    p.PartitionCellByDatumPlane(datumPlane=p.datums[dp3.id], cells=p.cells)

    # Sets und Surfaces
    p.Set(name='all', cells=p.cells)
    p.Set(name='xsym', faces=p.faces.getByBoundingBox(xMax=TOL))
    p.Set(name='xysym', faces=p.faces.findAt(((10*TOL,10*TOL,H+Hn-10*TOL),),
                                            ((B/2-10*TOL,B/2-10*TOL,10*TOL),),
                                            ((B/2-10*TOL,B/2-10*TOL,Hn*1.3+10*TOL),),
                                            ((B/2-10*TOL,B/2-10*TOL,H-10*TOL),)))
    p.Set(name='top', faces=p.faces.getByBoundingBox(zMin=H+Hn-TOL))

    p.Surface(name='contact-bot',side1Faces=p.faces.findAt(((10*TOL,B/2-T,10*TOL),),))
    p.Surface(name='contact-top',side1Faces=p.faces.findAt(((10*TOL,20*TOL,H+Hn),),
                                                        ((sin(pi/8)*R,cos(pi/8)*R,H+Hn-10*TOL),)))

    # Vernetzen
    p.seedPart(size=mesh_size)
    p.generateMesh()
    return p

def make_mat_sections(model,p,(E_abs,nu_abs),R,deltaR):
    # create material & section
    mat = model.Material(name='abs')
    mat.Elastic(table=((E_abs, nu_abs), ))
    # den CTE noch *1.1, damit am Anfang kein Kontakt?!?
    mat.Expansion(type=ORTHOTROPIC, table=((deltaR/R, deltaR/R, 0), ))
    # mat.Expansion(table=((deltaR/R*1.1, ), ))

    model.HomogeneousSolidSection(name='abs', material='abs', thickness=None)
    p.SectionAssignment(region=p.sets['all'], sectionName='abs')

    # Materialorientierungen
    p.MaterialOrientation(region=p.sets['all'], orientationType=GLOBAL, axis=AXIS_1,
                        additionalRotationType=ROTATION_NONE, stackDirection=STACK_1)
    return

def make_loads(model,p):
    # assembly
    a = model.rootAssembly
    inst_top = a.Instance(name='brick-1', part=p, dependent=ON)
    inst_bot = a.Instance(name='brick-2', part=p, dependent=ON)

    # den ersten nach oben verschieben
    a.translate(instanceList=('brick-1', ), vector=(0.0, 0.0, H))

    # define contact
    cp = model.ContactProperty('frictionless')
    cp.TangentialBehavior(formulation=FRICTIONLESS)
    cp.NormalBehavior(pressureOverclosure=HARD, allowSeparation=ON, 
                    constraintEnforcementMethod=DEFAULT)
    #
    # step and hostory output
    step1 = model.StaticStep(name='abkuehlen', previous='Initial', maxNumInc=100,
                            initialInc=1, minInc=1e-05, maxInc=1, nlgeom=ON)
    step2 = model.StaticStep(name='aufwaermen', previous='abkuehlen', maxNumInc=1000,
                            initialInc=0.1, minInc=1e-08, maxInc=0.1, nlgeom=ON)

    model.SurfaceToSurfaceContactStd(name='contact', createStepName='aufwaermen',
                                    master=inst_bot.surfaces['contact-top'],
                                    slave=inst_top.surfaces['contact-bot'],
                                    sliding=FINITE, thickness=ON, interactionProperty='frictionless')

    # history output: interaction
    model.HistoryOutputRequest(name='H-Output-2', createStepName='aufwaermen', 
                            variables=('CFN2', 'CAREA'), interactions=('contact',))

    # boundaries and load
    model.DisplacementBC(name='x_sym-top', createStepName='Initial',
                        region=inst_top.sets['xsym'], u1=0)
    model.DisplacementBC(name='x_sym-bot', createStepName='Initial',
                        region=inst_bot.sets['xsym'], u1=0)
    model.DisplacementBC(name='fix_top', createStepName='Initial',
                        region=inst_top.sets['top'], u3=0)
    model.DisplacementBC(name='fix_bot', createStepName='Initial',
                        region=inst_bot.sets['bot0'], u3=0)

    # eigenes Koordinatensystem fuer xy-Symmetrie
    cs = a.DatumCsysByThreePoints(name='rotated', coordSysType=CARTESIAN, origin=(0,0,0),
                                point1=(1,1,0), point2=(0,1,0))

    model.DisplacementBC(name='xy-sym-top', createStepName='Initial', 
        region=inst_top.sets['xysym'], u2=0, localCsys=a.datums[cs.id])
    model.DisplacementBC(name='xy-sym-bot', createStepName='Initial', 
        region=inst_bot.sets['xysym'], u2=0, localCsys=a.datums[cs.id])

    # temperature load: bottom brick
    t_field = model.Temperature(name='t-change', createStepName='abkuehlen',
                                region=inst_bot.sets['all'], magnitudes=(-1.0, ))
    t_field.setValuesInStep(stepName='aufwaermen', magnitudes=(0.0, ))
    return

def run_job(model,job_name):
    # create and run job
    job = mdb.Job(name=job_name, model='Model-1', type=ANALYSIS,
                resultsFormat=ODB)
    job.submit(consistencyChecking=OFF)
    job.waitForCompletion()
    return

def evaluate_ho(job_name,deltaR):
    #
    vp = session.viewports['Viewport: 1']
    odb = session.openOdb(job_name+'.odb')
    #
    step = odb.steps['aufwaermen']
    # select the history region with the name starting with 'Node '
    hr_rp = [i for i in step.historyRegions.values()
            if i.name.startswith('Node')][0]
        # get contact force
    ho = [i for i in hr_rp.historyOutputs.values() if i.name.startswith('CFN2')][0]
    # ((t,u),...), ((t,rf),...)
    res_f = np.array(ho.data)
    res_f[:,0] *= deltaR
    res_f[:,1] *= -2
    # write u-rf data to file
    np.savetxt(job_name+'_f.dat',res_f,header='deltaR [mm] force [N]')
    return res_f

def evaluate_image(job_name):
    #
    vp = session.viewports['Viewport: 1']
    odb = session.openOdb(job_name+'.odb')
    # Change size of viewport (e.g. 300x200 pixel)
    vp.restore()
    # position of the viwport
    vp.setValues(origin=(50,-50))
    vp.setValues(width=150, height=200)

    # set up in Abaqus Viewer and copied here
    """
    session.View(name='User-1', nearPlane=24.242, farPlane=39.003, width=7.2278,
        height=9.3665, projection=PERSPECTIVE, cameraPosition=(2.5, 5, 31.623),
        cameraUpVector=(0, 1, 0), cameraTarget=(2.5, 5, 0),
        viewOffsetX=-1.3504, viewOffsetY=0.25069, autoFit=OFF)

    # load the defined view
    vp.view.setValues(session.views['User-1'])
    """
    # for a changing plate size, take an automatic front view
    vp.view.setValues(session.views['Front'])

    # view the right filed output
    vp.odbDisplay.display.setValues(plotState=(CONTOURS_ON_DEF, ))
    vp.odbDisplay.setPrimaryVariable(variableLabel='S',
        outputPosition=INTEGRATION_POINT,
        refinement=(INVARIANT, 'Mises'),)

    # print viewport to png file
    session.printOptions.setValues(reduceColors=False, vpDecorations=OFF)
    session.pngOptions.setValues(imageSize=(1500, 2000))
    session.printToFile(fileName=job_name+'_mises', format=PNG,
                canvasObjects=(vp,))

def make_lego_model((T,B,H,H0,Hn,Ri,Hup),(E_abs,nu_abs),deltaR,mesh_size):
    #
    Mdb()                 # reset the model
    model = mdb.models['Model-1']
    #
    # make and check parameters
    R = B/2-T+deltaR
    #
    if Hup > H0 + Hn:
        raise ValueError('Loch oben ist zu tief')
    if Ri > R:
        raise ValueError('Loch oben ist zu grosz')
    #
    p = make_geometry(model,(T,B,H,H0,Hn,Ri,Hup,R),deltaR,mesh_size)
    #
    make_mat_sections(model,p,(E_abs,nu_abs),R,deltaR)
    #
    make_loads(model,p)
    #
    job_name = 'lego-1x1-mesh'+str(mesh_size).replace('.','_')+'_deltaR'+str(int(deltaR*1000))
    run_job(model,job_name)
    #
    res_f = evaluate_ho(job_name,deltaR)
    return res_f

# parameters for geometry, material, load and mesh (N-mm-s)
# ------------------------------------------------------
T = 1.6
B = 7.8
H = 9.6
H0 = 1.75
Hn = 1.7
Ri = 1.3
Hup = 1.75

deltaR = 0.1

E_abs = 2200.     # Young's modulus of ABS (MPa)
nu_abs = 0.35        # Poisson's ratio of ABS (1)
mesh_size = 0.25       # edge length of the mesh (mm)

# build & run the model
make_lego_model((T,B,H,H0,Hn,Ri,Hup),(E_abs,nu_abs),deltaR,0.4)
make_lego_model((T,B,H,H0,Hn,Ri,Hup),(E_abs,nu_abs),deltaR,0.3)
make_lego_model((T,B,H,H0,Hn,Ri,Hup),(E_abs,nu_abs),deltaR,0.2)
make_lego_model((T,B,H,H0,Hn,Ri,Hup),(E_abs,nu_abs),deltaR,0.1)
#make_lego_model((T,B,H,H0,Hn,Ri,Hup),(E_abs,nu_abs),deltaR,mesh_size)

# ----------------------------------------------------------------------------------------------
#raise ValueError('bis hier entwickelt'+'-'*80)
