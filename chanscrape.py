#JSON and tokenization
import basc_py4chan
import nltk
#data storage
import cPickle
#io
import os.path

#BOARDS TO SCRAPE
boardnames = {'mu', 'ck', 'pol', 'b', 'lgbt'}

def scrape( boardname ):

    #load 4chan board
    b = basc_py4chan.Board(boardname)

    #history file init
    histname = boardname + '.hist'
    here = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(here, histname)):
        print('no file ' + histname)
        #create history file and initialize variables
        hist = open(os.path.join(here, histname), 'wb+')
        history = set()
        freqdict = {}
        wordscollected = 0
        uniquecollected = 0
    else:
        print(histname + ' found')
        #open history file and unpickle data
        hist = open(os.path.join(here, histname), 'rb')
        history = cPickle.load(hist)
        freqdict = cPickle.load(hist)
        wordscollected = cPickle.load(hist)
        uniquecollected = cPickle.load(hist)
        hist.close()
        hist = open(os.path.join(here, histname), 'wb+')

    #open file for plaintext dump
    textname = boardname + '.txt'
    text = open(textname, 'a')

    #gather current thread IDs
    ids = b.get_all_thread_ids()
    print('gathering posts from /' + boardname + '/')
    print('-------------------------------')

    for x in range(1, len(ids)-1):
        #if the thread has not 404'd:
        if b.thread_exists(ids[x]):
            #fetch thread
            thread = b.get_thread(ids[x])

            #iterate through posts
            for post in thread.posts:
                if post.post_id not in history:
                    history.add(post.post_id)
                    text.write(str(post.post_id) + ' : \n\n' + post.text_comment.encode('ascii', 'ignore').decode('ascii') + '\n\n')
                    words = nltk.word_tokenize(post.text_comment)
                    for word in words:
                        value = freqdict.setdefault(word, 0)
                        if value == 0:
                            uniquecollected += 1
                        freqdict[word] = value + 1
                        wordscollected += 1

    #pickle history data
    cPickle.dump(history, hist)
    cPickle.dump(freqdict, hist)
    cPickle.dump(wordscollected, hist)
    cPickle.dump(uniquecollected, hist)

    #all done!
    text.close()
    hist.close()
    return

#main execution
for name in boardnames:
    scrape( name )

