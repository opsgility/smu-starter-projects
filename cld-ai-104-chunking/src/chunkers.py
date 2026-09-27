"""COMPLETE: fixed-size + recursive-character chunkers."""


def fixed_size(text: str, size: int, overlap: int = 0) -> list[str]:
    """Cut text into equal size chunks with optional overlap."""
    chunks = []
    step = max(size - overlap, 1)
    for i in range(0, len(text), step):
        chunks.append(text[i:i + size])
    return chunks


def recursive_split(text: str, max_chars: int = 500, overlap: int = 100) -> list[str]:
    """Split by paragraph first, then sentence. Preserve semantic boundaries."""
    if len(text) <= max_chars:
        return [text]
    paras = text.split("\n\n")
    if len(paras) > 1:
        chunks, cur = [], ""
        for p in paras:
            candidate = f"{cur}\n\n{p}" if cur else p
            if len(candidate) <= max_chars:
                cur = candidate
            else:
                if cur:
                    chunks.append(cur)
                if len(p) <= max_chars:
                    cur = p
                else:
                    chunks.extend(recursive_split(p, max_chars, overlap))
                    cur = ""
        if cur:
            chunks.append(cur)
    else:
        # Fall back to sentence split
        sents = text.replace(". ", ".\n").split("\n")
        chunks, cur = [], ""
        for s in sents:
            candidate = f"{cur} {s}".strip() if cur else s
            if len(candidate) <= max_chars:
                cur = candidate
            else:
                if cur:
                    chunks.append(cur)
                cur = s
        if cur:
            chunks.append(cur)

    # Apply overlap by prepending tail of previous chunk
    if overlap > 0 and len(chunks) > 1:
        out = [chunks[0]]
        for i in range(1, len(chunks)):
            prev_tail = chunks[i - 1][-overlap:] if len(chunks[i - 1]) > overlap else chunks[i - 1]
            out.append(f"...{prev_tail} {chunks[i]}")
        return out
    return chunks


def no_split(text: str) -> list[str]:
    """Baseline: one chunk = entire document."""
    return [text]
