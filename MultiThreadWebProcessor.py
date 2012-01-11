import Queue, threading, urllib2, time, sys

from BeautifulSoup import BeautifulSoup

hosts = ['http://www.baidu.com', 'http://www.google.com.hk',
          
         'http://www.51buy.com', 'http://www.163.com']

incomingQueue = Queue.Queue()
outcomingQueue = Queue.Queue()


class URLThread(threading.Thread):
    
    def __init__(self, incoming, outcoming):
        threading.Thread.__init__(self)
        self.incoming = incoming
        self.outcoming = outcoming
        
    def run(self):
        while True:
            host = self.incoming.get()
            url = urllib2.urlopen(host)
            chunk = url.read()
            try:
                chunk = chunk.decode('gbk')
            except:
                chunk = chunk
            url.close()
            self.outcoming.put(chunk)
            self.incoming.task_done()

class DataMineThread(threading.Thread):
    
    def __init__(self, outcoming):
        threading.Thread.__init__(self)
        self.outcoming = outcoming
        
    def run(self):
        while True:
            chunk = self.outcoming.get()
            soup = BeautifulSoup(chunk)
            print '====================================='
            print soup.findAll('title')[0].renderContents()
            soup.close()
            self.outcoming.task_done()
            

start = time.time()

def main():
    
    for u in range(5):
        t = URLThread(incomingQueue, outcomingQueue)
        t.setDaemon(True)
        t.start()
        
    for host in hosts:
        incomingQueue.put(host)
    
    for d in range(5):
        dt = DataMineThread(outcomingQueue)
        dt.setDaemon(True)
        dt.start()

    incomingQueue.join()
    outcomingQueue.join()


main()

print "Elapsed Time: %s" % (time.time() - start)