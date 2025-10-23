"""
Mini sistema de segmentação de imagem (HSV ou K-Means)
melhores resultados encontrados:

python segment.py --input samples/azul1.jpg --method hsv --target blue --hmin 105 --hmax 110 --smin 230 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/azul1.jpg --method kmeans --k 4 --target blue

python segment.py --input samples/azul2.jpg --method kmeans --k 3 --target blue
python segment.py --input samples/azul2.jpg --method hsv --target blue --hmin 105 --hmax 107 --smin 50 --smax 255 --vmin 40 --vmax 255

python segment.py --input samples/verde3.jpg --method hsv --target green --hmin 40 --hmax 45 --smin 50 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/verde3.jpg --method kmeans --k 3 --target green

python segment.py --input samples/verde4.jpg --method hsv --target green --hmin 35 --hmax 85 --smin 50 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/verde4.jpg --method kmeans --k 3 --target green

python segment.py --input samples/verde5.jpg --method hsv --target green --hmin 40 --hmax 44 --smin 50 --smax 255 --vmin 40 --vmax 255
python segment.py --input samples/verde5.jpg --method kmeans --k 8 --target green

"""

import argparse
import os
import time
from datetime import datetime

import cv2
import numpy as np


# Valores padrão de faixas HSV (OpenCV usa H: 0–179, S/V: 0–255)
DEFAULTS = {
    "green": {"hmin": 35, "hmax": 85, "smin": 50, "smax": 255, "vmin": 40, "vmax": 255},
    "blue":  {"hmin": 90, "hmax": 130, "smin": 50, "smax": 255, "vmin": 40, "vmax": 255},
}

# HSV representativo de cada cor (para o método K-Means)
TARGET_HSV_REP = {
    "green": np.array([60.0, 120.0, 120.0], dtype=np.float32),
    "blue":  np.array([120.0, 120.0, 120.0], dtype=np.float32),
}


def parse_args():
    parser = argparse.ArgumentParser(description="Segmentador por HSV ou K-Means")
    parser.add_argument("--input", type=str, required=True, help="Caminho da imagem de entrada")
    parser.add_argument("--method", choices=["hsv", "kmeans"], required=True, help="Método de segmentação")
    parser.add_argument("--target", choices=["green", "blue"], required=True, help="Cor alvo")
    parser.add_argument("--hmin", type=int)
    parser.add_argument("--hmax", type=int)
    parser.add_argument("--smin", type=int)
    parser.add_argument("--smax", type=int)
    parser.add_argument("--vmin", type=int)
    parser.add_argument("--vmax", type=int)
    parser.add_argument("--k", type=int, default=2, help="Número de clusters para K-Means (padrão: 2)")
    parser.add_argument("--output_dir", type=str, default="outputs", help="Pasta de saída")
    return parser.parse_args()


def load_image(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Não foi possível ler a imagem: {path}")
    return img


def hsv_segmentation(img, thresholds):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([thresholds["hmin"], thresholds["smin"], thresholds["vmin"]])
    upper = np.array([thresholds["hmax"], thresholds["smax"], thresholds["vmax"]])
    mask = cv2.inRange(hsv, lower, upper)
    return mask


def kmeans_segmentation(img, target, k=2):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, w = hsv.shape[:2]
    pixels = hsv.reshape((-1, 3)).astype(np.float32)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    compactness, labels, centers = cv2.kmeans(pixels, k, None, criteria, 3, cv2.KMEANS_PP_CENTERS)

    target_vec = TARGET_HSV_REP[target]
    dists = np.linalg.norm(centers - target_vec, axis=1)
    best_cluster = int(np.argmin(dists))

    mask_flat = (labels.flatten() == best_cluster).astype(np.uint8) * 255
    mask = mask_flat.reshape((h, w))
    return mask


def make_overlay(img, mask, color):
    overlay = img.copy()
    colored = np.zeros_like(img)
    colored[:, :] = color
    mask_3c = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR) // 255
    overlay = np.where(mask_3c == 1, cv2.addWeighted(img, 0.6, colored, 0.4, 0), img)
    return overlay


def save_outputs(output_dir, base, mask, overlay):
    os.makedirs(output_dir, exist_ok=True)
    mask_path = os.path.join(output_dir, f"{base}_mask.png")
    overlay_path = os.path.join(output_dir, f"{base}_overlay.png")
    cv2.imwrite(mask_path, mask)
    cv2.imwrite(overlay_path, overlay)
    return mask_path, overlay_path


def main():
    args = parse_args()
    start = time.time()

    img = load_image(args.input)
    source = os.path.splitext(os.path.basename(args.input))[0]

    thresholds = DEFAULTS[args.target].copy()
    for key in thresholds.keys():
        val = getattr(args, key)
        if val is not None:
            thresholds[key] = val

    if args.method == "hsv":
        mask = hsv_segmentation(img, thresholds)
    else:
        mask = kmeans_segmentation(img, args.target, k=args.k)

    color = (0, 255, 0) if args.target == "green" else (255, 0, 0)
    overlay = make_overlay(img, mask, color)

    base = f"{source}_{args.method}_{args.target}_{int(time.time())}"
    mask_path, overlay_path = save_outputs(args.output_dir, base, mask, overlay)

    percent = (np.count_nonzero(mask) / mask.size) * 100
    elapsed = time.time() - start

    print(f"Máscara salva em: {mask_path}")
    print(f"Overlay salvo em: {overlay_path}")
    print(f"Tempo de execução: {elapsed:.2f}s")
    print(f"Pixels segmentados: {percent:.2f}%")

if __name__ == "__main__":
    main()
