"""
Wikipedia Historical Analysis Agent
==================================

Searches Wikipedia for historical stampede incidents and venue information
to provide context for risk assessment.
"""

import wikipedia
from google.adk.agents import LlmAgent
from .config import DEFAULT_MODEL

def search_wikipedia_stampedes(query: str, max_results: int = 3) -> str:
    """
    Search Wikipedia for information about stampedes, crowd disasters, or venue incidents.
    
    Args:
        query: Search query (venue name, event type, or general stampede info)
        max_results: Maximum number of results to return (default: 3)
        
    Returns:
        str: Formatted search results with key information
    """
    try:
        # Search for pages related to the query
        search_results = wikipedia.search(f"{query} stampede crowd disaster", results=max_results)
        
        if not search_results:
            # Try broader search
            search_results = wikipedia.search(f"{query} incident crowd", results=max_results)
        
        if not search_results:
            return f"No Wikipedia articles found for '{query}' related to crowd incidents."
        
        results_text = f"📚 Wikipedia Historical Research: '{query}'\n\n"
        
        for i, title in enumerate(search_results, 1):
            try:
                # Get page summary
                page = wikipedia.page(title)
                summary = wikipedia.summary(title, sentences=2)
                
                results_text += f"{i}. **{title}**\n"
                results_text += f"   {summary}\n"
                results_text += f"   URL: {page.url}\n\n"
                
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation by taking the first option
                try:
                    page = wikipedia.page(e.options[0])
                    summary = wikipedia.summary(e.options[0], sentences=2)
                    results_text += f"{i}. **{e.options[0]}**\n"
                    results_text += f"   {summary}\n\n"
                except:
                    results_text += f"{i}. **{title}** - Multiple pages found, couldn't retrieve specific content.\n\n"
                    
            except wikipedia.exceptions.PageError:
                results_text += f"{i}. **{title}** - Page not found or unavailable.\n\n"
                
            except Exception as e:
                results_text += f"{i}. **{title}** - Error retrieving content: {str(e)}\n\n"
        
        return results_text
        
    except Exception as e:
        return f"Error searching Wikipedia: {str(e)}"

def search_venue_history(venue_name: str) -> str:
    """
    Search for historical information about a specific venue.
    
    Args:
        venue_name: Name of the venue to research
        
    Returns:
        str: Historical information about the venue
    """
    try:
        # Search for the venue specifically
        search_results = wikipedia.search(venue_name, results=2)
        
        if not search_results:
            return f"No Wikipedia information found for venue '{venue_name}'."
            
        results_text = f"🏛️ Venue History: {venue_name}\n\n"
        
        for title in search_results:
            try:
                summary = wikipedia.summary(title, sentences=3)
                page = wikipedia.page(title)
                
                # Check if this is likely the venue we want
                if venue_name.lower() in title.lower():
                    results_text += f"**{title}**\n"
                    results_text += f"{summary}\n"
                    results_text += f"URL: {page.url}\n\n"
                    break
                    
            except:
                continue
                
        return results_text
        
    except Exception as e:
        return f"Error searching venue history: {str(e)}"

# Create Wikipedia Historical Analysis Agent
wikipedia_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="wikipedia_historical_agent",
    description="""
    Historical Analysis Agent using Wikipedia
    
    Researches past stampede incidents, crowd disasters, and venue histories
    to provide context for stampede risk assessment.
    """,
    instruction="""
    You are a historical research specialist focused on crowd safety incidents.
    
    Your role is to provide historical context for stampede risk assessments by:
    
    1. **Researching Past Incidents**: Search for similar stampede or crowd disaster incidents
    2. **Venue History**: Find information about specific venues and their safety record
    3. **Pattern Recognition**: Identify common factors in historical crowd disasters
    4. **Lessons Learned**: Extract safety insights from past incidents
    
    When asked to research:
    - Use the search_wikipedia_stampedes tool for general incident research
    - Use the search_venue_history tool for specific venue information
    - Focus on factual, historical information
    - Highlight relevant safety lessons and risk factors
    
    Always provide accurate, factual information from reliable sources.
    Keep responses focused on safety-relevant historical context.
    """,
    tools=[search_wikipedia_stampedes, search_venue_history]
) 