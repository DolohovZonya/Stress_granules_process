# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 14:23:00 2025

@author: User
"""

import pandas as pd
import os


current = "D:/Downloads/stats_sg_merged/K_AMF_16mT_статистика_merged"
        # Путь к папке, где находятся ваши CSV файлы
folder_path = current

# Список для хранения каждого загруженного DataFrame
dfs = []

# Перебираем все файлы в папке
for filename in os.listdir(folder_path):
    print(filename)
    if filename.endswith('.csv'):
        # Извлекаем кусок имени файла (например, Snap-12345)
        file_prefix = filename.split('-')[0] + '-' + filename.split('-')[1][:5]  # предполагаем, что формат файла Snap-xxxxx.csv
        file_prefix = file_prefix.replace("statss_", "")
        # Загружаем CSV файл в DataFrame
        df = pd.read_csv(os.path.join(folder_path, filename))
        print(df)
        # Добавляем новый столбец с названием файла
        df.insert(0, 'File_Prefix', file_prefix)
        # Добавляем DataFrame в список
        dfs.append(df)
        
        # Объединяем все DataFrame в один
merged_df = pd.concat(dfs, ignore_index=True)
file_name = "K_AMF_16mT"
# Сохраняем объединенный DataFrame в новый CSV файл
merged_df.to_csv(current + "/" +f'{file_name}_merged_new.csv', index=False)

print(f"Файлы успешно объединены в {file_name}.csv с добавленным столбцом.")