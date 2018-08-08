import random
import math
 
# The following code solves a 8-puzzle using best first Search with 3 heuristics
# Heuristic 1 Tiles out of place
# Heuristic 2 Manhattan Distance
# Heuristic 3 Euclidean distance


# The goal state is defined as global and 'b' denotes blank
goal_state = [[1,2,3],[4,5,6],[7,8,'b']]

# Eight puzzle state is considered as a class.Each node denotes an object of the class
class Eightpuzzle:
  #Each node stores the heuristic value and depth of the node.It also points to the parent
  def __init__(self):
    
    self.hval = 0
    self.depth = 0
    self.parent = None
    self.node = [ [0,0,0],[0,0,0],[0,0,0]]

  def set(self,other):
  #  This function sets the node value
     for i in range(3):
       for j in range(3):
          self.node[i][j] =  other[i][j]

  def _find(self,value):   
  # This function finds the location of a value in a node
   
     for row in range(3):
       for col in range(3):
         if self.node[row][col] == value:
           return row, col

  def _clone(self):
  # The parent is cloned to generate a child node with an increment in depth.
  # Legal moves can be applied to the child
    p = Eightpuzzle()
    p.hval = 0
    p.depth = self.depth + 1
    p.parent = self
    for i in range(3):
      for j in range(3):
        p.node[i][j] = self.node[i][j] 
    return p
   
  def _visited(self,item,seq):
  # This function returns if the node is visted or not
     for n in range(len(seq)):
       if (cmp(item.node,seq[n].node) == 0):
         return n
     return -1
      
  def _move_up(self,row,col):
   # Moves the blank space up
    p = self._clone()
   # Swap 
    p.node[row - 1][col],p.node[row][col] = p.node[row][col],p.node[row - 1][col]
    return p

  def _move_down(self,row,col):
   # Moves the blank space down
    p = self._clone()
    p.node[row + 1][col],p.node[row][col] = p.node[row][col],p.node[row + 1][col]
    return p
 
  def _move_left(self,row,col):
    # Moves the blank space Left
    p = self._clone()
    p.node[row][col + 1],p.node[row][col] = p.node[row][col],p.node[row][col + 1]
    return p

  def _move_right(self,row,col):
    # Moves the blank space right
    p = self._clone()
    p.node[row][col - 1],p.node[row][col] = p.node[row][col],p.node[row][col - 1]
    return p


  def _generate_moves(self):
    # Generates successors function for a node
     legal_moves = []
     row,col = self._find('b')
     if row > 0:
        up_move = self._move_up(row,col)
        legal_moves.append(up_move)
     if row < 2:
        down_move = self._move_down(row,col)
        legal_moves.append(down_move)
     if col > 0:
        right_move = self._move_right(row,col)
        legal_moves.append(right_move)
     if col < 2:
        left_move = self._move_left(row,col)
        legal_moves.append(left_move)
     return legal_moves
  
  def _generate_solution_path(self, path):
     # The path to the solution to the goal node is generated
     if self.parent == None:
         return path
     else:
         path.append(self)
         return self.parent._generate_solution_path(path)

  def _heuristic_top(self):
     # This function generates the Tiles out of Place Heuristic value
    h_val = 0
    for i in range(3):
      for j in range(3):
        if self.node[i][j] != goal_state[i][j]:
          h_val = h_val + 1
    if self.node[2][2] != 'b':
      h_val = h_val - 1
    return h_val
  
  def _heuristic_manhattan(self):
     # This function calculates the manhattan distance for a given node
     h_val = 0
     for i in range(3):
       for j in range(3):
         if self.node[i][j] != 'b':
           if self.node[i][j] != goal_state[i][j]:
              c = self.node[i][j] - 1
              target_col = c % 3
              target_row = c / 3
              h_val = h_val + abs(target_row - i) + abs(target_col - j)

     return h_val

  def _heuristic_chebby_shev(self):
     # This function calculates the chebby shev distance heuristics
     h_val = 0
     for i in range(3):
       for j in range(3):
         if self.node[i][j] != 'b':
           if self.node[i][j] != goal_state[i][j]:
              d = 0
              c = self.node[i][j] - 1
              target_col = c % 3
              target_row = c / 3
              d =  max((abs(target_row - i)),(abs(target_col - j)))
              h_val = h_val + d

     return h_val

  
 
  def solve(self,h):
    # The puzzle is solved with a specific heuristic
    openlist = [self]
    closelist = []
    count = 0
     
    # Checks if a puzzle is solved by comparing with the goal state
    def issolved(puzzle):
        if cmp(puzzle.node,goal_state) == 0:
          return 1

    
    while  len(openlist) > 0:      # Loop until we have unexplored nodes
      if count < 1000:		   # Limit the search by setting the depth level by 1000
         x = openlist.pop(0)       # Pop the first node in the sorted openlist
         count = count + 1
         if issolved(x):
           print "Solved"
           if len(closelist) > 0:
                    return x._generate_solution_path([]),x.depth  # If solved generate the solution path
           return []
         else:
          successor_states = x._generate_moves()                #generate successor nodes
          idx_open = idx_closed = - 1
       
          for every_node in successor_states:
         
           idx_open = self._visited(every_node, openlist)      # Check if successor node in open or close list
           idx_closed = self._visited(every_node, closelist)   # Perform the heuristc calculation according to the function
           if h == 1:
            hval = every_node._heuristic_top()               
           elif h == 2:
            hval = every_node._heuristic_manhattan()
           elif h == 3:
            hval = every_node._heuristic_chebby_shev()
           fval = hval 			                       # The evalution function used for best first search
           

           if idx_closed == -1 and idx_open == -1:             # If node is neither in open list or closed list add it to
		                                               #  openlist
              every_node.hval = hval
              openlist.append(every_node)
               
           elif idx_open > -1:                                 # If it is the open list check if it has a different heuristic value
                    
              copy = openlist[idx_open]
              if fval < copy.hval:
         
                 copy.hval = hval
                 copy.parent = every_node.parent
                 copy.depth = every_node.depth

           elif idx_closed > -1:
           
                copy = closelist[idx_closed]
                if fval < copy.hval:         		       # If it is in the closed with a lesser heuristic value add it to open list
                   copy.hval = hval
                   closedlist.remove(copy)
                   openlist.append(every_node)     
          closelist.append(x)
          openlist = sorted(openlist, key=lambda p: p.hval)    #sorts the openlist according to heuristic function 
      else:
        return [0,0] 
                
	    
