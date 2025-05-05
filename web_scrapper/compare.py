import json
import re
import os

import json
import re
import os

def normalize_click_element(element_str):
    parts = re.split(r'(?=[#.])', element_str)
    tag = parts[0]
    id_part = ''
    classes = []

    for part in parts[1:]:
        if part.startswith('#'):
            id_part = part
        elif part.startswith('.'):
            classes.append(part)

    return f"{tag}{id_part}{''.join(sorted(classes))}"

def compare_elements(clicks_file, sections_file, scraping_file):
    with open(clicks_file, 'r', encoding='utf-8') as f:
        click_data = json.load(f)

    with open(sections_file, 'r', encoding='utf-8') as f:
        section_data = json.load(f)

    with open(scraping_file, 'r', encoding='utf-8') as f:
        scraping_data = json.load(f)

    click_elements_dataset = {normalize_click_element(e["element"]) for e in click_data}
    viewed_sections_dataset = {k for k, v in section_data.items() if v > 0}

    # Scraped elements
    click_elements_scraped = {
        normalize_click_element(e["clickElement"]) for e in scraping_data if "clickElement" in e
    }
    section_fields_scraped = {
        e["sectionViewedElement"] for e in scraping_data if "sectionViewedElement" in e
    }
    section_signatures_scraped = {
        e["sectionSignature"] for e in scraping_data if "sectionSignature" in e
    }

    # Comparisons
    matched_clicks = sorted(click_elements_dataset & click_elements_scraped)
    unmatched_clicks = sorted(click_elements_dataset - click_elements_scraped)

    matched_sections = sorted(viewed_sections_dataset & section_fields_scraped)
    unmatched_sections = sorted(viewed_sections_dataset - section_fields_scraped)

    # Try to catch additional matches via sectionSignature
    fuzzy_matches = sorted(viewed_sections_dataset & section_signatures_scraped)

    click_rate = len(matched_clicks) / len(click_elements_dataset) * 100 if click_elements_dataset else 0
    section_rate = len(matched_sections) / len(viewed_sections_dataset) * 100 if viewed_sections_dataset else 0

    output_dir = "outputcomparaison"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "rapport_comparaison_enhanced9.txt")

    with open(output_file, 'w', encoding='utf-8') as out:
        def write_and_print(line):
            print(line)
            out.write(line + "\n")

        write_and_print(f"\n📊 CLICKS : {click_rate:.2f}% match ({len(matched_clicks)}/{len(click_elements_dataset)})")
        write_and_print(f"📊 SECTIONS : {section_rate:.2f}% match ({len(matched_sections)}/{len(viewed_sections_dataset)})")

        write_and_print("\n✅ Clicks trouvés :")
        for e in matched_clicks:
            write_and_print(f" - {e}")

        write_and_print("\n❌ Clicks non trouvés :")
        for e in unmatched_clicks:
            write_and_print(f" - {e}")

        write_and_print("\n✅ Sections vues trouvées :")
        for s in matched_sections:
            write_and_print(f" - {s}")

        write_and_print("\n❌ Sections vues non trouvées :")
        for s in unmatched_sections:
            write_and_print(f" - {s}")

        write_and_print("\n🔍 Bonus: Sections matched via `sectionSignature` only :")
        for s in fuzzy_matches:
            if s not in matched_sections:
                write_and_print(f" - {s}")

    print(f"\n✅ Rapport sauvegardé dans : {output_file}")

# Utilisation
if __name__ == "__main__":
    compare_elements(
        clicks_file="clickEvents.json",
        sections_file="sectionViewed.json",
        scraping_file="outputs/scraping_outputmercedes9.json"
    )
