from pysat.solvers import Glucose3
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from itertools import combinations
import numpy as np
import random
import time


"""
KN(k,n) = U(k,n) ^ L(k,n)
KN(k,n): k out of n adjacent unknown squares are mines
U(k,n): At most k out of n squares contain a mine
L(k,n): At least k out of n squares contain a mine

Conversion to at least
The proposition holds True if and only if k > 0 and k + 1 <= n
U(k,n): For any k+1 squares out of n, at least one is not a mine
L(k,n): For any n-(k-1) squares out of n, at least one is mine

With the problem: The number of unknown squares = The number of adjacent squares
"""

class Puzzle_Solver:
    def __init__(self, shape):
        """
        Input:
            shape: A tuple of 2 integers. E.g: (4, 5)
        """
        self.shape = shape
        self.matrix = np.zeros(shape)
        self.model = list()

    def isValid(self, x, y):
        """
        Input:
            x, y: integers
            shape: The shape of the matrix
        Output:
            Returns True if x, y are valid matrix indices. Otherwise, returns False
        """
        return x >= 0 and y >= 0 and x < self.shape[0] and y < self.shape[1]

    def createPuzzle(self, threshold=20):
        """
        Input:
            shape: A tuple of 2 integers. E.g: (4, 5)
            threshold: A threshold to use probability when generating a random number 
        Output:
            puzzle: A numpy array
        """
        print('Creating a puzzle...')
        dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        dy = [0, 0, 0, -1, -1, -1, 1, 1, 1]
        num_rows = self.shape[0]
        num_cols = self.shape[1]
        
        for x in range(num_rows):
            for y in range(num_cols):
                rand = random.randint(0, 99)
                
                if rand < threshold:
                    self.matrix[x][y] = True
                else:
                    self.matrix[x][y] = False
        
        
        # Count the number of adjacent squares and stores it in arr
        arr = np.zeros(shape=self.shape)
        for x in range(num_rows):
            for y in range(num_cols):
                for k in range(9):
                    if self.isValid(x+dx[k], y+dy[k]) and self.matrix[x+dx[k]][y+dy[k]]:
                        arr[x][y] += 1
                print(round(arr[x][y]), end=' ')
            print()
        
        self.matrix = arr.astype(int)
        print('A puzzle created!')


    def solve(self):
        """
        Input:
            matrix: A numpy array
        """
        start = time.time()
        g = Glucose3() # A SAT-solver
        
        num_rows = self.shape[0]
        num_cols = self.shape[1]
        dx = [-1, 0, 1, -1, 0, 1, -1, 0, 1]
        dy = [0, 0, 0, -1, -1, -1, 1, 1, 1]
        U = list()
        L = list()
        
        for x in range(num_rows):
            for y in range(num_cols):
                adjacents = list()
                for z in range(9):
                    if self.isValid(x+dx[z], y+dy[z]):
                        adjacents.append(1 + (x+dx[z])*num_cols + y+dy[z]) # convert 2d array indexes to 1d array indexes (one-based indexes)
                
                k = int(self.matrix[x][y])
                n = len(adjacents)
                for combination in combinations(adjacents, k+1):
                    U.append({i*-1 for i in combination}) # element-wise multiplication with -1
                
                for combination in combinations(adjacents, n - k + 1):
                    L.append(set(combination))
                
        for clause in np.unique(U):
            g.add_clause(clause)
                
        for clause in np.unique(L):
            g.add_clause(clause)
                
        if not g.solve():
            print('No solutions!')
        else:
            self.model = g.get_model()
            # self.display(model)
            print('Solving time: {} s'.format(time.time() - start))

    
    def display(self):
        print('Showing the solution')
        mod = np.array(self.model).reshape(self.shape)
        mod = mod > 0
        
        fig, ax = plt.subplots()
        
        cmap = ListedColormap(['w', 'g'])
        ax.matshow(mod, cmap=cmap)
        
        num_rows = self.shape[0]
        num_cols = self.shape[1]
        for i in range(num_rows):
            for j in range(num_cols):
                value = self.matrix[i][j]
                ax.text(j, i, value , va='center', ha='center')
        plt.show()


def main():
    solver = Puzzle_Solver(shape=(10, 10))
    solver.createPuzzle(threshold=20)
    solver.solve()
    solver.display()


if __name__ == '__main__':
    main()