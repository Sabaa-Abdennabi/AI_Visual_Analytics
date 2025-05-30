import pandas as pd
import re
from sklearn.preprocessing import StandardScaler

def parse_rgb(color_str):
    if pd.isna(color_str) or color_str.strip() == '':
        return (0, 0, 0, 1)  # Default black
    try:
        match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*(\d*\.?\d+))?\)', color_str)
        if match:
            r, g, b = int(match.group(1)), int(match.group(2)), int(match.group(3))
            a = float(match.group(4)) if match.group(4) else 1.0
            return (r, g, b, a)
    except Exception as e:
        print(f"Failed to parse color: {color_str} -> {e}")
    return (0, 0, 0, 1)

def preprocess_dataframe(df):
    df[['text_r', 'text_g', 'text_b', 'text_a']] = df['color'].apply(lambda x: pd.Series(parse_rgb(x)))
    df[['bg_r', 'bg_g', 'bg_b', 'bg_a']] = df['background_color'].apply(lambda x: pd.Series(parse_rgb(x)))
    df = df.dropna(subset=['x', 'y', 'width', 'height'])
    df['font_size'] = df['font_size'].str.replace('px', '').astype(float)
    df['area'] = df['width'] * df['height']
    layout_features = ['x', 'y', 'area','text_r', 'text_g', 'text_b', 'text_a','bg_r', 'bg_g', 'bg_b', 'bg_a']
    scaler = StandardScaler()
    df[layout_features] = scaler.fit_transform(df[layout_features])

    return df