from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings

embeddings=OllamaEmbeddings(
    model="nomic-embed-text"
)

vectorstore=FAISS.load_local(
    "vectorstore/fiass_index",
    embeddings,
    allow_dangerous_deserialization=True
)

retriever=vectorstore.as_retriever(search_kwargs={"k":3})

query="Explain normalization in DBMS"

docs=retriever.invoke(query)

print("\n retrieved chunks: \n")

for i,doc in enumerate(docs,start=1):
    print(f"--chunk {i} --")
    print(doc.page_content[:500])
    print("Metadata:",doc.metadata)