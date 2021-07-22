import argparse as ap

import math

import re

import platform

'''
Defining a function findVertices which refines possible the moves of every node
by removing all the conditions imposed for traversing. Initially defining all the 
moves and setting its appropriate (x,y) values and it's cost.
'''
def findVertices( x, y, node,n,nodes):
    v1 = vertex("D", x + 1, y, 2);
    v2 = vertex("U", x - 1, y, 2);
    v3 = vertex("RU", x - 1, y + 1, 1);
    v4 = vertex("LU", x - 1, y - 1, 1);
    v5 = vertex("L", x, y - 1, 2);
    v6 = vertex("LD", x + 1, y - 1, 1);
    v7 = vertex("R", x, y + 1, 2);
    v8 = vertex("RD", x + 1, y + 1, 1);
    validMoves = [v1, v2, v3, v4, v5, v6, v7, v8]; #A list which has all the possible moves

    # check if moving Down is possible
    if x + 1 < n: #check if moving down is within the size of the matrix
        if str(nodes[x + 1][y].type) == ("X"): #check if the tile is a mountain, eliminate those moves as we can't move to a mountainous tile
            if v1 in validMoves:
                validMoves.remove(v1)
            if v6 in validMoves:
                validMoves.remove(v6)
            if v8 in validMoves:
                validMoves.remove(v8)
    else: #if moving down exceeds the size of the matrix, eliminate those moves
        if v1 in validMoves:
            validMoves.remove(v1)
        if v6 in validMoves:
            validMoves.remove(v6)
        if v8 in validMoves:
            validMoves.remove(v8)

    # check if moving Up is possible
    if x - 1 >= 0:  #check if moving up is within the size of the matrix
        if nodes[x - 1][y].type == ("X"): #check if the tile is a mountain, eliminate those moves as we can't move to a mountainous tile
            if v2 in validMoves:
                validMoves.remove(v2)
            if v3 in validMoves:
                validMoves.remove(v3)
            if v4 in validMoves:
                validMoves.remove(v4)

    else: #if moving up becomes less than 0 i.e. negative, eliminate those moves
        if v2 in validMoves:
            validMoves.remove(v2)
        if v3 in validMoves:
            validMoves.remove(v3)
        if v4 in validMoves:
            validMoves.remove(v4)

    # check if moving Left is possible
    if y - 1 >= 0:  #check if moving left is within the size of the matrix
        if nodes[x][y - 1].type == ("X"): #check if the tile is a mountain, eliminate those moves as we can't move to a mountainous tile
            if v4 in validMoves:
                validMoves.remove(v4)
            if v5 in validMoves:
                validMoves.remove(v5)
            if v6 in validMoves:
                validMoves.remove(v6)

    else: #if moving left becomes less than 0 i.e. negative, eliminate those moves
        if v4 in validMoves:
            validMoves.remove(v4)
        if v5 in validMoves:
            validMoves.remove(v5)
        if v6 in validMoves:
            validMoves.remove(v6)

    # check if moving Right is possible
    if y + 1 < n:  #check if moving right is within the size of the matrix
        if nodes[x][y + 1].type == ("X"): #check if the tile is a mountain, eliminate those moves as we can't move to a mountainous tile
            if v3 in validMoves:
                validMoves.remove(v3)
            if v7 in validMoves:
                validMoves.remove(v7)
            if v8 in validMoves:
                validMoves.remove(v8)

    else: #if moving right exceeds the size of the matrix, eliminate those moves
        if v3 in validMoves:
            validMoves.remove(v3)
        if v7 in validMoves:
            validMoves.remove(v7)
        if v8 in validMoves:
            validMoves.remove(v8)

    #iterate over the valid moves and set the source node vector
    for v in validMoves:
        v.setSourceNode(nodes[v.x][v.y])

    for v in validMoves:

        try:
            if str(nodes[v.x][v.y].type) == ("X"): #if moving over a mountainous tile, eliminate that move
                validMoves.remove(v)

        except:
            print("")

    node.vertices = validMoves;

