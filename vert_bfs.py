''' 
   Problem Solving with Algorithms and Data Structures using Python
   Cite: https://runestone.academy/runestone/books/published/pythonds/Graphs/Implementation.html
   with a few modifications by Lamont Samuels 
'''
from queue import Queue

WHITE=0
BLACK=1
GRAY=2

class Vertex:
    '''
    A Vertex in a graph contains a label for that vertex (i.e., the data) and the edges it is connected to. 
    '''
    def __init__(self, label):
        self.label = label
        self.edges = [] 
        self.distance = 0 
        self.pred = None 
        self.color = WHITE 

    def add_edge(self, neighbor):
        self._edges.append(neighbor)

    @property
    def label(self):
        return self._label 
    
    @label.setter
    def label(self, new_label):
        self._label = new_label 

    @property 
    def edges(self):
        return self._edges 
    
    @edges.setter
    def edges(self,new_edges):
        self._edges = new_edges 

    @property
    def distance(self):
        return self._distance 

    @distance.setter
    def distance(self, dist):
        if dist < 0: 
            raise ValueError("dist argument must be greater than 0")
        self._distance = dist 
    @property 
    def pred(self):
        return self._pred 
    
    @pred.setter
    def pred(self, pred):
        self._pred = pred 

    @property 
    def color(self):
        return self._color  
    
    @color.setter 
    def color(self, c):
        self._color = c
