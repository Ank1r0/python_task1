import numpy as np  # %%
import numpy as np

# %%
raw_data = np.arange(15)
print(f"raw data:{raw_data}")

# %%
# 1. Дан случайный массив, поменять знак у элементов, значения которых между 3 и 8
task1 = raw_data.copy()
task1[3:9] *= -1
print(
    "Task1:Дан случайный массив, поменять знак у элементов, значения которых между 3 и 8"
)
print(f"solution: {task1}")

# 2. Заменить максимальный элемент случайного массива на 0
print("Task2:Заменить максимальный элемент случайного массива на 0")

task2 = raw_data.copy()

task2[task2.argmax()] = 0
print(f"Solution: {task2}")
