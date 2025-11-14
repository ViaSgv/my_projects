import numpy as np
import matplotlib.pyplot as plt


#График функции
x = np.linspace(-10, 10, 100)
y = x ** 2

plt.plot(x, y)
plt.title('График')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

plt.show()

#Несколько графиков
x = np.linspace(0, 5, 100)

y1 = x
y2 = x ** 2
y3 = x ** 3

plt.plot(x, y1)
plt.plot(x, y2)
plt.plot(x, y3)

plt.title('Графики')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)

plt.show()

#Гистограмма с нормальным распределением
normal_arr = np.random.normal(loc = 0, scale = 1, size = 1000)

plt.hist(normal_arr, bins = 50, color = 'red')
plt.title('Гистограмма')
plt.xlabel('x')
plt.ylabel('y')
plt.show()

#Круговая диграмма
nums =  [25, 35, 20, 20]
labels = ['A', 'B', 'C', 'D']

plt.pie(nums, labels = labels)
plt.title('Круговая диаграмма')
plt.show()

#Диаграмма рассеяния
x = np.random.rand(100)
y = np.random.rand(100)

plt.scatter(x, y)

plt.title('Диграмма рассеяния')
plt.xlabel('x')
plt.ylabel('y')

plt.show()

#График функции y = sin(x) с легендой графика
x = np.linspace(0, 4*np.pi, 100)

y = np.sin(x)

plt.plot(x, y,'r--', label = 'y=sin(x)')

plt.xlabel('x')
plt.ylabel('y')
plt.title('График y=sin(x)')
plt.legend()

plt.show()

#Построение 4ёх графиков в одном окне
x = np.linspace(0, 10, 100)

y1 = np.sin(x)
y2 = np.tan(x)

nums = np.random.normal(0, 10, 100)

x_sc = np.random.rand(100)
y_sc = np.random.rand(100)

nums_pie =  [25, 35, 20, 20]
labels_pie = ['A', 'B', 'C', 'D']

fig, axes = plt.subplots(2, 2, figsize = (10, 10))

axes[0,0].plot(x, y1, 'b-', label = 'y=sin(x)')
axes[0,0].plot(x, y2, 'r-', label = 'y=tg(x)')
axes[0,0].set_title('Графики y(x)')
axes[0,0].set_xlabel('x')
axes[0,0].set_ylabel('y')
axes[0,0].legend()


axes[0,1].hist(nums, color = 'red')
axes[0,1].set_title('Гистограмма')
axes[0,1].set_xlabel('x')
axes[0,1].set_ylabel('y')


axes[1,0].scatter(x_sc, y_sc, color = 'orange')
axes[1,0].set_title('Диграмма рассеяния')
axes[1,0].set_xlabel('x')
axes[1,0].set_ylabel('y')

axes[1,1].pie(nums_pie, labels = labels_pie)
axes[1,1].set_title('Круговая диаграмма')

plt.suptitle('4 графика')

plt.show()