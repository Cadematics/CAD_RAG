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
    current = []
    current_section = None

    for block in text_blocks:
        if block["section"] != current_section:
            if current:
                chunks.append({
                    "text": " ".join(current),
                    "section": current_section
                })
            current = []
            current_section = block["section"]

        current.append(block["text"])

    if current:
        chunks.append({
            "text": " ".join(current),
            "section": current_section
        })

    return chunks




def semantic_chunking(text_blocks):
    # Placeholder for embedding-based splitting
    return section_chunking(text_blocks)




