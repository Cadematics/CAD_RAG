import re

SECTION_REGEX = re.compile(
    r"^(abstract|introduction|methodology|methods|results|discussion|conclusion)",
    re.IGNORECASE
)

def detect_sections(pages):
    current_section = "Unknown"
    structured = []

    for page in pages:
        lines = page["text"].split("\n")
        for line in lines:
            if SECTION_REGEX.match(line.strip()):
                current_section = line.strip()

            structured.append({
                "page": page["page_number"],
                "section": current_section,
                "text": line.strip()
            })

    return structured
