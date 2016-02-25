
import urllib2
import time
import threading
links = ["http://www.reddit.com/",
         "https://www.reddit.com/r/random/",
         "https://www.reddit.com/r/AskReddit/",
         "https://www.reddit.com/r/pics/",
         "https://www.reddit.com/r/Showerthoughts/",
         "https://www.reddit.com/r/Showerthoughts/controversial/",
         "https://www.reddit.com/r/Showerthoughts/ads/",
         "https://www.reddit.com/r/gifs/",
         "https://www.reddit.com/r/worldnews/",
         "https://www.reddit.com/r/worldnews/new/",
         "https://www.reddit.com/r/todayilearned/"
         ]
def requestEngine():
    while True:
        for i in links:
            try:
                urllib2.urlopen(i).read()
            except urllib2.HTTPError:
                print("ERROR:")



threads = []
for i in range(0, 2):
    threads.append(threading.Thread(None, requestEngine(), None, None, None, None))
    threads[i].start()
