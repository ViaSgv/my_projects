import numpy as np

matrix_1 = np.array([[1,5], [4,3]])
matrix_2 = np.array([[2,8], [7,0]])

print(matrix_1)
print(matrix_2)
#сумма
print(matrix_1 + matrix_2)
#разница
print(matrix_1 - matrix_2)
#умножение матриц
print(matrix_1 * matrix_2)

matrix_3 = np.array([[1, 3, 6], [2, 7, 8], [3, 1, 9]])
#транспонированная матрица
print(matrix_3.T)
#обратная матрица
print(np.linalg.inv(matrix_3))

#решение системы уравнений
matrix_4 = np.array([1, 0, 1])
print("Решение ", np.linalg.solve(matrix_3, matrix_4))

#собственные значения и векторы
nums, vectors = np.linalg.eig(matrix_3)
print("Собственные числа ", nums)
print('Собственные векторы ', vectors)
