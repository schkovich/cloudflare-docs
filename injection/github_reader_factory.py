from llama_hub.github_repo import GithubRepositoryReader

class GithubRepositoryReaderFactory:
    @staticmethod
    def create_reader(github_client: GithubClient, owner: str, repo: str,
                      filter_directories: list = ["/"],
                      filter_file_extensions: list = [".md"],
                      verbose: bool = False,
                      concurrent_requests: int = 10,
                      timeout: int = 5) -> GithubRepositoryReader:
        """
        Create an instance of GithubRepositoryReader.

        Parameters:
            github_client (GithubClient): An instance of GithubClient for interacting with the GitHub API.
            owner (str): Repository owner.
            repo (str): Repository name.
            filter_directories (list, optional): List of directories to filter. Default is ["/"].
            filter_file_extensions (list, optional): List of file extensions to filter. Default is [".md"].
            verbose (bool, optional): Whether to enable verbose mode. Default is False.
            concurrent_requests (int, optional): Number of concurrent requests. Default is 10.
            timeout (int, optional): Timeout for requests in seconds. Default is 5.

        Returns:
            GithubRepositoryReader: An instance of GithubRepositoryReader.
        """
        return GithubRepositoryReader(
            github_client=github_client,
            owner=owner,
            repo=repo,
            filter_directories=filter_directories,
            filter_file_extensions=filter_file_extensions,
            verbose=verbose,
            concurrent_requests=concurrent_requests,
            timeout=timeout
        )
