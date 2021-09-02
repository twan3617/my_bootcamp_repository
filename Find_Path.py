'''The FIND_PATH algorithm is as follows: FIND_PATH(x, y) 
    1. 	if (x,y outside maze) return false 
    2. 	if (x,y is goal) return true 
    3. 	if (x,y not open) return false 
    4. 	mark x,y as part of solution path 
    5. 	if (FIND-PATH(North of x,y) == true) return true 
    6. 	if (FIND-PATH(East of x,y) == true) return true 
    7. 	if (FIND-PATH(South of x,y) == true) return true 
    8. 	if (FIND-PATH(West of x,y) == true) return true 
    9. 	unmark x,y as part of solution path 
    10. return false 
    Our solution can be improved vastly. We should be able to provide the code with a text file or 
    csv file that defines a grid, rather than hard coding it ourselves. We should be able to deal with 
    non-square grids. There should also be an implementation of a "shortest path" algorithm (e.g. Dijkstra's)'''
import matplotlib.pyplot as plt
import time as time


grid = [[0, 0, 0, 1, 0, 1],
        [1, 1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1],
        [0, 0, 0, 0, 1, 1],
        [0, 1, 0, 0, 0, 2]]

xlen = len(grid) - 1 # first assume square 

# use 0 as empty space, 1 as walls, 2 as end goal, 3 as visited. 
def find_path(x, y):
    # if required: import grid as global variable
    if (x > xlen or y > xlen or x < 0 or y < 0): #(x,y) outside maze
        return False 
    elif grid[x][y] == 2: #Goal reached
        print(f"Goal reached at ({x},{y})!")
        return True
    elif grid[x][y] == 1: #Wall 
        print(f"Wall at ({x},{y}). \n ")
        return False 
    elif grid[x][y] == 3: #Already visited
        print(f"Already visited at ({x},{y}). \n")
        return False

    grid[x][y] = 3 #visited 
    # animation!
    plt.pcolormesh(grid)
    plt.axes().set_aspect('equal') #set the x and y axes to the same scale
    plt.xticks([]) # remove the tick marks by setting to an empty list
    plt.yticks([]) # remove the tick marks by setting to an empty list
    #plt.axes().invert_yaxis() #invert the y-axis so the first row of data is at the top
    plt.show(block = False)    
    plt.pause(0.5)

    print(f"({x},{y}) visited.\n")

    if find_path(x,y+1) == True: #East
        return True
    if find_path(x+1,y) == True: #South
        return True
    if find_path(x,y-1) == True: #West
        return True
    if find_path(x-1,y) == True: #North
        return True 
    
    grid[x][y] = 0 #backtrack
    print(f"({x},{y}) backtracked.\n") 
    return False
        


def main():
    if __name__ == "__main__":
        find_path(0,0) 


main()