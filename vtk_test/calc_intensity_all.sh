#!/bin/bash -x 

for i in car8 adra1b nlgn1 klf12 klf12_2 vim plxdc2 dtl pax6 pax6_2 prlr eral1 ; \
do \
    python draw_intensity.py ../matching_area/result/${i}.txt 1 ${i}; \
done;

