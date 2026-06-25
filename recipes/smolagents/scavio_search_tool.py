from smolagents import Tool


class ScavioSearchTool(Tool):
    """Web search tool that performs searches using the Scavio API (https://scavio.dev).

    Scavio is a unified search API for AI agents. This tool uses its Google web search
    endpoint and returns the top results as markdown. The same `scavio` SDK also covers
    YouTube, Amazon, Walmart, Reddit, TikTok and Instagram for users who need them.

    Args:
        api_key (`str`, *optional*): Scavio API key. Falls back to the `SCAVIO_API_KEY` env variable.
        max_results (`int`, default `10`): Maximum number of search results to return.
        country_code (`str`, *optional*): Two-letter country code to localize results (e.g. "us").

    Examples:
        ```python
        >>> from scavio_search_tool import ScavioSearchTool
        >>> web_search_tool = ScavioSearchTool(max_results=5)
        >>> results = web_search_tool("Hugging Face")
        >>> print(results)
        ```
    """

    name = "web_search"
    description = "Performs a web search using the Scavio API and returns the top results formatted as markdown with titles, links, and descriptions."
    inputs = {"query": {"type": "string", "description": "The search query to perform."}}
    output_type = "string"

    def __init__(self, api_key: str | None = None, max_results: int = 10, country_code: str | None = None):
        super().__init__()
        import os

        try:
            from scavio import ScavioClient
        except ImportError as e:
            raise ImportError(
                "You must install package `scavio` to run this tool: for instance run `pip install scavio`."
            ) from e
        self.api_key = api_key or os.getenv("SCAVIO_API_KEY")
        if self.api_key is None:
            raise ValueError("Missing API key. Make sure you have 'SCAVIO_API_KEY' in your env variables.")
        self.max_results = max_results
        self.country_code = country_code
        self.client = ScavioClient(api_key=self.api_key)

    def forward(self, query: str) -> str:
        response = self.client.google.search(query, country_code=self.country_code)
        results = response.get("results", [])
        if not results:
            raise Exception(f"No results found for query: '{query}'. Use a less restrictive query.")
        web_snippets = []
        for idx, page in enumerate(results[: self.max_results], start=1):
            title = page.get("title", "")
            link = page.get("url") or page.get("link", "")
            snippet = page.get("content") or page.get("description") or page.get("snippet", "")
            web_snippets.append(f"{idx}. [{title}]({link})\n{snippet}")
        return "## Search Results\n\n" + "\n\n".join(web_snippets)
