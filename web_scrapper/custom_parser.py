import re

def extract_elements(page):
    # ✅ Scroll automatique pour charger tous les éléments dynamiques
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(3000)

    tags_to_scrape = "h1, h2, h3, p, span, a, button, li, img, input, label, div, svg, section, article, aside, footer, header, main, nav, ul, ol"
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
            color = el.evaluate("e => getComputedStyle(e).color")
            background_color = el.evaluate("e => getComputedStyle(e).backgroundColor")

            tag_upper = el.evaluate("e => e.tagName")  # pour clickElement
            tag_lower = tag_upper.lower()
            el_id = el.get_attribute("id") or ""
            el_class = el.get_attribute("class") or ""
            sorted_classes = "." + ".".join(sorted(el_class.split())) if el_class else ""

            result.append({
                "tag": tag_lower,
                "id": el_id,
                "classes": el_class,
                "selector": f"{tag_lower}{sorted_classes}",
                "clickElement": f"{tag_upper}{'#' + el_id if el_id else ''}{sorted_classes}",
                "sectionViewedElement": el_id or el_class or tag_upper,
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
