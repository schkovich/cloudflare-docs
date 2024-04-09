import argparse
import os
from llama_hub.github_repo import GithubClient
from loaders.github_loader import GithubContentLoader
from processors.content_processor import ContentProcessor
from persister.context_persister import ContextPersister
from persisters.sqlite_persister import SQLitePersister
from github_reader_factory import GithubRepositoryReaderFactory

def parse_arguments():
    parser = argparse.ArgumentParser(description="Your application description")
    parser.add_argument("--github-token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub access token")
    parser.add_argument("--owner", default=os.environ.get("REPO_OWNER"), help="Repository owner")
    parser.add_argument("--repo", default=os.environ.get("REPO_NAME"), help="Repository name")
    parser.add_argument("--commit", required=True, help="Commit SHA")
    parser.add_argument("--db-file", default=os.environ.get("DB_FILE"), help="SQLite database file path")
    return parser.parse_args()

# example
# python main.py --github-token <token> --owner <owner> --repo <repo> --commit <commit> --db-file <path_to_db>
def main():
    args = parse_arguments()

    # Initialize components and perform necessary actions
    loader = GithubContentLoader(
        GithubRepositoryReaderFactory.create_reader(
            GithubClient(args.github_token, args.owner, args.repo)
        )
    )
    content = loader.load_content(args.commit)

    processor = ContentProcessor()
    context = processor.process_content(content)

    persister = ContextPersister(SQLitePersister(args.db_file))
    persister.persist_data(context)

if __name__ == "__main__":
    main()
