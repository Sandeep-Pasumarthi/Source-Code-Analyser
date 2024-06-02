from src.data_ingestion.github import clone_repo
from src.embeddings_generator.embeddings import EmbeddingsGenerator
from src.utils.langchain import get_language
from src.utils.common import random_text

from pathlib import Path


class GitHubIngestion:
    def __init__(self, repo_url: str, user_id: str):
        self.repo_url = repo_url
        self.user_id = user_id
    
    def generate_new_repo_id(self):
        self.repo_id = random_text(15)
    
    def data_ingestion(self, path: Path | str):
        result = clone_repo(repo_url=self.repo_url, path=path)
        if result:
            self.path = result[0]
            self.branch = result[1]
            return True
        return False
    
    def generate_embeddings(self):
        self.retirever = EmbeddingsGenerator(self.path, self.branch, get_language("python"), self.user_id).run()
    
    def run(self, path: Path | str):
        if self.data_ingestion(path):
            self.generate_embeddings()
            return self.repo_id
        else: return False
