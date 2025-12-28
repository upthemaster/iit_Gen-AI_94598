import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.chat_models import init_chat_model
import streamlit as st

st.title("Sunbeam | Resume Handler...")

#embedding model
embed_model = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.Client(settings=chromadb.Settings(persist_directory="./chroma_db"))
collection = client.get_or_create_collection(name = "demo")

#load document
loader = DirectoryLoader(
        path="E:\\SUNBEAM_INTERNSHIP\\DAY_2\\iit_Gen-AI_94598\\CLASSWORK\\DAY8_CW\\fake_resumes",
        glob= "**/*.pdf",
        loader_cls=PyPDFLoader
    )

documents = loader.load()

#creating metadata
for doc in documents:
        doc.metadata["pdf_name"] = doc.metadata["source"].split("/")[-1]
        doc.metadata["page_number"] = doc.metadata["page"] + 1

#chunking of data
splitter = RecursiveCharacterTextSplitter(
        chunk_size = 800,
        chunk_overlap = 50,
        separators=[" ","\n","\n\n"]
)
chunks = splitter.split_documents(documents=documents)

# metadata for chunking level
texts = []
metadatas = []
ids = []
for idx, chunk in enumerate(chunks):
    texts.append(chunk.page_content)
    chunk.metadata["chunk_id"] = str(idx)
    chunk.metadata["chunk_size"] = len(chunk.page_content)
    metadatas.append(chunk.metadata)
    ids.append(str(idx))
embeddings = embed_model.embed_documents(texts)

#Add to Chroma
collection.add(ids=ids,documents=texts,embeddings=embeddings,metadatas=metadatas)
print("Document successfully added in chroma db")


#Read (similarity search)
query = st.chat_input("Enter job description about resumes...")
if query:
    query_embedding = embed_model.embed_query(query)
    results = collection.query(query_embeddings=[query_embedding],n_results=3)
    #print(results)


    #Inspect the result 
    for doc,meta in zip(results["documents"][0],results["metadatas"][0]):
        st.write("\n📄 Metadata:", meta)
        st.write("📝 Content:", doc[:300], "...")


    llm = init_chat_model(
        model = "google_gemma-3-4b-it",
        model_provider="openai",
        base_url = "http://127.0.0.1:1234/v1",
        api_key = "not-needed"
    )

    llm_prompt = f"""
        User Query:
        {query}

    Resume Context:
        {results}

    Instruction:
    From the resume context above, extract the names of candidates whose profiles
    best match the user query.

    Return the result as:
    - process and give result for an input for the query
    -  explanations
    -  extra text
    - Give result as only original content of data

    """
    result = llm.invoke(llm_prompt)
    st.write()
    st.write(result.content)