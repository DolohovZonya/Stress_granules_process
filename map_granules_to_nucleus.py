# -*- coding: utf-8 -*-
"""
Created on Fri Feb  7 16:18:03 2025

@author: User
"""

import os
import numpy as np
import pandas as pd

def get_files_from_folder(folder_path, file_pattern):
    return [f for f in os.listdir(folder_path) if file_pattern in f]

sg_tests_folder = os.getcwd()



out_folder = "D:/Downloads/salu_координаты"
if os.path.isdir(out_folder) == False:
    os.mkdir(out_folder)
for i in range(1,6):
    for j in range(1,3):
        nuclei_folder = os.listdir(f"D:/Downloads/all_archive/salu/salu_nuclei/salu_{i}_{j}_coords")# Папки с "tables"
        image_folder = os.listdir(f"D:/Games/Icy_2.5.2/Icy/salu_{i}_{j}") # Папки без "tables"
        image_folder = sorted(image_folder)
        nuclei_folder = sorted(nuclei_folder)
        image_file_patterns = []
        print(image_folder)
        for file in image_folder:
            pattern = file[0:10]
            image_file_patterns.append(pattern)
        for image_file_pattern in image_file_patterns:

            radius = 10
            a = 10
            b = 5
            nuclei_file = image_file_pattern + "_coords.csv"
            print(nuclei_file)
            centers = pd.read_csv(os.path.join(f"D:/Downloads/all_archive/salu/salu_nuclei/salu_{i}_{j}_coords" + "/" + nuclei_file))

            data1 = pd.read_excel(os.path.join(f"D:/Games/Icy_2.5.2/Icy/salu_{i}_{j}" + "/" + image_file_pattern + "_1.tif_DetectionResults.xlsx"))  # Первый файл
            data2 = pd.read_excel(os.path.join(f"D:/Games/Icy_2.5.2/Icy/salu_{i}_{j}" + "/" + image_file_pattern + "_2.tif_DetectionResults.xlsx"))  # Второй файл

            x1, y1 = data1['X Coordinate'], data1['Y Coordinate']
            x2, y2 = data2['X Coordinate'], data2['Y Coordinate']
            centers_x, centers_y = centers['X'], centers['Y']
        

            def is_within_circle(x, y, center_x, center_y, radius, a, b):
                return (((x - center_x)**2)/(a**2)) + (((y - center_y)**2)/b**2) <= radius**2
            def count_points_per_nucleus(data_x, data_y, centers_x, centers_y, radius):
                results = []
                for cx, cy in zip(centers_x, centers_y):
                    count = 0
                    dots = []
                    for x, y in zip(data_x, data_y):
                        if is_within_circle(x, y, cx, cy, radius, a, b):
                            count += 1
                            dots.append([x,y])
                    results.append({"nucleus_center": (cx, cy), "points_count": dots})
                return pd.DataFrame(results)
        
                # Подсчет точек для обоих файлов
            results1 = count_points_per_nucleus(x1, y1, centers_x, centers_y, radius)
            results2 = count_points_per_nucleus(x2, y2, centers_x, centers_y, radius)
                # Сохранение результатов в файлы
            out_csv_1 = os.path.join(out_folder, f"results_{image_file_pattern}_file1.csv")
            out_csv_2 = os.path.join(out_folder, f"results_{image_file_pattern}_file2.csv")
            results1.to_csv(out_csv_1, index=False)
            results2.to_csv(out_csv_2, index=False)
            # out_csv = os.path.join(out_folder, f"{base_name}_coords.csv")
                # Вывод итогов в консоль
            print(f"Результаты для первого файла {data1}:")
            print(results1)
            print(f"Результаты для второго файла {data2}:")
            print(results2)
            
            
# %%
import os
import numpy as np
import pandas as pd

# def get_files_from_folder(folder_path, file_pattern):
#     return [f for f in os.listdir(folder_path) if file_pattern in f]

# sg_tests_folder = os.getcwd()



out_folder = "D:/Downloads/NPs_M@B_CA_AMF_6mT_координаты_фильтрованные"
if os.path.isdir(out_folder) == False:
    os.mkdir(out_folder)