#defining a class node
class node:
    def __init__(self,nodeId,nodeType): #initializing the nodeid, nodetype, g, f, and h cost, parent node, path, path cost and vertices
        self.id=nodeId;
        self.type=nodeType;
        self.g = None
        self.parent = None
        self.f = None
        self.cost=0
        self.path= ""
        self.vertices = [];

    def EvaluateHval(self, xVal, yVal, targetX,targetY): #calculating the heuristic value using Euclidean distance
        self.hVal = abs(math.sqrt(math.pow((xVal-targetX), 2) +math.pow((yVal-targetY),2)))

    def setStats(self,initialCost,costToReachNode,parentNode,cost,path): #defining a function which calculates the f,g,h cost values and sets the path
        if(self.f==None):
            self.g=initialCost+costToReachNode;
            self.f=self.g+self.hVal
            self.parent=parentNode
        else:
            if self.f>initialCost + costToReachNode+self.hVal:

                self.g = initialCost + costToReachNode;
                self.f = self.g + self.hVal
                self.parent = parentNode
        self.cost=cost
        self.path=path

    def printChildren(self): #displaying the children nodes and the path traversed
        children="Children:{"
        for vertex in self.vertices:
            children= children + vertex.newNode.id +":" + self.path + "-" + vertex.vertexName + ","

        if(children.endswith(",")):
            children=children[:len(children)-1]
        children=children+"}"
        return children

    def printNodeInfo(self): #dispay the node id, path traversed and g,h,f costs
        return self.id + ":" + self.path + " " + str(self.g) + " " + str(self.hVal) + " " + str(self.f)

# defining a class vertex which takes the node name, (x,y) co-ordinates of the next node and the cost to reach the next node
class vertex:
    def __init__(self,name,x,y,c):
        self.vertexName=name;
        self.x=x
        self.y=y
        self.vertexCost=c;

    def setSourceNode(self,node):
        self.newNode=node

#defining a method graphSearch that calculates the costs and gives the best path for reaching from the source node to the target node
def graphsearch(map, flag):
    solution = "" #the string which stores and displays the output in the output file
    initialCost=0

    #get the source and target nodes from the map
    sourceNode=map.get('nodes')[map.get('sourceX')][map.get('sourceY')]
    targetNode=map.get('nodes')[map.get('targetX')][map.get('targetY')]

    #initialize an open list and a closed list
    openList=[]
    closedList = []

    openList.append(sourceNode) #Add the start node on the open list
    currNode = openList[0] #set the current node as the 1st element of open list
    currNode.setStats(initialCost,initialCost,None,0,"S")  #set the start node as the current node and start the path from 'S'

    #Loop until the end node is found
    while(len(openList)>0):

	#iterate over the list of vertices, if a vertex is not in open or closed list, add it to closed list
        for vertex in currNode.vertices:
            if(vertex.newNode not in openList and vertex.newNode not in closedList):
                vertex.newNode.setStats(currNode.g,vertex.vertexCost,currNode,currNode.cost+vertex.vertexCost,currNode.path+"-"+vertex.vertexName)
                openList.append(vertex.newNode)

	#remove the nose which is already traversedfrom the open list and add to closed list
        openList.remove(currNode)
        closedList.append(currNode)

        # displaying the output on console
        if (flag > 0):
            print("--------")
            print(currNode.printNodeInfo())
            print(currNode.printChildren())

            # displaying the open and closed lists
            openListdisplay = "OPEN: {"
            if (len(openList) > 0):
                for node in openList:
                    openListdisplay = openListdisplay + "(" + node.printNodeInfo() + "),"
            if (openListdisplay.endswith(",")):
                openListdisplay = openListdisplay[:len(openListdisplay) - 1]

            openListdisplay = openListdisplay + "}"
            print(openListdisplay)

            closedListdisplay = "CLOSED: {"
            if (len(closedList) > 0):
                for node in closedList:
                    closedListdisplay = closedListdisplay + "(" + node.printNodeInfo() + "),"
            if (closedListdisplay.endswith(",")):
                closedListdisplay = closedListdisplay[:len(closedListdisplay) - 1]

            closedListdisplay = closedListdisplay + "}"
            print(closedListdisplay)
            flag = flag - 1

        if len(openList)==0:
            return "No Available Path"

        min = openList[0].f
        for v in openList:
            if (v.f <= min):
                min = v.f
                vmin = v
        currNode = vmin

	#target node found, now backtracking to get the entire path and store it in the string 'solution'
        if(currNode==targetNode):
            temp=currNode.path + "-G " + str(currNode.cost)
            while(currNode!=None):
                solution=currNode.path+" "+str(currNode.cost)+"\n"+solution

                graphString = ""
                for x in range(map.get('size')):
                    for y in range(map.get('size')):
                        if (map.get('nodes')[x][y] == currNode):
                            graphString = graphString + "*,"
                        else:
                            graphString = graphString + map.get('nodes')[x][y].type + ","
                    graphString = graphString[:len(graphString) - 1]
                    graphString = graphString + "\n"
                solution = "\n" +graphString + "\n" + solution
                currNode=currNode.parent
            solution = solution +temp


            return solution

    pathParent=currNode
    return "No Available Path"


