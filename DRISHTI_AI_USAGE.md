# 🚨 DrishtiAI Multi-Agent System - Quick Usage Guide

## 🎯 What is DrishtiAI?

DrishtiAI is a multi-agent system that predicts stampede probability by analyzing:
- **🏛️ Past events** at the venue
- **📱 Internet buzz** and social media sentiment  
- **🚗 Celebrity car movements** and VIP arrivals
- **🚪 Entry gate congestion** patterns
- **🌤️ Weather impact** on crowd behavior
- **📡 Real-time event intelligence**

## ⚡ Quick Setup

1. **Get Google API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

2. **Configure Environment**:
   ```bash
   cp env.sample .env
   # Edit .env and add: GOOGLE_API_KEY=your_api_key_here
   ```

3. **Test Installation**:
   ```bash
   python demo_drishti_agents.py
   ```

## 🚀 Using with ADK Web Dashboard

### Start the System
```bash
adk web drishti_agents/
```

### Example Queries

**🏟️ Sports Stadium**:
```
Analyze stampede risk for Wembley Stadium football final with 90,000 attendees. 
The match is England vs Brazil and there's been massive social media buzz.
```

**🎵 Concert Venue**:
```
Assess crowd safety for Madison Square Garden concert tonight. 
Expecting 20,000 fans for Taylor Swift concert. There are rumors of surprise guests.
```

**🙏 Religious Festival**:
```
Evaluate stampede probability for Kumbh Mela with 1 million expected pilgrims. 
Weather forecast shows possible rain in the afternoon.
```

**🎉 Public Celebration**:
```
Check crowd surge risk for Times Square New Year's Eve celebration.
Expected 50,000 people, celebrity performances announced.
```

## 📊 Understanding the Output

The system provides:

### Risk Score (0.0 - 1.0)
- **0.0-0.3**: Low risk (normal precautions)
- **0.3-0.6**: Medium risk (increased vigilance)  
- **0.6-0.8**: High risk (enhanced security needed)
- **0.8-1.0**: Critical risk (emergency protocols)

### Individual Agent Scores
- **Historical**: Past incident patterns at venue
- **Social Buzz**: Online sentiment and viral content
- **Traffic**: Celebrity movements and congestion
- **Entry Gates**: Bottlenecks and queue analysis
- **Weather**: Impact on crowd behavior
- **Intelligence**: Real-time event monitoring

### Recommendations
- Specific actions to take based on risk level
- Immediate interventions if critical risk detected
- Preventive measures for ongoing safety

## 🎯 Real-World Usage

### For Event Managers
```
Query: "Stadium capacity 80,000, sold out concert, rain expected"
Use: Plan additional covered areas and crowd flow management
```

### For Security Teams
```
Query: "Celebrity surprise appearance rumored on social media"  
Use: Prepare for crowd surges at VIP entrance areas
```

### For Emergency Services
```
Query: "Religious festival, historical stampede incidents at venue"
Use: Position additional medical teams and evacuation resources
```

## ⚠️ Important Safety Notes

1. **Always verify AI analysis** with on-ground observations
2. **Coordinate with local authorities** and emergency services
3. **Use as early warning tool** - not replacement for human judgment  
4. **Document incidents** to help improve the system
5. **Better to over-prepare** than under-prepare for crowd safety

## 🛠️ Advanced Configuration

### Additional APIs (Optional)
Add these to `.env` for enhanced analysis:
```bash
TWITTER_API_KEY=your_twitter_key
NEWS_API_KEY=your_news_key  
WEATHER_API_KEY=your_weather_key
GOOGLE_MAPS_API_KEY=your_maps_key
```

### Custom Risk Thresholds
Edit `drishti_agents/config.py`:
```python
RISK_THRESHOLDS = {
    "LOW": 0.3,      # Adjust based on your risk tolerance
    "MEDIUM": 0.6,   
    "HIGH": 0.8,     
    "CRITICAL": 0.9  
}
```

## 🆘 Troubleshooting

### "Configuration Error"
- Check your `.env` file has `GOOGLE_API_KEY=your_actual_key`
- Ensure Google API key is valid and has access to Gemini models

### "Import Error"  
- Run `pip install -r requirements.txt`
- Ensure you're in the project root directory

### "Agent not responding"
- Check internet connection (agents use Google Search)
- Verify Google API quota/billing is sufficient

## 📞 Need Help?

- **Demo**: Run `python demo_drishti_agents.py` for guided tour
- **Documentation**: Check `drishti_agents/README.md`
- **Issues**: Report bugs or requests on GitHub

---

**💡 This system can help save lives by predicting dangerous crowd situations before they occur. Use responsibly and always combine with human expertise.** 