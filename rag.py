import os
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = "./chroma_db"
KNOWLEDGE_DIR = "./knowledge"


def load_documents():
    from langchain_core.documents import Document
    docs = []
    if not os.path.exists(KNOWLEDGE_DIR):
        raise FileNotFoundError(f"Knowledge directory '{KNOWLEDGE_DIR}' not found.")
    for fname in os.listdir(KNOWLEDGE_DIR):
        if fname.endswith(".txt"):
            fpath = os.path.join(KNOWLEDGE_DIR, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = [b.strip() for b in content.split("\n\n") if b.strip()]
            for block in blocks:
                docs.append(Document(
                    page_content=block,
                    metadata={"source": fname}
                ))
    return docs


def get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True}
    )


def build_vectorstore():
    from langchain_community.vectorstores import Chroma
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    docs = load_documents()
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vectorstore


def load_vectorstore():
    from langchain_community.vectorstores import Chroma
    if not os.path.exists(CHROMA_DIR):
        return build_vectorstore()
    return Chroma(
        persist_directory=CHROMA_DIR,
        embedding_function=get_embeddings()
    )


def get_retriever():
    vs = load_vectorstore()
    return vs.as_retriever(search_kwargs={"k": 3})


if __name__ == "__main__":
    print("Building knowledge base...")
    build_vectorstore()
    print("Done.")