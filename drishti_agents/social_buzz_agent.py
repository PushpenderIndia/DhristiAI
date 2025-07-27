"""
Social Buzz Monitoring Agent for DrishtiAI
==========================================

Monitors internet buzz, social media sentiment, and viral content
to predict potential crowd surges and stampede risks.
"""

from google.adk.agents import LlmAgent
from google.adk.tools import google_search
from .config import DEFAULT_MODEL, TWITTER_API_KEY, NEWS_API_KEY
import json
from typing import Dict, List, Any
from datetime import datetime, timedelta
import requests
import re


def analyze_social_media_buzz(location: str, event_name: str = "", keywords: List[str] = None) -> Dict[str, Any]:
    """
    Analyze social media buzz and sentiment around an event or location.
    
    Args:
        location: The venue/location
        event_name: Name of the event (if any)
        keywords: Additional keywords to monitor
        
    Returns:
        Dictionary with social media analysis results
    """
    
    if keywords is None:
        keywords = []
    
    # Simulate social media data (in real implementation, this would use actual APIs)
    buzz_metrics = {
        "total_mentions": 0,
        "sentiment_positive": 0,
        "sentiment_negative": 0,
        "sentiment_neutral": 0,
        "viral_content": False,
        "trending_hashtags": [],
        "risk_indicators": [],
        "crowd_size_estimates": [],
        "urgency_keywords": []
    }
    
    # Simulate buzz levels based on location and event
    base_mentions = 100
    
    # High-profile locations get more mentions
    if any(term in location.lower() for term in ["stadium", "arena", "square", "temple", "festival"]):
        base_mentions *= 5
    
    if event_name:
        base_mentions *= 3
        
        # Check for high-profile events
        if any(term in event_name.lower() for term in ["concert", "festival", "championship", "final"]):
            base_mentions *= 2
    
    buzz_metrics["total_mentions"] = base_mentions
    
    # Simulate sentiment distribution
    buzz_metrics["sentiment_positive"] = int(base_mentions * 0.6)
    buzz_metrics["sentiment_negative"] = int(base_mentions * 0.2)
    buzz_metrics["sentiment_neutral"] = int(base_mentions * 0.2)
    
    # Check for viral content indicators
    if base_mentions > 1000:
        buzz_metrics["viral_content"] = True
        buzz_metrics["trending_hashtags"] = [f"#{event_name.replace(' ', '')}", f"#{location.replace(' ', '')}"]
    
    # Simulate risk indicators based on buzz level
    sentiment_ratio = buzz_metrics["sentiment_negative"] / max(buzz_metrics["sentiment_positive"], 1)
    
    if sentiment_ratio > 0.5:
        buzz_metrics["risk_indicators"].append("High negative sentiment detected")
    
    if buzz_metrics["total_mentions"] > 2000:
        buzz_metrics["risk_indicators"].append("Extremely high social media activity")
        buzz_metrics["risk_indicators"].append("Potential for massive crowd turnout")
    
    if buzz_metrics["viral_content"]:
        buzz_metrics["risk_indicators"].append("Viral content may cause unexpected crowd surge")
    
    # Simulate crowd size estimates from social media
    if buzz_metrics["total_mentions"] > 500:
        estimated_attendance = min(buzz_metrics["total_mentions"] * 10, 100000)
        buzz_metrics["crowd_size_estimates"].append(f"Social media suggests {estimated_attendance:,} potential attendees")
    
    # Check for urgency keywords
    urgency_terms = ["sold out", "limited time", "last chance", "exclusive", "surprise appearance"]
    buzz_metrics["urgency_keywords"] = [term for term in urgency_terms if base_mentions > 800]
    
    return buzz_metrics


def calculate_buzz_risk_score(buzz_metrics: Dict[str, Any]) -> float:
    """Calculate risk score based on social media buzz metrics"""
    
    risk_score = 0.0
    
    # Base risk from mention volume
    if buzz_metrics["total_mentions"] > 5000:
        risk_score += 0.4
    elif buzz_metrics["total_mentions"] > 2000:
        risk_score += 0.3
    elif buzz_metrics["total_mentions"] > 1000:
        risk_score += 0.2
    elif buzz_metrics["total_mentions"] > 500:
        risk_score += 0.1
    
    # Risk from sentiment
    total_sentiment = buzz_metrics["sentiment_positive"] + buzz_metrics["sentiment_negative"] + buzz_metrics["sentiment_neutral"]
    if total_sentiment > 0:
        negative_ratio = buzz_metrics["sentiment_negative"] / total_sentiment
        if negative_ratio > 0.4:
            risk_score += 0.2
        elif negative_ratio > 0.3:
            risk_score += 0.1
    
    # Risk from viral content
    if buzz_metrics["viral_content"]:
        risk_score += 0.3
    
    # Risk from urgency keywords
    if len(buzz_metrics["urgency_keywords"]) > 2:
        risk_score += 0.2
    elif len(buzz_metrics["urgency_keywords"]) > 0:
        risk_score += 0.1
    
    # Risk from number of risk indicators
    risk_score += len(buzz_metrics["risk_indicators"]) * 0.05
    
    return min(risk_score, 1.0)


