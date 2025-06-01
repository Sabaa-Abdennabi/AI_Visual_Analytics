import pandas as pd
import re
import joblib
import os
from sklearn.preprocessing import StandardScaler

def extract_rgba(s):
    if pd.isna(s):
        return (0, 0, 0, 1.0)  # valeur par défaut (opaque noir)
    match = re.match(r"rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)", s)
    if match:
        r, g, b = map(int, match.groups()[:3])
        a = float(match.group(4)) if match.group(4) else 1.0
        return (r, g, b, a)
    return (0, 0, 0, 1.0)

def extract_rgb(s):
    if pd.isna(s):
        return (0, 0, 0)
    s = s.strip().lower()
    match = re.match(r"rgb\((\d+),\s*(\d+),\s*(\d+)\)", s)
    if match:
        return tuple(map(int, match.groups()))
    return (0, 0, 0)


def group_tag(tag):
    if tag in ['header', 'nav', 'footer', 'main', 'section', 'article', 'aside']:
        return 'structure'
    elif tag in ['a', 'button', 'input', 'form', 'label']:
        return 'interactive'
    elif tag in ['div', 'span', 'ul', 'li', 'p', 'h1', 'h2', 'h3']:
        return 'content'
    elif tag in ['img', 'svg']:
        return 'media'
    elif tag == 'table':
        return 'table'
    else:
        return 'other'

def preprocess_heatmap(df):
    #df["original_x"] = df["x"]
    #df["original_y"] = df["y"]
    colonnes_a_supprimer = ['selector', 'sectionSignature', 'session_id','id', 'classes', 'clickElement','sectionViewedElement','text', 'page_url','time_on_site']
    df = df.drop(columns=colonnes_a_supprimer)
    df[['r_bg', 'g_bg', 'b_bg', 'a_bg']] = df['background_color'].apply(extract_rgba).apply(pd.Series)
    df[['r_c', 'g_c', 'b_c']] = df['color'].apply(extract_rgb).apply(pd.Series)
    colonnes_a_supprimer = ['color','background_color']
    df = df.drop(columns=colonnes_a_supprimer)
    df['font_size'] = df['font_size'].str.replace('px', '', regex=False).astype(float).astype(int)
    df['y'] = df['y'].apply(lambda v: max(v, 0))
    df['x'] = df['x'].apply(lambda v: max(v, 0))
    df['tag_group'] = df['tag'].apply(group_tag)

    # One-hot encoding avec des 1 et 0 (pas True/False)
    one_hot = pd.get_dummies(df['tag_group'], dtype=int)

    # Joindre les colonnes encodées au dataframe
    df = pd.concat([df, one_hot], axis=1)
    df = df.drop_duplicates()
    df.drop(["tag_group"], axis=1, inplace=True)
    df["area"] = df["height"] * df["width"]
    df.drop(["height", "width","tag"], axis=1, inplace=True)
    layout_features = ['x', 'y', 'area','font_size','r_bg', 'g_bg','b_bg', 'a_bg', 'r_c', 'g_c','b_c']
    backend_dir = os.path.dirname(__file__)
    scaler_x = joblib.load(os.path.join(backend_dir, "scaler_x.pkl"))
    df[layout_features] = scaler_x.transform(df[layout_features])
    
    
    # Forçage des colonnes tag_* manquantes
    expected_tags = ['content', 'interactive', 'media', 'other', 'structure', 'table']
    for tag_col in expected_tags:
        if tag_col not in df.columns:
            df[tag_col] = 0

    return df