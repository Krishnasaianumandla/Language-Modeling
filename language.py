"""
Language Modeling Project
Name: Anumandla Krishna Sai
Roll No: 2021501010
"""

import language_tests as test

project = "Language" # don't edit this

### WEEK 1 ###

'''
loadBook(filename)
#1 [Check6-1]
Parameters: str
Returns: 2D list of strs
'''
def loadBook(filename):
    lst=[]
    f= open(filename,"r")
    for x in f:
        if x!="\n":
            lst.append(x.split())
    return lst


'''
getCorpusLength(corpus)
#2 [Check6-1]
Parameters: 2D list of strs
Returns: int
'''
def getCorpusLength(corpus):
    length=0
    for outer in corpus:
        length+=len(outer)
    return length


'''
buildVocabulary(corpus)
#3 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def buildVocabulary(corpus):
    vocub=[]
    for outer in corpus:
        for inner in outer:
            if inner not in vocub:
                vocub.append(inner)
    return vocub


'''
countUnigrams(corpus)
#4 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countUnigrams(corpus):
    unigram={}
    for row in corpus:
        for col in row:
            if col not in unigram:
                unigram[col]=1
            else:
                unigram[col]+=1
    return unigram


'''
getStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: list of strs
'''
def getStartWords(corpus):
    startWords=[]
    for inner in corpus:
        if inner[0] not in startWords:
            startWords.append(inner[0])
    return startWords


'''
countStartWords(corpus)
#5 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to ints
'''
def countStartWords(corpus):
    startWordsDic={}
    for inner in corpus:
        if inner[0] not in startWordsDic:
            startWordsDic[inner[0]]=1
        else:
            startWordsDic[inner[0]]+=1
    return startWordsDic


'''
countBigrams(corpus)
#6 [Check6-1]
Parameters: 2D list of strs
Returns: dict mapping strs to (dicts mapping strs to ints)
'''
def countBigrams(corpus):
    bigrams={}
    for sent in corpus:
        for i in range(len(sent)-1):          
            if sent[i] not in bigrams:
                bigrams[sent[i]]={}
            if sent[i+1] not in bigrams[sent[i]]:
                bigrams[sent[i]][sent[i+1]]=1
            else:
                bigrams[sent[i]][sent[i+1]]+=1
    return bigrams


### WEEK 2 ###

'''
buildUniformProbs(unigrams)
#1 [Check6-2]
Parameters: list of strs
Returns: list of floats
'''
def buildUniformProbs(unigrams):
    return [1/len(unigrams) for i in unigrams]

'''
buildUnigramProbs(unigrams, unigramCounts, totalCount)
#2 [Check6-2]
Parameters: list of strs ; dict mapping strs to ints ; int
Returns: list of floats
'''
def buildUnigramProbs(unigrams, unigramCounts, totalCount):
    return [unigramCounts[i]/totalCount for i in unigrams]

'''
buildBigramProbs(unigramCounts, bigramCounts)
#3 [Check6-2]
Parameters: dict mapping strs to ints ; dict mapping strs to (dicts mapping strs to ints)
Returns: dict mapping strs to (dicts mapping strs to (lists of values))
'''
def buildBigramProbs(unigramCounts, bigramCounts):
    bigramProbs={}
    for prevWord in bigramCounts:
        bigramProbs[prevWord]={}
        bigramProbs[prevWord]["words"]=[bigram for bigram in bigramCounts[prevWord]]
        bigramProbs[prevWord]["probs"]=[bigramCounts[prevWord][i]/unigramCounts[prevWord] for i in bigramCounts[prevWord]]
    return bigramProbs


'''
getTopWords(count, words, probs, ignoreList)
#4 [Check6-2]
Parameters: int ; list of strs ; list of floats ; list of strs
Returns: dict mapping strs to floats
'''
def getTopWords(count, words, probs, ignoreList):
    topWords=dict(zip(words,probs))
    for i in ignoreList:
        if i in topWords:
            topWords.pop(i)
    return dict(sorted(topWords.items(),key=lambda x:x[1],reverse=True)[:count])


'''
generateTextFromUnigrams(count, words, probs)
#5 [Check6-2]
Parameters: int ; list of strs ; list of floats
Returns: str
'''
from random import choices
def generateTextFromUnigrams(count, words, probs):
    sentence=""
    for i in range(count):
        sentence+=" "+choices(words,weights=probs)[0]
    return sentence.strip()

