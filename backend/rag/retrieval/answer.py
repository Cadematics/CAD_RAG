def generate_answer(query, context, llm):
    prompt = f"""
You are an expert CAD/CAE research assistant.

Answer the question using ONLY the context below.
If the answer is not in the context, say "Not found in the provided documents."

Context:
{context}

Question:
{query}

Answer:
"""
    return llm(prompt)
