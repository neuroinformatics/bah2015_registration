import vtk

obj_filename = '../obj/mousebrain_small.obj'
obj2_filename = '../obj/slice.obj'
png_filename = 'CD21594.1-Prlr.png'
plot_filename = '../analysis_obj/test.vtk'
#plot_filename = 'mousebrain_small1000.vtk'
poly_filename = '/media/nebula/data/bah/vtk/seg00001.vtk'
plane_scale = 25
plane_ratio = 385. / 614.


###############################################################################
# read plot file
#
plot = vtk.vtkUnstructuredGridReader()
plot.SetFileName(plot_filename)

ball = vtk.vtkSphereSource()
ball.SetRadius(0.12)
ball.SetThetaResolution(12)
ball.SetPhiResolution(12)
ballGlyph = vtk.vtkGlyph3D()
ballGlyph.SetSourceConnection(ball.GetOutputPort())
ballGlyph.SetInputConnection(plot.GetOutputPort())
ballGlyph.SetScaleModeToDataScalingOff()
ballMapper = vtk.vtkPolyDataMapper()
ballMapper.SetInputConnection(ballGlyph.GetOutputPort())

colorTransferFunction = vtk.vtkColorTransferFunction()
colorTransferFunction.AddRGBPoint(5.0 , 0.0, 0.0, 1.0)
colorTransferFunction.AddRGBPoint(10.0, 0.0, 1.0, 1.0)
colorTransferFunction.AddRGBPoint(15.0, 0.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(20.0, 1.0, 1.0, 0.0)
colorTransferFunction.AddRGBPoint(25.0, 1.0, 0.0, 0.0)
colorTransferFunction.AddRGBPoint(30.0, 1.0, 0.0, 1.0)
ballMapper.SetLookupTable(colorTransferFunction)
ballActor = vtk.vtkActor()
ballActor.SetMapper(ballMapper)

arrow = vtk.vtkArrowSource()
arrow.SetTipRadius(0.2)
arrow.SetShaftRadius(0.075)
arrowGlyph = vtk.vtkGlyph3D()
arrowGlyph.SetInputConnection(plot.GetOutputPort())
arrowGlyph.SetSourceConnection(arrow.GetOutputPort())
arrowGlyph.SetScaleFactor(0.4)
arrowGlyph.SetScaleModeToDataScalingOff()
arrowMapper = vtk.vtkPolyDataMapper()
arrowMapper.SetInputConnection(arrowGlyph.GetOutputPort())
arrowMapper.SetLookupTable(colorTransferFunction)
arrowActor = vtk.vtkActor()
arrowActor.SetMapper(arrowMapper)



###############################################################################
# read polydata file
#
poly = vtk.vtkPolyDataReader()
poly.SetFileName(poly_filename)
polyMapper = vtk.vtkPolyDataMapper()
polyMapper.SetInputConnection(poly.GetOutputPort())
polyActor = vtk.vtkActor()
polyActor.SetMapper(polyMapper)
#polyActor.GetProperty().SetRepresentationToWireframe();
#polyActor.GetProperty().SetColor(1.0, 0.2, 0.2)


###############################################################################
# read obj file
#
object = vtk.vtkOBJReader()
object.SetFileName(obj_filename)
objectMapper = vtk.vtkPolyDataMapper()
objectMapper.SetInputConnection(object.GetOutputPort())
objectActor = vtk.vtkActor()
objectActor.SetMapper(objectMapper)
objectActor.GetProperty().SetRepresentationToWireframe();
objectActor.GetProperty().SetColor(1.0, 0.2, 0.2)


###############################################################################
# read second obj file
#
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
object2Actor.GetProperty().SetColor(0.3, 1.0, 0.4)


###############################################################################
# draw plane
#
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


###############################################################################
# draw axis
#
axesActor = vtk.vtkAxesActor()


###############################################################################
# prepare rendering
#
ren = vtk.vtkRenderer()

ren.AddActor(ballActor)
#ren.AddActor(arrowActor)
ren.AddActor(objectActor)
ren.AddActor(object2Actor)
ren.AddActor(planeActor)
ren.AddActor(axesActor)
#ren.AddActor(polyActor)
ren.SetBackground(0.0, 0.0, 0.0)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('Mouse Brain Viewer')
renWin.SetSize(1200, 1200)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()

