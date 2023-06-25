import os

from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter, SpacyTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.chains import VectorDBQA
from langchain import OpenAI
import pinecone

path = "/Users/opeoluwao/Library/CloudStorage/Dropbox/Ope/Personal/Projects/langchain/resources/data/mediumblog1.txt"

pinecone.init(
    api_key=os.environ.get("PINECONE_API_KEY"),
    environment=os.environ.get("PINECONE_ENVIRONMENT"),
)

if __name__ == "__main__":
    print("Hello Vectorstore")
    loader = TextLoader(path)
    document = loader.load()
    # print(document)
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    text_splitter = SpacyTextSplitter()
    texts = text_splitter.split_documents(document)
    print(len(texts))

    embeddings = OpenAIEmbeddings(openai_api_key=os.environ.get("OPENAI_API_KEY"))
    docsearch = Pinecone.from_documents(
        texts, embeddings, index_name="medium-blogs-embeddings-index"
    )
