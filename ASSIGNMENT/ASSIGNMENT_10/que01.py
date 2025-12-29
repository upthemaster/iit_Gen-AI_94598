# Basic fixed size chunking
from langchain_text_splitters import CharacterTextSplitter

raw_text = ["I love football. "
            "Soccer is my favourite sport." 
            "I love pasta"]

text_splitter = CharacterTextSplitter(chunk_size=50,chunk_overlap=10)
docs = text_splitter.create_documents(raw_text)

print(docs)