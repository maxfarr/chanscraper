#JSON
import basc_py4chan
#tokenization
import nltk
#data storage
import cPickle
#io
import os.path
import os
#xml
import xml.etree.ElementTree
#datetime objects
from datetime import datetime

#BOARDS TO SCRAPE
#boardnames = {'mu', 'vg', 'k', 'pol', 'b', 'lgbt'}
boardnames = {'pol'}

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
    print('--------------------------------')

    for x in range(1, len(ids)-1):
        #if the thread has not 404'd:
        if b.thread_exists(ids[x]):
            #fetch thread
            thread = b.get_thread(ids[x])

            #iterate through posts
            for post in thread.posts:
                if post.post_id not in history:
                    #new post protocol

                    #add to history
                    history.add(post.post_id)

                    #dump text comment
                    text.write(str(post.post_id) + ' : \n\n' + post.text_comment.encode('ascii', 'ignore').decode('ascii') + '\n\n')

                    #create xml file
                    if not os.path.exists(boardname + "_xml"):
                        os.mkdir(boardname + "_xml")
                    directory = boardname + "_xml\\4chan_" + str(ids[x]) + "_" + str(post.post_id) + ".xml"
                    xmlfile = open(os.path.join(here, directory), 'w+')

                    #build xml tree/fill in data
                    postname = "" if not post.name else post.name.encode('ascii', 'ignore').decode('ascii').replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')
                    posturl = "" if not thread.semantic_url else thread.semantic_url.encode('ascii', 'ignore').decode('ascii').replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;') + "#p" + str(post.post_id)
                    postcomment = "" if not post.text_comment else post.text_comment.encode('ascii', 'ignore').decode('ascii').replace('&', '&amp;').replace('>', '&gt;').replace('<', '&lt;')
                    xmltext = """\
<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
<teiHeader>
<fileDesc>
<titleStmt><title>/""" + boardname + """/</title></titleStmt>
<publicationStmt>
<publisher>http://www.4chan.org</publisher>
</publicationStmt>
<sourceDesc>
<msDesc>
<msIdentifier>
<repository>4chan</repository>
<idno type="URL">""" + posturl + """</idno>
</msIdentifier>
</msDesc>
</sourceDesc>
<notesStmt>
<note type="post_id">""" + str(post.post_id) + """</note>
<note type="thread_id">""" + str(ids[x]) + """</note>
</notesStmt>
</fileDesc>
<profileDesc>
<particDesc><listPerson><person xml:id=\"""" + postname + """\"/></listPerson></particDesc>
</profileDesc>
</teiHeader>
<text>
<front><timeline><when xml:id="a" absolute=\"""" + post.datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ") + """\" /></timeline></front>
<body><div type="thread"><posting who=\"""" + postname + """\" synch="#a">""" + postcomment + """</posting></div></body>
</text>
</TEI>
"""

                    #write to + close xml file
                    xmlfile.write(xmltext)
                    xmlfile.close
                    
                    #update metadata
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

