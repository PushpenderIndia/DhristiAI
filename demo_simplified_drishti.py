#!/usr/bin/env python3
"""
DrishtiAI Simplified System Demo
===============================

This demo shows the simplified DrishtiAI stampede prediction system with:
- One main Gemini agent for core analysis
- Wikipedia agent for historical research
- Optional agents that load only if API keys are provided
"""

from datetime import datetime
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_banner():
    """Print the demo banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════╗
║                    DrishtiAI Simplified Demo                        ║
║                 Stampede Prediction System v2.0                     ║
╠══════════════════════════════════════════════════════════════════════╣
║  🧠 Main Agent: Gemini-powered stampede risk analysis               ║
║  🏛️ Wikipedia Agent: Historical incident research                   ║
║  📱 Optional Agents: Load only with API keys                        ║
╚══════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def demo_system_status():
    """Demo the system status check"""
    print("\n🔍 SYSTEM STATUS CHECK")
    print("=" * 50)
    
    try:
        from drishti_agents import get_system_status
        status = get_system_status()
        
        print(f"✅ Main Agent: {status['main_agent']}")
        print(f"✅ Wikipedia Agent: {status['wikipedia_agent']}")
        print(f"📦 Version: {status['version']}")
        
        print(f"\n📱 Optional Agents Status:")
        optional_status = status['optional_agents']
        if isinstance(optional_status, dict) and 'total_optional_agents' in optional_status:
            print(f"   Total Available: {optional_status['total_optional_agents']}")
            
            for agent_type, status_msg in optional_status.items():
                if agent_type != 'total_optional_agents':
                    emoji = "✅" if "Available" in status_msg else "❌"
                    print(f"   {emoji} {agent_type.replace('_', ' ').title()}: {status_msg}")
        else:
            print(f"   ❌ {optional_status}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking system status: {e}")
        return False

def demo_core_capabilities():
    """Demo the core system capabilities"""
    print("\n🎯 CORE CAPABILITIES")
    print("=" * 50)
    
    print("1. 🧠 Main Gemini Agent:")
    print("   • Comprehensive stampede risk analysis")
    print("   • Multi-factor safety assessment")
    print("   • Actionable safety recommendations")
    print("   • Emergency protocol generation")
    
    print("\n2. 🏛️ Wikipedia Historical Agent:")
    print("   • Historical stampede incident research")
    print("   • Venue safety history lookup")
    print("   • Pattern analysis from past disasters")
    print("   • Lessons learned extraction")
    
    print("\n3. 📱 Optional Enhancement Agents:")
    print("   • Social Media: Buzz and viral content monitoring")
    print("   • News Coverage: Media attention analysis")
    print("   • Weather Impact: Crowd behavior prediction")
    print("   • Traffic Analysis: Transportation bottleneck detection")

def demo_example_analysis():
    """Demo example analysis scenarios"""
    print("\n📊 EXAMPLE ANALYSIS SCENARIOS")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "Concert Venue",
            "query": "Analyze stampede risk for Madison Square Garden concert tonight, 20,000 attendees, Taylor Swift performance",
            "focus": "Celebrity crowds, social buzz, venue capacity"
        },
        {
            "name": "Sports Event", 
            "query": "Evaluate crowd safety for Super Bowl at MetLife Stadium, 82,000 capacity",
            "focus": "Large crowds, traffic, weather impact"
        },
        {
            "name": "Religious Gathering",
            "query": "Assess risk for Hajj pilgrimage gathering, 2 million attendees",
            "focus": "Historical incidents, crowd density, movement patterns"
        },
        {
            "name": "Festival",
            "query": "Check safety for Coachella music festival, 125,000 daily attendance",
            "focus": "Multi-day event, weather, social media excitement"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. 🎪 {scenario['name']}")
        print(f"   Query: \"{scenario['query']}\"")
        print(f"   Focus Areas: {scenario['focus']}")

def demo_adk_integration():
    """Demo ADK integration instructions"""
    print("\n🚀 ADK WEB INTERFACE INTEGRATION")
    print("=" * 50)
    
    print("1. 📁 Start the ADK web server:")
    print("   Command: adk web")
    print("   (Run from the project root directory)")
    
    print("\n2. 🌐 Access the web interface:")
    print("   URL: http://localhost:8000")
    
    print("\n3. 🎯 Select your agent:")
    print("   Agent: 'drishti_stampede_predictor'")
    
    print("\n4. 💬 Example queries to try:")
    example_queries = [
        "Analyze stampede risk for a small venue concert with 500 people",
        "What historical stampede incidents happened at large stadiums?",
        "Evaluate safety for an outdoor festival in rainy weather",
        "Quick risk check for a sold-out arena show tonight"
    ]
    
    for i, query in enumerate(example_queries, 1):
        print(f"   {i}. \"{query}\"")

def demo_configuration_guide():
    """Demo configuration setup"""
    print("\n⚙️ CONFIGURATION GUIDE")
    print("=" * 50)
    
    print("Required Setup:")
    print("1. 🔑 Create .env file:")
    print("   cp env.sample .env")
    
    print("\n2. 🎯 Add your Google API key:")
    print("   GOOGLE_API_KEY=your_actual_api_key_here")
    
    print("\n3. 📦 Install dependencies:")
    print("   pip install -r requirements.txt")
    
    print("\nOptional API Keys (for enhanced features):")
    optional_apis = [
        ("TWITTER_API_KEY", "Social media buzz monitoring"),
        ("REDDIT_API_KEY", "Community discussion analysis"),
        ("NEWS_API_KEY", "News coverage monitoring"),
        ("WEATHER_API_KEY", "Weather impact analysis"),
        ("GOOGLE_MAPS_API_KEY", "Traffic and transportation analysis")
    ]
    
    for api_key, description in optional_apis:
        print(f"   • {api_key}: {description}")

def main():
    """Main demo function"""
    print_banner()
    
    print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check system status
    system_working = demo_system_status()
    
    # Show capabilities
    demo_core_capabilities()
    
    # Show example scenarios
    demo_example_analysis()
    
    # Show ADK integration
    demo_adk_integration()
    
    # Show configuration
    demo_configuration_guide()
    
    print("\n" + "=" * 70)
    if system_working:
        print("🎯 READY TO USE: DrishtiAI Simplified System")
        print("\n🚀 Quick Start:")
        print("1. Ensure your .env file has GOOGLE_API_KEY set")
        print("2. Run: adk web")
        print("3. Open: http://localhost:8000")
        print("4. Select: 'drishti_stampede_predictor'")
        print("5. Ask: 'Analyze stampede risk for [your venue/event]'")
    else:
        print("⚠️ SETUP NEEDED: Please configure your environment")
        print("\n🔧 Next Steps:")
        print("1. Copy env.sample to .env")
        print("2. Add your Google API key")
        print("3. Run: pip install -r requirements.txt")
        print("4. Restart this demo")
    
    print("\n💡 This simplified system focuses on core functionality!")
    print("🚨 Remember: Always verify AI analysis with local authorities.")
    print(f"\n📊 System Version: v2.0 - Simplified & Optimized")

if __name__ == "__main__":
    main() 