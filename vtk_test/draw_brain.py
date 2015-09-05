import vtk

obj_filename = 'mousebrain_small.obj'
png_filename = 'CD21594.1-Prlr.png'
plane_scale = 25
plane_ratio = 385. / 614.

# read obj file
object = vtk.vtkOBJReader()
object.SetFileName(obj_filename)
objectMapper = vtk.vtkPolyDataMapper()
objectMapper.SetInputConnection(object.GetOutputPort())

objectActor = vtk.vtkActor()
objectActor.SetMapper(objectMapper)
objectActor.GetProperty().SetRepresentationToWireframe();
objectActor.GetProperty().SetColor(1.0, 0.0, 0.0)

# draw plane
plane = vtk.vtkPlaneSource()
plane.SetCenter(0,0,0)
plane.SetNormal(1.0, 0.0, 0.0)
#planeMapper = vtk.vtkPolyDataMapper()


# build texture for plane
reader = vtk.vtkPNGReader()
reader.SetFileName(png_filename)
texture = vtk.vtkTexture()
texture.SetInputConnection(reader.GetOutputPort())

map_to_plane = vtk.vtkTextureMapToPlane()
map_to_plane.SetInputConnection(plane.GetOutputPort())
#map_to_plane.PreventSeamOn() 
planeMapper = vtk.vtkPolyDataMapper()
planeMapper.SetInputConnection(map_to_plane.GetOutputPort()) 


# transform plane
transform = vtk.vtkTransform()
transform.Translate(5, 10, 5)
transform.Scale(1, plane_scale, plane_scale * plane_ratio)
#transform.RotateWXYZ(45,0,1,0)
transformFilter = vtk.vtkTransformPolyDataFilter()
transformFilter.SetTransform(transform)
transformFilter.SetInputConnection(plane.GetOutputPort())
transformFilter.Update()
planeMapper.SetInputConnection(transformFilter.GetOutputPort())


planeActor = vtk.vtkActor()
planeActor.SetMapper(planeMapper)
planeActor.SetTexture(texture)
#planeActor.GetProperty().SetColor(0.5, 0.5, 0.5)


# prepare rendering
ren = vtk.vtkRenderer()
ren.AddActor(objectActor)
ren.AddActor(planeActor)
ren.SetBackground(0.0, 0.0, 0.0)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('Mouse Brain Viewer')
renWin.SetSize(1200, 1200)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()

