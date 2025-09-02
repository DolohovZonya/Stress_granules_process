import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Ваши данные
df = pd.read_csv("stats_channel_ob_filtered_mouse_w_sem.csv")

df = df[df['level_2'] == 'mean']
# df = df[df['channel'] == 1]

# Задаем желаемый порядок групп
# group_order = ['4', '10', '16', '22', 'perk', 'salu']
group_order = ['4', '10', '16', '22']
# Преобразуем Group в категориальный тип с заданным порядком
df['Group'] = pd.Categorical(df['Group'], categories=group_order, ordered=True)

# Сортируем данные согласно заданному порядку
df = df.sort_values(by='Group')

# Создаем фигуру с настроенным размером
plt.figure(figsize=(12, 6), dpi=600)

# Палитра для каналов
channel_palette = {1: '#32CD32', 2: '#DC143C'}  # синий и оранжевый

# Построение отдельных линий для каждого канала
for channel in [1]:
    channel_data = df[df['channel'] == channel]
    sns.lineplot(data=channel_data, x='Group', y='total_particles',
                 estimator='mean', errorbar='sd',
                 linewidth=2.5, marker='o', markersize=8,
                 color=channel_palette[channel],
                 label=f'{channel}',
                 err_kws={'alpha': 0.2})  # полупрозрачные доверительные интервалы

# Настройка осей и заголовка
plt.title('Mean amount of stress granules in OB')
plt.xlabel('Group')
plt.ylabel('Stress granules/structure')

# Легенда внутри графика
plt.legend(title='Channel:', loc='upper right', framealpha=1)

# Устанавливаем правильный порядок на оси X
plt.xticks(range(len(group_order)), group_order)

# Убираем лишние рамки
ax = plt.gca()
ax.spines[['top', 'right']].set_visible(False)

# Автоматическое размещение элементов
plt.tight_layout()

# Сохраняем график в высоком качестве
plt.savefig('particles_by_group_and_channel_ob_wo_inh.svg', bbox_inches='tight', dpi=600)
plt.show()
