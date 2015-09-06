import vtk
import matplotlib.cm as cm

###############################################################################
# read polydata file
#
segs = []
segs_mapper = []
segs_actor = []
seg_fileformat = '/media/nebula/data/bah/vtk/seg%05d.vtk'

for i in range(1, 39):
    segs.append(vtk.vtkPolyDataReader())
    segs[-1].SetFileName(seg_fileformat % i)
    segs_mapper.append(vtk.vtkPolyDataMapper())
    segs_mapper[-1].SetInputConnection(segs[-1].GetOutputPort())
    segs_actor.append(vtk.vtkActor())
    segs_actor[-1].SetMapper(segs_mapper[-1])
    segs_actor[-1].GetProperty().SetOpacity(0.6)
    color = cm.jet(i/39.)
    segs_actor[-1].GetProperty().SetColor(color[0], color[1], color[2])

#polyActor.GetProperty().SetRepresentationToWireframe();
#polyActor.GetProperty().SetColor(1.0, 0.2, 0.2)


###############################################################################
# draw axis
#
axesActor = vtk.vtkAxesActor()


###############################################################################
# prepare rendering
#
ren = vtk.vtkRenderer()

ren.AddActor(axesActor)
ren.SetBackground(0.0, 0.0, 0.0)

for seg in segs_actor:
    ren.AddActor(seg)


renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
renWin.SetWindowName('Mouse Brain Viewer 2')
renWin.SetSize(1200, 1200)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Initialize()
iren.Start()

