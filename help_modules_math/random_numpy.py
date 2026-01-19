import numpy as np

#массивы из 10 чисел с разными диапазонами
nums_1 = np.random.random(6)
print(nums_1)

nums_2 = np.random.randint(5, 10, size = 10)
print(nums_2)

#массив из 20 случайных чисел от 1 до 100
nums_3 = np.random.randint(1, 100, size = 20)
print(nums_3)

#нормальное распределение
nums_4 = np.random.normal(loc = 0, scale = 1, size = 100)
print(nums_4)

print(f'Среднее значени {np.mean(nums_4)}')
print(f'Стандартное отклонение {np.std(nums_4)}')

#Случайная выборка
arr_1 = np.array([1,2,3,4,5])

print(np.random.choice(arr_1, size = 10, replace = True))

#Случайная перестановка
arr_2 = np.array([1,2,3,4,5,6,7,8,9,10])

per_arr = np.random.permutation(arr_2)
print(f'Изначальный массив {arr_2} Массив с перестановкой {per_arr}')

#Матрица с нормальным распределением
normal_matrix = np.random.normal(loc = 0, scale = 1, size = (5, 5))
print(normal_matrix)

#Бинормальное распределение
binormal_arr = np.random.binomial(n = 5, p = 0.5, size = 1000)
print(binormal_arr)