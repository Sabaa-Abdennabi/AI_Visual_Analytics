import numpy as np
import cv2
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import io
from scipy.ndimage import gaussian_filter
import os
import hashlib
from urllib.parse import urlparse

def generate_heatmap(url: str, raw_points):
    # Capture d'écran du site
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    total_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(1920, total_height)
    png = driver.get_screenshot_as_png()
    driver.quit()

    # Charger l'image
    image = Image.open(io.BytesIO(png))
    width, height = image.size

    # Analyser les données d'abord
    all_durations = [d for _, _, d in raw_points]
    print(f"Total des points: {len(raw_points)}")
    print(f"Valeurs originales min/max: {min(all_durations):.2e} / {max(all_durations):.2f}")
    

    points=raw_points
    if not points:
        print("Pas de points significatifs pour la heatmap.")
        return

    print(f"Points significatifs gardés: {len(points)}")
    print(f"Valeurs filtrées min/max: {min(d for _,_,d in points):.2f} / {max(d for _,_,d in points):.2f}")

    # Créer une heatmap vide
    heatmap = np.zeros((height, width), dtype=np.float64)
    
    # Normaliser les valeurs d'abord (comme en JS: Math.round(val))
    durations = [d for _, _, d in points]
    max_duration = max(durations)
    
    # Créer une heatmap vide
    heatmap = np.zeros((height, width), dtype=np.float64)
    point_count = 0
    
    # Traitement de chaque point individuellement (comme en JS)
    for x, y, duration in points:
        # Corriger y == 0 comme en JS  
        if y == 0:
            y = height // 2
        
        # S'assurer que les coordonnées sont dans l'image
        x = max(0, min(int(round(x)), width - 1))
        y = max(0, min(int(round(y)), height - 1))
        
        # Normaliser la valeur (comme en JS: Math.round(val))
        normalized_value = round(duration)
        
        if point_count < 10:  # Debug les 10 premiers points
            print(f"Point {point_count}: ({x}, {y}) = {duration:.2f} -> {normalized_value}")
        
        # Créer un "blob" circulaire autour du point (radius=40 comme en JS)
        radius = 40
        y_min, y_max = max(0, y - radius), min(height, y + radius + 1)
        x_min, x_max = max(0, x - radius), min(width, x + radius + 1)
        
        # Générer une gaussienne centrée sur le point
        yy, xx = np.ogrid[y_min:y_max, x_min:x_max]
        distance_sq = (xx - x) ** 2 + (yy - y) ** 2
        gaussian_blob = np.exp(-distance_sq / (2 * (radius/3) ** 2))  # sigma = radius/3
        
        # Ajouter l'intensité du point à la heatmap
        heatmap[y_min:y_max, x_min:x_max] += gaussian_blob * normalized_value
        point_count += 1

    # Appliquer un flou léger (blur=0.8 en JS)
    heatmap = gaussian_filter(heatmap, sigma=0.8)
    
    print(f"Heatmap min/max après blur: {heatmap.min():.2f} / {heatmap.max():.2f}")
    
    # Normaliser la heatmap (0-1)
    if heatmap.max() > 0:
        heatmap_normalized = heatmap / heatmap.max()
    else:
        print("⚠️  Heatmap vide!")
        return
    
    print(f"Heatmap normalisée min/max: {heatmap_normalized.min():.2f} / {heatmap_normalized.max():.2f}")
    
    # Créer la colormap avec OpenCV (plus simple)
    # Convertir en 0-255 pour OpenCV
    heatmap_255 = (heatmap_normalized * 255).astype(np.uint8)
    
    # Appliquer une colormap (COLORMAP_JET ressemble au gradient JS)
    heatmap_colored = cv2.applyColorMap(heatmap_255, cv2.COLORMAP_JET)
    
    # Créer le masque de transparence - zones sans activité = transparentes
    alpha = np.zeros_like(heatmap_normalized)
    threshold = 0.01  # Seuil minimal pour afficher quelque chose
    
    # Seulement les zones avec de l'activité significative
    mask = heatmap_normalized > threshold
    alpha[mask] = np.clip(heatmap_normalized[mask] * 0.6, 0.1, 0.6)  # min=0.1, max=0.6
    
    # Conversion de l'image de base
    image_np = np.array(image.convert("RGB"))
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    print(f"Image originale shape: {image_bgr.shape}")
    print(f"Heatmap shape: {heatmap_colored.shape}")
    print(f"Alpha shape: {alpha.shape}")
    
    # S'assurer que toutes les dimensions correspondent
    if image_bgr.shape[:2] != heatmap_colored.shape[:2]:
        print("⚠️  Redimensionnement de la heatmap...")
        heatmap_colored = cv2.resize(heatmap_colored, (image_bgr.shape[1], image_bgr.shape[0]))
        alpha = cv2.resize(alpha, (image_bgr.shape[1], image_bgr.shape[0]))
    print(f"image_bgr.shape = {image_bgr.shape}")
    print(f"heatmap_colored.shape = {heatmap_colored.shape}")

    # Commencer avec l'image originale
    result = image_bgr.copy()

    # Appliquer la heatmap seulement là où alpha > 0
    mask = alpha > 0
    if np.any(mask):
        # Fusion pixel par pixel seulement sur les zones avec activité
        alpha_3d = np.stack([alpha, alpha, alpha], axis=2)
        result = result.astype(np.float64)
        heatmap_colored = heatmap_colored.astype(np.float64)
        
        # Formule de fusion: result = background * (1-alpha) + overlay * alpha
        result = result * (1 - alpha_3d) + heatmap_colored * alpha_3d
        result = np.clip(result, 0, 255).astype(np.uint8)
    else:
        print("⚠️  Aucune zone d'activité détectée, image originale conservée")
        
    # Sauvegarder
    parsed = urlparse(url)
    domain = parsed.netloc.replace('.', '_')
    url_hash = hashlib.md5(url.encode("utf-8")).hexdigest()[:8]
    filename = f"{domain}_{url_hash}.png"
    output_dir = "../Dashboard_front/src/assets"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    # Sauvegarder
    cv2.imwrite(output_path, result)
    print(f"✅ Heatmap générée : {output_path}")
    return output_path
