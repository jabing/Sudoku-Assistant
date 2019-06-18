
"""
Solution Features
=========================
    Sudoku solution both for 6 square grid and 9 square gid
    Class input:
        Sudoku(matrix) or
        Sudoku.matrix      # for example a six square grid matrix as below
                                  [ [3, 0, 0, 0, 4, 0],
                                    [0, 5, 0, 0, 6, 0],
                                    [0, 6, 0, 0, 0, 2],
                                    [0, 3, 0, 0, 0, 0],
                                    [0, 0, 2, 0, 0, 6],
                                    [0, 0, 0, 0, 0, 4] ]
    function and output:
        Sudoku.check(x, y, value)   # x, y are position of a target cell, and x is the cell value
           return True/False        # check the value if it's valid in the Row, Col and Square where the value located

        Sudoku.solve()              # Calculate the solve
           return True/False        # if True, the Sudoku.matrix_result will be a correct solve
                                    # if False, the Sudoku problem should be NO correct solve
        Sudoku.matrix        # the correct solve if so.

Author: Jiang JIaping
Data: 2019-06-08
"""

import datetime


class Solution(object):
    def __init__(self, matrix):
        self.matrix = matrix  # input matrix
        self.t = 0
        self.mode = len(matrix)

    def change_cell(self, row, col, value):
        if not value:
            self.matrix[row][col] = 0
            return True
        else:
            self.matrix[row][col] = value if self.check(row, col, value) else 0
            return bool(self.matrix[row][col])

    def check(self, cell_x, cell_y, cell_value):
        for row_item in self.matrix[cell_x]:  # check by Row
            if row_item == cell_value:
                return False
        for row_all in self.matrix:  # check by Col
            if row_all[cell_y] == cell_value:
                return False
        # calculate which Square the cell is located
        row, col = cell_x // (self.mode // 3) * (self.mode // 3), cell_y // 3 * 3
        # get all cell of the Square
        square = self.matrix[row][col:col + 3] + self.matrix[row + 1][col:col + 3]
        if self.mode == 9:
            square += self.matrix[row + 2][col:col + 3]
        for cell_v in square:  # check by Square
            if cell_v == cell_value:
                return False
        return True

    def get_next(self, x, y):  # find the next empty cell
        for next_soulu in range(y + 1, self.mode):
            if self.matrix[x][next_soulu] == 0:
                return x, next_soulu
        for row_n in range(x + 1, self.mode):
            for col_n in range(0, 6):
                if self.matrix[row_n][col_n] == 0:
                    return row_n, col_n
        return -1, -1  # if no empty cell than return value -1

    def try_it(self, x, y):  # calculating main loop
        if self.matrix[x][y] == 0:
            for i in range(1, self.mode + 1):  # try from 1 to the max number 6 or 9
                self.t += 1
                if self.check(x, y, i):  # check cell value is ok template
                    self.matrix[x][y] = i  # fill to answer
                    next_x, next_y = self.get_next(x, y)  # next empty cell
                    if next_x == -1:  # NO empty cell
                        return True  # completed
                    else:  # have empty cell, recursive call to try
                        end = self.try_it(next_x, next_y)
                    if not end:  # back to the previous level and redo it again
                        self.matrix[x][y] = 0
                    else:
                        return True  # Failed, No correct solve

    def solve(self):
        if self.matrix[0][0] == 0:
            self.try_it(0, 0)
        else:
            x, y = self.get_next(0, 0)
            self.try_it(x, y)

        for line in self.matrix:
            for grid in line:
                if grid <= 0:
                    return False
        return True


if __name__ == "__main__":

    def start(sudo):
        begin = datetime.datetime.now()
        result = sudo.solve()
        end = datetime.datetime.now()

        print("the Result is: " + ("Valid input." if result else "Invalid input"))
        for i in sudo.matrix:
            print(i)
        print('\ncost time: ' + str(end - begin))
        print('times: ' + str(sudo.t))
        return


    print("""
    #====================================================
    #    Six Square Grid testing
    #----------------------------------------------------
    """)
    s1 = Sudoku([
        [3, 0, 0, 0, 4, 0],
        [0, 5, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 2],
        [0, 3, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 6],
        [0, 0, 0, 0, 0, 4]
    ])
    print("check single invalid input, result should be False: " + str(s1.check(3, 3, 2)))
    print("check single valid input, result should be True: " + str(s1.check(1, 1, 2)))
    start(s1)

    s3 = Sudoku([
        [3, 0, 0, 0, 4, 0],
        [0, 5, 0, 0, 6, 0],
        [0, 6, 0, 0, 0, 2],
        [0, 3, 0, 2, 0, 0],
        [0, 0, 2, 0, 0, 6],
        [0, 0, 0, 0, 0, 4]
    ])
    start(s3)

    print("""
    #====================================================
    #    Six Square Grid testing
    #----------------------------------------------------
    """)

    s2 = Sudoku([
        [3, 0, 0, 0, 4, 0, 0, 0, 0],
        [0, 5, 0, 0, 6, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 2, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    print("check single invalid input, result should be False: " + str(s2.check(0, 2, 5)))
    print("check single valid input, result should be True: " + str(s2.check(2, 2, 9)))
    start(s2)

    s4 = Sudoku([
        [3, 0, 5, 0, 4, 0, 0, 0, 0],
        [0, 5, 0, 0, 6, 0, 0, 0, 0],
        [0, 6, 0, 0, 0, 2, 0, 0, 0],
        [0, 3, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 2, 0, 0, 6, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ])
    start(s4)
