'''
    Find the path out of a maze using BFS
'''

import turtle
from queue import ListQueue
from vert_bfs import Vertex

OBSTACLE = '+'
EMPTY = ' '
EXIT = '<'

WHITE=0
BLACK=1
GRAY=2
RED=3 # An empty space on the edge of the maze i.e. EXIT

class Maze:
    # Read in maxe txt and create list of lists of Vertices with labels
    # represent wall/space and edges pointing to adjacent space.
    # Create Screen and Turtle objects to navigate maze graphically.
    def __init__(self,mazeFileName):
        rowsInMaze = 0
        columnsInMaze = 0
        self.mazelist = []
        mazeFile = open(mazeFileName,'r')
        rowsInMaze = 0
        for line in mazeFile:
            rowList = []
            col = 0
            for ch in line[:-1]:
                if ch == 'S':
                    self.startRow = rowsInMaze
                    self.startCol = col
                    ch = ' '
                rowList.append(Vertex((ch, col, rowsInMaze)))
                col = col + 1
            rowsInMaze = rowsInMaze + 1
            self.mazelist.append(rowList)
            columnsInMaze = len(rowList)
        # After initializing all Vert with labels, loop through entire maze,
        # if a vert is empty (ie ' '), check all 4 neighbors for emptiness,
        # and add an edge to every empty neighbor. This will allow us to 
        # perform BFS on the path coordinates only
        r = -1
        for row in self.mazelist:
            r +=1
            c = -1
            for v in row:
                c += 1
                t_border = r == 0
                b_border = r == rowsInMaze - 1
                l_border = c == 0
                r_border = c == columnsInMaze - 1
                if v.label[0] == EMPTY:
                    if t_border or b_border or l_border or r_border:
                        v.color = RED
                    if not t_border:
                        up_nbr = self.mazelist[r-1][c]
                        if up_nbr.label[0] == EMPTY:
                            v.add_edge(up_nbr)
                    if not b_border:
                        down_nbr = self.mazelist[r+1][c]
                        if down_nbr.label[0] == EMPTY:
                            v.add_edge(down_nbr)
                    if not l_border:
                        left_nbr = self.mazelist[r][c-1]
                        if left_nbr.label[0] == EMPTY:
                            v.add_edge(left_nbr)
                    if not r_border:
                        right_nbr = self.mazelist[r][c+1]
                        if right_nbr.label[0] == EMPTY:
                            v.add_edge(right_nbr)

        self.rowsInMaze = rowsInMaze
        self.columnsInMaze = columnsInMaze
        self.xTranslate = -columnsInMaze/2
        self.yTranslate = rowsInMaze/2
        self.t = turtle.Turtle()
        self.t.shape('turtle')
        self.wn = turtle.Screen()
        self.wn.setworldcoordinates(-(columnsInMaze-1)/2-.5,-(rowsInMaze-1)/2-.5,(columnsInMaze-1)/2+.5,(rowsInMaze-1)/2+.5)

    def drawMaze(self):
        self.t.speed(1)
        self.wn.tracer(0)
        for y in range(self.rowsInMaze):
            for x in range(self.columnsInMaze):
                if self.mazelist[y][x].label[0] == OBSTACLE:
                    self.drawCenteredBox(x+self.xTranslate,-y+self.yTranslate,'orange')
        self.t.color('black')
        self.t.fillcolor('blue')
        self.wn.update()
        self.wn.tracer(1)

    def drawCenteredBox(self,x,y,color):
        self.t.up()
        self.t.goto(x-.5,y-.5)
        self.t.color(color)
        self.t.fillcolor(color)
        self.t.setheading(90)
        self.t.down()
        self.t.begin_fill()
        for i in range(4):
            self.t.forward(1)
            self.t.right(90)
        self.t.end_fill()

    def moveTurtle(self,x,y):
        self.t.up()
        self.t.setheading(self.t.towards(x+self.xTranslate,-y+self.yTranslate))
        self.t.goto(x+self.xTranslate,-y+self.yTranslate)

    def __getitem__(self,idx):
        return self.mazelist[idx]

    # Perfom a BFS from the start Vertex. Once an exit is reached,
    # break and return the exit Vertex
    def bfs(self):
        start = self.mazelist[self.startRow][self.startCol]
        start.distance = 0
        start.pred = None
        vertQ = ListQueue()
        vertQ.enqueue(start)
        while vertQ:
            v = vertQ.dequeue()
            v.color = BLACK
            for nbr in v.edges:
                if nbr.color == WHITE:
                    nbr.color = GRAY
                    nbr.pred = v
                    nbr.distance = v.distance + 1
                    vertQ.enqueue(nbr)
                elif nbr.color == RED:
                    nbr.pred = v
                    nbr.distance = v.distance + 1
                    END = nbr
                    vertQ = False
                    break

        return END

    def traverse(self, exit):
        path = []

        # a little recursive helper
        def traverse_h(end):
            nonlocal path
            path.append(end.label[1:])
            if end.pred == None:
                return
            traverse_h(end.pred)
        
        traverse_h(exit)
        return path





if __name__ == "__main__":
    myMaze = Maze('maze2.txt')
    myMaze.drawMaze()
    myMaze.moveTurtle(myMaze.startCol,myMaze.startRow)
    exit = myMaze.bfs()
    path = myMaze.traverse(exit)
    for x, y in path[::-1]:
        myMaze.moveTurtle(x, y)


