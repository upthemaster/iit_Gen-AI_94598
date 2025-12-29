from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.embeddings import init_embeddings
import os

class VectorStoreManager:
    def __init__(self, persist_dir="data/chroma_db"):
        self.embedding = init_embeddings(
            model="text-embedding-nomic-embed-text-v1.5",
            provider="openai",
            base_url="http://127.0.0.1:1234/v1",
            api_key="not-required",
            check_embedding_ctx_length=False
        )

        self.persist_dir = persist_dir

        self.vectordb = Chroma(
            persist_directory=self.persist_dir,
            embedding_function=self.embedding
        )

    def add_resume(self, pdf_path):
        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(docs)

        for chunk in chunks:
            chunk.metadata["source"] = os.path.basename(pdf_path)

        self.vectordb.add_documents(chunks)
        self.vectordb.persist()


    def delete_resume_vectors(self, filename):
        self.vectordb._collection.delete(
            where={"source": filename}
        )
        self.vectordb.persist()

    def similarity_search(self, query, k):
        return self.vectordb.similarity_search(query, k=k)
