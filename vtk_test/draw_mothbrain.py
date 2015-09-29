import vtk

obj_filename = '/mnt/data1/StandardBrain/SB/SB256.obj'
obj2_filename = '../obj/slice.obj'
png_filename = 'CD21594.1-Prlr.png'
plot_filename = '../analysis_obj/tmp.vtk'
#plot_filename = 'mousebrain_small1000.vtk'
poly_filename = '/media/nebula/data/bah/vtk/seg00001.vtk'
plane_scale = 25
plane_ratio = 385. / 614.


###############################################################################
# read obj file
#
object = vtk.vtkOBJReader()
object.SetFileName(obj_filename)
objectSmoother = vtk.vtkSmoothPolyDataFilter()
objectSmoother.SetInputConnection(object.GetOutputPort())
objectSmoother.SetNumberOfIterations(100)

objectMapper = vtk.vtkPolyDataMapper()
#objectMapper.SetInputConnection(object.GetOutputPort())
objectMapper.SetInputConnection(objectSmoother.GetOutputPort())
objectActor = vtk.vtkActor()
objectActor.SetMapper(objectMapper)
#objectActor.GetProperty().SetRepresentationToWireframe();
objectActor.GetProperty().SetColor(0.8, 0.8, 0.8)
objectActor.GetProperty().SetOpacity(0.5)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(object.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(1.0, 0.0, 0.0)
outlineActor.GetProperty().SetOpacity(0.4)


###############################################################################
# read second obj file
#
filepos = '/mnt/data1/StandardBrain/SB/LALobj/'
obj_list = ['LAL1.obj','LAL2.obj','LAL3.obj','LAL4.obj','LAL5.obj', 'LAL1_flip.obj', 'LAL2_flip.obj', 'LAL3_flip.obj', 'LAL4_flip.obj', 'LAL5_flip.obj']

lut = vtk.vtkLookupTable()
lut.Build()
scalar_bar = vtk.vtkScalarBarActor()
scalar_bar.SetLookupTable(lut)

objs = []
objs_mapper = []
objs_actor = []
objs_smoother = []

for i, obj_name in enumerate(obj_list):
    objs.append(vtk.vtkOBJReader())
    objs[-1].SetFileName(filepos+obj_name)

    objs_smoother.append(vtk.vtkSmoothPolyDataFilter())
    objs_smoother[-1].SetInputConnection(objs[-1].GetOutputPort())
    objs_smoother[-1].SetNumberOfIterations(50)

    objs_mapper.append(vtk.vtkPolyDataMapper())
    objs_mapper[-1].SetInputConnection(objs_smoother[-1].GetOutputPort())
    objs_mapper[-1].SetLookupTable(lut)
    objs_actor.append(vtk.vtkActor())
    objs_actor[-1].SetMapper(objs_mapper[-1])
    rgb = [0.0, 0.0, 0.0]
    lut.GetColor((i / float(len(obj_list))), rgb)
    objs_actor[-1].GetProperty().SetColor(rgb)
    objs_actor[-1].GetProperty().SetOpacity(0.4)

'''
object2 = vtk.vtkOBJReader()
object2.SetFileName(obj2_filename)
object2Mapper = vtk.vtkPolyDataMapper()
#object2Mapper.SetInputConnection(object2.GetOutputPort())

# transform plane
obj_transform = vtk.vtkTransform()
obj_transform.Translate(5, 23, 13)
obj_transform.Scale(0.02, 0.02, 0.02)
obj_transform.RotateWXYZ(90, 0, 0, 1)
obj_transform.RotateWXYZ(-90, 1, 0, 0)
obj_transform.RotateWXYZ(180, 0, 1, 0)
obj_transformFilter = vtk.vtkTransformPolyDataFilter()
obj_transformFilter.SetTransform(obj_transform)
obj_transformFilter.SetInputConnection(object2.GetOutputPort())
obj_transformFilter.Update()
object2Mapper.SetInputConnection(obj_transformFilter.GetOutputPort())


object2Actor = vtk.vtkActor()
object2Actor.SetMapper(object2Mapper)
#object2Actor.GetProperty().SetRepresentationToWireframe();
object2Actor.GetProperty().SetColor(0.8, 0.8, 0.8)
'''

###############################################################################
# draw axis
#
axesActor = vtk.vtkAxesActor()


###############################################################################
# prepare rendering
#
ren = vtk.vtkRenderer()

ren.AddActor(objectActor)
#ren.AddActor(object2Actor)
ren.AddActor(outlineActor)
ren.AddActor(scalar_bar)
for actor in objs_actor:
    ren.AddActor(actor)

ren.AddActor(axesActor)
ren.SetBackground(.1, .2, .3)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('Silkmoth Brain Viewer')
renWin.SetSize(1400, 1200)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()

