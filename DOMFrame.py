import wx
from xml.dom import minidom
class DOMFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="XML Reader", size=(450,350))
        # Create the tree
        treePanel = wx.Panel(self, -1)
        textPanel = wx.Panel(self, -1)
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        self.tree = wx.TreeCtrl(treePanel )
        self.display = wx.StaticText(textPanel, style=wx.ALIGN_LEFT)      
        root = minidom.parse('DataMaintenance.xml').documentElement
        self.addNode(None, root)
        
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onSelectChanged, self.tree)
        self.tree.Expand(self.tree.GetRootItem())
        
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(treePanel, 1, wx.EXPAND)
        hbox.Add(textPanel, 1, wx.EXPAND)
        
        treePanel.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Center()
    
    def addNode(self, parentNode, node):
        if node.nodeType == node.ELEMENT_NODE:
            if parentNode:
                x = self.tree.AppendItem(parentNode, node.nodeName)
            else:
                x = self.tree.AddRoot(node.nodeName)
            if node.hasAttributes():
                for a in node.attributes.keys():
                    self.tree.AppendItem(x, a + "=" + unicode.strip(node.attributes.get(a).value))
            if node.hasChildNodes():
                for c in node.childNodes:
                    self.addNode(x, c)
    
    def onSelectChanged(self,evt):
        item =  evt.GetItem()
        self.display.SetLabel(self.tree.GetItemText(item)) 

app = wx.PySimpleApp(redirect=True)
frame = DOMFrame()
frame.Show()
app.MainLoop()