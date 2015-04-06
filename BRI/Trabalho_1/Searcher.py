# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 23:44:07 2015

@author: raul
"""
import ast
import nltk
import operator
import os
from pprint import pprint as pp
#globals
PATH = os.path.dirname(__file__)

def strToDict(listString, hasListInside=True):
    dictionary = {}
    if hasListInside is True:
        for s in listString:
            dictionary.update({s[0]: ast.literal_eval(s[1])})
    else:
        for s in listString:
            dictionary.update({s[0]: s[1]})
    return dictionary
    
    
    
def makeSearch(indexes, queries, stop=[]):
    rankings = {}
    for queryNumber in queries.keys():
        #N = len(queries)
        tokens = nltk.word_tokenize(queries[queryNumber])
        #freq_iq = nltk.FreqDist(tokens)
        #using only valid tokens and cleaning invalid ones, e.g. (?, brackets and etc)
        ranking = {}
        for token in tokens:
            if token in stop or len(token) < 2:
                tokens.remove(token)
        for token in tokens:
            #updating weights based on terms frequence
            try:
                for k in indexes[token].keys():
                    #n_q = len(indexes[token])
                    #maxFreq_iq = freq_iq.most_common(1)
                    w_iq = 1 
                    #w_iq=(freq_iq[token]/maxFreq_iq[0][1])*math.log(N/n_q)
                    tf_idf = indexes[token][k]*w_iq
                    #cosine = math.sqrt(math.pow(w_iq, 2))*math.sqrt(math.pow(indexes[token][k], 2))
                    #sim=tf_idf/cosine
                    try:
                        weight = ranking[k] + tf_idf
                        ranking.update({k: 1/weight})
                    except KeyError:
                        ranking.update({k: 1/tf_idf})
            except KeyError:
                pp("word '"+token+"' not found!")
        rankings.update({queryNumber: sorted(ranking.items(), key=operator.itemgetter(1), reverse=False)})
    return rankings
    
    
    
def writeResults(rankings, path):
    f = open(PATH+path, 'w+')
    for ident in rankings.keys():
        line = ''
        line+= ident+';'
        i=0
        for docNum in rankings[ident]:
            #don't print documents umbers with 0 weight (e.g. no occurrence)            
            if docNum[1] > 0.0:
                i+=1
                line+='['            
                line+= str(i)+', '           
                line+= str(docNum[0])+', '
                line+= str('%.2f' % round(docNum[1], 2))#distance
                line+='],'
        line=line.rstrip(',')+'\n'
        f.write(line)
    f.close()