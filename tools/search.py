from ddgs import DDGS # Uses the updated entry point
import warnings

# Suppress the persistent rename warning
warnings.filterwarnings("ignore", message="This package .* has been renamed to `ddgs`!")

def web_search(query: str):
    """Robust search for Jarvis with error handling and limiters."""
    try:
        # Increased timeout to 25s for slower network conditions
        with DDGS(timeout=25) as ddgs:
            results = list(ddgs.text(query, max_results=4))
            
            if not results:
                return "I couldn't find any specific live results for that, sir."

            # Structure the data clearly for Llama 3
            output = [f"Search results for: {query}\n"]
            for r in results:
                # Truncate body to prevent token overflow/400 errors
                body = r['body'][:250] + "..." if len(r['body']) > 250 else r['body']
                output.append(f"Title: {r['title']}\nSnippet: {body}\nLink: {r['href']}\n")
            
            return "\n".join(output)
    except Exception as e:
        print(f"❌ Search Tool Error: {e}")
        return "Sir, I'm having trouble reaching the search network."