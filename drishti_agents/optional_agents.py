"""
Optional Agents for DrishtiAI
=============================

These agents only load if their respective API keys are configured.
They provide enhanced analysis capabilities when external services are available.
"""

import os
from google.adk.agents import LlmAgent
from .config import DEFAULT_MODEL

# Check for available API keys
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
REDDIT_API_KEY = os.getenv("REDDIT_API_KEY") 
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Optional Agents List
optional_agents = []

# Social Media Monitoring Agent (if Twitter/Reddit APIs available)
if TWITTER_API_KEY or REDDIT_API_KEY:
    def mock_social_analysis(event_name: str, location: str) -> str:
        """
        Analyze social media buzz around an event.
        Note: This is a placeholder function. Implement actual API calls when ready.
        """
        return f"""
        🔍 Social Media Analysis: {event_name} at {location}
        
        Twitter Activity: {'Available' if TWITTER_API_KEY else 'API key needed'}
        Reddit Discussions: {'Available' if REDDIT_API_KEY else 'API key needed'}
        
        Buzz Level: [Requires API implementation]
        Trending Topics: [Requires API implementation] 
        Sentiment: [Requires API implementation]
        
        Note: Connect your social media API keys to get real-time analysis.
        """
    
    social_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="social_media_agent",
        description="Monitors social media buzz and viral content that could drive crowds",
        instruction="""
        You analyze social media activity around events to predict crowd behavior.
        
        Focus on:
        - Viral content driving attendance
        - Celebrity social media activity
        - Trending hashtags and mentions
        - Public sentiment and excitement levels
        
        Use the mock_social_analysis tool to gather social media intelligence.
        Provide insights on how social buzz might affect crowd size and behavior.
        """,
        tools=[mock_social_analysis]
    )
    optional_agents.append(social_agent)

# News Monitoring Agent (if News API available)
if NEWS_API_KEY:
    def mock_news_analysis(event_name: str, location: str) -> str:
        """
        Search for recent news about the event or venue.
        Note: This is a placeholder function. Implement actual News API calls when ready.
        """
        return f"""
        📰 News Analysis: {event_name} at {location}
        
        News API Status: {'Connected' if NEWS_API_KEY else 'API key needed'}
        
        Recent Headlines: [Requires API implementation]
        Media Coverage Level: [Requires API implementation]
        Safety Concerns Mentioned: [Requires API implementation]
        
        Note: Connect your News API key to get real-time news analysis.
        """
    
    news_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="news_monitoring_agent", 
        description="Monitors news coverage and media attention around events",
        instruction="""
        You analyze recent news coverage to identify factors that might affect crowd safety.
        
        Focus on:
        - Media attention driving crowds
        - Reported safety concerns
        - Coverage of similar events
        - Public statements by organizers
        
        Use the mock_news_analysis tool to gather news intelligence.
        Highlight any news factors that could impact crowd size or safety.
        """,
        tools=[mock_news_analysis]
    )
    optional_agents.append(news_agent)

