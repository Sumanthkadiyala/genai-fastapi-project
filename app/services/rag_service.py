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