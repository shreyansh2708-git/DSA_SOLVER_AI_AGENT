from langchain_community.tools.tavily_search import TavilySearchResults

def get_search_tool():
    return TavilySearchResults(
        max_results=3,
        description=(
            "Search internet for DSA problems, algorithms, similar competitive "
            "programming problems, or solution approaches."
        )
    )