# Weather Analysis Agent (always available)
def get_weather_analysis(location: str) -> str:
    """
    Get weather conditions using free wttr.in service (no API key required).
    
    Args:
        location: Location name (city, venue, etc.)
        
    Returns:
        str: Weather analysis with crowd safety implications
    """
    import requests
    import re
    
    try:
        # Use wttr.in free weather service
        url = f"http://wttr.in/{location}?format=j1"
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        weather_data = response.json()
        
        # Extract current weather
        current = weather_data['current_condition'][0]
        temp = int(current['temp_C'])
        feels_like = int(current['FeelsLikeC'])
        humidity = int(current['humidity'])
        desc = current['weatherDesc'][0]['value']
        wind_speed = int(current['windspeedKmph'])
        precipitation = float(current.get('precipMM', 0))
        
        # Analyze crowd impact
        crowd_impact = []
        risk_factors = []
        
        # Temperature analysis
        if temp < 0:
            crowd_impact.append("Extremely cold weather will drive crowds indoors")
            risk_factors.append("HIGH RISK: Indoor crowding expected")
        elif temp < 10:
            crowd_impact.append("Cold weather may increase indoor gathering preference")
            risk_factors.append("Moderate indoor crowding tendency")
        elif temp > 35:
            crowd_impact.append("Hot weather will drive crowds to seek air conditioning/shade")
            risk_factors.append("Heat-related crowd migration to cool areas")
        elif temp > 25 and humidity > 80:
            crowd_impact.append("Hot and humid conditions may cause discomfort and crowd movement")
            risk_factors.append("Discomfort-driven crowd behavior changes")
            
        # Weather condition analysis
        desc_lower = desc.lower()
        if any(word in desc_lower for word in ['rain', 'drizzle', 'shower']):
            crowd_impact.append("Precipitation will cause rapid indoor migration")
            risk_factors.append("CRITICAL RISK: Sudden mass indoor movement expected")
        elif any(word in desc_lower for word in ['snow', 'blizzard']):
            crowd_impact.append("Snow conditions will drive crowds indoors immediately")
            risk_factors.append("CRITICAL RISK: Emergency indoor crowding likely")
        elif any(word in desc_lower for word in ['fog', 'mist']):
            crowd_impact.append("Reduced visibility will impair crowd navigation and emergency exits")
            risk_factors.append("Navigation safety concerns - poor visibility")
        elif any(word in desc_lower for word in ['storm', 'thunder']):
            crowd_impact.append("Storm conditions create immediate safety risks")
            risk_factors.append("EMERGENCY RISK: Event cancellation may be necessary")
            
        # Wind analysis
        if wind_speed > 30:
            crowd_impact.append("High winds pose risks to outdoor structures and crowd stability")
            risk_factors.append("Structural safety concerns for outdoor events")
        elif wind_speed > 20:
            crowd_impact.append("Moderate winds may affect outdoor event comfort")
            risk_factors.append("Minor outdoor event impact")
            
        return f"""
🌤️ **REAL-TIME WEATHER ANALYSIS: {location}** (via wttr.in)

**Current Conditions:**
• Temperature: {temp}°C (feels like {feels_like}°C)
• Conditions: {desc}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} km/h
• Precipitation: {precipitation}mm

**Crowd Safety Impact:**
{chr(10).join(f"• {impact}" for impact in crowd_impact) if crowd_impact else "• Weather conditions are favorable for outdoor events"}

**Risk Factors:**
{chr(10).join(f"⚠️ {risk}" for risk in risk_factors) if risk_factors else "✅ No significant weather-related crowd risks identified"}

**Safety Recommendations:**
• {"Indoor venue capacity planning essential" if any("indoor" in impact.lower() for impact in crowd_impact) else "Standard outdoor precautions sufficient"}
• {"Enhanced exit signage and lighting needed" if any("visibility" in risk.lower() for risk in risk_factors) else "Standard visibility conditions"}
• {"Monitor for rapid crowd movements" if any("rapid" in impact.lower() for impact in crowd_impact) else "Weather stable for event duration"}
• {"Consider event postponement" if any("EMERGENCY" in risk for risk in risk_factors) else "Safe to proceed with normal precautions"}
        """
        
    except requests.exceptions.Timeout:
        return f"""
🌤️ **Weather Analysis: {location}**

⏱️ **Timeout:** Weather service temporarily slow. 

**Quick Assessment Needed:**
• Manually check current conditions in {location}
• Look for rain/snow that could drive crowds indoors suddenly
• Assess temperature comfort for outdoor events
• Check wind conditions for outdoor structures

**Recommendation:** Verify weather through local sources before event start.
        """
        
    except Exception as e:
        return f"""
🌤️ **Weather Analysis: {location}**

❌ **Service Unavailable:** {str(e)}

**Fallback Weather Assessment:**
Consider these key crowd safety factors:
• Precipitation → Immediate indoor crowding risk
• Temperature extremes → Comfort-driven crowd movement  
• High winds → Outdoor event safety concerns
• Poor visibility → Navigation and exit safety issues

**Action:** Use local weather apps/services for real-time conditions.
        """

