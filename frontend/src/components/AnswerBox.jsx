export default function AnswerBox({ answer }) {
  return (
    <div style={{ padding: 16, borderRadius: 14, border: "1px solid #333", marginTop: 16 }}>
      <h3 style={{ marginTop: 0 }}>Answer</h3>
      <p style={{ whiteSpace: "pre-wrap", marginBottom: 0 }}>{answer}</p>
    </div>
  );
}

