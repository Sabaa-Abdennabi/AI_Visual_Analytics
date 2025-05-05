import re

# Clickability detection
def is_clickable(e):
    tag = e.evaluate("el => el.tagName.toLowerCase()")
    has_click = e.get_attribute("onclick") is not None
    role = (e.get_attribute("role") or "").lower()
    cursor_pointer = "cursor:pointer" in (e.get_attribute("style") or "")
    has_tabindex = e.get_attribute("tabindex") is not None
    return (
        tag in ["a", "button", "input", "label"]
        or role in ["button", "link"]
        or has_click
        or cursor_pointer
        or has_tabindex
    )

def get_element_xpath(el):
    return el.evaluate("""
        function(el) {
            let path = '';
            while (el && el.nodeType === Node.ELEMENT_NODE) {
                let index = 1;
                let sibling = el.previousElementSibling;
                while (sibling) {
                    if (sibling.tagName === el.tagName) index++;
                    sibling = sibling.previousElementSibling;
                }
                const tagName = el.tagName.toLowerCase();
                path = '/' + tagName + '[' + index + ']' + path;
                el = el.parentElement;
            }
            return path;
        }
    """)

##more sections ama less clicks 
# def extract_elements(page):
#     # Scroll to ensure all dynamic elements are loaded
#     for _ in range(6):
#         page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#         page.wait_for_timeout(2000)

#     tags_to_scrape = (
#         "h1, h2, h3, p, span, a, button, li, img, input, label, div, svg, section, "
#         "article, aside, footer, header, main, nav, ul, ol, form, table"
#     )
#     elements = page.query_selector_all(tags_to_scrape)

#     result = []

#     for el in elements:
#         try:
#             if el.evaluate("e => !e.isConnected"):
#                 continue
#             style = el.get_attribute("style") or ""
#             classes = el.get_attribute("class") or ""
#             hidden = el.get_attribute("hidden")
#             aria_hidden = el.get_attribute("aria-hidden")
#             bounding_box = el.bounding_box()

#             if (
#                 "display:none" in style
#                 or "hidden" in classes
#                 or hidden is not None
#                 or aria_hidden == "true"
#                 or bounding_box is None  # Not visible
#             ):
#                 continue

#             raw_text = el.text_content().strip()
#             el_id = el.get_attribute("id") or ""
#             el_class = el.get_attribute("class") or ""

#             # Still include if it has an ID/class even if text is short
#             if not raw_text and not el_id and not el_class:
#                 continue

#             tag_upper = el.evaluate("e => e.tagName")
#             tag_lower = tag_upper.lower()
#             sorted_classes = "." + ".".join(sorted(el_class.split())) if el_class else ""

#             # Get XPath (optional for precise matching)
#             xpath = el.evaluate("e => { const getXPath = el => { if (el.id) return '//*[@id=\"' + el.id + '\"]'; if (el === document.body) return '/html/body'; let ix= 0; const siblings = el.parentNode.childNodes; for (let i= 0; i<siblings.length; i++) { const sib= siblings[i]; if (sib===el) return getXPath(el.parentNode)+'/'+el.tagName.toLowerCase()+'['+(ix+1)+']'; if (sib.nodeType===1 && sib.tagName===el.tagName) ix++; } }; return getXPath(e); }")

#             fallback_text = (
#                 el.get_attribute("alt") or 
#                 el.get_attribute("placeholder") or 
#                 raw_text
#             )

#             result.append({
#                 "tag": tag_lower,
#                 "id": el_id,
#                 "classes": el_class,
#                 "selector": f"{tag_lower}{sorted_classes}",
#                 "clickElement": f"{tag_upper}{'#' + el_id if el_id else ''}{sorted_classes}",
#                 "sectionViewedElement": el_id or el_class or fallback_text[:30],  # More useful fallback
#                 "text": fallback_text.strip(),
#             })
#             result.append({
#                 "tag": tag_lower,
#                 "id": el_id,
#                 "classes": el_class,
#                 "selector": f"{tag_lower}{sorted_classes}",
#                 "clickElement": clickable_selector,
#                 "sectionViewedElement": el_id or el_class or tag_upper,
#                 "sectionSignature": f"{el_id}-{raw_text}" if el_id else raw_text,
#                 "text": fallback_text.strip(),
#                 "xpath": xpath,
#             })

#         except Exception as e:
#             print(f"⚠️ Error extracting element: {e}")
#             continue

#     return result

def extract_elements(page):
    # Scroll to load dynamic content
    for _ in range(6):
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(2000)

    tags_to_scrape = (
        "h1, h2, h3, p, span, a, button, li, img, input, label, div, svg, section, "
        "article, aside, footer, header, main, nav, ul, ol, form, table"
    )
    elements = page.query_selector_all(tags_to_scrape)

    result = []

    for el in elements:
        try:
            # Check if element is still in DOM
            if el.evaluate("e => !e.isConnected"):
                continue

            style = el.get_attribute("style") or ""
            classes = el.get_attribute("class") or ""
            hidden = el.get_attribute("hidden")
            aria_hidden = el.get_attribute("aria-hidden")
            bounding_box = el.bounding_box()

            # Skip invisible or off-screen elements
            if (
                "display:none" in style
                or "hidden" in classes
                or hidden is not None
                or aria_hidden == "true"
                or bounding_box is None
            ):
                continue

            raw_text = el.text_content().strip()
            el_id = el.get_attribute("id") or ""
            el_class = el.get_attribute("class") or ""
            sorted_classes = "." + ".".join(sorted(el_class.split())) if el_class else ""

            # Skip if no useful identifier or content
            if not raw_text and not el_id and not el_class and el.get_attribute("alt") is None:
                continue

            tag_upper = el.evaluate("e => e.tagName")
            tag_lower = tag_upper.lower()

            # Fallback text: alt for img, placeholder for input, etc.
            fallback_text = (
                el.get_attribute("alt") or 
                el.get_attribute("placeholder") or 
                raw_text
            )

            # Detect clickability
            def is_clickable(el_handle):
                try:
                    role = el_handle.get_attribute("role") or ""
                    tag = el_handle.evaluate("e => e.tagName.toLowerCase()")
                    return tag in ["a", "button"] or "click" in role or el_handle.get_attribute("onclick")
                except:
                    return False

            clickable_selector = f"{tag_upper}{'#' + el_id if el_id else ''}{sorted_classes}"
            found_clickable = is_clickable(el)

            # Go up 5 ancestors to find a clickable container
            if not found_clickable:
                parent = el
                for _ in range(5):
                    parent = parent.evaluate_handle("e => e.parentElement")
                    if parent is None:
                        break
                    if is_clickable(parent):
                        tag = parent.evaluate("e => e.tagName")
                        pid = parent.get_attribute("id") or ""
                        pclass = parent.get_attribute("class") or ""
                        pclass_sorted = "." + ".".join(sorted(pclass.split())) if pclass else ""
                        clickable_selector = f"{tag}{'#' + pid if pid else ''}{pclass_sorted}"
                        break

            result.append({
                "tag": tag_lower,
                "id": el_id,
                "classes": el_class,
                "selector": f"{tag_lower}{sorted_classes}",
                "clickElement": clickable_selector,
                "sectionViewedElement": el_id or el_class or fallback_text[:30],
                "sectionSignature": f"{el_id}-{raw_text}" if el_id else raw_text,
                "text": fallback_text.strip(),
            })

        except Exception as e:
            print(f"⚠️ Error extracting element: {e}")
            continue

    return result
