
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rag.serializers import QuerySerializer
from rag.graphs.query_graph import build_query_graph
from rag.retrieval.answer import generate_answer
import os
from dotenv import load_dotenv
from rag.llms.openai_llm import OpenAILLM
from django.shortcuts import get_object_or_404
from rag.models import Chunk


load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    print("⚠️ WARNING: OPENAI_API_KEY not found in environment")
else:
    print("✅ OPENAI_API_KEY found in environment") 






# --------------------------------------------------
# Health check
# --------------------------------------------------
@api_view(["GET"])
def health(request):
    return Response({"status": "ok"})





# --------------------------------------------------
# Main RAG query endpoint
# --------------------------------------------------
@csrf_exempt
@api_view(["POST"])
def query_rag(request):
    serializer = QuerySerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data

    graph = build_query_graph()

    # LangGraph returns a DICT, not an object
    state = graph.invoke({
        "query": data["query"],
        "domain": data.get("domain"),
        "top_k": data["top_k"],
    })

    # Defensive access (important)
    context = state.get("context", "")
    citations = state.get("citations", [])

    llm = OpenAILLM()


    answer = generate_answer(
        data["query"],
        context,
        llm,
    )

    response = {
        "answer": answer,
        "citations": citations,
    }

    if data.get("debug"):
        response["debug"] = {
            "num_chunks": len(citations),
            "scores": [c["score"] for c in citations],
        }

    return Response(response, status=status.HTTP_200_OK)



# -------------------------
# Chunk detail endpoint
# -------------------------f


@api_view(["GET"])
def chunk_detail(request, chunk_id):
    chunk = get_object_or_404(Chunk, id=chunk_id)

    return Response({
        "id": str(chunk.id),
        "paper": chunk.paper.title,
        "section": chunk.section,
        "page_start": chunk.page_start,
        "page_end": chunk.page_end,
        "chunk_strategy": chunk.chunk_strategy,
        "embedding_model": chunk.embedding_model,
        "text": chunk.text,
    })