'''
generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs)
#6 [Check6-2]
Parameters: int ; list of strs ; list of floats ; dict mapping strs to (dicts mapping strs to (lists of values))
Returns: str
'''
def generateTextFromBigrams(count, startWords, startWordProbs, bigramProbs):
    text=""
    z=choices(startWords,weights=startWordProbs)[0]
    text=z
    for i in range(count-1):
        if z!=".":
            z=choices(bigramProbs[z]["words"],weights=bigramProbs[z]["probs"])[0]
            text+=" "+z
        else:
            z=choices(startWords,weights=startWordProbs)[0]
            text+=" "+z   
    return text


### WEEK 3 ###

ignore = [ ",", ".", "?", "'", '"', "-", "!", ":", ";", "by", "around", "over",
           "a", "on", "be", "in", "the", "is", "on", "and", "to", "of", "it",
           "as", "an", "but", "at", "if", "so", "was", "were", "for", "this",
           "that", "onto", "from", "not", "into" ]

'''
graphTop50Words(corpus)
#3 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTop50Words(corpus):
    unigrams=buildVocabulary(corpus)
    unigramProbs=buildUnigramProbs(unigrams, countUnigrams(corpus), getCorpusLength(corpus))
    mostFreqWords=getTopWords(50, unigrams, unigramProbs, ignore)
    barPlot(mostFreqWords, "Top 50 most frequent words using Unigram model")


'''
graphTopStartWords(corpus)
#4 [Hw6]
Parameters: 2D list of strs
Returns: None
'''
def graphTopStartWords(corpus):
    startWords=getStartWords(corpus)
    startWordProbs = buildUnigramProbs(startWords, countStartWords(corpus), getCorpusLength(corpus))
    mostFreqWords=getTopWords(50, startWords, startWordProbs, ignore)
    barPlot(mostFreqWords,"Top 50 most frequent start words")


'''
graphTopNextWords(corpus, word)
#5 [Hw6]
Parameters: 2D list of strs ; str
Returns: None
'''
def graphTopNextWords(corpus, word):
    bigramProbs=buildBigramProbs(countUnigrams(corpus),countBigrams(corpus))
    mostFreqWords=getTopWords(10,bigramProbs[word]["words"],bigramProbs[word]["probs"],ignore)
    wordName="Top 10 words after the given word: {}".format(word)
    barPlot(mostFreqWords,wordName)


'''
setupChartData(corpus1, corpus2, topWordCount)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int
Returns: dict mapping strs to (lists of values)
'''
def setupChartData(corpus1, corpus2, topWordCount):
    unigrams1=buildVocabulary(corpus1)
    unigramProbs1=buildUnigramProbs(unigrams1, countUnigrams(corpus1), getCorpusLength(corpus1))
    mostFreqWords1=getTopWords(topWordCount, unigrams1, unigramProbs1, ignore)
    unigrams2=buildVocabulary(corpus2)
    unigramProbs2=buildUnigramProbs(unigrams2, countUnigrams(corpus2), getCorpusLength(corpus2))
    mostFreqWords2=getTopWords(topWordCount, unigrams2, unigramProbs2, ignore)
    probs1,probs2=[],[]
    lst = list(mostFreqWords1.keys()) + list(mostFreqWords2.keys())
    topWords = list(dict.fromkeys(lst))
    for i in topWords:
        probs1.append(unigramProbs1[unigrams1.index(i)]) if i in unigrams1 else probs1.append(0)
        probs2.append(unigramProbs2[unigrams2.index(i)]) if i in unigrams2 else probs2.append(0)       
    return {"topWords":topWords,"corpus1Probs":probs1,"corpus2Probs":probs2}


'''
graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; str ; 2D list of strs ; str ; int ; str
Returns: None
'''
def graphTopWordsSideBySide(corpus1, name1, corpus2, name2, numWords, title):
    chartData=setupChartData(corpus1, corpus2, numWords)
    sideBySideBarPlots(chartData["topWords"], chartData["corpus1Probs"], chartData["corpus2Probs"], name1, name2, title)

'''
graphTopWordsInScatterplot(corpus1, corpus2, numWords, title)
#6 [Hw6]
Parameters: 2D list of strs ; 2D list of strs ; int ; str
Returns: None
'''
def graphTopWordsInScatterplot(corpus1, corpus2, numWords, title):
    chartData=setupChartData(corpus1, corpus2, numWords)
    scatterPlot(chartData["corpus1Probs"], chartData["corpus2Probs"], chartData["topWords"], title)

### WEEK 3 PROVIDED CODE ###

"""
Expects a dictionary of words as keys with probabilities as values, and a title
Plots the words on the x axis, probabilities as the y axis and puts a title on top.
"""
def barPlot(dict, title):
    import matplotlib.pyplot as plt

    names = []
    values = []
    for k in dict:
        names.append(k)
        values.append(dict[k])

    plt.bar(names, values)

    plt.xticks(rotation='vertical')
    plt.title(title,weight="bold",fontsize=15,color="red")

    plt.show()


"""
Expects 3 lists - one of x values, and two of values such that the index of a name
corresponds to a value at the same index in both lists. Category1 and Category2
are the labels for the different colors in the graph. For example, you may use
it to graph two categories of probabilities side by side to look at the differences.
"""
def sideBySideBarPlots(xValues, values1, values2, category1, category2, title):
    import matplotlib.pyplot as plt

    w = 0.35  # the width of the bars

    plt.bar(xValues, values1, width=-w, align='edge', label=category1)
    plt.bar(xValues, values2, width= w, align='edge', label=category2)

    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)

    plt.show()

"""
Expects two lists of probabilities and a list of labels (words) all the same length
and plots the probabilities of x and y, labels each point, and puts a title on top.
Note that this limits the graph to go from 0x0 to 0.02 x 0.02.
"""
def scatterPlot(xs, ys, labels, title):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()

    plt.scatter(xs, ys)

    # make labels for the points
    for i in range(len(labels)):
        plt.annotate(labels[i], # this is the text
                    (xs[i], ys[i]), # this is the point to label
                    textcoords="offset points", # how to position the text
                    xytext=(0, 10), # distance from text to points (x,y)
                    ha='center') # horizontal alignment can be left, right or center

    plt.title(title)
    plt.xlim(0, 0.02)
    plt.ylim(0, 0.02)

    # a bit of advanced code to draw a y=x line
    ax.plot([0, 1], [0, 1], color='black', transform=ax.transAxes)

    plt.show()


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek1()
    '''
    d={ "hello" : 1, "and" : 1, "welcome" : 1, "to" : 2, "15-110" : 1, 
          "." : 2, "we're" : 1, "happy" : 1, "have" : 1, "you" : 1 }
    barPlot(d,"Most used words of the authors")
    words = [ "hello", "and", "welcome", "to", "15-110", ".", "we're", "happy", "have", "you" ]
    probs = [ 4/12, 3/12, 2/12, 2/12, 1/12, 2/12, 1/12, 6/12, 7/12, 7/12 ]
    probs1 = [ 6/12, 5/12, 4/12, 2/12, 5/12, 8/12, 9/12, 10/12, 11/12, 4/12 ]
    sideBySideBarPlots(words, probs, probs1, "Unigram Model", "Bigram Model", "Probabilities of word occuring in Unigram Model VS Bigram Model")
    labels=[ "hello", "and", "welcome", "to", "15-110", ".", "we're", "happy", "have", "you" ]
    ys = [ -4/12, 3/12, -2/12, 2/12, -1/12, 2/12, -1/12, 6/12, -7/12, 7/12 ]
    xs=[25, 15, 18, 29, 15, 32, 34, 12, 5, 15]
    scatterPlot(xs, ys, labels, "Scatterplot for Unigram model")'''
    # test.testLoadBook()
    # test.testGetCorpusLength()
    # test.testBuildVocabulary()
    # test.testCountUnigrams()
    # test.testGetStartWords()
    # test.testCountStartWords()
    # test.testCountBigrams()
    # test.testBuildUniformProbs()
    # test.testBuildUnigramProbs()
    # test.testBuildBigramProbs()
    # test.testGetTopWords()
    # test.testGenerateTextFromUnigrams()
    # test.testGenerateTextFromBigrams()
    # test.testSetupChartData()
    ## Uncomment these for Week 2 ##

    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # test.runWeek2()


    # Uncomment these for Week 3 ##
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    test.runWeek3()
