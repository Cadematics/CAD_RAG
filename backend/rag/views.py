from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rag.serializers import QuerySerializer
from rag.graphs.query_graph import build_query_graph
from rag.retrieval.answer import generate_answer
import os
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# TEMP: simple dummy LLM (safe, no external deps)
# --------------------------------------------------
def dummy_llm(prompt: str) -> str:
    return "Answer generation not yet connected."

## OPENAI  ##
from openai import OpenAI
client = OpenAI()

def openai_llm(prompt):
    return client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

## OLLAMA ##
import subprocess

def ollama_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3:8b"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout




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

    answer = generate_answer(
        data["query"],
        context,
        dummy_llm,
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



# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status

# from rag.serializers import QuerySerializer
# from rag.graphs.query_graph import build_query_graph
# from rag.retrieval.answer import generate_answer
# # from rag.llms.openai_llm import OpenAILLM  # or Gemini wrapper

# from django.views.decorators.csrf import csrf_exempt


# from rest_framework.decorators import api_view
# from rest_framework.response import Response



# # TEMP: simple dummy LLM for now
# def dummy_llm(prompt: str) -> str:
#     return "Answer generation not yet connected."




# @api_view(['GET'])
# def health(request):
#     return Response({"status": "ok"})



# @csrf_exempt
# @api_view(["POST"])
# def query_rag(request):
#     serializer = QuerySerializer(data=request.data)
#     serializer.is_valid(raise_exception=True)

#     data = serializer.validated_data

#     graph = build_query_graph()
#     state = graph.invoke({
#         "query": data["query"],
#         "domain": data.get("domain"),
#         "top_k": data["top_k"]
#     })


#     # llm = OpenAILLM()  # simple wrapper
#     llm = dummy_llm  # simple wrapper

#     answer = generate_answer(
#         data["query"],
#         state.context,
#         llm
#     )

#     response = {
#         "answer": answer,
#         "citations": state.citations,
#     }

#     if data["debug"]:
#         response["debug"] = {
#             "num_chunks": len(state.citations),
#             "scores": [c["score"] for c in state.citations]
#         }

#     return Response(response, status=status.HTTP_200_OK)

