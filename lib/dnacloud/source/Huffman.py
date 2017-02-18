"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 28 July 2013
Website: www.guptalab.org/dnacloud
This module is nothing but Huffman Encoding given any string as input we
get there Huffman values as output.
#########################################################################
"""

from collections import Counter
from treelib import Node,Tree

def stringToAsciiList(string):
        listOfAscii = []
        byteArray = bytearray(string)
        for i in byteArray:
            listOfAscii.append(i)
        #print listOfAscii
        return listOfAscii

class Huffman:
        def __init__(self):
                self.counter = 0
        
        def __init__(self,counter):
                self.counter = counter

#Removes the minimum item from the counter with minimum frequency
        def removeMin(self):
                minimum = min(self.counter.values())
                for i in self.counter.iteritems():
                        if i[1] == minimum:
                                break
                self.counter.pop(i[0])
                #print i[1]
                return i

        def node2Tree(self,tuple1,tuple2,tuple3):
                t = Tree()
#Id of each node = freq of that node(i[1])
#Node(tag,identifier(ID))       #create_node(tag,identifier(ID),parent)
#Nodes added in decreasing order of Frequency 
                node1 = Node(tuple1,tuple1[0])
                node2 = Node(tuple2,tuple2[0])
                node3 = Node(tuple3,tuple3[0])
                freq = tuple1[1] + tuple2[1] + tuple3[1]
                tag = tuple1[0] + tuple2[0] + tuple3[0]
                t.create_node("("+str(tag)+", " + str(freq)+")",tag,None)
#Addded the nodes as left right mid according to there frequency
#so the first node has always the highest frequency
                if tuple1[1] >= tuple2[1] and tuple1[1] >= tuple3[1]:
                        if tuple2[1] >= tuple3[1]:
                                t.add_node(node1,tag)
                                t.add_node(node2,tag)
                                t.add_node(node3,tag)
                        else:
                                t.add_node(node1,tag)
                                t.add_node(node3,tag)
                                t.add_node(node2,tag)
                elif tuple2[1] >= tuple3[1] and tuple2[1] >= tuple1[1]:
                        if tuple1[1] >= tuple3[1]:
                                t.add_node(node2,tag)
                                t.add_node(node1,tag)
                                t.add_node(node3,tag)
                        else:
                                t.add_node(node2,tag)
                                t.add_node(node3,tag)
                                t.add_node(node1,tag)
                else:
                        if tuple1[1] >= tuple2[1]:
                                t.add_node(node3,tag)
                                t.add_node(node1,tag)
                                t.add_node(node2,tag)
                        else:
                                t.add_node(node3,tag)
                                t.add_node(node2,tag)
                                t.add_node(node1,tag)

                #t.show()
                return t

        def node2TreeOfTwo(self,tuple1,tuple2):
                t = Tree()
                node1 = Node(tuple1,tuple1[0])
                node2 = Node(tuple2,tuple2[0])
                freq = tuple1[1] + tuple2[1]
                tag = tuple1[0] + tuple2[0]
                t.create_node("("+str(tag)+", " + str(freq)+")",tag,None)
                if tuple1[1] >= tuple2[1]:
                        t.add_node(node1,tag)
                        t.add_node(node2,tag)
                else:
                        t.add_node(node2,tag)
                        t.add_node(node1,tag)
                return t
#get_node(nid) return node      #tree.root return nid of root'
#node.fointer prints all its nodes ID's in order for us its in frequency order

        def base3String(self,node,tree):
                stack = []
                base3String = ""
                pNode = tree.get_node(node.bpointer)
                while isinstance(pNode,Node):
                        childList = pNode.fpointer
                        stack.append(len(childList) - 1 - int(childList.index(node.identifier)))
                        node = pNode
                        pNode = tree.get_node(pNode.bpointer)
                for i in range(len(stack)):
                        base3String = base3String + str(stack.pop())
                #print base3String
                return base3String

class HuffmanHelper:
        def __init__(self,string):
#Error check if there are less than 3 different words in a string
                self.string = string
                while 1:
#string = raw_input("Please Enter the String u wanna Encode:-")
                        if len(Counter(list(string))) >= 3:
                                break
                        else:
                                print "Inorder to Encode string should have atleast 3 different characters!!"
                a = stringToAsciiList(string)
                count = Counter(a)
                self.abc = Huffman(count)
#print count.items()
                tree = None
                treeList = []
                while len(count.items()) >= 3:
                        i = self.abc.removeMin()
                        j = self.abc.removeMin()
                        k = self.abc.removeMin()
                        tree = self.abc.node2Tree(i,j,k)
                        a = int(tree.get_node(tree.root).tag[1])
                        count.update({int(i[0]+j[0]+k[0]):int(i[1]+j[1]+k[1])})
#print count.items()
#This contains references to all the trees made
                        treeList.append(tree)
                ref2 = treeList[0]
#i = 0
#while i != len(treeList):
#        treeList[i].show()
#        i = i + 1
                ignoreTreeList = []
                for ix in range(len(treeList) - 1):
                        ref1 = treeList[ix]
                        for jx in range(ix + 1,len(treeList)):
                                ref2 = treeList[jx]
                                idRoot = ref1.root
                                if isinstance(ref2.get_node(idRoot),Node):
                                        node = ref2.get_node(idRoot)
                                        pNode = ref2.get_node(node.bpointer)
                                        childList = pNode.fpointer
                                        index = childList.index(ref1.root)
                                        if index == 2:
                                                ref2.remove_node(ref1.root)
                                                ref2.paste(pNode.identifier,ref1)
                                #ref2.show()
                                        elif index == 1:
                                                tree2 = ref2.subtree(childList[2])
                                                ref2.remove_node(childList[2])
                                                ref2.remove_node(node.identifier)
                                                ref2.paste(pNode.identifier,ref1)
                                                ref2.paste(pNode.identifier,tree2)
                                #ref2.show()
                                        elif index == 0:
                                                tree1 = ref2.subtree(childList[1])
                                                tree2 = ref2.subtree(childList[2])
                                                ref2.remove_node(childList[2])
                                                ref2.remove_node(childList[1])
                                                ref2.remove_node(idRoot)
                                                ref2.paste(pNode.identifier,ref1)
                                                ref2.paste(pNode.identifier,tree1)
                                                ref2.paste(pNode.identifier,tree2)
                                        ignoreTreeList.append(ref1)
                                        break

#There are two cases a->when count is left with only one node
#b->other when it is left with 2 nodes when we convert this to a tree
                if len(count) == 2:
                        t = self.abc.node2TreeOfTwo(count.items()[0],count.items()[1])
                        node = t.get_node(ref2.root)
                        pNode = t.get_node(node.bpointer)
                        childList = pNode.fpointer
                        index = childList.index(ref2.root)
                        if index == 0:
                                tree1 = t.subtree(childList[1])
                                t.remove_node(childList[1])
                                t.remove_node(ref2.root)
                                t.paste(pNode.identifier,ref2)
                                t.paste(pNode.identifier,tree1)
                        elif index == 1:
                                t.remove_node(ref2.root)
                                t.paste(pNode.identifier,ref2)
                else:   
                        t = treeList[len(treeList) - 1]

#Added the main tree to ignore list since it never comes in any of the subtrees
                ignoreTreeList.append(t)

#If a tree is not a part of any subtree then it should be added over here
                for i in treeList:
                        tx = treeList.pop()
                        if not tx in ignoreTreeList:
                                childList = t.get_node(t.root).fpointer
                                index = childList.index(tx.root)
                                if index == 0:
                                        tree1 = t.subtree(childList[1])
                                        t.remove_node(childList[1])
                                        t.remove_node(tx.root)
                                        t.paste(pNode.identifier,tx)
                                        t.paste(pNode.identifier,tree1)          
                                elif index == 1:
                                        t.remove_node(tx.root)
                                        t.paste(pNode.identifier,tx)         
                self.tree = t
                #t.show()
                #return t


        def charToHuffman(self):
                tx = self.tree
                count = 0
                dicty = {}
#Error check for enteing single charecter and that too should be part of input string
                while len(self.string) - count > 0:
#string = raw_input("Please enter the char for which you want the Huffman String:")
                        char = self.string[count]
                        nidList = stringToAsciiList(char)
# if not isinstance(tx.get_node(int(nidList[0])),Node) or len(nidList) != 1:
#        print "No such Node exist or the word/digit you entered is improper"
#else:
#break
                        n = tx.get_node(int(nidList[0]))
                        dicty.update({char : self.abc.base3String(n,tx)})
                        count = count + 1
                #print dicty
                return dicty
      
print HuffmanHelper(raw_input("Please enter the Huffman String:")).charToHuffman()
