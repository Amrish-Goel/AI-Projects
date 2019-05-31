import time
from functools import wraps
from collections import defaultdict, Counter
import sys
import copy
import numpy as np
from collections import defaultdict, Counter
import sys
import copy
import numpy as np

best_score = -1
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time() * 1000
        func(*args, **kwargs)
        end = time.time() * 1000
        print "Time taken by {} is {} ms".format(func.__name__, str(end - start))
    return wrapper


def parse_input(input_file):
    with open(input_file) as fp:  
        line = fp.readline()
        cnt = 1
        while line:
            # print("Line {}: {}".format(cnt, line.strip()))
            line.strip()
            if (cnt == 1):
                n = int(line)
                scooter_position_counter = np.zeros([n, n],  dtype = int)
       #line = fp.readline()
            if (cnt == 2):
                p = int(line)
            if(cnt == 3):
                s = int(line)
            if (cnt > 3):
                coordinates = line.split(',')
                x = int(coordinates[0])
                y = int(coordinates[1])
                # print(x)
                # print(y)
                scooter_position_counter[x][y]+= 1
            line = fp.readline() 
            cnt += 1
    return n,p,s,scooter_position_counter



class BacktrackingNQueensOptimizedSafetyCheck:
    def __init__(self, N, P, scooter_position_counter):
        self.diagonals = {}
        self.anti_diagonals = {}
        self.rows = {}
        self.columns = {}
        self.N = N
        self.number_of_queens = P
        self.board = [[0 for x in range(N)] for y in range(N)]
        self.board = np.zeros((N,N))
        self.scooter_position_counter = scooter_position_counter
        self.number_of_solutions = 0
        self.activity_score = 0

    def is_cell_safe(self, r, c):
        if r in self.rows:
            return False
        if c in self.columns:
            return False
        if r - c in self.diagonals:
            return False
        if r + c  in self.anti_diagonals:
            return False

        return True

    def place_a_queen(self, r, c):
        self.rows[r] = True
        self.columns[c] = True
        self.diagonals[r - c] = True
        self.anti_diagonals[r + c] = True
        self.board[r][c] = 1
        self.activity_score += self.scooter_position_counter[r][c]

    def undo_placing_a_queen(self, r, c):
        del self.rows[r]
        del self.columns[c]
        del self.diagonals[r - c]
        del self.anti_diagonals[r + c]
        self.board[r][c] = 0
        self.activity_score -= self.scooter_position_counter[r][c]

    @timer
    def run(self):
        self.solve(0,0)

    def solve(self, column, no_of_queens_placed):
        global best_score
        if no_of_queens_placed == self.number_of_queens or column == self.N:
            self.number_of_solutions += 1
            best_score = max(self.activity_score, best_score) 
            return self.activity_score

        if(self.number_of_queens == self.N):
            for i in range(self.N):
                if self.is_cell_safe(i, column):
                    self.place_a_queen(i, column)
                    self.solve(column + 1, no_of_queens_placed + 1)
                    self.undo_placing_a_queen(i, column)
        else:
            for column in range(self.N - self.number_of_queens + no_of_queens_placed + 1):
                for i in range(self.N):
                    if (self.is_cell_safe(i, column) and self.scooter_position_counter[i, column] != 0) :
                        self.place_a_queen(i, column)
                        self.solve(column + 1, no_of_queens_placed + 1)
                        self.undo_placing_a_queen(i, column)

    def get_number_of_solutions(self):
        return self.number_of_solutions

if __name__ == "__main__":
    # input_file = sys.argv[1]
    n,p,s,scooter_position_counter = parse_input("input3.txt")
    n = int(n)
    p = int(p)

    print(scooter_position_counter)
    board = np.zeros((n,n))
    solver = BacktrackingNQueensOptimizedSafetyCheck(n, p, scooter_position_counter)
    solver.run()
    print (best_score)
    ofile = open ("output.txt", "w")
    output = best_score
    ofile.write('%s' %output)
    ofile.close()
