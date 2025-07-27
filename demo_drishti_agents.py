#!/usr/bin/env python3
"""
DrishtiAI Multi-Agent System Demo
=================================

Demo script showcasing the DrishtiAI multi-agent system for
stampede prediction and crowd safety analysis.

Usage:
    python demo_drishti_agents.py

Requirements:
    - Google API key set in .env file
    - All required dependencies installed
"""

import os
import sys
from datetime import datetime

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from drishti_agents import create_system, analyze_stampede_risk, get_status
    from drishti_agents.config import validate_config
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("Please ensure you're running from the project root directory and all dependencies are installed.")
    sys.exit(1)


def print_banner():
    """Print the DrishtiAI banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                    🚨 DRISHTI AI SYSTEM 🚨                       ║
    ║                Multi-Agent Stampede Prediction                   ║
    ║                                                                  ║
    ║  🏛️ Historical Analysis  📱 Social Buzz   🚗 Traffic Patterns   ║
    ║  🚪 Entry Gate Monitor   🌤️ Weather Impact 📡 Event Intelligence ║
    ╚══════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def demo_system_status():
    """Demo the system status functionality"""
    print("\n🔍 SYSTEM STATUS CHECK")
    print("=" * 50)
    
    try:
        status = get_status()
        print(f"✅ System: {status['system_name']}")
        print(f"📊 Version: {status['version']}")
        print(f"🤖 Agents: {len(status['agents'])} specialized agents")
        print(f"⚙️ Configuration: {status['config_status']}")
        
        print("\n🎯 ACTIVE AGENTS:")
        for agent_name, description in status['agents'].items():
            print(f"  • {agent_name}: {description}")
        
        print(f"\n🏟️ SUPPORTED VENUES ({len(status['supported_venues'])}):")
        for venue in status['supported_venues']:
            print(f"  • {venue}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error checking system status: {e}")
        return False


def demo_configuration_check():
    """Demo the configuration validation"""
    print("\n🔧 CONFIGURATION VALIDATION")
    print("=" * 50)
    
    try:
        validate_config()
        print("✅ Configuration is valid - all required API keys are present")
        return True
    except ValueError as e:
        print(f"⚠️ Configuration Issue: {e}")
        print("\n📝 To fix this:")
        print("1. Copy env.sample to .env")
        print("2. Add your Google API key to the .env file")
        print("3. Optionally add other API keys for enhanced functionality")
        return False


def demo_analysis_scenarios():
    """Demo various analysis scenarios"""
    print("\n📊 ANALYSIS SCENARIOS")
    print("=" * 50)
    
    scenarios = [
        {
            "name": "🏟️ Major Stadium Event",
            "location": "MetLife Stadium",
            "event_name": "Super Bowl Final",
            "event_type": "sports",
            "expected_attendance": 82500
        },
        {
            "name": "🎵 Concert Arena",
            "location": "Madison Square Garden",
            "event_name": "World Tour Concert",
            "event_type": "concert",
            "expected_attendance": 20000
        },
        {
            "name": "🙏 Religious Festival",
            "location": "Kumbh Mela Grounds",
            "event_name": "Kumbh Mela Festival",
            "event_type": "religious",
            "expected_attendance": 1000000
        },
        {
            "name": "🎉 Public Celebration",
            "location": "Times Square",
            "event_name": "New Year's Eve Celebration",
            "event_type": "celebration",
            "expected_attendance": 50000
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print(f"   📍 {scenario['location']}")
        print(f"   🎪 {scenario['event_name']}")
        print(f"   👥 {scenario['expected_attendance']:,} expected attendees")
        
        try:
            analysis_setup = analyze_stampede_risk(
                location=scenario['location'],
                event_name=scenario['event_name'],
                event_type=scenario['event_type'],
                expected_attendance=scenario['expected_attendance']
            )
            
            if analysis_setup.get('status') == 'ready_for_analysis':
                print("   ✅ Analysis ready - would coordinate all agents")
                print("   📋 Multi-agent risk assessment prepared")
            else:
                print("   ❌ Analysis setup failed")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")


def demo_adk_integration():
    """Demo ADK integration instructions"""
    print("\n🔌 ADK INTEGRATION GUIDE")
    print("=" * 50)
    
    integration_code = '''
# To use DrishtiAI with Google ADK:

# 1. Create the main agent system
from drishti_agents import create_system
drishti_agent = create_system()

# 2. Run using ADK CLI
# adk run drishti_agents/

# 3. Use ADK Web UI for interactive testing  
# adk web drishti_agents/

# 4. Example query for the system:
query = """
Analyze stampede risk for Madison Square Garden concert with 20,000 expected attendees.
Event: Pop Concert by Major Artist
Please provide comprehensive risk assessment and recommendations.
"""

# The system will automatically coordinate all specialized agents
# and provide a complete multi-factor risk analysis.
'''
    
    print(integration_code)


def demo_agent_capabilities():
    """Demo individual agent capabilities"""
    print("\n🤖 AGENT CAPABILITIES OVERVIEW")
    print("=" * 50)
    
    agents = {
        "🏛️ Historical Analysis Agent": [
            "• Analyzes past stampede incidents at venue",
            "• Evaluates event type risk factors",
            "• Reviews venue safety history",
            "• Provides lessons learned from similar events"
        ],
        "📱 Social Buzz Agent": [
            "• Monitors social media sentiment",
            "• Detects viral content and trending topics",
            "• Tracks celebrity mentions and appearances",
            "• Estimates crowd size from online engagement"
        ],
        "🚗 Traffic Analysis Agent": [
            "• Tracks celebrity car movements",
            "• Analyzes traffic congestion patterns",
            "• Monitors VIP arrival points",
            "• Assesses transportation bottlenecks"
        ],
        "🚪 Entry Gate Agent": [
            "• Calculates gate processing capacity",
            "• Identifies bottleneck gates",
            "• Monitors queue formation patterns",
            "• Analyzes crowd flow dynamics"
        ],
        "🌤️ Weather Agent": [
            "• Assesses weather impact on crowds",
            "• Predicts shelter-seeking behavior",
            "• Monitors severe weather alerts",
            "• Analyzes temperature and precipitation effects"
        ],
        "📡 Event Intelligence Agent": [
            "• Gathers real-time event data",
            "• Monitors crowd sentiment changes",
            "• Tracks security incidents",
            "• Assesses emerging risk factors"
        ]
    }
    
    for agent_name, capabilities in agents.items():
        print(f"\n{agent_name}:")
        for capability in capabilities:
            print(f"  {capability}")


def main():
    """Main demo function"""
    print_banner()
    
    print(f"⏰ Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check system status
    if not demo_system_status():
        return
    
    # Validate configuration
    config_valid = demo_configuration_check()
    
    # Show agent capabilities
    demo_agent_capabilities()
    
    # Demo analysis scenarios
    demo_analysis_scenarios()
    
    # Show ADK integration
    demo_adk_integration()
    
    print("\n" + "=" * 70)
    if config_valid:
        print("🎯 READY TO USE: Your DrishtiAI system is configured and ready!")
        print("\n🚀 Next Steps:")
        print("1. Run: adk web drishti_agents/")
        print("2. Open the web interface in your browser")
        print("3. Ask: 'Analyze stampede risk for [your venue] with [event details]'")
        print("4. The system will coordinate all agents for comprehensive analysis")
    else:
        print("⚠️ CONFIGURATION NEEDED: Please set up your API keys first")
        print("\n🔧 Setup Steps:")
        print("1. Copy env.sample to .env") 
        print("2. Add your Google API key to GOOGLE_API_KEY in .env")
        print("3. Restart the demo to verify configuration")
    
    print("\n💡 This system can help prevent stampede incidents and save lives!")
    print("🚨 Remember: Always verify AI analysis with local authorities and on-ground observations.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your setup and try again.") 