import { useState } from "react";
import QueryForm from "./components/QueryForm";
import AnswerBox from "./components/AnswerBox";
import CitationList from "./components/CitationList";
import DebugPanel from "./components/DebugPanel";
import ChunkModal from "./components/ChunkModal";
import { queryRag, getChunk } from "./api/client";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errMsg, setErrMsg] = useState("");

  const [chunkOpen, setChunkOpen] = useState(false);
  const [chunkLoading, setChunkLoading] = useState(false);
  const [chunkError, setChunkError] = useState("");
  const [chunk, setChunk] = useState(null);

  const onSubmit = async (payload) => {
    setErrMsg("");
    setLoading(true);
    try {
      const data = await queryRag(payload);
      setResult(data);
    } catch (err) {
      setResult(null);
      setErrMsg(err?.response?.data ? JSON.stringify(err.response.data) : (err.message || "Request failed"));
    } finally {
      setLoading(false);
    }
  };

  const onOpenChunk = async (chunkId) => {
    setChunkOpen(true);
    setChunk(null);
    setChunkError("");
    setChunkLoading(true);

    try {
      const data = await getChunk(chunkId);
      setChunk(data);
    } catch (err) {
      setChunkError(err?.response?.data ? JSON.stringify(err.response.data) : (err.message || "Failed to load chunk"));
    } finally {
      setChunkLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: 980, margin: "0 auto", padding: 18 }}>
      <h1 style={{ marginTop: 0 }}>CAD / CAE RAG Assistant</h1>
      <p style={{ marginTop: 6, opacity: 0.85 }}>
        Ask questions about your ingested CAD/CAM/CFD/FEA papers. Answers are grounded with citations.
      </p>

      <QueryForm onSubmit={onSubmit} isLoading={loading} />

      {errMsg && (
        <div style={{ marginTop: 16, padding: 12, borderRadius: 12, border: "1px solid tomato" }}>
          <b>Error:</b> <span style={{ whiteSpace: "pre-wrap" }}>{errMsg}</span>
        </div>
      )}

      {result?.answer && <AnswerBox answer={result.answer} />}

      {result && (
        <CitationList citations={result.citations} onOpenChunk={onOpenChunk} />
      )}

      {result?.debug && <DebugPanel debug={result.debug} />}

      <ChunkModal
        open={chunkOpen}
        chunk={chunk}
        loading={chunkLoading}
        error={chunkError}
        onClose={() => setChunkOpen(false)}
      />
    </div>
  );
}




// import { useEffect, useState } from "react";
// import axios from "axios";

// function App() {
//   const [status, setStatus] = useState("loading");

//   useEffect(() => {
//     axios.get("http://127.0.0.1:8000/api/health/")
//       .then(res => setStatus(res.data.status))
//       .catch(() => setStatus("error"));
//   }, []);

//   return (
//     <div style={{ padding: 20 }}>
//       <h1>CAD RAG System</h1>
//       <p>Backend status: {status}</p>
//     </div>
//   );
// }

// export default App;
