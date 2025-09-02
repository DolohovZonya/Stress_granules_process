# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 20:35:24 2025

@author: User
"""

import numpy as np
import pandas as pd
import os
import cv2
import czifile
import tifffile
import matplotlib.pyplot as plt
from skimage import morphology, filters, measure, io
from scipy import ndimage as ndi


def np_minmax(x, axis):
    mi = np.min(x, axis)
    ma = np.max(x, axis)
    x = (x - mi) / (ma - mi)
    return mi, ma, x


def load_image(ext, file_path, image):
            if ext == ".czi":
                img = czifile.imread(file_path + image)
                img = img.swapaxes(0, 3).squeeze()
            elif ext in (".tif", ".tiff"):
                img = tifffile.imread(file_path + image)
                if img.ndim == 2:
                    img = np.expand_dims(img, axis=-1)  # Добавляем канал, если изображение ч/б
                elif img.ndim == 3 and img.shape[0] < img.shape[-1]:  
                    img = np.moveaxis(img, 0, -1)  # Приводим порядок осей к (H, W, C)
            else:
                raise ValueError(f"Формат {ext} не поддерживается! Используйте .czi или .tif")
        
            return img


def process_image(inp_path, out_folder, ch_dapi=-1):
    #ext = os.path.splitext(file_path)[1].lower()
    inp_folder =[f for f in os.listdir(inp_path)]

    for image in inp_folder:
            ext = ".czi"
            img = load_image(ext, inp_path, image)
            print(image, img)
            assert img.ndim == 3  # Должно быть (H, W, C)
        
            # Нормализация изображения
            img_min, img_max, img = np_minmax(img, axis=(0, 1))
        
            # Выбираем канал DAPI (если он есть)
            dapi = img[..., ch_dapi]
        
            # Пороговая сегментация (локальный порог)
            nmask = dapi > filters.threshold_local(dapi, block_size=101, method="mean", offset=-0.001)
        
            # Заполнение дырок и морфологическая очистка
            nmask = ndi.binary_fill_holes(nmask)
            nmask = morphology.opening(nmask, morphology.disk(5))
        
            # Маркировка ядер
            labeled_mask, num_regions = ndi.label(nmask)
            properties = measure.regionprops(labeled_mask)
        
            # Минимальный порог площади объекта, чтобы отфильтровать шум
            area_threshold = 400
            nuclei_coordinates = []
        
            # Создаём копию изображения для визуализации
            vis_image = (dapi * 255).astype(np.uint8)
            vis_image = cv2.cvtColor(vis_image, cv2.COLOR_GRAY2BGR)
        
            for region in properties:
                if region.area >= area_threshold:
                    y, x = region.centroid
                    nuclei_coordinates.append((x, y))
                    cv2.circle(vis_image, (int(x), int(y)), 5, (0, 255, 0), -1)  # Рисуем центроиды
        
            # Сохраняем координаты в CSV
            base_name = os.path.basename(inp_path).rsplit(".", 1)[0]
            out_csv = os.path.join(out_folder, f"{base_name}_coords.csv")
            df = pd.DataFrame(nuclei_coordinates, columns=["X", "Y"])
            df.to_csv(out_csv, index=False)
        
            # Сохраняем изображение с выделенными ядрами
            out_img = os.path.join(out_folder, f"{base_name}_segmented.png")
            cv2.imwrite(out_img, vis_image)
        
            # Отображаем результат
            plt.figure(figsize=(8, 8))
            plt.imshow(vis_image)
            plt.title("Выделенные ядра")
            plt.axis("off")
            plt.show()
        
            return df


# Указываем пути
inp_path = "D:/Downloads/NPs_M@B_CA_AMF_6mT_tiff"  # Поддерживает .czi и .tif
out_folder = "D:/Downloads/NPs_M@B_CA_AMF_6mT_tables"

# Создаем папку, если её нет
os.makedirs(out_folder, exist_ok=True)
# Запуск обработки
df = process_image(inp_path, out_folder, ch_dapi=-1)

print(df)