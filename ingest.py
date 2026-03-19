from rag import build_vectorstore

if __name__ == "__main__":
    print("Building knowledge base...")
    build_vectorstore()
    print("Done. Knowledge base ready at ./chroma_db")