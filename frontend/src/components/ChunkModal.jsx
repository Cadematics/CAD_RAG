export default function ChunkModal({ open, chunk, loading, error, onClose }) {
  if (!open) return null;

  return (
    <div
      onClick={onClose}
      style={{
        position: "fixed",
        inset: 0,
        background: "rgba(0,0,0,0.6)",
        display: "grid",
        placeItems: "center",
        padding: 16,
      }}
    >
      <div
        onClick={(e) => e.stopPropagation()}
        style={{
          width: "min(900px, 100%)",
          maxHeight: "80vh",
          overflow: "auto",
          background: "#111",
          border: "1px solid #333",
          borderRadius: 16,
          padding: 16,
        }}
      >
        <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
          <h3 style={{ marginTop: 0, marginBottom: 8 }}>Cited chunk</h3>
          <button onClick={onClose} style={{ borderRadius: 10, padding: "6px 10px" }}>
            Close
          </button>
        </div>

        {loading && <p>Loading chunk…</p>}
        {error && <p style={{ color: "tomato" }}>{error}</p>}

        {chunk && !loading && (
          <>
            <div style={{ opacity: 0.85, marginBottom: 10 }}>
              <div><b>Paper:</b> {chunk.paper_title}</div>
              <div><b>Section:</b> {chunk.section || "Unknown"}</div>
              <div><b>Pages:</b> {chunk.page_start ?? "?"}–{chunk.page_end ?? "?"}</div>
              <div><b>Chunk ID:</b> {chunk.id}</div>
            </div>
            <pre style={{ whiteSpace: "pre-wrap", margin: 0, fontFamily: "inherit" }}>
              {chunk.text}
            </pre>
          </>
        )}
      </div>
    </div>
  );
}
