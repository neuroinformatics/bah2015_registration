import vtk



###############################################################################
# read obj file
#
obj_filename = '/mnt/data1/StandardBrain/SB/SB256.obj'
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
objectActor.GetProperty().SetColor(0.5, 0.5, 0.5)
objectActor.GetProperty().SetOpacity(0.5)

outline = vtk.vtkOutlineFilter()
outline.SetInputConnection(object.GetOutputPort())
outlineMapper = vtk.vtkPolyDataMapper()
outlineMapper.SetInputConnection(outline.GetOutputPort())
outlineActor = vtk.vtkActor()
outlineActor.SetMapper(outlineMapper)
outlineActor.GetProperty().SetColor(1.0, 0.0, 0.0)
outlineActor.GetProperty().SetOpacity(0.2)


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

neuronpos = '/mnt/data1/StandardBrain/highres/'
neuron_list = ['0004.obj', '0004flip.obj', '0005.obj', '0005flip.obj', '0008.obj', '0008flip.obj', '0009.obj', '0009flip.obj', '0012.obj', '0012flip.obj', '0017.obj', '0017flip.obj', '0019.obj', '0019flip.obj', '0021.obj', '0021flip.obj', '0655.obj', '0655flip.obj', '0661.obj', '0661flip.obj']
neurons = []
neurons_mapper = []
neurons_actor = []
neurons_smoother = []
for i, neuron_name in enumerate(neuron_list):
    neurons.append(vtk.vtkOBJReader())
    neurons[-1].SetFileName(neuronpos+neuron_name)

    neurons_smoother.append(vtk.vtkSmoothPolyDataFilter())
    neurons_smoother[-1].SetInputConnection(neurons[-1].GetOutputPort())
    neurons_smoother[-1].SetNumberOfIterations(50)

    neurons_mapper.append(vtk.vtkPolyDataMapper())
    neurons_mapper[-1].SetInputConnection(neurons_smoother[-1].GetOutputPort())
    neurons_mapper[-1].SetLookupTable(lut)
    neurons_actor.append(vtk.vtkActor())
    neurons_actor[-1].SetMapper(neurons_mapper[-1])
    rgb = [0.0, 0.0, 0.0]
    lut.GetColor((i / float(len(neuron_list))), rgb)
    #neurons_actor[-1].GetProperty().SetColor(1.0, 1.0, 0.5)
    neurons_actor[-1].GetProperty().SetColor(rgb)
    neurons_actor[-1].GetProperty().SetOpacity(0.9)


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

#for actor in objs_actor:
#    ren.AddActor(actor)
for actor in neurons_actor:
    ren.AddActor(actor)

ren.AddActor(axesActor)
ren.SetBackground(.0, .0, .1)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('Silkmoth Brain Viewer')
renWin.SetSize(1400, 1200)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()