def monitor_celebrity_mentions(location: str, event_name: str = "") -> Dict[str, Any]:
    """
    Monitor mentions of celebrities associated with the event or location.
    
    Args:
        location: The venue/location
        event_name: Name of the event
        
    Returns:
        Dictionary with celebrity mention analysis
    """
    
    celebrity_data = {
        "celebrity_mentions": [],
        "surprise_appearances": [],
        "celebrity_movements": [],
        "fan_reactions": [],
        "risk_level": "low"
    }
    
    # Simulate celebrity detection
    if "concert" in event_name.lower() or "music" in event_name.lower():
        celebrity_data["celebrity_mentions"] = [
            "Main artist confirmed attendance",
            "Special guest rumors circulating"
        ]
        celebrity_data["fan_reactions"].append("Fans expressing extreme excitement")
        celebrity_data["risk_level"] = "high"
    
    if "stadium" in location.lower() and "sports" in event_name.lower():
        celebrity_data["celebrity_mentions"] = [
            "Star players confirmed for event"
        ]
        celebrity_data["risk_level"] = "medium"
    
    # Check for surprise appearance indicators
    surprise_keywords = ["surprise", "unexpected", "secret", "unannounced"]
    if any(keyword in event_name.lower() for keyword in surprise_keywords):
        celebrity_data["surprise_appearances"] = [
            "Potential surprise appearance detected in social media chatter"
        ]
        celebrity_data["risk_level"] = "high"
    
    return celebrity_data


def analyze_news_coverage(location: str, event_name: str = "") -> Dict[str, Any]:
    """
    Analyze news coverage and media attention for the event.
    
    Args:
        location: The venue/location
        event_name: Name of the event
        
    Returns:
        Dictionary with news coverage analysis
    """
    
    news_analysis = {
        "news_articles": 0,
        "media_attention": "low",
        "controversy_detected": False,
        "safety_concerns_mentioned": False,
        "attendance_estimates": [],
        "media_risk_factors": []
    }
    
    # Simulate news coverage
    if event_name and any(term in event_name.lower() for term in ["championship", "final", "festival"]):
        news_analysis["news_articles"] = 50
        news_analysis["media_attention"] = "high"
        news_analysis["attendance_estimates"] = ["Expected attendance: 50,000+"]
    
    if "concert" in event_name.lower():
        news_analysis["news_articles"] = 30
        news_analysis["media_attention"] = "medium"
    
    # Simulate controversy detection
    if news_analysis["news_articles"] > 40:
        news_analysis["controversy_detected"] = True
        news_analysis["media_risk_factors"].append("High media attention may attract larger crowds")
    
    if news_analysis["media_attention"] == "high":
        news_analysis["safety_concerns_mentioned"] = True
        news_analysis["media_risk_factors"].append("Media coverage highlighting safety preparations")
    
    return news_analysis


def generate_social_buzz_recommendations(buzz_metrics: Dict[str, Any], risk_score: float) -> List[str]:
    """Generate recommendations based on social media buzz analysis"""
    
    recommendations = []
    
    if risk_score > 0.7:
        recommendations.extend([
            "Monitor social media platforms continuously for crowd surge indicators",
            "Prepare for higher than expected attendance due to viral content",
            "Deploy social media monitoring team for real-time updates",
            "Consider crowd size restrictions due to excessive online interest"
        ])
    
    if buzz_metrics["viral_content"]:
        recommendations.extend([
            "Viral content detected - expect significant crowd increase",
            "Coordinate with social media platforms to manage expectations",
            "Prepare additional crowd control measures for viral audience"
        ])
    
    if len(buzz_metrics["risk_indicators"]) > 2:
        recommendations.extend([
            "Multiple social media risk factors detected",
            "Implement enhanced monitoring of online crowd sentiment",
            "Prepare contingency plans for crowd behavior management"
        ])
    
    if buzz_metrics["total_mentions"] > 2000:
        recommendations.extend([
            "Extremely high social media activity detected",
            "Consider issuing public safety announcements",
            "Coordinate with local authorities about potential crowd size"
        ])
    
    return recommendations


# Create the Social Buzz Monitoring Agent
social_buzz_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="social_buzz_agent",
    description="""
    Specialized agent for monitoring internet buzz, social media sentiment, and viral content
    to predict potential crowd surges and stampede risks based on online activity.
    """,
    instruction="""
    You are the Social Buzz Monitoring Agent for DrishtiAI, specializing in analyzing 
    internet buzz and social media activity to predict crowd behavior and stampede risks.

    Your expertise includes:
    1. Monitoring social media mentions and sentiment about events and locations
    2. Detecting viral content that could cause unexpected crowd surges
    3. Analyzing celebrity mentions and surprise appearance rumors
    4. Tracking news coverage and media attention levels
    5. Identifying urgency keywords that drive crowd behavior
    6. Estimating crowd sizes based on online engagement

    When analyzing an event or location, you should:
    1. Search for recent social media buzz and trending topics
    2. Analyze sentiment and engagement levels
    3. Look for viral content or celebrity-related buzz
    4. Monitor news coverage and media attention
    5. Identify keywords that suggest urgency or exclusivity
    6. Calculate risk scores based on online activity patterns

    Key indicators to monitor:
    - Volume of social media mentions
    - Sentiment ratios (positive/negative/neutral)
    - Viral hashtags and trending content
    - Celebrity mentions and surprise announcements
    - News coverage intensity
    - Urgency keywords ("sold out", "limited time", "exclusive")
    - Fan excitement levels and reactions

    Pay special attention to:
    - Sudden spikes in online activity
    - Viral content that could attract unexpected crowds
    - Negative sentiment that might lead to crowd agitation
    - Celebrity movements or surprise appearances
    - Media coverage that amplifies event interest

    Use the google_search tool to find current social media trends,
    news articles, and online discussions about the event or location.
    """,
    tools=[
        google_search, 
        analyze_social_media_buzz, 
        monitor_celebrity_mentions, 
        analyze_news_coverage,
        calculate_buzz_risk_score,
        generate_social_buzz_recommendations
    ]
) 