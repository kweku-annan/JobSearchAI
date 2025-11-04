# JobSearchAI - AI-Powered Job Search & Portfolio Recommendation Agent

## Overview

JobInsightAI is an intelligent career assistant that helps job seekers stand out in competitive markets. It searches for job listings and recommends tailored portfolio projects that demonstrate the exact skills employers are looking for.

Built for the HNG Internship Stage 3 Backend Task, this agent integrates with Telex.im using the A2A (Agent-to-Agent) protocol.

## What It Does

- **Job Search**: Finds relevant job listings based on job titles you're interested in
- **Smart Analysis**: Extracts key skills and requirements from job postings
- **Portfolio Recommendations**: Suggests 3 specific, buildable projects that prove you have the skills
- **Flexible Input**: Works with cached job data or allows you to paste custom job descriptions
- **AI-Powered**: Uses Google Gemini AI to generate intelligent, tailored recommendations

## Features

### Core Functionality
- Natural language job search (e.g., "software engineer jobs", "looking for backend developer roles")
- Intelligent job title extraction from conversational queries
- Database caching for faster responses and reduced API calls
- Multi-API integration with fallback mechanisms for reliability
- HTML tag cleaning from job descriptions
- Language handling (responds in English regardless of input language)

### AI Recommendations
Each job search returns:
- Job title and company
- Required skills and technologies
- Brief job description
- 3 tailored portfolio project ideas with:
  - Specific project names
  - Detailed descriptions
  - Technologies to use
  - How it demonstrates job requirements
  - Estimated completion time (1-3 weeks)

### Fallback Mode
When no jobs are found in the database, users can paste a full job description for instant analysis and recommendations.

## Tech Stack

**Backend Framework**
- Python 3.11+
- Flask (Web framework)
- Gunicorn (Production server)

**Database**
- SQLAlchemy (ORM)
- SQLite (Local development and caching)

**AI/ML**
- Google Generative AI (Gemini 1.5 Flash)

**External APIs**
- Arbeitnow API (Job listings)
- Findwork.dev API (Job listings backup)

**Deployment**
- Railway (Cloud platform)

**Other Tools**
- python-dotenv (Environment management)
- Requests (HTTP client)

## Architecture

### High-Level Flow
```
User Message → Telex.im → A2A Protocol → Flask Webhook
    ↓
Extract Job Title → Query Database (with caching)
    ↓
If Found: Retrieve Jobs → Pick First Job → Generate Recommendations
    ↓
If Not Found: Prompt User to Paste Job Description
    ↓
Format Response → Return to Telex → Display to User
```

### Key Components
- **Agent Handler**: Processes incoming messages and routes requests
- **Job Service**: Manages job data fetching and caching
- **LLM Service**: Interfaces with Google Gemini for AI recommendations
- **Adapters**: Abstraction layer for multiple job APIs
- **Formatters**: Creates user-friendly response messages

## Environment Variables

Required environment variables for the application:
```
GEMINI_API_KEY=your_google_gemini_api_key
PORT=5000
```

Optional (if using authenticated job APIs):
```
JOB_API_KEY_1=your_job_api_key
JOB_API_KEY_2=your_backup_api_key
```

## Installation & Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**
```bash
   git clone <your-repo-url>
   cd jobinsightai
```

2. **Create virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
   - Create a `.env` file in the root directory
   - Add your API keys (see Environment Variables section)

5. **Initialize the database**
```bash
   python -c "from models.database import init_db; init_db()"
```

6. **Run the application**
```bash
   python app.py
```

   The server will start at `http://localhost:5000`

### Testing Locally

**Health check:**
```bash
curl http://localhost:5000/health
```

**Test the agent:**
```bash
curl -X POST http://localhost:5000/a2a/jobsearchai \
  -H "Content-Type: application/json" \
  -d '{"params": {"message": {"parts": [{"kind": "text", "text": "python developer"}]}}}'
```

