import vtk
from vtk.util.colors import tomato

object = vtk.vtkOBJReader()

object.SetFileName('mousebrain_small.obj')
#object.SetFileName('teapot.obj')

objectMapper = vtk.vtkPolyDataMapper()
objectMapper.SetInputConnection(object.GetOutputPort())

objectActor = vtk.vtkActor()
objectActor.SetMapper(objectMapper)
objectActor.GetProperty().SetRepresentationToWireframe();
objectActor.GetProperty().SetColor(1.0, 0.0, 0.0)


plane = vtk.vtkPlaneSource()
plane.SetCenter(0,0,0)
plane.SetNormal(1.0, 0.0, 0.0)
planeMapper = vtk.vtkPolyDataMapper()

transform = vtk.vtkTransform()
transform.Translate(5, 10, 5)
transform.Scale(1, 20, 10)
#transform.RotateWXYZ(45,0,1,0)
transformFilter=vtk.vtkTransformPolyDataFilter()
transformFilter.SetTransform(transform)
transformFilter.SetInputConnection(plane.GetOutputPort())
transformFilter.Update()

planeMapper.SetInputConnection(transformFilter.GetOutputPort())

planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.GetProperty().SetColor(0.5, 0.5, 0.5)


ren = vtk.vtkRenderer()
ren.AddActor(objectActor)
ren.AddActor(planeActor)
ren.SetBackground(0.0, 0.0, 0.0)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('load obj')
renWin.SetSize(1000, 1000)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()


