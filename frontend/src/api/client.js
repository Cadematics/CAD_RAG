import axios from "axios";

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000",
  timeout: 60000,
});

export async function queryRag({ query, top_k, domain, debug }) {
  const res = await api.post("/api/query/", {
    query,
    top_k,
    domain: domain || "",
    debug: !!debug,
  });
  return res.data;
}

export async function getChunk(chunkId) {
  const res = await api.get(`/api/chunks/${chunkId}/`);
  return res.data;
}
