# coding=utf-8
'''
Created on Sep. 29, 2015

@author: LuDan
'''
import Segmentation as seg

fdir='E:/Other/USTB/nlp/Text1.txt'
frfile=True
ofile='text.txt'

SegResults=seg.rtSegResult(fdir, frfile, True)
#get the segmentation results
seg.FileSegResult(ofile, SegResults)
#put the segmentation results to a file
seg.PlotWordCloud(SegResults,  'Ttag_cloud.jpg',30,20,80)
#plot the wordcloud