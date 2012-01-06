
from xml.dom import minidom

class DOMReader:
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.level = 0
        self.nodelist = {}
        
    def load2List(self, node, level):
        if node.nodeType == node.ELEMENT_NODE:
            self.nodelist[node] = level
            for c in node.childNodes:
                self.load2List(c, level + 1)
    
    def loadfile(self, filename):
        sock = open(filename)
        return minidom.parse(sock).documentElement

if __name__ == '__main__':
    reader = DOMReader()
    n = reader.loadfile('DataMaintenance.xml')
    reader.load2List(n, 0)
    print len(reader.nodelist.keys())
        