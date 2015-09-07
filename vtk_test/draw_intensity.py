import vtk
import matplotlib.cm as cm
import sys

def draw_scene(int_filename, color_mode=0):
    ###############################################################################
    # read polydata file
    #
    offscreen = False
    draw_axes = False
    
    segs = []
    segs_mapper = []
    segs_actor = []
    seg_fileformat = '/media/nebula/data/bah/vtk/seg%05d.vtk'
    #seg_fileformat = '/media/nebula/data/bah/vtk/seg%05d.vtk'
    #int_filename = '../matching_area/result.txt'

    int_data = {}
    int_data_sorted = {}
    
    fp = open(int_filename, 'r')
    lines = fp.readlines()
    for line in lines:
        splited = line.strip().split(',')
        int_data[int(splited[0])] = float(splited[1])
        
        #print int_data
        

    for i in range(1, 39):
        segs.append(vtk.vtkPolyDataReader())
        segs[-1].SetFileName(seg_fileformat % i)
        segs_mapper.append(vtk.vtkPolyDataMapper())
        segs_mapper[-1].SetInputConnection(segs[-1].GetOutputPort())
        segs_actor.append(vtk.vtkActor())
        segs_actor[-1].SetMapper(segs_mapper[-1])
        segs_actor[-1].GetProperty().SetOpacity(0.1)
        #color = cm.jet(i/39.)
        #segs_actor[-1].GetProperty().SetColor(color[0], color[1], color[2])


    i = 0
    for k, v in sorted(int_data.items(), key=lambda x:x[1], reverse=True):
        if i < 6:
            segs_actor[k-1].GetProperty().SetOpacity(0.8)
            if color_mode == 0:
                color = ((v-40) / 20.)
                segs_actor[k-1].GetProperty().SetColor(color, 0, 0)
            elif color_mode == 1:
                color = cm.jet(((v-40) / 60.))
                segs_actor[k-1].GetProperty().SetColor(color[0], color[1], color[2])

            print k, v, color
            i += 1
            #int_data_sorted[k] = v
        #print 'Lank %5d : %d (%d)' % (i, k, v)

    ###############################################################################
    # draw axis
    #
    if draw_axes:
        axesActor = vtk.vtkAxesActor()


    ###############################################################################
    # prepare rendering
    #
    ren = vtk.vtkRenderer()
    ren.SetBackground(0.0, 0.0, 0.0)

    if draw_axes:
        ren.AddActor(axesActor)

    for seg in segs_actor:
        ren.AddActor(seg)

    renWin = vtk.vtkRenderWindow()
    if offscreen:
        renWin.SetOffScreenRendering(True)
    renWin.AddRenderer(ren)
    renWin.SetWindowName('Mouse Brain Viewer 2')
    renWin.SetSize(1200, 1200)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Initialize()

    print 'start'

    iren.Start()

    w2if = vtk.vtkWindowToImageFilter()
    w2if.SetInput(renWin)
    w2if.Update()
    writer = vtk.vtkPNGWriter()
    writer.SetFileName('screen.png')
    writer.SetInput(w2if.GetOutput())
    writer.Write()

    print 'finish'

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    filename = ''

    if(argc >= 2):
        filename = argvs[1]
    else:
        filename = '../matching_area/result.txt'
    
    if(argc >= 3):
        color_mode = int(argvs[2])
    else:
        color_mode = 0

    draw_scene(filename, color_mode)
