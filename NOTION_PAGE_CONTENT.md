# 🌟 U NO HOO - AI-Powered Relationship Manager

> **Tagline**: Remember everyone you meet, nurture every relationship that matters.

---

## 📌 Project Overview

**U NO HOO** is an intelligent relationship management system that helps you build and maintain meaningful connections through natural conversation. Powered by SpoonOS AI Agent Framework and Google's Gemini 2.5 Pro, it transforms casual chats about people in your life into structured, actionable relationship insights.

### 🎯 The Problem We're Solving

In today's fast-paced world:
- We meet countless people but struggle to **remember meaningful details** about them
- Maintaining relationships feels like a chore rather than a **genuine connection**
- Traditional CRM tools are **too mechanical** and sales-focused
- We miss opportunities to **deepen relationships** because we forget context

### 💡 Our Solution

U NO HOO is **NOT** a sales CRM. Instead, it's your personal relationship companion that:
- Extracts person details through **natural conversation** (no forms!)
- Automatically tags personalities, interests, goals, and backgrounds
- Generates **vivid profile cards** that capture what makes each person unique
- Suggests **thoughtful, non-pushy next steps** to nurture relationships
- Helps you **search and rediscover** connections when you need them

---

## ✨ Key Features

### 🗣️ Conversational Interface
Simply chat about someone you know:
> "I just met Alice at the AI conference. She's working on music generation using transformers..."

The AI understands context and asks follow-up questions when needed.

### 🏷️ Smart Tagging System
Automatically categorizes information into:
- **Personality** traits (e.g., "thoughtful listener", "energetic")
- **Goals** they're working towards (e.g., "launch startup", "learn Japanese")
- **Interests** and hobbies (e.g., "indie music", "hiking")
- **Career/Education** background (e.g., "Stanford CS PhD", "Product Manager")

### 🎴 Dynamic Profile Cards
Each person gets a unique card with:
- **Vivid title** capturing their essence (e.g., "AI Music Hacker Classmate")
- **Rich summary** of your relationship
- **Actionable suggestion** for next contact (e.g., "Send her that new AI music paper you read")
- **All key details** at a glance

### 🔍 Intelligent Search
Find people by asking naturally:
> "Find people interested in Web3" or "Who do I know from Stanford?"

### 📱 Mobile-Optimized
Fully responsive design works beautifully on:
- 📱 Phones (iOS/Android)
- 💻 Tablets (iPad)
- 🖥️ Desktop browsers

---

## 🛠️ Technical Architecture

### Tech Stack

**Frontend:**
- HTML5 + Modern CSS (Glassmorphism design)
- Vanilla JavaScript (no framework overhead)
- Responsive breakpoints: 900px, 640px, 375px

**Backend:**
- FastAPI (Python 3.12+)
- SQLite database for person records
- Uvicorn ASGI server

**AI Framework:**
- **SpoonOS Core Developer Framework (SCDF)** - Advanced agentic OS
- Google **Gemini 2.5 Pro** - Latest multimodal LLM
- Custom ReAct agent with structured output parsing

**Infrastructure:**
- Deployable to: Render.com, Railway, Vercel
- Environment-based configuration
- CORS-enabled API for cross-origin access

### System Flow

```
User Input (Chat) 
    ↓
Frontend JavaScript (index.html)
    ↓
POST /api/spark (FastAPI)
    ↓
RelationshipSparkAgent (SpoonOS)
    ↓
Gemini 2.5 Pro API
    ↓
Structured Output Parsing
    ↓
SQLite Storage + Frontend Update
```

### SpoonOS Integration

This project leverages SpoonOS's powerful features:
- **🧠 ReAct Intelligent Agent** - Reasoning + Action loop
- **💬 Multi-Model Support** - Easy LLM provider switching
- **🔧 Custom Tool Ecosystem** - Extensible tool registration
- **📊 State Management** - Session history and context persistence

---

## 🎨 User Experience Highlights

### Scenario-Based Design
Choose from 5 relationship contexts:
1. **Stay in Touch** - Maintain existing friendships
2. **First Meeting** - Document new connections
3. **Long Time No See** - Rekindle old relationships
4. **Repair Tension** - Navigate conflicts thoughtfully
5. **Uncertain** - Explore ambiguous relationships

### Intelligent Conversation Flow
The agent:
- Detects what information is **missing** (name, contact, etc.)
- Asks **contextual follow-up questions** naturally
- Respects **user's language** (auto-detects English/Chinese)
- Never contradicts what you've explicitly stated

### Visual Design Philosophy
- **Dark mode** optimized for comfort
- **Glassmorphism** aesthetic for modern feel
- **Color-coded tags** for quick scanning
- **Chat bubbles** for natural conversation feel
- **Smooth animations** for polished interactions

---

## 🚀 Demo & Deployment

