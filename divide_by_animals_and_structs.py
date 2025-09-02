# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 22:47:13 2025

@author: User
"""

import pandas as pd
import os

# Пути к файлам и директориям
input_file = "D:/Downloads/salu_filtered_статистика_big_ellipse/salu_filtered_big_merged_new.csv"  # Таблица со статистикой
images_dir = "07"  # Директория со снимками
output_dir = "salu_filtered_big_SG_stat_new"  # Куда сохранять файлы

# Словарь названий структур
structure_mapping = {
    "1": "ob", "2": "Cortex", "3": "Striatum",
    "4": "CA", "5": "DG", "6": "Thalamus",
    "7": "Midbrain", "8": "Cerebellum"
}

# Читаем таблицу со статистикой
df = pd.read_csv(input_file)

# Создаем выходную директорию, если её нет
os.makedirs(output_dir, exist_ok=True)

# Словарь для хранения данных по структурам
structured_data = {}

# Обход файловой структуры
for animal in os.listdir(images_dir):
    animal_path = os.path.join(images_dir, animal)
    if not os.path.isdir(animal_path):
        continue

    for slice_num in os.listdir(animal_path):
        slice_path = os.path.join(animal_path, slice_num)
        if not os.path.isdir(slice_path):
            continue

        for structure in os.listdir(slice_path):
            structure_path = os.path.join(slice_path, structure)
            if not os.path.isdir(structure_path):
                continue

            structure_name = structure_mapping.get(structure, structure)  # Название структуры

            for side in os.listdir(structure_path):
                side_path = os.path.join(structure_path, side)
                if not os.path.isdir(side_path):
                    continue

                side_label = "R" if side == "01" else "L"

                # Получаем список снимков
                image_files = [f[:10] for f in os.listdir(side_path)]

                # Фильтруем таблицу
                df_filtered = df[df["File_Prefix"].isin(image_files)].copy()
                if df_filtered.empty:
                    continue
                
                # Добавляем информацию о животном, срезе, структуре и стороне
                df_filtered["mouse"] = int(animal)
                df_filtered["channel"] = df_filtered.groupby(["mouse", "File_Prefix"]).cumcount() + 1
                # Ключ для группировки данных
                key = f"{structure_mapping.get(structure_name[1])}_{side_label.lower()}_slice_{slice_num[1]}"

                # Добавляем данные в общий словарь
                if key in structured_data:
                    structured_data[key] = pd.concat([structured_data[key], df_filtered], ignore_index=True)
                else:
                    structured_data[key] = df_filtered

# Сохраняем все файлы
for key, data in structured_data.items():
    output_file = os.path.join(output_dir, f"{key}.csv")
    data.drop_duplicates().to_csv(output_file, index=False)
    print(f"Сохранено: {output_file}")

print("Разбиение завершено.")