# Premium Weather Analysis Agent (if Weather API available)
if WEATHER_API_KEY:
    def get_premium_weather_analysis(location: str) -> str:
        """
        Get current and forecast weather conditions using OpenWeatherMap API.
        
        Args:
            location: Location name (city, venue, etc.)
            
        Returns:
            str: Weather analysis with crowd safety implications
        """
        import requests
        
        try:
            # OpenWeatherMap API endpoint
            base_url = "http://api.openweathermap.org/data/2.5/weather"
            
            # Parameters for the API call
            params = {
                'q': location,
                'appid': WEATHER_API_KEY,
                'units': 'metric'  # Celsius
            }
            
            # Make API request
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            
            weather_data = response.json()
            
            # Extract key information
            temp = weather_data['main']['temp']
            feels_like = weather_data['main']['feels_like']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            wind_speed = weather_data['wind']['speed']
            
            # Check for precipitation
            rain = weather_data.get('rain', {}).get('1h', 0)
            snow = weather_data.get('snow', {}).get('1h', 0)
            
            # Analyze crowd impact
            crowd_impact = []
            risk_factors = []
            
            # Temperature analysis
            if temp < 0:
                crowd_impact.append("Extremely cold weather may drive crowds indoors")
                risk_factors.append("Indoor crowding risk")
            elif temp < 10:
                crowd_impact.append("Cold weather may increase indoor gathering")
                risk_factors.append("Moderate indoor crowding tendency")
            elif temp > 35:
                crowd_impact.append("Hot weather may drive crowds to seek shelter/shade")
                risk_factors.append("Heat-related crowd movement")
            
            # Precipitation analysis
            if rain > 0 or snow > 0:
                crowd_impact.append("Precipitation will drive crowds indoors rapidly")
                risk_factors.append("HIGH RISK: Rapid indoor migration")
            
            # Wind analysis
            if wind_speed > 10:
                crowd_impact.append("High winds may affect outdoor event safety")
                risk_factors.append("Outdoor event stability concerns")
            
            # Visibility analysis
            if 'fog' in description.lower() or 'mist' in description.lower():
                crowd_impact.append("Reduced visibility may impair crowd navigation")
                risk_factors.append("Navigation and exit visibility issues")
                
            return f"""
🌤️ **REAL-TIME WEATHER ANALYSIS: {location}**

**Current Conditions:**
• Temperature: {temp}°C (feels like {feels_like}°C)
• Conditions: {description.title()}
• Humidity: {humidity}%
• Wind Speed: {wind_speed} m/s
• Precipitation: {"Rain " + str(rain) + "mm" if rain > 0 else ""}{"Snow " + str(snow) + "mm" if snow > 0 else ""}

**Crowd Safety Impact:**
{chr(10).join(f"• {impact}" for impact in crowd_impact) if crowd_impact else "• Weather conditions are favorable for outdoor events"}

**Risk Factors:**
{chr(10).join(f"⚠️ {risk}" for risk in risk_factors) if risk_factors else "✅ No significant weather-related crowd risks identified"}

**Recommendations:**
• {"Indoor venue preparation recommended" if any("indoor" in impact.lower() for impact in crowd_impact) else "Standard outdoor precautions sufficient"}
• {"Enhanced exit signage needed due to visibility" if any("visibility" in risk.lower() for risk in risk_factors) else "Standard visibility conditions"}
• {"Monitor for rapid crowd movements if weather worsens" if rain > 0 or snow > 0 else "Weather stable for event duration"}
            """
            
        except requests.exceptions.RequestException as e:
            return f"""
🌤️ **Weather Analysis: {location}**

❌ **API Connection Error:** {str(e)}

🔄 **Fallback Analysis:**
Weather API temporarily unavailable. Consider these general weather factors:
• Check local weather conditions manually
• Monitor for precipitation that could drive crowds indoors
• Assess temperature comfort levels for outdoor events
• Evaluate wind conditions for outdoor structures
• Consider visibility conditions for crowd navigation

**Recommendation:** Verify current weather conditions through alternative sources.
            """
            
        except Exception as e:
            return f"""
🌤️ **Weather Analysis: {location}**

❌ **Analysis Error:** {str(e)}

Please check:
• Weather API key is valid
• Location name is correct
• Network connection is stable

**Fallback:** Use manual weather assessment for now.
            """
    
    weather_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="weather_analysis_agent",
        description="Analyzes real-time weather conditions and their impact on crowd behavior using OpenWeatherMap API",
        instruction="""
        You are a weather specialist focused on crowd safety analysis. 
        
        Your role is to analyze current weather conditions and predict how they will affect crowd behavior and safety.
        
        Key Analysis Areas:
        - Temperature effects on crowd comfort and movement
        - Precipitation driving rapid indoor migration
        - Wind impact on outdoor event stability
        - Visibility conditions affecting crowd navigation
        - Severe weather risks requiring immediate action
        
        Use the get_weather_analysis tool to fetch real-time weather data and provide specific safety recommendations based on current conditions.
        
        Focus on actionable insights that event organizers can use immediately.
        """,
        tools=[get_premium_weather_analysis]
    )
    optional_agents.append(weather_agent)

