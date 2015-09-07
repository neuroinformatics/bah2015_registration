# -*- coding: utf-8 -*-

import sys
from PIL import Image
from PIL import ImageStat

def regen_segfile(labeled_filename, out_fileformat=''):
    labeled = Image.open(labeled_filename)
    labeled_count = {}


    for z in range(256):
        labeled.seek(z)
        print 'Area Counting : slice %d' % z
        data = labeled.getdata()
        for value in data:
            value = int(value)
            if value not in labeled_count:
                labeled_count[value] = 1
            else:
                labeled_count[value] += 1


    i = 1
    for k, v in sorted(labeled_count.items(), key=lambda x:x[1], reverse=True):
        print 'Lank %5d : %d (%d)' % (i, k, v)
        i += 1
    #print labeled_count

    '''
    print 'Generating New Segmentation File'
    for z in range(256):
        labeled.seek(z)
        data = labeled.getdata()
        print 'Generationg : slice %d' % z
    '''

def matching_ish(labeled_filename, ish_filename, output_filename, slice):
    labeled = Image.open(labeled_filename)
    ish = Image.open(ish_filename)
    ish_data = ish.getdata()

    labeled_count = {}
    labeled_volume = {}
    result_value = {}
    result_value_max = {}
    result_value_per_vol = {}

    '''
    for z in range(256):
        labeled.seek(z)
        print 'Area Counting : slice %d' % z
        data = labeled.getdata()
        for value in data:
            value = int(value)
            if value not in labeled_count:
                labeled_volume[value] = 0
                result_value[value] = 0
            else:
                pass
    '''
    for value in range(40):
        labeled_volume[value] = 0
        result_value[value] = 0
        result_value_max[value] = 0
        result_value_per_vol[value] = 0
    

    labeled.seek(slice)
    labeled_data = labeled.getdata()

    for value in labeled_data:
        value = int(value)
        labeled_volume[value] += 1

    threshold = 128
    for (ish_val, labeled_val) in zip(ish_data, labeled_data):
        if(int(labeled_val)!=0 and int(ish_val[0])!=0):
            if (ish_val[0] + ish_val[1] + ish_val[2])/3 > threshold:
                value = 256 - (ish_val[0] + ish_val[1] + ish_val[2])/3
                result_value[int(labeled_val)] += value
                if value > result_value_max[int(labeled_val)]:
                    result_value_max[int(labeled_val)] = value

    print labeled_volume
    volume_threshold = 200
    for i in range(40):
        if labeled_volume[i] > volume_threshold:
            result_value_per_vol[i] = float(result_value[i]) / float(labeled_volume[i])

    lines = []
    fp = open(output_filename, 'w')
    '''
    for (k, v) in result_value.items():
        lines.append('%d, %d\n' % (k, v))
    '''
    for (k, v) in result_value_per_vol.items():
        lines.append('%d, %6.1f\n' % (k, v))
    fp.writelines(lines)
    fp.close()
    #print result_value
    #print result_value_per_vol

    i = 1
    for k, v in sorted(result_value_per_vol.items(), key=lambda x:x[1], reverse=True):
        print 'Lank %5d : %d (%d)' % (i, k, v)
        i += 1


    return result_value




def analysis_tif(labeled_filename, ish_filename, out_filename, slice):
    labeled = Image.open(labeled_filename)
    ish = Image.open(ish_filename)

    labeled.seek(slice)
    #labeled.show()
    #ish.show()

    #ish.show()
    #stat = ImageStat.Stat(labeled)
    #hist = stat.histgram()
    #print hist
    
    #for i in range(1, 256):
    #    image.seek(i)

    size = labeled.size
    labeled_data = {}
    labeled_num = {}
    labeled_final = {}

    # make dict
    for z in range(256):
        labeled.seek(z)
        print 'Area Counting : slice %d' % z
        for x in range(size[0]):
            for y in range(size[1]):
                value = labeled.getpixel((x, y))
                if value not in labeled_data:
                    labeled_data[value] = 0
                    labeled_num[value] = 0
                else:
                    pass
                #labeled_data[value] += 1

    #print labeled_data


    labeled.seek(slice)
    for x in range(size[0]):
        for y in range(size[1]):
            value = labeled.getpixel((x, y))
            value2 = ish.getpixel((x, y))
            sum_value2 = 255 - (value2[0] + value2[1] + value2[2])/3
            #sum_value2 = 255 - value2[2]

            labeled_num[value] += 1
            if value <= 10 or sum_value2 < 90 or sum_value2 > 200:
                pass
                #labeled.putpixel((x, y), 0)
            else:
                labeled_data[value] += sum_value2
                #labeled.putpixel((x, y), sum_value2)
    

    for z in range(256):
        labeled.seek(z)
        print 'Processing : slice %d' % z
        for x in range(size[0]):
            for y in range(size[1]):
                value = labeled.getpixel((x, y))
                if labeled_num[value] > 100:
                    if value not in labeled_final:
                        labeled_final[value] = int(labeled_data[value] / labeled_num[value])

                    labeled.putpixel((x, y), labeled_final[value])
                else:
                    labeled.putpixel((x, y), 0)
        labeled.save(out_filename % z)

    #labeled.seek(slice)
    #labeled.show()
    #print labeled_data
    #print labeled_num
    print labeled_final


if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)

    labeled_filename = '/media/nebula/data/bah/reslice_labeled.tif'

    if argc >= 2:
        ish_filename = argvs[1]
    else:
        #ish_filename = '/media/nebula/data/bah/CD00050.1-VimRegistered.tif'
        ish_filename = '/media/nebula/data/bah/registration_Affine/CD00012.1-Car8.tif'

    if argc >= 3:
        out_filename = argvs[2]
    else:
        out_filename = './result/car8.txt'

    if argc >= 4:
        slice = int(argvs[3])
    else:
        slice = 113

    #analysis_tif(labeled_filename, ish_filename, out_filename, slice)
    #regen_segfile(labeled_filename)
    matching_ish(labeled_filename, ish_filename, out_filename, slice)

