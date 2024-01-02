# Only solution for part 2; part 1 was same but with simpler worry level
# reduction (always divide by three) and less rounds to calculate
# Link to the Advent of Code site with detailed explanation of the problem:
# https://adventofcode.com/2022/day/11
#
# Import heap sort
import heapq

# Open the input file and read line by line
with open('input.txt') as f:
    lines = f.readlines()
  
# Gather the relevant information from the input
# The division operators for each monkey            
comparison=[13,11,2,5,7,3,19,17]
# Collection of all items' worry levels
items=[]
# Evaluate items for each monkey separately
for i in range(8):
    # Collection of items for the current monkey
    item=[]
    # Extract each word and value in the starting items-line for the current 
    # monkey
    si=lines[i*7+1].split()
    # Evaluate the items one by one
    for s in range(2,len(si)):
        # Current item
        startingvalue=int(si[s][0:2])
        # Comparison value of the current item to each monkey
        mods=[]
        for q in range(8):
            # Calculate the remainder of the current item per comparison value 
            mods=mods+[startingvalue % comparison[q]]
        # Add all the remainders into the collection
        item=item+[mods]
    # Add the current monkey's items to the collection of all items
    items=items+[item]
  
# Function for updating the worry levels after an inspection
# wl: current worry level
# mul: value to multiply by, defaults to 1
# add: value to add, defaults to 0
# square: used for monkey 2, where the old value is squared
def update (wl, mul=1, add=0, square=False):
    # Quadratic residue tables from https://en.wikipedia.org/wiki/Quadratic_residue
    if square:
        # Update each worrylevel by using the quadratic residue tables
        # wl[0], 13
        rem=[0,1,4,9,3,12,10,10,12,3,9,4,1]
        wl[0]=rem[wl[0]]
        
        # wl[1], 11
        rem=[0,1,4,9,5,3,3,5,9,4,1] 	
        wl[1]=rem[wl[1]]
        
        # wl[2], 2
        rem=[0,1]
        wl[2]=rem[wl[2]]
        
        # wl[3], 5
        rem=[0,1,4,4,1]
        wl[3]=rem[wl[3]]
        
        # wl[4], 7
        rem=[0,1,4,2,2,4,1] 	
        wl[4]=rem[wl[4]]
        
        # wl[5], 3
        rem=[0,1,1]
        wl[5]=rem[wl[5]]
        
        # wl[6], 19
        rem=[0,1,4,9,16,6,17,11,7,5,5,7,11,17,6,16,9,4,1]
        wl[6]=rem[wl[6]]
        
        # wl[7], 17
        rem=[0,1,4,9,16,8,2,15,13,13,15,2,8,16,9,4,1]
        wl[7]=rem[wl[7]]
    else:
        # Multiply and add, then take the remainder and return that
        for i in range(8):
            wl[i]=(wl[i]*mul) % comparison[i]
            wl[i]=(wl[i]+add) % comparison[i]
    return wl

# Function for carrying out the inspection and evaluating the new recipient
# id: active monkey
# wl: current item's worry level
# Each monkey has its own operation, test and throws the item to different
# recipients. The operation and test are handled mostly in the update-function,
# but partly the comparison is done here. Depending on the active monkey, the
# recipients will be different. Returns the new worry level and recipient of 
# the item.
def inspect (id, wl):
    recip=0
    if id==0:
        wl = update(wl,mul=11)
        if wl[0] == 0:
            recip=4
        else:
            recip=7
            
    if id==1:
        wl = update(wl,add=4)
        if wl[1] == 0:
            recip=5
        else:
            recip=3
    
    if id==2:
        # Operation is square, so we select the square-parameter
        wl = update(wl, square=True)
        if wl[2] == 0:
            recip=3
        else:
            recip=1
            
    if id==3:
        wl = update(wl,add=2)
        if wl[3] == 0:
            recip=5
        else:
            recip=6
            
    if id==4:
        wl = update(wl,add=3)
        if wl[4]== 0:
            recip=7
        else:
            recip=2
            
    if id==5:
        wl = update(wl,add=1)
        if wl[5] == 0:
            recip=0
        else:
            recip=6
            
    if id==6:
        wl = update(wl,add=5)
        if wl[6] == 0:
            recip=4
        else:
            recip=0
            
    if id==7:
        wl = update(wl,mul=19)
        if wl[7] == 0:
            recip=2
        else:
            recip=1
            
    return(wl, recip)
        
# Keep track of each monkey's activity
activity=[0,0,0,0,0,0,0,0]
for i in range(8*10000):
    # Find the active monkey
    activemonkey = i % 8
    # Go over all the items on the active monkey
    for j in range(len(items[activemonkey])):
        # Find the current item
        item=items[activemonkey][j]
        # Find the new recipient
        [wl, recip] = inspect(activemonkey, item)
        # Add the item to the recipient
        items[recip]=items[recip]+[wl]
        # Add to the activity
        activity[activemonkey]+=1
        
    # Remove items from active monkey
    items[activemonkey]=[]
    
# Find the two largest activities and print them
print(heapq.nlargest(2, activity))
# Print the product of the two largest activities
print((heapq.nlargest(2, activity))[0]*(heapq.nlargest(2, activity))[1])