## Deployment

### Deploying to Railway

1. **Create Railway Account**
   - Sign up at https://railway.app

2. **Create New Project**
   - Click "New Project"
   - Choose "Deploy from GitHub repo"
   - Select your repository

3. **Configure Environment Variables**
   - Go to project settings → Variables
   - Add `GEMINI_API_KEY`
   - Railway automatically sets `PORT`

4. **Configure Start Command** (if needed)
   - Railway auto-detects Python apps
   - Or manually set: `gunicorn app:app --timeout 120 --bind 0.0.0.0:$PORT`

5. **Deploy**
   - Railway automatically deploys on push to main branch
   - Get your public URL from the deployment

6. **Verify Deployment**
   - Visit `https://your-app.up.railway.app/health`
   - Should return `{"status": "healthy"}`

## Telex.im Integration

### A2A Protocol

This agent uses the A2A (Agent-to-Agent) protocol to communicate with Telex.im.

**Endpoint**: `/a2a/jobsearchai`

**Request Format** (from Telex):
The agent receives JSON-RPC formatted requests with nested message structures containing conversation history and the latest user message.

**Response Format** (to Telex):
Returns JSON-RPC responses with structured message parts that Telex renders in the UI.

### Registering the Agent

1. **Get Telex Access**
   - Use `/telex-invite your-email@example.com` command
   - Accept the invitation

2. **Create Workflow JSON**
   - Use the workflow configuration with your Railway URL
   - Set appropriate agent descriptions and behavior

3. **Submit to Telex**
   - Register your agent through the Telex platform
   - Test in the Telex UI

4. **Monitor Agent Logs**
   - View interactions at: `https://api.telex.im/agent-logs/{channel-id}.txt`
   - Channel ID found in Telex conversation URL

## Usage Examples

### Example 1: Basic Job Search
```
User: "software engineer jobs"

Agent Response:
🎯 Found 5 software engineer positions!

✨ Recommended Portfolio Projects:
(Based on: Backend Engineer at TechCorp)

1. 🚀 Microservices API Gateway
   • Build a scalable API gateway handling authentication, rate limiting, and routing
   • Stack: Python, FastAPI, Redis, Docker
   • Shows: System design, API development, scalability
   • Time: 2-3 weeks

[... 2 more projects ...]

📋 Available Positions:
1. Backend Engineer @ TechCorp
   💼 Skills: Python, FastAPI, PostgreSQL, Docker
   
[... 4 more jobs ...]
```

### Example 2: No Results - Fallback
```
User: "quantum computing engineer"

Agent Response:
🔍 No cached jobs found for "quantum computing engineer".

📝 But I can still help!

Paste a job description and I'll analyze it to recommend portfolio projects 
that will make you stand out.
```

### Example 3: Custom Job Description
```
User: [Pastes full job description]

Agent Response:
📋 Analyzing the job description...

Key Requirements Identified:
- React, TypeScript, Node.js
- REST APIs, GraphQL
- Testing (Jest, Cypress)

✨ Recommended Portfolio Projects:
[... tailored recommendations ...]
```

## API Endpoints

### `GET /`
Returns basic agent information and usage instructions.

### `GET /health`
Health check endpoint for monitoring.

**Response:**
```json
{
  "status": "healthy",
  "service": "JobInsightAI"
}
```

### `POST /a2a/jobsearchai`
Main webhook endpoint for Telex A2A protocol.

Accepts JSON-RPC formatted requests and returns structured responses.