# Weather Agent (always available, no API key required)
weather_analysis_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="weather_analysis_agent",
    description="Analyzes weather conditions using free wttr.in service (no API key required)",
    instruction="""
    You are a weather specialist focused on crowd safety analysis using free weather data.
    
    Your role is to analyze current weather conditions and predict how they will affect crowd behavior and safety.
    
    Key Analysis Areas:
    - Temperature effects on crowd comfort and movement patterns
    - Precipitation causing rapid indoor migration 
    - Wind impact on outdoor event safety and structures
    - Visibility conditions affecting crowd navigation and emergency exits
    - Severe weather creating immediate safety risks
    
    Use the get_weather_analysis tool to fetch real-time weather data from wttr.in (a free service).
    
    Focus on providing actionable safety insights that event organizers can implement immediately.
    Always prioritize crowd safety and provide specific recommendations.
    """,
    tools=[get_weather_analysis]
)

# Always add the weather agent (no API key required)
optional_agents.append(weather_analysis_agent)

# Traffic Analysis using basic geocoding (always available)
def get_traffic_analysis(location: str) -> str:
    """
    Analyze transportation accessibility using free geocoding services.
    
    Args:
        location: Location name (city, venue, etc.)
        
    Returns:
        str: Transportation analysis with crowd safety implications
    """
    try:
        import requests
        from geopy.geocoders import Nominatim
        
        # Geocode the location using Nominatim (free)
        geolocator = Nominatim(user_agent="drishti_traffic_analysis")
        geo_location = geolocator.geocode(location, timeout=10)
        
        if not geo_location:
            return f"""
🚗 **Transportation Analysis: {location}**

❌ **Location Error:** Could not find location "{location}"

**Try these specific formats:**
• "Bangalore International Exhibition Centre, Tumkur Road, Bengaluru"
• "BIEC, Madavara, Bengaluru, Karnataka"  
• "MG Road, Bengaluru, Karnataka"
• Include state/country for better results
            """
        
        lat, lng = geo_location.latitude, geo_location.longitude
        formatted_address = geo_location.address
        
        # Extract location details for analysis
        address_parts = formatted_address.lower()
        city_analysis = {}
        
        # Analyze based on location characteristics
        if 'bengaluru' in address_parts or 'bangalore' in address_parts:
            city_analysis = {
                'metro_available': True,
                'traffic_density': 'high',
                'public_transit': 'good',
                'parking_challenge': 'high',
                'major_roads': ['Outer Ring Road', 'Hosur Road', 'Tumkur Road', 'Old Airport Road']
            }
        elif 'mumbai' in address_parts:
            city_analysis = {
                'metro_available': True,
                'traffic_density': 'very_high', 
                'public_transit': 'excellent',
                'parking_challenge': 'very_high',
                'major_roads': ['Western Express Highway', 'Eastern Express Highway', 'SV Road']
            }
        elif 'delhi' in address_parts:
            city_analysis = {
                'metro_available': True,
                'traffic_density': 'very_high',
                'public_transit': 'excellent', 
                'parking_challenge': 'high',
                'major_roads': ['Ring Road', 'Outer Ring Road', 'NH1']
            }
        else:
            # Generic analysis for other cities
            city_analysis = {
                'metro_available': False,
                'traffic_density': 'moderate',
                'public_transit': 'moderate',
                'parking_challenge': 'moderate',
                'major_roads': ['Main roads', 'Highway access']
            }
        
        # Generate crowd impact analysis
        crowd_impact = []
        risk_factors = []
        recommendations = []
        
        # Traffic density analysis
        if city_analysis['traffic_density'] == 'very_high':
            crowd_impact.append("Very high traffic density will cause severe delays and compressed arrivals")
            risk_factors.append("CRITICAL RISK: Mass simultaneous arrivals likely due to traffic delays")
            recommendations.append("URGENT: Implement staggered entry times and promote public transit heavily")
        elif city_analysis['traffic_density'] == 'high':
            crowd_impact.append("High traffic density may cause delays and crowd compression")
            risk_factors.append("HIGH RISK: Compressed arrival windows during peak hours")
            recommendations.append("Strongly encourage public transit and off-peak arrivals")
        else:
            crowd_impact.append("Moderate traffic conditions should allow steady crowd flow")
            recommendations.append("Standard traffic management should be sufficient")
        
        # Public transit analysis
        if city_analysis['metro_available']:
            crowd_impact.append("Metro system available for efficient crowd distribution")
            if city_analysis['public_transit'] == 'excellent':
                risk_factors.append("Good crowd distribution expected via metro")
            else:
                recommendations.append("Coordinate with metro authorities for increased frequency")
        else:
            crowd_impact.append("Limited metro access increases dependency on road transport")
            risk_factors.append("Road congestion risk due to limited rail transit")
            recommendations.append("Consider shuttle services from nearest rail stations")
        
        # Parking analysis
        if city_analysis['parking_challenge'] == 'very_high':
            crowd_impact.append("Severe parking shortage will force heavy public transit usage")
            risk_factors.append("Public transit overcrowding risk")
            recommendations.append("Strongly discourage private vehicles, promote metro/bus")
        elif city_analysis['parking_challenge'] == 'high':
            crowd_impact.append("Limited parking will increase public transit dependency")
            risk_factors.append("Mixed transportation load - monitor both road and transit")
            recommendations.append("Encourage public transit, arrange overflow parking with shuttles")
        else:
            crowd_impact.append("Adequate parking supports private vehicle access")
            recommendations.append("Standard parking management with clear directional signage")
        
        return f"""
🚗 **TRANSPORTATION ANALYSIS: {formatted_address}**

**Location Details:**
• Coordinates: {lat:.4f}, {lng:.4f}
• Metro Available: {"Yes" if city_analysis['metro_available'] else "No"}
• Traffic Density: {city_analysis['traffic_density'].replace('_', ' ').title()}
• Public Transit Quality: {city_analysis['public_transit'].title()}
• Parking Challenge Level: {city_analysis['parking_challenge'].replace('_', ' ').title()}

**Transportation Infrastructure:**
• Major Access Routes: {', '.join(city_analysis['major_roads'])}
• Public Transit: {"Metro + Bus network" if city_analysis['metro_available'] else "Bus network primarily"}
• Expected Vehicle Mix: {"70% Public Transit, 30% Private" if city_analysis['metro_available'] else "40% Public Transit, 60% Private"}

**Crowd Movement Impact:**
{chr(10).join(f"• {impact}" for impact in crowd_impact)}

**Risk Assessment:**
{chr(10).join(f"⚠️ {risk}" for risk in risk_factors) if risk_factors else "✅ No significant transportation-related crowd risks identified"}

**Actionable Recommendations:**
{chr(10).join(f"• {rec}" for rec in recommendations)}

**Traffic Timing Advice:**
• Arrive 60-90 minutes early during peak hours (5-7 PM)
• Consider arrivals before 4 PM or after 8 PM for easier access
• Monitor live traffic apps: Google Maps, Ola/Uber for route updates

**Emergency Protocols:**
• Coordinate with local traffic police 2 hours before event
• {"Activate metro crowd management protocols" if city_analysis['metro_available'] else "Prepare bus shuttle contingencies"}
• Establish alternate routes for emergency vehicle access

**Note:** This analysis combines geocoding with local transportation patterns. Check live traffic conditions closer to event time.
        """
        
    except ImportError as e:
        return f"""
🚗 **Transportation Analysis: {location}**

❌ **Missing Package:** {str(e)}

**Quick Install:** 
   pip install geopy

**Manual Assessment Guide:**
• Check Google Maps for live traffic to {location}
• Look for nearby metro/bus stations
• Assess parking availability in the area
• Identify major access roads and potential bottlenecks
        """
        
    except Exception as e:
        return f"""
🚗 **Transportation Analysis: {location}**

❌ **Analysis Error:** {str(e)}

**Alternative Analysis Steps:**
1. **Use Google Maps:** Search "{location}" and check:
   - Current traffic conditions (red/yellow/green roads)
   - Public transit directions and timing
   - Parking locations nearby

2. **Transportation Assessment:**
   - Count major roads leading to the venue
   - Check metro/bus station proximity (within 1-2km is good)
   - Assess if area is known for traffic congestion

3. **Crowd Impact Prediction:**
   - Heavy traffic = compressed arrivals = crowding risk
   - Good transit = distributed arrivals = safer
   - Limited parking = transit dependency = monitor capacity

**Recommendation:** Manual check recommended before large events.
        """

