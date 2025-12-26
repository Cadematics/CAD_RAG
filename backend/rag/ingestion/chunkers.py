def fixed_chunking(text_blocks, chunk_size=500, overlap=50):
    chunks = []
    buffer = []
    token_count = 0

    for block in text_blocks:
        words = block["text"].split()
        buffer.extend(words)
        token_count += len(words)

        if token_count >= chunk_size:
            chunks.append({
                "text": " ".join(buffer),
                "page_start": block["page"],
                "page_end": block["page"],
                "section": block["section"]
            })
            buffer = buffer[-overlap:]
            token_count = len(buffer)

    return chunks





def section_chunking(text_blocks, max_words=700):
    chunks = []
    current_text = []
    current_pages = []
    current_section = None

    for block in text_blocks:
        # New section → flush previous chunk
        if block["section"] != current_section:
            if current_text:
                chunks.append({
                    "text": " ".join(current_text),
                    "section": current_section,
                    "page_start": min(current_pages),
                    "page_end": max(current_pages),
                })
            current_text = []
            current_pages = []
            current_section = block["section"]

        words = block["text"].split()
        current_text.extend(words)
        current_pages.append(block["page"])

        # Optional safety: split very large sections
        if len(current_text) >= max_words:
            chunks.append({
                "text": " ".join(current_text),
                "section": current_section,
                "page_start": min(current_pages),
                "page_end": max(current_pages),
            })
            current_text = []
            current_pages = []

    # Flush last chunk
    if current_text:
        chunks.append({
            "text": " ".join(current_text),
            "section": current_section,
            "page_start": min(current_pages),
            "page_end": max(current_pages),
        })

    return chunks





def semantic_chunking(text_blocks):
    # Placeholder for embedding-based splitting
    return section_chunking(text_blocks)




