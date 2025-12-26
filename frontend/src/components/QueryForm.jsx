import { useState } from "react";

export default function QueryForm({ onSubmit, isLoading }) {
  const [query, setQuery] = useState("How is artificial intelligence integrated into CAD systems?");
  const [topK, setTopK] = useState(5);
  const [domain, setDomain] = useState("");
  const [debug, setDebug] = useState(false);

  const submit = (e) => {
    e.preventDefault();
    if (!query.trim()) return;
    onSubmit({ query: query.trim(), top_k: Number(topK), domain, debug });
  };

  return (
    <form onSubmit={submit} style={{ display: "grid", gap: 12 }}>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        rows={5}
        placeholder="Ask a question about CAD / CAM / CFD / FEA papers…"
        style={{ width: "100%", padding: 12, borderRadius: 10 }}
      />

      <div style={{ display: "flex", gap: 12, flexWrap: "wrap", alignItems: "center" }}>
        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          Top K
          <input
            type="number"
            min={1}
            max={20}
            value={topK}
            onChange={(e) => setTopK(e.target.value)}
            style={{ width: 80, padding: 8, borderRadius: 10 }}
          />
        </label>

        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          Domain
          <select
            value={domain}
            onChange={(e) => setDomain(e.target.value)}
            style={{ padding: 8, borderRadius: 10 }}
          >
            <option value="">All</option>
            <option value="CAD">CAD</option>
            <option value="CAM">CAM</option>
            <option value="CFD">CFD</option>
            <option value="FEA">FEA</option>
          </select>
        </label>

        <label style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <input
            type="checkbox"
            checked={debug}
            onChange={(e) => setDebug(e.target.checked)}
          />
          Debug
        </label>

        <button
          type="submit"
          disabled={isLoading}
          style={{
            padding: "10px 16px",
            borderRadius: 12,
            cursor: isLoading ? "not-allowed" : "pointer",
          }}
        >
          {isLoading ? "Searching…" : "Ask"}
        </button>
      </div>
    </form>
  );
}