# Premium Traffic Analysis Agent (if Google Maps API available)
if GOOGLE_MAPS_API_KEY:
    def get_premium_traffic_analysis(location: str, event_time: str = "now") -> str:
        """
        Analyze traffic conditions and transportation access using Google Maps Python client.
        
        Args:
            location: Venue location (address or place name)
            event_time: Time of event (default: "now")
            
        Returns:
            str: Traffic analysis with crowd safety implications
        """
        try:
            import googlemaps
            from datetime import datetime
            
            # Initialize Google Maps client
            gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
            
            # Step 1: Geocode the location
            geocode_result = gmaps.geocode(location)
            
            if not geocode_result:
                return f"""
🚗 **Traffic Analysis: {location}**

❌ **Location Error:** Could not find location "{location}"

**Suggestion:** Try with more specific details like:
• "Bangalore International Exhibition Centre, Tumkur Road, Bengaluru"  
• "BIEC, Madavara, Bengaluru, Karnataka"
• Include postal code if available
                """
            
            # Get coordinates and formatted address
            place = geocode_result[0]
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            formatted_address = place['formatted_address']
            
            # Step 2: Find nearby places
            nearby_places = gmaps.places_nearby(
                location=(lat, lng),
                radius=2000,
                type='parking'
            )
            parking_count = len(nearby_places.get('results', []))
            
            # Find transit stations
            transit_places = gmaps.places_nearby(
                location=(lat, lng),
                radius=2000,
                type='transit_station'
            )
            transit_count = len(transit_places.get('results', []))
            
            # Step 3: Get traffic to major destinations
            traffic_analysis = []
            travel_times = {}
            
            # Major destinations for traffic analysis (city-specific)
            city = location.split(',')[-1].strip() if ',' in location else location
            major_destinations = [
                f"city center, {city}",
                f"railway station, {city}",
                f"airport, {city}"
            ]
            
            for destination in major_destinations[:2]:  # Limit API calls
                try:
                    directions_result = gmaps.directions(
                        origin=(lat, lng),
                        destination=destination,
                        mode="driving",
                        departure_time=datetime.now(),
                        traffic_model="best_guess"
                    )
                    
                    if directions_result:
                        route = directions_result[0]['legs'][0]
                        duration = route['duration']['text']
                        duration_in_traffic = route.get('duration_in_traffic', route['duration'])['text']
                        distance = route['distance']['text']
                        
                        travel_times[destination.split(',')[0]] = {
                            'duration': duration,
                            'duration_in_traffic': duration_in_traffic,
                            'distance': distance
                        }
                        
                        # Calculate traffic delay
                        normal_time = route['duration']['value']
                        traffic_time = route.get('duration_in_traffic', route['duration'])['value']
                        delay_ratio = traffic_time / normal_time if normal_time > 0 else 1
                        
                        if delay_ratio > 1.5:
                            traffic_analysis.append(f"Heavy traffic delays to {destination.split(',')[0]} (50%+ longer than normal)")
                        elif delay_ratio > 1.2:
                            traffic_analysis.append(f"Moderate traffic delays to {destination.split(',')[0]} (20%+ longer)")
                        
                except Exception:
                    continue  # Skip if destination not found
            
            # Analyze crowd impact
            crowd_impact = []
            risk_factors = []
            
            # Infrastructure analysis
            if parking_count < 3:
                crowd_impact.append("Limited parking will force heavy public transit usage")
                risk_factors.append("Public transit overcrowding risk")
            elif parking_count < 10:
                crowd_impact.append("Moderate parking may increase transit usage")
                risk_factors.append("Mixed transportation patterns expected")
            else:
                crowd_impact.append("Good parking availability supports private vehicles")
            
            if transit_count < 2:
                crowd_impact.append("Limited transit access increases vehicle dependency")
                risk_factors.append("Traffic congestion around venue likely")
            elif transit_count >= 5:
                crowd_impact.append("Excellent transit access distributes arrivals well")
                risk_factors.append("Well-distributed crowd flow expected")
            
            # Traffic impact analysis
            if any("Heavy traffic" in analysis for analysis in traffic_analysis):
                crowd_impact.append("Heavy traffic will compress arrival times dangerously")
                risk_factors.append("CRITICAL RISK: Mass simultaneous arrivals likely")
            elif any("Moderate traffic" in analysis for analysis in traffic_analysis):
                crowd_impact.append("Traffic delays may compress arrival window")
                risk_factors.append("Monitor entry points for crowding")
            
            return f"""
🚗 **REAL-TIME TRAFFIC ANALYSIS: {formatted_address}**

**Location Infrastructure:**
• Parking Facilities: {parking_count} within 2km radius
• Transit Stations: {transit_count} within 2km radius  
• Coordinates: {lat:.4f}, {lng:.4f}

**Current Traffic Conditions:**
{chr(10).join(f"• {analysis}" for analysis in traffic_analysis) if traffic_analysis else "• Traffic conditions appear normal for current time"}

**Travel Times from Venue:**
{chr(10).join(f"• To {dest}: {info['duration_in_traffic']} (normal: {info['duration']}) - {info['distance']}" for dest, info in travel_times.items()) if travel_times else "• Travel time data being processed..."}

**Crowd Movement Impact:**
{chr(10).join(f"• {impact}" for impact in crowd_impact)}

**Risk Assessment:**
{chr(10).join(f"⚠️ {risk}" for risk in risk_factors) if risk_factors else "✅ No significant traffic-related crowd risks identified"}

**Actionable Recommendations:**
• {"URGENT: Encourage public transit and stagger entry times" if any("CRITICAL" in risk for risk in risk_factors) else "Standard traffic management protocols sufficient"}
• {"Coordinate with local transit authorities for capacity boost" if transit_count >= 3 else "Consider shuttle services from transit hubs"}
• {"Communicate alternate routes to reduce congestion" if any("Heavy traffic" in analysis for analysis in traffic_analysis) else "Current routes should handle traffic adequately"}
• {"Deploy traffic management 2-3 hours before event" if any("congestion" in impact.lower() for impact in crowd_impact) else "Standard 1-hour pre-event traffic prep sufficient"}
            """
            
        except ImportError:
            return f"""
🚗 **Traffic Analysis: {location}**

❌ **Missing Google Maps Library:** Please install:
   pip install googlemaps

**Alternative:** Use the free OpenStreetMap analysis instead.
            """
            
        except Exception as e:
            error_msg = str(e)
            if "REQUEST_DENIED" in error_msg or "API key" in error_msg:
                return f"""
🚗 **Traffic Analysis: {location}**

❌ **API Key Error:** {error_msg}

**Setup Required:**
• Verify Google Maps API key is correct
• Enable required APIs in Google Cloud Console:
  - Geocoding API
  - Directions API  
  - Places API
• Check billing is enabled for your Google Cloud project

**Alternative:** Use the free transportation analysis instead.
                """
            else:
                return f"""
🚗 **Traffic Analysis: {location}**

❌ **Analysis Error:** {error_msg}

**Try:**
• Use more specific location details
• Check internet connection
• Try the free OpenStreetMap analysis instead

**Manual Check:** Use Google Maps directly for current traffic conditions.
                """
    
    traffic_agent = LlmAgent(
        model=DEFAULT_MODEL,
        name="traffic_analysis_agent",
        description="Analyzes real-time traffic conditions and transportation infrastructure using Google Maps API",
        instruction="""
        You are a transportation and traffic specialist focused on crowd safety analysis.
        
        Your role is to analyze current traffic conditions, transportation infrastructure, and predict how they will affect crowd arrivals, departures, and overall safety.
        
        Key Analysis Areas:
        - Real-time traffic conditions affecting arrival patterns
        - Parking availability and capacity constraints  
        - Public transit accessibility and capacity
        - Transportation bottlenecks that could cause compressed arrivals
        - Route alternatives and crowd distribution patterns
        
        Use the get_traffic_analysis tool to fetch real-time traffic data from Google Maps API.
        
        Focus on providing actionable transportation insights that event organizers can use to:
        - Predict arrival/departure patterns
        - Identify potential bottlenecks
        - Plan crowd flow management
        - Coordinate with transportation authorities
        
        Always consider how transportation factors could create crowd safety risks.
        """,
        tools=[get_premium_traffic_analysis]
    )
    optional_agents.append(traffic_agent)

