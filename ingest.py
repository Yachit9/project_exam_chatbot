import os
import re
import pdfplumber
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv
load_dotenv()

def load_notes(folder_path):
    documents=[]

    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            file_path=os.path.join(folder_path,file)
            loader=PyPDFLoader(file_path)
            pdf_docs=loader.load()

            for docs in pdf_docs:
                docs.metadata["source"]="notes"
                docs.metadata["subject"]=file.replace(".pdf","").upper()
            documents.extend(pdf_docs)
    return documents

def chunk_docs(documents):
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200
    )
    chunks=splitter.split_documents(documents)
    return chunks

def create_vectorstore(chunks):
    embeddings=OllamaEmbeddings(model="nomic-embed-text")

    vectorstore=FAISS.from_documents(
        documents=chunks,
        embedding=embeddings
    )
    vectorstore.save_local('vectorstore/fiass_index/')

def load_gate_answer_key(answer_key_pdf_path):
    answer_map={}

    with pdfplumber.open(answer_key_pdf_path) as pdf:
        for page in pdf.pages:
            table=page.extract_table()

            if not table:
                continue
            for row in table[1:]:
                q_no=row[0]
                q_type=row[2]
                key=row[4]

                if q_type=="MCQ" and key in ["A","B","C","D"]:
                    answer_map[str(q_no)]=key
    return answer_map

def main():
    notes_path="data/notes"

    print("Loading notes....")
    notes=load_notes(notes_path)
    print(f"Loaded {len(notes)} pages")

    print("Chunking docs")
    chunks=chunk_docs(notes)
    print(f"created {len(chunks)} chunks")

    print("creating vector store")
    create_vectorstore(chunks)

    print("Notes ingestion complete")

    answers=load_gate_answer_key("data/pyq/answers/gate_2025_answer.pdf")
    print(list(answers.items())[:10])

if __name__=="__main__":
    main()