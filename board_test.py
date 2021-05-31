
import numpy as np 
from board import *
import copy 



b=Board()
#print(b.roll_numbers)



#if a 6 is contained in this location an 8 cannot be contained in the other locations .. 

""" 0:1,3,4
    1:0,2,4,5
    2:1,5,6
    3:0,4,7,8
    4:0,1,3,5,8,9
    5:1,2,4,6,9,20
    6:2,5,10,11
    7:3,8,12
    8:3,4,7,9,12,13
    9:4,5,8,10,13,14
    10:5,6,9,11,14,15
    11:6,10,15
    12:7,8,13,16
    13:8,9,12,14,16,17
    14:9,10,13,15,17,18
    15:10,11,14,18
    16:12,13,17
    17:13,14,16,18
    18:14,15,17
 """

#if a 6 is in one of these locations an 8 cannot be in the list and vice versa
taboo_places={0:[1,3,4],
   1:[0,2,4,5],
   2: [1,5,6],
   3:[0,4,7,8],
   4:[0,1,3,5,8,9],
   5:[1,2,4,6,9,20],
   6:[2,5,10,11],
   7:[3,8,12],
   8: [3,4,7,9,12,13],
   9: [4,5,8,10,13,14],
   10: [15,6,9,11,14,15],
   11: [6,10,15],
   12: [7,8,13,16],
   13: [8,9,12,14,16,17],
   14: [9,10,13,15,17,18],
   15: [10,11,14,18],
   16: [12,13,17],
   17: [13,14,16,18],
   18: [14,15,17]}


#getting the index of 6 and 8 
six_index=[]
eight_index=[]

def see_problem():
  #this method sees where the problem is at what locations
  for num in six_index:
    for elm in taboo_places[num]:
        if b.roll_numbers[elm]==8:
          #redo()
          #print('6 is next to 8')
          problem_point(num,elm)
          

def problem_point(six,eight):
    #we want to make a trade so the 6 and 8 will not be next to each other 
    buffer=19
    for i in range(19):
        if b.roll_numbers[i] not in taboo_places[six]:
          buffer=b.roll_numbers[i]
          i=8
          b.roll_numbers[eight]=buffer
          #print('problem resolved')
          #print(b.roll_numbers)
          break



index=0
for num in b.roll_numbers:
    if num==6:
      six_index.append(index)
    if num==8:
        eight_index.append(index)
    index+=1

see_problem()


        

"""for num in eight_index:
    for elm in taboo_places[num]:
        if b.roll_numbers[elm]==6:
          #redo()
          print('you have 6 next to 8')"""

#def redo(self):
    #pass


