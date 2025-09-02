import numpy as np
import pandas as pd
import os
import cv2
import tifffile
import matplotlib.pyplot as plt
from skimage import morphology, filters, measure
from scipy import ndimage as ndi

def np_minmax(x, axis):
    mi = np.min(x, axis, keepdims=True)
    ma = np.max(x, axis, keepdims=True)
    return mi, ma, (x - mi) / (ma - mi)

def load_tiff_image(file_path):
    img = tifffile.imread(file_path)
    if img.ndim == 2:
        img = np.expand_dims(img, axis=-1)  # Добавляем канал, если изображение ч/б
    elif img.ndim == 3 and img.shape[0] < img.shape[-1]:
        img = np.moveaxis(img, 0, -1)  # Приводим порядок осей к (H, W, C)
    return img

def process_tiff_images(inp_path, out_folder, ch_dapi=-1):
    inp_files = [f for f in os.listdir(inp_path) if f.endswith("_3.tif")]
    
    for image in inp_files:
        file_path = os.path.join(inp_path, image)
        img = load_tiff_image(file_path)
        assert img.ndim == 3  # Должно быть (H, W, C)

        # Нормализация изображения
        _, _, img = np_minmax(img, axis=(0, 1))
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
        base_name = os.path.splitext(image)[0]
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
# %%


# Указываем пути
cells = ['K-_tiff', 'K_2DG_tif', 'K_2DG_tiff', 'K_AMF_16mT_tiff', 'K_AMF_6mT_tiff', 'K_SMF_tiff', 'NPs_M@B_CA_AMF_16mT_tiff', 'NPs_M@B_CA_AMF_6mT_tiff', 'NPs_M@B_CA_SMF_tiff', 'NPs_M@B_CA_tiff', 'NPs_M_CA_AMF_16mT_tiff', 'NPs_M_CA_AMF_6mT_tiff', 'NPs_M_CA_SMF_tiff', 'NPs_M_CA_tiff']
for i in cells:
    inp_path = f"D:/Downloads/SG_28012025/{i}/"
    out_folder = f"D:/Downloads/SG_28012025/{i}_coords/"
# %%


# Создаем папку, если её нет
    os.makedirs(out_folder, exist_ok=True)
    
    # Запуск обработки
    process_tiff_images(inp_path, out_folder, ch_dapi=-1)