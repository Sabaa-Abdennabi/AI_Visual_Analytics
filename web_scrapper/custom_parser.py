import re

def extract_elements(page):
    tags_to_scrape = "section, div, main, article, h1, h2, h3, p, span, a, button, li, img, input, label"
    elements = page.query_selector_all(tags_to_scrape)

    result = []
    seen = set()
    MAX_LENGTH = 300

    for el in elements:
        try:
            style = el.get_attribute("style") or ""
            classes = el.get_attribute("class") or ""
            element_id = el.get_attribute("id") or ""

            if "display:none" in style or "hidden" in classes:
                continue

            raw_text = el.text_content().strip()

            if not raw_text or len(raw_text) < 2:
                continue
            if any(kw in raw_text for kw in ["main-header-container >", "#header-", "::", "@media", "{", "}"]):
                continue
            if re.search(r"[#\.]?[a-zA-Z0-9_-]+\s*[>{:]", raw_text):
                continue
            if re.search(r"[\{\};]", raw_text):
                continue

            cleaned_text = re.sub(r"\s+", " ", raw_text)
            if cleaned_text.lower() in {"ok", "close", "submit", "reset"}:
                continue
            if cleaned_text in seen:
                continue
            seen.add(cleaned_text)

            if len(cleaned_text) > MAX_LENGTH:
                cleaned_text = cleaned_text[:MAX_LENGTH] + "..."

            bounding_box = el.bounding_box()

            # Evaluate tag name
            tag_name = el.evaluate("e => e.tagName.toLowerCase()")

            # Selector format: TAG#id.class1.class2
            # Match JS tracker format: TAG#id.class1.class2
            class_selector = ""
            if isinstance(classes, str):
                class_selector = "." + ".".join(classes.strip().split())

            selector = f"{tag_name.upper()}{'#' + element_id if element_id else ''}{class_selector}"


            # Get styles
            color = el.evaluate("e => getComputedStyle(e).color")
            background_color = el.evaluate("e => getComputedStyle(e).backgroundColor")

            result.append({
                "tag": tag_name,
                "id": element_id,
                "classes": classes,
                "selector": selector,
                "text": cleaned_text,
                "x": bounding_box["x"] if bounding_box else None,
                "y": bounding_box["y"] if bounding_box else None,
                "width": bounding_box["width"] if bounding_box else None,
                "height": bounding_box["height"] if bounding_box else None,
                "color": color,
                "backgroundColor": background_color,
                "href": el.get_attribute("href"),
            })

        except Exception as e:
            print(f"Skipped element due to error: {e}")
            continue

    return result