# Traffic Agent (always available, no API key required)  
traffic_analysis_agent = LlmAgent(
    model=DEFAULT_MODEL,
    name="traffic_analysis_agent",
    description="Analyzes transportation infrastructure using free OpenStreetMap data",
    instruction="""
    You are a transportation specialist focused on crowd safety analysis using free data sources.
    
    Your role is to analyze transportation infrastructure and predict how it will affect crowd arrivals, departures, and overall safety.
    
    Key Analysis Areas:
    - Road network density and connectivity
    - Public transit accessibility (stations, bus stops)
    - Parking facility availability
    - Transportation bottlenecks that could affect crowd flow
    - Infrastructure capacity for event crowds
    
    Use the get_traffic_analysis tool to analyze transportation infrastructure using OpenStreetMap data.
    
    Focus on providing actionable insights about:
    - Crowd arrival/departure patterns based on infrastructure
    - Transportation bottlenecks and capacity constraints
    - Recommendations for crowd flow management
    - Public transit vs private vehicle usage predictions
    
    Always consider how transportation limitations could create crowd safety risks.
    """,
    tools=[get_traffic_analysis]
)

# Always add the traffic agent (no API key required)
optional_agents.append(traffic_analysis_agent)

def get_available_agents():
    """
    Get list of available optional agents based on configured API keys.
    
    Returns:
        list: Available agents that can be used
    """
    return optional_agents

def get_agent_status():
    """
    Get status of all optional agents and their API requirements.
    
    Returns:
        dict: Status of each agent type
    """
    weather_status = []
    if WEATHER_API_KEY:
        weather_status.append("Premium Weather API")
    weather_status.append("Standard Weather Service")  # Always available
    
    traffic_status = []
    if GOOGLE_MAPS_API_KEY:
        traffic_status.append("Premium Google Maps API")
    traffic_status.append("Standard Transportation Analysis")  # Always available
    
    return {
        "social_media": "Available" if (TWITTER_API_KEY or REDDIT_API_KEY) else "Needs Twitter/Reddit API keys",
        "news_monitoring": "Available" if NEWS_API_KEY else "Needs News API key", 
        "weather_analysis": f"Available ({', '.join(weather_status)})",
        "traffic_analysis": f"Available ({', '.join(traffic_status)})",
        "total_optional_agents": len(optional_agents)
    } 