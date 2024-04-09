from datetime import datetime, timezone

class GithubContentLoader:
    """Class responsible for loading content from GitHub using a provided GithubRepositoryReader."""

    def __init__(self, github_reader):
        """
        Initialize the GithubContentLoader.

        Parameters:
            github_reader (GithubRepositoryReader): An instance of GithubRepositoryReader to handle data loading.
        """
        self.github_reader = github_reader

    def load_content(self, commit):
        """
        Load content from GitHub using the provided GithubRepositoryReader.

        Returns:
            list: A list of loaded documents.
        """
        docs = self.github_reader.load_data(commit_sha = commit)
        import_date = datetime.now(timezone.utc)

        for document in docs:
            document.metadata.update({"commit_sha": self.commit, "created": timestamp, "import_date": int(import_date.timestamp())})

        return docs
