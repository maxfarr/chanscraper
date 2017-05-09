import cPickle
import os.path

def status( boardname ):
    #history file init
    histname = boardname + '.hist'
    here = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(here, histname)):
        print('no file ' + histname)
        return
    else:
        print('/' + boardname + '/')
        
        #open history file and unpickle data
        hist = open(os.path.join(here, histname), 'rb')
        history = cPickle.load(hist)
        freqdict = cPickle.load(hist)
        wordscollected = cPickle.load(hist)
        uniquecollected = cPickle.load(hist)

        #output data
        print('posts scraped: ' + str(len(history)))
        print('total tokens: ' + str(wordscollected))
        print('unique tokens: ' + str(uniquecollected))
        print('\ntokens:\n')
        for w in sorted(freqdict, key=freqdict.get, reverse=True):
            if freqdict[w] > 4:
                print (w + ' : ' + str(freqdict[w]))
        print('\n-------------------------------')

    #all done!
    hist.close()
    return

#main execution
while 1 == 1:
    status( raw_input('board to check: ') )
