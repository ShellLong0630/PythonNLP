#coding=utf-8
'''
Created on Sep. 25, 2015

@author: LuDan
'''
import jieba
from nltk import *
import codecs
from operator import itemgetter
from pytagcloud import *
from PIL import Image

def rtSegResult(fdir, frfile, stopuse):
    '''
    Return the segmentation results. Only can be applied in Chinese. 
    If frfile is true, fdir is the filepath of the source text,
    else the fdir is the source text itself. 
    If stopuse is true, use the stopwords.
    '''
    text=""
    
    if frfile:
        try:
            file1=codecs.open(fdir,'r',"utf-8")
            text=file1.read()
            re_h=re.compile(u"[^\u2e80-\u9fff]")
            text=re_h.sub('',text)
        except Exception as e:
            print e
        
    else:
        text=fdir
    seg_list = jieba.cut(text,cut_all=False)
    stop_words=[]
    if stopuse:
        stop_words=LoadStopWords()
    long_words=[s for s in seg_list if len(s)>1 and s not in stop_words]
    V=FreqDist(long_words)
    SegResults=sorted(V.iteritems(),key=itemgetter(1),reverse=True)
    
    return SegResults

def FileSegResult(ofile,SegResults):
    '''
    The ofile is the filepath of the output file which contains 
    the segmentation result and the words frenquencies.
    '''
    try:
        file2=codecs.open(ofile,'w','utf-8')
        for v in SegResults:
            file2.write(v[0]+str(v[1])+'\n')
    except Exception as e:
        print e


def LoadStopWords():
    '''
    Read the stopwords.txt and load the stop words list.
    '''
    stop_words=[]
    try:
        stopfile=codecs.open('stopwords.txt','r','utf-8')
        for line in stopfile.readlines():
            line=line.replace('\r\n','')
            stop_words.append(line)
        print 'Load stop words list succesfully.'
        return stop_words
    except Exception as e:
        print e
        return []

def PlotWordCloud(SegResults, filename, wordnum=50, fMinSize=20, fMaxSize=100, pLen=700, pWidth=500):
    '''
    plot the wordcloud
    '''
    tags = make_tags(SegResults[:wordnum],minsize=fMinSize,maxsize=fMaxSize)
    create_tag_image(tags,filename,size=(pLen, pWidth),fontname="MsYH")
    im=Image.open(filename)
    #im.show()

    