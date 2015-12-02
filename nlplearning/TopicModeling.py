#coding=utf-8
'''
Created on Sep. 28, 2015

@author: LuDan
'''
import os
import codecs
import Segmentation as seg
from numpy import *
import lda

def rtTopics(dire,direo,topicnum,topicwordsnum,iternum=1000):
    """
    Return Topics. dire is the path of the filepath, topicnum is the
    number of topics, topicwordsnum is the number of words in every topic.
    """
    model=lda.LDA(n_topics=topicnum,n_iter=iternum,random_state=1)
    for filename in os.listdir(dire):
        vocab=()
        wordsdic={}
        filenum=0
        filename=filename.decode('gbk').encode('utf-8')
        fdir=dire+filename
        SegResults=seg.rtSegResult(fdir, True, True)
        seg.FileSegResult(direo+'words'+str(filenum+1)+'.txt', SegResults)
        seg.PlotWordCloud(SegResults,  'E:/Other/USTB/nlp/WordCloud/tag_cloud'+str(filenum+1)+'.jpg')
        for s in SegResults:
            sf=s[0].encode('utf-8')
            if wordsdic.has_key(sf):
                tmpdict=wordsdic[sf].copy()
                tmpdict[filenum]=s[1]
                wordsdic[sf]=tmpdict.copy()
            else:
                tmpdict={}
                tmpdict[filenum]=s[1]
                wordsdic[sf]=tmpdict.copy()
        filenum+=1
        vocab=tuple(wordsdic.keys())
        X=zeros((filenum,len(vocab)),dtype=int)
        wordnum=0
        for w in wordsdic.keys():
            tmpdict=wordsdic[w].copy()
            for t in tmpdict.keys():
                X[t][wordnum]=tmpdict[t]
            wordnum+=1
        print X.sum()
        model.fit(X)
        topic_word = model.topic_word_
        n_top_words = topicwordsnum
        fileout=codecs.open(direo+'topics'+str(filenum)+'.txt','w','utf-8')
        for i, topic_dist in enumerate(topic_word):
            topic_words = array(vocab)[argsort(topic_dist)][:-(n_top_words+1):-1]
            fileout.write(('Topic {}: {}'.format(i, '+'.join(topic_words))+'\n').decode('utf-8'))
        fileout.close()
    