
import urllib2
import time
import threading
links = ["http://www.reddit.com.com/",
         "https://www.reddit.com/r/random/",
         "https://www.reddit.com/r/AskReddit/",
         "https://www.reddit.com/r/pics/"
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
