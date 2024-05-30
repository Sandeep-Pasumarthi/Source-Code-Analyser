from git import Repo
from pathlib import Path


def clone_repo(repo_url: str, path: Path | str) -> tuple | None:
    try:
        repo = Repo.clone_from(repo_url, path)
        return Path(path), repo.head.reference
    except Exception as e:
        print(e)
        return False
