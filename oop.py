from sys import stdin
from copy import deepcopy


class MatrixError(BaseException):
    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class Matrix:
    def __init__(self, list):
        self.list = deepcopy(list)

    def __str__(self):
        rows = []
        for row in self.list:
            rows.append('\t'.join(map(str, row)))
        return '\n'.join(rows)

    def __add__(self, mtr):
        if self.size() == mtr.size():
            rows = deepcopy(self.list)
            for row in range(len(self.list)):
                for i in range(len(self.list[row])):
                    rows[row][i] += mtr.list[row][i]
        else:
            raise MatrixError(self, mtr)
        return Matrix(rows)

    def __mul__(self, n):
        rows = deepcopy(self.list)
        if isinstance(n, int) or isinstance(n, float):
            for row in range(len(self.list)):
                for i in range(len(self.list[row])):
                    rows[row][i] *= n
            return Matrix(rows)

        elif isinstance(n, Matrix):
            if len(self.list[0]) != len(n.list):
                raise MatrixError(self, n)
            zip_b = zip(*n.list)
            zip_b = list(zip_b)
            return Matrix([[sum(ele_a * ele_b for ele_a, ele_b in zip(row_a, col_b))
                            for col_b in zip_b] for row_a in self.list])

    @staticmethod
    def transposed(m):
        return Matrix(list(map(list, zip(*m.list))))

    def transpose(self):
        newList = list(map(list, zip(*self.list)))
        self.list = newList
        return self

    def size(self):
        return len(self.list), len(self.list[0])

    __rmul__ = __mul__

    def solve(self, matrix):
        return self.Gauss(self.list, matrix)

    def SwapRows(self, A, B, row1, row2):
        A[row1], A[row2] = A[row2], A[row1]
        B[row1], B[row2] = B[row2], B[
            row1]  # ---end of перемена местами двух строк системы# ---деление строки системы на число

    def DivideRow(self, A, B, row, divider):
        A[row] = [a / divider for a in A[row]]
        B[
            row] /= divider  # ---end of деление строки системы на число# ---сложение строки системы с другой строкой, умноженной на число

    def CombineRows(self, A, B, row, source_row, weight):
        A[row] = [(a + k * weight) for a, k in zip(A[row], A[source_row])]
        B[row] += B[
                      source_row] * weight  # ---end of сложение строки системы с другой строкой, умноженной на число# ---решение системы методом Гаусса (приведением к треугольному виду)

    def Gauss(self, A, B):
        column = 0
        while (column < len(B)):
            current_row = None
            for r in range(column, len(A)):
                if current_row is None or abs(A[r][column]) > abs(A[current_row][column]):
                    current_row = r
            if current_row is None:
                raise MatrixError(A, B)
                return None

            if current_row != column:
                self.SwapRows(A, B, current_row, column)

            self.DivideRow(A, B, column, A[column][column])

            for r in range(column + 1, len(A)):
                self.CombineRows(A, B, r, column, -A[r][column])

            column += 1
        X = [0 for b in B]
        for i in range(len(B) - 1, -1, -1):
            X[i] = B[i] - sum(x * a for x, a in zip(X[(i + 1):], A[i][(i + 1):]))
        return X


class SquareMatrix(Matrix):
    def __pow__(self, n):
        # start_time = datetime.now()
        # copy=deepcopy(self.list)
        if n == 0:
            for i in range(len(self.list)):
                for j in range(len(self.list[i])):
                    if i == j:
                        self.list[i][j] = 1
                    else:
                        self.list[i][j] = 0
            return self

        # elif n==1500:
        #     n=900
        res = self.matpow(self, n)
        # print(datetime.now() - start_time)
        return res

    def matpow(self, m, p):
        if p == 0:
            return m
        if p == 1:
            return m
        elif p % 2 == 0:  # even
            return self.matpow(m * m, p // 2)
        else:  # odd
            return m * self.matpow(m * m, p // 2)


exec(stdin.read())