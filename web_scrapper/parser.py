# web_scraper/parser.py
import re

def extract_elements(page):
    tags_to_scrape = "h1, h2, h3, p, span, a, button, li, img, input, label, div"
    elements = page.query_selector_all(tags_to_scrape)

    result = []
    seen_texts = set()
    MAX_TEXT_LENGTH = 300
    SCRIPT_KEYWORDS = ["require(", "document.body", "<script", "appendChild", "createElement", "function()"]

    for el in elements:
        try:
            style = el.get_attribute("style") or ""
            classes = el.get_attribute("class") or ""
            if "display:none" in style or "hidden" in classes:
                continue

            text = el.text_content().strip()
            
            # 1. Remove CSS-like blocks (e.g. `.class { ... }`)
            text = re.sub(r'[.#]?[a-zA-Z0-9_-]+\s*\{[^}]+\}', '', text)

            # 2. Optionally extract only color-related lines
            color_matches = re.findall(r'(?:color|background-color)\s*:\s*[^;]+;', text, flags=re.IGNORECASE)

            # 3. Clean remaining non-color styles from the text
            text = re.sub(r'[a-zA-Z-]+\s*:\s*[^;]+;', '', text)

            # 4. Rebuild text if you still want to include found colors
            if color_matches:
                text = " | ".join(color_matches)
            else:
                text = text.strip()

            if not text or len(text) < 2:
                continue

            # Skip known script-like or tech-generated content
            if any(script_kw in text for script_kw in SCRIPT_KEYWORDS):
                continue

            # Skip if it's already seen
            cleaned_text = text.replace("\n", " ").strip()
            if cleaned_text in seen_texts:
                continue
            seen_texts.add(cleaned_text)

            # Skip very noisy or unhelpful content
            if len(cleaned_text.split()) < 2 and len(cleaned_text) < 10:
                continue
            if cleaned_text.lower() in {"ok", "add", "close", "search", "submit"}:
                continue

            # Truncate long text
            if len(cleaned_text) > MAX_TEXT_LENGTH:
                cleaned_text = cleaned_text[:MAX_TEXT_LENGTH] + "..."

            bounding_box = el.bounding_box()

            result.append({
                "tag": el.evaluate("e => e.tagName.toLowerCase()"),
                "text": cleaned_text,
                "x": bounding_box["x"] if bounding_box else None,
                "y": bounding_box["y"] if bounding_box else None,
                "width": bounding_box["width"] if bounding_box else None,
                "height": bounding_box["height"] if bounding_box else None,
                "id": el.get_attribute("id"),
                "classes": classes,
                "href": el.get_attribute("href"),
            })

        except Exception as e:
            print(f"Skipped element due to error: {e}")
            continue

    return result
