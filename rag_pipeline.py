
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter



embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

def ingest_pipeline():
    loader = PyPDFLoader("MSMED2006act.pdf")
    documents = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
    texts = text_splitter.split_documents(documents)

    if not texts:
        raise ValueError(
            "No text was extracted from MSMED2006act.pdf. "
            "The PDF may be scanned; run OCR before indexing it."
        )
    
    db = Chroma.from_documents(documents=texts, embedding=embeddings)
    return db

db = ingest_pipeline()
count = db._collection.count()
print(f"Number of documents in the database: {count}")