#defining a function which reads the file and finds all the possible moves from each node.
def read_from_file(file_name):
    file_handle = open(file_name)
    lines = file_handle.readlines()  #read all the lines from the input file and store them in an array
    size = int(lines[0])  #the first line indicates the size of the matrix
    nodes = [[0 for i in range(size)] for j in range(size)] #Creating a 2D array of size nXn
    graph={'size':size,'nodes':nodes}
    nodeNumber = 1
    xVal = 0

    #iterate over the lines of the input file
    for i in range(1, size + 1):
        line = str(lines[i])
        line = line.replace("\n", "")
        yVal = 0

        #iterte over each node
        for each in line:
            #set the node ids for each node
            graph.get('nodes')[xVal][yVal] = node("N" + str(nodeNumber), each)

            #get the source and target vectors
            if (each == "S"):
                graph['sourceX'] = xVal
                graph['sourceY'] = yVal
            if (each == "G"):
                graph['targetX'] = xVal
                graph['targetY'] = yVal

            yVal += 1
            nodeNumber += 1
        xVal += 1

    for x in range(size):
        for y in range(size):

            #find the possible moves from all the nodes and evaluate the heuristic values of the nodes.
            findVertices(x, y, graph.get('nodes')[x][y],size,graph.get('nodes'));
            graph.get('nodes')[x][y].EvaluateHval(x, y, graph['targetX'], graph['targetY'])
    return graph #returns a dictionary with the size of matrix, all the nodes and source and target vectors


###############################################################################

########### DO NOT CHANGE ANYTHING BELOW ######################################

###############################################################################



def write_to_file(file_name, solution):

    file_handle = open(file_name, 'w')

    file_handle.write(solution)



def main():

    # create a parser object

    parser = ap.ArgumentParser()



    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)





    # get all the arguments

    arguments = parser.parse_args()



##############################################################################

# these print statements are here to check if the arguments are correct.

    print("The input_file_name is " + arguments.input_file_name)

    print("The output_file_name is " + arguments.output_file_name)

    print("The flag is " + str(arguments.flag))

#    print("The procedure_name is " + arguments.procedure_name)

##############################################################################



    # Extract the required arguments



    operating_system = platform.system()


    print(operating_system)
    if operating_system == "Windows":

        input_file_name = arguments.input_file_name


        input_tokens = input_file_name.split("\\")
        print(input_file_name)
        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):

            print("Error: input path should be of the format INPUT\input#.txt")

            return -1



        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):

            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):

            print("Error: input path should be of the format INPUT/input#.txt")

            return -1



        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):

            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1



    flag = arguments.flag

    # procedure_name = arguments.procedure_name





    try:

        map = read_from_file(input_file_name) # get the map

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # print(map)



    solution_string = "" # contains solution



    solution_string = graphsearch(map, flag)

    write_flag = 1



    # call function write to file only in case we have a solution

    if write_flag == 1:

        write_to_file(output_file_name, solution_string)



if __name__ == "__main__":
    main()

