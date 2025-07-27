# 🚨 DrishtiAI Multi-Agent Stampede Prediction System

**Predicting and preventing stampede incidents through advanced AI multi-agent coordination**

![DrishtiAI System](https://img.shields.io/badge/DrishtiAI-v1.0.0-blue) ![Agents](https://img.shields.io/badge/Agents-6_Specialized-green) ![Status](https://img.shields.io/badge/Status-Production_Ready-brightgreen)

## 🎯 Overview

DrishtiAI is an advanced multi-agent system built with Google's Agent Development Kit (ADK) that predicts stampede probability and crowd surges **before they occur**. By analyzing multiple risk factors simultaneously, it provides early warnings to prevent dangerous crowd incidents and save lives.

### 🚀 Key Features

- **🏛️ Historical Analysis**: Learns from past stampede incidents and venue history
- **📱 Social Media Monitoring**: Tracks viral content and internet buzz that drives crowds  
- **🚗 Celebrity Movement Tracking**: Monitors VIP arrivals that attract fan crowds
- **🚪 Entry Gate Analysis**: Analyzes congestion patterns and bottlenecks
- **🌤️ Weather Impact Assessment**: Predicts weather effects on crowd behavior
- **📡 Real-time Intelligence**: Gathers live event data and emerging risks

## 🤖 Multi-Agent Architecture

The system consists of 6 specialized AI agents coordinated by a main orchestrator:

```
DrishtiAI Main Orchestrator
├── 🏛️ Historical Analysis Agent
├── 📱 Social Buzz Monitoring Agent  
├── 🚗 Traffic & Celebrity Movement Agent
├── 🚪 Entry Gate Congestion Agent
├── 🌤️ Weather Impact Agent
└── 📡 Event Intelligence Agent
```

Each agent specializes in a specific risk factor while the orchestrator combines all analyses into a unified risk assessment.

## ⚡ Quick Start

### Prerequisites

- Python 3.9+
- Google API Key (for Gemini models)
- Google ADK installed (`pip install google-adk`)

### Installation

1. **Clone and setup**:
   ```bash
   cd DhristiAI
   pip install -r requirements.txt
   ```

2. **Configure API keys**:
   ```bash
   cp env.sample .env
   # Edit .env and add your Google API key
   ```

3. **Test the system**:
   ```bash
   python demo_drishti_agents.py
   ```

### Using with ADK Web Interface

1. **Start the ADK web interface**:
   ```bash
   adk web drishti_agents/
   ```

2. **Open in browser** (usually http://localhost:8000)

3. **Select the DrishtiAI agent** and start analyzing!

## 💡 Usage Examples

### Command Line Analysis

```python
from drishti_agents import analyze_stampede_risk

# Analyze a major sporting event
result = analyze_stampede_risk(
    location="MetLife Stadium",
    event_name="Super Bowl Final", 
    event_type="sports",
    expected_attendance=82500
)
```

### ADK Web Interface Queries

Try these example queries in the ADK web interface:

```
🏟️ Sports Event:
"Analyze stampede risk for Wembley Stadium football final with 90,000 attendees"

🎵 Concert:
"Assess crowd safety for Madison Square Garden concert, expecting 20,000 fans with major celebrity performer"

🙏 Religious Event:  
"Evaluate stampede probability for temple festival with 100,000 expected pilgrims"

🎉 Public Event:
"Check crowd surge risk for Times Square New Year's celebration"
```

## 📊 Risk Assessment Output

The system provides comprehensive risk analysis including:

### Risk Scoring
- **Overall Risk Score**: 0.0 to 1.0 scale
- **Risk Level**: MINIMAL/LOW/MEDIUM/HIGH/CRITICAL  
- **Confidence Level**: Based on data quality and analysis depth

### Detailed Analysis
- **Risk Factor Breakdown**: Individual scores from each agent
- **Specific Recommendations**: Actionable safety measures
- **Immediate Actions**: Time-sensitive interventions if needed
- **Historical Context**: Lessons from similar past events

### Example Output

```
🚨 DRISHTI AI STAMPEDE PREDICTION REPORT 🚨
=============================================

📍 LOCATION: Madison Square Garden
⏰ ANALYSIS TIME: 2025-01-15 14:30:00

🎯 OVERALL RISK ASSESSMENT
========================
Risk Score: 0.72 / 1.0
Risk Level: HIGH
Alert Status: HIGH ALERT

📊 DETAILED RISK FACTORS
========================
🏛️  Historical Events: 0.600
📱 Social Media Buzz: 0.850  
🚗 Traffic Patterns: 0.700
🚪 Entry Gate Congestion: 0.800
🌤️  Weather Impact: 0.200
📡 Event Intelligence: 0.750

💡 RECOMMENDATIONS
==================
1. Deploy additional security personnel immediately
2. Implement crowd control barriers at key entry/exit points
3. Monitor social media for real-time sentiment changes
4. Prepare for celebrity arrival crowds at VIP entrances
```

## 🔧 Configuration

### Required Environment Variables

```bash
# Google AI Configuration (Required)
GOOGLE_API_KEY=your_google_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=false
GOOGLE_CLOUD_PROJECT=your_project_id

# Optional APIs for Enhanced Analysis
TWITTER_API_KEY=your_twitter_api_key
NEWS_API_KEY=your_news_api_key  
WEATHER_API_KEY=your_weather_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

### Risk Thresholds (Customizable)

```python
RISK_THRESHOLDS = {
    "LOW": 0.3,      # Minimal concern
    "MEDIUM": 0.6,   # Increased vigilance  
    "HIGH": 0.8,     # High alert
    "CRITICAL": 0.9  # Emergency response
}
```

## 🏗️ Architecture Details

### Agent Coordination

The system uses Google ADK's multi-agent coordination with:

- **Hierarchical Structure**: Main orchestrator manages specialized sub-agents
- **Tool Integration**: Each agent has specialized analysis tools
- **Event-driven Communication**: Agents share findings through structured events
- **Weighted Risk Calculation**: Combines multiple risk factors with configurable weights

### Supported Venue Types

- **🏟️ Sports Venues**: Stadiums, arenas, sports complexes
- **🎵 Entertainment**: Concert halls, theaters, music venues
- **🙏 Religious Sites**: Temples, churches, pilgrimage sites  
- **🎉 Public Events**: Festivals, parades, celebrations
- **🏢 Commercial**: Shopping centers, convention centers
- **🚊 Transportation**: Airports, train stations, transit hubs

## 📈 Performance & Accuracy

### System Capabilities

- **Real-time Analysis**: Sub-second risk assessment updates
- **Scalable Architecture**: Handles events from 1,000 to 1,000,000+ attendees
- **Multi-factor Correlation**: Combines 6+ risk dimensions
- **Historical Learning**: Improves predictions based on past incident data

### Validation

- **Historical Incident Analysis**: Tested against known stampede events
- **Cross-validation**: Multiple agent consensus improves accuracy  
- **Continuous Learning**: System improves with more data and feedback
- **Expert Review**: Recommendations align with crowd safety best practices

## 🛡️ Safety & Ethics

### Safety First Principles

- **Human Life Priority**: All recommendations prioritize saving lives
- **Conservative Estimates**: Better to over-prepare than under-prepare
- **Expert Verification**: Always verify AI analysis with local authorities
- **Transparent Reasoning**: Clear explanation of risk factors and recommendations

### Ethical Considerations

- **Privacy Protection**: No personal data collection or storage
- **Bias Mitigation**: Diverse training data and multiple validation sources
- **Responsible Deployment**: Designed for safety enhancement, not replacement of human judgment

### Areas for Contribution

- **New Risk Factors**: Additional analysis dimensions
- **Historical Data**: More incident case studies and patterns
- **Integration APIs**: Additional data sources and monitoring tools
- **Venue Types**: Support for new venue categories
- **Localization**: Support for different regions and cultures

## 📞 Support & Contact

### Getting Help

- **Documentation**: Check this README and code comments
- **Demo Script**: Run `python demo_drishti_agents.py` for guided tour
- **Issues**: Open GitHub issues for bugs or feature requests

### Emergency Use

⚠️ **IMPORTANT**: This system is designed to **assist** crowd safety professionals, not replace human judgment. In emergency situations:

1. **Always verify AI analysis** with on-ground observations
2. **Coordinate with local authorities** and emergency services  
3. **Use as early warning tool** combined with standard safety protocols
4. **Document incidents** to help improve the system

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

## 🙏 Acknowledgments

- **Google ADK Team**: For the powerful multi-agent development framework
- **Crowd Safety Experts**: For validation and real-world insights  
- **Historical Incident Research**: Learning from past tragedies to prevent future ones
- **Open Source Community**: For tools and libraries that make this possible

---

**💡 Remember: Technology should serve humanity. This system exists to prevent stampede tragedies and protect human lives.**

*Built with ❤️ by the DrishtiAI Team* 