### 🌐 Live Demo
👉 **[Try U NO HOO](http://127.0.0.1:8000)** *(Update with your deployment URL)*

### 📦 GitHub Repository
👉 **[View Source Code](https://github.com/Fan-Runming/spoon-core)**

### 🎥 Video Walkthrough
*(Optional: Add Loom/YouTube link showing the app in action)*

---

## 🧪 How to Test the Demo

### Quick Start (3 steps):

1️⃣ **Choose a scenario** from the dropdown (e.g., "First Meeting")

2️⃣ **Start chatting** about someone:
```
Example: "I met David at the hackathon last weekend. He's a 
blockchain developer from Singapore working on DeFi protocols. 
Really passionate about decentralization."
```

3️⃣ **Watch the magic happen**:
- AI extracts: name, location, career tags
- Generates: profile card with title "DeFi Builder from SG"
- Suggests: "Share that new Uniswap v4 article with him"

### Advanced Features to Try:

**Add Multiple People:**
- Click "**+ New Person**" button after creating first profile
- Conversation state resets automatically
- All profiles appear in "Recently Added" list

**Search Your Network:**
- Type: "Find people interested in AI"
- Or: "Search blockchain developers"
- Matches appear instantly

**Edit Existing Profiles:**
- Click any mini-card in the right panel
- Continue the conversation to update details
- Agent intelligently merges new information

---

## 💡 Use Cases

### For Individuals:
- 🎓 **Students** - Remember classmates and research collaborators
- 👔 **Professionals** - Build genuine network connections
- 🧳 **Travelers** - Document people met during trips
- 💑 **Social butterflies** - Manage large friend circles

### For Communities:
- 🏢 **Startups** - Team intros and culture building
- 🎤 **Event organizers** - Remember attendees and speakers
- 🏫 **Educators** - Understand students' backgrounds
- 🤝 **Nonprofits** - Donor/volunteer relationship management

---

## 🔮 Future Roadmap

### Phase 1 (Current) ✅
- [x] Conversational person extraction
- [x] Multi-tag categorization
- [x] Profile card generation
- [x] Mobile-responsive UI
- [x] Search functionality

### Phase 2 (Next 3 months)
- [ ] **Photo upload** for profile pictures
- [ ] **Reminder system** for follow-ups
- [ ] **Calendar integration** (Google/Outlook)
- [ ] **Relationship graph visualization**
- [ ] **Export to contacts/CRM**

### Phase 3 (6 months+)
- [ ] **Multi-user support** with privacy controls
- [ ] **Collaborative networks** (shared contacts)
- [ ] **AI-suggested introductions** (connect mutual friends)
- [ ] **Sentiment analysis** for relationship health tracking
- [ ] **Voice input** for hands-free updates

---

## 🏆 What Makes This Special

### 🎯 Human-Centric Design
Unlike traditional CRMs that treat people as "leads" or "prospects", U NO HOO focuses on **authentic relationship building**. No sales funnels, no conversion tracking—just genuine connections.

### 🧠 AI That Understands Context
Powered by Gemini 2.5 Pro and SpoonOS's agentic architecture, the system doesn't just extract keywords—it **understands nuance**, asks **clarifying questions**, and generates **personalized insights**.

### 🚀 Built on SpoonOS Framework
Leverages a **production-grade AI agent framework** designed for:
- Web3 interoperability
- Multi-model flexibility
- Extensible tool ecosystem
- Enterprise-scale reliability

### 📱 Seamless Mobile Experience
Not an afterthought—the mobile UI is **carefully optimized** with:
- Touch-friendly button sizes (42px minimum)
- Optimized chat window heights
- Vertical stacking layout
- Readable typography at all screen sizes

---

## 🎓 What We Learned

### Technical Insights:
1. **Structured output parsing** from LLMs requires careful prompt engineering
2. **State management** in conversational UIs is non-trivial (solved with explicit reset mechanisms)
3. **Mobile-first design** dramatically improves overall UX
4. **SpoonOS framework** accelerates AI agent development significantly

### Design Insights:
1. People prefer **conversation over forms** for data entry
2. **Visual tags** make information scanning 10x faster
3. **Actionable suggestions** turn passive records into active relationship building
4. **Dark mode + glassmorphism** resonates with modern users

### Product Insights:
1. **Scenario-based framing** helps users think about relationships contextually
2. **"New Person" button** is critical for multi-entry workflows
3. **Search by natural language** feels magical compared to filters
4. **Less is more** - focus on core features rather than feature bloat

---

## 👥 Team

**Your Name/Team Name**
- Project Lead & Full-Stack Developer
- AI Agent Design & Implementation
- UX/UI Design

*(Add team member names and roles if applicable)*

---

## 📞 Contact & Links

- 📧 Email: your-email@example.com
- 🐙 GitHub: [@Fan-Runming](https://github.com/Fan-Runming)
- 🔗 LinkedIn: your-linkedin-profile
- 🌐 Demo: your-deployment-url

---

## 📜 License

This project is built on **SpoonOS Core Developer Framework**, which is open source.  
U NO HOO application code is available under [specify license].

---

## 🙏 Acknowledgments

- **SpoonOS Team** - For the incredible AI agent framework
- **Google** - For Gemini 2.5 Pro API access
- **Open Source Community** - For the tools and libraries that made this possible

---

## 📸 Screenshots

*(Add 3-5 key screenshots showing:)*
1. Main chat interface with conversation
2. Generated profile card with tags
3. People list with mini-cards
4. Mobile responsive view
5. Search functionality in action

---

## 🎬 How to Run Locally

```bash
# Clone the repository
git clone https://github.com/Fan-Runming/spoon-core.git
cd spoon-core

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Add your GEMINI_API_KEY to .env

# Run the server
uvicorn main:app --reload --port 8000

# Open in browser
# Visit: http://127.0.0.1:8000
```

---

**Built with ❤️ using SpoonOS**

*Remember: Technology should bring people closer, not replace human connection. U NO HOO is a tool to help you nurture relationships, not a substitute for genuine care.*
