from langchain_community.document_loaders import GitLoader
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings

from pathlib import Path
from dotenv import load_dotenv

import os
import shutil

load_dotenv()


class EmbeddingsGenerator:
    def __init__(self, path: Path | str, git_branch: str, programming_language: str, namespace: str, repo_id: str):
        self.path = path
        self.git_branch = git_branch
        self.programming_language = programming_language
        self.repo_id = repo_id
        self.__splitter = RecursiveCharacterTextSplitter.from_language(language=self.programming_language, chunk_size=2000, chunk_overlap=200)
        self.__vector_store = PineconeVectorStore(index_name=os.getenv("PINECONE_INDEX"), namespace=namespace, embedding=OpenAIEmbeddings(model=os.getenv("EMBEDDING_MODEL"), dimensions=1024), text_key=os.getenv("PINECONE_TEXT_KEY"))

    def __generate_documents(self):
        self.loader = GitLoader(repo_path=self.path, branch=self.git_branch)
        self.documents = self.loader.load()

        for document in self.documents:
            document.metadata["repo_id"] = self.repo_id
    
    def __generate_chunks(self):
        self.chunks = self.__splitter.split_documents(self.documents)

    def __generate_embeddings(self):
        chunk_size = 100
        chunks = [self.chunks[i:i + chunk_size] for i in range(0, len(self.chunks), chunk_size)]
        [self.__vector_store.add_documents(chunk) for chunk in chunks]

    def run(self):
        self.__generate_documents()
        self.__generate_chunks()
        self.__generate_embeddings()
        return True
    
    def remove_repo(self):
        shutil.rmtree(self.path)
        return True
