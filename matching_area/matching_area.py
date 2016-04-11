# -*- coding: utf-8 -*-

import sys
from PIL import Image
from PIL import ImageStat


def matching_ish(labeled_filename, ish_filename, output_filename, slice):
    N_AREA = 40
    threshold = 10
    volume_threshold = 10
    volume_bias = 40

    labeled_count = {}
    labeled_volume = {}
    result_value = {}
    result_value_max = {}
    result_value_per_vol = {}


    labeled = Image.open(labeled_filename)
    labeled.seek(slice)
    labeled_data = labeled.getdata()

    ish = Image.open(ish_filename)
    ish_data = ish.getdata()

    for value in range(N_AREA):
        labeled_volume[value] = 0
        result_value[value] = 0
        result_value_max[value] = 0
        result_value_per_vol[value] = 0
    


    # calculate volume of each area
    for value in labeled_data:
        value = int(value)
        labeled_volume[value] += 1

    # summation value of each area
    for (ish_val, labeled_val) in zip(ish_data, labeled_data):
        if(int(labeled_val)!=0 and ish_val):
            #value = 256 - (ish_val[0] + ish_val[1] + ish_val[2]) / 3
            #value = ish_val[2]*2 - ish_val[0] - ish_val[1];
            value = ish_val[2]*2 - (ish_val[0] + ish_val[1]) * 0.9;

            if  value > threshold:
                result_value[int(labeled_val)] += value

                if value > result_value_max[int(labeled_val)]:
                    result_value_max[int(labeled_val)] = value

    # normalize value by volume
    for i in range(N_AREA):
        if labeled_volume[i] > volume_threshold:
            result_value_per_vol[i] = float(result_value[i]) / float(labeled_volume[i] + volume_bias)
        else:
            result_value_per_vol[i] = 0

    # write to file
    fp = open(output_filename, 'w')
    lines = []
    #for (k, v) in result_value.items():
    for (k, v) in result_value_per_vol.items():
        lines.append('%d, %6.1f\n' % (k, v))
    fp.writelines(lines)
    fp.close()

    
    # show result
    i = 1
    for k, v in sorted(result_value_per_vol.items(), key=lambda x:x[1], reverse=True):
        print 'Rank %3d : Area %3d (normal value = %6.1f, value = %6d, volume = %6d)' % (i, k, v, result_value[k], labeled_volume[k])
        i += 1

    return result_value


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    labeled_filename = '/mnt/data1/bah2015/reslice_labeled.tif'

    if argc >= 2:
        ish_filename = argvs[1]
    else:
        #ish_filename = '/media/nebula/data/bah/CD00050.1-VimRegistered.tif'
        ish_filename = '/mnt/data1/bah2015/registration_Affine/CD02689.1-Dtl.tif'

    if argc >= 3:
        out_filename = argvs[2]
    else:
        out_filename = './result/CD02689.1-Dtl.txt'

    if argc >= 4:
        slice = int(argvs[3])
    else:
        slice = 112

    #analysis_tif(labeled_filename, ish_filename, out_filename, slice)
    #regen_segfile(labeled_filename)
    print ish_filename
    matching_ish(labeled_filename, ish_filename, out_filename, slice)