nuclei_folder = os.listdir(f"D:/Downloads/SG_28012025/NPs_M@B_CA_AMF_6mT_tiff_coords")# Папки с "tables"
image_folder = os.listdir(f"D:/Games/Icy_2.5.2/Icy/NPs_M@B_CA_AMF_6mT") # Папки без "tables"
image_folder = sorted(image_folder)
nuclei_folder = sorted(nuclei_folder)
image_file_patterns = []
print(image_folder)
for file in image_folder:
    pattern = file[0:10]
    image_file_patterns.append(pattern)
for image_file_pattern in image_file_patterns:

    radius = 5
    a = 8
    b = 6
    nuclei_file = image_file_pattern + "_3_coords.csv"
    print(nuclei_file)
    centers = pd.read_csv(os.path.join(f"D:/Downloads/SG_28012025/NPs_M@B_CA_AMF_6mT_tiff_coords" + "/" + nuclei_file))

    data1 = pd.read_csv(os.path.join(f"D:/Downloads/NPs_M@B_CA_AMF_6mT_merged" + "/" + image_file_pattern + "_only_channel1.csv"))  # Первый файл
    data2 = pd.read_csv(os.path.join(f"D:/Downloads/NPs_M@B_CA_AMF_6mT_merged" + "/" + image_file_pattern + "_only_channel2.csv"))
    datam = pd.read_csv(os.path.join(f"D:/Downloads/NPs_M@B_CA_AMF_6mT_merged" + "/" + image_file_pattern + "_matched.csv"))# Второй файл
    # data1 = pd.read_excel(os.path.join(f"D:/Games/Icy_2.5.2/Icy/K_SMF" + "/" + image_file_pattern + "_1.tif_DetectionResults.xlsx"))  # Первый файл
    # data2 = pd.read_excel(os.path.join(f"D:/Games/Icy_2.5.2/Icy/K_SMF" + "/" + image_file_pattern + "_2.tif_DetectionResults.xlsx"))
    # D:/Downloads/SG_28012025/NPs_M@B_CA_AMF_6mT_tiff_coords
    data1 = data1[data1['Average Intensity'] > 2000]
    data2 = data2[data2['Average Intensity'] > 2300]
    datam = datam[datam['Average Intensity'] > 2000]

    x1, y1 = data1['X Coordinate'], data1['Y Coordinate']
    x2, y2 = data2['X Coordinate'], data2['Y Coordinate']
    xm, ym = datam['X Coordinate'], datam['Y Coordinate']
    centers_x, centers_y = centers['X'], centers['Y']


    def is_within_circle(x, y, center_x, center_y, radius, a, b):
        return (((x - center_x)**2)/(a**2)) + (((y - center_y)**2)/b**2) <= radius**2
    def count_points_per_nucleus(data_x, data_y, centers_x, centers_y, radius):
        results = []
        for cx, cy in zip(centers_x, centers_y):
            count = 0
            dots = []
            for x, y in zip(data_x, data_y):
                if is_within_circle(x, y, cx, cy, radius, a, b):
                    count += 1
                    dots.append([x,y])
            results.append({"nucleus_center": (cx, cy), "points_count": dots})
        return pd.DataFrame(results)

        # Подсчет точек для обоих файлов
    results1 = count_points_per_nucleus(x1, y1, centers_x, centers_y, radius)
    results2 = count_points_per_nucleus(x2, y2, centers_x, centers_y, radius)
    resultsm = count_points_per_nucleus(xm, ym, centers_x, centers_y, radius)
        # Сохранение результатов в файлы
    out_csv_1 = os.path.join(out_folder, f"results_{image_file_pattern}_channel1.csv")
    out_csv_2 = os.path.join(out_folder, f"results_{image_file_pattern}_channel2.csv")
    out_csv_m = os.path.join(out_folder, f"results_{image_file_pattern}_matched.csv")
    results1.to_csv(out_csv_1, index=False)
    results2.to_csv(out_csv_2, index=False)
    resultsm.to_csv(out_csv_m, index=False)
    # out_csv = os.path.join(out_folder, f"{base_name}_coords.csv")
        # Вывод итогов в консоль
    # print(f"Результаты для первого файла {data1}:")
    # print(results1)
    # print(f"Результаты для второго файла {data2}:")
    # print(results2)
# %%