## Project Structure
```
jobinsightai/
├── agent/
│   ├── handler.py          # Main message processing logic
│   └── intent_detector.py  # Job title extraction
├── services/
│   ├── job_service.py      # Job fetching and caching
│   ├── llm_service.py      # Google Gemini integration
│   └── recommendation_service.py  # Recommendation generation
├── adapters/
│   ├── base.py            # Abstract adapter interface
│   ├── arbeitnow.py       # Arbeitnow API adapter
│   └── findwork.py        # Findwork API adapter
├── models/
│   └── database.py        # SQLAlchemy models and setup
├── utils/
│   ├── cache.py           # Caching utilities
│   └── formatters.py      # Response formatting
├── app.py                 # Flask application entry point
├── config.py              # Configuration management
├── requirements.txt       # Python dependencies
├── Procfile              # Railway deployment config
├── .env.example          # Environment variables template
└── README.md             # This file
```

## Key Design Decisions

### Caching Strategy
Jobs are cached in SQLite with a 24-hour expiration. This reduces API calls, improves response time, and provides fallback when external APIs fail.

### API Fallback Chain
The system tries multiple job APIs in sequence. If the primary fails, it automatically attempts backup APIs before giving up.

### LLM Selection
Google Gemini was chosen for its generous free tier, no billing requirement, and good performance on structured output tasks.

### First Job Analysis
To manage costs and response time, recommendations are generated for the first job in results rather than all jobs. This provides value while keeping the system fast and affordable.

### Error Handling Philosophy
The agent never completely fails. If one component fails (LLM, database, API), it gracefully degrades and provides partial results or helpful fallback messages.

## Known Limitations & Future Improvements

### Current Limitations
- Recommendations based on first job only (not all returned jobs)
- Limited to text-based jobs (no PDF parsing)
- No user profile/preference persistence across sessions
- No job application tracking
- Basic job title matching (no advanced NLP)

### Planned Improvements
- Job-specific recommendations for each listing
- User profile creation with skill tracking
- Resume analysis and gap identification
- Direct application link integration
- Advanced search with filters (location, salary, experience)
- Difficulty ratings for recommended projects
- Tutorial/resource links for each project
- Multi-language support for job descriptions
- Integration with GitHub to check existing projects
- Automated follow-up reminders

## Troubleshooting

### Common Issues

**Issue: "Please provide a job title" keeps appearing**
- Solution: Ensure message extraction is working correctly. Check Railway logs for extracted message.

**Issue: Worker timeout errors**
- Solution: Increase Gunicorn timeout in Procfile: `--timeout 120`

**Issue: No recommendations generated**
- Solution: Verify GEMINI_API_KEY is set correctly in Railway environment variables.

**Issue: Database errors on Railway**
- Solution: SQLite file system is ephemeral on Railway. Data resets on deployment. Consider PostgreSQL for persistence.

**Issue: Agent not responding in Telex**
- Solution: Check agent logs at Telex logs URL. Verify JSON-RPC response format is correct.

## Performance Considerations

- **Average Response Time**: 3-8 seconds (depending on LLM response time)
- **Cache Hit Response Time**: < 1 second
- **API Call Optimization**: Caching reduces external API calls by ~80%
- **Token Usage**: ~500-800 tokens per request (affordable with free tier)
- **Concurrent Users**: Supports multiple users via Gunicorn worker processes

## Contributing

This project was built as part of the HNG Internship Stage 3 Backend Task. 

If you'd like to contribute or use this as a base for your own project:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available for educational purposes.

## Acknowledgments

- **HNG Internship** for the opportunity and challenge
- **Telex.im** for the A2A protocol and platform
- **Google** for Gemini API access
- **Railway** for free deployment hosting
- Job API providers (Arbeitnow, Findwork.dev)

## Contact & Links

- **Project Repository**: [https://github.com/kweku-annan/JobSearchAI]
- **Live Demo**: [https://jobsearchai-production.up.railway.app/a2a/jobsearchai]
- **Blog Post**: [https://dev.to/kweku_annan/building-jobinsightai-an-intelligent-telex-agent-for-career-growth-hng-stage-3-backend-task-1pa6]
- **HNG Internship**: https://hng.tech/internship
- **Telex.im**: https://telex.im

---

Built with ❤️ for HNG Internship Stage 3 Backend Task