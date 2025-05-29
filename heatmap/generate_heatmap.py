import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from scipy.ndimage import gaussian_filter
import io

def generate_heatmap(url: str, elements_df: pd.DataFrame, output_path: str = "smooth_heatmap.png"):
    # Headless browser screenshot
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--hide-scrollbars")
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # Full height screenshot
    # total_height = driver.execute_script("return document.body.scrollHeight")
    # driver.set_window_size(1920, total_height)
    png = driver.get_screenshot_as_png()
    driver.quit()

    screenshot = Image.open(io.BytesIO(png))
    width, height = screenshot.size

    # Filter for viewed elements
    viewed = elements_df[elements_df['was_viewed'] == True].copy()
    viewed['x'] = viewed['x'].clip(0, width - 1)
    viewed['y'] = viewed['y'].clip(0, height - 1)

    # Create a blank "heat" image
    heatmap = np.zeros((height, width))

    # Drop coordinates onto heatmap
    for _, row in viewed.iterrows():
        x = int(row['x'])
        y = int(row['y'])
        heatmap[y, x] += 1  # You can use weights like area or duration if needed

    # Apply Gaussian blur
    heatmap_blurred = gaussian_filter(heatmap, sigma=30)  # Sigma controls the "spread"

    # Normalize for display
    heatmap_blurred = heatmap_blurred / np.max(heatmap_blurred)

    # Plot the overlay
    fig, ax = plt.subplots(figsize=(width / 100, height / 100), dpi=100)
    ax.imshow(screenshot)
    ax.imshow(heatmap_blurred, cmap='jet', alpha=0.5, extent=[0, width, height, 0])  # alpha=0.5 for transparency
    ax.axis('off')
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)

    print(f"🔥 Smooth heatmap saved to {output_path}")


if __name__ == "__main__":
    # hottou lahnee esm l .parquet file (nhezzou mel dossier merged_parquet)
    df = pd.read_parquet("../web_scrapper/merged_parquet/0ca2705800.parquet")
    generate_heatmap(df["page_url"].iloc[0], df)
    pass
