# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:10:13 2025

@author: User
"""

# %%
import os
import pandas as pd

folder = "D:/Downloads/сг_фильтр_большой_эллипс"


for papka in os.listdir(folder):
    name = papka.replace("_filtered_big_SG_stat_new","")
    for table in os.listdir(folder + "/" + papka):
        table_path = folder + "/" + papka + "/" + table
        df = pd.read_csv(table_path)
        group = [name] * len(df)
        df['Group'] = group
        df.to_csv(table_path)
# %%
import os
import pandas as pd

folder = "D:/Downloads/сг_фильтр_большой_эллипс"
structures = ['CA', 'Cerebellum', 'Cortex', 'DG', 'Midbrain', 'ob', 'Striatum', 'Thalamus']

# Цикл по структурам мозг
for st in structures:
    dfs = []  # Очищаем список для каждой структуры
    for papka in os.listdir(folder):
        name = papka.split("_")[0]
        folder_path = os.path.join(folder, papka)  # Полный путь к папке
        if not os.path.isdir(folder_path):
            continue  # Пропускаем файлы, если есть

        # Цикл по файлам в папке
        for table in os.listdir(folder_path):
            table_path = os.path.join(folder_path, table)
            if st in table_path:  # Проверяем, относится ли файл к текущей структуре
                try:
                    df = pd.read_csv(table_path)
                    dfs.append(df)
                except Exception as e:
                    print(f"Ошибка при чтении {table_path}: {e}")

    # Проверяем, есть ли данные для объединения
    if dfs:
        merged_df = pd.concat(dfs)
        output_path = os.path.join(folder, f'{st}_filtered_merged_new.csv')
        merged_df.to_csv(output_path, index=False)
        print(f"Файл сохранен: {output_path}")
    else:
        print(f"Нет данных для структуры {st}, пропускаем.")
        
        
        
# %%import os
import pandas as pd

folder = "D:/Downloads/статистика_эксперимент_сг_старвейшн_динамика_и_голод"
structures = ['CA', 'Cerebellum', 'Cortex', 'DG', 'Midbrain', 'ob', 'Striatum', 'Thalamus']

# Цикл по структурам мозг
for st in structures:
    dfs = []  # Очищаем список для каждой структуры
    for papka in os.listdir(folder):
        name = papka.split("_")[0]
        folder_path = os.path.join(folder, papka)  # Полный путь к папке
        if not os.path.isdir(folder_path):
            continue  # Пропускаем файлы, если есть
        # Цикл по файлам в папке
        for table in os.listdir(folder_path):
            table_path = os.path.join(folder_path, table)
            if st in table_path:  # Проверяем, относится ли файл к текущей структуре
                try:
                    # Чтение файла с указанием нужных столбцов
                    df = pd.read_csv(table_path, usecols=lambda column: not column.startswith('Unnamed'))
                    dfs.append(df)
                except Exception as e:
                    print(f"Ошибка при чтении {table_path}: {e}")
    # Проверяtм, есть ли данные для объединения
    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        output_path = os.path.join(folder, f'{st}_merged_new.csv')
        merged_df.to_csv(output_path, index=False)
        print(f"Файл сохранен: {output_path}")
    else:
        print(f"Нет данных для структуры {st}, пропускаем.")

# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder = "D:/Downloads/сг_фильтр_большой_эллипс"
# Загрузка данных
df = pd.read_csv( folder + "/" + "ob_filtered_merged_new.csv") 
print(df)
df = df.drop('File_Prefix', axis=1)
# Функция для расчета средних значений и стандартных отклонений
def calculate_statistics(group_data):
    return group_data.agg(['mean', 'std'])
print(df)
# Группировка и расчет статистики для канала 1
stats_channel_1 = df[df['channel'] == 1].groupby('mouse','Group').apply(calculate_statistics).reset_index()

# Группировка и расчет статистики для канала 2
stats_channel_2 = df[df['channel'] == 2].groupby('mouse','Group').apply(calculate_statistics).reset_index()
len_df = len(stats_channel_1)
channels = [1,2] * int(len_df / 2)
stats_channel_1['Channel'] = channels
stats_channel_1 = stats_channel_1.drop('channel', axis=1)

len_df = len(stats_channel_2)
channels = 1 * int(len_df)
stats_channel_2['Channel'] = channels
stats_channel_2 = stats_channel_2.drop('channel', axis=1)
# Сохранение результатов в CSV файлы
stats_channel_1.to_csv(folder + "/" + "stats_channel_1_filtered_ob_mouse.csv")
stats_channel_2.to_csv(folder + "/" + "stats_channel_2_filtered_ob_mouse.csv")

print(stats_channel_1)
print(stats_channel_2)

# %%


import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder = "D:/Downloads/статистика_эксперимент_сг_старвейшн_динамика_и_голод"
structures = ['CA', 'Cerebellum', 'Cortex', 'DG', 'Midbrain', 'ob', 'Striatum', 'Thalamus']
for st in structures:
# Загрузка данных
    data = pd.read_csv( folder + "/" + f"stats_channel_{st}_mouse.csv")  # Замените на путь к вашему файлу
    
    # Преобразуем названия столбцов, если есть пробелы или лишние символы
    data.columns = data.columns.str.strip()
    
    # Строим боксплоты для каждого числового параметра отдельно
    metrics = [
        "total_particles", "num_unique_cores", 
        "ratio_particles_to_unique_cores", "ratio_unique_cores_to_total_cores"
    ]
    
    # Устанавливаем стиль
    sns.set_style("whitegrid")
    
    for metric in metrics:
        plt.figure(figsize=(32, 8))
        sns.lineplot(data=data, x="Group", y=metric, hue="Channel", palette="Set2")
        title = f"{metric}_{st}"
        plt.title(title)
        plt.xlabel("Group")
        plt.ylabel(metric)
        plt.legend(title="Channel")
        plt.savefig(f"D:/Downloads/статистика_эксперимент_сг_старвейшн_динамика_и_голод/картиночки/{title}.png")
        plt.show()

# %%
# %%
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

folder = "D:/Downloads/сг_фильтр_большой_эллипс"
df = pd.read_csv(folder + "/" + "ob_filtered_merged_new.csv") 

# Удаляем ненужный столбец
if 'File_Prefix' in df.columns:
    df = df.drop('File_Prefix', axis=1)
# Функция для расчета статистики (среднее и std)
def calculate_statistics(group_data):
    return group_data.agg(['mean', 'std','se'])

# Группировка по мышам и группам для каждого канала
stats_channel_mean = df.groupby(['mouse', 'Group','channel']).mean().reset_index()
stats_channel_std = df.groupby(['mouse', 'Group','channel']).std().reset_index()
stats_channel_sem = df.groupby(['mouse', 'Group','channel']).sem().reset_index()
stats_channel_mean['level_2'] = 'mean'
stats_channel_std['level_2'] = 'std'
stats_channel_sem['level_2'] = 'se'
# print(stats_channel_1_std)
stat_channel = pd.concat([stats_channel_mean,stats_channel_mean,stats_channel_sem])

stat_channel.columns = stat_channel.columns.str.strip()
stat_channel.to_csv(folder + "/" + "stats_channel_ob_filtered_mouse_w_sem.csv", index=False)

# stats_channel_2 = df[df['channel'] == 2].groupby(['mouse', 'Group']).apply(calculate_statistics).reset_index()

# Добавляем информацию о канале
# stats_channel_1['Channel'] = 1
# stats_channel_2['Channel'] = 2

# merged_df = pd.concat([stats_channel_1, stats_channel_2], ignore_index=True)
# merged_df.to_csv(folder + "/" + "stats_channel_Midbrain_mouse.csv", index=False)
# Сохраняем результаты
# stats_channel_1.to_csv(folder + "/" + "stats_channel_1_ob_mouse.csv", index=False)
# stats_channel_2.to_csv(folder + "/" + "stats_channel_2_ob_mouse.csv", index=False)

# # Выводим для проверки
# print(stats_channel_1)
# print(stats_channel_2)
# %%

import pandas as pd
import numpy as np

# Предположим, что у вас есть DataFrame df

def calculate_statistics(group_data):
    mean_values = group_data.mean()
    std_values = group_data.std()
    n = len(group_data)  # количество наблюдений
    se_values = std_values / np.sqrt(n)  # стандартная ошибка

    # Объединяем результаты в один DataFrame
    stats = pd.DataFrame({
        'mean': mean_values,
        'std': std_values,
        'se': se_values
    })
    
    return stats

# Группировка по мышам и группам для каждого канала
stats_channel_1 = df[df['channel'] == 1].groupby(['mouse', 'Group']).apply(calculate_statistics).reset_index()
stats_channel_2 = df[df['channel'] == 2].groupby(['mouse', 'Group']).apply(calculate_statistics).reset_index()

stats_channel_1 = stats_channel_1[stats_channel_1['level_2'] != 'channel']

# Преобразуем DataFrame с помощью метода pivot
stats_channel_1 = stats_channel_1.pivot_table(index=['mouse', 'Group'], 
                           columns='level_2', 
                           values=['mean', 'std', 'se'])

# Упрощаем MultiIndex в столбцах
stats_channel_2.columns = [f'{stat}_{level}' for stat, level in stats_channel_1.columns]

stats_channel_2 = stats_channel_2.pivot_table(index=['mouse', 'Group'], 
                           columns='level_2', 
                           values=['mean', 'std', 'se'])

# Упрощаем MultiIndex в столбцах
stats_channel_2.columns = [f'{stat}_{level}' for stat, level in stats_channel_2.columns]

merged_df = pd.concat([stats_channel_1, stats_channel_2], ignore_index=True)
merged_df.to_csv(folder + "/" + "stats_channel_Midbrain_mouse_nnn.csv", index=False)


