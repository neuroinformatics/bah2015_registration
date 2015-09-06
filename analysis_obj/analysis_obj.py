# -*- coding: utf-8 -*-
usage = \
'''
$ python analysis_obj.py [input:obj filename] [output:vtk filename]
'''

import sys
import random

vtk_header = '''\
# vtk DataFile Version 1.0
Unstructured Grid Example
ASCII

DATASET UNSTRUCTURED_GRID
POINTS %d float

'''


def read_obj_file(filename):
    points = []

    f = open(filename, 'r')
    line = f.readline()
    while line:
        if line[0] == 'v':
            splited = line.split(' ')
            points.append([float(splited[1]), float(splited[2]), float(splited[3])])

        line = f.readline()
    f.close()

    #print len(points)
    return points

def write_vtk_file(filename, points):
    f = open(filename, 'w')
    f.write(vtk_header % len(points))
    for x in points:
        f.write('%f %f %f\n' % (x[0], x[1], x[2]))
    f.close()



if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc != 3:
        print 'error : input filename.'
        print usage
        quit()

    points = read_obj_file(argvs[1])
    sampled_points = random.sample(points, 1000)
    #print sampled_points
    write_vtk_file(argvs[2], sampled_points)

