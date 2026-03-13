from duckduckgo_search import DDGS

class SearchManager:
    def __init__(self):
        pass

    def search_web(self, query):
        try:
            with DDGS() as ddgs:
                results = ddgs.text(query, max_results=5)
                if results:
                    # Format results as a string for context
                    formatted = "\n".join([f"- {r['title']}: {r['body']}" for r in results])
                    return formatted
                return "No web results found."
        except Exception as e:
            print(f"Direct DuckDuckGo search failed: {e}")
            return f"Search failed: {str(e)}"
    
