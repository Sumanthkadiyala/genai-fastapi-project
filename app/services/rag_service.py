from app.services.vector_store_service import load_vector_store
from app.services.llm_service import get_llm


def ask_rag(question: str):
    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 4}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    prompt = f"""
You are a helpful assistant.
Answer ONLY using the provided context.
If the answer is not in the context, say: 'I could not find that information in the documents.'

Context:
{context}

Question:
{question}
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    return response.content
'''

from app.services.vector_store_service import load_vector_store
from app.services.llm_service import get_llm


def ask_rag(question: str):
    # Load FAISS vector store
    vector_store = load_vector_store()

    # Retrieve top 4 chunks with similarity scores
    docs_with_scores = vector_store.similarity_search_with_score(
        query=question,
        k=4
    )

    # If nothing retrieved
    if not docs_with_scores:
        return {
            "answer": "I could not find that information in the documents.",
            "confidence_score": 0.0,
            "retrieved_chunks": 0,
            "citations": []
        }

    # Separate documents and scores
    docs = []
    scores = []

    for doc, score in docs_with_scores:
        docs.append(doc)
        scores.append(score)

    # Build context for LLM
    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    # Prompt
    prompt = f"""
You are a helpful assistant.

Answer ONLY using the provided context.
If the answer is not present in the context, say:
'I could not find that information in the documents.'

At the end of the answer, include the relevant source document names.

Context:
{context}

Question:
{question}
"""

    # Call Gemini
    llm = get_llm()
    response = llm.invoke(prompt)
    answer = response.content

    # Build citations
    citations = []

    for doc, score in docs_with_scores:
        source_path = doc.metadata.get("source", "Unknown Source")
        page = doc.metadata.get("page", "N/A")

        # Extract filename only
        source_document = source_path.split("/")[-1].split("\\")[-1]

        # Short excerpt for reference
        excerpt = doc.page_content[:200].replace("\n", " ")

        citations.append({
            "source_document": source_document,
            "page_number": page + 1 if isinstance(page, int) else page,
            "similarity_score": float(score),
            "excerpt": excerpt
        })

    # Convert FAISS distances into a confidence score (0-1)
    # Lower distance = better match
    best_distance = min(scores)

    # Simple heuristic conversion
    confidence_score = 1 / (1 + best_distance)

    # Round for cleaner API response
    confidence_score = round(confidence_score, 4)

    return {
        "answer": answer,
        "confidence_score": confidence_score,
        "retrieved_chunks": len(docs),
        "citations": citations
    }
    '''