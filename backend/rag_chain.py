from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings,OllamaLLM

def load_vectorstore():
    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    vectorstore=FAISS.load_local(
        folder_path="vectorstore/fiass_index",
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )
    return vectorstore

def get_retriever(vectorstore):
    return vectorstore.as_retriever(search_kwargs={"k":4})

def load_llm():
    return OllamaLLM(model="gemma3:4b",temperature=0)

def answer_theory(llm, context, query):
    prompt = f"""
You are a GATE exam assistant.

Answer the question using ONLY the context below.
Write in exam-oriented language.

Context:
{context}

Question:
{query}

Answer:
"""
    return llm.invoke(prompt)

def answer_pyq(llm, context, metadata):
    q_type = metadata.get("question_type")
    answer = metadata.get("answer")
    if q_type == "MCQ":
        prompt = f"""
This is a GATE MCQ.

Question:
{context}

Correct Option:
{answer}

Explain why this option is correct.
Also briefly explain why other options are incorrect.
"""
    return llm.invoke(prompt)

def answer_gate_question(query):
    vectorstore = load_vectorstore()
    retriever = get_retriever(vectorstore)
    llm = load_llm()

    docs = retriever.invoke(query)

    if not docs:
        return "No relevant information found."

    doc = docs[0]  # best match
    metadata = doc.metadata
    context = doc.page_content

    source = metadata.get("source")

    if source == "notes":
        return answer_theory(llm, context, query)

    if source == "pyq":
        return answer_pyq(llm, context, metadata)
