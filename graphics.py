import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv("9x9_5.csv", index_col=False)

df = data[:500]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# График длины пути
ax1.plot(df['DFS_len'], label='DFS Length', color='blue')
ax1.plot(df['BFS_len'], label='BFS Length', color='orange')
ax1.plot(df['AStar_len'], label='A* Length', color='green')
ax1.set_title('Path Length for Different Algorithms')
ax1.set_xlabel('Experiment')
ax1.set_ylabel('Path Length')
ax1.set_ylim(0, df[['DFS_len', 'BFS_len', 'AStar_len']].max().max() + 5)
ax1.legend()

# График времени выполнения
ax2.plot(df['DFS_time'], label='DFS Time', color='blue')
ax2.plot(df['BFS_time'], label='BFS Time', color='orange')
ax2.plot(df['AStar_time'], label='A* Time', color='green')
ax2.set_title('Execution Time for Different Algorithms')
ax2.set_xlabel('Experiment')
ax2.set_ylabel('Time (seconds)')
ax2.set_ylim(0, df[['DFS_time', 'BFS_time', 'AStar_time']].max().max()+0.001)
ax2.legend()

# Отображение графиков
plt.tight_layout()  # Автоматическая настройка отступов
plt.show()
