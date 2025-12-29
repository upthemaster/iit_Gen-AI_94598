class RAGEngine:
    def __init__(self, vector_store):
        self.vector_store = vector_store

    def shortlist_resumes(self, job_description, top_n):
        results = self.vector_store.similarity_search(
            job_description,
            k=top_n
        )

        shortlisted = {}
        for doc in results:
            src = doc.metadata.get("source")
            shortlisted[src] = shortlisted.get(src, 0) + 1

        return list(shortlisted.keys())
