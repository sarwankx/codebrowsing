# get directory name
# scan through all file names
# read file name having .ts extension
# collect all the selectors.
# Scan through all html files.
# check each html file if it has any of these selectors.
# check if selector component name node already exists, if not create one.
# check if there is a node with this component name.
# if not exists, Create a node having ts component name 
# if already exists, set its child to that selector component name.
# also search class name for each component.
# check if this component is opened as dialog in any other components.
#
import os
import re
""" directoryName = "C:\\work\\code\\vantage-lake\\janus\\apps\\data-sharing" """
directoryName = "C:\\work\\code\\demo-branch\\data-sharing\\apps\\data-sharing"
searchstring = "selector"

allNodes = []

class Tree:
    def __init__(self, componentName, selectorName,componentClassName,dialogs):
        self.children = []
        self.htmlFileName = componentName + ".html"
        self.tsFileName = componentName + ".ts"
        self.cssFileName = componentName + ".scss"
        self.selectorName = selectorName
        self.componentClassName = componentClassName
        self.dialogs = dialogs
        self.parent = False

# root = Tree("app.component","data-sharing-root","AppComponent")
""" root.children = [left, middle, right] """
def searchWordInDirectory(searchstring,directoryName):

    directory = os.listdir(directoryName)
    selectorPattern = re.compile(r"selector:( *)'(.*)'")
    """ matches one or more spaces between export and class"""
    componentNamePattern = re.compile(r"export(\s)*class(\s)*(.*)Component") 
    dialogPattern = re.compile(r"\.open((.*)Component)")
    inputPattern = re.compile("Input")
    outputPattern = re.compile(r"@Output().*")
    for fname in directory:
        if os.path.isfile(directoryName + os.sep + fname):
            # Full path
            if(fname.endswith("component.ts")):
                """ print(fname) """
                fullFilePath = directoryName + os.sep + fname
                f = open(fullFilePath, 'r')
                componentName = ''
                selectorName = ''
                componentClassName = ''
                dialogComponent = ''
                inputs = []
                outputs = []
                
                for i, line in enumerate(f):
                    
                    for match in re.finditer(selectorPattern, line):
                        word = match.group()
                        selectorName = word[word.index("'")+1:len(word)-1]
                        componentName = fname[0:(len(fname)-3)]
                        
                    if selectorName!='':
                        break
                
                for i, line in enumerate(f):  
                    for match in re.finditer(componentNamePattern, line):
                        word = match.group()
                        componentClassName = word[word.rindex(" ")+1:len(word)]
                    if componentClassName!='':
                        break
                
                for i, line in enumerate(f):  
                    for match in re.finditer(dialogPattern, line):
                        word = match.group()
                        dialogComponent = word[word.index("(")+1:len(word)]
                        print('dialogComponent = ',dialogComponent)
                    if dialogComponent!='':
                        break
                textfile = open(fullFilePath, 'r')
                filetext = textfile.read()
                textfile.close()
                inputMatches = re.findall("@Input\(\).*", filetext)
                outputMatches = re.findall("@Output\(\).*", filetext)
                print("inputMatches = ",inputMatches)
                print("outputMatches = ",outputMatches)
                
                print(inputs,outputs)
                   
                
                node = Tree(componentName,selectorName,componentClassName,dialogComponent)
                allNodes.append(node)
                    
                f.close()
        else:
            searchWordInDirectory(searchstring,directoryName + os.sep + fname)
def printAllNodes(nodeList):
    print('printAllNodes')
    for node in nodeList:
        if not node.parent:
            printAllChildren(node,1)
                
def printAllChildren(node,level):
    for i in range(level):
        print("    ",end="")
    if node.dialogs!='':
        print(node.componentClassName,end="")
        print("  ===>  DialogComponent ===> ",node.dialogs)
    else:
        print(node.componentClassName)
       
    for child in node.children:
        printAllChildren(child,level + 1)
        


def setChildren(childNode,htmlFileName):
    """  print('setChildren called ',childNode,htmlFileName) """
    for node in allNodes:
        if node.htmlFileName == htmlFileName:
            node.children.append(childNode)

def drawTreeMap(allNodes,dirName):
    directory = os.listdir(dirName)
    for fname in directory:
        if os.path.isfile(dirName + os.sep + fname):
            # Full path
            if(fname.endswith("component.html")):
                with open(dirName + os.sep + fname, 'r') as f:
                    datafile = f.readlines()
                    for line in datafile:
                        for node in allNodes:
                            selector =  "</" + node.selectorName + ">"
                            if selector in line:
                                node.parent = True
                                setChildren(node,fname)
        else:
            drawTreeMap(allNodes,dirName + os.sep + fname)
        

searchWordInDirectory(searchstring,directoryName)
drawTreeMap(allNodes,directoryName)
printAllNodes(allNodes)