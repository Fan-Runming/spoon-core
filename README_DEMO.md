# U NO HOO - AI-Powered Relationship Management

## 🎯 Project Overview

**U NO HOO** is an intelligent relationship management system that helps users maintain and deepen their personal and professional connections through conversational AI.

### Key Features
- 💬 **Conversational Interface**: Talk to an AI agent about the people in your life
- 🏷️ **Smart Tagging**: Automatically extracts personality, interests, career info, and goals
- 🎯 **Actionable Suggestions**: Get personalized next-step recommendations for each relationship
- 📸 **Photo Integration**: Upload and associate photos with contacts
- 🎤 **Voice Input**: Support for voice-based interaction
- 🔍 **Semantic Search**: Find people by skills, interests, or background

### Tech Stack
- **Backend**: FastAPI (Python)
- **AI**: Google Gemini 2.5 Flash
- **Frontend**: Vanilla JavaScript with Glassmorphism UI
- **Integrations**: Apify LinkedIn Profile Scraper

## 🚀 Live Demo

[Demo Link will be here after deployment]

## 📦 Installation

### Prerequisites
- Python 3.11+
- Gemini API Key

### Setup
```bash
# Clone repository
git clone https://github.com/Fan-Runming/spoon-core.git
cd spoon-core

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Run the application
uvicorn main:app --host 0.0.0.0 --port 8000
```

Visit http://localhost:8000

## 🎨 Features Showcase

### 1. Conversational Person Recording
Simply chat with the AI about someone you know, and it will automatically:
- Extract their name and contact info
- Identify personality traits and interests
- Suggest how to maintain the relationship

### 2. Smart Tagging System
People are categorized with:
- **Personality tags**: Creative, analytical, outgoing, etc.
- **Career tags**: Software engineer, designer, researcher, etc.
- **Interest tags**: Photography, hiking, cooking, etc.
- **Goal tags**: Networking, collaboration, mentorship, etc.

### 3. LinkedIn Integration
Enrich contact information automatically by providing a LinkedIn profile URL.

## 📖 How It Works

1. **Select a scenario** (stay in touch, first meeting, long time no see, etc.)
2. **Describe the person** in natural language
3. **AI extracts key information** and generates a person card
4. **Get suggestions** for maintaining or deepening the relationship
5. **View recent contacts** in the sidebar (up to 5 most recent)

## 🔐 Environment Variables

Required:
- `GEMINI_API_KEY`: Your Google Gemini API key

Optional:
- `APIFY_API_TOKEN`: For LinkedIn profile scraping
- `OPENAI_API_KEY`: Alternative LLM provider
- `ANTHROPIC_API_KEY`: Alternative LLM provider

## 📝 Project Structure

```
spoon-core/
├── main.py                          # FastAPI backend
├── relationship_spark_agent.py      # AI agent logic
├── static/
│   ├── index.html                   # Main UI
│   └── mobile.html                  # Mobile preview
├── spoon_ai/                        # Core AI modules
│   ├── agents/                      # Agent implementations
│   ├── tools/                       # Tool integrations
│   └── llm/                         # LLM providers
└── requirements.txt                 # Python dependencies
```

## 🎯 Use Cases

- **Networking**: Keep track of professional contacts and their expertise
- **Personal Relationships**: Remember important details about friends and family
- **Team Building**: Understand team members' skills and interests
- **Community Management**: Maintain connections in communities or organizations

## 🚧 Future Enhancements

- [ ] Persistent database (currently in-memory)
- [ ] Calendar integration for follow-up reminders
- [ ] Email/message draft generation
- [ ] Batch LinkedIn import
- [ ] Relationship analytics dashboard
- [ ] Mobile app

## 📄 License

[Add your license here]

## 👥 Team

[Add team member information]

## 🙏 Acknowledgments

Built with SpoonAI framework
Powered by Google Gemini API
UI inspired by modern glassmorphism design trends
