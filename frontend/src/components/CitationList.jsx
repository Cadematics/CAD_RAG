export default function CitationList({ citations, onOpenChunk }) {
  if (!citations?.length) {
    return (
      <div style={{ padding: 16, borderRadius: 14, border: "1px solid #333", marginTop: 16 }}>
        <h3 style={{ marginTop: 0 }}>Citations</h3>
        <p style={{ marginBottom: 0, opacity: 0.8 }}>No citations returned.</p>
      </div>
    );
  }

  return (
    <div style={{ padding: 16, borderRadius: 14, border: "1px solid #333", marginTop: 16 }}>
      <h3 style={{ marginTop: 0 }}>Citations</h3>

      <ul style={{ margin: 0, paddingLeft: 18, display: "grid", gap: 10 }}>
        {citations.map((c, i) => (
          <li key={`${c.chunk_id}-${i}`}>
            <button
              onClick={() => onOpenChunk(c.chunk_id)}
              style={{
                background: "transparent",
                border: "none",
                textAlign: "left",
                cursor: "pointer",
                padding: 0,
              }}
              title="Open cited chunk text"
            >
              <div style={{ fontWeight: 700 }}>{c.paper}</div>
              <div style={{ opacity: 0.85 }}>
                Pages: {c.page_start ?? "?"}–{c.page_end ?? "?"} · Score:{" "}
                {typeof c.score === "number" ? c.score.toFixed(3) : c.score}
              </div>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
