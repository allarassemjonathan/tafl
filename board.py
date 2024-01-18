import numpy as np
import math
import copy
import random

class hn_Board():
    def __init__(self, board):
        if board=='':
            self.board = {}
            self.attacker = 1
            self.defender = 2
            self.symbols = [self.attacker, self.defender]
            self.king_pos = (6,6)
            s0 = ['o','o','o','o',self.attacker,self.attacker, self.attacker, self.attacker, self.attacker,'o','o', 'o','o']
            s1 = ['o','o','o','o','o','o', self.attacker,'o', 'o', 'o', 'o', 'o','o']
            s2 = ['o','o','o','o','o','o', 'o','o', 'o', 'o', 'o', 'o','o']
            s3 = [self.attacker,'o', 'o', 'o', 'o', 'o', self.defender, 'o', 'o', 'o', 'o', 'o', self.attacker]
            s4 = [self.attacker, 'o', 'o', 'o', 'o', self.defender, self.defender, self.defender, 'o', 'o', 'o', 'o', self.attacker]
            s5 = [self.attacker, self.attacker, 'o', 'o', self.defender, self.defender, 'K', self.defender, self.defender, 'o', 'o', self.attacker, self.attacker]
            l = [s0, s1, s2, s2.copy(), s3, s4, s5, s4.copy(), s3.copy(), s2.copy() , s2.copy(), s1.copy(), s0.copy()]
            for i,el in enumerate(l):
                self.board[i]=el 
        else:
            self.board = board
    
    def vizualize(self):
        for el in self.board.keys():
            print(list(map(lambda x: str(x).replace('o', ' '), self.board[el])))
    
    def access(self, row:int, col:int):
        position = row*13 + col
        return self.board[position]
    
    def move(self, ini_t:tuple[int], final_t:tuple[int]):
        val = self.board[ini_t[0]][ini_t[1]]
        if val =='K':
            self.king_pos = final_t

        # dont allow for switching pawns TODO
        self.board[ini_t[0]][ini_t[1]] = 'o'
        self.board[final_t[0]][final_t[1]] = val
        return
    
    def eval(self):
        b = self.board
        player = False
        # number of pawns 
        pawns = [x.count(int(player)+1) for x in self.board][0]

        # number of ennemies
        ennemies = [x.count(int(not player)+1) for x in self.board][0]

        #average distance to the king
        mus = []
        for  key in self.board.keys():
            row = self.board[key]
            j = 0
            for el in row:
                if el==1:
                    mus.append((key,j))
                    j = j +1
        
        mus = [math.sqrt(math.pow(e[0]-self.king_pos[0],2)+math.pow(e[1]-self.king_pos[1], 2)) for e in mus]
        mu_king = sum(mus)/len(mus)

        

        return .0
    def corner_score(self, ranging, w0, motif):

        # score how well the left top corner are blocaded
        # get the board top left corner
        v1 = [self.board[i][0:ranging] for i in range(ranging)]
        v = list()
        for el in v1:
            v.extend(el)
        print(v)
        v = ''.join(v)
        if motif==self.symbols[0]:
            curr = self.symbols[1]
        else:
            curr = self.symbols[0]

        # turn empty spots into 0
        v = v.replace('o', '0')

        # turn your spots into 1s
        v = list(v.replace(motif, '1'))
        v1 = [int(el) for el in v]

        # generate the ideal vector for that corner
        v2 = ''.join(['0'*(ranging-1), ('1' + '0'*(ranging-2))*(ranging) ,'0'])
        v2 = [int(el) for el in v2]
        return w0*cosine(v1,v2)
    
    def is_empty(self, el:tuple[int]):
        return el[1] < len(self.board[0]) and el[0] < len(self.board) and self.board[el[0]][el[1]]=='o'
    
    def gen_children(self, attack):
        children = []

        for key in self.board.keys():
            # moving to the left horizontally
            row = self.board[key]
            for j in range(len(row)):
                if row[j]==attack and j-1>= 0 and j < len(self.board[0]) and self.is_empty((key, j-1)):
                    c=1
                    # spot is empty and not out of bounce
                    while self.is_empty((key, j-c)) and j-c>=0:
                        self.move((key, j), (key,j-c))
                        children.append(copy.deepcopy(self.board))
                        self.move((key,j-c), (key, j))
                        c = c+1
            
            # moving to the right horizontally
            row = self.board[key]
            for j in range(len(row)):
                if row[j]==attack  and j+1 < len(self.board[0]) and self.is_empty((key, j+1)):
                    c=1
                    # spot is empty and not out of bounce
                    while self.is_empty((key, j+c)) and j+c< len(self.board[0]):
                        self.move((key, j), (key,j+c))
                        children.append(copy.deepcopy(self.board))
                        self.move((key,j+c), (key, j))
                        c = c+1

        # moving vertically downward
        j = 0
        for key in self.board.keys():
            row = self.board[key]
            j = 0
            for el in row:
                if el==attack and key+1 < len(self.board)-1 and self.is_empty((key+1,j)):
                    i =1
                    while (self.is_empty((key+i, j))):
                        self.move((key,j), (key+i,j))
                        children.append(copy.deepcopy(self.board))
                        self.move((key+i,j), (key,j))
                        i = i+1 
                j=j+1

        # moving vertically upward
        j = 0
        for key in self.board.keys():
            row = self.board[key]
            j = 0
            for el in row:
                if el==attack and key-1 >= 0 and self.is_empty((key-1,j)):
                    i =1
                    while key-i >=0 and (self.is_empty((key-i, j))):
                        self.move((key,j), (key-i,j))
                        children.append(copy.deepcopy(self.board))
                        self.move((key-i,j), (key,j))
                        i = i+1 
                j=j+1
            
        return children


def dot(v,u):
    dot = 0
    for i in range(len(u)):
        dot+= u[i]*v[i]
    return dot

def cosine(v,u):
    return dot(v,u)/(math.sqrt(dot(v,v))* math.sqrt(dot(u,u)) + epsilon)

def random_board_sample(depth=1, player=False):
    table =''
    while depth>0:
        b = hn_Board(table)
        li = b.gen_children(int(player)+1)
        n = random.randrange(len(li))
        next = hn_Board(li[n])
        table = li[n]
        depth= depth-1  
        player = not player
    return next

epsilon = 10e-4

random_board_sample(1000, False).vizualize()



# print('first', board.access(1,7))
# print()
# print()
# board.vizualize()
