export default function DebugPanel({ debug }) {
  return (
    <div style={{ padding: 16, borderRadius: 14, border: "1px dashed #555", marginTop: 16 }}>
      <h3 style={{ marginTop: 0 }}>Debug</h3>
      <pre style={{ whiteSpace: "pre-wrap", margin: 0 }}>
        {JSON.stringify(debug, null, 2)}
      </pre>
    </div>
  );
}

