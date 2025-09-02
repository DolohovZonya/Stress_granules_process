# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 00:22:36 2025

@author: User
"""

#правильный код
import pandas as pd
import os
import ast  # Для безопасного преобразования строки в список

# Функция для обработки данных
def process_particle_data(file_path, output_folder):
    # Читаем таблицу с координатами ядер и частиц
    df = pd.read_csv(file_path)
    
    # Преобразуем строковые представления списков в настоящие списки
    df['points_count'] = df['points_count'].apply(lambda x: ast.literal_eval(x))
    
    # Создаем колонку с количеством частиц вокруг каждого ядра
    df['num_particles'] = df['points_count'].apply(lambda x: len(x))
    
    # Считаем общее количество частиц на снимке
    total_particles = df['num_particles'].sum()
    
    # Найдем уникальные частицы
    all_particles = [str(p) for sublist in df['points_count'] for p in sublist]
    unique_particles = set([p for p in all_particles if all_particles.count(p) == 1])
    
    # Считаем количество ядер с уникальными частицами
    df['unique_particles'] = df['points_count'].apply(lambda x: len(set(map(str, x)).intersection(unique_particles)))
    num_unique_cores = df[df['unique_particles'] > 0].shape[0]
    
    # Общее количество ядер
    total_cores = df.shape[0]
    
    # Считаем нужные метрики
    ratio_particles_to_unique_cores = total_particles / num_unique_cores if num_unique_cores != 0 else 0
    ratio_unique_cores_to_total_cores = num_unique_cores / total_cores if total_cores != 0 else 0
    
    # Создаем финальный датафрейм с результатами
    result = pd.DataFrame({
        'total_particles': [total_particles],
        'num_unique_cores': [num_unique_cores],
        'ratio_particles_to_unique_cores': [ratio_particles_to_unique_cores],
        'ratio_unique_cores_to_total_cores': [ratio_unique_cores_to_total_cores]
    })
    
    # Формируем имя выходного файла
    if os.path.isdir(output_folder) == False:
        os.mkdir(output_folder)
    output_file = os.path.join(output_folder, os.path.basename(file_path).replace("result", "stats"))
    result.to_csv(output_file, index=False)
    
    return result

# Обрабатываем все файлы в папке
input_folder = 'D:/Downloads/NPs_M@B_CA_AMF_6mT_координаты_фильтрованные'
output_folder = 'D:/Downloads/NPs_M@B_CA_AMF_6mT_статистика_merged'

for filename in os.listdir(input_folder):
    if filename.endswith(".csv") and "result" in filename:
        file_path = os.path.join(input_folder, filename)
        process_particle_data(file_path, output_folder)