def main():
   
  for h in range(3):        # The puzzle is solved for all 3 heuristics
   if h == 0:
      print "Tiles Out of place Heuristic"
   elif h == 1:
      print "Manhattan distance"
   elif h == 2:
      print "Chebvy distance"
   Average_Step_Count = 0

   " Five Puzzle Instances are created and run with A*  algorithm"
   puzzle1 = Eightpuzzle()
   puzzle1.set( [[1,2,3],[4,5,7],[8,'b',6]]) # Intial puzzle state is passed
   path,move = puzzle1.solve(h + 1)
   if move > 0:
    path.reverse()
    for i in path:
        print i.node,'->',
    print move
    Average_Step_Count = Average_Step_Count + move
   puzzle2 = Eightpuzzle()
   puzzle2.set( [[1,2,3],[4,6,5],['b',8,7]])
   path,move = puzzle2.solve(h + 1)
   if move > 0:
    path.reverse()
    for i in path:
        print i.node,'->',
    print move
    Average_Step_Count = Average_Step_Count + move
   else:
     print "No solution found"
  
   puzzle3 = Eightpuzzle()
   puzzle3.set( [[1,2,3],[4,6,'b'],[5,8,7]])
   path,move = puzzle3.solve(h + 1)
   if move > 0:
    path.reverse()
    for i in path:
        print i.node,'->',
    print move
    Average_Step_Count = Average_Step_Count + move
   else :
    print "No solution found"

   puzzle4 = Eightpuzzle()
   puzzle4.set( [[1,'b',3],[4,6,2],[5,8,7]])
   path,move = puzzle4.solve(h + 1)
   if move > 0:
    path.reverse()
    for i in path:
        print i.node,'->',
    print move
    Average_Step_Count = Average_Step_Count + move
   else:
    print "No Solution Found for puzzle 4"

   puzzle5 = Eightpuzzle()
   puzzle5.set( [[1,2,5],['b',4,3],[6,8,7]])
   path,move = puzzle5.solve(h + 1)
   if move > 0:
    path.reverse()
    for i in path:
        print i.node,'->',
    print move
    Average_Step_Count = Average_Step_Count + move
   else:
    print "No Solution Found for puzzle 5"
  
   # Prints the average steps required to solve a puzzle 
   print "Average Step Count is",
   print Average_Step_Count/4
    


if __name__ == "__main__":
  main()



