
from xml.dom import minidom

class DOMReader:
    nodespace = '\t'
    expandspace = '+'
    attributespace = '@'
    
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
    
    def output(self, node, level):
        if node.nodeType == node.ELEMENT_NODE:
            if node.hasChildNodes():
                print self.nodespace * level, self.expandspace, node.nodeName
            else:
                print self.nodespace * level, node.nodeName
            attributesMap = node.attributes
            for a in attributesMap.keys():
                print self.nodespace * level, self.attributespace, a, '=', attributesMap.get(a).value
            for c in node.childNodes:
                self.output(c, level + 1)
            

if __name__ == '__main__':
    reader = DOMReader()
    n = reader.loadfile('DataMaintenance.xml')
    reader.output(n, 0)
        