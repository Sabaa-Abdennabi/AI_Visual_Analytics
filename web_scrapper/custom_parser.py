import re

def extract_elements(page):
    tags_to_scrape = "h1, h2, h3, p, span, a, button, li, img, input, label, div"
    elements = page.query_selector_all(tags_to_scrape)

    result = []
    seen = set()
    MAX_LENGTH = 300

    for el in elements:
        try:
            style = el.get_attribute("style") or ""
            classes = el.get_attribute("class") or ""
            if "display:none" in style or "hidden" in classes:
                continue

            raw_text = el.text_content().strip()

            # ⛔ Skip noise
            if not raw_text or len(raw_text) < 2:
                continue
            if any(kw in raw_text for kw in ["main-header-container >", "#header-", "::", "@media", "{", "}"]):
                continue
            if re.search(r"[#\.]?[a-zA-Z0-9_-]+\s*[>{:]", raw_text):  # CSS selector-like pattern
                continue
            if re.search(r"[\{\};]", raw_text):  # Skip code fragments
                continue

            # ✅ Clean content
            cleaned_text = re.sub(r"\s+", " ", raw_text)
            if cleaned_text.lower() in {"ok", "close", "submit", "reset"}:
                continue
            if cleaned_text in seen:
                continue
            seen.add(cleaned_text)

            if len(cleaned_text) > MAX_LENGTH:
                cleaned_text = cleaned_text[:MAX_LENGTH] + "..."

            bounding_box = el.bounding_box()

            # ✅ Add CSS style values
            color = el.evaluate("e => getComputedStyle(e).color")
            background_color = el.evaluate("e => getComputedStyle(e).backgroundColor")

            result.append({
                "tag": el.evaluate("e => e.tagName.toLowerCase()"),
                "id": el.get_attribute("id") or "",
                "classes": classes,
                "selector": f"{el.evaluate('e => e.tagName.toLowerCase()')}" + (
                    "." + ".".join(classes.split()) if classes else ""
                ),
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
